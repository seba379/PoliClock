"""Post-elaborazione dell'output di easyeda2kicad (vedi hardware/README.md):
 pin electrical types, LCSC field, references,
SHT40 die pad removal (Sensirion SHT4x datasheet V7.3 sect. 5.3: die pad must not be soldered)."""
import os
import re
import sys
from sexp import parse, dump, find, find1, Sym

HW = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIB = f"{HW}/lib/PoliClock.kicad_sym"

root = parse(open(LIB, encoding="utf-8").read())[0]

REF = {"TYPE-C-31-M-12": "J", "AFC01-S16FCA-00": "J", "AFC01-S18FCA-00": "J",
       "SM04B-SRSS-TB": "J", "SM02B-SRSS-TB": "J", "SHT40-AD1B-R2": "U",
       "ESP32-C3-MINI-1-N4": "U", "TS-1187A-B-A-B": "SW"}
DS = {
    "ESP32-C3-MINI-1-N4": "https://www.espressif.com/sites/default/files/documentation/esp32-c3-mini-1_datasheet_en.pdf",
    "SHT40-AD1B-R2": "https://sensirion.com/media/documents/33FD6951/6A7C10A0/HT_DS_Datasheet_SHT4x_V7.3.pdf",
}


def ptype(sym, num, name):
    if sym == "ESP32-C3-MINI-1-N4":
        if name == "GND" or name == "3V3":
            return "power_in"
        if name == "NC":
            return "no_connect"
        if name == "EN":
            return "input"
        return "bidirectional"
    if sym == "SHT40-AD1B-R2":
        return {"SDA": "bidirectional", "SCL": "input", "VDD": "power_in", "VSS": "power_in"}[name]
    return "passive"


for s in find(root, "symbol"):
    name = s[1]
    for p in find(s, "property"):
        if p[1] == "LCSC Part":
            p[1] = "LCSC"
        if p[1] == "Reference" and name in REF:
            p[2] = REF[name]
        if p[1] == "Datasheet" and name in DS:
            p[2] = DS[name]
    for sub in find(s, "symbol"):
        keep = []
        for e in sub:
            if isinstance(e, list) and e and e[0] == "pin":
                num = find1(e, "number")[1]
                pname = find1(e, "name")[1]
                if name == "SHT40-AD1B-R2" and num == "5":
                    continue
                e[1] = Sym(ptype(name, num, pname))
            keep.append(e)
        sub[:] = keep

open(LIB, "w", encoding="utf-8", newline="\n").write(dump(root) + "\n")

# SHT40 footprint: drop the exposed die pad (pad 5) and rename it (eseguire una sola volta dopo easyeda2kicad)
old = f"{HW}/lib/PoliClock.pretty/DFN-4_L1.5-W1.5-P0.8-TL-EP.kicad_mod"
new_name = "SHT4x_DFN-4_1.5x1.5mm_P0.8mm_NoDiePad"
if os.path.exists(old):
    t = parse(open(old, encoding="utf-8").read())[0]
    t[:] = [e for e in t if not (isinstance(e, list) and e and e[0] == "pad" and e[1] == "5")]
    t[1] = new_name
    open(f"{HW}/lib/PoliClock.pretty/{new_name}.kicad_mod", "w", encoding="utf-8", newline="\n").write(dump(t) + "\n")
    os.remove(old)
lib = open(LIB, encoding="utf-8").read().replace('"PoliClock:DFN-4_L1.5-W1.5-P0.8"', f'"PoliClock:{new_name}"')
open(LIB, "w", encoding="utf-8", newline="\n").write(lib)
print("ok - poi eseguire: kicad-cli fp upgrade --force lib/PoliClock.pretty e kicad-cli sym upgrade --force lib/PoliClock.kicad_sym")
