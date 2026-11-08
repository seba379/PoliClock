"""DEC-044 (modulo ESP32-C3-WROOM-02-N4) e FIN-003/FIN-005: modifica una tantum del .kicad_pcb.

Prima eseguire  python hardware/scripts/dec044_schema.py  (schema). Poi, con il Python di KiCad 10:
  "C:/Program Files/KiCad/10.0/bin/python.exe" hardware/scripts/dec044_pcb.py
  "C:/Program Files/KiCad/10.0/bin/python.exe" hardware/scripts/sbroglia_main.py
  "C:/Program Files/KiCad/10.0/bin/python.exe" hardware/scripts/cucitura_gnd.py

Cosa fa:
1. crea in lib/PoliClock.pretty l'impronta ESP32-C3-WROOM-02 derivata da RF_Module:ESP32-C3-WROOM-02 di KiCad 10
   (piazzole identiche, confrontate col disegno Espressif, fig. 11-1 del datasheet v1.7): le 12 vie termiche da 0,2 mm
   diventano 4 vie 0,3/0,7 mm (minimi JLC e regole del progetto) e si toglie la serigrafia sopra l'antenna/intaglio;
2. U3 diventa il WROOM-02 (antenna verso destra, sopra l'intaglio; pin 13/14 = D-/D+ sull'asse di J1), C11 si aggiunge,
   campi di U3/R16/C11 dalla netlist dello schema;
3. intaglio allargato a sinistra fino all'inizio dell'antenna; tolta la vecchia zona "antenna" (la sostituisce la zona
   vietata dell'impronta, 5 mm oltre l'antenna);
4. tolte tutte le piste e vie, ridisegnata la coppia USB con usb_coppia.py (DEC-041), spostati i componenti attorno;
5. testi della serigrafia del retro a 1,0 mm (FIN-005).

Ritocchi a mano fatti una volta dopo lo sbroglio (2026-11-08), da rifare se si risbroglia:
- il tratto +5V bloccato sotto R4 (da U1 pin 5 a x = 131,26 mm) va collegato al pad 2 di F1 con una pista 0,3 mm
  (131,26; 122,555) -> (131,26; 128,8) -> (130,39; 129,65): Freerouting lo considera gia' collegato;
- collegamento diretto +3V3 da C6 al pin 1 del modulo, pista 0,4 mm su F.Cu sotto il modulo:
  via del pin 1 (140,41; 103,0) -> (140,41; 104,5) -> (127,6; 104,5) -> (127,6; 108,675) -> C6 pad 1, togliendo le piste GND
  di Freerouting che lo incrociavano (il piano GND le sostituisce) e aggiungendo una via GND a (139,5; 103,5) per
  l'isola di piano sopra la nuova pista;
- etichetta "USB" del retro sotto J1, a (133,66; 139,0).
"""
import os
import re
import subprocess
import sys

import pcbnew

HERE = os.path.dirname(os.path.abspath(__file__))
HW = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import usb_coppia  # noqa: E402

PRJ = os.path.join(HW, "policlock-main")
PCB = os.path.join(PRJ, "policlock-main.kicad_pcb")
SCH = os.path.join(PRJ, "policlock-main.kicad_sch")
LIBFP = os.path.join(HW, "lib", "PoliClock.pretty")
KFP = r"C:\Program Files\KiCad\10.0\share\kicad\footprints"
KICAD_CLI = os.environ.get("KICAD_CLI", r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe")
MM = pcbnew.FromMM
T = pcbnew.ToMM
OX, OY = 100.0, 100.0
cestino = []                      # oggetti tolti: restano referenziati (tipi SWIG stabili)


def V(x, y):
    return pcbnew.VECTOR2I(MM(x), MM(y))


# ------------------------------------------------------------------ 1. impronta di progetto
def crea_impronta():
    fp = pcbnew.FootprintLoad(os.path.join(KFP, "RF_Module.pretty"), "ESP32-C3-WROOM-02")
    for p in list(fp.Pads()):
        if p.GetNumber() == "19" and p.GetAttribute() == pcbnew.PAD_ATTRIB_PTH:
            fp.Remove(p)
            cestino.append(p)
    ep = [p for p in fp.Pads() if p.GetNumber() == "19"][0]       # EPAD 2,9 x 2,9 mm
    cx, cy = T(ep.GetPosition().x), T(ep.GetPosition().y)
    for dx in (-0.55, 0.55):
        for dy in (-0.55, 0.55):
            v = pcbnew.PAD(fp)
            v.SetNumber("19")
            v.SetAttribute(pcbnew.PAD_ATTRIB_PTH)
            v.SetShape(pcbnew.PAD_SHAPE_CIRCLE)
            v.SetSize(V(0.7, 0.7))
            v.SetDrillSize(V(0.3, 0.3))
            ls = pcbnew.LSET()
            for lay in (pcbnew.F_Cu, pcbnew.B_Cu, pcbnew.F_Mask):
                ls.AddLayer(lay)
            v.SetLayerSet(ls)
            v.SetPosition(V(cx + dx, cy + dy))
            v.SetLocalZoneConnection(pcbnew.ZONE_CONNECTION_FULL)
            v.SetProperty(pcbnew.PAD_PROP_HEATSINK)          # come le vie termiche della libreria KiCad
            fp.Add(v)
    # serigrafia: via le linee attorno all'antenna (y < -6,6 mm, finirebbero sopra l'intaglio) e il triangolo del pin 1
    for g in list(fp.GraphicalItems()):
        if isinstance(g, pcbnew.PCB_SHAPE) and g.GetLayer() == pcbnew.F_SilkS and T(g.GetBoundingBox().GetTop()) < -6.6:
            fp.Remove(g)
            cestino.append(g)
    # nuovo segno del pin 1 fuori dalla piazzola, lato opposto all'antenna rispetto al vecchio triangolo
    d = pcbnew.PCB_SHAPE(fp, pcbnew.SHAPE_T_CIRCLE)
    d.SetLayer(pcbnew.F_SilkS)
    d.SetCenter(V(-9.82, -6.0))
    d.SetEnd(V(-9.82 + 0.15, -6.0))
    d.SetFilled(True)
    d.SetWidth(MM(0.0))
    fp.Add(d)
    fp.Reference().SetLayer(pcbnew.F_Fab)
    fp.SetLibDescription("ESP32-C3-WROOM-02 (Espressif datasheet v1.7, fig. 11-1); derivata da RF_Module:ESP32-C3-WROOM-02 "
                         "di KiCad 10: piazzole identiche, 4 vie termiche 0,3/0,7 mm nella EPAD, niente serigrafia sopra "
                         "l'antenna (PoliClock, DEC-044)")
    fp.SetFPID(pcbnew.LIB_ID("PoliClock", "ESP32-C3-WROOM-02"))
    pcbnew.FootprintSave(LIBFP, fp)
    return fp


crea_impronta()

# ------------------------------------------------------------------ netlist dello schema
NET = os.path.join(os.environ.get("TEMP", HW), "dec044.net")
subprocess.run([KICAD_CLI, "sch", "export", "netlist", "-o", NET, SCH], check=True, capture_output=True)
nl = re.sub(r"\s+", " ", open(NET, encoding="utf-8").read())


def comp(ref):
    i = nl.index('(comp (ref "%s")' % ref)
    j = min(k for k in (nl.find("(comp (ref", i + 5), nl.find("(libparts", i)) if k > 0)
    c = nl[i:j]
    f = {"Value": re.search(r'\(value "([^"]*)"\)', c).group(1),
         "Footprint": re.search(r'\(footprint "([^"]*)"\)', c).group(1)}
    for n, v in re.findall(r'\(field \(name "([^"]+)"\) "([^"]*)"\)', c):
        f[n] = v
    sp = re.search(r'\(sheetpath \(names "([^"]*)"\) \(tstamps "([^"]*)"\) ?\)', c)
    tss = re.findall(r'\(tstamps "([^"]*)"\)', c)
    return f, sp.group(2), tss[-1], sp.group(1)


pins = {}
for m in re.finditer(r'\(net \(code "?\d+"?\) \(name "([^"]*)"\)(.*?)(?=\(net \(code|$)', nl):
    for r, p in re.findall(r'\(node \(ref "([^"]+)"\) \(pin "([^"]+)"\)', m.group(2)):
        pins[(r, p)] = m.group(1)
print("nodi netlist:", len(pins))


board = pcbnew.LoadBoard(PCB)


def net(name):
    n = board.FindNet(name)
    if n is None:
        n = pcbnew.NETINFO_ITEM(board, name)
        board.Add(n)
    return n


def sincronizza(fp, ref):
    f, sheet_ts, sym_ts, sheetname = comp(ref)
    fp.SetValue(f["Value"])
    for k, v in f.items():
        if k in ("Value", "Footprint"):
            continue
        fld = fp.GetField(k) if fp.HasField(k) else None
        if fld is None:
            fld = pcbnew.PCB_FIELD(fp, fp.GetNextFieldOrdinal(), k)
            fld.SetLayer(pcbnew.F_Fab)
            fld.SetVisible(False)
            fp.Add(fld)
        fld.SetText(v)
    fp.SetPath(pcbnew.KIID_PATH(sheet_ts.rstrip("/") + "/" + sym_ts))
    for p in fp.Pads():
        n = pins.get((ref, p.GetNumber()))
        if n:
            p.SetNet(net(n))
        elif p.GetNumber():
            p.SetNetCode(0)


# ------------------------------------------------------------------ 2. U3, C11, R16
old = board.FindFootprintByReference("U3")
vecchie_reti = {p.GetNetname(): p.GetNet() for p in old.Pads()}
u3 = pcbnew.FootprintLoad(LIBFP, "ESP32-C3-WROOM-02")
u3.SetFPID(pcbnew.LIB_ID("PoliClock", "ESP32-C3-WROOM-02"))
u3.SetParent(board)
board.Add(u3)
u3.SetReference("U3")
for k in ("Sheetname", "Sheetfile"):
    fld = pcbnew.PCB_FIELD(u3, u3.GetNextFieldOrdinal(), k)
    fld.SetText(old.GetFieldText(k))
    fld.SetLayer(pcbnew.F_Fab)
    fld.SetVisible(False)
    u3.Add(fld)
u3.SetSheetname(old.GetSheetname())
u3.SetSheetfile(old.GetSheetfile())
board.Remove(old)
cestino.append(old)
sincronizza(u3, "U3")
u3.SetOrientationDegrees(-90)       # antenna verso destra (+x), pin 1-9 sul lato superiore, 10-18 su quello inferiore
j1 = board.FindFootprintByReference("J1")
asse = sum(T(p.GetPosition().x) for p in j1.Pads() if p.GetNumber() in ("B7", "B6")) / 2
u3.SetPosition(V(asse + 0.75, 110.5))
p13 = [p for p in u3.Pads() if p.GetNumber() == "13"][0]
p14 = [p for p in u3.Pads() if p.GetNumber() == "14"][0]
assert abs((T(p13.GetPosition().x) + T(p14.GetPosition().x)) / 2 - asse) < 0.01
assert T(p13.GetPosition().x) < T(p14.GetPosition().x), "D- deve stare a sinistra di D+"
inizio_antenna = T(u3.GetPosition().x) + 7.1        # bordo della zona antenna (datasheet: antenna 6 mm all'estremita')
for nome, n in vecchie_reti.items():
    if nome.startswith("unconnected-(U3-NC"):
        board.Remove(n)
        cestino.append(n)

c10 = board.FindFootprintByReference("C10")
c11 = pcbnew.FootprintLoad(os.path.join(KFP, "Capacitor_SMD.pretty"), "C_0603_1608Metric")
c11.SetFPID(pcbnew.LIB_ID("Capacitor_SMD", "C_0603_1608Metric"))
c11.SetParent(board)
board.Add(c11)
c11.SetReference("C11")
for k in ("Sheetname", "Sheetfile"):
    fld = pcbnew.PCB_FIELD(c11, c11.GetNextFieldOrdinal(), k)
    fld.SetText(c10.GetFieldText(k))
    fld.SetLayer(pcbnew.F_Fab)
    fld.SetVisible(False)
    c11.Add(fld)
c11.SetSheetname(c10.GetSheetname())
c11.SetSheetfile(c10.GetSheetfile())
c11.Reference().SetLayer(c10.Reference().GetLayer())
c11.Reference().SetVisible(c10.Reference().IsVisible())
sincronizza(c11, "C11")
sincronizza(board.FindFootprintByReference("R16"), "R16")

# ------------------------------------------------------------------ 3. intaglio e zone
VECCHIO_X = 142.16
for s in board.GetDrawings():
    if s.GetLayer() == pcbnew.Edge_Cuts and s.GetShape() == pcbnew.SHAPE_T_SEGMENT:
        for get, setp in ((s.GetStart, s.SetStart), (s.GetEnd, s.SetEnd)):
            p = get()
            if abs(T(p.x) - VECCHIO_X) < 0.001:
                setp(V(round(inizio_antenna, 3), T(p.y)))
for z in list(board.Zones()):
    if z.GetZoneName() in ("antenna", "usb_coppia_retro"):
        board.Remove(z)
        cestino.append(z)
for t in list(board.GetTracks()):
    board.Remove(t)
    cestino.append(t)

# ------------------------------------------------------------------ 4. posizionamento
POS = {   # centro (mm, origine del foglio), rotazione: colonne a sinistra del modulo, sotto l'header J2
    "C6": (126.0, 107.9, 90), "C5": (126.0, 111.3, 90), "R8": (126.0, 114.7, 90), "R9": (126.0, 118.1, 90),
    "R6": (123.5, 107.9, 90), "C7": (123.5, 111.3, 90), "R7": (123.5, 114.7, 90), "R17": (123.5, 118.1, 90),
    "R15": (121.0, 107.9, 90), "R16": (121.0, 111.3, 90), "C11": (121.0, 114.7, 90), "C10": (121.0, 118.1, 90),
    "Q1": (117.9, 117.0, 90), "C9": (118.5, 121.5, 90),
}
for ref, (x, y, r) in POS.items():
    fp = board.FindFootprintByReference(ref)
    fp.SetOrientationDegrees(r)
    fp.SetPosition(V(x, y))

# ------------------------------------------------------------------ coppia USB (DEC-041) e zona sul retro
fps = {f.GetReference(): f for f in board.GetFootprints()}
zona, lung = usb_coppia.traccia(board, fps, OX, OY)
for k, v in lung.items():
    print(f"  {k}: {v:.2f} mm")
x0, x1, y0, y1 = zona
ku = pcbnew.ZONE(board)
ku.SetIsRuleArea(True)
ku.SetZoneName("usb_coppia_retro")
ku.SetLayer(pcbnew.B_Cu)
ku.SetDoNotAllowTracks(True)
ku.SetDoNotAllowVias(True)
ku.SetDoNotAllowZoneFills(False)
ku.SetDoNotAllowPads(False)
ku.SetDoNotAllowFootprints(False)
ol = ku.Outline()
ol.NewOutline()
for x, y in ((x0, y0), (x1, y0), (x1, y1), (x0, y1)):
    ol.Append(MM(OX + x), MM(OY + y))
board.Add(ku)

# ------------------------------------------------------------------ 5. serigrafia del retro >= 1,0 mm (FIN-005)
CORTI = {"TP11 IO9_BOOT": "TP11 IO9", "TP5 UART_TX": "TP5 TX", "TP7 I2C_SDA": "TP7 SDA", "TP8 I2C_SCL": "TP8 SCL",
         "DISPLAY 1=VCC": "DISP 1=VCC", "TP1 VBUS": "TP1 VBUS"}
for d in board.GetDrawings():
    if d.GetClass() == "PCB_TEXT" and d.GetLayer() == pcbnew.B_SilkS:
        d.SetText(CORTI.get(d.GetText(), d.GetText()))
        if d.GetText() == "USB":                         # a 1,0 mm toccherebbe la piazzola di H1: va sotto J1
            d.SetPosition(V(133.66, 139.0))                # sotto J1, fra le asole del guscio
        d.SetTextSize(V(1.0, 1.0))
        d.SetTextThickness(MM(0.15))

ds = board.GetDesignSettings()
ds.m_MinSilkTextHeight = MM(1.0)
ds.m_MinSilkTextThickness = MM(0.15)
board.Save(PCB)
print("salvato", PCB, "| asse USB", round(asse, 3), "| intaglio da x =", round(inizio_antenna, 3))
