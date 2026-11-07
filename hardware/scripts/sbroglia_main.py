"""Bozza di sbroglio della scheda principale con Freerouting.

Uso (Python di KiCad 10):
  "C:/Program Files/KiCad/10.0/bin/python.exe" hardware/scripts/sbroglia_main.py [--solo-import]

1. imposta la classe di rete "Power" (piste 0,4 mm) sulle alimentazioni;
2. esporta il DSN (Specctra), lancia Freerouting 2.5.0 (jar, Java 25 portatile), reimporta la sessione SES;
3. riempie i piani di massa e salva policlock-main.kicad_pcb.
Con --solo-import salta Freerouting e importa il .ses gia' presente.
Il risultato e' una BOZZA: va rivista a mano in KiCad (vedi docs/02 par. 3.2).
Nota: la build nativa "freerouting-cli" 2.5.0 per Windows si blocca nel router; usare il jar.
"""
import os
import subprocess
import sys
import pcbnew

HERE = os.path.dirname(os.path.abspath(__file__))
PRJ = os.path.join(os.path.dirname(HERE), "policlock-main")
PCB = os.path.join(PRJ, "policlock-main.kicad_pcb")
DSN = os.path.join(PRJ, "policlock-main.dsn")
SES = os.path.join(PRJ, "policlock-main.ses")
FRDIR = os.path.join(os.environ["LOCALAPPDATA"], "Programs", "freerouting-2.5.0")
JAVA = os.path.join(FRDIR, "jdk-25.0.5+8-jre", "bin", "java.exe")
JAR = os.path.join(FRDIR, "freerouting-2.5.0.jar")
IMPORT_ONLY = "--solo-import" in sys.argv
MM = pcbnew.FromMM

POWER_NETS = ["VBUS", "+5V", "+3V3", "GND", "*5V_LDO", "*3V3_DISP", "*3V3_EXT", "*LCD_LEDK", "*BL_D"]

board = pcbnew.LoadBoard(PCB)
ns = board.GetDesignSettings().m_NetSettings
pw = pcbnew.NETCLASS("Power")
pw.SetTrackWidth(MM(0.4))
pw.SetClearance(MM(0.15))
pw.SetViaDiameter(MM(0.7))
pw.SetViaDrill(MM(0.35))
ns.SetNetclass("Power", pw)
ns.ClearNetclassPatternAssignments()
for pat in POWER_NETS:
    ns.SetNetclassPatternAssignment(pat, "Power")
board.SynchronizeNetsAndNetClasses(True)
ds = board.GetDesignSettings()
# minimi JLCPCB 2 strati (Freerouting restringe le piste vicino alle piazzole fini)
ds.m_TrackMinWidth = MM(0.1)
ds.m_ViasMinAnnularWidth = MM(0.1)
for t in list(board.GetTracks()):
    board.Remove(t)

# fascia lungo il bordo vietata a piste e vie (Freerouting non conosce la distanza rame-bordo)
for z in list(board.Zones()):
    if z.GetIsRuleArea() and z.GetZoneName() == "bordo":
        board.Remove(z)
bb = board.GetBoardEdgesBoundingBox()
x0, y0, x1, y1 = bb.GetLeft(), bb.GetTop(), bb.GetRight(), bb.GetBottom()
e = MM(0.45)
for layer in (pcbnew.F_Cu, pcbnew.B_Cu):
    for (ax, ay, bx, by) in ((x0, y0, x1, y0 + e), (x0, y1 - e, x1, y1), (x0, y0, x0 + e, y1), (x1 - e, y0, x1, y1)):
        ra = pcbnew.ZONE(board)
        ra.SetIsRuleArea(True)
        ra.SetZoneName("bordo")
        ra.SetLayer(layer)
        ra.SetDoNotAllowTracks(True)
        ra.SetDoNotAllowVias(True)
        ra.SetDoNotAllowZoneFills(False)
        ra.SetDoNotAllowPads(False)
        ra.SetDoNotAllowFootprints(False)
        ol = ra.Outline()
        ol.NewOutline()
        for px, py in ((ax, ay), (bx, ay), (bx, by), (ax, by)):
            ol.Append(px, py)
        board.Add(ra)

# i piani GND vengono tolti durante lo sbroglio (Freerouting li tratterebbe come piani interi
# e lascerebbe isole): la massa viene tracciata come le altre reti, poi i piani si rimettono
pours = [z for z in board.Zones() if not z.GetIsRuleArea()]
for z in pours:
    board.Remove(z)

if not IMPORT_ONLY:
    if not pcbnew.ExportSpecctraDSN(board, DSN):
        sys.exit("export DSN fallito")
    print("DSN esportato")
    if os.path.exists(SES):
        os.remove(SES)
    r = subprocess.run([JAVA, "-jar", JAR, "-de", DSN, "-do", SES, "--router.autorouter.max_passes=20",
                        "--gui.enabled=false"], capture_output=True, text=True,
                       stdin=subprocess.DEVNULL)
    for line in r.stdout.splitlines():
        if "stage completed" in line:
            print(line)
    if not os.path.exists(SES):
        print(r.stderr[-3000:])
        sys.exit("Freerouting non ha prodotto la sessione")
if not pcbnew.ImportSpecctraSES(board, SES):
    sys.exit("import SES fallito")
for z in pours:
    board.Add(z)
filler = pcbnew.ZONE_FILLER(board)
filler.Fill(board.Zones())
board.Save(PCB)
print("salvato", PCB, "piste+vie:", len(board.GetTracks()))
