"""Posizionamento della scheda principale (policlock-main.kicad_pcb), rev 0.2.

Da eseguire con il Python di KiCad 10:
  "C:/Program Files/KiCad/10.0/bin/python.exe" hardware/scripts/genera_pcb_main.py

Legge la netlist esportata dallo schema (policlock-main.net), carica i footprint, assegna le net,
posiziona i componenti (tabelle in posizioni_main.py), disegna contorno con intaglio per l'antenna,
fori, piani GND, zona antenna senza rame, legenda sul retro e regole JLCPCB; riabilita i controlli
DRC su courtyard e footprint. Lo sbroglio si fa poi con sbroglia_main.py.
Dopo la prima modifica manuale in KiCad il file .kicad_pcb diventa la fonte: non rieseguire.
"""
import json
import os
import sys
import pcbnew

HERE = os.path.dirname(os.path.abspath(__file__))
HW = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from sexp import parse, find, find1  # noqa: E402
from posizioni_main import (PLACE, W, H, HOLES, AUTO_ORDER, BOTTOM, ANCHOR, OUTLINE, NOTCH,  # noqa: E402
                            ANT_KEEPOUT, SIDE_MARGIN, FIDUCIALS, USB_FREE)
import usb_coppia  # noqa: E402

PRJ = os.path.join(HW, "policlock-main")
NET = os.path.join(PRJ, "policlock-main.net")
OUT = os.path.join(PRJ, "policlock-main.kicad_pcb")
PRO = os.path.join(PRJ, "policlock-main.kicad_pro")
STD = "C:/Program Files/KiCad/10.0/share/kicad/footprints"
LOCAL = os.path.join(HW, "lib", "PoliClock.pretty")

MM = pcbnew.FromMM
OX, OY = 100.0, 100.0          # origine della scheda nel foglio
GAP = float(os.environ.get("PCB_GAP", "0.5"))   # spazio extra fra i courtyard per lo sbroglio (mm)
EDGE = 0.4                      # solo ritaglio della serigrafia; i componenti usano SIDE_MARGIN su tutti i bordi


def V(x, y):
    return pcbnew.VECTOR2I(MM(OX + x), MM(OY + y))


def local_bbox(fp):
    """Courtyard unito alle piazzole (+0,25 mm), footprint non ruotato, in mm relativi all'origine."""
    fp.SetOrientationDegrees(0)
    fp.SetPosition(pcbnew.VECTOR2I(0, 0))
    fp.BuildCourtyardCaches()
    cy = fp.GetCourtyard(pcbnew.F_CrtYd)
    bb = cy.BBox() if cy.OutlineCount() else fp.GetBoundingBox(False)
    b = [pcbnew.ToMM(bb.GetLeft()), pcbnew.ToMM(bb.GetRight()), pcbnew.ToMM(bb.GetTop()), pcbnew.ToMM(bb.GetBottom())]
    for pad in fp.Pads():
        pb = pad.GetBoundingBox()
        b[0] = min(b[0], pcbnew.ToMM(pb.GetLeft()) - 0.25)
        b[1] = max(b[1], pcbnew.ToMM(pb.GetRight()) + 0.25)
        b[2] = min(b[2], pcbnew.ToMM(pb.GetTop()) - 0.25)
        b[3] = max(b[3], pcbnew.ToMM(pb.GetBottom()) + 0.25)
    return tuple(b)


def rot_bbox(b, rot):
    x0, x1, y0, y1 = b
    if rot == 90:
        return (y0, y1, -x1, -x0)
    if rot == 180:
        return (-x1, -x0, -y1, -y0)
    if rot == 270:
        return (-y1, -y0, x0, x1)
    return b


def overlap(a, b, gap=0.0):
    return not (a[1] + gap <= b[0] or b[1] + gap <= a[0] or a[3] + gap <= b[2] or b[3] + gap <= a[2])


def inside_board(r, m=EDGE, side=None):
    """r in coordinate scheda; m e side sono i margini su tutti i bordi e sui lati."""
    sm = m if side is None else side
    if r[0] < sm or r[1] > W - sm or r[2] < m or r[3] > H - m:
        return False
    nx0, ny0, nx1, ny1 = NOTCH
    return not overlap(r, (nx0 - m, nx1, ny0, ny1 + m))


def load_netlist():
    root = parse(open(NET, encoding="utf-8").read())[0]
    comps = {}
    for c in find(find1(root, "components"), "comp"):
        ref = find1(c, "ref")[1]
        comps[ref] = {"fp": find1(c, "footprint")[1], "value": find1(c, "value")[1],
                      "fields": {find1(f, "name")[1]: (f[-1] if isinstance(f[-1], str) else "")
                                 for f in find(find1(c, "fields") or [], "field")},
                      "dnp": any(p[1] == "dnp" for p in find(c, "property")),
                      "props": {find1(p, "name")[1]: (find1(p, "value") or [None, ""])[1] for p in find(c, "property")},
                      "path": find1(find1(c, "sheetpath"), "tstamps")[1] + find1(c, "tstamps")[1]}
    pads = {}
    for n in find(find1(root, "nets"), "net"):
        name = find1(n, "name")[1]
        for node in find(n, "node"):
            pads[(find1(node, "ref")[1], find1(node, "pin")[1])] = name
    return comps, pads


def load_fp(fpid):
    lib, name = fpid.split(":")
    path = LOCAL if lib == "PoliClock" else f"{STD}/{lib}.pretty"
    fp = pcbnew.FootprintLoad(path, name)
    fp.SetFPID(pcbnew.LIB_ID(lib, name))
    return fp


def poly(points):
    ps = pcbnew.SHAPE_POLY_SET()
    ps.NewOutline()
    for x, y in points:
        ps.Append(MM(OX + x), MM(OY + y))
    return ps


LBOX = {}


def build():
    comps, pads = load_netlist()
    board = pcbnew.BOARD()
    board.SetCopperLayerCount(2)
    ds = board.GetDesignSettings()
    # Regole compatibili JLCPCB 2 strati (con margine sui minimi del produttore)
    ds.m_MinClearance = MM(0.1)          # minimo JLC; la classe di default usa 0,15 mm
    ds.m_TrackMinWidth = MM(0.15)
    ds.m_ViasMinSize = MM(0.6)
    ds.m_ViasMinAnnularWidth = MM(0.15)
    ds.m_MinThroughDrill = MM(0.3)
    ds.m_HoleClearance = MM(0.3)         # JLC: foro-pista >= 0,28 mm
    ds.m_HoleToHoleMin = MM(0.25)        # JLC: foro-foro delle vie >= 0,2 mm
    ds.m_CopperEdgeClearance = MM(0.3)
    ds.m_SilkClearance = MM(0.1)
    ds.SetBoardThickness(MM(1.6))
    ds.SetAuxOrigin(V(0, H))              # origine di foratura/CPL: angolo in basso a sinistra
    nc = ds.m_NetSettings.GetDefaultNetclass()
    nc.SetClearance(MM(0.15))
    nc.SetTrackWidth(MM(0.2))
    nc.SetViaDiameter(MM(0.6))
    nc.SetViaDrill(MM(0.3))

    netcodes = {}
    for name in sorted(set(pads.values())):
        ni = pcbnew.NETINFO_ITEM(board, name)
        board.Add(ni)
        netcodes[name] = ni

    for ref, c in comps.items():
        fp = load_fp(c["fp"])
        fp.SetReference(ref)
        fp.SetValue(c["value"])
        # campi come in "Aggiorna PCB dallo schema": tutti i campi del simbolo (tranne Footprint), foglio, percorso
        for name, val in c["fields"].items():
            if name != "Footprint":
                fp.SetField(name, val)
        for name in ("Sheetname", "Sheetfile"):
            if name in c["props"]:
                fp.SetField(name, c["props"][name])
        fp.SetPath(pcbnew.KIID_PATH(c["path"]))
        LBOX[ref] = local_bbox(fp)
        # serigrafia: riferimenti sul disegno di assemblaggio (F.Fab), valori e campi nascosti
        fp.Value().SetVisible(False)
        for fld in fp.GetFields():
            if fld.GetName() not in ("Reference", "Value"):
                fld.SetVisible(False)
        fp.Reference().SetLayer(pcbnew.F_Fab)
        fp.Reference().SetTextSize(pcbnew.VECTOR2I(MM(0.5), MM(0.5)))
        fp.Reference().SetTextThickness(MM(0.08))
        for item in list(fp.GraphicalItems()):
            if isinstance(item, pcbnew.PCB_TEXT) and item.GetLayer() == pcbnew.F_SilkS:
                item.SetLayer(pcbnew.F_Fab)
        board.Add(fp)
        for pad in fp.Pads():
            key = (ref, pad.GetNumber())
            if key in pads:
                pad.SetNet(netcodes[pads[key]])
        if ref in PLACE:
            x, y, rot, side = PLACE[ref]
            if side == "B":
                fp.Flip(fp.GetPosition(), pcbnew.FLIP_DIRECTION_TOP_BOTTOM)
            fp.SetOrientationDegrees(rot)
            fp.SetPosition(V(x, y))

    fps = {f.GetReference(): f for f in board.GetFootprints()}

    # ------------------------------------------------ piazzamento automatico vicino ai pin
    occ = {"F": [], "B": []}
    for ref, (x, y, rot, side) in PLACE.items():
        b = rot_bbox(LBOX[ref], rot)
        r = (x + b[0], x + b[1], y + b[2], y + b[3])
        occ[side].append((ref, r))
        if any(p.GetAttribute() in (pcbnew.PAD_ATTRIB_PTH, pcbnew.PAD_ATTRIB_NPTH) for p in fps[ref].Pads()):
            occ["B" if side == "F" else "F"].append((ref, r))
    for hx, hy in HOLES:
        r = (hx - 2.6, hx + 2.6, hy - 2.6, hy + 2.6)
        occ["F"].append(("H", r))
        occ["B"].append(("H", r))
    for fx, fy in FIDUCIALS:
        r = (fx - 1.5, fx + 1.5, fy - 1.5, fy + 1.5)
        occ["F"].append(("FID", r))
    kx0, ky0, kx1, ky1 = ANT_KEEPOUT
    occ["F"].append(("ANT", (kx0, kx1, ky0, ky1)))
    for r in USB_FREE:
        occ["F"].append(("USB", r))
    occ["B"].append(("ANT", (kx0, kx1, ky0, ky1)))
    placed = set(PLACE)
    failed = []
    for ref in AUTO_ORDER:
        f = fps[ref]
        side = "B" if ref in BOTTOM else "F"
        if ref in ANCHOR:
            aref, apin = ANCHOR[ref]
            pad = [p for p in fps[aref].Pads() if p.GetNumber() == apin][0]
            tx, ty = pcbnew.ToMM(pad.GetPosition().x) - OX, pcbnew.ToMM(pad.GetPosition().y) - OY
        else:
            nets = {p.GetNetname() for p in f.Pads()} - {""}
            pts = [p.GetPosition() for o in placed for p in fps[o].Pads() if p.GetNetname() in nets]
            tx = sum(pcbnew.ToMM(p.x) - OX for p in pts) / len(pts)
            ty = sum(pcbnew.ToMM(p.y) - OY for p in pts) / len(pts)
        best = None
        for ring in range(0, 200):
            cands = []
            for i in range(-ring, ring + 1):
                for j in (-ring, ring) if abs(i) != ring else range(-ring, ring + 1):
                    cands.append((tx + i * 0.25, ty + j * 0.25))
            for cx, cy in sorted(cands, key=lambda c: (c[0] - tx) ** 2 + (c[1] - ty) ** 2):
                for rot in (0, 90, 180, 270):
                    b = rot_bbox(LBOX[ref], rot)
                    r = (cx + b[0], cx + b[1], cy + b[2], cy + b[3])
                    if not inside_board(r, m=SIDE_MARGIN, side=SIDE_MARGIN):
                        continue
                    if any(overlap(r, o, GAP) for _, o in occ[side]):
                        continue
                    best = (cx, cy, rot, r)
                    break
                if best:
                    break
            if best:
                break
        if not best:
            failed.append(ref)
            continue
        cx, cy, rot, r = best
        cx, cy = round(cx / 0.05) * 0.05, round(cy / 0.05) * 0.05
        if side == "B":
            f.Flip(f.GetPosition(), pcbnew.FLIP_DIRECTION_TOP_BOTTOM)
        f.SetOrientationDegrees(rot)
        f.SetPosition(V(cx, cy))
        occ[side].append((ref, r))
        placed.add(ref)
    if failed:
        print("NON PIAZZATI:", failed)

    for f in board.GetFootprints():
        if comps.get(f.GetReference(), {}).get("dnp"):
            f.SetDNP(True)
        if f.GetReference().startswith("TP"):
            f.SetExcludedFromBOM(True)
            f.SetExcludedFromPosFiles(True)

    # ------------------------------------------------ contorno con intaglio per l'antenna
    for a, b in zip(OUTLINE, OUTLINE[1:] + OUTLINE[:1]):
        s = pcbnew.PCB_SHAPE(board, pcbnew.SHAPE_T_SEGMENT)
        s.SetStart(V(*a))
        s.SetEnd(V(*b))
        s.SetLayer(pcbnew.Edge_Cuts)
        s.SetWidth(MM(0.05))
        board.Add(s)

    # serigrafia dei footprint fuori scheda o a meno di 0,3 mm dal bordo: tolta (connettori a filo bordo)
    for f in board.GetFootprints():
        for item in list(f.GraphicalItems()):
            if item.GetLayer() not in (pcbnew.F_SilkS, pcbnew.B_SilkS):
                continue
            bb = item.GetBoundingBox()
            r = (pcbnew.ToMM(bb.GetLeft()) - OX, pcbnew.ToMM(bb.GetRight()) - OX,
                 pcbnew.ToMM(bb.GetTop()) - OY, pcbnew.ToMM(bb.GetBottom()) - OY)
            if not inside_board(r, 0.3):
                f.Remove(item)

    # fori di fissaggio M2 (pad a GND)
    for i, (hx, hy) in enumerate(HOLES, 1):
        fp = load_fp("MountingHole:MountingHole_2.2mm_M2_Pad")
        fp.SetReference(f"H{i}")
        fp.SetValue("M2")
        fp.Reference().SetLayer(pcbnew.F_Fab)
        fp.Value().SetVisible(False)
        fp.SetPosition(V(hx, hy))
        fp.SetBoardOnly(True)              # parte solo meccanica: non e' nello schema
        fp.SetExcludedFromBOM(True)
        fp.SetExcludedFromPosFiles(True)
        board.Add(fp)
        for pad in fp.Pads():
            pad.SetNet(netcodes["GND"])

    # fiducial per l'assemblaggio (1 mm rame, 2 mm apertura maschera), lato superiore
    for i, (fx, fy) in enumerate(FIDUCIALS, 1):
        fp = load_fp("Fiducial:Fiducial_1mm_Mask2mm")
        fp.SetReference(f"FID{i}")
        fp.SetValue("Fiducial")
        fp.Reference().SetLayer(pcbnew.F_Fab)
        fp.Value().SetVisible(False)
        fp.SetPosition(V(fx, fy))
        fp.SetBoardOnly(True)              # riferimento ottico per l'assemblaggio: non e' nello schema
        fp.SetExcludedFromBOM(True)
        fp.SetExcludedFromPosFiles(True)
        board.Add(fp)
        # zona di rispetto del fiducial (3 x 3 mm): niente piste, vie o riempimenti sul lato superiore
        kf = pcbnew.ZONE(board)
        kf.SetIsRuleArea(True)
        kf.SetZoneName(f"fiducial{i}")
        kf.SetLayer(pcbnew.F_Cu)
        kf.SetDoNotAllowTracks(True)
        kf.SetDoNotAllowVias(True)
        kf.SetDoNotAllowZoneFills(True)
        kf.SetDoNotAllowPads(False)
        kf.SetDoNotAllowFootprints(False)
        kf.Outline().Append(poly([(fx - 1.5, fy - 1.5), (fx + 1.5, fy - 1.5), (fx + 1.5, fy + 1.5), (fx - 1.5, fy + 1.5)]))
        board.Add(kf)

    # Correzione REV-001/003: corpo-bordo su tutto il contorno e pad nei courtyard.
    # Le eccezioni J1/J2/U3 restano esplicite e soggette ad accettazione DFM.
    from verifica_meccanica_pcb import controlla
    meccanica = controlla(board)
    if meccanica['errori']:
        raise RuntimeError('Verifica meccanica fallita: ' + '; '.join(meccanica['errori']))

    # zona antenna: niente rame, piste, vie o componenti
    ka = pcbnew.ZONE(board)
    ka.SetIsRuleArea(True)
    ka.SetZoneName("antenna")
    ka.SetLayerSet(pcbnew.LSET.AllCuMask())
    ka.SetDoNotAllowTracks(True)
    ka.SetDoNotAllowVias(True)
    ka.SetDoNotAllowZoneFills(True)
    ka.SetDoNotAllowPads(True)
    ka.SetDoNotAllowFootprints(True)
    ka.Outline().Append(poly([(kx0, ky0), (kx1, ky0), (kx1, ky1), (kx0, ky1)]))
    board.Add(ka)

    # coppia USB D+/D- tracciata a mano e bloccata (DEC-041); sotto, sul retro, niente piste ne' vie
    zona, lung = usb_coppia.traccia(board, fps, OX, OY)
    for k, v in lung.items():
        print(f"USB {k}: {v:.2f} mm")
    ku = pcbnew.ZONE(board)
    ku.SetIsRuleArea(True)
    ku.SetZoneName("usb_coppia_retro")
    ku.SetLayer(pcbnew.B_Cu)
    ku.SetDoNotAllowTracks(True)
    ku.SetDoNotAllowVias(True)
    ku.SetDoNotAllowZoneFills(False)
    ku.SetDoNotAllowPads(False)
    ku.SetDoNotAllowFootprints(False)
    x0, x1, y0, y1 = zona
    ku.Outline().Append(poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)]))
    board.Add(ku)

    # piani di massa su entrambi gli strati
    for layer in (pcbnew.F_Cu, pcbnew.B_Cu):
        z = pcbnew.ZONE(board)
        z.SetLayer(layer)
        z.SetNet(netcodes["GND"])
        z.SetLocalClearance(MM(0.2))
        z.SetMinThickness(MM(0.2))
        z.SetPadConnection(pcbnew.ZONE_CONNECTION_THT_THERMAL)
        z.SetThermalReliefGap(MM(0.25))
        z.SetThermalReliefSpokeWidth(MM(0.3))
        z.SetIslandRemovalMode(pcbnew.ISLAND_REMOVAL_MODE_ALWAYS)
        z.Outline().Append(poly(OUTLINE))
        board.Add(z)

    # ------------------------------------------------ legenda sul retro (nessun componente assemblato)
    def btext(txt, x, y, size=0.8):
        t = pcbnew.PCB_TEXT(board)
        t.SetText(txt)
        t.SetLayer(pcbnew.B_SilkS)
        t.SetMirrored(True)
        t.SetTextSize(pcbnew.VECTOR2I(MM(size), MM(size)))
        t.SetTextThickness(MM(0.15))
        t.SetPosition(V(x, y))
        board.Add(t)
        return t

    def pos(ref):
        p = fps[ref].GetPosition()
        return pcbnew.ToMM(p.x) - OX, pcbnew.ToMM(p.y) - OY

    btext("PoliClock main rev 0.2", 10.5, H - 1.5, 0.9)
    x, y = pos("J3")
    btext("SHT40", x, y)
    x, y = pos("J4")
    btext("RTC", x, y)
    x, y = pos("J5")
    btext("BTN", x, y)
    x, y = pos("J2")
    btext("DISPLAY 1=VCC", x, y + 2.0)
    x, y = pos("J1")
    btext("USB", x - 6.0, y - 1.0)
    tps = sorted((f for f in fps.values() if f.GetReference().startswith("TP")), key=lambda f: (round(pos(f.GetReference())[1]), pos(f.GetReference())[0]))
    rows = {}
    for f in tps:
        rows.setdefault(round(pos(f.GetReference())[1]), []).append(f)
    tps = [(i, f) for row in rows.values() for i, f in enumerate(row)]
    for i, f in tps:
        x, y = pos(f.GetReference())
        name = f.Pads()[0].GetNetname().split("/")[-1]
        # etichette alternate sotto/sopra il pad per non sovrapporsi
        btext(f"{f.GetReference()} {name}", x, y + (1.8 if i % 2 == 0 else -1.8), 0.8)

    filler = pcbnew.ZONE_FILLER(board)
    filler.Fill(board.Zones())
    board.Save(OUT)

    # controlli DRC riabilitati (P1-08): courtyard e coerenza dei footprint
    pro = json.load(open(PRO, encoding="utf-8"))
    sev = pro.setdefault("board", {}).setdefault("design_settings", {}).setdefault("rule_severities", {})
    sev.update({"missing_courtyard": "error", "courtyards_overlap": "error", "pth_inside_courtyard": "error",
                "npth_inside_courtyard": "error", "lib_footprint_issues": "warning",
                "lib_footprint_mismatch": "warning", "footprint_type_mismatch": "warning",
                "silk_overlap": "error", "silk_over_copper": "warning", "silk_edge_clearance": "error",
                "text_height": "warning", "text_thickness": "warning"})
    json.dump(pro, open(PRO, "w", encoding="utf-8", newline="\n"), indent=2)
    print("saved", OUT)


if __name__ == "__main__":
    build()
