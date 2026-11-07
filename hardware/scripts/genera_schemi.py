"""Generate the PoliClock KiCad 10 schematics (main board, display carrier)."""
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
CAP = {"100nF": ("C14663", C0603), "1uF": ("C15849", C0603), "10uF": ("C19702", C0603),
       "22uF": ("C45783", C0805)}
TP_FP = "TestPoint:TestPoint_Pad_D1.5mm"

DS_ESP = "https://www.espressif.com/sites/default/files/documentation/esp32-c3-mini-1_datasheet_en.pdf"
DS_USBLC6 = "https://www.st.com/resource/en/datasheet/usblc6-2.pdf"
DS_AMS = "http://www.advanced-monolithic.com/pdf/ds1117.pdf"
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
             comment="Schema gerarchico. Rev 0.1 NON validata: revisione visiva del proprietario richiesta.\n"
                     "ESP32-C3-MINI-1-N4, USB-C, AMS1117-3.3, FFC 16 poli verso portadisplay.\n"
                     "RTC esterno: modulo Adafruit DS3231 STEMMA QT su J4 (DEC-024).")

subs = [("USB e alimentazione", "usb_alimentazione.kicad_sch"), ("MCU", "mcu.kicad_sch"),
        ("Display (cavo FFC)", "display.kicad_sch"), ("Periferiche I2C e pulsante", "periferiche.kicad_sch")]
sheets = {}
for i, (nm, fn) in enumerate(subs):
    sid = root.subsheet(nm, fn, 30 + i * 90, 40, 70, 30, i + 2)
    sheets[fn] = Sheet(P, nm, fn, ROOT, f"/{ROOT}/{sid}", title=f"PoliClock main - {nm}")

root.text("""Blocchi (vedi docs/02-architettura-hardware.md e docs/12-selezione-componenti.md):
 - USB e alimentazione: USB-C 2.0 (CC 5,1 k), PTC 500 mA, ESD USBLC6-2SC6, LDO AMS1117-3.3, punti di test.
 - MCU: ESP32-C3-MINI-1-N4, RC su EN, tasti RESET/BOOT, disaccoppiamento.
 - Display: connettore FFC 16 poli 0,5 mm verso la schedina portadisplay, driver retroilluminazione PWM,
   predisposizione touch con resistenze 0 ohm NON montate (DEC-019).
 - Periferiche: pull-up I2C, connettori JST-SH 4 poli tipo Qwiic per SHT40 (J3) e modulo RTC DS3231 (J4),
   pulsante utente remoto su connettore (J5).

Assegnazione GPIO (ESP32-C3-MINI-1):
 IO0 TP_INT | IO1 TP_RST | IO2 I2C_SDA | IO3 BTN_USER | IO4 LCD_DC | IO5 LCD_RST | IO6 LCD_SCLK
 IO7 LCD_MOSI | IO8 I2C_SCL | IO9 BOOT | IO10 LCD_CS | IO18 USB_D- | IO19 USB_D+ | IO20 (RXD0) LCD_BL
 IO21 (TXD0) UART_TX su punto di test.  Strapping: IO2 e IO8 con pull-up 4,7 k (I2C), IO9 pull-up 10 k.

Indirizzi I2C: SHT40 0x44, DS3231 0x68 (EEPROM assente sul modulo Adafruit), touch CST816S 0x15 (da verificare).
Componenti DNP (non montati): R11 R12 R13 R14 (touch).""", 30, 90)

# ----------------------------------------------------------------- USB e alimentazione
s = sheets["usb_alimentazione.kicad_sch"]
s.box(15, 25, 175, 175, "Ingresso USB-C, CC, ESD")
j1 = s.add(L, "PoliClock:TYPE-C-31-M-12", "J1", "TYPE-C-31-M-12", 70, 95, lcsc="C165948",
           ds="https://www.lcsc.com/datasheet/C165948.pdf",
           desc="Ricettacolo USB-C 16P, solo USB 2.0")
for p in ("A1B12", "B1A12", "1", "2", "3", "4"):
    s.conn(L, j1, p, "GND")
for p in ("A4B9", "B4A9"):
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
s.conn(L, u1, "1", "USB_DP_C")
s.conn(L, u1, "6", "USB_DP_C")
s.conn(L, u1, "3", "USB_DN_C")
s.conn(L, u1, "4", "USB_DN_C")
s.conn(L, u1, "5", "+5V")
s.conn(L, u1, "2", "GND")
R(s, "R3", "0", 150, 110, "USB_DP_C", "USB_DP", rot=90, kind2="global", note="0 ohm: isola USB D+ (eventuale 22 ohm)")
R(s, "R4", "0", 150, 130, "USB_DN_C", "USB_DN", rot=90, kind2="global", note="0 ohm: isola USB D- (eventuale 22 ohm)")
s.text("D+/D- verso IO19/IO18 (USB Serial/JTAG nativa).\nLinee differenziali 90 ohm, corte, USBLC6 vicino al connettore.", 110, 150)

s.box(185, 25, 400, 175, "Protezione VBUS e regolatore 3,3 V")
f1 = s.add(L, "Device:Polyfuse", "F1", "BSMD0805-050-12V", 210, 70, rot=90, fp="Fuse:Fuse_0805_2012Metric",
           lcsc="C2977522", ds=DS_PTC, desc="PTC BSMD0805-050-12V: hold 0,5 A / trip 1 A",
           ref_off=(-2.54, -5.08), val_off=(-5.08, 5.08))
s.conn(L, f1, "1", "VBUS")
s.conn(L, f1, "2", "+5V")
C(s, "C1", "10uF", 235, 85, "+5V", "GND")
R(s, "R5", "0", 260, 70, "+5V", "5V_LDO", rot=90, note="0 ohm: isola il regolatore per il bring-up")
C(s, "C2", "10uF", 285, 85, "5V_LDO", "GND")
u2 = s.add(L, "Regulator_Linear:AMS1117-3.3", "U2", "AMS1117-3.3", 315, 70, lcsc="C6186", ds=DS_AMS)
s.conn(L, u2, "3", "5V_LDO")
s.conn(L, u2, "2", "+3V3")
s.conn(L, u2, "1", "GND")
C(s, "C3", "22uF", 345, 85, "+3V3", "GND")
C(s, "C4", "100nF", 360, 85, "+3V3", "GND")
s.text("AMS1117: Cout 22 uF (datasheet: 22 uF tantalio per la stabilita').\n"
       "Verificare stabilita' con MLCC al bring-up; Pd ~ (5-3,3) V x I.", 290, 100)
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
s.box(60, 20, 260, 190, "Modulo ESP32-C3-MINI-1-N4 (4 MB flash, antenna PCB: zona di esclusione)")
u3 = s.add(L, "PoliClock:ESP32-C3-MINI-1-N4", "U3", "ESP32-C3-MINI-1-N4", 160, 105, lcsc="C2838502",
           ds=DS_ESP, desc="Modulo Wi-Fi/BLE (radio non usata in V1, DEC-012)")
pmap = {"3": "+3V3", "5": "I2C_SDA", "6": "BTN_USER", "8": "EN", "12": "TP_INT", "13": "TP_RST",
        "16": "LCD_CS", "18": "LCD_DC", "19": "LCD_RST", "20": "LCD_SCLK", "21": "LCD_MOSI",
        "22": "I2C_SCL", "23": "IO9_BOOT", "26": "USB_DN", "27": "USB_DP", "30": "LCD_BL", "31": "UART_TX"}
local = {"EN", "IO9_BOOT", "UART_TX"}
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

s.box(270, 20, 400, 100, "EN (reset) e BOOT")
R(s, "R6", "10k", 285, 45, "+3V3", "EN", note="RC su EN (Espressif: R 10 k, C 1 uF)")
C(s, "C7", "1uF", 300, 60, "EN", "GND")
sw1 = s.add(L, "PoliClock:TS-1088-AR02016", "SW1", "RESET", 340, 45, lcsc="C720477",
            ds="https://www.lcsc.com/datasheet/C720477.pdf", desc="Tasto 4x3 mm (DEC-029)")
s.conn(L, sw1, "1", "EN")
s.conn(L, sw1, "2", "GND")
R(s, "R7", "10k", 285, 80, "+3V3", "IO9_BOOT", note="Pull-up strapping IO9 (SPI boot)")
sw2 = s.add(L, "PoliClock:TS-1088-AR02016", "SW2", "BOOT", 340, 80, lcsc="C720477",
            ds="https://www.lcsc.com/datasheet/C720477.pdf", desc="Tasto 4x3 mm (DEC-029)")
s.conn(L, sw2, "1", "IO9_BOOT")
s.conn(L, sw2, "2", "GND")
s.text("Download: tenere BOOT e premere/rilasciare RESET (IO9=0, IO8=1).", 275, 92)

s.box(270, 110, 400, 150, "Debug")
TP(s, "TP5", 290, 125, "UART_TX", name="UART_TX (IO21)")
TP(s, "TP6", 320, 125, "EN", name="EN")
s.text("Log e flash principali via USB nativa;\nTXD0 su punto di test per debug di riserva.", 275, 138)

# ----------------------------------------------------------------- Display
s = sheets["display.kicad_sch"]
s.box(15, 20, 400, 200, "Collegamento alla schedina portadisplay (FFC 16 poli, passo 0,5 mm, contatti in basso)")
j2 = s.add(L, "PoliClock:AFC01-S16FCA-00", "J2", "AFC01-S16FCA-00", 300, 95, lcsc="C262665",
           ds="https://www.lcsc.com/datasheet/C262665.pdf", desc="FFC/FPC ZIF 16P 0,5 mm, H 2,0 mm")
FFC = {"1": "GND", "2": "3V3_DISP", "3": "3V3_DISP", "4": "GND", "5": "LCD_SCLK_C", "6": "GND",
       "7": "LCD_MOSI_C", "8": "LCD_CS", "9": "LCD_DC", "10": "LCD_RST", "11": "GND", "12": "TP_SDA",
       "13": "TP_SCL", "14": "TP_INT", "15": "TP_RST", "16": "LCD_LEDK", "17": "GND", "18": "GND"}
GLOB = {"LCD_CS", "LCD_DC", "LCD_RST", "TP_INT", "TP_RST", "LCD_SCLK", "LCD_MOSI", "LCD_BL", "I2C_SDA", "I2C_SCL"}
for p, n in FFC.items():
    s.conn(L, j2, p, n, "global" if n in GLOB else None)
s.text("Pinout cavo (identico sulla portadisplay):\n 1 GND  2 3V3  3 3V3  4 GND  5 SCLK  6 GND  7 MOSI  8 CS\n"
       " 9 DC  10 RST  11 GND  12 TP_SDA  13 TP_SCL  14 TP_INT  15 TP_RST  16 LEDK\n"
       "Orientamento cavo (tipo A/B) da fissare nel layout: pin n -> pin n.", 320, 130)
R(s, "R8", "22", 60, 50, "LCD_SCLK", "LCD_SCLK_C", rot=90, kind1="global", note="Smorzamento SCLK (valore da M1)")
R(s, "R9", "22", 60, 65, "LCD_MOSI", "LCD_MOSI_C", rot=90, kind1="global", note="Smorzamento MOSI (valore da M1)")
R(s, "R10", "0", 60, 85, "+3V3", "3V3_DISP", rot=90, note="0 ohm: isola l'alimentazione del display")
s.text("Touch predisposto (DEC-019): R11-R14 NON montati.\nMontare R11/R12 per collegare il touch al bus I2C.", 115, 100)
R(s, "R11", "0", 130, 120, "I2C_SDA", "TP_SDA", rot=90, dnp=True, kind1="global", note="DNP: touch SDA")
R(s, "R12", "0", 130, 135, "I2C_SCL", "TP_SCL", rot=90, dnp=True, kind1="global", note="DNP: touch SCL")
R(s, "R13", "10k", 175, 125, "+3V3", "TP_INT", dnp=True, kind2="global", note="DNP: pull-up INT touch")
R(s, "R14", "10k", 190, 125, "+3V3", "TP_RST", dnp=True, kind2="global", note="DNP: pull-up RST touch")
R(s, "R15", "10k", 210, 50, "+3V3", "LCD_RST", kind2="global", note="Pull-up reset pannello")
s.text("Retroilluminazione: LEDA a 3V3 sulla portadisplay, LEDK commutato a massa.\n"
       "R18 limita la corrente: valore TBD dal datasheet del pannello acquistato.", 30, 150)
q1 = s.add(L, "Transistor_FET:AO3400A", "Q1", "AO3400A", 100, 175, lcsc="C20917", ds=DS_AO3400)
R(s, "R16", "100", 75, 175, "LCD_BL", "BL_G", rot=90, kind1="global", note="Resistenza di gate")
s.conn(L, q1, "1", "BL_G")
s.conn(L, q1, "2", "GND")
s.conn(L, q1, "3", "BL_D")
R(s, "R17", "100k", 88, 188, "BL_G", "GND", note="Gate a massa: retroilluminazione spenta al reset")
R(s, "R18", "10", 130, 170, "LCD_LEDK", "BL_D", note="Limitazione corrente LED (TBD da datasheet pannello)")

# ----------------------------------------------------------------- Periferiche
s = sheets["periferiche.kicad_sch"]
s.box(15, 20, 200, 110, "Bus I2C (SHT40 0x44, RTC DS3231 0x68, touch 0x15)")
R(s, "R19", "4.7k", 35, 50, "+3V3", "I2C_SDA", kind2="global", note="Pull-up I2C SDA (anche strapping IO2)")
R(s, "R20", "4.7k", 50, 50, "+3V3", "I2C_SCL", kind2="global", note="Pull-up I2C SCL (anche strapping IO8)")
R(s, "R21", "0", 35, 85, "+3V3", "3V3_EXT", rot=90, note="0 ohm: isola l'alimentazione dei moduli esterni")
TP(s, "TP7", 100, 50, "I2C_SDA", "global")
TP(s, "TP8", 120, 50, "I2C_SCL", "global")
s.text("Il modulo Adafruit DS3231 ha gia' pull-up 10 k verso Vin:\nin parallelo a R19/R20 -> ~3,2 k, accettabile.", 80, 75)

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

# =====================================================================================
# DISPLAY CARRIER
# =====================================================================================
P = "policlock-display"
D = f"{HW}/{P}"
ROOT = U(P + "/root")
s = Sheet(P, "root", f"{P}.kicad_sch", ROOT, "/" + ROOT, paper="A4", title="PoliClock - schedina portadisplay",
          comment="Solo connettori e condensatori. Pinout pannello da rif. Waveshare 1.28inch Touch LCD\n"
                  "(GC9A01 + CST816S, FPC 18 poli): CONFERMARE sul pannello acquistato (OPEN-016).")
j1 = s.add(L, "PoliClock:AFC01-S16FCA-00", "J1", "AFC01-S16FCA-00", 60, 95, lcsc="C262665", desc="Cavo FFC verso scheda principale",
           ds="https://www.lcsc.com/datasheet/C262665.pdf")
CAB = {"1": "GND", "2": "+3V3", "3": "+3V3", "4": "GND", "5": "LCD_SCLK", "6": "GND", "7": "LCD_MOSI",
       "8": "LCD_CS", "9": "LCD_DC", "10": "LCD_RST", "11": "GND", "12": "TP_SDA", "13": "TP_SCL",
       "14": "TP_INT", "15": "TP_RST", "16": "LCD_LEDK", "17": "GND", "18": "GND"}
for p, n in CAB.items():
    s.conn(L, j1, p, n)
j2 = s.add(L, "PoliClock:AFC01-S18FCA-00", "J2", "AFC01-S18FCA-00", 200, 95, lcsc="C262666",
           ds="https://www.lcsc.com/datasheet/C262666.pdf",
           desc="FPC 18P 0,5 mm: passo e lato contatti da confermare sul pannello acquistato")
PAN = {"1": "GND", "2": "TP_INT", "3": "TP_SCL", "4": "TP_SDA", "5": "TP_RST", "6": "+3V3", "7": "GND",
       "8": "+3V3", "9": "LCD_DC", "10": "LCD_MOSI", "12": "LCD_SCLK", "13": "LCD_CS", "14": "LCD_RST",
       "15": "GND", "16": "LCD_LEDK", "17": "LCD_LEDA", "18": "GND", "19": "GND", "20": "GND"}
for p, n in PAN.items():
    s.conn(L, j2, p, n)
s.nc(j2, "11")
s.text("Pannello (rif. Waveshare): 1 GND, 2 TP_INT, 3 TP_SCL, 4 TP_SDA, 5 TP_RST, 6 TP_VDD,\n"
       "7 GND, 8 LCD_VDD, 9 D/C, 10 SDA(MOSI), 11 SDO (n.c.), 12 SCL(SCLK), 13 CS, 14 RST,\n"
       "15 GND, 16 LEDK, 17 LEDA, 18 GND.", 150, 140)
R(s, "R1", "0", 130, 40, "+3V3", "LCD_LEDA", rot=90, note="0 ohm: anodo retroilluminazione (resistenza se richiesta dal pannello)")
C(s, "C1", "10uF", 150, 55, "+3V3", "GND")
C(s, "C2", "100nF", 162, 55, "+3V3", "GND")
C(s, "C3", "100nF", 174, 55, "+3V3", "GND")
s.text("C1 bulk, C2 LCD_VDD, C3 TP_VDD: vicino al connettore del pannello.", 140, 70)
s.flag(L, "+3V3", 30, 160)
s.flag(L, "GND", 45, 160)
os.makedirs(D, exist_ok=True)
s.write(f"{D}/{P}.kicad_sch", True)
project_files(D, P, [[ROOT, "Root"]])

print("generated")
