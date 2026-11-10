"""Studio volumetrico 1:1 della base di PoliClock (OPEN-028, DEC-048).

La scheda principale sta nella base d'appoggio della statuetta; la USB-C esce
dal retro della base. Lo script costruisce:
- guscio della base (pareti + piano superiore, stampato capovolto);
- fondo apribile (sportello di servizio, OPEN-008) con vasca della zavorra;
- ingombri: scheda (dallo STEP di KiCad), componenti alti, spine dei cavi,
  modulo DS3231, modulo SHT40, zavorra, spina USB-C del cavo;
poi controlla interferenze e distanza del metallo dall'antenna e scrive un
rapporto con le quote minime.

Uso (dalla radice del repository):
  ..\\.venv-cad\\Scripts\\python.exe mechanical/cad/studio_base.py
Opzioni:
  --senza-export   solo controlli e rapporto
  --viewer         mostra il modello in OCP CAD Viewer (VS Code)

Uscite:
  mechanical/prints/base-guscio.stl, base-fondo.stl   prova dimensionale 1:1
  mechanical/prints/studio-volumi-base.step           assieme con gli ingombri
  mechanical/cad/out/*.stl                            ingombri per Blender (non versionati)
  mechanical/cad/studio_base_rapporto.txt             quote e controlli
"""

import argparse
import math
import os
import sys

from build123d import (
    Align, Axis, Box, Compound, Cylinder, Location, Pos, Rectangle,
    RectangleRounded, Solid, export_step, export_stl, extrude, fillet,
    import_step,
)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import parametri as P  # noqa: E402

RADICE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
STEP_SCHEDA = os.path.join(RADICE, "hardware", "policlock-main", "policlock-main-scheda.step")
DIR_PRINTS = os.path.join(RADICE, "mechanical", "prints")
DIR_OUT = os.path.join(RADICE, "mechanical", "cad", "out")
RAPPORTO = os.path.join(RADICE, "mechanical", "cad", "studio_base_rapporto.txt")


# --------------------------------------------------------------------------
# Utilità
# --------------------------------------------------------------------------
def scatola(x0, x1, y0, y1, z0, z1):
    """Parallelepipedo dati gli estremi (in qualunque ordine)."""
    x0, x1 = sorted((x0, x1))
    y0, y1 = sorted((y0, y1))
    z0, z1 = sorted((z0, z1))
    return Pos(x0, y0, z0) * Box(x1 - x0, y1 - y0, z1 - z0, align=(Align.MIN,) * 3)


def cilindro(x, y, z0, z1, d):
    return Pos(x, y, z0) * Cylinder(d / 2, z1 - z0, align=(Align.CENTER, Align.CENTER, Align.MIN))


def forma_d(x0, x1, y0, y1, r_fronte, r_retro):
    """Pianta della base: retro piatto (spigoli piccoli), fronte arrotondato."""
    f = Pos((x0 + x1) / 2, (y0 + y1) / 2) * Rectangle(x1 - x0, y1 - y0)
    f = fillet(f.vertices().sort_by(Axis.Y)[:2], r_fronte)
    f = fillet(f.vertices().sort_by(Axis.Y)[-2:], r_retro)
    return f


def da_scheda(u, v):
    """Coordinate scheda (u, v) -> statuetta (X, Y). Scheda ruotata di 180°."""
    return P.J2_U - u, P.J2_V - v


def volume_cm3(forma):
    return forma.volume / 1000.0 if forma is not None else 0.0


def interseca(a, b):
    try:
        r = a & b
        return r.volume if r is not None else 0.0
    except Exception:  # OCCT può fallire su intersezioni vuote
        return 0.0


# --------------------------------------------------------------------------
# Quote derivate
# --------------------------------------------------------------------------
Z_SCHEDA = P.FONDO + P.LUCE_SOTTO_SCHEDA          # lato inferiore della scheda
Z_SCHEDA_SU = Z_SCHEDA + P.SCHEDA_SPESSORE        # lato componenti
Z_CIELO_INT = Z_SCHEDA_SU + P.PH_CAVO_SOPRA_SCHEDA  # faccia inferiore del piano superiore
ALTEZZA_BASE = Z_CIELO_INT + P.CIELO

# Estremi della scheda nella statuetta
SX, DX = da_scheda(P.SCHEDA_L, 0)[0], da_scheda(0, 0)[0]          # -33.0, 17.5
FR, RE = da_scheda(0, P.SCHEDA_P)[1], da_scheda(0, 0)[1]          # -4.4, 37.1

# Cavità interna
INT_X0 = SX - P.GIOCO_SCHEDA
INT_X1 = DX + P.LARGHEZZA_DESTRA
INT_Y1 = RE + 0.4 + 0.3                     # guscio USB-C sporgente 0,4 + gioco
INT_Y0 = -P.PROFONDITA_FRONTE + P.PARETE
# Esterno
EST_X0, EST_X1 = INT_X0 - P.PARETE, INT_X1 + P.PARETE
EST_Y0, EST_Y1 = INT_Y0 - P.PARETE, INT_Y1 + P.PARETE_RETRO

USB_X, _ = da_scheda(P.USB_U, 0)
USB_Z = Z_SCHEDA + P.USB_Z_SU_SCHEDA


# --------------------------------------------------------------------------
# Ingombri (non stampati)
# --------------------------------------------------------------------------
def ingombri():
    ing = {}
    # Scheda dallo STEP di KiCad (solo contorno), ruotata e traslata
    pcb = import_step(STEP_SCHEDA)
    pcb = pcb.rotate(Axis.Z, 180).moved(Location((P.J2_U + 100.0, P.J2_V - 140.0, Z_SCHEDA)))
    ing["scheda"] = pcb
    for nome, (u0, u1, v0, v1, z0, z1) in P.COMPONENTI.items():
        x0, y0 = da_scheda(u0, v0)
        x1, y1 = da_scheda(u1, v1)
        ing[nome] = scatola(x0, x1, y0, y1, Z_SCHEDA + z0, Z_SCHEDA + z1)
    # Spine JST PH con cavo che sale e piega (segnaposto)
    for nome in ("J3 SHT40", "J4 RTC", "J5 pulsante"):
        u0, u1, v0, v1, _, _ = P.COMPONENTI[nome]
        x0, y0 = da_scheda(u0, v0)
        x1, y1 = da_scheda(u1, v1)
        ing["spina " + nome] = scatola(x0, x1, y0, y1, Z_SCHEDA + 7.6, Z_SCHEDA_SU + P.PH_CAVO_SOPRA_SCHEDA - 0.5)
    # Header J2 diritto + spina Dupont 7 vie verticale (variante consigliata)
    zc = Z_SCHEDA_SU + P.HEADER_DIRITTO_CORPO_H
    # header 1x8: dal pin 1 al pin 8, mezzo passo oltre i pin estremi
    ha, _ = da_scheda(P.J2_PIN1_U - 1.27, 0)
    hb, _ = da_scheda(P.J2_PIN1_U + (P.J2_N_PIN - 1) * 2.54 + 1.27, 0)
    ing["J2 header diritto"] = scatola(ha, hb, -1.27, 1.27, Z_SCHEDA_SU, zc)
    ing["spina Dupont display"] = scatola(-P.DUPONT_7_L / 2, P.DUPONT_7_L / 2, -1.27, 1.27, zc, zc + P.DUPONT_H)
    # DS3231 nella culla sotto il piano, pila verso il fondo (accessibile)
    l, w, h = P.DS3231
    x0, x1 = INT_X1 - 1.2 - w, INT_X1 - 1.2
    y1 = INT_Y1 - 1.0
    y0 = y1 - l
    z1 = Z_CIELO_INT - 0.5
    zp = z1 - P.DS3231_SOPRA - P.DS3231_PCB
    xc, yc, mp = (x0 + x1) / 2, (y0 + y1) / 2, P.DS3231_PILA / 2
    ing["DS3231 (5188)"] = scatola(x0, x1, y0, y1, zp, z1)
    ing["DS3231 pila CR1220"] = scatola(xc - mp, xc + mp, yc - mp, yc + mp, z1 - h, zp)
    ds = (x0, x1, y0, y1, z1 - h, z1)
    # SHT40 in piedi contro la parete destra ventilata, spina orizzontale
    sx1 = INT_X1 - 1.6
    ing["SHT40 modulo"] = scatola(sx1 - P.SHT40[2], sx1, -10.0, -10.0 + P.SHT40[0], 5.0, 5.0 + P.SHT40[1])
    ing["SHT40 spina"] = scatola(sx1 - P.SHT40[2] - 2.5 - P.DUPONT_H, sx1 - P.SHT40[2],
                                 -10.0 + (P.SHT40[0] - P.DUPONT_4_L) / 2,
                                 -10.0 + (P.SHT40[0] + P.DUPONT_4_L) / 2, 13.0, 15.5)
    # Spina USB-C del cavo, inserita
    lw, lh, ll = P.SPINA_USB_SOVRASTAMPO
    ing["spina USB-C (sovrastampo)"] = scatola(USB_X - lw / 2, USB_X + lw / 2, INT_Y1, INT_Y1 + ll,
                                               USB_Z - lh / 2, USB_Z + lh / 2)
    ing["spina USB-C (guscio)"] = scatola(USB_X - 4.2, USB_X + 4.2, RE - 6.0, INT_Y1, USB_Z - 1.3, USB_Z + 1.3)
    return ing, ds


# --------------------------------------------------------------------------
# Guscio della base
# --------------------------------------------------------------------------
CAMERA_SHT40 = (INT_X1 - 20.0, INT_X1, -16.0, 8.0)   # x0, x1, y0, y1 (interno)


def guscio(ds):
    est = forma_d(EST_X0, EST_X1, EST_Y0, EST_Y1, P.RAGGIO_FRONTE, P.RAGGIO_RETRO)
    inn = forma_d(INT_X0, INT_X1, INT_Y0, INT_Y1, P.RAGGIO_FRONTE - P.PARETE, P.RAGGIO_RETRO - P.PARETE_RETRO)
    g = extrude(est, ALTEZZA_BASE) - extrude(inn, Z_CIELO_INT)

    # Apertura USB-C sul retro (sovrastampo della spina)
    aw, ah, ar = P.APERTURA_USB
    ap = Pos(USB_X, INT_Y1 - 1.0, USB_Z) * extrude(
        RectangleRounded(aw, ah, ar).rotate(Axis.X, 90), P.PARETE_RETRO + 2.0, dir=(0, 1, 0))
    g -= ap

    # Colonnine pendenti per le viti M2 della scheda (vite dal basso)
    for (u, v) in P.FORI_M2_UV:
        x, y = da_scheda(u, v)
        g += cilindro(x, y, Z_SCHEDA_SU, Z_CIELO_INT, 5.5)
        g -= cilindro(x, y, Z_SCHEDA_SU - 0.1, Z_SCHEDA_SU + 10.0, 1.7)

    # Passaggio del cavetto display verso le gambe (sopra J2)
    cw, cd = P.CANALE_CAVO
    g -= Pos(0, 0, Z_CIELO_INT - 0.1) * extrude(RectangleRounded(cw, cd, 2.0), P.CIELO + 0.2)

    # Fori per le viti del corpo (M3 dal basso negli inserti delle gambe)
    for (x, y) in P.VITI_CORPO_XY:
        g -= cilindro(x, y, Z_CIELO_INT - 0.1, ALTEZZA_BASE + 0.1, 3.4)

    # Rinforzi per le viti del fondo (M2,5 autofilettanti)
    for (x, y) in P.VITI_FONDO_XY:
        g += cilindro(x, y, P.FONDO + P.GIOCO, Z_CIELO_INT, 7.0)
        g -= cilindro(x, y, P.FONDO, P.FONDO + 10.0, 2.2)

    # Culla del DS3231: due guide con labbro sotto i bordi lunghi del PCB
    x0, x1, y0, y1, z0, z1 = ds
    zpcb = z1 - P.DS3231_SOPRA - P.DS3231_PCB
    for (a, b, la, lb) in ((x0 - 1.2, x0, x0, x0 + 1.0), (x1, x1 + 1.2, x1 - 1.0, x1)):
        g += scatola(a, b, y0, y1, zpcb - 1.2, Z_CIELO_INT)
        g += scatola(la, lb, y0 + 3.0, y1, zpcb - 1.2, zpcb)

    # Camera SHT40: pareti divisorie e feritoie
    cx0, cx1, cy0, cy1 = CAMERA_SHT40
    t = 1.5
    g += scatola(cx0 - t, cx0, cy0 - t, cy1 + t, P.FONDO + P.GIOCO, Z_CIELO_INT)
    g += scatola(cx0, cx1, cy0 - t, cy0, P.FONDO + P.GIOCO, Z_CIELO_INT)
    g += scatola(cx0, cx1, cy1, cy1 + t, P.FONDO + P.GIOCO, Z_CIELO_INT)
    g -= scatola(cx0 - t - 0.1, cx0 + 0.1, -7.0, -1.0, 15.0, 19.0)      # passaggio cavo
    for i in range(6):
        y = cy0 + 3.0 + i * 3.4
        g -= scatola(INT_X1 - 0.5, EST_X1 + 0.5, y, y + 1.6, 5.0, Z_CIELO_INT - 2.0)

    # Sedi delle linguette posteriori del fondo
    for xl in (-28.0, 22.0):
        g -= scatola(xl, xl + 8.0, INT_Y1 - 0.1, INT_Y1 + 1.0, 0.8, P.FONDO + 0.2)
    return g


# --------------------------------------------------------------------------
# Fondo apribile (sportello) con vasca della zavorra
# --------------------------------------------------------------------------
def zona_zavorra():
    """Striscia anteriore, oltre 15 mm dall'antenna e fuori dalla camera SHT40."""
    inn = forma_d(INT_X0, INT_X1, INT_Y0, INT_Y1, P.RAGGIO_FRONTE - P.PARETE, P.RAGGIO_RETRO - P.PARETE_RETRO)
    ys = CAMERA_SHT40[2] - 1.5 - 1.0
    z = extrude(inn, Z_CIELO_INT) & scatola(INT_X0 + 0.5, INT_X1 - 0.5, INT_Y0 + 0.5, ys,
                                             P.FONDO, Z_CIELO_INT - 1.5)
    for (x, y) in P.VITI_FONDO_XY:
        z -= cilindro(x, y, 0, Z_CIELO_INT, 9.0)
    return z


def fondo():
    inn = forma_d(INT_X0 + P.GIOCO, INT_X1 - P.GIOCO, INT_Y0 + P.GIOCO, INT_Y1 - P.GIOCO,
                  P.RAGGIO_FRONTE - P.PARETE - P.GIOCO, max(0.5, P.RAGGIO_RETRO - P.PARETE_RETRO - P.GIOCO))
    f = extrude(inn, P.FONDO)
    # Vasca della zavorra (pareti 1,2 mm, chiusa con coperchio o resina)
    zz = zona_zavorra()
    bb = zz.bounding_box()
    vasca = scatola(bb.min.X - 1.2, bb.max.X + 1.2, bb.min.Y - 1.2, bb.max.Y + 1.2, P.FONDO, bb.max.Z)
    vasca &= extrude(inn, Z_CIELO_INT)
    for (x, y) in P.VITI_FONDO_XY:
        vasca -= cilindro(x, y, 0, Z_CIELO_INT, 7.6)
    f += vasca - zz
    # Viti del fondo: fori passanti svasati
    for (x, y) in P.VITI_FONDO_XY:
        f -= cilindro(x, y, -0.1, P.FONDO + 0.1, 2.8)
        f -= cilindro(x, y, -0.1, 1.5, 5.2)
    # Colonnine di appoggio del bordo anteriore della scheda
    for (u, v) in ((1.5, P.SCHEDA_P - 1.5), (P.SCHEDA_L - 1.5, P.SCHEDA_P - 1.5)):
        x, y = da_scheda(u, v)
        f += cilindro(x, y, P.FONDO, Z_SCHEDA - 0.2, 4.0)
    # Feritoie sotto la camera SHT40
    cx0, cx1, cy0, cy1 = CAMERA_SHT40
    for i in range(4):
        x = cx0 + 3.0 + i * 4.0
        f -= scatola(x, x + 1.6, cy0 + 2.0, cy1 - 2.0, -0.1, P.FONDO + 0.1)
    # Linguette posteriori
    for xl in (-28.0, 22.0):
        f += scatola(xl + 0.3, xl + 7.7, INT_Y1 - P.GIOCO - 0.1, INT_Y1 + 0.7, 1.0, P.FONDO)
    return f, zz


# --------------------------------------------------------------------------
# Controlli
# --------------------------------------------------------------------------
def antenna():
    x0, y0 = da_scheda(P.ANTENNA_U[0], P.ANTENNA_V[0])
    x1, y1 = da_scheda(P.ANTENNA_U[1], P.ANTENNA_V[1])
    return scatola(x0, x1, y0, y1, Z_SCHEDA_SU, Z_SCHEDA + 4.79)


def metalli(zz):
    m = {"zavorra": zz}
    for i, (u, v) in enumerate(P.FORI_M2_UV, 1):
        x, y = da_scheda(u, v)
        m[f"vite M2 H{i}"] = cilindro(x, y, Z_SCHEDA - 1.6, Z_SCHEDA_SU + 8.0, 3.8)
    for i, (x, y) in enumerate(P.VITI_CORPO_XY, 1):
        m[f"vite M3 corpo {i}"] = cilindro(x, y, Z_CIELO_INT - 3.0, ALTEZZA_BASE + 8.0, 5.5)
    for i, (x, y) in enumerate(P.VITI_FONDO_XY, 1):
        m[f"vite M2,5 fondo {i}"] = cilindro(x, y, 0, P.FONDO + 10.0, 4.7)
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--senza-export", action="store_true")
    ap.add_argument("--viewer", action="store_true")
    args = ap.parse_args()

    ing, ds = ingombri()
    g = guscio(ds)
    f, zz = fondo()

    righe = []
    w = righe.append
    w("STUDIO VOLUMETRICO DELLA BASE - PoliClock (OPEN-028, DEC-048)")
    w("Generato da mechanical/cad/studio_base.py; quote in mm. Riferimento: X destra, Y retro, Z alto,")
    w("origine sull'asse del connettore display J2 (asse del corpo), tavolo a Z = 0.")
    w("")
    w("== Quote della base ==")
    w(f"Esterno: {EST_X1 - EST_X0:.1f} (largh.) x {EST_Y1 - EST_Y0:.1f} (prof.) x {ALTEZZA_BASE:.1f} (alt.)")
    w(f"  X da {EST_X0:.1f} a {EST_X1:.1f}; Y da {EST_Y0:.1f} a {EST_Y1:.1f}")
    w(f"Interno: {INT_X1 - INT_X0:.1f} x {INT_Y1 - INT_Y0:.1f}, altezza utile {Z_CIELO_INT - P.FONDO:.1f}")
    w(f"Scheda: X da {SX:.1f} a {DX:.1f}, Y da {FR:.1f} a {RE:.1f}, lato inferiore a Z {Z_SCHEDA:.1f}, componenti a Z {Z_SCHEDA_SU:.1f}")
    w(f"Asse USB-C: X {USB_X:.2f}, Z {USB_Z:.2f} dal tavolo; apertura {P.APERTURA_USB[0]} x {P.APERTURA_USB[1]} mm")
    min_l = P.SCHEDA_L + 2 * (P.GIOCO_SCHEDA + P.PARETE)
    min_p = P.SCHEDA_P + 0.7 + P.PARETE_RETRO + P.GIOCO_SCHEDA + P.PARETE
    min_h = P.FONDO + P.LUCE_SOTTO_SCHEDA + P.SCHEDA_SPESSORE + 7.6 - 1.51 + 1.0 + P.CIELO
    w(f"Minimo teorico della sola scheda (senza moduli, zavorra, piedi, cavi PH dritti): "
      f"{min_l:.1f} x {min_p:.1f} x {min_h:.1f}")
    w("")
    w("== Volumi ==")
    vz = volume_cm3(zz)
    w(f"Vasca zavorra: {vz:.1f} cm3 -> acciaio pieno {vz * P.DENS_ACCIAIO:.0f} g, "
      f"pallini d'acciaio {vz * P.DENS_PALLINI:.0f} g")
    w(f"Guscio: {volume_cm3(g):.1f} cm3; fondo: {volume_cm3(f):.1f} cm3 (PLA ~1,24 g/cm3 pieno: "
      f"{(volume_cm3(g) + volume_cm3(f)) * 1.24:.0f} g)")
    w("")
    w("== Interferenze (volume in mm3, atteso 0) ==")
    stampati = {"guscio": g, "fondo": f}
    peggiore = 0.0
    for sn, s in stampati.items():
        for n, o in ing.items():
            if n.startswith("spina USB-C (sovrastampo)") and sn == "guscio":
                continue  # entra apposta nell'apertura: controllo separato sotto
            v = interseca(s, o)
            peggiore = max(peggiore, v)
            if v > 0.01:
                w(f"  ATTENZIONE {sn} / {n}: {v:.2f}")
    vsp = interseca(g, ing["spina USB-C (sovrastampo)"])
    w(f"  guscio / sovrastampo spina USB-C: {vsp:.2f} (deve essere 0: entra nell'apertura)")
    peggiore = max(peggiore, vsp)
    w(f"  Esito: {'PASS' if peggiore <= 0.01 else 'FALLITO'} (massimo {peggiore:.2f})")
    w("")
    w(f"== Distanza del metallo dall'antenna (minimo {P.DISTANZA_METALLO_ANTENNA:.0f} mm) ==")
    ant = antenna()
    ok = True
    for n, m in metalli(zz).items():
        d = ant.distance_to(m)
        ok &= d >= P.DISTANZA_METALLO_ANTENNA
        w(f"  {n:22s} {d:6.1f} mm {'ok' if d >= P.DISTANZA_METALLO_ANTENNA else 'TROPPO VICINO'}")
    for n in ("DS3231 pila CR1220", "spina Dupont display", "spina USB-C (guscio)"):
        d = ant.distance_to(ing[n])
        w(f"  {n:22s} {d:6.1f} mm (parte elettronica, informativo)")
    w(f"  Esito: {'PASS' if ok else 'FALLITO'}")
    w("")
    w("== Cavetto display ==")
    w(f"Spina Dupont con header diritto: da Z {Z_SCHEDA_SU + P.HEADER_DIRITTO_CORPO_H:.1f} "
      f"a Z {Z_SCHEDA_SU + P.HEADER_DIRITTO_CORPO_H + P.DUPONT_H:.1f}; piano superiore della base a Z {ALTEZZA_BASE:.1f}")
    w(f"Passaggio nel piano superiore e nelle gambe: {P.CANALE_CAVO[0]} x {P.CANALE_CAVO[1]} mm, centrato su X 0, Y 0")
    w(f"Con header a 90°: piedini fino a Y {FR - P.HEADER_90_SPORGENZA:.1f}, spina fino a Y "
      f"{FR - P.HEADER_90_SPORGENZA - P.DUPONT_H:.1f}, piega dei fili ~5 mm: "
      f"servirebbero circa {P.HEADER_90_SPORGENZA + P.DUPONT_H + 5:.0f} mm di base in più davanti alla scheda")
    w("")
    w("== Posizioni ==")
    for n in ("DS3231 (5188)", "DS3231 pila CR1220", "SHT40 modulo"):
        b = ing[n].bounding_box()
        w(f"  {n}: X {b.min.X:.1f}..{b.max.X:.1f}, Y {b.min.Y:.1f}..{b.max.Y:.1f}, Z {b.min.Z:.1f}..{b.max.Z:.1f}")
    w(f"  Camera SHT40 (interno): X {CAMERA_SHT40[0]:.1f}..{CAMERA_SHT40[1]:.1f}, Y {CAMERA_SHT40[2]:.1f}..{CAMERA_SHT40[3]:.1f}")
    bz = zz.bounding_box()
    w(f"  Zavorra: X {bz.min.X:.1f}..{bz.max.X:.1f}, Y {bz.min.Y:.1f}..{bz.max.Y:.1f}, Z {bz.min.Z:.1f}..{bz.max.Z:.1f}")
    for (u, v), i in zip(P.FORI_M2_UV, (1, 2)):
        x, y = da_scheda(u, v)
        w(f"  Foro M2 H{i}: X {x:.2f}, Y {y:.2f}")
    testo = "\n".join(righe) + "\n"
    print(testo)

    if not args.senza_export:
        os.makedirs(DIR_PRINTS, exist_ok=True)
        os.makedirs(DIR_OUT, exist_ok=True)
        with open(RAPPORTO, "w", encoding="utf-8") as fh:
            fh.write(testo)
        export_stl(g, os.path.join(DIR_PRINTS, "base-guscio.stl"), tolerance=0.02, angular_tolerance=0.2)
        export_stl(f, os.path.join(DIR_PRINTS, "base-fondo.stl"), tolerance=0.02, angular_tolerance=0.2)
        parti = []
        for n, o in list(ing.items()) + [("zavorra", zz)]:
            o.label = n
            parti.append(o)
        g.label, f.label = "base guscio", "base fondo"
        ass = Compound(children=[g, f] + parti, label="studio volumi base")
        export_step(ass, os.path.join(DIR_PRINTS, "studio-volumi-base.step"))
        # Ingombri per Blender (vista in sezione), non versionati
        for n, o in list(ing.items()) + [("zavorra", zz)]:
            nome = n.replace(" ", "_").replace("(", "").replace(")", "").replace(",", "")
            export_stl(o, os.path.join(DIR_OUT, f"ingombro_{nome}.stl"), tolerance=0.05)
        print("Esportati: mechanical/prints/base-guscio.stl, base-fondo.stl, studio-volumi-base.step")

    if args.viewer:
        from ocp_vscode import show
        show(g, f, *ing.values(), zz, names=["guscio", "fondo", *ing.keys(), "zavorra"])


if __name__ == "__main__":
    main()
