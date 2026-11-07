"""Posizioni fisse della scheda principale (mm, origine = angolo in alto a sinistra, rotazione antioraria).

Disposizione (vista dall'alto):
  - bordo destro: modulo ESP32-C3 ruotato di 270 gradi, l'antenna sporge oltre il bordo (DEC-031);
  - bordo superiore: connettore FFC del cavo display, ingresso cavo verso l'alto;
  - bordo inferiore: USB-C con l'apertura verso il basso (opzione A, verso il sedere) e due fori M2 ai lati;
  - bordo sinistro: connettori JST-SH (SHT40, RTC, pulsante) con l'apertura verso l'esterno.
I componenti non elencati sono piazzati automaticamente vicino ai pin collegati.
"""
import os
W, H = (float(v) for v in os.environ.get("PCB_WH", "35,27").split(","))

XM = W - 5.7          # centro modulo: il bordo destro coincide con l'inizio dell'antenna
YM = 8.4

PLACE = {
    # ref: (x, y, rotazione, lato)
    "U3": (XM, YM, 270, "F"),
    "J2": (XM - 12.7, 4.6, 0, "F"),          # FFC 16P, corpo verso il bordo superiore
    "J1": (XM - 4.2, H - 5.1, 0, "F"),      # USB-C, apertura verso il bordo inferiore
    "J3": (3.15, 4.3, 270, "F"),        # JST-SH 4P SHT40, apertura a sinistra
    "J4": (3.15, 11.3, 270, "F"),       # JST-SH 4P RTC
    "J5": (3.15, 17.6, 270, "F"),       # JST-SH 2P pulsante
    "SW3": (3.9, H - 3.0, 0, "F"),      # tasto USER su scheda, sotto il connettore del pulsante
    "U2": (11.55, H - 4.55, 90, "F"),     # LDO SOT-223 vicino all'ingresso 5 V
}

HOLES = [(XM - 11.6, H - 2.6), (W - 2.5, H - 2.6)]    # M2, ai lati della USB-C per scaricare lo sforzo del cavo

# ordine del piazzamento automatico (prima i componenti che contano di piu' per lo sbroglio)
AUTO_ORDER = ["U1", "R3", "R4", "R1", "R2", "F1", "C1", "C5", "C6", "R6", "C7", "SW1", "R7", "SW2",
              "R8", "R9", "R19", "R20", "R15", "R10", "R11", "R12", "R13", "R14",
              "Q1", "R16", "R17", "R18", "R5", "C2", "C3", "C4", "R21", "R22", "C8",
              "TP1", "TP2", "TP3", "TP4", "TP5", "TP6", "TP7", "TP8"]
BOTTOM = {"TP1", "TP2", "TP3", "TP4", "TP5", "TP6", "TP7", "TP8"}   # pad nudi sul retro, non assemblati
