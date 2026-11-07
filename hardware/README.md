# Hardware PoliClock (KiCad 10)

**Stato:** schema rev 0.1 (M2, solo schematico). **Non validato**: prima dell'ordine servono prototipo M1, layout, DRC, checklist e revisione visiva del proprietario in KiCad (`VT-PCB-001`). Il layout PCB non è ancora iniziato.

## Struttura

| Cartella | Contenuto |
|---|---|
| `policlock-main/` | Scheda principale: schema gerarchico (USB e alimentazione, MCU, display/cavo FFC, periferiche I²C e pulsante), PDF, BOM, report ERC |
| `policlock-display/` | Schedina portadisplay nella testa: connettore cavo FFC 16P, connettore pannello FPC 18P, condensatori |
| `policlock-sht40/` | Mini-PCB SHT40 con connettore JST-SH 4 poli (Qwiic) |
| `lib/` | Libreria di progetto `PoliClock` (simboli e footprint delle parti LCSC specifiche) |
| `scripts/` | Generatore dello schema rev 0.1 ed esportazioni |

Sono **tre progetti KiCad separati** (un PCB ciascuno); la pannellizzazione in un unico ordine JLC si decide col layout. Simboli e footprint di resistenze, condensatori, AMS1117, USBLC6, AO3400A provengono dalle librerie standard di KiCad 10; le altre parti dalla libreria `PoliClock`.

Ogni simbolo montato ha il campo **`LCSC`** (codice JLCPCB/LCSC). I componenti DNP (predisposizione touch) sono marcati *Do not populate*.

## File esportati

- `*/<progetto>.pdf` — schema in PDF.
- `*/<progetto>-bom-jlcpcb.csv` — BOM nel formato di assemblaggio JLCPCB (`Comment, Designator, Footprint, LCSC Part #`), **senza** DNP e punti di test.
- `*/<progetto>-bom-completa.csv` — BOM con DNP e note.
- `*/erc.rpt` — report ERC di `kicad-cli` (0 violazioni alla rev 0.1, tutte le severità).

## Rigenerare / verificare

```bash
python hardware/scripts/esporta.py
```

Esegue ERC (`--severity-all`, esce con errore se ci sono violazioni), PDF e BOM dei tre progetti con `kicad-cli` (percorso modificabile con la variabile `KICAD_CLI`).

Lo schema rev 0.1 è stato **generato** da `scripts/genera_schemi.py` (posizionamento, collegamenti con etichette e simboli di alimentazione). Dopo la prima modifica manuale in KiCad **i file `.kicad_sch` diventano la fonte**: non rieseguire il generatore, che li sovrascriverebbe.

## Libreria `PoliClock`

Importata da LCSC con [easyeda2kicad](https://github.com/uPesy/easyeda2kicad.py):

```bash
easyeda2kicad --full --lcsc_id=C2838502 --output hardware/lib/PoliClock
```

(codici: C2838502, C165948, C262665, C262666, C160404, C160402, C2909890, C318884), poi corretta con `scripts/correggi_libreria.py` e aggiornata al formato KiCad 10 con `kicad-cli fp upgrade` / `kicad-cli sym upgrade`. Correzioni applicate:

- tipi elettrici dei pin (alimentazione, NC, bidirezionali) per un ERC significativo;
- campo `LCSC Part` rinominato `LCSC`, riferimenti `J`/`U`/`SW`;
- **SHT40**: rimosso il pad centrale (die pad) dal footprint, come richiesto dal datasheet Sensirion SHT4x V7.3 §5.3.

I **modelli 3D** EasyEDA non sono nel repository (licenza non verificata, ~21 MB): si rigenerano con lo stesso comando e finiscono in `lib/PoliClock.3dshapes/` (ignorata da git). I footprint vanno confrontati con i disegni dei produttori durante il layout.

Selezione e motivazioni dei componenti: [docs/12-selezione-componenti.md](../docs/12-selezione-componenti.md).
