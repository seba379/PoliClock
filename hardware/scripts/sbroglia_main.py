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
# pista minima 0,15 mm (JLC ammette 0,10 mm): margine di fabbricazione anche dove Freerouting restringe le piste
ds.m_TrackMinWidth = MM(0.15)
ds.m_ViasMinAnnularWidth = MM(0.1)
for t in list(board.GetTracks()):
    if not t.IsLocked():          # la coppia USB tracciata a mano (bloccata) resta e Freerouting la rispetta
        board.Remove(t)

# fascia lungo il bordo vietata a piste e vie (Freerouting non conosce la distanza rame-bordo)
for z in list(board.Zones()):
    if z.GetIsRuleArea() and z.GetZoneName() == "bordo":
        board.Remove(z)
e = MM(0.45)
strips = []
for sh in board.GetDrawings():
    if sh.GetLayer() == pcbnew.Edge_Cuts and sh.GetShape() == pcbnew.SHAPE_T_SEGMENT:
        a, b = sh.GetStart(), sh.GetEnd()
        strips.append((min(a.x, b.x) - e, min(a.y, b.y) - e, max(a.x, b.x) + e, max(a.y, b.y) + e))
for layer in (pcbnew.F_Cu, pcbnew.B_Cu):
    for (ax, ay, bx, by) in strips:
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
# Freerouting restringe a volte una pista a 0,10 mm (minimo JLC) vicino alle piazzole fini: la riporta a
# 0,15 mm solo se resta la distanza di 0,15 mm dal rame delle altre reti (verificata poi dal DRC di esporta.py)
strette = [t for t in board.GetTracks() if t.GetClass() != "PCB_VIA" and t.GetWidth() < MM(0.15)]
altri = list(board.GetTracks()) + list(board.GetPads())
allargate = 0
for t in strette:
    w0 = t.GetWidth()
    t.SetWidth(MM(0.15))
    lay = t.GetLayer()
    urto = any(o is not t and o.GetNetCode() != t.GetNetCode() and o.IsOnLayer(lay)
               and t.GetEffectiveShape(lay).Collide(o.GetEffectiveShape(lay), MM(0.15))
               for o in altri)
    if urto:
        t.SetWidth(w0)
    else:
        allargate += 1
print("piste strette:", len(strette), "allargate a 0,15 mm:", allargate)


# Freerouting lascia a volte vie collegate su un solo strato e pezzi di pista senza uscita: si tolgono, ripetendo
# finche' non cambia piu' nulla (la rete GND resta intatta; la coppia USB bloccata resta)
def tocca(item, pos, layer):
    if item.GetClass() == "PCB_VIA":
        return item.IsOnLayer(layer) and (item.GetPosition() - pos).EuclideanNorm() <= item.GetWidth(layer) // 2
    if item.GetClass() == "PCB_TRACK":
        return item.GetLayer() == layer and (item.GetStart() == pos or item.GetEnd() == pos
                                             or item.HitTest(pos, 0))
    return item.IsOnLayer(layer) and item.HitTest(pos, 0)          # piazzola


tolti = 0
while True:
    per_rete = {}
    for o in list(board.GetTracks()) + list(board.GetPads()):
        per_rete.setdefault(o.GetNetCode(), []).append(o)
    da_togliere = []
    for t in board.GetTracks():
        if t.IsLocked() or t.GetNetname() == "GND":
            continue
        tid = t.m_Uuid.AsString()          # i wrapper SWIG cambiano: confronto per UUID
        altri_rete = [o for o in per_rete[t.GetNetCode()] if o.m_Uuid.AsString() != tid]
        if t.GetClass() == "PCB_VIA":
            strati = {lay for lay in (pcbnew.F_Cu, pcbnew.B_Cu)
                      if any(tocca(o, t.GetPosition(), lay) for o in altri_rete)}
            if len(strati) < 2:
                da_togliere.append(t)
        elif t.GetLength() < MM(0.001):
            da_togliere.append(t)                                      # pista di lunghezza nulla
        else:
            lay = t.GetLayer()
            if not all(any(tocca(o, p, lay) for o in altri_rete) for p in (t.GetStart(), t.GetEnd())):
                da_togliere.append(t)
    if not da_togliere:
        break
    for t in da_togliere:
        board.Remove(t)
    tolti += len(da_togliere)
print("vie e piste senza uscita tolte:", tolti)
for z in pours:
    board.Add(z)
filler = pcbnew.ZONE_FILLER(board)
filler.Fill(board.Zones())
board.Save(PCB)
print("salvato", PCB, "piste+vie:", len(board.GetTracks()))
