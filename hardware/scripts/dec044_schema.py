"""DEC-044 e FIN-003: modifica una tantum dello schema (la fonte sono i file .kicad_sch).

1. U3: ESP32-C3-MINI-1-H4X -> ESP32-C3-WROOM-02-N4 (C2934560). Nuovo simbolo PoliClock:ESP32-C3-WROOM-02 con i pin
   nelle stesse posizioni dei segnali del simbolo MINI-1: etichette e fili restano collegati. Tolti i pin NC
   (e i loro flag) e i pin GND in eccesso (con i loro fili e simboli GND).
2. FIN-003: R16 da 1 k a 10 k (C25804); nuovo C11 10 nF (C57112) fra DISP_G e 3V3_DISP (rampa di accensione di Q1).

Uso:  python hardware/scripts/dec044_schema.py
"""
import os
import re
import uuid

HW = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIB = os.path.join(HW, "lib", "PoliClock.kicad_sym")
MCU = os.path.join(HW, "policlock-main", "mcu.kicad_sch")
DIS = os.path.join(HW, "policlock-main", "display.kicad_sch")
ROOT = os.path.join(HW, "policlock-main", "policlock-main.kicad_sch")
DS = "https://documentation.espressif.com/esp32-c3-wroom-02_datasheet_en.pdf"

# pin WROOM-02 (numero, nome, tipo) -> posizione nel simbolo (stessa del segnale sul simbolo MINI-1)
PIN = [
    ("1", "3V3", "power_in", -11.43, 25.4, 0), ("2", "EN", "input", -11.43, 12.7, 0),
    ("3", "IO4", "bidirectional", -11.43, -12.7, 0), ("4", "IO5", "bidirectional", -11.43, -15.24, 0),
    ("5", "IO6", "bidirectional", -11.43, -17.78, 0), ("6", "IO7", "bidirectional", -11.43, -20.32, 0),
    ("7", "IO8", "bidirectional", -11.43, -22.86, 0), ("8", "IO9", "bidirectional", -11.43, -25.4, 0),
    ("9", "GND", "power_in", -11.43, 30.48, 0), ("10", "IO10", "bidirectional", -11.43, -7.62, 0),
    ("11", "RXD", "bidirectional", 11.43, -25.4, 180), ("12", "TXD", "bidirectional", 11.43, -22.86, 180),
    ("13", "IO18", "bidirectional", -11.43, -33.02, 0), ("14", "IO19", "bidirectional", 11.43, -33.02, 180),
    ("15", "IO3", "bidirectional", -11.43, 17.78, 0), ("16", "IO2", "bidirectional", -11.43, 20.32, 0),
    ("17", "IO1", "bidirectional", -11.43, 0.0, 0), ("18", "IO0", "bidirectional", -11.43, 2.54, 0),
    ("19", "GND", "passive", 11.43, -10.16, 180),
]


def block(text, start):
    depth, i, instr = 0, start, False
    while True:
        c = text[i]
        if instr:
            if c == "\\":
                i += 2
                continue
            if c == '"':
                instr = False
        elif c == '"':
            instr = True
        elif c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1


def set_prop(blk, name, value):
    pat = '(property "%s" "' % name
    i = blk.index(pat) + len(pat)
    j = i
    while blk[j] != '"':
        j += 2 if blk[j] == "\\" else 1
    return blk[:i] + value + blk[j:]


def pin_sexpr(ind, num, name, typ, x, y, rot):
    f = ind + "\t\t"
    return (f"{ind}(pin {typ} line\n{ind}\t(at {x} {y} {rot})\n{ind}\t(length 2.54)\n"
            f"{ind}\t(name \"{name}\"\n{f}(effects\n{f}\t(font\n{f}\t\t(size 1.27 1.27)\n{f}\t)\n{f})\n{ind}\t)\n"
            f"{ind}\t(number \"{num}\"\n{f}(effects\n{f}\t(font\n{f}\t\t(size 1.27 1.27)\n{f}\t)\n{f})\n{ind}\t)\n{ind})")


def nuovo_simbolo(src, ind):
    """dal blocco del simbolo MINI-1 (src, indentazione ind) ricava quello WROOM-02"""
    b = src.replace('"ESP32-C3-MINI-1_0_1"', '"ESP32-C3-WROOM-02_0_1"').replace('"ESP32-C3-MINI-1_1_1"', '"ESP32-C3-WROOM-02_1_1"')
    b = re.sub(r'\(symbol "(PoliClock:)?ESP32-C3-MINI-1"', lambda m: '(symbol "%sESP32-C3-WROOM-02"' % (m.group(1) or ""), b, count=1)
    b = set_prop(b, "Value", "ESP32-C3-WROOM-02-N4")
    b = set_prop(b, "Footprint", "PoliClock:ESP32-C3-WROOM-02")
    b = set_prop(b, "Datasheet", DS)
    b = set_prop(b, "LCSC", "C2934560")
    if '(property "MPN" "' in b:
        b = set_prop(b, "MPN", "ESP32-C3-WROOM-02-N4")
    if '(property "Description" "' in b:
        b = set_prop(b, "Description", "Modulo Wi-Fi/BLE ESP32-C3, 4 MB flash, antenna PCB, 19 pin (EPAD = 19)")
    # tolgo tutti i pin e metto i nuovi al posto del primo
    spans = []
    for m in re.finditer(r"\(pin \w+ \w+\n", b):
        s = b.rindex("\n", 0, m.start()) + 1
        e = b.index("\n", block(b, m.start())) + 1
        spans.append((s, e))
    pins = "\n".join(pin_sexpr(ind + "\t\t", *p) for p in PIN) + "\n"
    out = b[:spans[0][0]] + pins
    for (s0, e0), (s1, _) in zip(spans, spans[1:] + [(len(b), None)]):
        out += b[e0:s1]
    return out


# ------------------------------------------------------------------ libreria
lib = open(LIB, encoding="utf-8").read()
if '(symbol "ESP32-C3-WROOM-02"' not in lib:
    s = lib.index('(symbol "ESP32-C3-MINI-1"')
    e = block(lib, s)
    nuovo = nuovo_simbolo(lib[s:e], "\t")
    k = lib.rstrip().rindex(")")
    lib = lib[:k].rstrip("\n") + "\n\t" + nuovo + "\n)\n"
    open(LIB, "w", encoding="utf-8", newline="\n").write(lib)

# ------------------------------------------------------------------ foglio MCU
t = open(MCU, encoding="utf-8").read()
if "PoliClock:ESP32-C3-WROOM-02" not in t:
    s = t.index('(symbol "PoliClock:ESP32-C3-MINI-1"')
    e = block(t, s)
    t = t[:s] + nuovo_simbolo(t[s:e], "\t\t") + t[e:]
    # istanza U3
    i = t.index('(property "Reference" "U3"')
    s = t.rindex("\n\t(symbol\n", 0, i) + 1
    e = block(t, s + 1)
    blk = t[s:e].replace('(lib_id "PoliClock:ESP32-C3-MINI-1")', '(lib_id "PoliClock:ESP32-C3-WROOM-02")')
    blk = set_prop(blk, "Value", "ESP32-C3-WROOM-02-N4")
    blk = set_prop(blk, "Footprint", "PoliClock:ESP32-C3-WROOM-02")
    blk = set_prop(blk, "Datasheet", DS)
    blk = set_prop(blk, "LCSC", "C2934560")
    blk = set_prop(blk, "Description", "ESP32-C3-WROOM-02-N4 (DEC-044): assemblaggio JLC Economic; radio non usata in V1 (DEC-012)")
    a = blk.index("\t\t(pin \"1\"")
    b2 = blk.index("\t\t(instances")
    pins = "".join('\t\t(pin "%s"\n\t\t\t(uuid "%s")\n\t\t)\n' % (p[0], uuid.uuid4()) for p in PIN)
    blk = blk[:a] + pins + blk[b2:]
    t = t[:s] + blk + t[e:]
    # flag NC sui pin del simbolo (x 148,59 / 171,45): non servono piu'
    for m in list(re.finditer(r"\t\(no_connect\n\t\t\(at (148\.59|171\.45) [\d.]+\)\n\t\t\(uuid \"[^\"]+\"\)\n\t\)\n", t))[::-1]:
        t = t[:m.start()] + t[m.end():]

    def drop_wire(t, x1, y1, x2, y2):
        pat = "(xy %s %s) (xy %s %s)" % (x1, y1, x2, y2)
        alt = "(xy %s %s) (xy %s %s)" % (x2, y2, x1, y1)
        k = t.find(pat)
        if k < 0:
            k = t.find(alt)
        assert k >= 0, pat
        s = t.rindex("\t(wire\n", 0, k)
        e = block(t, s + 1)
        return t[:s] + t[e + 1:]

    def drop_at(t, kind, x, y):
        for m in re.finditer(r"\t\(%s\n\t\t\(at %s %s\)" % (kind, re.escape(x), re.escape(y)), t):
            e = block(t, m.start() + 1)
            return t[:m.start()] + t[e + 1:]
        raise KeyError((kind, x, y))

    def drop_symbol_at(t, lib_id, x, y):
        k = t.index('(lib_id "%s")\n\t\t(at %s %s ' % (lib_id, x, y))
        s = t.rindex("\n\t(symbol\n", 0, k) + 1
        e = block(t, s + 1)
        return t[:s] + t[e + 1:]

    # bus GND di destra: resta solo il pin 19 (y 115,57) con il filo verso il simbolo GND a (176,53; 120,65)
    ys = ["72.39", "74.93", "77.47", "80.01", "82.55", "85.09", "87.63", "90.17", "92.71", "95.25", "97.79",
          "100.33", "102.87", "105.41", "107.95", "110.49", "113.03"]
    for y in ys:
        t = drop_wire(t, "171.45", y, "176.53", y)
    for a_, b_ in zip(ys + [], ys[1:] + ["115.57"]):
        t = drop_wire(t, "176.53", a_, "176.53", b_)
    for y in ys:
        try:
            t = drop_at(t, "junction", "176.53", y)
        except KeyError:
            pass
    # GND a sinistra: resta il pin 9 (y 74,93); tolti i pin 2/11/14 del MINI-1 con fili e simboli GND
    for y in ("77.47", "100.33", "107.95"):
        t = drop_wire(t, "148.59", y, "140.97", y)
        t = drop_symbol_at(t, "power:GND", "140.97", y)
    t = t.replace("Modulo ESP32-C3-MINI-1-H4X (chip v1.1, 4 MB flash, antenna PCB oltre il bordo)",
                  "Modulo ESP32-C3-WROOM-02-N4 (DEC-044: chip v0.4, 4 MB flash, antenna PCB sopra l'intaglio)")
    open(MCU, "w", encoding="utf-8", newline="\n").write(t)

# ------------------------------------------------------------------ foglio display (FIN-003)
t = open(DIS, encoding="utf-8").read()
if '"Reference" "C11"' not in t:
    i = t.index('(property "Reference" "R16"')
    s = t.rindex("\n\t(symbol\n", 0, i) + 1
    e = block(t, s + 1)
    blk = t[s:e]
    blk = re.sub(r'\(property "Value" "[^"]*"', '(property "Value" "10k"', blk, count=1)
    blk = re.sub(r'\(property "LCSC" "[^"]*"', '(property "LCSC" "C25804"', blk, count=1)
    blk = re.sub(r'\(property "Description" "[^"]*"',
                 '(property "Description" "Resistenza di gate 10 k: con C11 rampa di accensione lenta (FIN-003)"', blk, count=1)
    t = t[:s] + blk + t[e:]
    # C11 copiato da C10
    i = t.index('(property "Reference" "C10"')
    s = t.rindex("\n\t(symbol\n", 0, i) + 1
    e = block(t, s + 1)
    c = t[s:e]
    X = 128.27
    c = re.sub(r"\(at 165\.1 ", "(at %s " % X, c)
    c = re.sub(r"\(at 167\.64 ", "(at %s " % round(X + 2.54, 2), c)
    c = re.sub(r"\(at 166\.37 ", "(at %s " % round(X + 1.27, 2), c)
    c = c.replace('"Reference" "C10"', '"Reference" "C11"').replace('(reference "C10")', '(reference "C11")')
    c = re.sub(r'\(property "Value" "[^"]*"', '(property "Value" "10nF"', c, count=1)
    c = re.sub(r'\(property "LCSC" "[^"]*"', '(property "LCSC" "C57112"', c, count=1)
    c = re.sub(r'\(property "Description" "[^"]*"',
               '(property "Description" "Gate-drain di Q1: rampa di accensione del display (FIN-003)"', c, count=1)
    c = re.sub(r'\(uuid "[^"]+"\)', lambda m: '(uuid "%s")' % uuid.uuid4(), c)
    wires = ""
    for a_, b_ in (("171.45", "168.91"), ("179.07", "181.61")):
        wires += ('\t(wire\n\t\t(pts\n\t\t\t(xy %s %s) (xy %s %s)\n\t\t)\n\t\t(stroke\n\t\t\t(width 0)\n\t\t\t(type default)\n'
                  '\t\t)\n\t\t(uuid "%s")\n\t)\n') % (X, a_, X, b_, uuid.uuid4())
    labels = ""
    for name, y, rot in (("3V3_DISP", "168.91", 90), ("DISP_G", "181.61", 270)):
        just = "left" if rot == 90 else "right"
        labels += ('\t(label "%s"\n\t\t(at %s %s %d)\n\t\t(effects\n\t\t\t(font\n\t\t\t\t(size 1.27 1.27)\n\t\t\t)\n'
                   '\t\t\t(justify %s bottom)\n\t\t)\n\t\t(uuid "%s")\n\t)\n') % (name, X, y, rot, just, uuid.uuid4())
    k = t.index("\t(wire\n")
    t = t[:k] + wires + labels + t[k:]
    k = t.index("\n\t(symbol\n") + 1
    t = t[:k] + c + "\n" + t[k:]
    open(DIS, "w", encoding="utf-8", newline="\n").write(t)

# ------------------------------------------------------------------ foglio principale
t = open(ROOT, encoding="utf-8").read()
t = t.replace("MCU: ESP32-C3-MINI-1-H4X, RC su EN", "MCU: ESP32-C3-WROOM-02-N4 (DEC-044), RC su EN")
t = t.replace("Assegnazione GPIO (ESP32-C3-MINI-1):", "Assegnazione GPIO (ESP32-C3-WROOM-02):")
open(ROOT, "w", encoding="utf-8", newline="\n").write(t)
print("ok")
