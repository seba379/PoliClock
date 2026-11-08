# Revisione finale pre-Gerber — scheda principale PoliClock rev 0.2

**Data:** 2026-11-08 · **Revisore:** Claude (sessione di revisione, solo lettura del progetto) · **Base:** commit `1241a0a` (ramo `codex/pcb-edge-courtyard-fixes` = `claude/hardware-schematic-4ff868`), KiCad 10.0.6.

Nessun file di progetto è stato modificato: schema, PCB, `.kicad_pro`, `.kicad_dru`, librerie, script, BOM e CPL sono come nel commit di base (`git status` pulito fuori da questa cartella). Nessun Gerber generato, nessun push. In questa cartella ci sono solo il rapporto, i report ERC/DRC, l'esito del controllo meccanico e uno script di audit in sola lettura.

## 1. Esito

### **NON PRONTO** per generare i Gerber — per due decisioni del proprietario, non per difetti del rame

Il progetto è elettricamente coerente e pulito:

- ERC: 0 violazioni.
- DRC con tutte le severità, zone ricalcolate e parità: 0 violazioni, 0 connessioni aperte, 0 problemi di parità.
- Controllo meccanico: PASS.
- Pinout del modulo conforme al datasheet Espressif v2.2.
- Coppia USB identica a quella approvata (`DEC-041`).
- BOM/CPL coerenti con il PCB.
- Tutti i codici LCSC a magazzino oggi.

Due rilievi **P1** però impediscono di generare oggi i file definitivi:

1. **FIN-001.** Il modulo ESP32-C3-MINI-1-H4X è **"PCBA Type: Standard Only"** sulla pagina JLC. `DEC-040` prevede invece l'assemblaggio "Economic". L'assemblaggio Standard chiede schede da almeno 70 × 70 mm oppure bordi tecnici: va deciso chi li aggiunge e su quali lati. Se li aggiunge il proprietario, i Gerber cambiano. Cambiano anche i costi di `docs/08`.
2. **FIN-002.** Dopo `DEC-043` il layout è cambiato: J2–J5, R15, R19–R21 e C8 sono stati spostati e le reti toccate risbrogliate. `docs/10` §10 chiede una **nuova revisione a vista del proprietario in KiCad**, che non risulta registrata.

Risolti i due P1, l'esito diventa **PRONTO CON RISERVE**. Prima dell'ordine vanno chiusi anche i P2.

Alcuni P2 (FIN-003 e FIN-005) e il P3 FIN-008 cambiano rame o serigrafia: conviene decidere **prima** di generare i Gerber, per non doverli rigenerare. Restano aperti i gate già noti: `OPEN-028`, `OPEN-016`, `OPEN-021` e la DFM JLC su J1/U3.

| ID | Priorità | Titolo | Tipo |
|---|---|---|---|
| FIN-001 | **P1** | Modulo ESP32 solo in assemblaggio Standard: conflitto con "Economic" di `DEC-040`, bordi tecnici da decidere | Fatto osservato (pagina JLC) |
| FIN-002 | **P1** | Revisione a vista del proprietario dopo `DEC-043` non registrata | Gate di processo |
| FIN-003 | P2 | Calo di 3V3 all'accensione del display (Q1 a commutazione brusca su C9 + capacità del modulo) | Rischio non misurato, stima |
| FIN-004 | P2 | Rotazioni e origini della CPL non corrette per JLC: da verificare parte per parte nell'anteprima | Fatto (CPL = valori KiCad) + rischio |
| FIN-005 | P2 | Testi della serigrafia del retro alti 0,8 mm, sotto il minimo JLC di 1,0 mm | Fatto osservato |
| FIN-006 | P2 | Manca una procedura documentata di esportazione Gerber/forature per JLC (asole di J1) | Lacuna di processo |
| FIN-007 | P3 | Regole DRC di KiCad non allineate a tutti i minimi JLC letti oggi | Fatto osservato |
| FIN-008 | P3 | Cucitura GND scarsa (6 vie GND) e nessuna via nella piazzola termica del modulo | Fatto osservato, rischio basso |
| FIN-009 | P3 | Incoerenze fra documentazione e PCB (larghezze, vie, posizione C9, distanze USB-C, classi di rete) | Fatto osservato |
| FIN-010 | P3 | Linee esterne (pulsante, I²C) senza protezione ESD né resistenza in serie | Scelta di progetto da confermare |
| FIN-011 | P3 | Impronta JST PH non riconfrontata con il disegno JST | Verifica mancante |

## 2. Controlli eseguiti

Letti: `AGENTS.md`, `README.md`, `docs/00`–`12` (in particolare 01, 02 §3, 07 VT-PCB-*/VT-PWR-*, 08, 10 con `DEC-001`…`DEC-043` e §6–10, 12), `hardware/README.md`, le revisioni in `docs/revisioni/2026-11-08/` (rapporto Codex, correzioni, verifica di Claude) e la nota di passaggio della sessione hardware.

| Controllo | Comando / fonte | Risultato |
|---|---|---|
| Versione KiCad | `kicad-cli version` | 10.0.6 |
| ERC, tutte le severità | `kicad-cli sch erc --severity-all --exit-code-violations --format json -o …/erc.json hardware/policlock-main/policlock-main.kicad_sch` (anche `--format report`) | **0 violazioni**, codice d'uscita 0 → [erc.rpt](erc.rpt), [erc.json](erc.json). Controlli ignorati dal progetto: etichetta globale singola, giunzione a quattro, modello SPICE, filtri footprint. Verificato sulla netlist che nessuna rete di segnale ha un solo nodo, quindi l'esclusione dell'etichetta globale singola non nasconde errori |
| DRC completo | `kicad-cli pcb drc --severity-all --all-track-errors --schematic-parity --refill-zones --exit-code-violations --format json -o …/drc.json hardware/policlock-main/policlock-main.kicad_pcb` (anche `--format report`) | **0 violazioni, 0 non connessi, 0 problemi di parità**, codice d'uscita 0 → [drc.rpt](drc.rpt), [drc.json](drc.json). Ignorati: pista non centrata sulla via, geometrie dei profili di accordatura, filtri footprint. Zone ricalcolate solo in memoria (nessun `--save-board`) |
| Controllo meccanico | `python.exe hardware/scripts/verifica_meccanica_pcb.py --output …/verifica-meccanica.json` (Python di KiCad) | **PASS** → [verifica-meccanica.json](verifica-meccanica.json). Margine minimo dei corpi JLC: C6 2,51 mm, C7 2,60 mm, Q1 2,70 mm. Eccezioni DFM aperte: J1, U3. Courtyard di J2–J5 completi |
| Audit geometrico | [audit_finale.py](audit_finale.py) → [audit-finale.json](audit-finale.json) (Python di KiCad, sola lettura) | Contorno, posizioni, piazzole THT e anelli, reti e larghezze, vie, zone, test point rispetto a J2–J5 |
| Netlist | `kicad-cli sch export netlist` (in una cartella temporanea) | Tutti i blocchi controllati rete per rete (§5) |
| Coppia USB | Confronto delle piste e vie USB_DN/DP e USB_DN_C/DP_C fra `4fb9200`, `16f9bf7` e `1241a0a` | 36 elementi, tutti bloccati, **impronta identica** (hash `4079b51fe7c7`); J1/U1/R3/R4/U3 nella stessa posizione; zona `usb_coppia_retro` invariata |
| Piani GND | Riempimento in memoria (`ZONE_FILLER`) | F.Cu: 4 isole (1091 / 138 / 18 / 3 mm²), 68 % della scheda; B.Cu: 2 isole (1309 / 20 mm²), 72 %. Isole scollegate rimosse ("always") |
| BOM/CPL ↔ PCB | Confronto programmatico | 32 designatori in BOM JLC = CPL = parti sopra non escluse; coordinate (origine in basso a sinistra = `aux_axis_origin` 100,140) e rotazioni identiche al PCB; LCSC e valori coincidenti. Esclusi: J2–J5, TP1–TP11, H1/H2, FID1–3 |
| Pagine JLC (oggi) | [capacità PCB](https://jlcpcb.com/capabilities/pcb-capabilities), [capacità assemblaggio](https://jlcpcb.com/capabilities/pcb-assembly-capabilities), [termini assemblaggio](https://jlcpcb.com/help/article/Terms-and-Conditions-of-JLCPCB-Assembly-Service) | Vedi §4 e FIN-001/005/007 |
| Codici LCSC (oggi) | Pagine `jlcpcb.com/partdetail/<codice>` lette nel browser | Tutti a magazzino, tabella in §4.3 |
| Datasheet Espressif | [ESP32-C3-MINI-1 datasheet v2.2](https://documentation.espressif.com/esp32-c3-mini-1_datasheet_en.pdf), tab. 3-1, tab. 4-1, fig. 11-1; [linee guida PCB ESP32-C3](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32c3/pcb-layout-design.html) | Pinout e strapping confermati; antenna §5.3 |
| `git status` dopo tutti i comandi | — | Solo questa cartella non tracciata: `kicad-cli` non ha riscritto il `.kicad_pro` |

## 3. Rilievi

### FIN-001 — P1: il modulo ESP32 si monta solo con l'assemblaggio "Standard", non con l'"Economic" di `DEC-040`

**Fatto osservato.** La [pagina JLC di C41349510](https://jlcpcb.com/partdetail/C41349510), letta oggi, indica per ESP32-C3-MINI-1-H4X **"PCBA Type: Standard Only"** e **"X-ray Inspection: Required"**. Tutte le altre 16 parti sono "Economic and Standard".

La [pagina delle capacità di assemblaggio](https://jlcpcb.com/capabilities/pcb-assembly-capabilities) indica:

- per lo **Standard**: scheda singola da 70 × 70 mm in su, bordi tecnici e fiducial "Necessary";
- per l'**Economic**: da 10 × 10 mm in su, bordi tecnici non necessari.

I [termini dell'assemblaggio](https://jlcpcb.com/help/article/Terms-and-Conditions-of-JLCPCB-Assembly-Service) dicono che, se una scheda è sotto 70 × 70 mm o mancano i bordi tecnici, JLC sceglie lei come realizzarli (ad esempio a "mouse bite").

**Conflitto con le decisioni.** La nostra scheda è 50 × 40 mm. Invece:

- `DEC-040` ([docs/10](../../../10-decisioni-aperte.md), riga 49) dice: "assemblaggio "Economic" su un solo lato";
- la stessa ipotesi compare in [docs/02](../../../02-architettura-hardware.md) riga 101, in [docs/08](../../../08-bom-preliminare.md) righe 87 e 92 (setup Economic 8,18 $) e in [docs/11](../../../11-fonti.md) riga 53.

Non è un difetto del rame, ma l'ordine non può seguire la decisione così com'è scritta.

**Perché blocca i Gerber.** Con lo Standard servono bordi tecnici. Ci sono due strade:

- **(a)** li aggiunge JLC: nessuna modifica ai Gerber, ma bisogna indicare i lati;
- **(b)** li disegna il proprietario: i Gerber cambiano.

Inoltre il guscio di J1 sporge 0,4 mm oltre il bordo inferiore (F.Fab di J1 fino a y = 140,4 contro il bordo a 140,0). Un bordo tecnico sul lato inferiore sarebbe quindi incompatibile.

**Proposta (decisione del proprietario, da registrare come nuova `DEC` che aggiorna `DEC-040`):**

- Ordinare con **assemblaggio Standard** e "bordi tecnici aggiunti da JLC" **sui lati sinistro e destro**: mai quello inferiore, per J1. Sul destro l'intaglio dell'antenna resta un vuoto interno al pannello. A sinistra le piazzole di J3–J5 sono a ≥ 2,4 mm dal bordo: i ponticelli da staccare passano lì vicino, ma i JST si saldano dopo la separazione.
- In alternativa, chiedere a JLC prima dell'ordine se accetta il modulo con l'Economic. La pagina oggi dice di no.
- Aggiornare in `docs/08` i costi (setup Standard, eventuale radiografia) e in `docs/02`/`docs/11` la dicitura "Economic".
- Con i bordi tecnici sui lati sinistro e destro, la regola dei 2,5 mm sui lati superiore e inferiore perde in pratica il motivo del trasporto. Le eccezioni J1/U3 vanno comunque sottoposte alla DFM.

### FIN-002 — P1: manca la revisione a vista del proprietario dopo `DEC-043`

**Evidenza.** [docs/10](../../../10-decisioni-aperte.md) riga 203 (§10, dopo `DEC-043`): "serve una nuova revisione a vista del proprietario in KiCad". La revisione a vista registrata (§9, `OPEN-027` chiusa) è **precedente** a `DEC-043`. Il commit `1241a0a` ha poi:

- spostato J2–J5, R15, R19, R20, R21 e C8;
- invertito la posizione del pin 1 di J2 (ora a sinistra);
- risbrogliato LCD_*, I²C, BTN_USER e 3V3_DISP, con BTN_USER ora lungo circa 72 mm sui bordi superiore e sinistro.

Non si trova traccia della nuova approvazione. `AGENTS.md` richiede la revisione visiva del proprietario prima dell'ordine.

**Proposta.** Il proprietario apre il PCB in KiCad. Controlla soprattutto:

- la zona di J2 e Q1;
- la colonna R19/R20/R21/C8;
- i percorsi di BTN_USER e I²C;
- le etichette del retro accanto a J3–J5.

Poi si registra l'esito in `docs/10` §10. Se la revisione è già stata fatta ma non scritta, basta registrarla.

### FIN-003 — P2: calo di 3V3 all'accensione del modulo display (rischio non misurato)

**Fatti.** Q1 (AO3401A) collega direttamente +3V3 a 3V3_DISP, con R16 = 1 kΩ in serie al gate e R17 = 100 kΩ di pull-up (netlist: `DISP_G` = Q1.1, R16.2, R17.2). Su 3V3_DISP ci sono:

- C9 = 10 µF (CL10A106KP8NNNC, X5R 10 V 0603);
- C10 = 100 nF;
- la capacità d'ingresso del modulo display, sconosciuta.

Sul lato +3V3 ci sono C3 e C5 da 10 µF (stesso codice) e C4/C6 da 100 nF. Il datasheet Espressif v2.2 fissa l'alimentazione raccomandata del modulo a **3,0–3,6 V**.

**Stima (non misura).** Con 1 kΩ sul gate il MOSFET si chiude in pochi µs, troppo in fretta perché l'anello dell'LDO compensi. Il primo istante è dunque governato dalla ripartizione di carica fra le due capacità:

- tenendo conto della riduzione dei 10 µF 0603 sotto polarizzazione (circa 5–7 µF effettivi), +3V3 ha circa 10–15 µF;
- 3V3_DISP ha circa 5–7 µF da C9, più il modulo;
- la tensione scende a circa 3,3 · C_main / (C_main + C_disp), cioè **circa 2,5 V con il solo C9 e fino a circa 1,5–2 V** se il modulo ha qualche µF a bordo.

È un ordine di grandezza: resistenze, tempi di commutazione e risposta dell'LDO lo riducono, ma nulla nel progetto lo controlla.

**Scenario di guasto.** Il firmware accende il display dopo l'avvio. Se il calo provoca un brown-out o un reset, il firmware riaccende il display e si entra in un **ciclo di riavvii**. Succede a ogni uscita dalla modalità notte e a ogni `NIGHT_PEEK`. `VT-PWR-003` prevede già di osservare VBUS e 3V3 durante le commutazioni di Q1, ma solo dopo l'ordine.

**Proposte (scelta del proprietario):**

1. **Prima dell'ordine**, sul banco M1: replicare Q1 con R16/R17/C9 e il modulo display vero, poi misurare 3V3 con l'oscilloscopio.
2. In alternativa, aggiungere ora una **piazzola 0603 per un condensatore gate-drain** (fra `DISP_G` e 3V3_DISP) e portare R16 a circa 10 kΩ. Valori da provare: 10 nF con 10 kΩ danno una rampa di circa 0,2–0,3 ms e uno spunto di circa 0,2 A. Con 10 kΩ e R17 = 100 kΩ, VGS in conduzione resta circa −3,0 V. Il condensatore si può lasciare non montato se la misura è buona.
3. Riserva senza modifiche al PCB: un condensatore da 0603 saldato a mano fra i pin 1 e 3 di Q1 (SOT-23) dopo la consegna.

Ridurre solo C9 non basta, perché la capacità del modulo resta.

### FIN-004 — P2: rotazioni e origini della CPL da verificare nell'anteprima JLC

**Fatti.**

- La [CPL](../../../../hardware/policlock-main/policlock-main-cpl-jlcpcb.csv) riporta le rotazioni native di KiCad, senza correzioni per JLC. Le parti orientate sono:
  - U1 SOT-23-6 a 90°;
  - U2 SOT-23-5 a 0°;
  - Q1 SOT-23 a 90°;
  - U3 a −90°;
  - J1 a 0°.
- **U3**: l'impronta viene da **C2838502** (ESP32-C3-MINI-1-N4), non dal codice montato C41349510. La sua origine è il **centro delle piazzole**, (36,46; 27,36). Il centro del corpo, antenna compresa, sta 2,70 mm più in là lungo l'asse lungo (courtyard x 130,835–147,485 mm).
- **J1**: l'origine coincide con il centro del corpo F.Fab (133,66; 136,70).
- I termini JLC dicono: "For SMD parts, please check the placement and polarity in 2D production file". La responsabilità del controllo resta al cliente.

**Rischio.** Fonti della comunità indicano spesso uno scarto di 180° fra le impronte KiCad della famiglia SOT-23 e la libreria JLC, ma avvertono di non applicarlo a occhio a tutta la famiglia:

- [forum KiCad](https://forum.kicad.info/t/placement-rotations-am-i-missing-something/38833);
- [KiKit, nota JLCPCB](https://yaqwsx.github.io/KiKit/v1.3/fabrication/jlcpcb).

Un modulo spostato di 2,7 mm o un SOT-23 ruotato sarebbero difetti di assemblaggio.

**Proposta.** All'ordine, controllare **ogni** parte nell'anteprima 2D/3D di JLC: pin 1 di U1/U2/Q1, posizione dell'antenna di U3 sopra l'intaglio, apertura di J1 verso il bordo inferiore. Correggere solo dove serve, caricando una CPL corretta, e annotare le correzioni in `docs/12`, così da poterle ripetere. Non modificare la CPL a priori.

### FIN-005 — P2: testi della serigrafia del retro sotto il minimo JLC

**Fatto.** I 17 testi di B.Silkscreen sono alti **0,8 mm**, con tratto da 0,15 mm: SHT40, RTC, BTN, USB, "DISPLAY 1=VCC", TP1…TP11 con il nome della rete e "PoliClock main rev 0.2" a 0,9 mm. Si trovano nel PCB dalla riga 12123 circa.

La [pagina delle capacità JLC](https://jlcpcb.com/capabilities/pcb-capabilities) indica come altezza minima "40 mil (1.0mm)" e avverte che sotto quel valore i caratteri sono illeggibili. Il DRC passa perché `min_text_height` nel [.kicad_pro](../../../../hardware/policlock-main/policlock-main.kicad_pro) riga 153 vale 0,8 mm.

Queste etichette servono al proprietario per il bring-up (TP6 EN, TP11 IO9) e per riconoscere J3/J4/J5, che sul lato superiore non hanno nomi.

**Proposta.** Portare i testi del retro a 1,0 mm, accorciando le etichette dove serve spazio, e `min_text_height` a 1,0 mm. È una modifica della serigrafia: va fatta prima dei Gerber. Le linee di serigrafia delle impronte standard sono da 0,12 mm (JLC: minimo 0,15 mm): vedi FIN-007.

### FIN-006 — P2: manca la procedura di esportazione Gerber e forature

**Fatti.**

- `hardware/scripts/esporta.py` non genera Gerber né forature, e va bene così fino all'approvazione.
- Le impostazioni di stampa salvate nel PCB (righe 54–89) hanno `usegerberextensions no` e `subtractmaskfromsilk no`.
- J1 ha **asole metallizzate** di 0,6 × 1,7 e 0,6 × 1,2 mm. Le esportazioni per JLC le scrivono di solito nel file di foratura come fresature, e un'impostazione sbagliata le trasforma in fori tondi.

**Proposta.** Prima di generare i Gerber, scrivere e salvare la procedura `kicad-cli pcb export gerbers` / `export drill` con le impostazioni della guida JLC per KiCad in vigore all'ordine (strati, formato Excellon in mm, fori PTH/NPTH, modalità delle asole, origine). Poi controllare l'esito in un visualizzatore Gerber e nell'anteprima JLC: le asole di J1, il contorno con l'intaglio, i fiducial, l'assenza di serigrafia fuori bordo. Si può fare con uno script a parte che parte solo con un flag esplicito, mantenendo il vincolo "nessun Gerber senza approvazione".

### FIN-007 — P3: regole DRC di KiCad non allineate a tutti i minimi JLC letti oggi

Confronto fra la [pagina delle capacità JLC](https://jlcpcb.com/capabilities/pcb-capabilities) (2 strati, 1 oz, letta oggi) e il progetto ([.kicad_pro](../../../../hardware/policlock-main/policlock-main.kicad_pro) righe 143–157, classi di rete Default e Power, `.kicad_dru`):

| Voce | JLC (oggi) | Regola KiCad | Valore sulla scheda | Esito |
|---|---|---|---|---|
| Pista / distanza | 0,10 / 0,10 mm | pista ≥ 0,15; distanza 0,15 nelle classi di rete (minimo scheda 0,10) | piste ≥ 0,15; piazzole J1 a ≥ 0,20 | OK con margine |
| Via (foro/diametro) | 0,15 / 0,25 mm; diametro ≥ foro + 0,1 (0,15 preferito) | 0,3 / 0,6 | 28 × 0,6/0,3, 14 × 0,7/0,35, 2 × 0,6/0,35 | OK |
| Anello delle piazzole PTH | **≥ 0,18 assoluto**, 0,25 raccomandato | `min_via_annular_width` 0,1 (vale anche per le piazzole) | J1 asole 0,20; JST 0,225; J2 0,35; H1/H2 1,1 | Valori OK, ma la regola non protegge sotto 0,18 |
| Foro PTH-pista | 0,28 min, 0,35 raccomandato | `min_hole_clearance` 0,3 | — | OK, sotto il raccomandato |
| Foro-foro | 0,2 (vie), 0,45 (piazzole) | 0,25 | asole di J1 a 2,7 mm l'una dall'altra | OK |
| Rame-bordo | 0,2 | 0,3 più una fascia di 0,45 mm senza piste e vie | — | OK |
| Asole metallizzate | larghezza ≥ 0,5; lunghezza ≥ 2 × larghezza | — | 0,6 × 1,2 (al limite di 2×) e 0,6 × 1,7 | OK, al limite |
| Foro NPTH | ≥ 0,5 | — | pioli di J1 Ø 0,65 | OK |
| Diga di solder mask | ≥ 0,10 (verde) | maschera 1:1 | spazio minimo fra piazzole J1 0,20 | OK |
| Serigrafia: testo / tratto | 1,0 mm / 0,15 mm | 0,8 / 0,08 | testi 0,8 (FIN-005); linee delle impronte 0,12 | **Non conforme** |

**Proposta.** Aggiungere a `.kicad_dru` una regola per l'anello delle piazzole PTH ≥ 0,18 mm e portare il testo della serigrafia a 1,0 mm. Valutare se ingrossare a 0,15 mm le linee di serigrafia delle impronte (sono quelle della libreria KiCad: JLC di solito le stampa, ma restano sottili). Non serve toccare piste e vie.

### FIN-008 — P3: cucitura dei piani GND e piazzola termica del modulo

**Fatti.**

- Ci sono **6 vie GND** in tutta la scheda, a (33,36; 28,57), (33,23; 14,78), (23,22; 8,73), (31,0; 19,45), (31,62; 30,6) e (26,22; 5,93) mm dall'angolo in alto a sinistra.
- F.Cu e B.Cu si collegano anche tramite i piedini GND a foro passante (J1 ×4, J2.2, J3.1, J4.1, J5.2, H1, H2).
- La piazzola termica del modulo (pin 49, griglia 3 × 3 di quadrati da 1,45 mm) **non ha vie**.

Le [linee guida Espressif](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32c3/pcb-layout-design.html) chiedono di "place ground vias in the gaps" della EPAD e "dense ground vias … near the antenna".

**Rischio.** È basso con la radio spenta (`DEC-012`) e una dissipazione di circa 0,1 W. Riguarda di più la qualità del riferimento per USB e SPI e una futura V2 con Wi-Fi.

**Proposta (facoltativa, prima dei Gerber).** Aggiungere vie 0,6/0,3 negli spazi della griglia termica e una cucitura lungo il contorno e vicino all'intaglio. Non toccare la zona vietata `usb_coppia_retro` né le piste bloccate di `DEC-041`. Dopo, rieseguire il DRC.

### FIN-009 — P3: incoerenze fra documentazione e PCB

Fatti osservati:

- **Larghezze delle alimentazioni**: [docs/02](../../../02-architettura-hardware.md) §3.2 e [hardware/README](../../../../hardware/README.md) dicono "alimentazioni 0,4 mm". Nel PCB +3V3, +5V, VBUS, 5V_LDO e 3V3_DISP hanno anche tratti da 0,30 mm e GND da 0,24 mm. Elettricamente basta: le correnti sono sotto 0,2 A. La classe di rete non è un vincolo DRC.
- **Vie**: 2 vie 0,6/0,35 su 3V3_DISP non corrispondono né alla classe Default (0,6/0,3) né alla Power (0,7/0,35).
- **C9**: [docs/12](../../../12-selezione-componenti.md) riga 40 lo colloca "vicino a J2". Dopo `DEC-043` è a 18,4 mm dal pin 1 di J2 (C10 a 15,2 mm), accanto a Q1. Va bene come bulk all'uscita dell'interruttore; va corretto il testo.
- **"0,10 mm fra le piazzole USB-C"** (docs/02, hardware/README): l'impronta KiCad attuale ha piazzole a ≥ 0,20 mm e la classe impone 0,15 mm ovunque. Il valore è un residuo dell'impronta EasyEDA scartata.
- **Classi di rete**: nel .kicad_pro (righe 571 e 575) restano i pattern `*LCD_LEDK` e `*BL_D` di reti che non esistono più.
- **BOM JLC**: il commento "0Ω" è in UTF-8 senza BOM. JLC abbina per codice LCSC; potrebbe solo mostrare caratteri strani nel commento.

**Proposta.** Allineare i testi al PCB e togliere i pattern inutili quando si rimette mano al progetto. Nessuna modifica al rame è necessaria.

### FIN-010 — P3: linee che escono dalla scheda senza protezione

**Fatti.** BTN_USER (IO3) va dal JST J5 al pulsante remoto con un cavo, e sulla scheda corre per circa 72 mm. La protezione è solo R22 10 kΩ / C8 100 nF. SDA/SCL/3V3_EXT escono su J3/J4 verso i moduli. Non ci sono TVS né resistenze in serie: l'ESD è protetto solo sulla USB (U1).

**Rischio.** È basso per un oggetto da scrivania al chiuso. Il pulsante, però, è la parte che si tocca.

**Proposta (facoltativa).** Valutare una resistenza da 1 kΩ in serie fra J5.1 e IO3: la rete RC resta valida. Altrimenti accettare il rischio in modo esplicito.

### FIN-011 — P3: impronta JST PH non riconfrontata con il disegno JST

**Fatto.** J3–J5 usano l'impronta standard di KiCad `JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical`: fori Ø 0,75 mm, piazzole 1,2 × 1,75 mm, passo 2,0 mm. Il [PDF JST della serie PH](https://www.jst-mfg.com/product/pdf/eng/ePH.pdf) è cifrato e non è stato letto in questa revisione. La libreria KiCad è una fonte affidabile, ma non sostituisce il disegno.

**Proposta.** Il proprietario ha già i connettori: stampare il layout in scala 1:1 (o usare la prima scheda nuda) e provare l'innesto di un B4B-PH-K-S e dell'header. In alternativa, confrontare con il disegno JST.

## 4. Regole JLCPCB e produzione

### 4.1 Fabbricazione

Tutti i valori della scheda rispettano i minimi letti oggi (tabella di FIN-007). Le regole impostate in KiCad sono uguali o più severe dei minimi JLC per piste, distanze, vie, fori e bordo. Fanno eccezione la serigrafia (FIN-005) e l'anello delle PTH, che non ha una regola dedicata. Lo spessore di 1,6 mm è compatibile anche con l'Economic.

### 4.2 Assemblaggio

- **Lato unico**: tutte le 32 parti JLC sono sopra; sul retro ci sono solo test point nudi (esclusi), legenda e piedini THT. Conforme.
- **Corpo-bordo ≥ 2,5 mm** ([termini](https://jlcpcb.com/help/article/Terms-and-Conditions-of-JLCPCB-Assembly-Service): "must be equal or greater than 2.5mm"): PASS per tutte le parti JLC, tranne le eccezioni dichiarate J1 (a bordo, guscio 0,4 mm oltre) e U3 (sopra l'intaglio). Da far accettare alla DFM e da rivedere con la scelta dei bordi tecnici (FIN-001).
- **Fiducial**: tre da 1 mm con apertura della maschera di 2 mm e zona vietata di 3 × 3 mm, in posizione asimmetrica (FID1 3,5/7,5; FID2 16/28; FID3 46/9 mm dall'angolo in basso a sinistra). Con lo Standard JLC mette i propri fiducial sui bordi tecnici; quelli sulla scheda restano utili.
- **J2–J5 fuori dall'assemblaggio** (`DEC-043`): impronte a foro passante con attributo "escluso dai file di posizionamento", campo `Montaggio`, nessun LCSC; assenti da BOM JLC e CPL, presenti nella BOM completa. Conforme. I loro fori sono metallizzati e coperti dalle regole di fabbricazione.
- **BOM** (`Comment, Designator, Footprint, LCSC Part #, Qty`) e **CPL** (`Designator, Mid X, Mid Y, Layer, Rotation`, mm, origine in basso a sinistra): formato JLC corretto; contenuto coerente con il PCB. Rotazioni: FIN-004.

### 4.3 Codici LCSC (pagine `jlcpcb.com/partdetail`, 2026-11-08)

| LCSC | Parte | Rif. | Libreria | Tipo PCBA | Magazzino |
|---|---|---|---|---|---:|
| C41349510 | ESP32-C3-MINI-1-H4X | U3 | Extended | **Standard Only**, radiografia richiesta | 4 805 |
| C165948 | HRO TYPE-C-31-M-12 | J1 | Extended | Economic e Standard | 317 984 |
| C2977522 | BHFUSE BSMD0805-050-12V | F1 | Extended | Economic e Standard | 58 850 |
| C7519 | USBLC6-2SC6 | U1 | Extended | Economic e Standard | 23 494 |
| C404027 | TLV75533PDBVR | U2 | Extended | Economic e Standard | 93 975 |
| C15849 | CL10A105KB8NNNC 1 µF | C1, C7 | Basic | Economic e Standard | 12 929 773 |
| C19666 | CL10A475KO8NNNC 4,7 µF | C2 | Basic | Economic e Standard | 3 835 848 |
| C19702 | CL10A106KP8NNNC 10 µF | C3, C5, C9 | Basic | Economic e Standard | 10 291 320 |
| C14663 | CC0603KRX7R9BB104 100 nF | C4, C6, C8, C10 | Basic | Economic e Standard | 34 057 897 |
| C15127 | AO3401A | Q1 | Basic | Economic e Standard | 1 773 123 |
| C23186 | 0603WAF5101T5E 5,1 kΩ | R1, R2 | Basic | Economic e Standard | 20 326 582 |
| C21189 | 0603WAF0000T5E 0 Ω | R3, R4, R5, R21 | Basic | Economic e Standard | 19 075 860 |
| C25804 | 0603WAF1002T5E 10 kΩ | R6, R7, R15, R22 | Basic | Economic e Standard | 47 545 179 |
| C23345 | 0603WAF220JT5E 22 Ω | R8, R9 | Basic | Economic e Standard | 5 976 206 |
| C21190 | 0603WAF1001T5E 1 kΩ | R16 | Basic | Economic e Standard | 27 014 507 |
| C25803 | 0603WAF1003T5E 100 kΩ | R17 | Basic | Economic e Standard | 16 148 758 |
| C23162 | 0603WAF4701T5E 4,7 kΩ | R19, R20 | Basic | Economic e Standard | 15 968 211 |

Nessun codice risulta a fine produzione o non raccomandato. 5 Extended (come in `docs/12`), 12 Basic. Le scorte cambiano ogni giorno: ricontrollarle all'ordine.

## 5. Parti confermate corrette

### 5.1 Schema (netlist esportata)

- **USB-C e alimentazione**:
  - VBUS (A4, A9, B4, B9) → F1 PTC 0,5 A → +5V;
  - CC1 (A5) e CC2 (B5) con 5,1 kΩ ciascuno verso GND (R1, R2);
  - SBU A8/B8 non collegati; schermo a GND;
  - U1 USBLC6-2SC6: pin 1/6 su USB_DN_C, 3/4 su USB_DP_C, 2 a GND, 5 a +5V, come nel [datasheet ST](https://www.st.com/resource/en/datasheet/usblc6-2.pdf).
- **LDO**:
  - +5V → R5 0 Ω → 5V_LDO, con C2 4,7 µF (C19666) e U2 IN (pin 1) + EN (pin 3);
  - pin 2 a GND, pin 4 non collegato, pin 5 su +3V3 con C3 10 µF e C4 100 nF (pinout DBV del TLV755P);
  - C1 da 1 µF su +5V: totale su VBUS 5,7 µF nominali, come `DEC-042`;
  - distanze dai pin: C2 2,39 mm, C3 2,38 mm, C4 2,24 mm.
- **ESP32-C3-MINI-1-H4X** (datasheet v2.2, tab. 3-1):
  - GND sui pin 1, 2, 11, 14, 36–53; 3V3 sul pin 3, con C5 10 µF a 3,74 mm e C6 100 nF a 2,37 mm;
  - EN (8) con R6 10 kΩ e C7 1 µF, TP6;
  - IO2 (5) = SDA con R19 4,7 kΩ; IO8 (22) = SCL con R20 4,7 kΩ; IO9 (23) con R7 10 kΩ e TP11. Strapping secondo la tab. 4-1: IO2/IO8 di default flottanti, quindi servono i pull-up;
  - IO18 (26) = D-, IO19 (27) = D+ tramite R4/R3 0 Ω;
  - IO4 DC, IO5 RST, IO6 SCLK (FSPICLK), IO7 MOSI (FSPID), IO10 CS (FSPICS0), R8/R9 22 Ω su SCLK/MOSI;
  - IO20/RXD0 (30) = DISP_EN_N; IO21/TXD0 (31) su TP5; IO0/IO1 su TP9/TP10;
  - tutti gli NC isolati.
- **Display** (`DEC-034`):
  - Q1 AO3401A: G = pin 1 (DISP_G), S = pin 2 (+3V3), D = pin 3 (3V3_DISP);
  - R17 tiene il gate alto, quindi il display resta spento al reset; con IO20 basso il gate va a circa 0,03 V (VGS circa −3,3 V);
  - J2: 1 3V3_DISP, 2 GND, 3 SCLK, 4 MOSI, 5 DC, 6 CS, 7 RST; R15 tira LCD_RST verso 3V3_DISP.
- **I²C e pulsante**:
  - J3/J4: 1 GND, 2 3V3_EXT (tramite R21 0 Ω), 3 SDA, 4 SCL, nello stesso ordine del connettore Qwiic/STEMMA QT;
  - J5: 1 BTN_USER (IO3, R22 10 kΩ, C8 100 nF), 2 GND, 3–4 non collegati.
- **Fuori perimetro**: nessuna batteria, nessun touch, nessun circuito radio aggiuntivo (`DEC-023`, `DEC-034`, `DEC-012`). Il modulo ha l'antenna integrata, che resta inutilizzata.

### 5.2 PCB

- **Sagoma**: 50 × 40 mm con intaglio da x = 42,16 mm a destra, fino a 20,18 mm dal bordo superiore; 2 strati; componenti solo sopra (`DEC-030`, `DEC-036`).
- **Coppia USB**: identica a `4fb9200` (36 elementi bloccati) e conforme a `DEC-041`; retro vietato sotto la coppia.
- **Antenna** (`DEC-036`, Espressif):
  - nella fig. 11-1 del datasheet il modulo è lungo 16,6 mm e la zona antenna comincia 11,2 mm dal lato dei pin;
  - con il corpo da x = 130,84 mm, la zona antenna parte da circa 142,0–142,1 mm e l'intaglio comincia a 142,16 mm: al massimo circa 0,1 mm di laminato **senza rame** sotto l'inizio dell'antenna. La copertura GND si ferma ≥ 0,3 mm prima del bordo;
  - fascia vietata di 3 mm sotto l'intaglio su entrambi gli strati; modulo in angolo, mai al centro della scheda.
  - **Rischio non misurato**: le linee guida chiedono 15 mm liberi nella custodia, cosa che conta solo con la radio attiva (V2).
- **Alimentazioni**: piste da 0,3–0,4 mm, adeguate alle correnti previste. GND solido verso U2 sulla copertura superiore.
- **Termica dell'LDO**: stima di `docs/12` circa 0,14 W, cioè +14…32 °C: è un rischio da misurare (`VT-PWR-002`), non un difetto.
- **Vie**: tutte coperte dalla maschera su entrambi i lati. Le 4 vie di segnale sotto il modulo (EN, IO1, I2C_SDA, DISP_EN_N) rispettano la distanza DRC di 0,15 mm dalle sue piazzole (la più vicina, EN, a circa 0,16 mm).
- **J1**:
  - 4 asole metallizzate del guscio a GND (anello 0,20 mm) e 2 pioli NPTH Ø 0,65 mm;
  - fori M2 H1/H2 ai lati, che scaricano lo sforzo d'inserimento;
  - spazio fra piazzole ≥ 0,20 mm.
- **J2–J5 a mano** (`DEC-043`):
  - piazzole PTH con pin 1 quadrato (J2) o rettangolare arrotondato (J3–J5);
  - collegamento GND a raggi (2 raggi da 0,3 mm), comodo per la saldatura a mano;
  - il test point più vicino ai piedini THT è TP1, a 3,4 mm dal pin 4 di J5; nessun conflitto sul retro;
  - nessuna parte sotto il corpo plastico dell'header (courtyard senza sovrapposizioni).
- **`.kicad_dru`**: l'unica regola ignora la distanza serigrafia-bordo solo per gli elementi di J2 rispetto a Edge.Cuts. Il DRC conferma che non nasconde altro: 0 avvisi di serigrafia su rame o sovrapposta.
- **`verifica_meccanica_pcb.py`**: PASS. Applica la regola dei 2,5 mm alle sole parti in CPL e controlla comunque i courtyard di J2–J5.

### 5.3 Coerenza

Requisiti, decisioni, schema, PCB, BOM e CPL sono coerenti, tranne:

- FIN-001: "Economic" contro "Standard Only";
- FIN-009: testi della documentazione.

I test del [piano di verifica](../../../07-piano-verifica.md) restano tutti NOT_RUN: questa revisione non li cambia.

## 6. Cosa manca prima di generare i Gerber

1. **FIN-001**: decisione del proprietario su assemblaggio Standard e bordi tecnici (chi li aggiunge, lati sinistro/destro), da registrare come nuova `DEC` che aggiorna `DEC-040`, e costi aggiornati in `docs/08`.
2. **FIN-002**: revisione a vista in KiCad del layout dopo `DEC-043`, registrata in `docs/10` §10.
3. Decidere **prima dei Gerber** le modifiche che toccano rame o serigrafia:
   - FIN-003: piazzola per il soft-start di Q1, oppure misura su banco;
   - FIN-005: serigrafia a 1,0 mm;
   - FIN-008: vie di cucitura, facoltativo.

   Dopo ogni modifica rieseguire ERC, DRC completo e controllo meccanico.
4. **FIN-006**: procedura Gerber/forature documentata e controllata in un visualizzatore (asole di J1).
5. **Approvazione esplicita del proprietario** per generare i Gerber.

Restano gate dell'**ordine**, non dei Gerber:

- `OPEN-028` (studio volumetrico, con la luce sotto la scheda per i piedini THT);
- `OPEN-016` (modulo display ricevuto);
- `OPEN-021` (SPI sul cavetto);
- DFM JLC con le eccezioni J1/U3;
- anteprima rotazioni (FIN-004);
- scorte ricontrollate all'ordine.

`OPEN-028` può ancora cambiare la sagoma o la posizione dei connettori: se lo studio volumetrico è vicino, conviene chiuderlo prima dei Gerber.

## 7. Evidenze e riproduzione

File in questa cartella:

- [erc.rpt](erc.rpt), [erc.json](erc.json): ERC con tutte le severità;
- [drc.rpt](drc.rpt), [drc.json](drc.json): DRC con tutte le severità, tutte le piste, parità, zone ricalcolate;
- [verifica-meccanica.json](verifica-meccanica.json): esito di `verifica_meccanica_pcb.py`;
- [audit_finale.py](audit_finale.py), [audit-finale.json](audit-finale.json): audit in sola lettura (contorno, footprint, piazzole THT, reti, vie, zone, test point).

Comandi dalla root del repository (PowerShell):

```powershell
$kicad = 'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe'
$py = 'C:\Program Files\KiCad\10.0\bin\python.exe'
$out = 'docs/revisioni/2026-11-08/revisione-finale'
& $kicad sch erc --severity-all --exit-code-violations --format json -o "$out/erc.json" hardware/policlock-main/policlock-main.kicad_sch
& $kicad pcb drc --severity-all --all-track-errors --schematic-parity --refill-zones --exit-code-violations --format json -o "$out/drc.json" hardware/policlock-main/policlock-main.kicad_pcb
& $py hardware/scripts/verifica_meccanica_pcb.py --output "$out/verifica-meccanica.json" hardware/policlock-main/policlock-main.kicad_pcb
& $py "$out/audit_finale.py"
git status --short   # se kicad-cli ha riscritto il .kicad_pro: git checkout -- hardware/policlock-main/policlock-main.kicad_pro
```

Le pagine JLC e le scorte sono state lette il 2026-11-08 e vanno ricontrollate all'ordine. Nessuna prova su hardware fisico è stata eseguita: le voci "rischio" e "stima" non sono misure.
