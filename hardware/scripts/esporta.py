"""ERC, PDF e BOM (formato JLCPCB) per i tre progetti KiCad di PoliClock.

Uso:  python hardware/scripts/esporta.py   (richiede kicad-cli di KiCad 10)
"""
import os
import subprocess
import sys

HW = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KICAD_CLI = os.environ.get("KICAD_CLI", r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe")
PROJECTS = ["policlock-main", "policlock-display", "policlock-sht40"]


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
sys.exit(0 if ok else 1)
