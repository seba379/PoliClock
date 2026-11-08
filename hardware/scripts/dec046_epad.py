"""DEC-046: niente vie nella piazzola termica (EPAD, pad 19) di U3 ESP32-C3-WROOM-02.

Revisione esterna del 2026-11-08 (P2-01) e R2-006: le 4 vie aperte 0,3/0,7 mm nella EPAD possono assorbire
stagno al reflow. Il datasheet Espressif dice che la saldatura della EPAD non e' obbligatoria e con la radio
spenta (DEC-012) la dissipazione e' minima: si tolgono le vie, la EPAD resta collegata a GND sul rame superiore.

Modifica una tantum (Python di KiCad 10):
  "C:/Program Files/KiCad/10.0/bin/python.exe" hardware/scripts/dec046_epad.py
Toglie le 4 piazzole passanti "19" dall'impronta di libreria e dall'istanza U3 sul PCB, ricalcola le zone e salva.
"""
import os
import re
import pcbnew

HW = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIB = os.path.join(HW, "lib", "PoliClock.pretty", "ESP32-C3-WROOM-02.kicad_mod")
PCB = os.path.join(HW, "policlock-main", "policlock-main.kicad_pcb")

# libreria: via i blocchi (pad "19" thru_hole ...)
raw = open(LIB, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in raw else "\n"
s = raw.replace("\r\n", "\n")
blocks = re.findall(r"\t\(pad \"19\" thru_hole circle\n.*?\n\t\)\n", s, re.S)
assert len(blocks) == 4, len(blocks)
for b in blocks:
    s = s.replace(b, "", 1)
s = s.replace("4 vie termiche 0,3/0,7 mm nella EPAD", "EPAD senza vie (DEC-046)")
open(LIB, "w", encoding="utf-8", newline="").write(s.replace("\n", nl))

# PCB: stessa modifica sull'istanza U3, poi zone ricalcolate
board = pcbnew.LoadBoard(PCB)
u3 = board.FindFootprintByReference("U3")
tolti = [p for p in u3.Pads() if p.GetNumber() == "19" and p.GetAttribute() == pcbnew.PAD_ATTRIB_PTH]
assert len(tolti) == 4, len(tolti)
for p in tolti:
    u3.Remove(p)
pcbnew.ZONE_FILLER(board).Fill(board.Zones())
board.Save(PCB)
print("EPAD di U3 senza vie: tolte", len(tolti), "piazzole passanti")
