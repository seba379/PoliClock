"""ERC, PDF e BOM (formato JLCPCB) per i progetti KiCad di PoliClock.

Uso:  python hardware/scripts/esporta.py   (richiede kicad-cli di KiCad 10)
"""
import os
import subprocess
import sys

HW = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KICAD_CLI = os.environ.get("KICAD_CLI", r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe")
PROJECTS = ["policlock-main"]


def run(args):
    r = subprocess.run([KICAD_CLI] + args, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        print(r.stdout, r.stderr)
        sys.exit(r.returncode)
    return r.stdout


ok = True
for p in PROJECTS:
    d = os.path.join(HW, p)
    sch = os.path.join(d, p + ".kicad_sch")
    r = subprocess.run([KICAD_CLI, "sch", "erc", "--severity-all", "--exit-code-violations",
                        "-o", os.path.join(d, "erc.rpt"), sch], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    print(p, "ERC:", (r.stdout.strip().splitlines() or ["?"])[0])
    ok &= r.returncode == 0
    run(["sch", "export", "pdf", "-o", os.path.join(d, p + ".pdf"), sch])
    run(["sch", "export", "bom", "-o", os.path.join(d, p + "-bom-jlcpcb.csv"),
         "--fields", "Value,Reference,Footprint,LCSC,${QUANTITY}",
         "--labels", "Comment,Designator,Footprint,LCSC Part #,Qty",
         "--group-by", "Value,Footprint,LCSC", "--ref-range-delimiter", "", "--exclude-dnp", sch])
    run(["sch", "export", "bom", "-o", os.path.join(d, p + "-bom-completa.csv"),
         "--fields", "Reference,Value,Footprint,LCSC,${QUANTITY},${DNP},Description",
         "--labels", "Riferimenti,Valore,Footprint,LCSC,Qta,DNP,Note",
         "--group-by", "Value,Footprint,LCSC,${DNP}", sch])


# ---------------------------------------------------------------- PCB della scheda principale
pcb = os.path.join(HW, "policlock-main", "policlock-main.kicad_pcb")
if os.path.exists(pcb):
    d = os.path.dirname(pcb)
    r = subprocess.run([KICAD_CLI, "pcb", "drc", "--severity-all", "-o", os.path.join(d, "drc.rpt"), pcb],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    print("policlock-main DRC:", " / ".join(r.stdout.strip().splitlines()[:2]))
    run(["pcb", "export", "pdf", "--mode-multipage", "--scale", "5", "--layers", "F.Fab,F.Cu,B.Cu,B.SilkS",
         "--common-layers", "Edge.Cuts", "--sketch-pads-on-fab-layers", "--crossout-DNP-footprints-on-fab-layers",
         "-o", os.path.join(d, "policlock-main-layout.pdf"), pcb])
    for side in ("top", "bottom"):
        run(["pcb", "render", "--side", side, "-w", "1600", "-h", "1200", "--background", "opaque",
             "-o", os.path.join(d, f"policlock-main-{side}.png"), pcb])
    run(["pcb", "export", "step", "--board-only", "-f", "-o", os.path.join(d, "policlock-main-scheda.step"), pcb])
    # file di posizionamento (CPL) nel formato JLCPCB: Designator, Mid X, Mid Y, Layer, Rotation
    tmp = os.path.join(d, "pos_tmp.csv")
    run(["pcb", "export", "pos", "--format", "csv", "--units", "mm", "--side", "front", "--exclude-dnp",
         "--use-drill-file-origin", "-o", tmp, pcb])
    import csv
    rows = list(csv.DictReader(open(tmp, encoding="utf-8")))
    os.remove(tmp)
    with open(os.path.join(d, "policlock-main-cpl-jlcpcb.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Designator", "Mid X", "Mid Y", "Layer", "Rotation"])
        for r_ in rows:
            w.writerow([r_["Ref"], r_["PosX"] + "mm", r_["PosY"] + "mm", "Top" if r_["Side"] == "top" else "Bottom",
                        r_["Rot"]])
    print("CPL:", len(rows), "componenti")
    # STEP completo con i modelli EasyEDA locali (non versionato, vedi README)
    run(["pcb", "export", "step", "--subst-models", "--no-dnp", "-f", "-o", os.path.join(d, "policlock-main.step"), pcb])

sys.exit(0 if ok else 1)
