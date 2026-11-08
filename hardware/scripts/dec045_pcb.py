"""DEC-045: scheda rettangolare senza intaglio, antenna di U3 sulla scheda con zona vietata, regola JLC dei 2,5 mm
corpo-bordo per tutte le parti montate da JLC tranne J1.

Modifica una tantum del .kicad_pcb (Python di KiCad 10):
  "C:/Program Files/KiCad/10.0/bin/python.exe" hardware/scripts/dec045_pcb.py
  "C:/Program Files/KiCad/10.0/bin/python.exe" hardware/scripts/sbroglia_main.py --conserva
  "C:/Program Files/KiCad/10.0/bin/python.exe" hardware/scripts/cucitura_gnd.py

- angolo in basso a sinistra fisso (100; 140): J1, H1/H2, coppia USB (DEC-041) e origine della CPL non si muovono;
- U3 non si muove (pin 13/14 sull'asse di J1); il contorno cresce solo verso destra e verso l'alto quanto basta:
  corpo di U3 (F.Fab) da x 127,51 a 147,51 e da y 101,5 a 119,5 -> bordo destro a 150,5 (margine 2,99 mm),
  bordo superiore a 98,5 (margine 3,0 mm: con 1,0 mm in piu' il margine sarebbe 2,50 mm esatti, senza tolleranza
  sulle dimensioni del modulo);
- la zona vietata dell'impronta di U3 (tutto il rame, piste, vie, riempimenti, piazzole e componenti) copre ora
  la scheda da x 141,51 al bordo destro e da y 98,5 a 124,5: antenna sulla scheda senza rame sotto e attorno;
- J2 sale di 1,5 mm con il nuovo bordo superiore (i piedini dell'header a 90 gradi restano oltre il bordo);
  si tolgono le piste delle sue reti, poi si risbrogliano solo le connessioni mancanti;
- i piani GND seguono il nuovo contorno; le fasce "bordo" le rifa' sbroglia_main.py.

Ritocchi fatti dopo il primo sbroglio (2026-11-08): LCD_MOSI_C e LCD_CS erano uscite lunghe (58 e 41 mm): tolte insieme
alle piste GND aggiunte da Freerouting in quel passaggio e risbrogliate con --conserva (33 mm con 4 vie e 48 mm);
pista LCD_SCLK_C fra le piazzole di C5 riportata a 0,15 mm; via GND a (112,4; 104,3) per il raccordo di J2 pin 2
sul retro (isola di piano altrimenti "starved"); poi cucitura_gnd.py.
"""
import os
import pcbnew

HERE = os.path.dirname(os.path.abspath(__file__))
PCB = os.path.join(os.path.dirname(HERE), "policlock-main", "policlock-main.kicad_pcb")
MM = pcbnew.FromMM
T = pcbnew.ToMM
X0, Y0, X1, Y1 = 100.0, 98.5, 150.5, 140.0       # nuovo contorno (mm, coordinate del foglio)
DY_J2 = -1.5
RETI_J2 = {"3V3_DISP", "LCD_SCLK_C", "LCD_MOSI_C", "LCD_DC", "LCD_CS", "LCD_RST"}

board = pcbnew.LoadBoard(PCB)
cestino = []


def V(x, y):
    return pcbnew.VECTOR2I(MM(x), MM(y))


# contorno: rettangolo senza intaglio
for s in list(board.GetDrawings()):
    if s.GetLayer() == pcbnew.Edge_Cuts:
        board.Remove(s)
        cestino.append(s)
for a, b in (((X0, Y0), (X1, Y0)), ((X1, Y0), (X1, Y1)), ((X1, Y1), (X0, Y1)), ((X0, Y1), (X0, Y0))):
    e = pcbnew.PCB_SHAPE(board, pcbnew.SHAPE_T_SEGMENT)
    e.SetLayer(pcbnew.Edge_Cuts)
    e.SetStart(V(*a))
    e.SetEnd(V(*b))
    e.SetWidth(MM(0.05))
    board.Add(e)

# piani GND sul nuovo contorno; via le fasce "bordo" (le rifa' lo sbroglio dal contorno)
for z in list(board.Zones()):
    if z.GetZoneName() == "bordo":
        board.Remove(z)
        cestino.append(z)
    elif not z.GetIsRuleArea() and z.GetNetname() == "GND":
        ol = z.Outline()
        ol.RemoveAllContours()
        ol.NewOutline()
        for x, y in ((X0, Y0), (X1, Y0), (X1, Y1), (X0, Y1)):
            ol.Append(V(x, y))

# J2 sul nuovo bordo superiore e piste delle sue reti da rifare
j2 = board.FindFootprintByReference("J2")
vecchie = [(p.GetNetCode(), p.GetPosition()) for p in j2.Pads()]
j2.Move(V(0, DY_J2))
for t in list(board.GetTracks()):
    if t.IsLocked():
        continue
    nome = t.GetNetname().split("/")[-1]
    estremi = [t.GetPosition()] if t.GetClass() == "PCB_VIA" else [t.GetStart(), t.GetEnd()]
    if nome in RETI_J2 or any(n == t.GetNetCode() and (e - p).EuclideanNorm() < MM(0.05)
                              for n, p in vecchie for e in estremi):
        board.Remove(t)
        cestino.append(t)
    else:
        # piste di altre reti che ora toccano le piazzole spostate di J2
        for p in j2.Pads():
            if p.GetNetCode() != t.GetNetCode() and any(
                    t.IsOnLayer(l) and t.GetEffectiveShape(l).Collide(p.GetEffectiveShape(l), MM(0.2))
                    for l in (pcbnew.F_Cu, pcbnew.B_Cu)):
                board.Remove(t)
                cestino.append(t)
                break

board.Save(PCB)
u3 = board.FindFootprintByReference("U3")
print("contorno", X1 - X0, "x", Y1 - Y0, "mm | U3 a", T(u3.GetPosition().x), T(u3.GetPosition().y))
