"""Concept 3D della statuetta PoliClock in stile "a cubetti" (voxel), versione 2.

Stile dal riferimento del proprietario (assets/concept/riferimento-stile-chibi-voxel.webp):
testa a cubo, cappello blu notte, capelli castani con coda laterale, camicia
blu notte a maniche corte con spalline e tasche, cintura con fondina e fibbia,
pantaloni azzurri con banda rossa, stivali neri, sul piedistallo che contiene
la scheda (DEC-048) con la USB-C sul retro.

Versione 2 (DEC-054, parole del proprietario: "Allungare un po' il busto e le
gambe. Inoltre, se facessimo una testa un po più piccola, cosi nel caso posso
mettere una emoji come faccia sul display?"):
- busto e gambe più lunghi, braccia leggibili (manica corta con risvolto e
  avambraccio);
- testa piccola: il display rotondo è tutto il volto, incorniciato solo da
  capelli e cappello. L'aletta dei pin del modulo e la spina Dupont scendono
  dal pavimento della testa in una cavità in cima al busto; la testa si
  sfila verso l'alto per la manutenzione.

Vincoli: modulo display segnaposto (OPEN-016), canale 21 x 6 mm per il
cavetto dal piano della base alla cavità del busto (docs/06 §12.2), base dallo
studio volumetrico, insegne stilizzate (DEC-053). Giunzioni, spessori e
tolleranze sono di concept (DEC-052, OPEN-032).

Uso (dalla radice del repository):
  ..\\.venv-cad\\Scripts\\python.exe mechanical/cad/concept_voxel.py
Uscite:
  mechanical/prints/concept/<parte>.stl     una per parte (concept, non definitive)
  mechanical/prints/concept-statuetta.step  assieme
  mechanical/cad/concept_rapporto.txt       quote e controlli
  mechanical/cad/out/concept/...            ingombri e dati per Blender (non versionati)
"""

import glob
import json
import math
import os
import sys

from build123d import Align, Compound, Cylinder, FontStyle, Pos, Rot, Text, export_step, export_stl, extrude

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, QUI)
import parametri as P  # noqa: E402

# Base "a blocco" coerente con lo stile: spigoli piccoli anche davanti.
P.RAGGIO_FRONTE = 5.0
P.RAGGIO_RETRO = 4.0
import studio_base as SB  # noqa: E402

RADICE = os.path.abspath(os.path.join(QUI, "..", ".."))
DIR_PARTI = os.path.join(RADICE, "mechanical", "prints", "concept")
STEP_ASSIEME = os.path.join(RADICE, "mechanical", "prints", "concept-statuetta.step")
DIR_OUT = os.path.join(RADICE, "mechanical", "cad", "out", "concept")
RAPPORTO = os.path.join(QUI, "concept_rapporto.txt")

# ---------------------------------------------------------------------------
# Quote del concept v2 (mm). Z dal tavolo; X, Y come nello studio della base.
# ---------------------------------------------------------------------------
Z_BASE = SB.ALTEZZA_BASE            # 24,1
Z_STIVALI = Z_BASE + 10.0           # 34,1
Z_PANTALONI = Z_STIVALI + 24.0      # 58,1
Z_CINTURA = Z_PANTALONI + 4.0       # 62,1
Z_BUSTO = Z_CINTURA + 28.0          # 90,1
Z_TESTA = Z_BUSTO                   # la testa appoggia sul busto (collo nascosto)
TESTA = (48.0, 40.0, 48.0)          # larghezza, profondità, altezza
FASCIA_H = 4.0                      # fascia del cappello
CAPPELLO_H = 11.0                   # calotta

PARETE_TESTA = 3.0
VOLTO_S = 2.0                       # spessore della piastra del volto
Y_FACCIA = -16.0                    # piano del volto = fronte del busto
Y_RETRO_TESTA = Y_FACCIA + TESTA[1]
VOLTO_X = 20.0                      # mezza larghezza della piastra del volto
FINESTRA_D = 38.0                   # vetro Ø 37,5 (segnaposto) + gioco
DISPLAY_Z = Z_TESTA + 21.0          # centro del vetro: 2 mm di mento sotto la finestra
Z_FRANGIA = DISPLAY_Z + FINESTRA_D / 2 + 1.0
PROFONDITA_FRONTE_TESTA = 8.0       # spessore della parte anteriore della testa

# Corpo (Y del busto spostata in avanti: il modulo display scende nel busto)
BUSTO_X, BUSTO_Y = 18.0, (-16.0, 12.0)
PANTALONI_X, PANTALONI_Y = 17.0, (-13.0, 9.0)
CINTURA_X, CINTURA_Y = 19.0, (-14.5, 10.5)
STIVALI_Y = (-19.0, 7.0)

CANALE = P.CANALE_CAVO              # 21 x 6
GIOCO = 0.2                         # fra parti incastrate (concept)
SPINA = 3.2                         # fori per spine di allineamento Ø 3 mm
SPINE_XY = [(-14.0, 0.0), (14.0, 0.0)]       # stivali -> busto
SPINE_TESTA_XY = [(-14.0, 2.0), (14.0, 2.0)]  # busto -> testa -> cappello

# Modulo display (segnaposto OPEN-016): tondo Ø 38 + aletta dei pin in basso
MOD_D = P.DISPLAY_PCB[0]
MOD_T = P.DISPLAY_SPESSORE
MOD_Y0 = Y_FACCIA + VOLTO_S         # vetro contro il retro della piastra
MOD_Y1 = MOD_Y0 + MOD_T
ALETTA_W = P.DISPLAY_ALETTA_L
ALETTA_Z0 = DISPLAY_Z - P.DISPLAY_TONDO_D / 2 - (P.DISPLAY_PCB[1] - P.DISPLAY_TONDO_D)
PIN_Z = ALETTA_Z0 + 2.5
SPINA_Y1 = MOD_Y1 + 2.5 + P.DUPONT_H

COLORI = {  # sRGB (0-1), convertiti in lineare da Blender
    "base": (0.48, 0.49, 0.51), "fondo": (0.30, 0.30, 0.32), "nero": (0.08, 0.08, 0.09),
    "pantaloni": (0.29, 0.39, 0.66), "rosso": (0.55, 0.11, 0.18), "camicia": (0.11, 0.16, 0.35),
    "cappello": (0.09, 0.12, 0.29), "pelle": (0.95, 0.76, 0.61), "capelli": (0.42, 0.23, 0.11),
    "oro": (0.88, 0.66, 0.12), "grigio": (0.62, 0.63, 0.65), "bianco": (0.95, 0.95, 0.95),
    "verde": (0.09, 0.54, 0.24), "targhetta": (0.07, 0.09, 0.20),
}


def S(x0, x1, y0, y1, z0, z1):
    return SB.scatola(x0, x1, y0, y1, z0, z1)


def foro(x, y, z0, z1, d=SPINA):
    return SB.cilindro(x, y, z0, z1, d)


def canale(z0, z1):
    return S(-CANALE[0] / 2, CANALE[0] / 2, -CANALE[1] / 2, CANALE[1] / 2, z0, z1)


def fori_spine(forma, z, sopra, sotto, xy=SPINE_XY):
    for (x, y) in xy:
        if sopra:
            forma -= foro(x, y, z - 4.0, z + 0.01)
        if sotto:
            forma -= foro(x, y, z - 0.01, z + 4.0)
    return forma


def passaggio_modulo(z0, z1, g=0.4):
    """Foro a "T" per aletta del modulo (davanti) e spina Dupont (dietro)."""
    a = S(-ALETTA_W / 2 - g, ALETTA_W / 2 + g, MOD_Y0 - g, MOD_Y1 + g, z0, z1)
    b = S(-P.DUPONT_7_L / 2 - g, P.DUPONT_7_L / 2 + g, MOD_Y1 - g, SPINA_Y1 + g, z0, z1)
    return a + b


def lati(sx, a, b):
    """Estremi ordinati di un intervallo specchiato sul lato sx (-1 o 1)."""
    return tuple(sorted((sx * a, sx * b)))


# ---------------------------------------------------------------------------
# Parti
# ---------------------------------------------------------------------------
def parti():
    pz = {}   # nome: (forma, colore, esploso (dx, dy, dz), nota di stampa)

    # --- Base dallo studio ------------------------------------------------
    ing, ds = SB.ingombri()
    pz["base_guscio"] = (SB.guscio(ds), "base", (0, 0, 0), "Capovolta (piano superiore sul piatto)")
    f, zz = SB.fondo()
    pz["base_fondo"] = (f, "fondo", (0, 0, -32), "Piatta; è lo sportello di servizio (OPEN-008)")

    # --- Stivali (mezzo canale ciascuno) ----------------------------------
    for lato, sx in (("dx", -1), ("sx", 1)):   # dx = destra della chibi = -X
        b = S(*lati(sx, 0.25, 17.25), *STIVALI_Y, Z_BASE, Z_STIVALI)
        b -= canale(Z_BASE - 1, Z_STIVALI + 1)
        vx, vy = [v for v in P.VITI_CORPO_XY if v[0] * sx > 0][0]
        b -= SB.cilindro(vx, vy, Z_BASE - 0.01, Z_BASE + 6.0, 4.0)   # inserto M3
        b = fori_spine(b, Z_STIVALI, sopra=True, sotto=False)
        pz[f"stivale_{lato}"] = (b, "nero", (sx * 6, 0, 10), "Suola sul piatto")

    # --- Pantaloni con banda rossa ----------------------------------------
    y0, y1 = PANTALONI_Y
    pa = S(-PANTALONI_X, PANTALONI_X, y0, y1, Z_STIVALI, Z_PANTALONI)
    for y in (y0, y1):   # solco fra le gambe
        pa -= S(-1.0, 1.0, y - 1.5, y + 1.5, Z_STIVALI - 0.1, Z_PANTALONI - 5.0)
    yc = (y0 + y1) / 2
    for sx in (-1, 1):
        pa -= S(*lati(sx, PANTALONI_X - 0.8, PANTALONI_X + 0.1), yc - 1.6, yc + 1.6, Z_STIVALI - 0.1, Z_PANTALONI + 0.1)
    pa -= canale(Z_STIVALI - 1, Z_PANTALONI + 1)
    pa = fori_spine(pa, Z_STIVALI, sopra=False, sotto=True)
    pa = fori_spine(pa, Z_PANTALONI, sopra=True, sotto=False)
    pz["pantaloni"] = (pa, "pantaloni", (0, 0, 20), "In piedi; banda rossa incastrata o dipinta")
    for lato, sx in (("dx", -1), ("sx", 1)):
        pz[f"banda_{lato}"] = (S(*lati(sx, PANTALONI_X - 0.8 + GIOCO / 2, PANTALONI_X), yc - 1.4, yc + 1.4,
                                 Z_STIVALI + 0.2, Z_PANTALONI - 0.2), "rosso", (sx * 16, 0, 20),
                               "Listello 0,8 mm: meglio dipinto se il servizio non regge lo spessore")

    # --- Cintura, fibbia, fondina, tasca ----------------------------------
    y0, y1 = CINTURA_Y
    ci = S(-CINTURA_X, CINTURA_X, y0, y1, Z_PANTALONI, Z_CINTURA)
    ci -= canale(Z_PANTALONI - 1, Z_CINTURA + 1)
    ci -= S(-4.2, 4.2, y0 - 0.1, y0 + 0.7, Z_PANTALONI + 0.4, Z_CINTURA - 0.4)   # sede fibbia
    for (x, y) in SPINE_XY:
        ci -= foro(x, y, Z_PANTALONI - 0.1, Z_CINTURA + 0.1)
    ci += S(-25.0, -18.5, -17.0, -8.5, Z_PANTALONI - 13.0, Z_CINTURA)      # fondina
    ci += S(-24.0, -19.5, -17.6, -16.9, Z_PANTALONI - 6.0, Z_PANTALONI - 2.0)  # patta
    ci += S(18.5, 24.0, -16.5, -10.0, Z_PANTALONI - 5.0, Z_CINTURA)        # tasca
    pz["cintura"] = (ci, "nero", (0, 0, 30), "Anello con fondina e tasca; le spine Ø 3 attraversano")
    pz["fibbia"] = (S(-4.0, 4.0, y0 - 1.0, y0 + 0.6, Z_PANTALONI + 0.6, Z_CINTURA - 0.6), "grigio", (0, -10, 30),
                    "Piastrina incastrata nella cintura")

    # --- Busto (camicia) --------------------------------------------------
    y0, y1 = BUSTO_Y
    bu = S(-BUSTO_X, BUSTO_X, y0, y1, Z_CINTURA, Z_BUSTO)
    for sx in (-1, 1):
        bu += S(*lati(sx, BUSTO_X, 27.0), -8.0, 6.0, Z_BUSTO - 15.0, Z_BUSTO - 3.0)       # manica corta
        bu += S(*lati(sx, BUSTO_X, 27.6), -8.6, 6.6, Z_BUSTO - 16.0, Z_BUSTO - 13.0)      # risvolto
        bu += S(*lati(sx, 4.0, 14.0), y0 - 1.0, y0, Z_CINTURA + 5.0, Z_CINTURA + 11.0)    # taschino
        bu += S(*lati(sx, 4.0, 14.0), y0 - 1.4, y0 - 0.9, Z_CINTURA + 9.6, Z_CINTURA + 11.6)  # patta
        for i in range(2):   # colletto a "V" a blocchi
            bu += S(*lati(sx, 1.5 + 2.5 * i, 4.0 + 2.5 * i), y0 - 1.0, y0 + 0.1,
                    Z_BUSTO - 2.5 - 2.0 * i, Z_BUSTO)
    zt = Z_CINTURA + 13.0
    bu -= S(-15.8, -4.6, y0 - 0.1, y0 + 0.6, zt - 0.2, zt + 5.5)    # sede toppa
    bu -= S(4.6, 15.8, y0 - 0.1, y0 + 0.6, zt - 0.2, zt + 5.5)      # sede targhetta
    bu -= canale(Z_CINTURA - 1, Z_BUSTO + 1)
    bu -= passaggio_modulo(ALETTA_Z0 - 2.0, Z_BUSTO + 0.1)          # cavità per aletta e spina
    for (x, y) in SPINE_XY:
        bu -= foro(x, y, Z_CINTURA - 0.01, Z_CINTURA + 4.0)
    bu = fori_spine(bu, Z_BUSTO, sopra=True, sotto=False, xy=SPINE_TESTA_XY)
    for sx in (-1, 1):
        bu -= foro(sx * 22.5, -1.0, Z_BUSTO - 16.01, Z_BUSTO - 12.0)   # spina del braccio
    pz["busto"] = (bu, "camicia", (0, 0, 42), "In piedi; cavità in cima per l'aletta del display")

    for lato, sx in (("dx", -1), ("sx", 1)):
        br = S(*lati(sx, 19.0, 26.0), -6.0, 4.0, Z_PANTALONI - 2.0, Z_BUSTO - 16.0)
        br -= foro(sx * 22.5, -1.0, Z_BUSTO - 20.0, Z_BUSTO - 15.99)
        pz[f"braccio_{lato}"] = (br, "pelle", (sx * 18, 0, 36), "Avambraccio e mano; spina Ø 3 nella manica")
        pz[f"spallina_{lato}"] = (S(*lati(sx, 18.5, 27.0), -6.0, 4.0, Z_BUSTO - 3.0, Z_BUSTO - 1.6), "rosso",
                                  (sx * 12, 0, 50), "Piastrina 1,4 mm sulla manica")
        pz[f"grado_{lato}"] = (S(*lati(sx, 23.0, 26.5), -4.0, 2.0, Z_BUSTO - 1.6, Z_BUSTO - 1.0), "oro",
                               (sx * 12, 0, 56), "Dettaglio 0,6 mm: dipinto se troppo sottile per il servizio")

    # Insegne stilizzate (DEC-053): toppa tricolore e "POLIZIA"
    pz["targhetta"] = (S(4.8, 15.6, y0 - 0.4, y0 + 0.55, zt, zt + 5.3), "targhetta", (0, -12, 42), "Piastrina")
    testo = extrude(Text("POLIZIA", font_size=2.8, font="Arial", font_style=FontStyle.BOLD), 0.5)
    pz["scritta_polizia"] = (Pos(10.2, y0 - 0.4, zt + 2.65) * (Rot(90, 0, 0) * testo), "bianco", (0, -14, 42),
                             "Lettere in rilievo 0,5 mm: stampa multicolore o pittura")
    for i, n in enumerate(("verde", "bianco", "rosso")):
        x0 = -15.6 + i * 3.6
        pz[f"toppa_{n}"] = (S(x0, x0 + 3.6, y0 - 0.4, y0 + 0.55, zt, zt + 5.3), n, (0, -12, 42), "Piastrina")

    # --- Testa -------------------------------------------------------------
    W, D, H = TESTA
    x0, x1, z0, z1 = -W / 2, W / 2, Z_TESTA, Z_TESTA + H
    ty0, ty1 = Y_FACCIA, Y_RETRO_TESTA
    t = PARETE_TESTA
    gt = S(x0, x1, ty0, ty1, z0, z1) - S(x0 + t, x1 - t, ty0 + t, ty1 - t, z0 + t, z1 - t)
    gt -= S(-VOLTO_X, VOLTO_X, ty0 - 1, ty0 + t + 0.01, z0 - 0.01, Z_FRANGIA)   # apertura del volto
    gt -= passaggio_modulo(z0 - 1, z0 + t + 1)                                  # pavimento: aletta e spina
    gt = fori_spine(gt, z0, sopra=False, sotto=True, xy=SPINE_TESTA_XY)
    gt = fori_spine(gt, z1, sopra=True, sotto=False, xy=SPINE_TESTA_XY)
    yf = ty0 + PROFONDITA_FRONTE_TESTA
    taglio = S(x0 - 1, x1 + 1, ty0 - 1, yf, z0 - 1, z1 + 1)
    fronte = gt & taglio
    retro = gt - taglio
    # ciuffi "a pixel" negli angoli, fuori dal cerchio del display
    for (a, b, h) in ((-VOLTO_X, -15.0, 3.0), (13.0, VOLTO_X, 5.0)):
        fronte += S(a, b, ty0, ty0 + VOLTO_S, Z_FRANGIA - h, Z_FRANGIA)
    pz["testa_fronte"] = (fronte, "capelli", (0, -14, 62),
                          "Cornice dei capelli attorno al volto; si unisce a testa_retro (viti M2 dal pavimento)")
    # coda laterale sul lato destro della chibi (-X), a gradini
    coda = S(x0 - 4.0, x0, 4.0, 14.0, z0 + 26.0, z0 + 33.0)
    coda += S(x0 - 7.0, x0 - 1.0, 2.0, 16.0, z0 + 10.0, z0 + 28.0)
    coda += S(x0 - 6.0, x0 - 1.0, 5.0, 13.0, z0 + 3.0, z0 + 10.0)
    pz["testa_retro"] = (retro + coda, "capelli", (0, 14, 62),
                         "Guscio posteriore con la coda: retro sul piatto, supporti sotto la coda")

    # Piastra del volto (pelle): sottile cornice attorno al display
    vo = S(-VOLTO_X + GIOCO / 2, VOLTO_X - GIOCO / 2, ty0, ty0 + VOLTO_S, z0, Z_FRANGIA - GIOCO / 2)
    vo -= fronte
    vo -= Pos(0, ty0 - 0.1, DISPLAY_Z) * (Rot(-90, 0, 0) * Cylinder(FINESTRA_D / 2, VOLTO_S + 0.2,
                                                                   align=(Align.CENTER, Align.CENTER, Align.MIN)))
    pz["volto"] = (vo, "pelle", (0, -30, 62), "Cornice 2 mm con la finestra Ø 38: il display è tutto il volto")

    # --- Cappello cavo -------------------------------------------------------
    cap = S(-27.0, 27.0, ty0 - 5.0, ty1 + 2.0, z1, z1 + FASCIA_H)
    cap += S(-23.0, 23.0, ty0, ty1 - 2.0, z1 + FASCIA_H, z1 + FASCIA_H + CAPPELLO_H)
    cap -= S(-20.5, 20.5, ty0 + 2.5, ty1 - 4.5, z1 - 0.01, z1 + FASCIA_H + CAPPELLO_H - 2.5)
    for (x, y) in SPINE_TESTA_XY:
        cap += SB.cilindro(x, y, z1, z1 + FASCIA_H + CAPPELLO_H - 2.5, 7.0)
        cap -= foro(x, y, z1 - 0.01, z1 + 4.0)
    pz["cappello"] = (cap, "cappello", (0, 0, 80), "Capovolto (cima sul piatto): la fascia sporge di 2–5 mm")
    # Fregio generico "a pixel" (non l'aquila ufficiale, DEC-053)
    px = 1.4
    schema = ["...#...", ".#.#.#.", "..###..", "#######", "..###..", ".#.#.#.", "...#..."]
    zc = z1 + FASCIA_H + CAPPELLO_H / 2
    fregio = None
    for r, riga in enumerate(schema):
        for c, ch in enumerate(riga):
            if ch == "#":
                q = S((c - 3.5) * px, (c - 2.5) * px, ty0 - 0.8, ty0, zc + (2.5 - r) * px, zc + (3.5 - r) * px)
                fregio = q if fregio is None else fregio + q
    pz["fregio"] = (fregio, "oro", (0, -12, 80), "Rilievo 0,8 mm a pixel 1,4 mm")

    # --- Ingombri non stampati ------------------------------------------------
    tondo = Pos(0, MOD_Y0, DISPLAY_Z) * (Rot(-90, 0, 0) * Cylinder(MOD_D / 2, MOD_T,
                                                                  align=(Align.CENTER, Align.CENTER, Align.MIN)))
    aletta = S(-ALETTA_W / 2, ALETTA_W / 2, MOD_Y0, MOD_Y1, ALETTA_Z0, DISPLAY_Z - 10.0)
    ingombri = {
        "modulo display": tondo + aletta,
        "spina Dupont display": S(-P.DUPONT_7_L / 2, P.DUPONT_7_L / 2, MOD_Y1, SPINA_Y1,
                                  PIN_Z - 1.27, PIN_Z + 1.27),
    }
    for n in ("scheda", "U3 WROOM-02", "J1 USB-C", "J3 SHT40", "J4 RTC", "J5 pulsante", "J2 header diritto",
              "spina Dupont display", "DS3231 (5188)", "DS3231 pila CR1220", "SHT40 modulo",
              "spina USB-C (sovrastampo)", "spina USB-C (guscio)"):
        ingombri["base " + n] = ing[n]
    ingombri["zavorra"] = zz
    return pz, ingombri


def main():
    pz, ingombri = parti()
    righe = []
    w = righe.append
    w("CONCEPT VOXEL v2 DELLA STATUETTA - PoliClock (DEC-053, DEC-054)")
    w("Generato da mechanical/cad/concept_voxel.py; quote in mm, Z dal tavolo.")
    w("")
    tutto = Compound(children=[v[0] for v in pz.values()])
    bb = tutto.bounding_box()
    h_testa_cap = TESTA[2] + FASCIA_H + CAPPELLO_H
    w("== Quote principali ==")
    w(f"Ingombro totale: {bb.size.X:.1f} (largh.) x {bb.size.Y:.1f} (prof.) x {bb.size.Z:.1f} (alt.)")
    w(f"Base: {SB.EST_X1 - SB.EST_X0:.1f} x {SB.EST_Y1 - SB.EST_Y0:.1f} x {Z_BASE:.1f}")
    w(f"Testa: {TESTA[0]:.0f} x {TESTA[1]:.0f} x {TESTA[2]:.0f}, da Z {Z_TESTA:.1f} a {Z_TESTA + TESTA[2]:.1f}; "
      f"cappello fino a Z {Z_TESTA + h_testa_cap:.1f}")
    w(f"Display: centro del vetro a Z {DISPLAY_Z:.1f}, finestra Ø {FINESTRA_D:.0f}; piastra del volto {2 * VOLTO_X:.0f} mm "
      f"(cornice di pelle di {VOLTO_X - FINESTRA_D / 2:.0f} mm ai lati)")
    w(f"Aletta del modulo fino a Z {ALETTA_Z0:.1f} ({Z_TESTA - ALETTA_Z0:.1f} mm dentro il busto); "
      f"spina Dupont a Z {PIN_Z:.1f}, da Y {MOD_Y1:.1f} a {SPINA_Y1:.1f}")
    w(f"Stivali Z {Z_BASE:.1f}-{Z_STIVALI:.1f}, pantaloni -{Z_PANTALONI:.1f}, cintura -{Z_CINTURA:.1f}, "
      f"busto -{Z_BUSTO:.1f}")
    w(f"Testa con cappello / altezza: {h_testa_cap / bb.size.Z:.2f}; altezza in teste (con cappello): "
      f"{bb.size.Z / h_testa_cap:.2f}")
    w("")
    w("== Parti (concept) ==")
    for n, (forma, col, _, nota) in pz.items():
        b = forma.bounding_box()
        w(f"{n:18s} {col:10s} {forma.volume / 1000:7.2f} cm3  {b.size.X:5.1f} x {b.size.Y:5.1f} x {b.size.Z:5.1f}  - {nota}")
    w("")
    w("== Controlli ==")
    nomi = list(pz)
    coppie = []
    for i, a in enumerate(nomi):
        for b in nomi[i + 1:]:
            v = SB.interseca(pz[a][0], pz[b][0])
            if v > 0.01:
                coppie.append((a, b, v))
    for a, b, v in coppie:
        w(f"  ATTENZIONE sovrapposizione {a} / {b}: {v:.2f} mm3")
    w(f"  Sovrapposizioni fra parti: {'PASS' if not coppie else 'FALLITO'}")
    vint = sum(SB.interseca(ingombri[k], pz[n][0]) for k in ("modulo display", "spina Dupont display") for n in nomi)
    w(f"  Modulo display (tondo + aletta) e spina senza interferenze: {'PASS' if vint < 0.01 else 'FALLITO'} ({vint:.2f} mm3)")
    sonda = S(-CANALE[0] / 2 + 1.0, CANALE[0] / 2 - 1.0, -CANALE[1] / 2 + 1.0, CANALE[1] / 2 - 1.0,
              Z_BASE - 2.4, ALETTA_Z0 - 1.0)
    vc = sum(SB.interseca(sonda, pz[n][0]) for n in nomi)
    w(f"  Canale {CANALE[0]:.0f} x {CANALE[1]:.0f} libero dalla base alla cavità del busto: "
      f"{'PASS' if vc < 0.01 else 'FALLITO'} ({vc:.2f} mm3)")
    w("  Interferenze nella base e distanze dall'antenna: vedi studio_base_rapporto.txt (stessa base, spigoli 5/4 mm)")
    zp_base = SB.Z_SCHEDA_SU + P.HEADER_DIRITTO_CORPO_H + P.DUPONT_H
    percorso = [(0, 0, zp_base), (0, 0, PIN_Z - 3.0), (0, SPINA_Y1 - 2.0, PIN_Z - 2.0), (0, SPINA_Y1, PIN_Z)]
    lung = sum(math.dist(percorso[i], percorso[i + 1]) for i in range(len(percorso) - 1))
    w(f"  Cavetto display: percorso fra le spine circa {lung:.0f} mm; Dupont da 10 cm "
      f"({'ok' if lung + 15 <= 100 else 'troppo corto'}, almeno 15 mm di gioco per sfilare la testa)")
    testo = "\n".join(righe) + "\n"
    print(testo)

    os.makedirs(DIR_PARTI, exist_ok=True)
    os.makedirs(DIR_OUT, exist_ok=True)
    for vecchio in glob.glob(os.path.join(DIR_PARTI, "*.stl")):   # niente parti residue della v1
        os.remove(vecchio)
    with open(RAPPORTO, "w", encoding="utf-8") as fh:
        fh.write(testo)
    dati = {"parti": {}, "ingombri": {}, "colori": COLORI, "percorso_cavo": percorso,
            "quote": {"z_base": Z_BASE, "z_testa": Z_TESTA, "z_cima": bb.max.Z, "display_z": DISPLAY_Z,
                      "faccia_y": Y_FACCIA, "spessore_volto": VOLTO_S, "testa": TESTA,
                      "finestra_d": FINESTRA_D}}
    for n, (forma, col, esp, nota) in pz.items():
        export_stl(forma, os.path.join(DIR_PARTI, n + ".stl"), tolerance=0.02, angular_tolerance=0.2)
        dati["parti"][n] = {"colore": col, "esploso": esp, "nota": nota}
        forma.label = n
    for vecchio in glob.glob(os.path.join(DIR_OUT, "ingombro_*.stl")):
        os.remove(vecchio)
    for n, forma in ingombri.items():
        fn = "ingombro_" + "".join(ch if ch.isalnum() else "_" for ch in n) + ".stl"
        export_stl(forma, os.path.join(DIR_OUT, fn), tolerance=0.05)
        dati["ingombri"][n] = fn
    with open(os.path.join(DIR_OUT, "concept.json"), "w", encoding="utf-8") as fh:
        json.dump(dati, fh, indent=1)
    export_step(Compound(children=[v[0] for v in pz.values()], label="PoliClock concept voxel v2"), STEP_ASSIEME)
    print(f"Esportate {len(pz)} parti in mechanical/prints/concept/ e l'assieme {os.path.basename(STEP_ASSIEME)}")


if __name__ == "__main__":
    main()
