# Seconda revisione finale pre-Gerber — scheda principale PoliClock rev 0.2

**Data:** 2026-11-08 · **Revisore:** Claude (sessione di revisione, sola lettura del progetto) · **Base:** `a2a62a3` (ramo `claude/hardware-schematic-4ff868`), unito nel ramo `claude/revisione-finale-ea91f4`. I file hardware sono identici a `09200dc`, il layout approvato a vista dal proprietario (`git diff 09200dc a2a62a3` tocca solo `docs/10` e `hardware/README.md`). KiCad 10.0.6.

Non ho modificato nessun file di progetto: schema, PCB, `.kicad_pro`, `.kicad_dru`, librerie, script, BOM e CPL sono come in `a2a62a3`, e `git status` è pulito fuori da questa cartella. Non ho generato Gerber: `esporta_gerber_jlc.py` è stato solo letto. Nessun push.

Rapporto precedente: [revisione finale](../revisione-finale/README.md) (commit `cd2505b`, base `1241a0a`).

## 1. Esito

### **PRONTO CON RISERVE**

Nessun rilievo **P1**. Il progetto rispetta le decisioni `CONF` (`DEC-001`…`DEC-045`), i datasheet e le regole JLCPCB lette oggi. Controlli superati:

- ERC: 0 violazioni.
- DRC con tutte le severità, tutte le piste, zone ricalcolate e parità schema ↔ PCB: 0 violazioni, 0 connessioni aperte, 0 problemi di parità.
- Controllo meccanico: PASS. J1 è l'unica eccezione; il margine minimo è U3 a 2,99 mm.
- Coppia USB: |ΔL| = 0,000 mm su entrambe le facce della spina, 2 vie per rete.
- Codici LCSC: tutti "Economic and Standard", nessuno con radiografia richiesta, tutti a magazzino.
- BOM e CPL coincidono con il PCB.

I Gerber si possono generare con `esporta_gerber_jlc.py --conferma-proprietario` **dopo l'approvazione esplicita del proprietario**.

Riserve da chiudere **prima dell'ordine**, non dei Gerber:

- **R2-001 (P2).** La tabella dei controlli di rotazione in `docs/12` §7 indica male il pin 1 di U2 e in modo ambiguo quello di Q1. È proprio il riferimento da usare nell'anteprima JLC.
- **R2-002 (P2).** La checklist dei controlli dopo il plot, in `esporta_gerber_jlc.py`, descrive ancora la scheda 50 × 40 mm con intaglio.
- I P3 (R2-003…R2-007) sono rischi non misurati o pulizia della documentazione.

Restano aperti i gate **dell'ordine** già noti:

- `OPEN-028` (studio volumetrico): può ancora cambiare sagoma o connettori;
- `OPEN-016` (modulo display ricevuto);
- `OPEN-021` (SPI sul cavetto);
- DFM JLC per J1;
- scorte da ricontrollare all'ordine;
- prova 1:1 dei JST PH (FIN-011), che `docs/12` §6 consiglia **prima dei Gerber**.

| ID | Priorità | Titolo | Tipo |
|---|---|---|---|
| R2-001 | P2 | Tabella FIN-004 (`docs/12` §7): pin 1 di U2 indicato "in basso a sinistra", ma nel PCB è in alto a sinistra; descrizione di Q1 ambigua | Fatto osservato |
| R2-002 | P2 | `esporta_gerber_jlc.py`: checklist dopo il plot ferma alla scheda 50 × 40 mm con intaglio | Fatto osservato |
| R2-003 | P3 | Con C11, all'inserzione della USB Q1 può condurre per qualche ms e alimentare brevemente il display | Rischio non misurato (analisi) |
| R2-004 | P3 | LCD_CS passa sotto il modulo a 0,3–0,4 mm dall'inizio della zona antenna; +3V3 ed EN passano sotto il modulo | Fatto osservato; impatto RF solo in V2 |
| R2-005 | P3 | Disaccoppiamento 3V3 e RC di EN lontani dai pin del modulo (circa 21 mm di pista per 3V3, 27 mm con 2 vie per EN) | Fatto osservato + rischio non misurato |
| R2-006 | P3 | Vie termiche aperte nella EPAD (via nella piazzola) | Fatto osservato, rischio basso |
| R2-007 | P3 | Residui nella documentazione (`docs/10` con due §12, tabella FIN non aggiornata, testi di `DEC-041`/`CAND-012`, ecc.) | Fatto osservato |

## 2. Controlli eseguiti

| Controllo | Comando / fonte | Risultato |
|---|---|---|
| Unione della base | `git merge claude/hardware-schematic-4ff868` | Un solo conflitto, in `docs/10` (la mia riga §11 del rapporto precedente): presa la versione del ramo hardware, che cita già il rapporto. Nessun file di progetto toccato |
| ERC | `kicad-cli sch erc --severity-all --exit-code-violations --format json` (anche `report`) | **0 violazioni**, codice d'uscita 0 → [erc.rpt](erc.rpt), [erc.json](erc.json) |
| DRC | `kicad-cli pcb drc --severity-all --all-track-errors --schematic-parity --refill-zones --exit-code-violations --format json` (anche `report`) | **0 / 0 / 0**, codice d'uscita 0 → [drc.rpt](drc.rpt), [drc.json](drc.json). Controlli ignorati: gli stessi tre di prima (pista non centrata sulla via, profili di accordatura, filtri footprint). Zone ricalcolate solo in memoria |
| Controllo meccanico | `python.exe hardware/scripts/verifica_meccanica_pcb.py --output …/verifica-meccanica.json` | **PASS** → [verifica-meccanica.json](verifica-meccanica.json). Unica eccezione J1. Margini minimi: U3 2,99, U2 5,05, C2 6,65 mm |
| Audit geometrico | [audit_finale.py](audit_finale.py) → [audit-finale.json](audit-finale.json) | 53 footprint, 60 vie (47 × 0,6/0,3, 11 × 0,7/0,35, 2 × 0,6/0,35), zone, reti e larghezze |
| Netlist | `kicad-cli sch export netlist` (in una cartella temporanea) | Blocchi controllati rete per rete (§5.1) |
| Coppia USB | Grafo piste + vie (1,6 mm per via) + R3/R4, dai contatti J1 ai pin 13/14 di U3 | D-: B7 → 13 = **13,730 mm**, A7 → 13 = **18,406 mm**; D+: B6 → 14 = **13,730 mm**, A6 → 14 = **18,406 mm**. 18 + 18 elementi tutti **bloccati**; 2 vie per rete (USB_DN_C, USB_DP_C) solo sui rami A |
| Piani GND | Riempimento in memoria | F.Cu: 3 isole (1223 / 38 / 3 mm²), 60 % della scheda. B.Cu: 3 isole (1064 / 195 / 0,7 mm²), 60 %. Isole scollegate rimosse ("always"). 19 vie GND più 4 vie termiche nella EPAD |
| Serigrafia | Audit dei testi | 17 testi su B.Silkscreen, tutti 1,0 mm / 0,15 mm; nessun testo su F.Silkscreen; linee delle impronte standard 0,12 mm |
| BOM/CPL ↔ PCB | Confronto programmatico | 33 designatori in BOM JLC (17 righe) = CPL = parti sopra non escluse; coordinate e rotazioni identiche al PCB (origine 100,140 = angolo in basso a sinistra); LCSC e valori coincidenti; formato `Comment, Designator, Footprint, LCSC Part #, Qty` / `Designator, Mid X, Mid Y, Layer, Rotation` |
| Codici LCSC | Pagine `jlcpcb.com/partdetail/<codice>` nel browser, oggi | §4.3 |
| Pagine JLC | [capacità PCB](https://jlcpcb.com/capabilities/pcb-capabilities), [capacità assemblaggio](https://jlcpcb.com/capabilities/pcb-assembly-capabilities), [termini](https://jlcpcb.com/help/article/Terms-and-Conditions-of-JLCPCB-Assembly-Service), [guida Gerber per KiCad 8](https://jlcpcb.com/help/article/how-to-generate-gerber-and-drill-files-in-kicad-8) ("Last updated on Sep 09, 2026") | §4 |
| Datasheet | [ESP32-C3-WROOM-02 datasheet v1.7](https://documentation.espressif.com/esp32-c3-wroom-02_datasheet_en.pdf): tab. 3-1, tab. 4-1, fig. 8-1 (schema del modulo), fig. 9-1 (schema periferico), fig. 11-1 (land pattern). [Linee guida PCB ESP32-C3](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32c3/pcb-layout-design.html) | §5 |
| Script Gerber | Lettura di `hardware/scripts/esporta_gerber_jlc.py` e `kicad-cli pcb export gerbers/drill --help` (KiCad 10.0.6) | §4.4, R2-002. **Non eseguito** |
| `git status` dopo tutti i comandi | — | Solo questa cartella non tracciata (`.kicad_pro` non riscritto) |

## 3. Rilievi nuovi

### R2-001 — P2: la tabella delle rotazioni in `docs/12` §7 indica male il pin 1 di U2

**Fatto.** Nel PCB, U2 (TLV75533, SOT-23-5, 0°) ha:

- pin 1 (IN) a (115,86; 132,55);
- pin 3 (EN) a (115,86; 134,45);
- pin 5 (OUT) a (118,14; 132,55).

In KiCad la y cresce verso il basso, quindi nella vista dall'alto **il pin 1 è in alto a sinistra**, con i pin 4/5 a destra e il 5 in alto. La tabella di [docs/12](../../../12-selezione-componenti.md) riga 124 dice invece "pin 1 = IN in basso a sinistra come nel PCB".

Per Q1 (riga 125) la tabella dice "gate (pin 1) verso R16/R17". Nel PCB:

- G (pin 1) è in basso a sinistra (116,95; 117,94);
- S (pin 2, +3V3) è in basso a destra, il più vicino a R17;
- D (pin 3) è in alto (117,90; 116,06).

Le righe di U1 (pin 1 in basso a sinistra, verso J1) e U3 (pin 1 in alto, vicino all'antenna) sono corrette.

**Rischio.** Questa tabella è il riferimento per controllare e correggere le rotazioni nell'anteprima JLC (FIN-004). Se l'anteprima mostra U2 giusto, cioè con il pin 1 in alto a sinistra, chi segue la tabella potrebbe "correggerlo" di 180°. Un LDO ruotato di 180° mette IN e OUT su piazzole scambiate.

**Proposta.** Riscrivere le righe U2 e Q1 con l'orientamento letto dal PCB (vista dall'alto, y verso il basso):

- U2: "pin 1 IN in alto a sinistra, pin 5 OUT in alto a destra, pin 2 GND a sinistra al centro";
- Q1: "G pin 1 in basso a sinistra, S pin 2 in basso a destra, D pin 3 in alto, verso C11/C9".

Meglio ancora, allegare un'immagine dello strato F.Fab con i pin 1. È un documento, non il progetto: va fatto prima dell'ordine e non cambia i Gerber.

### R2-002 — P2: la checklist di `esporta_gerber_jlc.py` è ferma alla scheda con l'intaglio

**Fatto.** In [esporta_gerber_jlc.py](../../../../hardware/scripts/esporta_gerber_jlc.py):

- la riga 21 dice "contorno 50 x 40 mm con l'intaglio dell'antenna in alto a destra";
- la riga 76 stampa "asole di J1, intaglio, fiducial…".

Dopo `DEC-045` il contorno è **50,5 × 41,5 mm, rettangolare, senza intaglio**, con l'antenna sulla scheda e la zona vietata di U3.

**Rischio.** Il controllo nel visualizzatore Gerber cercherebbe un intaglio che non c'è e non chiederebbe di controllare ciò che conta ora: contorno rettangolare e **niente rame nella zona antenna** su F.Cu e B.Cu, da x = 141,51 mm al bordo destro.

**Proposta.** Aggiornare il docstring e il messaggio finale:

- "contorno 50,5 × 41,5 mm rettangolare, nessun rame, piste, vie o riempimenti nella zona antenna di U3 su F.Cu e B.Cu";
- "4 vie termiche nella EPAD";
- "17 testi del retro leggibili".

Il resto dello script è conforme alla guida JLC (§4.4).

### R2-003 — P3: transitorio di Q1 all'inserzione della USB con C11 (rischio non misurato)

**Fatto.** C11 (10 nF) collega `DISP_G` a 3V3_DISP; R17 (100 kΩ) porta il gate a +3V3; R16 (10 kΩ) lo collega a IO20.

**Analisi.**

- **Accensione del display.** Con IO20 basso il gate va a 3,3 · 10/110 ≈ 0,30 V, cioè VGS ≈ −3,0 V. Nel [datasheet AO3401A](https://www.aosmd.com/res/datasheets/AO3401A.pdf) l'RDS(on) è specificato anche a −2,5 V. Prima c'è un ritardo di circa 0,1 ms, poi un plateau di Miller con (1,5 − 0,3) V / 9,1 kΩ ≈ 130 µA in C11: dV/dt ≈ 13 V/ms, cioè una rampa di circa **0,25 ms**. Lo spunto vale C · dV/dt ≈ (5–17 µF) · 13 V/ms ≈ **0,07–0,22 A**, sotto i 500 mA dell'LDO. **FIN-003 è risolto nel principio.**
- **Inserzione della USB.** Nuovo comportamento. Mentre +3V3 sale, il drain (C9 e modulo) è a 0 V e C11 tiene il gate vicino a 0 V. R17 lo riporta verso la source con τ = R17 · C11 ≈ 1 ms, paragonabile alla salita di 3V3. VGS può quindi superare la soglia (−0,5…−1,3 V) e Q1 **condurre per qualche ms**: il display si alimenta brevemente mentre IO20 non è ancora pilotato, poi Q1 si apre e C9 si scarica nel modulo. Non è un guasto: si vedrebbe al massimo un lampo della retroilluminazione, con un po' di carica in più sull'uscita dell'LDO (VBUS non cambia: è dopo l'LDO). Ma non è misurato.

**Proposta.** In `VT-PWR-003` aggiungere l'osservazione di 3V3_DISP e di `DISP_G` **all'inserzione del cavo**, oltre che alle commutazioni di Q1. Nessuna modifica al progetto, salvo esiti anomali.

Nel firmware (`docs/04` §6, sequenza di accensione), attendere almeno 1–2 ms dopo `DISP_EN_N` basso prima del reset del GC9A01. Il valore va poi confermato su banco come già previsto.

### R2-004 — P3: piste sotto il modulo vicino all'inizio della zona antenna

**Fatti.**

- Corpo del WROOM-02 (F.Fab): x = 127,46–147,56 mm. L'antenna occupa gli ultimi 6 mm (datasheet fig. 11-1), quindi parte da x ≈ 141,56.
- La zona vietata dell'impronta parte da x = 141,51 mm, su F.Cu e B.Cu, e il DRC è pulito.
- **LCD_CS** corre su F.Cu a x = 141,08–141,19 per y = 100,2–107,9 (foglio KiCad): a **0,3–0,4 mm** dal bordo della zona antenna, sotto il modulo.
- Sotto il corpo del modulo passano anche:
  - **+3V3** (0,4 mm, F.Cu, y = 104,5, da x = 127,6 a 140,4, più la diagonale B.Cu verso TP3);
  - **EN** (B.Cu, dalla via a (138,7; 102,96)).

**Valutazione.** Le [linee guida Espressif](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32c3/pcb-layout-design.html) preferiscono l'antenna fuori dalla scheda o sopra un intaglio, con "dense ground vias … near the antenna". `DEC-045` (CONF) ha scelto consapevolmente l'antenna sulla scheda con zona vietata: non va riaperta. In V1 la radio è spenta (`DEC-012`, `PR-REL-002`), quindi **nessun impatto in V1**.

**Proposta.** Nessuna modifica per la V1. Annotare in `docs/09` (backlog V2) che con la radio attiva vanno allontanate di almeno 1–2 mm le piste dal bordo della zona antenna (LCD_CS) e va valutato di nuovo il piano GND sotto il modulo.

### R2-005 — P3: disaccoppiamento di 3V3 e RC di EN lontani dai pin del modulo

**Fatti.**

- Il pin 1 (3V3) di U3 è in (140,41; 101,75), nell'angolo vicino all'antenna e al bordo superiore.
- C6 (100 nF) e C5 (10 µF) sono a 16,0 / 17,7 mm in linea d'aria. La pista C6 → pin 1 è lunga circa **21 mm** (F.Cu 0,4 mm via (127,6; 108,67) → (127,6; 104,5) → (140,41; 104,5) → pin 1).
- C7 (RC di EN) è a 18,6 mm dal pin 2; la rete EN è di 27,3 mm con 2 vie, in parte sul retro sotto il modulo.
- Lo [schema periferico Espressif](https://documentation.espressif.com/esp32-c3-wroom-02_datasheet_en.pdf) (fig. 9-1) mette 10 µF + 0,1 µF sul pin 3V3 e l'RC su EN.
- Lo schema del modulo (fig. 8-1) ha **già internamente** 10 µF, 1 µF e diversi 0,1 µF su 3V3. **Non** ha l'RC di EN: R8 10 kΩ è "NC".

**Vincolo.** Con la regola dei 2,5 mm (`DEC-045`) sopra la fila dei pin non c'è spazio per uno 0603: il bordo è a y = 98,5, il corpo dovrebbe partire da y ≥ 101,0, ma le piazzole cominciano a 101,3. A destra c'è la zona vietata dell'antenna. Il compromesso è stato approvato a vista (`OPEN-030`, che lo elencava).

**Rischio (non misurato).** Ondulazione di 3V3 al pin 1 durante l'attività di CPU e flash: basso, grazie ai condensatori interni. Disturbi su EN con reset spuri: basso, perché EN è a bassa impedenza con 10 kΩ / 1 µF, ma la pista è lunga.

**Proposta.** Nessuna modifica. Aggiungere a `VT-PCB-002` due misure:

- 3V3 al pin 1 con l'oscilloscopio durante boot e flash;
- EN senza impulsi spuri durante le commutazioni di Q1 e l'inserzione della USB.

### R2-006 — P3: vie aperte nella piazzola termica (EPAD)

**Fatti.**

- La EPAD (2,9 × 2,9 mm) ha 4 vie da 0,3/0,7 mm. Le piazzole PTH sono su F.Cu/F.Mask/B.Cu **senza B.Mask**: aperte sopra, coperte dalla maschera sotto.
- La pasta è divisa in 9 finestre da 0,7 mm, circa il 52 % della EPAD, che non toccano i fori (circa 0,05 mm di distanza).
- Il land pattern Espressif (fig. 11-1) prevede "Via for thermal pad". Il datasheet (§9) dice che saldare la EPAD non è obbligatorio e mette in guardia dall'eccesso di pasta.
- I termini JLC escludono la propria responsabilità per i problemi delle vie nella piazzola.

**Rischio.** Un po' di stagno può risalire nei fori; la tenuta del modulo è data dai 18 pin. È basso.

**Proposta.** Nessuna modifica. Guardare la EPAD nell'anteprima 3D/DFM di JLC.

### R2-007 — P3: residui nella documentazione

Fatti osservati:

- [docs/10](../../../10-decisioni-aperte.md):
  - ha **due sezioni "## 12."** (contorno `DEC-045` e approvazione a vista);
  - nella tabella di §11, FIN-002 risulta ancora "**Aperto** → `OPEN-030`", mentre `OPEN-030` è chiusa (§12);
  - nella riga di `DEC-041` resta "pin 26/27 del modulo" accanto a "pin 13/14";
  - `CAND-012` indica ancora il MINI-1 "consigliato";
  - in §6 P1-03 compare "zona antenna senza rame sopra l'intaglio".
- [docs/12](../../../12-selezione-componenti.md) §6 dice "C5/C6 a circa 16 mm, con pista diretta": 16 mm è la distanza in linea d'aria, la pista è di circa 21 mm e passa sotto il modulo (R2-005).
- [hardware/README](../../../../hardware/README.md) riga 76 cita ancora C2838502 (impronta MINI-1) fra le importazioni: è storico, ma non è segnato come tale.
- BOM JLC: il commento "0Ω" è UTF-8 senza BOM (già notato in FIN-009). JLC abbina per codice LCSC.

**Proposta.** Correggere i testi alla prossima modifica documentale, rinumerando la seconda §12 in §13 e aggiornando la tabella FIN di §11. Nessun effetto sul progetto.

## 4. Regole JLCPCB e produzione

### 4.1 Fabbricazione

Valori dalla [pagina capacità PCB](https://jlcpcb.com/capabilities/pcb-capabilities), 2 strati, 1 oz, letta oggi:

| Voce | JLC | Progetto | Esito |
|---|---|---|---|
| Pista / distanza | 0,10 / 0,10 mm | pista ≥ 0,15 mm; distanza 0,15 mm (classi di rete) | OK |
| Via | foro ≥ 0,15, diametro ≥ 0,25 mm; diametro ≥ foro + 0,1 mm | 0,6/0,3, 0,7/0,35, 0,6/0,35 | OK |
| Anello delle PTH | ≥ 0,18 assoluto (0,25 raccomandato) | regola `.kicad_dru` ≥ 0,18; J1 0,20, JST 0,225, vie EPAD 0,20, J2 0,35, H1/H2 1,1 | OK, sotto il raccomandato per J1/JST/EPAD |
| PTH-pista | 0,28 min, 0,35 raccomandato | `min_hole_clearance` 0,3 | OK |
| Foro-foro | 0,2 (vie), 0,45 (piazzole) | 0,25 | OK |
| Rame-bordo | 0,2 | 0,3 più una fascia di 0,45 mm senza piste e vie | OK |
| Asole metallizzate | larghezza ≥ 0,5, lunghezza ≥ 2× larghezza | J1 0,6 × 1,2 e 0,6 × 1,7 | OK, al limite di 2× |
| NPTH | ≥ 0,5 | J1 Ø 0,65 | OK |
| Serigrafia | testo ≥ 1,0 mm, tratto ≥ 0,15 mm | testi 1,0 / 0,15 (regola nel `.kicad_pro`); linee delle impronte 0,12 | Testi OK; linee della libreria come accettato in FIN-007 |

### 4.2 Assemblaggio

- **Economic**: lato unico, 2 strati, spessore 1,6 mm (Economic: 0,8–1,6), scheda ≥ 10 × 10 mm. Bordi tecnici e fiducial "Not necessary" ([capacità assemblaggio](https://jlcpcb.com/capabilities/pcb-assembly-capabilities)). I [termini](https://jlcpcb.com/help/article/Terms-and-Conditions-of-JLCPCB-Assembly-Service) dicono in generale che fori di attrezzaggio, bordi tecnici e fiducial sono richiesti, e che JLC li aggiunge se mancano: con l'Economic non è un'azione nostra. Tutti i 17 codici della BOM JLC sono "Economic and Standard" (§4.3). Conforme a `DEC-040`/`DEC-044`.
- **Corpo-bordo ≥ 2,5 mm** ("must be equal or greater than 2.5mm"): PASS per tutte le parti JLC (U3 2,99 mm). **Unica eccezione J1**, a filo del bordo inferiore con il guscio 0,4 mm oltre, da far accettare alla DFM JLC come stabilito in `DEC-045`.
- **J2–J5**: impronte a foro passante, "escluse dai file di posizionamento", campo `Montaggio`, nessun LCSC; fuori da BOM JLC e CPL, presenti nella BOM completa. Conforme a `DEC-043`.
- **Fiducial**: 3 da 1 mm con apertura della maschera di 2 mm e zona vietata di 3 × 3 mm, in posizione asimmetrica (dall'angolo in basso a sinistra: FID1 3,5/7,5; FID2 16/28; FID3 46/9 mm).
- **BOM/CPL**: formato JLC corretto, contenuto coerente con il PCB. Rotazioni KiCad native, da controllare nell'anteprima: tabella di `docs/12` §7, da correggere (R2-001). Origine di U3 = centro delle file di piazzole: il corpo è spostato di circa 3,1 mm verso l'antenna (F.Fab 127,46–147,56).

### 4.3 Codici LCSC (pagine `jlcpcb.com/partdetail`, 2026-11-08)

| LCSC | Parte | Rif. | Libreria | Tipo PCBA | Radiografia | Magazzino |
|---|---|---|---|---|---|---:|
| C2934560 | ESP32-C3-WROOM-02-N4 (MSL 3) | U3 | Extended | Economic e Standard | no | 13 098 |
| C57112 | 0603B103K500NT 10 nF 50 V X7R | C11 | Basic | Economic e Standard | no | 5 815 334 |
| C165948 | TYPE-C-31-M-12 | J1 | Extended | Economic e Standard | no | 317 984* |
| C2977522 | BSMD0805-050-12V | F1 | Extended | Economic e Standard | no | 58 850* |
| C7519 | USBLC6-2SC6 | U1 | Extended | Economic e Standard | no | 23 494* |
| C404027 | TLV75533PDBVR | U2 | Extended | Economic e Standard | no | 93 975* |
| C15849 | CL10A105KB8NNNC 1 µF | C1, C7 | Basic | Economic e Standard | no | 12 929 773* |
| C19666 | CL10A475KO8NNNC 4,7 µF | C2 | Basic | Economic e Standard | no | 3 835 848* |
| C19702 | CL10A106KP8NNNC 10 µF | C3, C5, C9 | Basic | Economic e Standard | no | 10 291 320* |
| C14663 | CC0603KRX7R9BB104 100 nF | C4, C6, C8, C10 | Basic | Economic e Standard | no | 34 057 897* |
| C15127 | AO3401A | Q1 | Basic | Economic e Standard | no | 1 773 123* |
| C23186 | 5,1 kΩ | R1, R2 | Basic | Economic e Standard | no | 20 326 582* |
| C21189 | 0 Ω | R3, R4, R5, R21 | Basic | Economic e Standard | no | 19 075 860* |
| C25804 | 10 kΩ | R6, R7, R15, R16, R22 | Basic | Economic e Standard | no | 47 545 179* |
| C23345 | 22 Ω | R8, R9 | Basic | Economic e Standard | no | 5 976 206* |
| C21190 | 1 kΩ | — (non più in BOM dopo FIN-003) | — | — | — | — |
| C25803 | 100 kΩ | R17 | Basic | Economic e Standard | no | 16 148 758* |
| C23162 | 4,7 kΩ | R19, R20 | Basic | Economic e Standard | no | 15 968 211* |

\* Magazzino letto nel primo passaggio di oggi (rapporto precedente); libreria e tipo PCBA riletti in questa revisione. 5 Extended (C2934560, C165948, C2977522, C7519, C404027), 12 Basic. Da ricontrollare all'ordine.

### 4.4 `esporta_gerber_jlc.py` (letto, non eseguito)

Confronto con la [guida JLC per KiCad 8](https://jlcpcb.com/help/article/how-to-generate-gerber-and-drill-files-in-kicad-8) (aggiornata il 2026-09-09) e con `kicad-cli` 10.0.6:

- **Gate**: si ferma senza `--conferma-proprietario`; prima del plot esegue `esporta.py` (ERC, DRC con parità e zone, controllo meccanico).
- **Strati**: F.Cu, B.Cu, F.Paste, B.Paste, F.Silkscreen, B.Silkscreen, F.Mask, B.Mask, Edge.Cuts, come nella guida.
- **Gerber**: estensioni Protel (predefinite in `kicad-cli`; si disattivano solo con `--no-protel-ext`, non usato), `--subtract-soldermask`, `--check-zones`, origine assoluta. X2 attivo (non trattato dalla guida; JLC lo accetta).
- **Forature**: Excellon, mm, zeri `decimal`, origine assoluta, ovali `alternate` (come nella guida; `route` resta un'opzione), PTH/NPTH separati, mappa in PDF.
- **Uscita**: `gerber-jlc/` e lo zip sono ignorati da git (`hardware/.gitignore`).
- **Da aggiornare**: la checklist (R2-002).

## 5. Parti confermate corrette

### 5.1 Circuito (netlist rispetto ai datasheet)

- **Modulo WROOM-02-N4** (datasheet v1.7, tab. 3-1):
  - 1 3V3, 2 EN, 3 IO4 = LCD_DC, 4 IO5 = LCD_RST, 5 IO6 = LCD_SCLK (FSPICLK), 6 IO7 = LCD_MOSI (FSPID), 7 IO8 = I2C_SCL, 8 IO9 = BOOT, 9 GND, 10 IO10 = LCD_CS (FSPICS0);
  - 11 RXD/IO20 = DISP_EN_N, 12 TXD/IO21 = TP5, 13 IO18 = USB D-, 14 IO19 = USB D+, 15 IO3 = BTN_USER, 16 IO2 = I2C_SDA, 17 IO1 = TP10, 18 IO0 = TP9, 19 EPAD = GND.
  - Tutti corrispondono.
- **Strapping** (tab. 4-1): GPIO2 e GPIO8 flottanti di default, tenuti alti da R19/R20 4,7 kΩ; GPIO9 con R7 10 kΩ e TP11 per il download. EN con R6 10 kΩ / C7 1 µF, come la fig. 9-1 ("R = 10 kΩ and C = 1µF"), e TP6.
- **USB-C / protezioni / LDO** (invariati):
  - CC1/CC2 con 5,1 kΩ; VBUS → F1 → +5V;
  - U1 USBLC6 sui pin 1/6 (D-) e 3/4 (D+), 2 GND, 5 +5V;
  - R5 → 5V_LDO con C2 4,7 µF;
  - U2 TLV75533: IN 1, GND 2, EN 3 = IN, NC 4, OUT 5 con C3 10 µF e C4 100 nF a 2,24–2,39 mm dai pin;
  - **capacità su VBUS = C1 1 µF + C2 4,7 µF = 5,7 µF nominali** (`DEC-042`).
- **Display**:
  - Q1 AO3401A con G = 1, S = 2 (+3V3), D = 3 (3V3_DISP); R16 10 kΩ, R17 100 kΩ, C11 10 nF fra gate e drain (R2-003);
  - J2: 1 3V3_DISP, 2 GND, 3 SCLK_C, 4 MOSI_C, 5 DC, 6 CS, 7 RST; R8/R9 22 Ω; R15 su LCD_RST verso 3V3_DISP; C9/C10 su 3V3_DISP.
- **I²C e pulsante** (`DEC-043`):
  - J3/J4: 1 GND, 2 3V3_EXT (R21), 3 SDA, 4 SCL, nello stesso ordine del connettore Qwiic/STEMMA QT;
  - J5: 1 BTN_USER (R22 10 kΩ, C8 100 nF), 2 GND, 3–4 non collegati.
- **Fuori perimetro**: nessuna batteria, nessun touch, nessun componente radio aggiuntivo. La radio del modulo resta inutilizzata in V1 (`DEC-012`, `DEC-023`, `DEC-034`).

### 5.2 PCB

- **Contorno**: 50,5 × 41,5 mm rettangolare (Edge.Cuts da (100; 98,5) a (150,5; 140)), 2 strati, componenti solo sopra (`DEC-030`, `DEC-045`).
- **Coppia USB** (`DEC-041`):
  - percorso B senza vie, 13,730 / 13,730 mm;
  - percorso A con 2 vie per rete, 18,406 / 18,406 mm;
  - |ΔL| = 0,000 mm (criterio < 0,5 mm);
  - 36 elementi bloccati;
  - zona `usb_coppia_retro` su B.Cu da U1 ai pin 13/14 (x 131,96–135,36, y 119,65–127,91).
- **Antenna** (`DEC-045`):
  - zona vietata nell'impronta di U3 su F.Cu e B.Cu, che vieta piste, vie, riempimenti, piazzole e footprint, da x = 141,51 oltre il bordo destro e da y = 96,5 a 124,5;
  - copre l'area antenna del datasheet (ultimi 6 mm del modulo, da x ≈ 141,56) e 5 mm oltre i lati;
  - DRC senza violazioni, quindi nessun rame dentro;
  - punta dell'antenna a 2,94 mm dal bordo destro.
  - Vedi R2-004 per le piste vicine.
- **GND e cucitura**: due piani GND, 19 vie GND (15 di cucitura lungo il contorno, nessuna nella zona USB) e 4 vie termiche nella EPAD (FIN-008).
- **Alimentazioni**: +3V3, +5V, VBUS, 5V_LDO, 3V3_DISP e 3V3_EXT a 0,3–0,4 mm (un tratto di 0,01 mm a 0,2 mm su +3V3 è un raccordo); vie di potenza 0,7/0,35.
- **Termica**: invariata (TLV75533 circa 0,14 W stimati, `VT-PWR-002`).
- **J1**: 4 asole metallizzate a GND (anello 0,20 mm), 2 pioli NPTH Ø 0,65 mm, fori M2 H1/H2 ai lati, invariati.
- **J2–J5**:
  - piazzole PTH con pin 1 quadrato o rettangolare arrotondato, raggi verso GND;
  - J2 con la fila dei fori a 4,4 mm dal bordo superiore;
  - test point sul retro lontani dai piedini THT;
  - courtyard controllati dal controllo meccanico.
- **Serigrafia**: testi del retro a 1,0/0,15 mm; regola `.kicad_dru` per la serigrafia di J2 oltre il bordo (solo rispetto a Edge.Cuts); nessun avviso di serigrafia sul rame.
- **Vie**: tutte coperte dalla maschera su entrambi i lati (`tenting` front/back = yes).

### 5.3 Stato dei rilievi FIN della prima revisione

| Rilievo | Stato | Evidenza |
|---|---|---|
| FIN-001 modulo "Standard Only" | **Chiuso** | `DEC-044`: C2934560 "Economic and Standard", senza radiografia (pagina JLC letta oggi) |
| FIN-002 revisione a vista dopo `DEC-043` | **Chiuso** | `OPEN-030` chiusa (`docs/10` §12): approvato `09200dc`; `a2a62a3` non cambia i file hardware |
| FIN-003 calo di 3V3 all'accensione del display | **Chiuso con riserva** | R16 10 kΩ + C11 10 nF: rampa di circa 0,25 ms, spunto 0,07–0,22 A (stima). Misura in `VT-PWR-003`; nuovo transitorio all'inserzione della USB (R2-003) |
| FIN-004 rotazioni CPL | **Chiuso con riserva** | Procedura in `docs/12` §7, ma righe U2/Q1 da correggere (R2-001) |
| FIN-005 testi della serigrafia | **Chiuso** | 17 testi a 1,0/0,15 mm; `min_text_height` 1,0 nel `.kicad_pro` |
| FIN-006 procedura Gerber | **Chiuso con riserva** | Script conforme alla guida JLC; checklist da aggiornare (R2-002) |
| FIN-007 regole DRC rispetto ai minimi JLC | **Chiuso con riserva** | Regola PTH ≥ 0,18 mm attiva; linee di serigrafia delle impronte a 0,12 mm lasciate come in libreria (scelta motivata) |
| FIN-008 cucitura GND | **Chiuso** | 19 vie GND e 4 vie termiche nella EPAD; nessuna nella zona USB né nella zona antenna |
| FIN-009 documenti ↔ PCB | **Chiuso con riserva** | Corretti i punti segnalati; restano residui nuovi (R2-007) |
| FIN-010 linee esterne senza ESD | **Chiuso** (rischio accettato) | `docs/12` §6, scelta del proprietario |
| FIN-011 impronta JST PH | **Aperto** (azione del proprietario) | Prova 1:1 con i B4B-PH-K-S, consigliata in `docs/12` §6 **prima dei Gerber**: non risulta fatta |

### 5.4 Coerenza

Requisiti (`docs/01`), decisioni (`DEC-001`…`DEC-045`), schema, PCB, BOM e CPL sono coerenti:

- V1 offline, senza batteria e senza touch;
- modulo WROOM-02-N4 in Economic;
- scheda 50,5 × 41,5 mm con J1 unica eccezione;
- J2–J5 saldati a mano;
- 5,7 µF su VBUS;
- coppia USB simmetrica.

Nessuna funzione fuori perimetro. Fanno eccezione i testi segnalati in R2-001, R2-002 e R2-007. I test del [piano di verifica](../../../07-piano-verifica.md) restano tutti NOT_RUN.

## 6. Decisioni e azioni del proprietario prima dei Gerber

1. **Autorizzazione esplicita** a generare i Gerber con `python hardware/scripts/esporta_gerber_jlc.py --conferma-proprietario`, da registrare in `docs/10`.
2. **Prova 1:1 dei JST PH e dell'header** (FIN-011), consigliata in `docs/12` prima dei Gerber. È rapida e i connettori sono già in casa.
3. **`OPEN-028`** (studio volumetrico): se può ancora cambiare sagoma o connettori, conviene chiuderlo prima dei Gerber per non doverli rigenerare. Resta comunque un gate dell'ordine.
4. **Confermare** che si accettano per la V1 i compromessi di R2-004 e R2-005 (piste vicino all'antenna, disaccoppiamento lontano), già visti nella revisione a vista, con le misure aggiunte a `VT-PCB-002`/`VT-PWR-003`.

Prima dell'**ordine**:

- correggere R2-001 e R2-002;
- anteprima JLC parte per parte con la tabella corretta;
- DFM per J1;
- scorte;
- `OPEN-016` e `OPEN-021`.

## 7. Evidenze e riproduzione

File in questa cartella:

- [erc.rpt](erc.rpt), [erc.json](erc.json);
- [drc.rpt](drc.rpt), [drc.json](drc.json);
- [verifica-meccanica.json](verifica-meccanica.json);
- [audit_finale.py](audit_finale.py), [audit-finale.json](audit-finale.json).

```powershell
$kicad = 'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe'
$py = 'C:\Program Files\KiCad\10.0\bin\python.exe'
$out = 'docs/revisioni/2026-11-08/revisione-finale-2'
& $kicad sch erc --severity-all --exit-code-violations --format json -o "$out/erc.json" hardware/policlock-main/policlock-main.kicad_sch
& $kicad pcb drc --severity-all --all-track-errors --schematic-parity --refill-zones --exit-code-violations --format json -o "$out/drc.json" hardware/policlock-main/policlock-main.kicad_pcb
& $py hardware/scripts/verifica_meccanica_pcb.py --output "$out/verifica-meccanica.json" hardware/policlock-main/policlock-main.kicad_pcb
& $py "$out/audit_finale.py"
git status --short   # se kicad-cli ha riscritto il .kicad_pro: git checkout -- hardware/policlock-main/policlock-main.kicad_pro
```

Nessuna prova su hardware fisico è stata eseguita: "stima", "analisi" e "rischio" non sono misure. Pagine JLC e scorte vanno ricontrollate all'ordine.
