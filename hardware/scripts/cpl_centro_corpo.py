"""CPL alternativa per JLCPCB con U3 al centro del corpo (F.Fab) invece che all'origine dell'impronta.

Revisione esterna del 2026-11-08 (P1-01): l'origine dell'impronta di U3 (ESP32-C3-WROOM-02) e' il centro delle
file di piazzole, mentre il corpo con l'antenna e' spostato di circa 3,1 mm. JLC usa il "centroide" della propria
impronta di libreria: quale dei due file sia quello giusto si vede solo nell'anteprima 2D/3D di JLC.
All'ordine si carica la CPL normale; se nell'anteprima il modulo risulta spostato si carica questa
(docs/12 sezione 7). Nessuna delle due va corretta "a occhio".

Uso (Python di KiCad 10, lo richiama esporta.py dopo la CPL normale):
  "C:/Program Files/KiCad/10.0/bin/python.exe" hardware/scripts/cpl_centro_corpo.py
"""
import csv
import os
import pcbnew

D = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "policlock-main")
PCB = os.path.join(D, "policlock-main.kicad_pcb")
CPL = os.path.join(D, "policlock-main-cpl-jlcpcb.csv")
OUT = os.path.join(D, "policlock-main-cpl-jlcpcb-u3-centro-corpo.csv")
RIF = ("U3",)

board = pcbnew.LoadBoard(PCB)
orig = board.GetDesignSettings().GetAuxOrigin()   # stessa origine della CPL (--use-drill-file-origin)
ox, oy = pcbnew.ToMM(orig.x), pcbnew.ToMM(orig.y)
centri = {}
for ref in RIF:
    fp = board.FindFootprintByReference(ref)
    xs, ys = [], []
    for g in fp.GraphicalItems():
        if isinstance(g, pcbnew.PCB_SHAPE) and g.GetLayer() == pcbnew.F_Fab:
            bb = g.GetBoundingBox()
            xs += [bb.GetLeft(), bb.GetRight()]
            ys += [bb.GetTop(), bb.GetBottom()]
    cx, cy = pcbnew.ToMM((min(xs) + max(xs)) / 2), pcbnew.ToMM((min(ys) + max(ys)) / 2)
    centri[ref] = (cx - ox, oy - cy)

rows = list(csv.reader(open(CPL, encoding="utf-8")))
for r in rows[1:]:
    if r[0] in centri:
        r[1], r[2] = "%.6fmm" % centri[r[0]][0], "%.6fmm" % centri[r[0]][1]
with open(OUT, "w", encoding="utf-8", newline="") as f:
    csv.writer(f).writerows(rows)
for ref, (x, y) in centri.items():
    print("CPL alternativa:", ref, "al centro del corpo X %.3f Y %.3f mm" % (x, y))
