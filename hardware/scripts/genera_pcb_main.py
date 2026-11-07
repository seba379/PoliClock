"""Primo posizionamento della scheda principale (policlock-main.kicad_pcb).

Da eseguire con il Python di KiCad 10:
  "C:/Program Files/KiCad/10.0/bin/python.exe" hardware/scripts/genera_pcb_main.py [--info]

Legge la netlist esportata dallo schema (policlock-main.net), carica i footprint, assegna le net,
posiziona i componenti secondo la tabella PLACE, disegna contorno, fori, piani GND e regole JLCPCB.
Dopo la prima modifica manuale in KiCad il file .kicad_pcb diventa la fonte: non rieseguire.
"""
import os
import sys
import pcbnew

HERE = os.path.dirname(os.path.abspath(__file__))
HW = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from sexp import parse, find, find1  # noqa: E402

PRJ = os.path.join(HW, "policlock-main")
NET = os.path.join(PRJ, "policlock-main.net")
OUT = os.path.join(PRJ, "policlock-main.kicad_pcb")
STD = "C:/Program Files/KiCad/10.0/share/kicad/footprints"
LOCAL = os.path.join(HW, "lib", "PoliClock.pretty")

MM = pcbnew.FromMM
OX, OY = 100.0, 100.0          # origine della scheda nel foglio
W, H = 34.0, 26.0              # dimensioni della scheda (mm) - aggiornate dal posizionamento

# ref: (x, y, rot, lato)  coordinate relative all'angolo in alto a sinistra della scheda
from posizioni_main import PLACE, W, H, HOLES, AUTO_ORDER, BOTTOM  # noqa: E402

POWER = {"GND", "+3V3", "+5V", "VBUS"}


def local_bbox(fp):
    """Courtyard (o bounding box) del footprint non ruotato, in mm relativi all'origine."""
    fp.SetOrientationDegrees(0)
    fp.SetPosition(pcbnew.VECTOR2I(0, 0))
    fp.BuildCourtyardCaches()
    cy = fp.GetCourtyard(pcbnew.F_CrtYd)
    bb = cy.BBox() if cy.OutlineCount() else fp.GetBoundingBox(False)
    b = [pcbnew.ToMM(bb.GetLeft()), pcbnew.ToMM(bb.GetRight()), pcbnew.ToMM(bb.GetTop()), pcbnew.ToMM(bb.GetBottom())]
    # i courtyard EasyEDA non sempre coprono le piazzole: unione con le piazzole + 0,25 mm
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


def load_netlist():
    root = parse(open(NET, encoding="utf-8").read())[0]
    comps = {}
    for c in find(find1(root, "components"), "comp"):
        ref = find1(c, "ref")[1]
        comps[ref] = {"fp": find1(c, "footprint")[1], "value": find1(c, "value")[1],
                      "fields": {find1(f, "name")[1]: (f[-1] if isinstance(f[-1], str) else "")
                                 for f in find(find1(c, "fields") or [], "field")}}
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


LBOX = {}


def build(info=False):
    comps, pads = load_netlist()
    board = pcbnew.BOARD()
    board.SetCopperLayerCount(2)
    ds = board.GetDesignSettings()
    # Regole compatibili JLCPCB 2 strati (con margine sui minimi del produttore)
    ds.m_MinClearance = MM(0.1)          # minimo JLC 2 strati; classe di default 0,15 mm
    ds.m_TrackMinWidth = MM(0.15)
    ds.m_ViasMinSize = MM(0.6)
    ds.m_ViasMinAnnularWidth = MM(0.15)
    ds.m_MinThroughDrill = MM(0.3)
    ds.m_HoleClearance = MM(0.25)
    ds.m_HoleToHoleMin = MM(0.5)
    ds.m_CopperEdgeClearance = MM(0.3)
    ds.m_SilkClearance = MM(0.0)
    ds.SetBoardThickness(MM(1.6))
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
        for k, v in c["fields"].items():
            if k in ("LCSC",):
                fp.SetField(k, v)
        if c["fields"].get("DNP") is not None:
            pass
        LBOX[ref] = local_bbox(fp)
        # serigrafia minima: riferimenti sul disegno di assemblaggio (F.Fab), valori e campi nascosti
        fp.Value().SetVisible(False)
        for fld in fp.GetFields():
            if fld.GetName() not in ("Reference", "Value"):
                fld.SetVisible(False)
        fp.Reference().SetLayer(pcbnew.F_Fab)
        fp.Reference().SetTextSize(pcbnew.VECTOR2I(MM(0.5), MM(0.5)))
        fp.Reference().SetTextThickness(MM(0.08))
        for item in fp.GraphicalItems():
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
            fp.SetPosition(pcbnew.VECTOR2I(MM(OX + x), MM(OY + y)))
        if info and ref == "U3":
            fp.SetOrientationDegrees(270)
            for pad in fp.Pads():
                p = pad.GetPosition() - fp.GetPosition()
                print(f"U3 pad {pad.GetNumber():>3} {pcbnew.ToMM(p.x):6.2f} {pcbnew.ToMM(p.y):6.2f} {pad.GetNetname()}")
    if info:
        return

    # ------------------------------------------------ piazzamento automatico
    fps = {f.GetReference(): f for f in board.GetFootprints()}
    occ = {"F": [], "B": []}
    for ref, (x, y, rot, side) in PLACE.items():
        f = fps[ref]
        b = rot_bbox(LBOX[ref], rot)
        r = (OX + x + b[0], OX + x + b[1], OY + y + b[2], OY + y + b[3])
        occ[side].append((ref, r))
        if any(p.GetAttribute() == pcbnew.PAD_ATTRIB_PTH for p in f.Pads()):
            occ["B" if side == "F" else "F"].append((ref, r))
    for hx, hy in HOLES:
        r = (OX + hx - 2.5, OX + hx + 2.5, OY + hy - 2.5, OY + hy + 2.5)
        occ["F"].append(("H", r))
        occ["B"].append(("H", r))
    placed = set(PLACE)
    failed = []
    for ref in AUTO_ORDER:
        f = fps[ref]
        side = "B" if ref in BOTTOM else "F"
        nets = {p.GetNetname() for p in f.Pads()} - {""}
        sig = (nets - POWER) or nets
        pts = [p.GetPosition() for o in placed for p in fps[o].Pads() if p.GetNetname() in sig]
        if not pts:
            pts = [pcbnew.VECTOR2I(MM(OX + W / 2), MM(OY + H / 2))]
        tx = sum(pcbnew.ToMM(p.x) for p in pts) / len(pts)
        ty = sum(pcbnew.ToMM(p.y) for p in pts) / len(pts)
        best = None
        step = 0.25
        for ring in range(0, 160):
            cands = []
            for i in range(-ring, ring + 1):
                for j in (-ring, ring) if abs(i) != ring else range(-ring, ring + 1):
                    cands.append((tx + i * step, ty + j * step))
            for cx, cy in sorted(cands, key=lambda c: (c[0] - tx) ** 2 + (c[1] - ty) ** 2):
                for rot in (0, 90):
                    b = rot_bbox(LBOX[ref], rot)
                    r = (cx + b[0], cx + b[1], cy + b[2], cy + b[3])
                    if r[0] < OX + 0.1 or r[1] > OX + W - 0.1 or r[2] < OY + 0.1 or r[3] > OY + H - 0.1:
                        continue
                    if any(overlap(r, o) for _, o in occ[side]):
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
        f.SetPosition(pcbnew.VECTOR2I(MM(cx), MM(cy)))
        occ[side].append((ref, r))
        placed.add(ref)
    if failed:
        print("NON PIAZZATI:", failed)

    # DNP dallo schema
    for fp in board.GetFootprints():
        if fp.GetReference() in ("R11", "R12", "R13", "R14"):
            fp.SetDNP(True)
        if fp.GetReference().startswith("TP"):
            fp.SetExcludedFromBOM(True)
            fp.SetExcludedFromPosFiles(True)

    # contorno con angoli arrotondati r = 1 mm
    r = 1.0
    x0, y0, x1, y1 = OX, OY, OX + W, OY + H

    def seg(a, b):
        s = pcbnew.PCB_SHAPE(board, pcbnew.SHAPE_T_SEGMENT)
        s.SetStart(pcbnew.VECTOR2I(MM(a[0]), MM(a[1])))
        s.SetEnd(pcbnew.VECTOR2I(MM(b[0]), MM(b[1])))
        s.SetLayer(pcbnew.Edge_Cuts)
        s.SetWidth(MM(0.05))
        board.Add(s)

    def arc(c, start, mid, end):
        s = pcbnew.PCB_SHAPE(board, pcbnew.SHAPE_T_ARC)
        s.SetArcGeometry(pcbnew.VECTOR2I(MM(start[0]), MM(start[1])), pcbnew.VECTOR2I(MM(mid[0]), MM(mid[1])),
                         pcbnew.VECTOR2I(MM(end[0]), MM(end[1])))
        s.SetLayer(pcbnew.Edge_Cuts)
        s.SetWidth(MM(0.05))
        board.Add(s)
    k = r * (1 - 0.70710678)
    seg((x0 + r, y0), (x1 - r, y0))
    seg((x1, y0 + r), (x1, y1 - r))
    seg((x1 - r, y1), (x0 + r, y1))
    seg((x0, y1 - r), (x0, y0 + r))
    arc(None, (x1 - r, y0), (x1 - k, y0 + k), (x1, y0 + r))
    arc(None, (x1, y1 - r), (x1 - k, y1 - k), (x1 - r, y1))
    arc(None, (x0 + r, y1), (x0 + k, y1 - k), (x0, y1 - r))
    arc(None, (x0, y0 + r), (x0 + k, y0 + k), (x0 + r, y0))

    # fori di fissaggio M2 (pad a GND)
    for i, (hx, hy) in enumerate(HOLES, 1):
        fp = load_fp("MountingHole:MountingHole_2.2mm_M2_Pad")
        fp.SetReference(f"H{i}")
        fp.SetValue("M2")
        fp.Reference().SetLayer(pcbnew.F_Fab)
        fp.Value().SetVisible(False)
        fp.SetPosition(pcbnew.VECTOR2I(MM(OX + hx), MM(OY + hy)))
        fp.SetExcludedFromBOM(True)
        fp.SetExcludedFromPosFiles(True)
        board.Add(fp)
        for pad in fp.Pads():
            pad.SetNet(netcodes["GND"])

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
        z.SetAssignedPriority(0)
        ol = z.Outline()
        ol.NewOutline()
        for px, py in ((x0, y0), (x1, y0), (x1, y1), (x0, y1)):
            ol.Append(MM(px), MM(py))
        board.Add(z)

    # legenda sul retro (lato senza componenti assemblati): nome scheda, connettori, tasti, punti di test
    def btext(txt, x, y, size=0.8):
        t = pcbnew.PCB_TEXT(board)
        t.SetText(txt)
        t.SetLayer(pcbnew.B_SilkS)
        t.SetMirrored(True)
        t.SetTextSize(pcbnew.VECTOR2I(MM(size), MM(size)))
        t.SetTextThickness(MM(0.15))
        t.SetPosition(pcbnew.VECTOR2I(MM(x), MM(y)))
        board.Add(t)
    btext("PoliClock main rev 0.1", OX + 8.0, OY + H - 1.3, 0.8)
    for ref, label in (("J3", "SHT40"), ("J4", "RTC"), ("J5", "BTN"), ("J2", "DISPLAY"), ("J1", "USB"),
                       ("SW1", "RST"), ("SW2", "BOOT"), ("SW3", "USER")):
        p = fps[ref].GetPosition()
        btext(label, pcbnew.ToMM(p.x), pcbnew.ToMM(p.y))
    for f in fps.values():
        if f.GetReference().startswith("TP"):
            p = f.GetPosition()
            name = f.Pads()[0].GetNetname().split("/")[-1]
            btext(name, pcbnew.ToMM(p.x), pcbnew.ToMM(p.y) + 1.6, 0.8)

    filler = pcbnew.ZONE_FILLER(board)
    filler.Fill(board.Zones())
    board.Save(OUT)
    print("saved", OUT)


if __name__ == "__main__":
    build(info="--info" in sys.argv)
