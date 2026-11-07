"""Post-elaborazione dell'output di easyeda2kicad (vedi hardware/README.md):
 tipi elettrici dei pin, campo LCSC, riferimenti."""
import os
import re
import sys
from sexp import parse, dump, find, find1, Sym

HW = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIB = f"{HW}/lib/PoliClock.kicad_sym"

root = parse(open(LIB, encoding="utf-8").read())[0]

REF = {"TYPE-C-31-M-12": "J", "AFC01-S16FCA-00": "J", "AFC01-S18FCA-00": "J",
       "SM04B-SRSS-TB": "J", "SM02B-SRSS-TB": "J",
       "ESP32-C3-MINI-1-N4": "U", "TS-1088-AR02016": "SW"}
DS = {
    "ESP32-C3-MINI-1-N4": "https://www.espressif.com/sites/default/files/documentation/esp32-c3-mini-1_datasheet_en.pdf",
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
                e[1] = Sym(ptype(name, num, pname))
            keep.append(e)
        sub[:] = keep

open(LIB, "w", encoding="utf-8", newline="\n").write(dump(root) + "\n")
print("ok - poi eseguire: kicad-cli fp upgrade --force lib/PoliClock.pretty e kicad-cli sym upgrade --force lib/PoliClock.kicad_sym")
