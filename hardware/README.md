# Hardware PoliClock (KiCad 10)

**Stato:** schema rev 0.1 (M2, solo schematico). **Non validato**: prima dell'ordine servono prototipo M1, layout, DRC, checklist e revisione visiva del proprietario in KiCad (`VT-PCB-001`). Il layout PCB non è ancora iniziato.

## Struttura

| Cartella | Contenuto |
|---|---|
| `policlock-main/` | Scheda principale: schema gerarchico (USB e alimentazione, MCU, display/cavo FFC, periferiche I²C e pulsante), PDF, BOM, report ERC |
| `policlock-display/` | Schedina portadisplay nella testa: connettore cavo FFC 16P, connettore pannello FPC 18P, condensatori |
| `lib/` | Libreria di progetto `PoliClock` (simboli e footprint delle parti LCSC specifiche) |
| `scripts/` | Generatore dello schema rev 0.1 ed esportazioni |

Sono **due progetti KiCad separati** (un PCB ciascuno); la pannellizzazione in un unico ordine JLC si decide col layout. Simboli e footprint di resistenze, condensatori, AMS1117, USBLC6, AO3400A provengono dalle librerie standard di KiCad 10; le altre parti dalla libreria `PoliClock`.

Ogni simbolo montato ha il campo **`LCSC`** (codice JLCPCB/LCSC). I componenti DNP (predisposizione touch) sono marcati *Do not populate*.

## File esportati

- `*/<progetto>.pdf` — schema in PDF.
- `*/<progetto>-bom-jlcpcb.csv` — BOM nel formato di assemblaggio JLCPCB (`Comment, Designator, Footprint, LCSC Part #`), **senza** DNP e punti di test.
- `*/<progetto>-bom-completa.csv` — BOM con DNP e note.
- `*/erc.rpt` — report ERC di `kicad-cli` (0 violazioni alla rev 0.1, tutte le severità).

Sensore SHT40 e RTC non hanno un PCB proprio: sono moduli commerciali collegati ai connettori J3 e J4 della scheda principale (`DEC-028`, `DEC-024`).

## PCB della scheda principale (bozza sbrogliata)

- `policlock-main/policlock-main.kicad_pcb`: **40 × 30 mm, 2 strati, componenti solo sopra**, antenna del modulo oltre il bordo destro (`DEC-029`…`DEC-033`). Posizionato e **sbrogliato con Freerouting**: DRC 0 errori e 0 connessioni aperte, da rivedere a vista (`OPEN-027`).
- `policlock-main-top.png` / `-bottom.png`: render 3D; `policlock-main-layout.pdf`: assemblaggio (F.Fab), rame e legenda del retro; `drc.rpt`: DRC (nessun errore, solo avvisi di serigrafia).
- `policlock-main-scheda.step`: sagoma della scheda con fori, per il CAD. Lo STEP completo con i componenti (`policlock-main.step`) usa i modelli 3D EasyEDA e resta **solo locale** (ignorato da git): si rigenera con `esporta.py` dopo aver scaricato i modelli (vedi sotto).
- Generato da `scripts/genera_pcb_main.py` (Python di KiCad: `"C:/Program Files/KiCad/10.0/bin/python.exe"`), posizioni fisse in `scripts/posizioni_main.py`, dimensioni con la variabile `PCB_WH` (default `40,30`) e spaziatura extra con `PCB_GAP` (default `0.6`). Sbroglio con `scripts/sbroglia_main.py` (Freerouting 2.5.0 jar + Java 25 portatile in `%LOCALAPPDATA%\Programs\freerouting-2.5.0`, non nel repository). Dopo la prima modifica manuale il `.kicad_pcb` diventa la fonte: non rieseguire gli script.

## Rigenerare / verificare

```bash
python hardware/scripts/esporta.py
```

Esegue ERC (`--severity-all`, esce con errore se ci sono violazioni), PDF e BOM dei progetti con `kicad-cli` (percorso modificabile con la variabile `KICAD_CLI`).

Lo schema rev 0.1 è stato **generato** da `scripts/genera_schemi.py` (posizionamento, collegamenti con etichette e simboli di alimentazione). Dopo la prima modifica manuale in KiCad **i file `.kicad_sch` diventano la fonte**: non rieseguire il generatore, che li sovrascriverebbe.

## Libreria `PoliClock`

Importata da LCSC con [easyeda2kicad](https://github.com/uPesy/easyeda2kicad.py):

```bash
easyeda2kicad --full --lcsc_id=C2838502 --output hardware/lib/PoliClock
```

(codici: C2838502, C165948, C262665, C262666, C160404, C160402, C720477), poi corretta con `scripts/correggi_libreria.py` e aggiornata al formato KiCad 10 con `kicad-cli fp upgrade` / `kicad-cli sym upgrade`. Correzioni applicate:

- tipi elettrici dei pin (alimentazione, NC, bidirezionali) per un ERC significativo;
- campo `LCSC Part` rinominato `LCSC`, riferimenti `J`/`U`/`SW`;
- USB-C: pioli di centraggio come fori non metallizzati e distanza locale 0,1 mm tra le piazzole a passo 0,5 mm.

I **modelli 3D** EasyEDA non sono nel repository (licenza non verificata, ~21 MB): si rigenerano con lo stesso comando e finiscono in `lib/PoliClock.3dshapes/` (ignorata da git). I footprint vanno confrontati con i disegni dei produttori durante il layout.

Selezione e motivazioni dei componenti: [docs/12-selezione-componenti.md](../docs/12-selezione-componenti.md).
