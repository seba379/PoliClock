# Hardware PoliClock (KiCad 10)

**Stato (rev 0.2, 2026-11-08):** schema e PCB della scheda principale **in bozza**, rifatti dopo la revisione tecnica indipendente (esito sulla rev 0.1: *NOT APPROVED FOR FABRICATION*; stato dei rilievi in [docs/10](../docs/10-decisioni-aperte.md) §6).

- **Report salvati**: ERC e DRC rieseguiti con `kicad-cli` sulla rev 0.2 (`policlock-main/erc.rpt`, `drc.rpt`). Sono verifiche automatiche del progetto.
- **Test eseguiti sull'hardware**: nessuno. Tutti i test del [piano di verifica](../docs/07-piano-verifica.md) sono NOT_RUN.
- **Non ordinare**: prima servono studio volumetrico 1:1 (`OPEN-028`), verifica del modulo display ricevuto (`OPEN-016`), revisione visiva del proprietario in KiCad (`OPEN-027`) e prototipo M1.

## Struttura

| Cartella | Contenuto |
|---|---|
| `policlock-main/` | Scheda principale: schema gerarchico (USB e alimentazione, MCU, display a 7 pin, periferiche I²C e pulsante), PCB 50 × 40 mm, PDF, BOM e CPL per JLCPCB, render, STEP della sagoma, report ERC/DRC |
| `lib/` | Libreria di progetto `PoliClock` (simboli e footprint delle parti specifiche) |
| `scripts/` | Generatori di schema e PCB, sbroglio con Freerouting, esportazioni |

È l'**unico PCB custom**: display, sensore SHT40 e RTC sono moduli commerciali collegati con cavetti (`DEC-024`, `DEC-028`, `DEC-034`).

Ogni componente montato ha il campo **`LCSC`** (codice JLCPCB/LCSC). Simboli e footprint di passivi, SOT, USBLC6, TLV75533 e AO3401A vengono dalle librerie standard di KiCad 10; la USB-C usa il footprint KiCad ricavato dal disegno HRO (copiato nella libreria di progetto con la serigrafia frontale tolta); le altre parti vengono dalla libreria `PoliClock`.

## PCB della scheda principale

- `policlock-main/policlock-main.kicad_pcb`: **50 × 40 mm, 2 strati, 1,6 mm, componenti solo sopra** (`DEC-030`, `DEC-036`). L'antenna del modulo ESP32 sta dentro l'ingombro, sopra un **intaglio** nell'angolo in alto a destra, con una zona senza rame davanti. Piani GND su entrambi gli strati. Nessun tasto: reset e boot dai punti di test TP6 (EN) e TP11 (IO9) sul retro (`DEC-039`). Tre fiducial da 1 mm sul lato componenti. Dettagli in [docs/02](../docs/02-architettura-hardware.md) §3.2.
- **Regole JLCPCB** (vincolo `SC-008`, `DEC-040`; pagine ufficiali consultate il 2026-11-08, da ricontrollare all'ordine):
  - fabbricazione 2 strati: distanza 0,15 mm (0,10 mm fra le piazzole USB-C a passo 0,5 mm), pista ≥ 0,15 mm (alimentazioni 0,4 mm), vie 0,6/0,3 mm, foro-foro ≥ 0,25 mm (JLC 0,2), foro-rame ≥ 0,3 mm (JLC 0,28), rame-bordo 0,3 mm (JLC 0,2) più una fascia di 0,45 mm senza piste lungo il contorno;
  - assemblaggio: corpo dei componenti ≥ 2,5 mm dai lati sinistro e destro (`genera_pcb_main.py` avvisa se non è così), connettori a filo solo sui lati superiore e inferiore, fiducial con zona senza rame.
- Controlli DRC **riabilitati**: courtyard mancante o sovrapposto, fori nei courtyard, footprint diversi dalla libreria, serigrafia sovrapposta o fuori bordo.
- File esportati: `policlock-main-top.png` / `-bottom.png` (render), `policlock-main-layout.pdf` (assemblaggio F.Fab, rame, legenda del retro), `policlock-main-scheda.step` (sagoma con fori, per il CAD), `policlock-main-bom-jlcpcb.csv` e `policlock-main-cpl-jlcpcb.csv` (assemblaggio JLC, origine nell'angolo in basso a sinistra). Lo STEP completo con i componenti (`policlock-main.step`) usa i modelli 3D EasyEDA e resta **solo locale** (ignorato da git).
- I file Gerber e di foratura **non** sono generati: si producono solo dopo l'approvazione esplicita del proprietario.

## Rigenerare / verificare

```bash
python hardware/scripts/esporta.py
```

Esegue ERC (`--severity-all`), DRC (con `--schematic-parity`), PDF, BOM, CPL, render e STEP con `kicad-cli` (percorso modificabile con la variabile `KICAD_CLI`).

Generatori (per i PCB serve il Python di KiCad, `"C:/Program Files/KiCad/10.0/bin/python.exe"`):

1. `scripts/genera_schemi.py` — schema (Python normale).
2. `scripts/genera_pcb_main.py` — posizionamento, contorno, fori, piani GND, zona antenna, legenda, campi e percorsi dei simboli dallo schema (confronto schema ↔ PCB pulito); **coppia USB D+/D- tracciata a mano** da `scripts/usb_coppia.py` con piste bloccate (`DEC-041`); posizioni in `scripts/posizioni_main.py` (dimensioni con la variabile `PCB_WH`, default `50,40`).
3. `scripts/sbroglia_main.py` — sbroglio con **Freerouting 2.5.0** (regole JLC passate nel file DSN) (jar ufficiale, SHA-256 verificato) e Java 25 portatile (Eclipse Temurin) in `%LOCALAPPDATA%\Programs\freerouting-2.5.0`, non nel repository. Va lanciato **subito dopo il punto 2**, su una scheda appena generata (su una scheda già sbrogliata fallisce). La build nativa `freerouting-cli` 2.5.0 per Windows si blocca nel router; KiCad non ha un autorouter.

Dopo la prima modifica manuale in KiCad **i file `.kicad_sch` e `.kicad_pcb` diventano la fonte**: non rieseguire i generatori, che li sovrascriverebbero.

## Libreria `PoliClock`

Parti importate da LCSC con [easyeda2kicad](https://github.com/uPesy/easyeda2kicad.py) (codici C2838502 per il footprint del modulo ESP32-C3-MINI-1, C160404, C160402, C720477, C46061680), corrette con `scripts/correggi_libreria.py` (tipi elettrici dei pin, campo `LCSC`, riferimenti) e aggiornate al formato KiCad 10 con `kicad-cli fp upgrade` / `kicad-cli sym upgrade`. `scripts/prepara_footprint.py` toglie la serigrafia che finirebbe fuori dal bordo (USB-C, antenna del modulo, piedini dell'header).

Confronto con i disegni ufficiali (revisione P1-08): JST-SH identici alla libreria KiCad; USB-C EasyEDA scartato a favore del footprint KiCad dal disegno HRO; header 7 pin SMD senza disegno ufficiale trovato (da verificare sul campione).

I **modelli 3D** EasyEDA non sono nel repository (licenza non verificata): si rigenerano con `easyeda2kicad --3d` e finiscono in `lib/PoliClock.3dshapes/` (ignorata da git).

Selezione e motivazioni dei componenti: [docs/12-selezione-componenti.md](../docs/12-selezione-componenti.md).
