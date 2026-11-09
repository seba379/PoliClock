"""DEC-049: pin BUSY su J2 (header 1x8) per un eventuale display e-paper; modifica una tantum dello schema.

Uso:  python hardware/scripts/dec049_schema.py

- simbolo PoliClock:PinHeader_1x07_P2.54_THT -> PoliClock:PinHeader_1x08_P2.54_THT (pin 8 sotto il pin 7);
  J2 diventa "Header 1x8 2,54 mm THT", impronta PinHeader_1x08_P2.54mm_Horizontal; pin 1-7 invariati;
- J2 pin 8 = DISP_BUSY_C -> R23 1 kOhm in serie (C21190, Basic) -> DISP_BUSY -> IO1 (pin 17 del WROOM-02) e TP10;
  nessun pull esterno: pull-down interno di IO1 abilitato dal firmware (docs/04);
- note dello schema aggiornate.
"""
import os
import re
import uuid

HERE = os.path.dirname(os.path.abspath(__file__))
PRJ = os.path.join(os.path.dirname(HERE), "policlock-main")
DISP = os.path.join(PRJ, "display.kicad_sch")
MCU = os.path.join(PRJ, "mcu.kicad_sch")
ROOT = os.path.join(PRJ, "policlock-main.kicad_sch")
PATH_DISP = "/8f25dc1f-4709-513e-82c3-d067157683da/20ad8c36-b999-56cb-b9d3-b8060cbfc155"


def u():
    return str(uuid.uuid4())


def sostituisci(t, vecchio, nuovo, n=1):
    assert t.count(vecchio) == n, (vecchio[:80], t.count(vecchio))
    return t.replace(vecchio, nuovo)


def wire(x1, y1, x2, y2):
    return (f'\t(wire\n\t\t(pts\n\t\t\t(xy {x1} {y1}) (xy {x2} {y2})\n\t\t)\n\t\t(stroke\n\t\t\t(width 0)\n'
            f'\t\t\t(type default)\n\t\t)\n\t\t(uuid "{u()}")\n\t)\n')


def label(nome, x, y, rot, just):
    return (f'\t(label "{nome}"\n\t\t(at {x} {y} {rot})\n\t\t(effects\n\t\t\t(font\n\t\t\t\t(size 1.27 1.27)\n'
            f'\t\t\t)\n\t\t\t(justify {just})\n\t\t)\n\t\t(uuid "{u()}")\n\t)\n')


def global_label(nome, x, y, rot, just):
    return (f'\t(global_label "{nome}"\n\t\t(shape input)\n\t\t(at {x} {y} {rot})\n\t\t(fields_autoplaced yes)\n'
            f'\t\t(effects\n\t\t\t(font\n\t\t\t\t(size 1.27 1.27)\n\t\t\t)\n\t\t\t(justify {just})\n\t\t)\n'
            f'\t\t(uuid "{u()}")\n\t\t(property "Intersheetrefs" "${{INTERSHEET_REFS}}"\n\t\t\t(at {x} {y} 0)\n'
            f'\t\t\t(hide yes)\n\t\t\t(show_name no)\n\t\t\t(do_not_autoplace no)\n\t\t\t(effects\n\t\t\t\t(font\n'
            f'\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t)\n\t\t\t)\n\t\t)\n\t)\n')


def prop(nome, val, x, y, rot, hide, extra=""):
    h = "\t\t\t(hide yes)\n" if hide else ""
    return (f'\t\t(property "{nome}" "{val}"\n\t\t\t(at {x} {y} {rot})\n{h}\t\t\t(show_name no)\n'
            f'\t\t\t(do_not_autoplace no)\n\t\t\t(effects\n\t\t\t\t(font\n\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t)\n'
            f'{extra}\t\t\t)\n\t\t)\n')


# ------------------------------------------------------------------ foglio display
t = open(DISP, encoding="utf-8").read()
# simbolo di libreria: 8 pin, rettangolo e campi piu' in basso di 2,54 mm
i = t.index('(symbol "PoliClock:PinHeader_1x07_P2.54_THT"')
j = t.index('\n\t\t(symbol "', i + 10) if '\n\t\t(symbol "' in t[i + 10:] else t.index("\n\t)", i)
lib = t[i:j]
nuovo = lib.replace("PinHeader_1x07_P2.54_THT", "PinHeader_1x08_P2.54_THT")
nuovo = nuovo.replace('"Header 1x7 2,54 mm THT"', '"Header 1x8 2,54 mm THT"')
nuovo = nuovo.replace("PinHeader_1x07_P2.54mm_Horizontal", "PinHeader_1x08_P2.54mm_Horizontal")
nuovo = nuovo.replace("Header maschio 1x7 passo 2,54 mm", "Header maschio 1x8 passo 2,54 mm")
# campi: si spostano tutti di -2,54 (dal basso verso l'alto per non sovrapporre le sostituzioni)
for y in ("-22.86", "-20.32", "-17.78", "-15.24", "-12.7"):
    ny = "%g" % (float(y) - 2.54)
    nuovo = nuovo.replace(f"(at 0 {y} 0)", f"(at 0 {ny} 0)")
nuovo = sostituisci(nuovo, "(end 3.81 -10.16)", "(end 3.81 -12.7)")
pin7 = re.search(r'\t\t\t\t\(pin passive line\n\t\t\t\t\t\(at -3\.81 -7\.62 0\).*?\n\t\t\t\t\)\n', nuovo, re.S).group(0)
pin8 = pin7.replace("(at -3.81 -7.62 0)", "(at -3.81 -10.16 0)").replace('"7"', '"8"')
nuovo = nuovo.replace(pin7, pin7 + pin8)
t = t.replace(lib, nuovo)

# istanza J2
t = sostituisci(t, '(lib_id "PoliClock:PinHeader_1x07_P2.54_THT")', '(lib_id "PoliClock:PinHeader_1x08_P2.54_THT")')
t = sostituisci(t, '(property "Value" "Header 1x7 2,54 mm THT"\n\t\t\t(at 299.72 107.95 0)',
                '(property "Value" "Header 1x8 2,54 mm THT"\n\t\t\t(at 299.72 110.49 0)')
t = sostituisci(t, '(property "Footprint" "Connector_PinHeader_2.54mm:PinHeader_1x07_P2.54mm_Horizontal"\n\t\t\t(at 299.72 110.49 0)',
                '(property "Footprint" "Connector_PinHeader_2.54mm:PinHeader_1x08_P2.54mm_Horizontal"\n\t\t\t(at 299.72 113.03 0)')
t = sostituisci(t, '(property "Datasheet" ""\n\t\t\t(at 299.72 113.03 0)', '(property "Datasheet" ""\n\t\t\t(at 299.72 115.57 0)')
t = sostituisci(t, "Header maschio 1x7 2,54 mm a foro passante, a 90 gradi (va bene anche diritto): cavo Dupont 7 fili verso il modulo",
                "Header maschio 1x8 2,54 mm a foro passante, a 90 gradi (va bene anche diritto): cavo Dupont 7 fili "
                "sui pin 1-7 verso il modulo GC9A01; pin 8 BUSY per un eventuale e-paper (DEC-049)")
t = sostituisci(t, '\t\t(pin "7"\n\t\t\t(uuid "2cf6b077-7907-52d2-b75e-0e7447b76ec7")\n\t\t)\n',
                '\t\t(pin "7"\n\t\t\t(uuid "2cf6b077-7907-52d2-b75e-0e7447b76ec7")\n\t\t)\n'
                f'\t\t(pin "8"\n\t\t\t(uuid "{u()}")\n\t\t)\n')

# R23 1 kOhm in serie su BUSY (stessa disposizione di R8/R9)
RX, RY = 59.69, 80.01
r23 = (f'\t(symbol\n\t\t(lib_id "Device:R")\n\t\t(at {RX} {RY} 90)\n\t\t(unit 1)\n\t\t(body_style 1)\n'
       f'\t\t(exclude_from_sim no)\n\t\t(in_bom yes)\n\t\t(on_board yes)\n\t\t(in_pos_files yes)\n\t\t(dnp no)\n'
       f'\t\t(uuid "{u()}")\n'
       + prop("Reference", "R23", 60.706, round(RY - 2.54, 2), 90, False, "\t\t\t\t(justify left)\n")
       + prop("Value", "1k", 61.722, round(RY + 2.54, 2), 90, False, "\t\t\t\t(justify left)\n")
       + prop("Footprint", "Resistor_SMD:R_0603_1608Metric", RX, round(RY + 1.27, 2), 0, True)
       + prop("Datasheet", "", RX, RY, 90, True)
       + prop("Description", "Serie su BUSY (e-paper, DEC-049): limita la corrente con il modulo spento o un conflitto", RX, RY, 90, True)
       + prop("LCSC", "C21190", RX, RY, 90, True)
       + f'\t\t(pin "1"\n\t\t\t(uuid "{u()}")\n\t\t)\n\t\t(pin "2"\n\t\t\t(uuid "{u()}")\n\t\t)\n'
       f'\t\t(instances\n\t\t\t(project "policlock-main"\n\t\t\t\t(path "{PATH_DISP}"\n'
       f'\t\t\t\t\t(reference "R23")\n\t\t\t\t\t(unit 1)\n\t\t\t\t)\n\t\t\t)\n\t\t)\n\t)\n')
agg = (wire(295.91, 105.41, 288.29, 105.41) + label("DISP_BUSY_C", 288.29, 105.41, 180, "right bottom")
       + wire(53.34, RY, 55.88, RY) + global_label("DISP_BUSY", 53.34, RY, 180, "right")
       + wire(63.5, RY, 66.04, RY) + label("DISP_BUSY_C", 66.04, RY, 0, "left bottom") + r23)
t = sostituisci(t, "J2 -> modulo (serigrafia del modulo): 1 VCC, 2 GND, 3 SCL, 4 SDA, 5 DC, 6 CS, 7 RST.",
                "J2 -> modulo (serigrafia del modulo): 1 VCC, 2 GND, 3 SCL, 4 SDA, 5 DC, 6 CS, 7 RST,\\n"
                "8 BUSY (solo e-paper, DEC-049; con il GC9A01 a 7 pin resta libero).")
t = sostituisci(t, "Il modulo non ha pin BLK: la retroilluminazione segue l'alimentazione VCC.",
                "Il modulo non ha pin BLK: la retroilluminazione segue l'alimentazione VCC.\\n"
                "BUSY: uscita del display, ingresso IO1 con pull-down interno (firmware); R23 1 k limita\\n"
                "la corrente verso un modulo spento da Q1 o in caso di conflitto.")
k = t.rstrip().rindex("\n)")          # parentesi di chiusura del file
t = t[:k + 1] + agg + t[k + 1:]
open(DISP, "w", encoding="utf-8", newline="\n").write(t)

# ------------------------------------------------------------------ foglio MCU: IO1 -> DISP_BUSY
t = open(MCU, encoding="utf-8").read()
for x, y, rot, just in ((379.73, 127, 270, "right"), (140.97, 105.41, 180, "right")):
    m = re.search(r'\t\(label "IO1"\n\t\t\(at %s %s %d\)\n.*?\n\t\)\n' % (re.escape("%g" % x), re.escape("%g" % y), rot), t, re.S)
    assert m, (x, y)
    t = t.replace(m.group(0), global_label("DISP_BUSY", "%g" % x, "%g" % y, rot, just))
t = sostituisci(t, '"IO1 (libero)"', '"IO1 (DISP_BUSY)"')
open(MCU, "w", encoding="utf-8", newline="\n").write(t)

# ------------------------------------------------------------------ foglio principale: note
t = open(ROOT, encoding="utf-8").read()
t = sostituisci(t, "header 7 pin 2,54 mm THT verso il modulo GC9A01 (VCC, GND, SCL, SDA, DC, CS, RST),",
                "header 8 pin 2,54 mm THT verso il modulo GC9A01 (VCC, GND, SCL, SDA, DC, CS, RST sui pin 1-7;\\n"
                "   pin 8 BUSY per un eventuale e-paper, DEC-049),")
t = sostituisci(t, "IO0, IO1 liberi su punti di test | IO2 I2C_SDA",
                "IO0 libero su TP9 | IO1 DISP_BUSY (J2 pin 8, TP10) | IO2 I2C_SDA")
open(ROOT, "w", encoding="utf-8", newline="\n").write(t)
# ------------------------------------------------------------------ libreria PoliClock: simbolo 1x8 (il 1x7 resta)
LIB = os.path.join(os.path.dirname(HERE), "lib", "PoliClock.kicad_sym")
lt = open(LIB, encoding="utf-8").read()
if '(symbol "PinHeader_1x08_P2.54_THT"' not in lt:
    sym = "\n".join(r[1:] if r.startswith("\t") else r for r in nuovo.split("\n"))
    sym = sym.replace('(symbol "PoliClock:PinHeader_1x08_P2.54_THT"', '(symbol "PinHeader_1x08_P2.54_THT"', 1)
    k = lt.rstrip().rindex("\n)")
    lt = lt[:k + 1] + "\t" + sym.rstrip() + "\n" + lt[k + 1:]
    open(LIB, "w", encoding="utf-8", newline="\n").write(lt)
print("schema aggiornato: J2 1x8, R23, DISP_BUSY su IO1")
