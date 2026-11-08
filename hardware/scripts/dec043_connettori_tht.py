"""DEC-043: J2 header 1x7 THT, J3/J4/J5 JST PH B4B-PH-K-S, saldati a mano dal proprietario.

Modifica una tantum del .kicad_pcb (dal 2026-11-08 la fonte e' il file KiCad, non i generatori):
1. sostituisce le impronte J2-J5 con quelle della libreria standard di KiCad 10, conservando
   riferimento, percorso nello schema e reti delle piazzole; attributi "a foro passante" ed
   "escluso dai file di posizionamento" (CPL di JLC), campo Montaggio = "a mano, parte del proprietario";
2. sposta J2-J5 e i componenti che intralciano (R15, R19, R20, R21, C8);
3. toglie le piste delle reti toccate e quelle in conflitto con le nuove piazzole; le altre piste restano
   (la coppia USB bloccata di DEC-041 e tutta la zona J1/U1/U3 non si toccano).
Lo sbroglio delle connessioni mancanti si fa poi con  sbroglia_main.py --conserva.

Uso:  "C:/Program Files/KiCad/10.0/bin/python.exe" hardware/scripts/dec043_connettori_tht.py
"""
import os
import pcbnew

HERE = os.path.dirname(os.path.abspath(__file__))
PCB = os.path.join(os.path.dirname(HERE), "policlock-main", "policlock-main.kicad_pcb")
FPLIB = os.environ.get("KICAD10_FOOTPRINT_DIR", r"C:\Program Files\KiCad\10.0\share\kicad\footprints")
MM = pcbnew.FromMM
MONT = "a mano, parte del proprietario"
PH = ("Connector_JST", "JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical")
PH_DS = "https://www.jst-mfg.com/product/pdf/eng/ePH.pdf"

# riferimento: (libreria, impronta, pin 1 (x, y) mm, rotazione, valore, datasheet, descrizione)
NUOVI = {
    # header a 90 gradi: corpo plastico sulla scheda (y 100,36-102,90), pin oltre il bordo superiore;
    # gli stessi fori accettano un header diritto
    "J2": ("Connector_PinHeader_2.54mm", "PinHeader_1x07_P2.54mm_Horizontal", (109.88, 104.4), 90,
           "Header 1x7 2,54 mm THT", "",
           "Header maschio 1x7 2,54 mm a foro passante, a 90 gradi (va bene anche diritto): "
           "cavo Dupont 7 fili verso il modulo"),
    "J3": PH + ((103.0, 109.0), 0, "B4B-PH-K-S", PH_DS, "JST PH 4 poli: modulo SHT40"),
    "J4": PH + ((103.0, 115.0), 0, "B4B-PH-K-S", PH_DS, "JST PH 4 poli: modulo RTC DS3231"),
    "J5": PH + ((103.0, 121.0), 0, "B4B-PH-K-S", PH_DS,
                "JST PH 4 poli: pulsante utente remoto (pin 1-2), pin 3-4 non collegati"),
}
# componenti SMD spostati per far posto ai connettori (centro mm, rotazione)
SPOSTA = {"R15": (124.3, 107.3, 0), "R21": (113.0, 108.4, 90), "R19": (113.0, 111.8, 90),
          "R20": (113.0, 115.2, 90), "C8": (113.0, 121.0, 90)}
RETI_DA_RISBROGLIARE = {"3V3_DISP", "LCD_SCLK_C", "LCD_MOSI_C", "LCD_DC", "LCD_CS", "LCD_RST",
                        "3V3_EXT", "I2C_SDA", "I2C_SCL", "BTN_USER"}

board = pcbnew.LoadBoard(PCB)


def corto(nome):
    return nome.split("/")[-1]


vecchie_piazzole = []          # (rete, posizione) delle piazzole di J2-J5 e dei componenti spostati
for ref in list(NUOVI) + list(SPOSTA):
    for p in board.FindFootprintByReference(ref).Pads():
        vecchie_piazzole.append((p.GetNetCode(), p.GetPosition()))

nuove = []
for ref, (lib, nome, (x, y), rot, valore, ds, descr) in NUOVI.items():
    old = board.FindFootprintByReference(ref)
    reti = {p.GetNumber(): p.GetNet() for p in old.Pads()}
    campi = {f.GetName(): f.GetText() for f in old.GetFields()}
    fp = pcbnew.FootprintLoad(os.path.join(FPLIB, lib + ".pretty"), nome)
    fp.SetFPID(pcbnew.LIB_ID(lib, nome))
    fp.SetParent(board)
    board.Add(fp)
    fp.SetReference(ref)
    fp.SetValue(valore)
    fp.SetPath(old.GetPath())
    fp.SetSheetname(old.GetSheetname())
    fp.SetSheetfile(old.GetSheetfile())
    fp.SetOrientationDegrees(rot)
    fp.SetPosition(pcbnew.VECTOR2I(MM(x), MM(y)))
    for nome_campo, testo in (("Datasheet", ds), ("Description", descr), ("Montaggio", MONT),
                              ("Sheetname", campi.get("Sheetname", "")), ("Sheetfile", campi.get("Sheetfile", ""))):
        f = fp.GetField(nome_campo) if fp.HasField(nome_campo) else None
        if f is None:
            f = pcbnew.PCB_FIELD(fp, fp.GetNextFieldOrdinal(), nome_campo)
            fp.Add(f)
        f.SetText(testo)
        f.SetVisible(False)
        f.SetLayer(pcbnew.F_Fab)
        f.SetPosition(fp.GetPosition())
    # riferimento sul livello F.Fab come nel resto della scheda (niente testi serigrafati sopra i corpi vicini)
    r = fp.Reference()
    r.SetLayer(pcbnew.F_Fab)
    r.SetVisible(True)
    fp.Value().SetLayer(pcbnew.F_Fab)
    fp.Value().SetVisible(False)
    cx = (min(p.GetPosition().x for p in fp.Pads()) + max(p.GetPosition().x for p in fp.Pads())) // 2
    cy = (min(p.GetPosition().y for p in fp.Pads()) + max(p.GetPosition().y for p in fp.Pads())) // 2
    r.SetPosition(pcbnew.VECTOR2I(cx, cy + MM(1.8 if ref != "J2" else -2.6)))
    r.SetTextAngleDegrees(0)
    for p in fp.Pads():
        if p.GetNumber() in reti:
            p.SetNet(reti[p.GetNumber()])
    fp.SetAttributes(pcbnew.FP_THROUGH_HOLE | pcbnew.FP_EXCLUDE_FROM_POS_FILES)
    fp.SetLocked(False)
    # reti delle piazzole di montaggio dei JST-SH (5, 6) che non esistono piu'
    orfane = [n for num, n in reti.items() if num not in {p.GetNumber() for p in fp.Pads()}]
    board.Remove(old)
    for n in orfane:
        board.Remove(n)
    nuove.append(fp)

for ref, (x, y, rot) in SPOSTA.items():
    fp = board.FindFootprintByReference(ref)
    fp.SetOrientationDegrees(rot)
    fp.SetPosition(pcbnew.VECTOR2I(MM(x), MM(y)))
    nuove.append(fp)

# piste da togliere: reti da risbrogliare, estremi sulle vecchie piazzole, conflitti con le nuove piazzole
piazzole_nuove = [p for fp in nuove for p in fp.Pads()]
tolte = 0
for t in list(board.GetTracks()):
    if t.IsLocked():
        continue
    via = t.GetClass() == "PCB_VIA"
    togli = corto(t.GetNetname()) in RETI_DA_RISBROGLIARE
    estremi = [t.GetPosition()] if via else [t.GetStart(), t.GetEnd()]
    if not togli:
        togli = any(n == t.GetNetCode() and (e - pos).EuclideanNorm() < MM(0.05)
                    for n, pos in vecchie_piazzole for e in estremi)
    if not togli:
        for p in piazzole_nuove:
            if p.GetNetCode() == t.GetNetCode():
                continue
            for lay in (pcbnew.F_Cu, pcbnew.B_Cu):
                if t.IsOnLayer(lay) and p.IsOnLayer(lay) and \
                        t.GetEffectiveShape(lay).Collide(p.GetEffectiveShape(lay), MM(0.2)):
                    togli = True
    if togli:
        board.Remove(t)
        tolte += 1
print("piste e vie tolte:", tolte)
board.Save(PCB)
print("salvato", PCB)
