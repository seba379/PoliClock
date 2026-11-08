"""FIN-008: vie di cucitura GND fra i piani F.Cu e B.Cu, lungo il contorno e vicino all'intaglio dell'antenna.

Uso (Python di KiCad 10, dopo lo sbroglio):
  "C:/Program Files/KiCad/10.0/bin/python.exe" hardware/scripts/cucitura_gnd.py

- vie 0,6/0,3 mm a GND ogni ~4 mm, rientrate di 1,3 mm dal contorno (fuori dalla fascia di 0,45 mm senza vie);
- niente vie nella zona USB (J1, U1, R3/R4, coppia D+/D-: DEC-041), sotto il modulo U3 (solo le 4 vie della EPAD,
  gia' nell'impronta), nelle zone vietate (antenna, fiducial, retro della coppia USB) e nei courtyard dei componenti;
- distanza >= 0,25 mm dal rame di altre reti e >= 0,3 mm foro-rame / 0,3 mm foro-foro (piu' severo delle regole);
- dopo il riempimento dei piani si tengono solo le vie collegate al GND su entrambi gli strati.
Le vie di cucitura gia' presenti (nome "cucitura" nel campo di gruppo) vengono tolte e rifatte.
"""
import os
import pcbnew

HERE = os.path.dirname(os.path.abspath(__file__))
PCB = os.path.join(os.path.dirname(HERE), "policlock-main", "policlock-main.kicad_pcb")
MM = pcbnew.FromMM
T = pcbnew.ToMM
INSET, PASSO = 1.3, 4.0
ZONA_USB = (127.5, 119.0, 140.2, 141.0)       # x0, y0, x1, y1 (mm, coordinate del foglio)

board = pcbnew.LoadBoard(PCB)
cestino = []
gnd = board.FindNet("GND")

# contorno (segmenti ortogonali)
edges = []
for s in board.GetDrawings():
    if s.GetLayer() == pcbnew.Edge_Cuts and s.GetShape() == pcbnew.SHAPE_T_SEGMENT:
        edges.append((T(s.GetStart().x), T(s.GetStart().y), T(s.GetEnd().x), T(s.GetEnd().y)))
poly = pcbnew.SHAPE_POLY_SET()
board.GetBoardPolygonOutlines(poly, False)


def dentro(x, y, margine):
    p = pcbnew.VECTOR2I(MM(x), MM(y))
    if not poly.Contains(p):
        return False
    for ax, ay, bx, by in edges:
        if pcbnew.SEG(pcbnew.VECTOR2I(MM(ax), MM(ay)), pcbnew.VECTOR2I(MM(bx), MM(by))).Distance(p) < MM(margine):
            return False
    return True


# candidati: per ogni lato, punti ogni PASSO mm rientrati di INSET verso l'interno
cand = []
for ax, ay, bx, by in edges:
    L = ((bx - ax) ** 2 + (by - ay) ** 2) ** 0.5
    n = max(1, int(L // PASSO))
    ux, uy = (bx - ax) / L, (by - ay) / L
    for k in range(n + 1):
        px, py = ax + ux * L * k / n, ay + uy * L * k / n
        for sx, sy in ((-uy, ux), (uy, -ux)):            # una delle due normali punta all'interno
            qx, qy = px + sx * INSET, py + sy * INSET
            if dentro(qx, qy, INSET - 0.01):
                cand.append((round(qx, 3), round(qy, 3)))

# rifai da capo le vie di cucitura precedenti
for t in list(board.GetTracks()):
    if t.GetClass() == "PCB_VIA" and t.GetNetCode() == gnd.GetNetCode() and t.GetParentGroup() is not None \
            and t.GetParentGroup().GetName() == "cucitura":
        board.Remove(t)
        cestino.append(t)
for g in list(board.Groups()):
    if g.GetName() == "cucitura":
        board.Remove(g)
        cestino.append(g)

vietate = [z for z in board.Zones() if z.GetIsRuleArea() and z.GetDoNotAllowVias()]
for fp in board.GetFootprints():
    vietate += [z for z in fp.Zones() if z.GetIsRuleArea() and z.GetDoNotAllowVias()]
cy = []
for fp in board.GetFootprints():
    c = fp.GetCourtyard(pcbnew.F_CrtYd)
    if c.OutlineCount():
        cy.append(c)
rame = [o for o in list(board.GetTracks()) + list(board.GetPads())]
fori = [o for o in board.GetPads() if o.HasHole()] + [t for t in board.GetTracks() if t.GetClass() == "PCB_VIA"]

gruppo = pcbnew.PCB_GROUP(board)
gruppo.SetName("cucitura")
board.Add(gruppo)
messe = []
for x, y in cand:
    if ZONA_USB[0] <= x <= ZONA_USB[2] and ZONA_USB[1] <= y <= ZONA_USB[3]:
        continue
    p = pcbnew.VECTOR2I(MM(x), MM(y))
    if any(z.Outline().Contains(p) or z.Outline().Collide(p, MM(0.35)) for z in vietate):
        continue
    if any(c.Collide(p, MM(0.3)) for c in cy):
        continue
    if any(abs(mx - x) < 2.0 and abs(my - y) < 2.0 for mx, my in messe):
        continue
    v = pcbnew.PCB_VIA(board)
    v.SetPosition(p)
    v.SetWidth(MM(0.6))
    v.SetDrill(MM(0.3))
    v.SetNet(gnd)
    ok = True
    for lay in (pcbnew.F_Cu, pcbnew.B_Cu):
        sh = v.GetEffectiveShape(lay)
        for o in rame:
            if o.GetNetCode() != gnd.GetNetCode() and o.IsOnLayer(lay) and sh.Collide(o.GetEffectiveShape(lay), MM(0.25)):
                ok = False
                break
        if not ok:
            break
    hole = pcbnew.SHAPE_CIRCLE(p, MM(0.15))
    if ok:
        for o in rame:
            if o.GetNetCode() == gnd.GetNetCode():
                continue
            for lay in (pcbnew.F_Cu, pcbnew.B_Cu):
                if o.IsOnLayer(lay) and o.GetEffectiveShape(lay).Collide(hole, MM(0.3)):
                    ok = False
    if ok:
        for o in fori:
            if (o.GetPosition() - p).EuclideanNorm() < MM(0.15 + 0.3 + 0.5):
                ok = False
    if not ok:
        continue
    board.Add(v)
    gruppo.AddItem(v)
    messe.append((x, y))

# riempimento e verifica: tengo solo le vie collegate al piano GND su entrambi gli strati
filler = pcbnew.ZONE_FILLER(board)
filler.Fill(board.Zones())
piani = {lay: [z for z in board.Zones() if not z.GetIsRuleArea() and z.GetNetCode() == gnd.GetNetCode()
               and z.IsOnLayer(lay)] for lay in (pcbnew.F_Cu, pcbnew.B_Cu)}
tolte = 0
for v in [t for t in board.GetTracks() if t.GetClass() == "PCB_VIA" and t.GetParentGroup() is not None
          and t.GetParentGroup().GetName() == "cucitura"]:
    if not all(any(z.HitTestFilledArea(lay, v.GetPosition()) for z in piani[lay]) for lay in piani):
        board.Remove(v)
        cestino.append(v)
        tolte += 1
filler.Fill(board.Zones())
board.Save(PCB)
print("candidati", len(cand), "vie messe", len(messe) - tolte, "(tolte perche' non collegate:", tolte, ")")
