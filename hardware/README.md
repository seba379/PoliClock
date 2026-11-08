# Hardware PoliClock (KiCad 10)

**Stato (rev 0.2, 2026-11-08):** schema e PCB della scheda principale **in bozza**, rifatti dopo la revisione tecnica indipendente (esito sulla rev 0.1: *NOT APPROVED FOR FABRICATION*; stato dei rilievi in [docs/10](../docs/10-decisioni-aperte.md) §6).

**Correzioni del 2026-11-08, ramo `codex/pcb-edge-courtyard-fixes`:** C7 spostato a 2,60 mm dal bordo; courtyard/F.Fab di J2–J5 completati; FID1 spostato di 1,5 mm con la sua zona di rispetto. Commit autorizzato dal proprietario; ERC/DRC e confronto riportati nella [nota delle modifiche](../docs/revisioni/2026-11-08/correzioni/README.md). Vista 2D dei courtyard: [pcb-courtyard.svg](../docs/revisioni/2026-11-08/correzioni/pcb-courtyard.svg).

**Chiusura dei rilievi residui (2026-11-08, [verifica](../docs/revisioni/2026-11-08/verifica-claude.md)):**

- C1 portato a **1 µF** (C15849) e C2 a **4,7 µF** (C19666, Basic): restano 5,7 µF nominali su VBUS (`DEC-042`).
- Cartigli portati a rev 0.2 e annotazioni dello schema corrette.
- `esporta.py` ora si ferma se ERC, DRC o il controllo meccanico falliscono.
- PDF, BOM, layout e render 3D sono rigenerati.

**Contorno rettangolare 50,5 × 41,5 mm (`DEC-045`, 2026-11-08):** niente intaglio, antenna di U3 sulla scheda con zona vietata, corpo di tutte le parti montate da JLC a ≥ 2,5 mm da ogni bordo tranne J1 (unica eccezione DFM). Modifica con `scripts/dec045_pcb.py`. ERC 0, DRC 0/0/0, controllo meccanico PASS (margine minimo 2,99 mm). Dettagli in [docs/10](../docs/10-decisioni-aperte.md) §12.

**Modulo ESP32-C3-WROOM-02-N4 (`DEC-044`, 2026-11-08):** sostituisce il MINI-1-H4X (a JLC solo "Standard"). Impronta di progetto `PoliClock:ESP32-C3-WROOM-02` (derivata da quella di KiCad, 4 vie termiche 0,3/0,7 mm, niente serigrafia sopra l'antenna), intaglio allargato a 8,5 × 20,2 mm, coppia USB ridisegnata sui pin 13/14, sbroglio rifatto, cucitura GND, R16 10 k + C11 10 nF (FIN-003), serigrafia a 1,0 mm (FIN-005), regola PTH in `.kicad_dru` (FIN-007), script Gerber bloccato (FIN-006). ERC 0, DRC 0/0/0 con parità, controllo meccanico PASS. Dettagli in [docs/10](../docs/10-decisioni-aperte.md) §11.

**Connettori a foro passante (`DEC-043`, 2026-11-08):** J2 (header 1×7 2,54 mm) e J3/J4/J5 (JST PH B4B-PH-K-S) sono a foro passante e **saldati a mano dal proprietario**; JLC monta tutto il resto, J1 compreso. Le impronte vengono dalla libreria standard di KiCad 10. J2–J5 hanno il campo `Montaggio` = "a mano, parte del proprietario" e l'attributo "escluso dai file di posizionamento": non compaiono in BOM JLC e CPL, ma sono nella BOM completa. Modifica con `scripts/dec043_connettori_tht.py`, poi sbroglio delle sole connessioni mancanti con `scripts/sbroglia_main.py --conserva`. ERC 0, DRC 0/0/0 con parità, controllo meccanico PASS. Dettagli in [docs/10](../docs/10-decisioni-aperte.md) §10.

- **Report salvati**: ERC e DRC rieseguiti con `kicad-cli` sulla rev 0.2 (`policlock-main/erc.rpt`, `drc.rpt`). Sono verifiche automatiche del progetto.
- **Test eseguiti sull'hardware**: nessuno. Tutti i test del [piano di verifica](../docs/07-piano-verifica.md) sono NOT_RUN.
- **Non ordinare**: prima servono studio volumetrico 1:1 (`OPEN-028`), verifica del modulo display ricevuto (`OPEN-016`), prototipo M1 e DFM JLC. La revisione visiva del proprietario in KiCad è stata fatta il 2026-11-08 con esito positivo (`OPEN-027` chiusa).

## Struttura

| Cartella | Contenuto |
|---|---|
| `policlock-main/` | Scheda principale: schema gerarchico (USB e alimentazione, MCU, display a 7 pin, periferiche I²C e pulsante), PCB 50,5 × 41,5 mm, PDF, BOM e CPL per JLCPCB, render, STEP della sagoma, report ERC/DRC |
| `lib/` | Libreria di progetto `PoliClock` (simboli e footprint delle parti specifiche) |
| `scripts/` | Generatori di schema e PCB, sbroglio con Freerouting, esportazioni |

È l'**unico PCB custom**: display, sensore SHT40 e RTC sono moduli commerciali collegati con cavetti (`DEC-024`, `DEC-028`, `DEC-034`).

Ogni componente montato da JLC ha il campo **`LCSC`** (codice JLCPCB/LCSC); J2–J5 non hanno codice LCSC e portano il campo **`Montaggio`** = "a mano, parte del proprietario" (`DEC-043`). Simboli e footprint di passivi, SOT, USBLC6, TLV75533 e AO3401A vengono dalle librerie standard di KiCad 10; la USB-C usa il footprint KiCad ricavato dal disegno HRO (copiato nella libreria di progetto con la serigrafia frontale tolta); anche i connettori a foro passante J2–J5 usano impronte standard (`Connector_PinHeader_2.54mm`, `Connector_JST`); le altre parti vengono dalla libreria `PoliClock`.

## PCB della scheda principale

- `policlock-main/policlock-main.kicad_pcb`: **50,5 × 41,5 mm, 2 strati, 1,6 mm, componenti solo sopra** (`DEC-030`, `DEC-045`). L'antenna del modulo ESP32 sta sulla scheda, verso il bordo destro, sopra una zona vietata senza rame su entrambi gli strati (niente intaglio). Piani GND su entrambi gli strati. Nessun tasto: reset e boot dai punti di test TP6 (EN) e TP11 (IO9) sul retro (`DEC-039`). Tre fiducial da 1 mm sul lato componenti. Dettagli in [docs/02](../docs/02-architettura-hardware.md) §3.2.
- **Regole JLCPCB** (vincolo `SC-008`, `DEC-040`; pagine ufficiali consultate il 2026-11-08, da ricontrollare all'ordine):
  - fabbricazione 2 strati: distanza 0,15 mm, pista ≥ 0,15 mm (alimentazioni 0,3–0,4 mm), anello delle piazzole PTH ≥ 0,18 mm (regola `.kicad_dru`), testi della serigrafia ≥ 1,0 mm, vie 0,6/0,3 mm, foro-foro ≥ 0,25 mm (JLC 0,2), foro-rame ≥ 0,3 mm (JLC 0,28), rame-bordo 0,3 mm (JLC 0,2) più una fascia di 0,45 mm senza piste lungo il contorno;
  - assemblaggio: corpo dei componenti montati da JLC ≥ 2,5 mm da ogni bordo; controllo aggiuntivo `scripts/verifica_meccanica_pcb.py`, richiamato anche dal generatore. **Unica eccezione J1** (USB-C a filo del bordo inferiore), da approvare al DFM JLC (`DEC-045`). Le parti saldate a mano (J2–J5, `DEC-043`) non hanno il margine, ma il loro courtyard è controllato; le regole di fabbricazione valgono anche per le loro piazzole. Fiducial con zona senza rame.
  - `policlock-main/policlock-main.kicad_dru`: anello PTH ≥ 0,18 mm (FIN-007) e una deroga che ignora il controllo serigrafia-bordo **solo per J2** (la serigrafia della libreria segue i piedini oltre il bordo e non viene stampata).
- Controlli DRC **riabilitati**: courtyard mancante o sovrapposto, fori nei courtyard, footprint diversi dalla libreria, serigrafia sovrapposta o fuori bordo.
- File esportati: `policlock-main-top.png` / `-bottom.png` (render), `policlock-main-layout.pdf` (assemblaggio F.Fab, rame, legenda del retro), `policlock-main-scheda.step` (sagoma con fori, per il CAD), `policlock-main-bom-jlcpcb.csv` e `policlock-main-cpl-jlcpcb.csv` (assemblaggio JLC, origine nell'angolo in basso a sinistra, senza le parti saldate a mano), `policlock-main-bom-completa.csv` (tutte le parti, con la colonna `Montaggio`: "JLC (PCBA)" oppure "a mano, parte del proprietario"). Lo STEP completo con i componenti (`policlock-main.step`) usa i modelli 3D EasyEDA e resta **solo locale** (ignorato da git).
- I file Gerber e di foratura **non** sono generati: si producono solo dopo l'approvazione esplicita del proprietario.

## Rigenerare / verificare

```bash
python hardware/scripts/esporta.py
```

Esegue ERC (`--severity-all`), DRC (`--schematic-parity --refill-zones --all-track-errors`) e il controllo meccanico `verifica_meccanica_pcb.py`, poi PDF, BOM, CPL, render e STEP con `kicad-cli` (percorso modificabile con le variabili `KICAD_CLI` e `KICAD_PYTHON`). **Se ERC, DRC o controllo meccanico falliscono, lo script si ferma con codice d'uscita diverso da zero e non esporta i file del PCB** (rilievo REV-004). Si ferma anche se una parte della BOM JLC non ha codice LCSC né campo `Montaggio`, o se BOM JLC e CPL non hanno gli stessi designatori (`DEC-043`). I render 3D richiedono i modelli locali in `lib/PoliClock.3dshapes/`.

Generatori (per i PCB serve il Python di KiCad, `"C:/Program Files/KiCad/10.0/bin/python.exe"`):

1. `scripts/genera_schemi.py` — schema (Python normale).
2. `scripts/genera_pcb_main.py` — posizionamento, contorno, fori, piani GND, zona antenna, legenda, campi e percorsi dei simboli dallo schema (confronto schema ↔ PCB pulito); **coppia USB D+/D- tracciata a mano** da `scripts/usb_coppia.py` con piste bloccate (`DEC-041`); posizioni in `scripts/posizioni_main.py` (dimensioni con la variabile `PCB_WH`, default `50,40`).
3. `scripts/sbroglia_main.py` — sbroglio con **Freerouting 2.5.0** (regole JLC passate nel file DSN) (jar ufficiale, SHA-256 verificato) e Java 25 portatile (Eclipse Temurin) in `%LOCALAPPDATA%\Programs\freerouting-2.5.0`, non nel repository. Va lanciato **subito dopo il punto 2**, su una scheda appena generata (su una scheda già sbrogliata fallisce). La build nativa `freerouting-cli` 2.5.0 per Windows si blocca nel router; KiCad non ha un autorouter.

Dopo la prima modifica manuale in KiCad **i file `.kicad_sch` e `.kicad_pcb` diventano la fonte**: non rieseguire i generatori, che li sovrascriverebbero. I generatori descrivono la scheda prima di `DEC-043` (JST-SH e header SMD).

Modifiche successive sui file KiCad:

- `scripts/dec043_connettori_tht.py` — una tantum (`DEC-043`): impronte a foro passante J2–J5, spostamenti e rimozione delle piste toccate.
- `scripts/dec044_schema.py` e `scripts/dec044_pcb.py` — una tantum (`DEC-044`): simbolo e impronta del WROOM-02, C11/R16, intaglio, posizionamento, coppia USB; i ritocchi fatti a mano dopo lo sbroglio sono descritti nel docstring.
- `scripts/dec045_pcb.py` — una tantum (`DEC-045`): contorno rettangolare 50,5 × 41,5 mm, piani GND, J2 sul nuovo bordo superiore e rimozione delle piste delle sue reti (poi `sbroglia_main.py --conserva` e `cucitura_gnd.py`).
- `scripts/cucitura_gnd.py` — vie di cucitura GND lungo il contorno, fuori dalla zona vietata dell'antenna (FIN-008), rifatte da capo a ogni esecuzione.
- `scripts/esporta_gerber_jlc.py --conferma-proprietario` — Gerber e forature per JLC (FIN-006): **solo dopo l'approvazione esplicita del proprietario**; senza il flag non scrive nulla. Uscita in `policlock-main/gerber-jlc/` (ignorata da git).
- `scripts/sbroglia_main.py --conserva` — sbroglia solo le connessioni mancanti, lasciando ferme le piste esistenti (bloccate durante lo sbroglio, poi sbloccate tranne la coppia USB). Con `--blocca-da-x=127` restano ferme solo le piste della zona J1/U1/U3.

## Libreria `PoliClock`

Simboli `B4B-PH-K-S` e `PinHeader_1x07_P2.54_THT` (`DEC-043`): stessa geometria dei pin dei simboli JST-SH e Hanxia, con le impronte della libreria standard di KiCad. I simboli e le impronte JST-SH/Hanxia restano in libreria ma non sono più usati.

Parti importate da LCSC con [easyeda2kicad](https://github.com/uPesy/easyeda2kicad.py) (codici C2838502 per il footprint del modulo ESP32-C3-MINI-1, C160404, C160402, C720477, C46061680), corrette con `scripts/correggi_libreria.py` (tipi elettrici dei pin, campo `LCSC`, riferimenti) e aggiornate al formato KiCad 10 con `kicad-cli fp upgrade` / `kicad-cli sym upgrade`. `scripts/prepara_footprint.py` toglie la serigrafia che finirebbe fuori dal bordo (USB-C, antenna del modulo, piedini dell'header).

Confronto con i disegni ufficiali (revisione P1-08): piazzole JST-SH confrontate con la libreria KiCad; USB-C EasyEDA scartato a favore del footprint KiCad dal disegno HRO. Nelle correzioni del 2026-11-08 i courtyard/F.Fab JST sono stati completati usando la libreria KiCad e quelli dell'header usando il disegno Hanxia ora recuperato: dettagli e verifiche residue nella [nota](../docs/revisioni/2026-11-08/correzioni/README.md).

I **modelli 3D** EasyEDA non sono nel repository (licenza non verificata): si rigenerano con `easyeda2kicad --3d` e finiscono in `lib/PoliClock.3dshapes/` (ignorata da git).

Selezione e motivazioni dei componenti: [docs/12-selezione-componenti.md](../docs/12-selezione-componenti.md).
