"""Parametri condivisi dello studio volumetrico di PoliClock (OPEN-028).

Tutte le quote sono in millimetri. Ogni valore indica la fonte:
- "STEP" = misurato il 2026-11-09 sullo STEP completo esportato da KiCad
  (`kicad-cli pcb export step --subst-models`) della scheda rev 0.2;
- "PCB"  = coordinate delle impronte in `policlock-main.kicad_pcb`;
- "DOC"  = documentazione del progetto (docs/02, docs/06, docs/12);
- "WEB"  = pagina del produttore citata;
- "SEGNAPOSTO" = valore provvisorio, da misurare sul pezzo reale (TBD);
- "SCELTA" = proposta dello studio, modificabile (non decisione del proprietario).

Sistema di riferimento della statuetta:
  X verso destra guardando la statuetta da davanti,
  Y verso il retro (la USB-C esce verso +Y),
  Z verso l'alto, piano del tavolo a Z = 0.
  Origine in pianta = asse del connettore display J2 (centro dei 7 pin),
  che coincide con l'asse verticale delle gambe e del corpo.

Coordinate locali della scheda (u, v): u dal bordo sinistro, v dal bordo
inferiore (quello della USB-C), vista lato componenti, come in docs/06 §3.
La scheda è ruotata di 180° attorno a Z: il bordo USB va verso il retro,
il bordo dell'header J2 verso il fronte, l'antenna verso -X (sinistra).
"""

# --------------------------------------------------------------------------
# Scheda principale rev 0.2 (DEC-045)
# --------------------------------------------------------------------------
SCHEDA_L = 50.5          # u, DOC/STEP
SCHEDA_P = 41.5          # v, DOC/STEP
SCHEDA_SPESSORE = 1.6    # nominale DOC (lo STEP riporta 1,51)

# J2 è un header 1x8 dal DEC-049 (hardware): pin 1 a u 7,34, pin 8 (BUSY) a
# u 25,12; fila a y = 102,9 nel foglio KiCad (PCB: at 107.34 102.9), bordo
# inferiore a y = 140. Il cavetto Dupont del GC9A01 usa i pin 1-7: l'asse del
# corpo è il centro di questi 7 pin.
J2_PIN1_U = 7.34
J2_N_PIN = 8
J2_PIN_CAVO = 7
J2_U = J2_PIN1_U + (J2_PIN_CAVO - 1) * 2.54 / 2   # 14.96
J2_V = 140.0 - 102.9                              # 37.10

# Fori M2 (PCB: 124.16/143.66, 136.5) -> u = x - 100, v = 140 - y
FORI_M2_UV = [(24.16, 3.5), (43.66, 3.5)]
FORO_M2_D = 2.2

# Antenna del WROOM-02 (DOC docs/02 §3.2): corpo del modulo da x 27,51 a
# 47,51 e da y 1,5 a 19,5 (origine vecchio angolo in alto a sinistra);
# antenna da x 41,51 al bordo del modulo. In coordinate scheda:
ANTENNA_U = (41.51, 47.51)
ANTENNA_V = (40.0 - 19.5, 40.0 - 1.5)   # (20.5, 38.5)
DISTANZA_METALLO_ANTENNA = 15.0         # DOC: Espressif, per una futura radio

# Quota del lato inferiore della scheda sopra il fondo (luce per i piedini
# a foro passante di J2-J5 e per le teste delle viti M2)
LUCE_SOTTO_SCHEDA = 3.5   # SCELTA: piedini fino a 1,81 mm (STEP) + margine

# Ingombri dei componenti sopra la scheda (u0, u1, v0, v1, z0, z1),
# z misurato dal lato inferiore della scheda (STEP: scheda da 0 a 1,51).
# Solo i componenti che contano per l'ingombro; i passivi 0603 sono alti
# meno di 1 mm e stanno sotto il modulo.
COMPONENTI = {
    # nome: (u0, u1, v0, v1, z0, z1)        fonte
    "U3 WROOM-02": (27.51, 47.51, 20.5, 38.5, 1.56, 4.79),   # STEP
    "J3 SHT40":    (1.05, 10.95, 28.2, 32.75, -1.81, 7.60),  # STEP (PH, con piedini sotto)
    "J4 RTC":      (1.05, 10.95, 22.2, 26.75, -1.81, 7.60),  # STEP
    "J5 pulsante": (1.05, 10.95, 16.2, 20.75, -1.81, 7.60),  # STEP
    # USB-C HRO TYPE-C-31-M-12: modello 3D assente in KiCad 10, quote del
    # disegno HRO (guscio 8,94 x 7,35 x 3,16), 0,4 mm oltre il bordo (DOC)
    "J1 USB-C":    (33.66 - 4.47, 33.66 + 4.47, -0.4, 6.95, 1.51, 4.67),
    "U2 LDO":      (15.6, 18.4, 5.05, 7.95, 1.59, 3.15),     # STEP
    "U1 ESD":      (32.21, 35.11, 12.22, 15.03, 1.59, 3.15), # STEP
}
# Asse della USB-C (centro dell'apertura del guscio)
USB_U = 33.66
USB_Z_SU_SCHEDA = 1.51 + 3.16 / 2   # dal lato inferiore della scheda

# --------------------------------------------------------------------------
# Header J2 e cavetto del display (DEC-043, OPEN-021)
# --------------------------------------------------------------------------
# Variante consigliata dallo studio: header DIRITTO negli stessi fori.
HEADER_DIRITTO_CORPO_H = 2.5     # corpo plastico sopra la scheda (generico)
HEADER_DIRITTO_PIN_H = 6.0       # piedini sopra il corpo (generico 2,54 mm)
DUPONT_7_L = 7 * 2.54            # 17,78 (DOC: circa 18 x 2,5 mm)
DUPONT_S = 2.54
DUPONT_H = 14.0                  # alloggiamento femmina standard
# Variante a 90° (montata nel progetto KiCad): piedini 5,64 mm oltre il
# bordo (STEP: fino a y 92,86 contro bordo 98,5), poi la spina in orizzontale
HEADER_90_SPORGENZA = 5.64
# Sezione minima del passaggio del cavetto (la spina deve poterlo
# attraversare, se il corpo non è diviso in due gusci)
CANALE_CAVO = (21.0, 6.0)        # SCELTA: spina 17,8 x 2,5 + gioco

# --------------------------------------------------------------------------
# Moduli esterni
# --------------------------------------------------------------------------
# Adafruit DS3231 Precision RTC STEMMA QT (5188): 25,4 x 17,8 x 7,8 mm,
# pila CR1220 sul retro (WEB adafruit.com/product/5188, letta il 2026-11-09)
DS3231 = (25.4, 17.8, 7.8)
DS3231_PCB = 1.6
DS3231_SOPRA = 3.0       # SEGNAPOSTO: componenti e STEMMA QT sopra il PCB
DS3231_PILA = 15.0       # SEGNAPOSTO: larghezza del portapila CR1220 sul retro
# SHT40 breakout generico "nero, con pin" (DEC-028): quote SEGNAPOSTO
SHT40 = (14.0, 11.0, 1.6)
DUPONT_4_L = 4 * 2.54
# Modulo display GC9A01 1,28" a 7 pin (DEC-034): SEGNAPOSTO, OPEN-016.
# Inserzioni simili riportano PCB 38 x 45,5 mm o 37,5 x 45 x 3,2 mm;
# area attiva Ø 32,4 mm (Waveshare 1,28").
DISPLAY_PCB = (38.0, 45.5)
DISPLAY_SPESSORE = 3.2 + 1.6     # vetro e cornice + PCB, SEGNAPOSTO
DISPLAY_ATTIVO_D = 32.4
DISPLAY_TONDO_D = 37.5
DISPLAY_ALETTA_L = 26.0          # larghezza dell'aletta dei pin sotto il tondo, SEGNAPOSTO
                                 # (7 pin = 17,8 mm più i margini del PCB)

# Spina USB-C del cavo (generica): guscio 8,4 x 2,6; sovrastampaggio
# fino a circa 12,4 x 6,5 (SEGNAPOSTO, dipende dal cavo)
SPINA_USB_SOVRASTAMPO = (12.4, 6.5, 24.0)
APERTURA_USB = (13.4, 7.6, 1.5)  # SCELTA: larghezza, altezza, raggio raccordo

# Spina JST PH accoppiata: altezza sopra la scheda con il cavo che esce
# dall'alto e piega a 90° (SEGNAPOSTO, prova 1:1 FIN-011)
PH_CAVO_SOPRA_SCHEDA = 14.0

# --------------------------------------------------------------------------
# Base (guscio + fondo apribile)
# --------------------------------------------------------------------------
PARETE = 2.0          # SCELTA: pareti laterali
PARETE_RETRO = 2.0    # SCELTA: parete della USB
CIELO = 2.5           # SCELTA: spessore del piano superiore
FONDO = 2.5           # SCELTA: spessore del fondo apribile (sportello)
GIOCO = 0.3           # SCELTA: gioco fra fondo e guscio (da tarare in stampa)
GIOCO_SCHEDA = 1.5    # SCELTA: gioco attorno alla scheda (lato antenna)
RAGGIO_RETRO = 5.0    # SCELTA: spigoli posteriori (retro piatto per la USB)
RAGGIO_FRONTE = 18.0  # SCELTA: spigoli anteriori
# Zona dei piedi davanti all'asse del corpo (piedi e zavorra anteriore)
PROFONDITA_FRONTE = 36.5   # SCELTA: dal piano Y = 0 alla faccia anteriore
LARGHEZZA_DESTRA = 22.5    # SCELTA: dal bordo destro della scheda alla parete interna

# Viti del corpo sulla base (M3 dal basso negli inserti delle gambe)
VITI_CORPO_XY = [(-10.0, -12.0), (10.0, -12.0)]   # negli stivali
# Viti del fondo (M2,5 nei rinforzi anteriori) + 2 linguette posteriori
VITI_FONDO_XY = [(-24.0, -26.0), (28.0, -24.0)]

# Zavorra: densità per il calcolo della massa
DENS_ACCIAIO = 7.85     # g/cm³, rondelle o piastrine
DENS_PALLINI = 4.6      # g/cm³ apparente, pallini d'acciaio sfusi (circa 60 %)
