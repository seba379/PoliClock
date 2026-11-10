"""DEC-049: J2 header 1x8 (pin 8 = BUSY per un eventuale e-paper), R23 1 kOhm in serie, rete DISP_BUSY su IO1.

Modifica una tantum del .kicad_pcb (Python di KiCad 10), dopo dec049_schema.py:
  "C:/Program Files/KiCad/10.0/bin/python.exe" hardware/scripts/dec049_pcb.py
  "C:/Program Files/KiCad/10.0/bin/python.exe" hardware/scripts/sbroglia_main.py --conserva
  "C:/Program Files/KiCad/10.0/bin/python.exe" hardware/scripts/cucitura_gnd.py

- J2: impronta PinHeader_1x08_P2.54mm_Horizontal, stessa riga e stessa rotazione; con il pin 1 fermo il pin 8
  cadrebbe a x = 127,66 sotto il corpo di U3 (da x = 127,51): l'header si sposta di un passo (2,54 mm) a
  sinistra, cosi' il pin 8 occupa il posto del vecchio pin 7 e il cavo Dupont a 7 fili si infila ancora
  sui pin 1-7; J2 resta a mano (attributi "a foro passante" ed "escluso dai file di posizionamento");
- R23 (0603, 1 kOhm, C21190) fra J2 pin 8 e il resto della rete, sotto J2 pin 8;
- la rete /MCU/IO1 (U3 pin 17, TP10 e le sue piste) diventa DISP_BUSY; nulla si sposta nella zona J1/U1/U3;
- si tolgono le piste delle reti di J2 e quelle di altre reti in conflitto con le nuove piazzole;
  poi sbroglia_main.py --conserva traccia solo le connessioni mancanti.

Ritocchi fatti dopo lo sbroglio (2026-11-09): DISP_BUSY passa dalla via (125,83; 100,99) sul retro sotto la fila di
piazzole superiore di U3 e scende lungo il lato destro del modulo fino alla via esistente di IO1 (67 mm, 2 vie;
rame a 0,22 mm dalla zona antenna, fuori dalla zona). Un secondo tentativo con una zona vietata temporanea lungo
l'antenna dava 76 mm e violazioni: scartato. Pista LCD_SCLK_C fra le piazzole di C5 riportata a 0,15 mm (come in
DEC-045); valore di TP10 "IO1 (DISP_BUSY)"; via GND a (130,6; 108,0) sotto U3: la pista DISP_BUSY chiudeva
un'isola del piano GND sul retro (collegata solo alla via (139,5; 103,5) e all'isola del rame superiore attorno
a U3 pin 9 e C6); poi cucitura_gnd.py.
"""
import os
import re
import subprocess
import pcbnew

HERE = os.path.dirname(os.path.abspath(__file__))
HW = os.path.dirname(HERE)
PCB = os.path.join(HW, "policlock-main", "policlock-main.kicad_pcb")
SCH = os.path.join(HW, "policlock-main", "policlock-main.kicad_sch")
KICAD_CLI = os.environ.get("KICAD_CLI", r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe")
KFP = os.environ.get("KICAD10_FOOTPRINT_DIR", r"C:\Program Files\KiCad\10.0\share\kicad\footprints")
MM = pcbnew.FromMM
T = pcbnew.ToMM
DX_J2 = -2.54
R23_POS, R23_ROT = (125.3, 105.45), 180
RETI_J2 = {"3V3_DISP", "LCD_SCLK_C", "LCD_MOSI_C", "LCD_DC", "LCD_CS", "LCD_RST", "DISP_BUSY_C"}
MONT = "a mano, parte del proprietario"

NET = os.path.join(os.environ.get("TEMP", HW), "dec049.net")
subprocess.run([KICAD_CLI, "sch", "export", "netlist", "-o", NET, SCH], check=True, capture_output=True)
nl = re.sub(r"\s+", " ", open(NET, encoding="utf-8").read())


def comp(ref):
    i = nl.index('(comp (ref "%s")' % ref)
    j = min(k for k in (nl.find("(comp (ref", i + 5), nl.find("(libparts", i)) if k > 0)
    c = nl[i:j]
    f = {"Value": re.search(r'\(value "([^"]*)"\)', c).group(1)}
    for n, v in re.findall(r'\(field \(name "([^"]+)"\) "([^"]*)"\)', c):
        f[n] = v
    sp = re.search(r'\(sheetpath \(names "([^"]*)"\) \(tstamps "([^"]*)"\) ?\)', c)
    tss = re.findall(r'\(tstamps "([^"]*)"\)', c)
    return f, sp.group(2), tss[-1]


pins = {}
for m in re.finditer(r'\(net \(code "?\d+"?\) \(name "([^"]*)"\)(.*?)(?=\(net \(code|$)', nl):
    for r, p in re.findall(r'\(node \(ref "([^"]+)"\) \(pin "([^"]+)"\)', m.group(2)):
        pins[(r, p)] = m.group(1)

board = pcbnew.LoadBoard(PCB)
cestino = []


def V(x, y):
    return pcbnew.VECTOR2I(MM(x), MM(y))


def net(name):
    n = board.FindNet(name)
    if n is None:
        n = pcbnew.NETINFO_ITEM(board, name)
        board.Add(n)
    return n


def sincronizza(fp, ref):
    f, sheet_ts, sym_ts = comp(ref)
    fp.SetValue(f["Value"])
    for k, v in f.items():
        if k in ("Value", "Footprint"):
            continue
        fld = fp.GetField(k) if fp.HasField(k) else None
        if fld is None:
            fld = pcbnew.PCB_FIELD(fp, fp.GetNextFieldOrdinal(), k)
            fld.SetLayer(pcbnew.F_Fab)
            fld.SetVisible(False)
            fld.SetPosition(fp.GetPosition())
            fp.Add(fld)
        fld.SetText(v)
    fp.SetPath(pcbnew.KIID_PATH(sheet_ts.rstrip("/") + "/" + sym_ts))
    for p in fp.Pads():
        n = pins.get((ref, p.GetNumber()))
        if n:
            p.SetNet(net(n))
        elif p.GetNumber():
            p.SetNetCode(0)


def nuova(lib, nome, ref, simile):
    fp = pcbnew.FootprintLoad(os.path.join(KFP, lib + ".pretty"), nome)
    fp.SetFPID(pcbnew.LIB_ID(lib, nome))
    fp.SetParent(board)
    board.Add(fp)
    fp.SetReference(ref)
    for k in ("Sheetname", "Sheetfile"):
        fld = pcbnew.PCB_FIELD(fp, fp.GetNextFieldOrdinal(), k)
        fld.SetText(simile.GetFieldText(k))
        fld.SetLayer(pcbnew.F_Fab)
        fld.SetVisible(False)
        fp.Add(fld)
    fp.SetSheetname(simile.GetSheetname())
    fp.SetSheetfile(simile.GetSheetfile())
    return fp


# ------------------------------------------------------------------ IO1 -> DISP_BUSY (piste comprese)
vecchia = board.FindNet("/MCU/IO1")
busy = net("DISP_BUSY")
for t in board.GetTracks():
    if t.GetNetCode() == vecchia.GetNetCode():
        t.SetNet(busy)
for ref in ("U3", "TP10"):
    for p in board.FindFootprintByReference(ref).Pads():
        if p.GetNetCode() == vecchia.GetNetCode():
            p.SetNet(busy)

# ------------------------------------------------------------------ J2 1x8, un passo a sinistra
old = board.FindFootprintByReference("J2")
vecchie_piazzole = [(p.GetNetCode(), p.GetPosition()) for p in old.Pads()]
p1 = [p for p in old.Pads() if p.GetNumber() == "1"][0].GetPosition()
j2 = nuova("Connector_PinHeader_2.54mm", "PinHeader_1x08_P2.54mm_Horizontal", "J2", old)
j2.SetOrientationDegrees(old.GetOrientationDegrees())
j2.SetPosition(pcbnew.VECTOR2I(p1.x + MM(DX_J2), p1.y))
assert [p for p in j2.Pads() if p.GetNumber() == "1"][0].GetPosition() == j2.GetPosition()
sincronizza(j2, "J2")
for k in ("Montaggio", "Description"):
    j2.GetField(k).SetVisible(False)
r = j2.Reference()
r.SetLayer(old.Reference().GetLayer())
r.SetVisible(old.Reference().IsVisible())
r.SetTextAngleDegrees(0)
cx = (min(p.GetPosition().x for p in j2.Pads()) + max(p.GetPosition().x for p in j2.Pads())) // 2
r.SetPosition(pcbnew.VECTOR2I(cx, j2.GetPosition().y - MM(2.6)))
j2.Value().SetLayer(pcbnew.F_Fab)
j2.Value().SetVisible(False)
j2.SetAttributes(pcbnew.FP_THROUGH_HOLE | pcbnew.FP_EXCLUDE_FROM_POS_FILES)
assert j2.GetFieldText("Montaggio") == MONT
board.Remove(old)
cestino.append(old)

# ------------------------------------------------------------------ R23 sotto J2 pin 8
r8 = board.FindFootprintByReference("R8")
r23 = nuova("Resistor_SMD", "R_0603_1608Metric", "R23", r8)
r23.SetOrientationDegrees(R23_ROT)
r23.SetPosition(V(*R23_POS))
sincronizza(r23, "R23")
r23.Reference().SetLayer(r8.Reference().GetLayer())
r23.Reference().SetVisible(r8.Reference().IsVisible())
r23.Reference().SetTextAngleDegrees(0)
r23.Reference().SetPosition(r23.GetPosition())
r23.SetAttributes(r8.GetAttributes())

board.Remove(vecchia)
cestino.append(vecchia)

# ------------------------------------------------------------------ piste da rifare
nuove = list(j2.Pads()) + list(r23.Pads())
tolte = 0
for t in list(board.GetTracks()):
    if t.IsLocked():
        continue
    estremi = [t.GetPosition()] if t.GetClass() == "PCB_VIA" else [t.GetStart(), t.GetEnd()]
    togli = t.GetNetname().split("/")[-1] in RETI_J2 or any(
        n == t.GetNetCode() and (e - pos).EuclideanNorm() < MM(0.05) for n, pos in vecchie_piazzole for e in estremi)
    if not togli:
        togli = any(p.GetNetCode() != t.GetNetCode() and t.IsOnLayer(l) and p.IsOnLayer(l)
                    and t.GetEffectiveShape(l).Collide(p.GetEffectiveShape(l), MM(0.2))
                    for p in nuove for l in (pcbnew.F_Cu, pcbnew.B_Cu))
    if togli:
        board.Remove(t)
        cestino.append(t)
        tolte += 1

board.Save(PCB)
print("J2 pin 1 a", T(j2.GetPosition().x), T(j2.GetPosition().y), "| pin 8 a",
      [(T(p.GetPosition().x), T(p.GetPosition().y)) for p in j2.Pads() if p.GetNumber() == "8"][0],
      "| R23 a", R23_POS, "| piste e vie tolte:", tolte)
