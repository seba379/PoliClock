"""FIN-006: Gerber e forature per JLCPCB. NON eseguire senza l'approvazione esplicita del proprietario.

Uso (solo dopo l'approvazione, registrata in docs/10):
  python hardware/scripts/esporta_gerber_jlc.py --conferma-proprietario

Senza --conferma-proprietario lo script si ferma subito e non scrive nulla.

Impostazioni dalla guida JLCPCB "How to generate Gerber and drill files in KiCad 8"
(https://jlcpcb.com/help/article/how-to-generate-gerber-and-drill-files-in-kicad-8, aggiornata il 2026-09-09,
letta il 2026-11-08; ricontrollarla all'ordine):
- Gerber: F.Cu, B.Cu, F.Paste, B.Paste, F.Silkscreen, B.Silkscreen, F.Mask, B.Mask, Edge.Cuts; estensioni Protel;
  maschera sottratta dalla serigrafia; zone ricontrollate prima del plot; origine assoluta;
- forature: Excellon, mm, zeri "decimal", origine assoluta, fori ovali in modalita' "alternate" (G85, come da guida;
  con --asole route si usa la fresatura G00/G01), PTH e NPTH in file separati, mappa delle forature in PDF.

Prima del plot esegue lo stesso gate di esporta.py (ERC, DRC con parita' e zone ricalcolate, controllo meccanico).
I file vanno in hardware/policlock-main/gerber-jlc/ (non versionata) e in un archivio .zip da caricare su JLCPCB.

Controlli da fare a mano DOPO (in un visualizzatore Gerber, es. GerbView di KiCad, e nell'anteprima JLC):
1. asole di J1: 4 asole metallizzate 0,6 x 1,7 / 0,6 x 1,2 mm (non fori tondi) e 2 pioli NPTH 0,65 mm;
2. contorno 50 x 40 mm con l'intaglio dell'antenna in alto a destra;
3. 3 fiducial con apertura della maschera; nessuna serigrafia fuori dal bordo (J2, U3);
4. rotazioni e origini nella CPL (docs/12, tabella FIN-004).
"""
import argparse
import os
import shutil
import subprocess
import sys
import zipfile

HW = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRJ = os.path.join(HW, "policlock-main")
PCB = os.path.join(PRJ, "policlock-main.kicad_pcb")
OUT = os.path.join(PRJ, "gerber-jlc")
KICAD_CLI = os.environ.get("KICAD_CLI", r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe")
LAYERS = "F.Cu,B.Cu,F.Paste,B.Paste,F.Silkscreen,B.Silkscreen,F.Mask,B.Mask,Edge.Cuts"

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("--conferma-proprietario", action="store_true",
                help="obbligatorio: il proprietario ha approvato la generazione dei Gerber")
ap.add_argument("--asole", choices=("alternate", "route"), default="alternate",
                help="modo dei fori ovali nel file Excellon (guida JLC: alternate)")
args = ap.parse_args()
if not args.conferma_proprietario:
    print("Gerber NON generati: serve --conferma-proprietario (approvazione esplicita del proprietario, AGENTS.md).")
    sys.exit(2)


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        print(r.stdout, r.stderr)
        sys.exit(r.returncode)
    return r.stdout


# gate: stesso controllo di esporta.py (si ferma se ERC/DRC/controllo meccanico falliscono)
run([sys.executable, os.path.join(HW, "scripts", "esporta.py")])

if os.path.isdir(OUT):
    shutil.rmtree(OUT)
os.makedirs(OUT)
run([KICAD_CLI, "pcb", "export", "gerbers", "-o", OUT + os.sep, "--layers", LAYERS, "--subtract-soldermask",
     "--check-zones", PCB])
run([KICAD_CLI, "pcb", "export", "drill", "-o", OUT + os.sep, "--format", "excellon", "--drill-origin", "absolute",
     "--excellon-units", "mm", "--excellon-zeros-format", "decimal", "--excellon-oval-format", args.asole,
     "--excellon-separate-th", "--generate-map", "--map-format", "pdf", PCB])
zip_path = os.path.join(PRJ, "policlock-main-gerber-jlc.zip")
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
    for f in sorted(os.listdir(OUT)):
        if not f.endswith(".pdf"):
            z.write(os.path.join(OUT, f), f)
print("Gerber e forature in", OUT)
print("Archivio per JLCPCB:", zip_path)
print("Ora controllare in un visualizzatore Gerber: asole di J1, intaglio, fiducial, serigrafia (vedi docstring).")
