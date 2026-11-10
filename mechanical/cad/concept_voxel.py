"""Primo concept 3D della statuetta PoliClock in stile "a cubetti" (voxel).

Stile dal riferimento del proprietario (assets/concept/riferimento-stile-chibi-voxel.webp):
testa a cubo, cappello blu notte, capelli castani con coda laterale, camicia
blu notte a maniche corte con spalline rosse e oro e tasche, cintura con
fondina e fibbia, pantaloni azzurri con banda rossa, stivali neri, tutto sul
piedistallo che contiene la scheda (DEC-048) con la USB-C sul retro.

Vincoli tecnici:
- il volto è il display rotondo 1,28" (SC-001): finestra nella piastra del
  volto, modulo segnaposto 38 x 45,5 x 4,8 mm con l'aletta dei pin in basso
  (OPEN-016);
- canale 21 x 6 mm per il cavetto Dupont dal piano della base al pavimento
  della testa (docs/06 §12.2);
- base dallo studio volumetrico (studio_base.py), con spigoli "a blocco";
- insegne stilizzate (DEC-053): fregio dorato generico a pixel (non l'aquila
  ufficiale), targhetta "POLIZIA", toppa tricolore. Nessuna insegna ufficiale.

Le parti sono divise per colore; giunzioni, spessori e tolleranze sono di
concept, da adattare al servizio di stampa (DEC-052, OPEN-032).

Uso (dalla radice del repository):
  ..\\.venv-cad\\Scripts\\python.exe mechanical/cad/concept_voxel.py
Uscite:
  mechanical/prints/concept/<parte>.stl     una per parte (concept, non definitive)
  mechanical/prints/concept-statuetta.step  assieme
  mechanical/cad/concept_rapporto.txt       quote e controlli
  mechanical/cad/out/concept/...            ingombri e dati per Blender (non versionati)
"""

import json
import os
import sys

from build123d import (
    Align, Compound, Cylinder, FontStyle, Pos, Rot, Text, Box,
    export_step, export_stl, extrude,
)

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
# Quote del concept (mm). Z dal tavolo; X, Y come nello studio della base.
# ---------------------------------------------------------------------------
Z_BASE = SB.ALTEZZA_BASE            # 24,1
Z_STIVALI = Z_BASE + 9.0            # 33,1
Z_PANTALONI = Z_STIVALI + 16.0      # 49,1
Z_CINTURA = Z_PANTALONI + 4.0       # 53,1
Z_BUSTO = Z_CINTURA + 23.0          # 76,1
Z_TESTA = Z_BUSTO + 2.0             # 78,1 (collo nascosto)
TESTA = (70.0, 64.0, 70.0)          # larghezza, profondità, altezza
Z_TESTA_SU = Z_TESTA + TESTA[2]     # 148,1
CAPPELLO_H = 14.0                   # calotta sopra la fascia
FASCIA_H = 5.0

PARETE_TESTA = 3.0
FACCIA_Y = -TESTA[1] / 2            # piano del volto
DISPLAY_Z = Z_TESTA + 30.0          # centro del vetro: aletta del modulo sopra il pavimento
FINESTRA_D = 38.0                   # vetro Ø 37,5 (segnaposto) + gioco
CANALE = P.CANALE_CAVO              # 21 x 6
GIOCO = 0.2                         # fra parti incastrate (concept)
SPINA = 3.2                         # fori per spine di allineamento Ø 3 mm
PROFONDITA_FRONTE_TESTA = 12.0      # spessore della parte anteriore della testa

# Colori in sRGB (0-1), convertiti in lineare da Blender
COLORI = {
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


# Spine di allineamento fra parti impilate (fori ciechi 4 mm per lato)
SPINE_XY = [(-14.0, 0.0), (14.0, 0.0)]


def con_spine(forma, z_giunto, sopra=True, sotto=True):
    for (x, y) in SPINE_XY:
        if sopra:
            forma -= foro(x, y, z_giunto - 4.0, z_giunto + 0.01)
        if sotto:
            forma -= foro(x, y, z_giunto - 0.01, z_giunto + 4.0)
    return forma


# ---------------------------------------------------------------------------
# Parti
# ---------------------------------------------------------------------------
def parti():
    pz = {}   # nome: (forma, colore, esploso (dx, dy, dz), nota di stampa)

    # --- Base dallo studio ------------------------------------------------
    ing, ds = SB.ingombri()
    g = SB.guscio(ds)
    f, zz = SB.fondo()
    pz["base_guscio"] = (g, "base", (0, 0, 0), "Capovolta (piano superiore sul piatto); USB-C e feritoie verticali")
    pz["base_fondo"] = (f, "fondo", (0, 0, -32), "Piatta; è lo sportello di servizio (OPEN-008)")

    # --- Stivali (due pezzi, mezzo canale ciascuno) ------------------------
    for lato, sx in (("dx", -1), ("sx", 1)):   # dx = destra della chibi = -X
        x0, x1 = sorted((sx * 0.25, sx * 19.75))
        b = S(x0, x1, -17.0, 9.0, Z_BASE, Z_STIVALI)
        b -= canale(Z_BASE - 1, Z_STIVALI + 1)
        # foro per l'inserto M3 della vite dal basso (VITI_CORPO_XY)
        vx, vy = [v for v in P.VITI_CORPO_XY if v[0] * sx > 0][0]
        b -= SB.cilindro(vx, vy, Z_BASE - 0.01, Z_BASE + 6.0, 4.0)
        b = con_spine(b, Z_STIVALI, sopra=True, sotto=False)
        pz[f"stivale_{lato}"] = (b, "nero", (sx * 6, 0, 10), "Suola sul piatto")

    # --- Pantaloni con banda rossa ------------------------------------------
    pa = S(-19.5, 19.5, -11.0, 11.0, Z_STIVALI, Z_PANTALONI)
    for y in (-11.0, 11.0):   # solco fra le gambe, davanti e dietro
        pa -= S(-1.0, 1.0, y - 1.5, y + 1.5, Z_STIVALI - 0.1, Z_PANTALONI - 4.0)
    for sx in (-1, 1):        # sede della banda
        pa -= S(sx * 18.7, sx * 19.6, -1.6, 1.6, Z_STIVALI - 0.1, Z_PANTALONI + 0.1)
    pa -= canale(Z_STIVALI - 1, Z_PANTALONI + 1)
    pa = con_spine(pa, Z_STIVALI, sopra=False, sotto=True)
    pa = con_spine(pa, Z_PANTALONI, sopra=True, sotto=False)
    pz["pantaloni"] = (pa, "pantaloni", (0, 0, 20), "In piedi; banda rossa incastrata o dipinta")
    for lato, sx in (("dx", -1), ("sx", 1)):
        x0, x1 = sorted((sx * (18.7 + GIOCO / 2), sx * 19.5))
        pz[f"banda_{lato}"] = (S(x0, x1, -1.4, 1.4, Z_STIVALI + 0.2, Z_PANTALONI - 0.2), "rosso",
                               (sx * 16, 0, 20), "Listello 0,8 mm: meglio dipinto se il servizio non regge lo spessore")

    # --- Cintura, fibbia, fondina, tasca ----------------------------------
    ci = S(-21.0, 21.0, -12.5, 12.5, Z_PANTALONI, Z_CINTURA)
    ci -= canale(Z_PANTALONI - 1, Z_CINTURA + 1)
    ci -= S(-4.2, 4.2, -12.6, -11.8, Z_PANTALONI + 0.4, Z_CINTURA - 0.4)   # sede fibbia
    for (x, y) in SPINE_XY:
        ci -= foro(x, y, Z_PANTALONI - 0.1, Z_CINTURA + 0.1)
    fondina = S(-27.5, -19.5, -15.0, -6.5, Z_PANTALONI - 13.0, Z_CINTURA)
    fondina += S(-26.5, -20.5, -15.6, -14.9, Z_PANTALONI - 6.0, Z_PANTALONI - 2.0)  # patta
    tasca = S(19.6, 26.0, -14.5, -8.0, Z_PANTALONI - 5.0, Z_CINTURA)
    ci = ci + fondina + tasca
    pz["cintura"] = (ci, "nero", (0, 0, 30), "Anello con fondina e tasca; le spine Ø 3 attraversano")
    pz["fibbia"] = (S(-4.0, 4.0, -13.5, -12.0, Z_PANTALONI + 0.6, Z_CINTURA - 0.6), "grigio", (0, -10, 30),
                    "Piastrina incastrata nella cintura")

    # --- Busto (camicia) con maniche, colletto, tasche ---------------------
    bu = S(-20.0, 20.0, -12.0, 12.0, Z_CINTURA, Z_BUSTO)
    for sx in (-1, 1):
        x0, x1 = sorted((sx * 20.0, sx * 30.0))
        bu += S(x0, x1, -7.0, 7.0, Z_BUSTO - 14.0, Z_BUSTO)          # manica corta
        x0, x1 = sorted((sx * 21.0, sx * 29.0))
        bu += S(x0, x1, -7.6, 7.6, Z_BUSTO - 16.0, Z_BUSTO - 13.0)   # risvolto della manica
        x0, x1 = sorted((sx * 5.0, sx * 15.0))
        bu += S(x0, x1, -13.0, -12.0, Z_CINTURA + 4.5, Z_CINTURA + 10.0)   # taschino
        bu += S(x0, x1, -13.4, -12.9, Z_CINTURA + 8.6, Z_CINTURA + 10.6)   # patta
    # colletto a "V" a blocchi
    for sx in (-1, 1):
        for i in range(2):
            x0, x1 = sorted((sx * (1.5 + 2.5 * i), sx * (4.0 + 2.5 * i)))
            bu += S(x0, x1, -13.0, -11.9, Z_BUSTO - 2.5 - 2.0 * i, Z_BUSTO)
    # sedi della targhetta e della toppa
    bu -= S(-18.0, -6.5, -12.1, -11.4, Z_CINTURA + 11.5, Z_CINTURA + 17.5)
    bu -= S(6.5, 18.5, -12.1, -11.4, Z_CINTURA + 11.5, Z_CINTURA + 17.5)
    bu -= canale(Z_CINTURA - 1, Z_BUSTO + 1)
    for (x, y) in SPINE_XY:
        bu -= foro(x, y, Z_CINTURA - 0.01, Z_CINTURA + 4.0)
        bu -= foro(x, y, Z_BUSTO - 4.0, Z_BUSTO + 0.01)
    # sedi delle braccia sotto le maniche
    for sx in (-1, 1):
        bu -= foro(sx * 25.0, 0.0, Z_BUSTO - 16.01, Z_BUSTO - 12.0)
    pz["busto"] = (bu, "camicia", (0, 0, 42), "In piedi; maniche e risvolti sporgono di 1 mm al massimo")

    # Braccia (pelle): avambraccio e mano
    for lato, sx in (("dx", -1), ("sx", 1)):
        x0, x1 = sorted((sx * 21.0, sx * 29.0))
        br = S(x0, x1, -6.0, 6.0, Z_PANTALONI - 4.0, Z_BUSTO - 16.0)
        br -= foro(sx * 25.0, 0.0, Z_BUSTO - 20.0, Z_BUSTO - 15.99)
        pz[f"braccio_{lato}"] = (br, "pelle", (sx * 18, 0, 36), "Spina Ø 3 nella manica")

    # Spalline rosse con grado dorato
    for lato, sx in (("dx", -1), ("sx", 1)):
        x0, x1 = sorted((sx * 13.2, sx * 26.0))
        pz[f"spallina_{lato}"] = (S(x0, x1, -5.0, 5.0, Z_BUSTO, Z_BUSTO + 1.4), "rosso", (sx * 10, 0, 52),
                                  "Piastrina 1,4 mm")
        x0, x1 = sorted((sx * 20.0, sx * 24.5))
        pz[f"grado_{lato}"] = (S(x0, x1, -3.0, 3.0, Z_BUSTO + 1.4, Z_BUSTO + 2.0), "oro", (sx * 10, 0, 58),
                               "Dettaglio 0,6 mm: dipinto se troppo sottile per il servizio")

    # Targhetta "POLIZIA" (destra del petto guardando, sinistra della chibi)
    zt = Z_CINTURA + 12.0
    pz["targhetta"] = (S(6.7, 18.3, -12.4, -11.45, zt, zt + 5.3), "targhetta", (0, -12, 42), "Piastrina")
    testo = extrude(Text("POLIZIA", font_size=2.9, font="Arial", font_style=FontStyle.BOLD), 0.5)
    testo = Pos(12.5, -12.4, zt + 2.65) * (Rot(90, 0, 0) * testo)
    pz["scritta_polizia"] = (testo, "bianco", (0, -14, 42), "Lettere in rilievo 0,5 mm: stampa multicolore o pittura")
    # Toppa tricolore (verde, bianco, rosso da sinistra guardando)
    for i, (n, c) in enumerate((("verde", "verde"), ("bianco", "bianco"), ("rosso", "rosso"))):
        x0 = -17.8 + i * 3.6
        pz[f"toppa_{n}"] = (S(x0, x0 + 3.6, -12.4, -11.45, zt, zt + 5.3), c, (0, -12, 42), "Piastrina")

    # Collo (pelle), nascosto sotto la testa
    co = S(-13.0, 13.0, -6.0, 6.0, Z_BUSTO, Z_TESTA)
    co -= canale(Z_BUSTO - 1, Z_TESTA + 1)
    for (x, y) in SPINE_XY:
        co -= foro(x, y, Z_BUSTO - 0.1, Z_TESTA + 0.1)
    pz["collo"] = (co, "pelle", (0, 0, 48), "Anello sottile; si può unire al busto")

    # --- Testa -----------------------------------------------------------
    W, D, H = TESTA
    x0, x1, y0, y1, z0, z1 = -W / 2, W / 2, -D / 2, D / 2, Z_TESTA, Z_TESTA_SU
    t = PARETE_TESTA
    guscio_testa = S(x0, x1, y0, y1, z0, z1) - S(x0 + t, x1 - t, y0 + t, y1 - t, z0 + t, z1 - t)
    guscio_testa -= canale(z0 - 1, z0 + t + 1)
    for (x, y) in SPINE_XY:
        guscio_testa -= foro(x, y, z0 - 0.1, z0 + 4.0)
        guscio_testa -= foro(x, y, z1 - 4.0, z1 + 0.1)   # spine del cappello
    # apertura del volto: la parte di pelle va fra le ciocche e sotto la frangia
    VOLTO_X = 30.0
    Z_FRANGIA = z1 - 12.0
    apertura = S(-VOLTO_X, VOLTO_X, y0 - 1, y0 + t + 0.01, z0 + t, Z_FRANGIA)
    guscio_testa -= apertura
    yf = y0 + PROFONDITA_FRONTE_TESTA
    fronte = guscio_testa & S(x0 - 1, x1 + 1, y0 - 1, yf, z0 - 1, z1 + 1)
    retro = guscio_testa - S(x0 - 1, x1 + 1, y0 - 1, yf, z0 - 1, z1 + 1)
    # ciuffi "a pixel" della frangia sul volto
    for (a, b, h) in ((-30.0, -21.0, 4.0), (-21.0, -12.0, 2.0), (8.0, 18.0, 3.0), (18.0, 30.0, 9.0)):
        fronte += S(a, b, y0, y0 + t, Z_FRANGIA - h, Z_FRANGIA)
    # basette che scendono lungo il volto
    for sx in (-1, 1):
        a, b = sorted((sx * VOLTO_X, sx * (VOLTO_X - 3.0)))
        fronte += S(a, b, y0, y0 + t, z0 + 30.0, Z_FRANGIA)
    pz["testa_fronte"] = (fronte, "capelli", (0, -14, 62),
                          "Cornice anteriore dei capelli; si unisce a testa_retro con 2 viti M2,5 dal pavimento")
    # coda laterale sul lato destro della chibi (-X), a gradini
    coda = S(x0 - 5.0, x0, 8.0, 22.0, z0 + 34.0, z0 + 44.0)            # elastico/attacco
    coda += S(x0 - 10.0, x0 - 2.0, 6.0, 24.0, z0 + 14.0, z0 + 36.0)
    coda += S(x0 - 8.0, x0 - 2.0, 9.0, 21.0, z0 + 4.0, z0 + 14.0)
    retro = retro + coda
    pz["testa_retro"] = (retro, "capelli", (0, 14, 62),
                         "Guscio posteriore con la coda: stampa con il retro sul piatto, supporti sotto la coda")

    # Piastra del volto (pelle) con la finestra del display
    zf0, zf1 = z0 + t + GIOCO / 2, Z_FRANGIA - GIOCO / 2
    vo = S(-VOLTO_X + GIOCO / 2, VOLTO_X - GIOCO / 2, y0, y0 + t, zf0, zf1)
    # le parti della frangia e delle basette coprono la piastra: sottrarle
    vo -= fronte
    fin = Pos(0, y0 - 0.1, DISPLAY_Z) * (Rot(-90, 0, 0) * Cylinder(FINESTRA_D / 2, t + 0.2, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    vo -= fin
    # cornice di appoggio del modulo dietro la piastra (guide laterali)
    mw, mh, mt = P.DISPLAY_PCB[0], P.DISPLAY_PCB[1], P.DISPLAY_SPESSORE
    zm0 = DISPLAY_Z - P.DISPLAY_TONDO_D / 2 - (mh - P.DISPLAY_TONDO_D)
    for sx in (-1, 1):
        a, b = sorted((sx * (mw / 2 + 0.3), sx * (mw / 2 + 2.3)))
        vo += S(a, b, y0 + t, y0 + t + mt + 1.0, zm0 + 4.0, zm0 + mh - 4.0)
    pz["volto"] = (vo, "pelle", (0, -30, 62), "Piastra 3 mm con la finestra Ø 38; il modulo display si appoggia dietro")

    # --- Cappello --------------------------------------------------------
    zc0 = z1
    fascia = S(-36.5, 36.5, -38.0, 34.0, zc0, zc0 + FASCIA_H)
    calotta = S(-32.0, 32.0, -31.0, 31.0, zc0 + FASCIA_H, zc0 + FASCIA_H + CAPPELLO_H)
    cap = fascia + calotta
    # cappello cavo (pareti 2,5 mm): appoggia sul tetto della testa
    cap -= S(-29.5, 29.5, -28.5, 28.5, zc0 - 0.01, zc0 + FASCIA_H + CAPPELLO_H - 2.5)
    for (x, y) in SPINE_XY:   # bossoli delle spine
        cap += SB.cilindro(x, y, zc0, zc0 + FASCIA_H + CAPPELLO_H - 2.5, 7.0)
    for (x, y) in SPINE_XY:
        cap -= foro(x, y, zc0 - 0.01, zc0 + 4.0)
    pz["cappello"] = (cap, "cappello", (0, 0, 84), "Capovolto (cima sul piatto): la fascia sporge di 4–7 mm")
    # Fregio generico "a pixel": stella a otto punte stilizzata (non l'aquila ufficiale)
    px = 1.6
    schema = ["...#...", ".#.#.#.", "..###..", "#######", "..###..", ".#.#.#.", "...#..."]
    zc = zc0 + FASCIA_H + CAPPELLO_H / 2
    fregio = None
    for r, riga in enumerate(schema):
        for c, ch in enumerate(riga):
            if ch == "#":
                q = S((c - 3.5) * px, (c - 2.5) * px, -31.8, -31.0, zc + (2.5 - r) * px, zc + (3.5 - r) * px)
                fregio = q if fregio is None else fregio + q
    pz["fregio"] = (fregio, "oro", (0, -12, 84), "Rilievo 0,8 mm a pixel 1,6 mm")

    ingombri = {
        "modulo display": S(-mw / 2, mw / 2, y0 + t, y0 + t + mt, zm0, zm0 + mh),
        "spina Dupont display": S(-P.DUPONT_7_L / 2, P.DUPONT_7_L / 2, y0 + t + mt, y0 + t + mt + 2.5 + P.DUPONT_H,
                                  zm0 + 1.2, zm0 + 1.2 + 2.54),
    }
    for n in ("scheda", "U3 WROOM-02", "J1 USB-C", "J3 SHT40", "J4 RTC", "J5 pulsante", "J2 header diritto",
              "spina Dupont display", "DS3231 (5188)", "DS3231 pila CR1220", "SHT40 modulo",
              "spina USB-C (sovrastampo)", "spina USB-C (guscio)"):
        ingombri["base " + n] = ing[n]
    ingombri["zavorra"] = zz
    return pz, ingombri, (zm0, mh, mt)


def main():
    pz, ingombri, (zm0, mh, mt) = parti()
    righe = []
    w = righe.append
    w("CONCEPT VOXEL DELLA STATUETTA - PoliClock (stile del riferimento del proprietario)")
    w("Generato da mechanical/cad/concept_voxel.py; quote in mm, Z dal tavolo.")
    w("")
    tutto = Compound(children=[v[0] for v in pz.values()])
    bb = tutto.bounding_box()
    w("== Quote principali ==")
    w(f"Ingombro totale: {bb.size.X:.1f} (largh.) x {bb.size.Y:.1f} (prof.) x {bb.size.Z:.1f} (alt.)")
    w(f"Base: {SB.EST_X1 - SB.EST_X0:.1f} x {SB.EST_Y1 - SB.EST_Y0:.1f} x {Z_BASE:.1f}")
    w(f"Testa: {TESTA[0]:.0f} x {TESTA[1]:.0f} x {TESTA[2]:.0f}, da Z {Z_TESTA:.1f} a {Z_TESTA_SU:.1f}; "
      f"cappello fino a Z {Z_TESTA_SU + FASCIA_H + CAPPELLO_H:.1f}")
    w(f"Display: centro del vetro a Z {DISPLAY_Z:.1f}, finestra Ø {FINESTRA_D:.0f}; modulo da Z {zm0:.1f} a {zm0 + mh:.1f}")
    w(f"Stivali Z {Z_BASE:.1f}-{Z_STIVALI:.1f}, pantaloni -{Z_PANTALONI:.1f}, cintura -{Z_CINTURA:.1f}, "
      f"busto -{Z_BUSTO:.1f}, collo -{Z_TESTA:.1f}")
    w(f"Proporzione testa (con cappello) / altezza: "
      f"{(TESTA[2] + FASCIA_H + CAPPELLO_H) / bb.size.Z:.2f}; altezza in teste: {bb.size.Z / TESTA[2]:.2f}")
    w("")
    w("== Parti (concept) ==")
    w(f"{'parte':22s} {'colore':10s} {'volume cm3':>10s}  ingombro (mm)")
    for n, (forma, col, _, nota) in pz.items():
        b = forma.bounding_box()
        w(f"{n:22s} {col:10s} {forma.volume / 1000:10.2f}  {b.size.X:5.1f} x {b.size.Y:5.1f} x {b.size.Z:5.1f}  - {nota}")
    w("")
    w("== Controlli ==")
    nomi = list(pz)
    peggiore, coppie = 0.0, []
    for i, a in enumerate(nomi):
        for b in nomi[i + 1:]:
            if pz[a][0].bounding_box().overlaps(pz[b][0].bounding_box()) if hasattr(pz[a][0].bounding_box(), "overlaps") else True:
                v = SB.interseca(pz[a][0], pz[b][0])
                if v > 0.01:
                    coppie.append((a, b, v))
                peggiore = max(peggiore, v)
    for a, b, v in coppie:
        w(f"  ATTENZIONE sovrapposizione {a} / {b}: {v:.2f} mm3")
    w(f"  Sovrapposizioni fra parti: {'PASS' if not coppie else 'FALLITO'} (massimo {peggiore:.2f} mm3)")
    mod = ingombri["modulo display"]
    spina = ingombri["spina Dupont display"]
    vint = sum(SB.interseca(mod, pz[n][0]) + SB.interseca(spina, pz[n][0]) for n in nomi)
    w(f"  Modulo display e spina dentro la testa senza interferenze: {'PASS' if vint < 0.01 else 'FALLITO'} ({vint:.2f} mm3)")
    # continuità del canale: un prisma 20 x 5 dal piano della base al pavimento della testa
    # sonda 19 x 4 (il foro nel piano della base ha raccordi di 2 mm agli spigoli)
    sonda = SB.scatola(-CANALE[0] / 2 + 1.0, CANALE[0] / 2 - 1.0, -CANALE[1] / 2 + 1.0, CANALE[1] / 2 - 1.0,
                       Z_BASE - 2.4, Z_TESTA + PARETE_TESTA + 0.5)
    vc = sum(SB.interseca(sonda, pz[n][0]) for n in nomi)
    w(f"  Canale {CANALE[0]:.0f} x {CANALE[1]:.0f} libero dalla base alla testa: {'PASS' if vc < 0.01 else 'FALLITO'} ({vc:.2f} mm3)")
    w("  Interferenze nella base e distanze dall'antenna: vedi studio_base_rapporto.txt (stessa base, spigoli 5/4 mm)")
    # percorso del cavetto per Blender e stima della lunghezza
    zp_base = SB.Z_SCHEDA_SU + P.HEADER_DIRITTO_CORPO_H + P.DUPONT_H
    yp_testa = FACCIA_Y + PARETE_TESTA + mt + 2.5 + P.DUPONT_H
    zp_testa = zm0 + 1.2 + 1.27
    percorso = [(0, 0, zp_base), (0, 0, Z_TESTA - 6.0), (0, -1.0, zp_testa - 0.5), (0, yp_testa - 1.0, zp_testa)]
    lung = sum(((percorso[i + 1][0] - percorso[i][0]) ** 2 + (percorso[i + 1][1] - percorso[i][1]) ** 2 +
                (percorso[i + 1][2] - percorso[i][2]) ** 2) ** 0.5 for i in range(len(percorso) - 1))
    w(f"  Cavetto display: percorso fra le spine circa {lung:.0f} mm (Dupont da 10 cm)")
    testo = "\n".join(righe) + "\n"
    print(testo)

    os.makedirs(DIR_PARTI, exist_ok=True)
    os.makedirs(DIR_OUT, exist_ok=True)
    with open(RAPPORTO, "w", encoding="utf-8") as fh:
        fh.write(testo)
    dati = {"parti": {}, "ingombri": {}, "colori": COLORI, "percorso_cavo": percorso,
            "quote": {"z_base": Z_BASE, "z_testa": Z_TESTA, "z_cima": bb.max.Z, "display_z": DISPLAY_Z,
                      "faccia_y": FACCIA_Y, "testa": TESTA}}
    for n, (forma, col, esp, nota) in pz.items():
        export_stl(forma, os.path.join(DIR_PARTI, n + ".stl"), tolerance=0.02, angular_tolerance=0.2)
        dati["parti"][n] = {"colore": col, "esploso": esp, "nota": nota}
        forma.label = n
    for n, forma in ingombri.items():
        fn = "ingombro_" + "".join(ch if ch.isalnum() else "_" for ch in n) + ".stl"
        export_stl(forma, os.path.join(DIR_OUT, fn), tolerance=0.05)
        dati["ingombri"][n] = fn
    with open(os.path.join(DIR_OUT, "concept.json"), "w", encoding="utf-8") as fh:
        json.dump(dati, fh, indent=1)
    export_step(Compound(children=[v[0] for v in pz.values()], label="PoliClock concept voxel"), STEP_ASSIEME)
    print(f"Esportate {len(pz)} parti in mechanical/prints/concept/ e l'assieme {os.path.basename(STEP_ASSIEME)}")


if __name__ == "__main__":
    main()
