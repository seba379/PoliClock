"""Generate the PoliClock KiCad 10 schematic (main board)."""
import json
import os
import sys
from kilib import Library
from schgen import Sheet, U, snap

HW = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIBF = f"{HW}/lib/PoliClock.kicad_sym"
L = Library({"PoliClock": LIBF})

R0603 = "Resistor_SMD:R_0603_1608Metric"
C0603 = "Capacitor_SMD:C_0603_1608Metric"
C0805 = "Capacitor_SMD:C_0805_2012Metric"
RES = {"0": "C21189", "10": "C22859", "22": "C23345", "100": "C22775", "1k": "C21190",
       "4.7k": "C23162", "5.1k": "C23186", "10k": "C25804", "100k": "C25803"}
CAP = {"100nF": ("C14663", C0603), "1uF": ("C15849", C0603), "4.7uF": ("C19666", C0603), "10uF": ("C19702", C0603),
       "22uF": ("C45783", C0805)}
TP_FP = "TestPoint:TestPoint_Pad_D1.5mm"

DS_ESP = "https://www.espressif.com/sites/default/files/documentation/esp32-c3-mini-1_datasheet_en.pdf"
DS_USBLC6 = "https://www.st.com/resource/en/datasheet/usblc6-2.pdf"
DS_LDO = "https://www.ti.com/lit/ds/symlink/tlv755p.pdf"
DS_AO3401 = "https://www.aosmd.com/res/datasheets/AO3401A.pdf"
DS_AO3400 = "https://www.aosmd.com/res/datasheets/AO3400A.pdf"
DS_PTC = "https://www.lcsc.com/datasheet/C2977522.pdf"


def R(sh, ref, val, x, y, n1, n2, rot=0, dnp=False, kind1=None, kind2=None, note=""):
    c = sh.add(L, "Device:R", ref, val + ("Ω" if val[-1].isdigit() else ""), x, y, rot=rot,
               fp=R0603, lcsc=RES[val], dnp=dnp, desc=note,
               ref_off=(2.54, -1.27) if rot == 0 else (-2.54, -2.54),
               val_off=(2.54, 1.27) if rot == 0 else (-2.54, 3.81))
    sh.conn(L, c, "1", n1, kind1)
    sh.conn(L, c, "2", n2, kind2)
    return c


def C(sh, ref, val, x, y, n1, n2, kind1=None, kind2=None, dnp=False):
    lc, fp = CAP[val]
    c = sh.add(L, "Device:C", ref, val, x, y, fp=fp, lcsc=lc, dnp=dnp)
    sh.conn(L, c, "1", n1, kind1)
    sh.conn(L, c, "2", n2, kind2)
    return c


def TP(sh, ref, x, y, net, kind=None, name=""):
    c = sh.add(L, "Connector:TestPoint", ref, name or net, x, y, fp=TP_FP, in_bom=False)
    sh.conn(L, c, "1", net, kind)
    return c


def flag_label(sh, net, x, y):
    x, y = snap(x), snap(y)
    from schgen import PWRN
    PWRN[sh.project] = PWRN.get(sh.project, 0) + 1
    sh.add(L, "power:PWR_FLAG", f"#FLG{PWRN[sh.project]:03d}", "PWR_FLAG", x, y)
    sh.wire((x, y), (x, snap(y + 2.54)))
    sh.label((x, snap(y + 2.54)), (0, 1), net)


def project_files(d, name, sheets_desc):
    os.makedirs(d, exist_ok=True)
    pro = {"meta": {"filename": f"{name}.kicad_pro", "version": 3},
           "schematic": {"legacy_lib_dir": "", "legacy_lib_list": []},
           "sheets": sheets_desc,
           "text_variables": {}}
    json.dump(pro, open(f"{d}/{name}.kicad_pro", "w", encoding="utf-8", newline="\n"), indent=2)
    open(f"{d}/sym-lib-table", "w", encoding="utf-8", newline="\n").write(
        '(sym_lib_table\n\t(version 7)\n\t(lib (name "PoliClock")(type "KiCad")'
        '(uri "${KIPRJMOD}/../lib/PoliClock.kicad_sym")(options "")(descr "Simboli PoliClock (LCSC/easyeda2kicad)"))\n)\n')
    open(f"{d}/fp-lib-table", "w", encoding="utf-8", newline="\n").write(
        '(fp_lib_table\n\t(version 7)\n\t(lib (name "PoliClock")(type "KiCad")'
        '(uri "${KIPRJMOD}/../lib/PoliClock.pretty")(options "")(descr "Footprint PoliClock (LCSC/easyeda2kicad)"))\n)\n')


# =====================================================================================
# MAIN BOARD
# =====================================================================================
P = "policlock-main"
D = f"{HW}/{P}"
ROOT = U(P + "/root")
root = Sheet(P, "root", f"{P}.kicad_sch", ROOT, "/" + ROOT, title="PoliClock - scheda principale",
             comment="Schema gerarchico. Rev 0.2 NON validata: revisione visiva del proprietario richiesta.\n"
                     "ESP32-C3-MINI-1-H4X, USB-C, LDO TLV75533, display GC9A01 su modulo 7 pin (DEC-034).\n"
                     "RTC esterno: modulo Adafruit DS3231 STEMMA QT su J4 (DEC-024).")

subs = [("USB e alimentazione", "usb_alimentazione.kicad_sch"), ("MCU", "mcu.kicad_sch"),
        ("Display (modulo 7 pin)", "display.kicad_sch"), ("Periferiche I2C e pulsante", "periferiche.kicad_sch")]
sheets = {}
for i, (nm, fn) in enumerate(subs):
    sid = root.subsheet(nm, fn, 30 + i * 90, 40, 70, 30, i + 2)
    sheets[fn] = Sheet(P, nm, fn, ROOT, f"/{ROOT}/{sid}", title=f"PoliClock main - {nm}")

root.text("""Blocchi (vedi docs/02-architettura-hardware.md e docs/12-selezione-componenti.md):
 - USB e alimentazione: USB-C 2.0 (CC 5,1 k), PTC 500 mA, ESD USBLC6-2SC6, LDO TLV75533 (stabile con MLCC), punti di test.
 - MCU: ESP32-C3-MINI-1-H4X, RC su EN, disaccoppiamento; nessun tasto (DEC-039): EN e IO9 sui punti di test TP6/TP11.
 - Display: header 7 pin 2,54 mm verso il modulo GC9A01 (VCC, GND, SCL, SDA, DC, CS, RST),
   alimentazione del modulo commutata da Q1 per spegnerlo di notte (DEC-034). Niente touch.
 - Periferiche: pull-up I2C, connettori JST-SH 4 poli tipo Qwiic per SHT40 (J3) e modulo RTC DS3231 (J4),
   pulsante utente remoto su connettore (J5).

Assegnazione GPIO (ESP32-C3-MINI-1):
 IO0, IO1 liberi su punti di test | IO2 I2C_SDA | IO3 BTN_USER | IO4 LCD_DC | IO5 LCD_RST | IO6 LCD_SCLK
 IO7 LCD_MOSI | IO8 I2C_SCL | IO9 BOOT | IO10 LCD_CS | IO18 USB_D- | IO19 USB_D+ | IO20 (RXD0) DISP_EN_N
 IO21 (TXD0) UART_TX su punto di test.  Strapping: IO2 e IO8 con pull-up 4,7 k (I2C), IO9 pull-up 10 k.

Indirizzi I2C: SHT40 0x44, DS3231 0x68 (EEPROM assente sul modulo Adafruit).""", 30, 90)

# ----------------------------------------------------------------- USB e alimentazione
s = sheets["usb_alimentazione.kicad_sch"]
s.box(15, 25, 175, 175, "Ingresso USB-C, CC, ESD")
j1 = s.add(L, "Connector:USB_C_Receptacle_USB2.0_16P", "J1", "TYPE-C-31-M-12", 70, 95, lcsc="C165948",
           fp="PoliClock:USB_C_Receptacle_HRO_TYPE-C-31-M-12",
           ds="https://www.lcsc.com/datasheet/C165948.pdf",
           desc="Ricettacolo USB-C 16P HRO, solo USB 2.0 (footprint libreria KiCad dal disegno HRO)")
for p in ("A1", "A12", "B1", "B12", "SH"):
    s.conn(L, j1, p, "GND")
for p in ("A4", "A9", "B4", "B9"):
    s.conn(L, j1, p, "VBUS")
s.conn(L, j1, "A5", "CC1")
s.conn(L, j1, "B5", "CC2")
s.conn(L, j1, "A6", "USB_DP_C")
s.conn(L, j1, "B6", "USB_DP_C")
s.conn(L, j1, "A7", "USB_DN_C")
s.conn(L, j1, "B7", "USB_DN_C")
s.nc(j1, "A8")
s.nc(j1, "B8")
R(s, "R1", "5.1k", 30, 145, "CC1", "GND", note="CC1 pull-down Rd 5,1 k (sink USB-C)")
R(s, "R2", "5.1k", 45, 145, "CC2", "GND", note="CC2 pull-down Rd 5,1 k (sink USB-C)")
u1 = s.add(L, "Power_Protection:USBLC6-2SC6", "U1", "USBLC6-2SC6", 120, 120, lcsc="C7519", ds=DS_USBLC6)
# canali scelti per il layout (DEC-041): I/O1 (pin 1/6) su D-, I/O2 (pin 3/4) su D+, passaggio diretto
s.conn(L, u1, "1", "USB_DN_C")
s.conn(L, u1, "6", "USB_DN_C")
s.conn(L, u1, "3", "USB_DP_C")
s.conn(L, u1, "4", "USB_DP_C")
s.conn(L, u1, "5", "+5V")
s.conn(L, u1, "2", "GND")
R(s, "R3", "0", 150, 110, "USB_DP_C", "USB_DP", rot=90, kind2="global", note="0 ohm: isola USB D+ (eventuale 22 ohm)")
R(s, "R4", "0", 150, 130, "USB_DN_C", "USB_DN", rot=90, kind2="global", note="0 ohm: isola USB D- (eventuale 22 ohm)")
s.text("D+/D- verso IO19/IO18 (USB Serial/JTAG nativa).\nCoppia simmetrica, stessa lunghezza e stesse vie (DEC-041), USBLC6 vicino al connettore.", 110, 150)

s.box(185, 25, 400, 175, "Protezione VBUS e regolatore 3,3 V")
f1 = s.add(L, "Device:Polyfuse", "F1", "BSMD0805-050-12V", 210, 70, rot=90, fp="Fuse:Fuse_0805_2012Metric",
           lcsc="C2977522", ds=DS_PTC, desc="PTC BSMD0805-050-12V: hold 0,5 A / trip 1 A",
           ref_off=(-2.54, -5.08), val_off=(-5.08, 5.08))
s.conn(L, f1, "1", "VBUS")
s.conn(L, f1, "2", "+5V")
C(s, "C1", "1uF", 235, 85, "+5V", "GND")       # C1 + C2 < 10 uF su VBUS: spunto USB (OPEN-029)
R(s, "R5", "0", 260, 70, "+5V", "5V_LDO", rot=90, note="0 ohm: isola il regolatore per il bring-up")
C(s, "C2", "4.7uF", 285, 85, "5V_LDO", "GND")
u2 = s.add(L, "Regulator_Linear:TLV75533PDBV", "U2", "TLV75533PDBVR", 315, 70, lcsc="C404027", ds=DS_LDO,
           desc="LDO 500 mA, stabile con MLCC >= 1 uF (TI SBVS320D)")
s.conn(L, u2, "1", "5V_LDO")
s.conn(L, u2, "3", "5V_LDO")
s.conn(L, u2, "5", "+3V3")
s.conn(L, u2, "2", "GND")
s.nc(u2, "4")
C(s, "C3", "10uF", 345, 85, "+3V3", "GND")
C(s, "C4", "100nF", 360, 85, "+3V3", "GND")
s.text("TLV75533: C2 (ingresso) e C3/C4 (uscita) adiacenti ai pin, ritorno GND corto.\n"
       "C1 1 uF + C2 4,7 uF: capacita' su VBUS < 10 uF per limitare lo spunto USB (OPEN-029).\n"
       "Stabile con ceramici >= 1 uF effettivi; Pd ~ (5-3,3) V x I, RthJA 231 C/W (JEDEC).", 290, 100)
s.text("PWR_FLAG", 200, 125, 1.27, True)
s.flag(L, "VBUS", 200, 135)
s.flag(L, "GND", 215, 135)
s.flag(L, "+5V", 230, 135)
flag_label(s, "5V_LDO", 245, 135)
s.text("Punti di test", 290, 125, 1.27, True)
TP(s, "TP1", 290, 140, "VBUS")
TP(s, "TP2", 305, 140, "+5V")
TP(s, "TP3", 320, 140, "+3V3")
TP(s, "TP4", 335, 140, "GND")

# ----------------------------------------------------------------- MCU
s = sheets["mcu.kicad_sch"]
s.box(60, 20, 260, 190, "Modulo ESP32-C3-MINI-1-H4X (chip v1.1, 4 MB flash, antenna PCB oltre il bordo)")
u3 = s.add(L, "PoliClock:ESP32-C3-MINI-1", "U3", "ESP32-C3-MINI-1-H4X", 160, 105, lcsc="C41349510",
           ds=DS_ESP, desc="Variante Recommended (DEC-035); radio non usata in V1 (DEC-012)")
pmap = {"3": "+3V3", "5": "I2C_SDA", "6": "BTN_USER", "8": "EN", "12": "IO0", "13": "IO1",
        "16": "LCD_CS", "18": "LCD_DC", "19": "LCD_RST", "20": "LCD_SCLK", "21": "LCD_MOSI",
        "22": "I2C_SCL", "23": "IO9_BOOT", "26": "USB_DN", "27": "USB_DP", "30": "DISP_EN_N", "31": "UART_TX"}
local = {"EN", "IO9_BOOT", "UART_TX", "IO0", "IO1"}
for num, (px, py, prot, name, typ) in u3.pins.items():
    if name == "NC":
        s.nc(u3, num)
    elif name == "GND" and int(num) >= 36:
        continue
    elif name == "GND":
        s.conn(L, u3, num, "GND")
    else:
        net = pmap[num]
        s.conn(L, u3, num, net, None if net == "+3V3" else ("label" if net in local else "global"))
# right-side GND pins (36..53) joined by a vertical wire, one GND symbol
ends = []
for n in range(36, 54):
    (x, y), d = s.stub(u3, str(n), 5.08)
    ends.append((x, y))
ends.sort(key=lambda p: p[1])
for a, b in zip(ends, ends[1:]):
    s.wire(a, b)
for p in ends[1:-1]:
    s.items.append(["junction", ["at", p[0], p[1]], ["diameter", 0], ["color", 0, 0, 0, 0],
                    ["uuid", s.uid("j")]])
s.wire(ends[-1], (ends[-1][0], snap(ends[-1][1] + 5.08)))
s.power(L, "GND", (ends[-1][0], snap(ends[-1][1] + 5.08)), (0, 1))
from sexp import Sym as _S
for it in s.items:
    if it and it[0] == "junction":
        it[0] = _S("junction")
        it[1][0] = _S("at")
        it[2][0] = _S("diameter")
        it[3][0] = _S("color")
        it[4][0] = _S("uuid")

C(s, "C5", "10uF", 80, 40, "+3V3", "GND")
C(s, "C6", "100nF", 92, 40, "+3V3", "GND")
s.text("Disaccoppiamento vicino al pin 3V3 del modulo", 75, 52)

s.box(270, 20, 400, 100, "EN (reset) e IO9 (boot): senza tasti (DEC-039)")
R(s, "R6", "10k", 285, 45, "+3V3", "EN", note="RC su EN (Espressif: R 10 k, C 1 uF)")
C(s, "C7", "1uF", 300, 60, "EN", "GND")
R(s, "R7", "10k", 285, 80, "+3V3", "IO9_BOOT", note="Pull-up strapping IO9 (SPI boot)")
s.text("Nessun tasto (DEC-039): flash e reset via USB nativa.\nRecupero: collegare TP11 (IO9) a GND e dare\n"
       "alimentazione o portare TP6 (EN) a GND e rilasciarlo\n-> download (IO9=0, IO8=1).", 310, 40)

s.box(270, 110, 400, 150, "Debug")
TP(s, "TP5", 290, 125, "UART_TX", name="UART_TX (IO21)")
TP(s, "TP6", 320, 125, "EN", name="EN")
TP(s, "TP11", 305, 125, "IO9_BOOT", name="IO9 (BOOT)")
TP(s, "TP9", 350, 125, "IO0", name="IO0 (libero)")
TP(s, "TP10", 380, 125, "IO1", name="IO1 (libero)")
s.text("Log e flash principali via USB nativa;\nTXD0 su punto di test per debug di riserva.", 275, 143)

# ----------------------------------------------------------------- Display
s = sheets["display.kicad_sch"]
s.box(15, 20, 400, 200, "Modulo display GC9A01 1,28\" a 7 pin (DEC-034): header 2,54 mm, alimentazione commutata")
j2 = s.add(L, "PoliClock:HXPZ2.54-1X7PWT", "J2", "HX PZ2.54-1x7P WT", 300, 95, lcsc="C46061680",
           ds="https://www.lcsc.com/datasheet/C46061680.pdf",
           desc="Header maschio 1x7 2,54 mm SMD a 90 gradi: cavo Dupont 7 fili verso il modulo")
HDR = {"1": "3V3_DISP", "2": "GND", "3": "LCD_SCLK_C", "4": "LCD_MOSI_C", "5": "LCD_DC", "6": "LCD_CS",
       "7": "LCD_RST"}
GLOB = {"LCD_CS", "LCD_DC", "LCD_RST", "LCD_SCLK", "LCD_MOSI", "DISP_EN_N"}
for p, n in HDR.items():
    s.conn(L, j2, p, n, "global" if n in GLOB else None)
s.text("J2 -> modulo (serigrafia del modulo): 1 VCC, 2 GND, 3 SCL, 4 SDA, 5 DC, 6 CS, 7 RST.\n"
       "Ordine da verificare sul modulo ricevuto prima del collegamento.\n"
       "Il modulo non ha pin BLK: la retroilluminazione segue l'alimentazione VCC.", 250, 135)
R(s, "R8", "22", 60, 50, "LCD_SCLK", "LCD_SCLK_C", rot=90, kind1="global", note="Smorzamento SCLK (valore da M1)")
R(s, "R9", "22", 60, 65, "LCD_MOSI", "LCD_MOSI_C", rot=90, kind1="global", note="Smorzamento MOSI (valore da M1)")
R(s, "R15", "10k", 210, 50, "3V3_DISP", "LCD_RST", kind2="global", note="Pull-up reset verso l'alimentazione del modulo")
s.text("Interruttore di alimentazione del modulo (notte = spento, DEC-009):\n"
       "IO20 basso -> Q1 acceso. R17 tiene Q1 spento durante reset e boot.\n"
       "Con il modulo spento il firmware porta SCLK/MOSI/DC/CS/RST a livello basso.", 30, 140)
q1 = s.add(L, "Transistor_FET:AO3401A", "Q1", "AO3401A", 110, 175, lcsc="C15127", ds=DS_AO3401)
R(s, "R16", "1k", 85, 175, "DISP_EN_N", "DISP_G", rot=90, kind1="global", note="Resistenza di gate")
s.conn(L, q1, "1", "DISP_G")
s.conn(L, q1, "2", "+3V3")
s.conn(L, q1, "3", "3V3_DISP")
R(s, "R17", "100k", 95, 160, "+3V3", "DISP_G", note="Gate verso source: modulo spento di default")
C(s, "C9", "10uF", 150, 175, "3V3_DISP", "GND")
C(s, "C10", "100nF", 165, 175, "3V3_DISP", "GND")

# ----------------------------------------------------------------- Periferiche
s = sheets["periferiche.kicad_sch"]
s.box(15, 20, 200, 110, "Bus I2C (SHT40 0x44, RTC DS3231 0x68)")
R(s, "R19", "4.7k", 35, 50, "+3V3", "I2C_SDA", kind2="global", note="Pull-up I2C SDA (anche strapping IO2)")
R(s, "R20", "4.7k", 50, 50, "+3V3", "I2C_SCL", kind2="global", note="Pull-up I2C SCL (anche strapping IO8)")
R(s, "R21", "0", 35, 85, "+3V3", "3V3_EXT", rot=90, note="0 ohm: isola l'alimentazione dei moduli esterni")
TP(s, "TP7", 100, 50, "I2C_SDA", "global")
TP(s, "TP8", 120, 50, "I2C_SCL", "global")
s.text("Il modulo Adafruit DS3231 ha gia' pull-up 10 k verso Vin:\nin parallelo a R19/R20 -> ~3,2 k (~2,4 k se anche il breakout SHT40\nha pull-up 10 k, da verificare), accettabile.", 80, 75)

s.box(210, 20, 400, 110, "Connettori Qwiic / STEMMA QT (JST-SH 4 poli: 1 GND, 2 3V3, 3 SDA, 4 SCL)")
for ref, x, nm in (("J3", 250, "modulo SHT40"), ("J4", 330, "modulo RTC DS3231")):
    j = s.add(L, "PoliClock:SM04B-SRSS-TB", ref, "SM04B-SRSS-TB", x, 70, lcsc="C160404", desc=f"Qwiic/STEMMA QT: {nm}",
              ds="https://www.lcsc.com/datasheet/C160404.pdf")
    s.conn(L, j, "1", "GND", length=5.08)
    s.conn(L, j, "2", "3V3_EXT", length=7.62)
    s.conn(L, j, "3", "I2C_SDA", "global", length=10.16)
    s.conn(L, j, "4", "I2C_SCL", "global", length=12.7)
    s.nc(j, "5")
    s.nc(j, "6")
s.text("J3: modulo breakout SHT40 commerciale (header 2,54 mm), cavo JST-SH 4 poli -> jumper\n"
       "femmina; ordine dei pin dalla serigrafia del modulo (DEC-028).\n"
       "J4: modulo Adafruit DS3231 Precision RTC STEMMA QT (5188) con pila CR1220 (DEC-024).", 220, 90)

s.box(15, 120, 200, 200, "Pulsante utente")
j5 = s.add(L, "PoliClock:SM02B-SRSS-TB", "J5", "SM02B-SRSS-TB", 60, 165, lcsc="C160402", desc="Pulsante utente remoto",
           ds="https://www.lcsc.com/datasheet/C160402.pdf")
s.conn(L, j5, "1", "BTN_USER", "global", length=5.08)
s.conn(L, j5, "2", "GND", length=7.62)
s.nc(j5, "3")
s.nc(j5, "4")
R(s, "R22", "10k", 160, 150, "+3V3", "BTN_USER", kind2="global", note="Pull-up pulsante (attivo basso)")
C(s, "C8", "100nF", 175, 175, "BTN_USER", "GND", kind1="global")
s.text("IO3: risveglio da deep-sleep possibile (GPIO0-5).\nSolo pulsante remoto su J5 (DEC-032): nessun tasto USER su scheda.", 25, 185)

# ----------------------------------------------------------------- write main
os.makedirs(D, exist_ok=True)
root.write(f"{D}/{P}.kicad_sch", True)
for fn, sh in sheets.items():
    sh.write(f"{D}/{fn}", False)
project_files(D, P, [[ROOT, "Root"]] + [[U(P + "/" + fn), nm] for nm, fn in subs])

print("generated")
