"""Audit in sola lettura della scheda principale PoliClock (revisione finale pre-Gerber, 2026-11-08).

Da eseguire con il Python di KiCad 10 dalla root del repository:
    "C:/Program Files/KiCad/10.0/bin/python.exe" docs/revisioni/2026-11-08/revisione-finale/audit_finale.py
Scrive soltanto audit-finale.json in questa cartella. Non salva mai il PCB.
"""
import json
import math
import os
import sys
from collections import defaultdict

import pcbnew

QUI = os.path.dirname(os.path.abspath(__file__))
PCB = os.path.join("hardware", "policlock-main", "policlock-main.kicad_pcb")
mm = pcbnew.ToMM

b = pcbnew.LoadBoard(PCB)
out = {"kicad": pcbnew.GetBuildVersion(), "pcb": PCB}

# Contorno
bb = b.GetBoardEdgesBoundingBox()
out["contorno_bbox_mm"] = [mm(bb.GetX()), mm(bb.GetY()), mm(bb.GetRight()), mm(bb.GetBottom())]
ox, oy = mm(bb.GetX()), mm(bb.GetBottom())  # origine CPL: angolo in basso a sinistra
edges = []
for d in b.GetDrawings():
    if d.GetLayer() == pcbnew.Edge_Cuts:
        edges.append([d.GetShapeStr(), round(mm(d.GetStart().x) - ox, 3), round(oy - mm(d.GetStart().y), 3),
                      round(mm(d.GetEnd().x) - ox, 3), round(oy - mm(d.GetEnd().y), 3)])
out["edge_cuts_rel_bl"] = edges
out["aux_origin_mm"] = [mm(b.GetDesignSettings().GetAuxOrigin().x), mm(b.GetDesignSettings().GetAuxOrigin().y)]

def campo(f, nome):
    c = f.GetField(nome) if hasattr(f, "GetField") else None
    return c.GetText() if c else ""


# Footprint
fps = {}
for f in b.GetFootprints():
    p = f.GetPosition()
    attrs = f.GetAttributes()
    fps[f.GetReference()] = {
        "valore": f.GetValue(),
        "fpid": str(f.GetFPID().GetUniStringLibId()),
        "x_rel": round(mm(p.x) - ox, 4), "y_rel": round(oy - mm(p.y), 4),
        "x_abs": round(mm(p.x), 4), "y_abs": round(mm(p.y), 4),
        "rot": round(f.GetOrientationDegrees(), 2),
        "lato": "top" if f.GetLayer() == pcbnew.F_Cu else "bottom",
        "smd": bool(attrs & pcbnew.FP_SMD), "tht": bool(attrs & pcbnew.FP_THROUGH_HOLE),
        "escluso_pos": bool(attrs & pcbnew.FP_EXCLUDE_FROM_POS_FILES),
        "escluso_bom": bool(attrs & pcbnew.FP_EXCLUDE_FROM_BOM),
        "dnp": f.IsDNP() if hasattr(f, "IsDNP") else None,
        "lcsc": campo(f, "LCSC"),
        "montaggio": campo(f, "Montaggio"),
    }
out["footprint"] = fps

# Piazzole THT e fori
tht = []
for f in b.GetFootprints():
    for pad in f.Pads():
        if pad.GetAttribute() in (pcbnew.PAD_ATTRIB_PTH, pcbnew.PAD_ATTRIB_NPTH):
            dx, dy = mm(pad.GetDrillSizeX()), mm(pad.GetDrillSizeY())
            sx, sy = mm(pad.GetSizeX()), mm(pad.GetSizeY())
            ring = (min(sx - dx, sy - dy) / 2) if pad.GetAttribute() == pcbnew.PAD_ATTRIB_PTH else None
            tht.append({"ref": f.GetReference(), "pad": pad.GetNumber(), "net": pad.GetNetname(),
                        "tipo": "PTH" if pad.GetAttribute() == pcbnew.PAD_ATTRIB_PTH else "NPTH",
                        "forma": pad.ShapeAsString() if hasattr(pad, "ShapeAsString") else str(pad.GetShape()),
                        "foro": [round(dx, 3), round(dy, 3)], "dim_pad": [round(sx, 3), round(sy, 3)],
                        "anello_min": None if ring is None else round(ring, 3),
                        "x_abs": round(mm(pad.GetPosition().x), 3), "y_abs": round(mm(pad.GetPosition().y), 3),
                        "y_dal_bordo_sup": round(mm(pad.GetPosition().y) - mm(bb.GetY()), 3),
                        "x_dal_bordo_sx": round(mm(pad.GetPosition().x) - mm(bb.GetX()), 3)})
out["piazzole_tht"] = tht

# Piazzole sul retro (test point) e loro vicinanza ai fori THT
back = []
for f in b.GetFootprints():
    for pad in f.Pads():
        if pad.IsOnLayer(pcbnew.B_Cu) and pad.GetAttribute() == pcbnew.PAD_ATTRIB_SMD:
            back.append((f.GetReference(), pad.GetNumber(), pad.GetNetname(), mm(pad.GetPosition().x), mm(pad.GetPosition().y), mm(pad.GetSizeX())))
vic = []
for r, n, net, x, y, s in back:
    best = None
    for t in tht:
        if t["tipo"] != "PTH" or t["ref"].startswith("J1") or t["ref"].startswith("H"):
            continue
        d = math.hypot(t["x_abs"] - x, t["y_abs"] - y) - s / 2 - max(t["dim_pad"]) / 2
        if best is None or d < best[0]:
            best = (round(d, 3), t["ref"] + "." + t["pad"])
    vic.append({"tp": r, "net": net, "x_abs": round(x, 3), "y_abs": round(y, 3), "diam": s,
                "distanza_bordo_rame_da_THT_J2_J5": best})
out["test_point_retro"] = vic

# Piste per rete
seg = defaultdict(lambda: {"lunghezza": 0.0, "larghezze": set(), "segmenti": 0, "vie": 0, "strati": set()})
vias = []
for t in b.GetTracks():
    net = t.GetNetname()
    if t.Type() == pcbnew.PCB_VIA_T:
        seg[net]["vie"] += 1
        vias.append((net, round(mm(t.GetWidth(pcbnew.F_Cu)), 3), round(mm(t.GetDrillValue()), 3)))
    else:
        seg[net]["lunghezza"] += mm(t.GetLength())
        seg[net]["larghezze"].add(round(mm(t.GetWidth()), 3))
        seg[net]["segmenti"] += 1
        seg[net]["strati"].add(t.GetLayerName())
out["reti"] = {k: {"lunghezza_mm": round(v["lunghezza"], 2), "larghezze_mm": sorted(v["larghezze"]),
                   "segmenti": v["segmenti"], "vie": v["vie"], "strati": sorted(v["strati"])}
               for k, v in sorted(seg.items())}
vt = defaultdict(int)
for v in vias:
    vt[f"{v[1]}/{v[2]}"] += 1
out["vie_per_dimensione"] = dict(vt)
out["vie_totali"] = len(vias)
out["netclass_per_rete"] = {n.GetNetname(): n.GetNetClassName() for n in b.GetNetsByName().values() if n.GetNetname()}

# Zone
zones = []
for z in b.Zones():
    o = z.Outline().BBox()
    zones.append({"nome": z.GetZoneName(), "rete": z.GetNetname(), "strati": [b.GetLayerName(l) for l in z.GetLayerSet().Seq()],
                  "keepout": z.GetIsRuleArea(),
                  "vieta": {"piste": z.GetDoNotAllowTracks(), "vie": z.GetDoNotAllowVias(), "zone": z.GetDoNotAllowZoneFills(),
                            "piazzole": z.GetDoNotAllowPads(), "footprint": z.GetDoNotAllowFootprints()} if z.GetIsRuleArea() else None,
                  "bbox_abs": [round(mm(o.GetX()), 3), round(mm(o.GetY()), 3), round(mm(o.GetRight()), 3), round(mm(o.GetBottom()), 3)],
                  "clearance": round(mm(z.GetLocalClearance() or 0), 3) if not z.GetIsRuleArea() else None,
                  "min_thickness": round(mm(z.GetMinThickness()), 3) if not z.GetIsRuleArea() else None,
                  "thermal_gap": round(mm(z.GetThermalReliefGap()), 3) if not z.GetIsRuleArea() else None,
                  "spoke": round(mm(z.GetThermalReliefSpokeWidth()), 3) if not z.GetIsRuleArea() else None,
                  "pad_connection": int(z.GetPadConnection()) if not z.GetIsRuleArea() else None,
                  "riempita": z.IsFilled()})
out["zone"] = zones

# Rame nella regione dell'antenna (sopra l'intaglio e zona di rispetto)
u3 = b.FindFootprintByReference("U3")
out["U3_bbox_courtyard"] = None
if u3:
    c = u3.GetCourtyard(pcbnew.F_CrtYd).BBox()
    out["U3_bbox_courtyard"] = [round(mm(c.GetX()), 3), round(mm(c.GetY()), 3), round(mm(c.GetRight()), 3), round(mm(c.GetBottom()), 3)]

# Fiducial
out["fiducial"] = {r: v for r, v in fps.items() if r.startswith("FID")}

json.dump(out, open(os.path.join(QUI, "audit-finale.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False, default=list)
print("ok", len(fps), "footprint,", len(vias), "vie")
