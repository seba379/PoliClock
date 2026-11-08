"""Posizioni della scheda principale rev 0.2 (mm, origine = angolo in alto a sinistra, rotazione antioraria).

Scheda 50 x 40 mm (DEC-036) con intaglio nell'angolo in alto a destra: l'antenna del modulo ESP32 sta
dentro l'ingombro ma sopra l'intaglio, quindi senza PCB ne' rame sotto (linee guida Espressif:
antenna fuori dalla scheda base, punto di alimentazione vicino al bordo).

Regole di assemblaggio JLCPCB (SC-008, DEC-040): corpo dei componenti ad almeno 2,5 mm dal bordo sui lati
sinistro e destro (lati di trasporto, dove JLC aggiunge eventualmente i bordi tecnici); sui lati superiore e
inferiore solo i connettori che devono stare sul bordo (header display, USB-C).

Vista dall'alto:
  - in alto a destra: modulo ESP32-C3 ruotato di 270 gradi, antenna verso destra sopra l'intaglio;
  - bordo superiore a sinistra: header 7 pin del modulo display (piedini verso l'esterno);
  - bordo inferiore: USB-C (apertura verso il basso, opzione A) con due fori M2 ai lati, ESD tra USB-C e modulo;
  - in basso a sinistra: protezione VBUS e LDO con i condensatori sui pin;
  - a sinistra, rientrati di 2,5 mm: connettori JST-SH (SHT40, RTC, pulsante).
I componenti in ANCHOR sono piazzati automaticamente il piu' vicino possibile al pin indicato.
"""
import os

W, H = (float(v) for v in os.environ.get("PCB_WH", "50,40").split(","))
SIDE_MARGIN = 2.5                    # JLC: corpo dei componenti >= 2,5 mm dai lati di trasporto (sinistro/destro)

ANT_LEN = 11.04                      # dal centro del modulo alla punta dell'antenna (footprint ruotato)
XM = W - SIDE_MARGIN - ANT_LEN       # centro del modulo (rotazione 270): punta dell'antenna a 2,5 mm dal bordo
YM = 6.64 + 6.0                      # 6 mm liberi sopra il modulo per EN, 3V3 e le uscite dei segnali
NOTCH_X = XM + 5.7                   # da qui a destra c'e' l'antenna: niente PCB
NOTCH_Y = YM + 6.64 + 0.9            # fondo dell'intaglio

# contorno (senso orario), angoli vivi
OUTLINE = [(0, 0), (NOTCH_X, 0), (NOTCH_X, NOTCH_Y), (W, NOTCH_Y), (W, H), (0, H)]
NOTCH = (NOTCH_X, 0, W, NOTCH_Y)
# zona senza rame vicino all'antenna (oltre all'intaglio)
ANT_KEEPOUT = (NOTCH_X - 0.5, NOTCH_Y, W, NOTCH_Y + 3.0)

J1X = XM - 4.5
JX = 3.75 + SIDE_MARGIN              # JST: fronte del corpo a 2,5 mm dal bordo sinistro
PLACE = {
    # ref: (x, y, rotazione, lato)
    "U3": (XM, YM, 270, "F"),
    "J2": (17.5, 6.6, 180, "F"),            # header display: corpo verso il bordo superiore, piedini fuori scheda
    "J1": (J1X, H - 3.3, 0, "F"),           # USB-C: guscio sporge 0,4 mm dal bordo (disegno HRO)
    "U1": (J1X + 1.7, H - 11.0, 270, "F"),  # ESD tra connettore e modulo, D- a sinistra e D+ a destra
    "R4": (J1X + 0.8, H - 16.5, 90, "F"),   # 0 ohm D-
    "R3": (J1X + 2.6, H - 16.5, 90, "F"),   # 0 ohm D+
    "J3": (JX, 12.0, 270, "F"),             # JST-SH 4P SHT40, apertura a sinistra
    "J4": (JX, 20.0, 270, "F"),             # JST-SH 4P RTC
    "J5": (JX, 27.5, 270, "F"),             # JST-SH 2P pulsante
    "U2": (17.0, H - 6.5, 0, "F"),          # LDO TLV75533 (SOT-23-5)
}
# punti di test: pad nudi sul retro, in due file ordinate con l'etichetta (riferimento e rete) sotto ciascuno
# file a partire da x = 13 mm: lontane dalle etichette dei connettori JST (SHT40, RTC, BTN) sul lato sinistro
for i, ref in enumerate(["TP1", "TP2", "TP3", "TP4", "TP5"]):
    PLACE[ref] = (13.0 + (W - 20.0) / 5 * i, H * 0.6, 0, "B")
for i, ref in enumerate(["TP7", "TP8", "TP9", "TP10"]):
    PLACE[ref] = (13.0 + (W - 20.0) / 5 * i, H * 0.6 + 5.5, 0, "B")
# EN e IO9 vicino ai rispettivi pin del modulo: piste EN/IO9 corte (Espressif: CHIP_EN il piu' corto possibile)
PLACE["TP6"] = (XM - 4.5, YM - 6.2, 0, "B")      # EN (pin 8)
PLACE["TP11"] = (XM - 8.0, YM + 4.0, 0, "B")     # IO9 (pin 23)

HOLES = [(J1X - 9.5, H - 3.5), (J1X + 10.0, H - 3.5)]  # M2 ai lati della USB-C
FIDUCIALS = [(SIDE_MARGIN + 1.0, H - 9.0), (16.0, 12.0), (W - SIDE_MARGIN - 1.5, H - 9.0)]  # 1 mm, lato superiore

# piazzamento automatico vicino a un pin preciso: ref -> (ref, pin)
ANCHOR = {
    "C6": ("U3", "3"), "C5": ("U3", "3"),          # 0,1 uF + 10 uF sul pin 3V3 del modulo
    "R6": ("U3", "8"), "C7": ("U3", "8"),          # RC su EN
    "R7": ("U3", "23"),                            # pull-up IO9
    "C2": ("U2", "1"), "C3": ("U2", "5"), "C4": ("U2", "5"), "R5": ("U2", "1"),
    "F1": ("J1", "A4"), "C1": ("F1", "2"),
    "R1": ("J1", "A5"), "R2": ("J1", "B5"),
    "R8": ("U3", "20"), "R9": ("U3", "21"),
    "Q1": ("J2", "1"), "C9": ("J2", "1"), "C10": ("J2", "1"), "R16": ("Q1", "1"), "R17": ("Q1", "1"),
    "R15": ("J2", "7"),
    "R19": ("J3", "3"), "R20": ("J3", "4"), "R21": ("J3", "2"),
    "R22": ("J5", "1"), "C8": ("J5", "1"),
}
AUTO_ORDER = ["C6", "C5", "R6", "C7", "C2", "C3", "C4", "R5", "F1", "C1", "R1", "R2", "R7",
              "R8", "R9", "Q1", "C9", "C10", "R16", "R17", "R15", "R19", "R20", "R21", "R22", "C8"]
BOTTOM = set()
