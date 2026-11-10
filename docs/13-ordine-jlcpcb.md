# 13 — Preventivo JLCPCB della scheda principale (PCB + montaggio)

Guida passo passo per il proprietario. Serve a **chiedere il preventivo e la revisione DFM senza ordinare**. File generati il 2026-11-10 dal commit di progetto `e365648` (registrazione in [10](10-decisioni-aperte.md) §19, `DEC-051`).

> **Prima si fa solo il preventivo.** Non pagare e non confermare l'ordine. L'ordine richiede ancora i gate di [10](10-decisioni-aperte.md) §15 (`OPEN-028`, `OPEN-016`, `OPEN-021`) e una tua decisione esplicita.

## 1. File da caricare

Sono tutti in `hardware/policlock-main/jlc-quotazione/`. La cartella non è versionata: per ricrearla si esegue `python hardware/scripts/esporta_gerber_jlc.py --conferma-proprietario` e si copiano i file.

| File | Dove si carica | Note |
|---|---|---|
| `policlock-main-gerber-jlc.zip` | "Add gerber file" (PCB) | 9 Gerber, 2 file di foratura (PTH e NPTH), job file. SHA-256 `5f6216d11cc12e67eb175a987e5075481fc560d29b602cb1975685c2dd617b44` |
| `policlock-main-bom-jlcpcb.csv` | PCB Assembly → "Add BOM File" | 18 righe, 34 parti, senza J2–J5 |
| `policlock-main-cpl-jlcpcb.csv` | PCB Assembly → "Add CPL File" | 34 parti, tutte sul lato Top |
| `policlock-main-cpl-jlcpcb-u3-centro-corpo.csv` | solo se serve, al posto della CPL normale (§4) | uguale alla CPL normale, ma con U3 al centro del corpo (X 37,51 invece di 34,41 mm) |

## 2. Opzioni del PCB

| Opzione sul sito | Scelta | Perché |
|---|---|---|
| Base Material | FR-4 | `DEC-030` |
| Layers | 2 | `DEC-030` |
| Dimensions | 50,5 × 41,5 mm (le legge dai Gerber: controllare) | `DEC-045` |
| PCB Qty | **5** | `BOM-001` in [08](08-bom-preliminare.md) |
| Product Type / Different Design | Industrial/Consumer electronics, 1 | — |
| Delivery Format | Single PCB | niente pannello: l'assemblaggio Economic non richiede bordi tecnici |
| PCB Thickness | **1,6 mm** | spessore del progetto; ENIG in Economic solo a 1,6 mm |
| Outer Copper Weight | **1 oz** | — |
| Via Covering | Tented | nei Gerber le 70 vie sono coperte dalla maschera |
| Mark on PCB | **nessun marchio / "Remove"** | dal maggio 2026 JLC non aggiunge più il numero d'ordine e chiede di **non** usare il segnaposto `JLCJLCJLCJLC` ([pagina JLC](https://jlcpcb.com/help/article/How-to-mark-on-PCB), aggiornata il 2026-05-22). Se il sito propone comunque un numero o un codice 2D, scegliere "Remove" |
| PCB Color | a scelta (verde se si sceglie ENIG) | in Economic l'ENIG è disponibile solo sul verde |
| Surface Finish | **HASL lead-free** oppure **ENIG**: vedi sotto | — |
| Confirm Production File | Yes, se offerto | per vedere i file di produzione prima che partano |

**HASL lead-free o ENIG?** La scelta è tua.
- **HASL lead-free**: costa meno e va bene per 0603, SOT-23 e le piazzole del modulo. La superficie però non è perfettamente piana. Il punto delicato sono i contatti a passo fine della USB-C (J1), dove lo stagno in eccesso può fare ponti.
- **ENIG**: le piazzole sono piane, quindi la pasta si stampa meglio sulla USB-C e sulle piazzole del WROOM-02 (EPAD compresa), e le saldature a mano di J1–J5 risultano pulite. Costa di più e obbliga al verde. Conviene confrontare i due prezzi nel preventivo.
- **HASL con piombo**: da evitare (RoHS).

## 3. Opzioni del montaggio (PCB Assembly)

| Opzione | Scelta |
|---|---|
| PCBA Type | **Economic** (`DEC-040`, `DEC-044`: il WROOM-02-N4 è "Economic and Standard") |
| Assembly Side | **Top Side** |
| PCBA Qty | **2** (minimo Economic: 2) |
| Tooling holes | lasciare il valore proposto per l'Economic (non servono bordi tecnici) |
| Confirm Parts Placement | **Yes**, se offerto: JLC manda le foto del posizionamento da approvare |

Dopo il caricamento di BOM e CPL:
- controllare che tutte le **18 righe** siano abbinate al codice LCSC giusto;
- non deve risultare nessuna parte "unselected" o senza stock.

Scorte lette il 2026-11-10 sulle pagine JLC: tutte disponibili (§6).

## 4. Cosa controllare nell'anteprima e nella DFM

Riferimento completo: [12](12-selezione-componenti.md) §7. Annotare nella colonna "Correzione applicata" di quella tabella ogni correzione fatta.

1. **J1 al bordo**: la USB-C è a filo del bordo inferiore, con il guscio 0,4 mm oltre il bordo. È l'**unica eccezione** alla regola dei 2,5 mm (`DEC-045`). Se la DFM la segnala, rispondere che è voluta (connettore da bordo) e chiedere conferma che si monta.
2. **U3, scelta della CPL**: nell'anteprima 2D/3D le piazzole del modulo devono coincidere con il corpo, con l'antenna verso il bordo destro.
   - Se il modulo risulta spostato di circa 3 mm, caricare `policlock-main-cpl-jlcpcb-u3-centro-corpo.csv` e ricontrollare.
   - Non correggere "a occhio".
3. **Pin 1 e rotazioni** (viste dall'alto):
   - **U1**: pin 1 in basso a sinistra, verso J1;
   - **U2**: pin 1 = IN in alto a sinistra;
   - **Q1**: G in basso a sinistra, S in basso a destra, D da solo in alto.
   Se una rotazione è sbagliata, correggerla nello strumento di JLC e annotare l'angolo.
4. **Asole di J1**: 4 asole metallizzate (0,6 × 1,7 e 0,6 × 1,2 mm), non fori tondi, più 2 fori NPTH da 0,65 mm per i pioli.
5. **Fiducial**: 3 cerchi da 1 mm con apertura della maschera da 2 mm (FID1, FID2, FID3).
6. **Zona antenna**: a destra, sotto l'antenna di U3, niente rame su entrambi i lati.
7. **EPAD di U3**: nessuna via dentro la piazzola centrale, 9 aperture di pasta (`DEC-046`).
8. **J2–J5 non montati**: non devono comparire in BOM né in CPL. Sulla scheda restano solo i fori.
9. **Serigrafia**: la serigrafia di J2 oltre il bordo superiore non viene stampata ed è voluta. I testi del retro sono a 1,0 mm.

## 5. Da saldare a mano all'arrivo (`DEC-043`, `DEC-047`)

- **J2**: header 1×8 2,54 mm (90° oppure diritto); il pin 1 = VCC è la piazzola quadrata;
- **J3, J4, J5**: JST PH B4B-PH-K-S;
- **le 4 linguette del guscio di J1**, dal retro.

Prima di ordinare, se non è ancora stato fatto, provare l'innesto 1:1 dei JST PH e dell'header sul layout stampato (FIN-011, [12](12-selezione-componenti.md) §6).

## 6. Scorte LCSC (pagine JLC, 2026-11-10)

Tutti i 18 codici sono disponibili con tipo PCBA **"Economic and Standard"**.

| Codice | Parte | Tipo | A magazzino |
|---|---|---|---:|
| C15849 | 1 µF 0603 | Basic | 12 462 497 |
| C19666 | 4,7 µF 0603 | Basic | 3 741 927 |
| C19702 | 10 µF 0603 | Basic | 9 766 775 |
| C14663 | 100 nF 0603 | Basic | 36 575 655 |
| C57112 | 10 nF 0603 | Basic | 5 579 758 |
| C2977522 | PTC BSMD0805-050-12V | Extended | 58 397 |
| C165948 | USB-C TYPE-C-31-M-12 | Extended | 290 667 |
| C15127 | AO3401A | Basic | 1 638 068 |
| C23186 | 5,1 kΩ 0603 | Basic | 19 929 489 |
| C21189 | 0 Ω 0603 | Basic | 18 497 003 |
| C25804 | 10 kΩ 0603 | Basic | 45 426 466 |
| C23345 | 22 Ω 0603 | Basic | 5 770 138 |
| C25803 | 100 kΩ 0603 | Basic | 15 587 874 |
| C23162 | 4,7 kΩ 0603 | Basic | 15 297 265 |
| C21190 | 1 kΩ 0603 | Basic | 25 412 568 |
| C7519 | USBLC6-2SC6 | Extended | 29 448 |
| C404027 | TLV75533PDBVR | Extended | 77 627 |
| C2934560 | ESP32-C3-WROOM-02-N4 | Extended | 13 010 |

5 codici Extended, come previsto in [08](08-bom-preliminare.md) §8. Le scorte cambiano: ricontrollarle il giorno dell'ordine.

## 7. Dopo il preventivo

Riportare all'agente, per registrarli in [10](10-decisioni-aperte.md), [08](08-bom-preliminare.md) §8 e [12](12-selezione-componenti.md) §7:
- i prezzi: PCB, setup, stencil, Extended, componenti, saldature, spedizione;
- la differenza fra HASL ed ENIG;
- gli avvisi della DFM, soprattutto su J1;
- quale CPL è risultata giusta per U3;
- le eventuali correzioni di rotazione.

Non ordinare finché i gate non sono chiusi e non hai deciso.
