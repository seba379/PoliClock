"""ERC, PDF e BOM (formato JLCPCB) per i progetti KiCad di PoliClock.

Uso:  python hardware/scripts/esporta.py   (richiede kicad-cli di KiCad 10)
"""
import csv
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
    # BOM JLC: senza le parti saldate a mano dal proprietario (campo Montaggio, DEC-043)
    bom_jlc = os.path.join(d, p + "-bom-jlcpcb.csv")
    run(["sch", "export", "bom", "-o", bom_jlc,
         "--fields", "Value,Reference,Footprint,LCSC,${QUANTITY},Montaggio",
         "--labels", "Comment,Designator,Footprint,LCSC Part #,Qty,Montaggio",
         "--group-by", "Value,Footprint,LCSC,Montaggio", "--ref-range-delimiter", "", "--exclude-dnp", sch])
    rows = list(csv.reader(open(bom_jlc, encoding="utf-8")))
    a_mano = [r_ for r_ in rows[1:] if r_[5]]
    jlc = [r_[:5] for r_ in rows[1:] if not r_[5]]
    senza_lcsc = [r_[1] for r_ in jlc if not r_[3]]
    if senza_lcsc:
        print("BOM JLC: parti senza codice LCSC e senza campo Montaggio:", senza_lcsc)
        sys.exit(1)
    with open(bom_jlc, "w", encoding="utf-8", newline="") as f:
        csv.writer(f, quoting=csv.QUOTE_ALL).writerows([rows[0][:5]] + jlc)
    print("BOM JLC:", len(jlc), "righe; escluse (a mano):", ",".join(r_[1] for r_ in a_mano) or "nessuna")
    designatori_jlc = {x for r_ in jlc for x in r_[1].split(",")}
    designatori_a_mano = {x for r_ in a_mano for x in r_[1].split(",")}
    # BOM completa: tutte le parti, con chi le monta (JLC oppure a mano)
    bom_all = os.path.join(d, p + "-bom-completa.csv")
    run(["sch", "export", "bom", "-o", bom_all,
         "--fields", "Reference,Value,Footprint,LCSC,${QUANTITY},${DNP},Montaggio,Description",
         "--labels", "Riferimenti,Valore,Footprint,LCSC,Qta,DNP,Montaggio,Note",
         "--group-by", "Value,Footprint,LCSC,${DNP},Montaggio", sch])
    rows = list(csv.reader(open(bom_all, encoding="utf-8")))
    for r_ in rows[1:]:
        r_[6] = r_[6] or "JLC (PCBA)"
    with open(bom_all, "w", encoding="utf-8", newline="") as f:
        csv.writer(f, quoting=csv.QUOTE_ALL).writerows(rows)

if not ok:
    print("ERC con violazioni: esportazioni del PCB interrotte, vedi erc.rpt")
    sys.exit(1)

# ---------------------------------------------------------------- PCB della scheda principale
pcb = os.path.join(HW, "policlock-main", "policlock-main.kicad_pcb")
if os.path.exists(pcb):
    d = os.path.dirname(pcb)
    # Gate DRC (REV-004): zone ricalcolate in memoria, codice d'uscita sulle violazioni; niente esportazioni se fallisce
    r = subprocess.run([KICAD_CLI, "pcb", "drc", "--severity-all", "--all-track-errors", "--schematic-parity",
                        "--refill-zones", "--exit-code-violations", "-o", os.path.join(d, "drc.rpt"), pcb],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    print("policlock-main DRC:", " / ".join(r.stdout.strip().splitlines()[:3]))
    if r.returncode != 0:
        print(r.stdout, r.stderr)
        print("DRC fallito o con violazioni (codice", r.returncode, "): esportazioni del PCB interrotte, vedi drc.rpt")
        sys.exit(r.returncode)
    # controllo meccanico (REV-001/003): margini dal bordo e courtyard, con il Python di KiCad
    kpy = os.environ.get("KICAD_PYTHON", os.path.join(os.path.dirname(KICAD_CLI), "python.exe"))
    r = subprocess.run([kpy, os.path.join(HW, "scripts", "verifica_meccanica_pcb.py"), pcb],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    print("policlock-main verifica meccanica:", "PASS" if r.returncode == 0 else "FAIL")
    if r.returncode != 0:
        print(r.stdout[-3000:], r.stderr[-3000:])
        sys.exit(r.returncode)
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
    rows = list(csv.DictReader(open(tmp, encoding="utf-8")))
    os.remove(tmp)
    # coerenza BOM JLC <-> CPL: le parti a mano (attributo "escluso dai file di posizionamento") non vanno a JLC
    cpl_refs = {r_["Ref"] for r_ in rows}
    if cpl_refs != designatori_jlc or cpl_refs & designatori_a_mano:
        print("CPL e BOM JLC non coerenti: solo CPL", sorted(cpl_refs - designatori_jlc),
              "solo BOM", sorted(designatori_jlc - cpl_refs), "a mano nella CPL", sorted(cpl_refs & designatori_a_mano))
        sys.exit(1)
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
