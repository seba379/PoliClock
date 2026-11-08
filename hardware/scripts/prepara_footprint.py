"""Adatta la serigrafia di alcuni footprint ai bordi della scheda principale (eseguire una volta).

- USB-C HRO TYPE-C-31-M-12: copiato dalla libreria KiCad (pad dal disegno HRO); tolte le linee di serigrafia
  del fronte, che sporgono oltre il bordo scheda (il guscio sporge di 0,4 mm).
- ESP32-C3-MINI-1: tolta la serigrafia sopra l'antenna (sopra l'intaglio della scheda), lati accorciati.
- Header 7 pin SMD a 90 gradi: tolto il disegno dei piedini fuori dal corpo (sporgono oltre il bordo).
Pad, fori e courtyard non vengono toccati. Lavora direttamente sul testo dei .kicad_mod.
"""
import os
import uuid
from sexp import parse, dump, find, find1, Sym

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.join(os.path.dirname(HERE), "lib", "PoliClock.pretty")
STD = "C:/Program Files/KiCad/10.0/share/kicad/footprints"
GRAPHIC = ("fp_line", "fp_rect", "fp_circle", "fp_arc", "fp_poly")


def load(path):
    return parse(open(path, encoding="utf-8").read())[0]


def save(fp, name):
    fp[1] = name
    open(os.path.join(LIB, name + ".kicad_mod"), "w", encoding="utf-8", newline="\n").write(dump(fp) + "\n")


def ys(item):
    pts = []
    for key in ("start", "end", "center", "mid"):
        e = find1(item, key)
        if e:
            pts.append(float(e[2]))
    pts += [float(p[2]) for p in find(find1(item, "pts") or [], "xy")]
    return pts


def drop_silk(fp, cond):
    n = 0
    keep = []
    for e in fp:
        if isinstance(e, list) and e and e[0] in GRAPHIC and find1(e, "layer") and find1(e, "layer")[1] == "F.SilkS" \
                and cond(ys(e)):
            n += 1
            continue
        keep.append(e)
    fp[:] = keep
    return n


def add_line(fp, a, b):
    fp.append([Sym("fp_line"), [Sym("start"), a[0], a[1]], [Sym("end"), b[0], b[1]],
               [Sym("stroke"), [Sym("width"), 0.12], [Sym("type"), Sym("solid")]],
               [Sym("layer"), "F.SilkS"], [Sym("uuid"), str(uuid.uuid4())]])


fp = load(f"{STD}/Connector_USB.pretty/USB_C_Receptacle_HRO_TYPE-C-31-M-12.kicad_mod")
print("USB-C:", drop_silk(fp, lambda y: max(y) > 3.0), "linee tolte")
save(fp, "USB_C_Receptacle_HRO_TYPE-C-31-M-12")

fp = load(os.path.join(LIB, "WIFIM-SMD_ESP32-C3-MINI-1.kicad_mod"))
n = drop_silk(fp, lambda y: min(y) < -5.4)
if n:
    add_line(fp, (-6.6, -5.2), (-6.6, 5.6))
    add_line(fp, (6.6, -5.2), (6.6, 5.6))
print("ESP32:", n, "linee tolte")
save(fp, "WIFIM-SMD_ESP32-C3-MINI-1")

fp = load(os.path.join(LIB, "HDR-SMD_7P-P2.54-H-M-W13.3-N.kicad_mod"))
print("Header:", drop_silk(fp, lambda y: max(y) > 6.3), "linee tolte")
save(fp, "HDR-SMD_7P-P2.54-H-M-W13.3-N")
