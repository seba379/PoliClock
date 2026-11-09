# Terza revisione finale pre-Gerber — scheda principale PoliClock rev 0.2

**Data:** 2026-11-09 · **Revisore:** Claude (sessione di revisione, sola lettura del progetto) · **Base:** `edcef25` (ramo `claude/hardware-schematic-4ff868`), portato nel ramo `claude/revisione-finale-ea91f4` con un fast-forward da `4780565`. KiCad 10.0.6.

Cambiamenti rispetto alla [seconda revisione](../../2026-11-08/revisione-finale-2/README.md) (`810e50f` su `a2a62a3`):

- `4780565`: chiusura delle riserve R2-001…R2-007. Solo documenti e testo della checklist di `esporta_gerber_jlc.py`; il PCB è identico byte per byte a quello di `a2a62a3`.
- `21f998c`, dopo la revisione esterna ([docs/10](../../../10-decisioni-aperte.md) §15):
  - `DEC-046`: EPAD di U3 senza vie;
  - `DEC-047`: linguette del guscio di J1 saldate a mano;
  - CPL alternativa con U3 al centro del corpo.
- `edcef25` (`DEC-049`): J2 1×8 con il pin 8 = BUSY verso IO1 attraverso R23 1 kΩ; J2 spostato di 2,54 mm a sinistra; reti di J2 e DISP_BUSY risbrogliate.

Non ho modificato nessun file di progetto: schema, PCB, `.kicad_pro`, `.kicad_dru`, librerie, script, BOM e CPL sono come in `edcef25`. `git status` è pulito fuori da questa cartella (`kicad-cli` non ha riscritto il `.kicad_pro`). Non ho generato Gerber: `esporta_gerber_jlc.py` è stato solo letto. Nessun push.

## 1. Esito

### **PRONTO CON RISERVE**

Nessun rilievo **P1**. Il progetto rispetta le decisioni `CONF` (`DEC-001`…`DEC-049`), i datasheet Espressif e le regole JLCPCB lette oggi. Controlli superati:

- ERC: 0 violazioni.
- DRC con tutte le severità, tutte le piste, zone ricalcolate e parità schema ↔ PCB: 0 violazioni, 0 connessioni aperte, 0 problemi di parità.
- Controllo meccanico: PASS. J1 è l'unica eccezione; margine minimo U3 a 2,99 mm, R23 a 6,54 mm.
- Coppia USB: i 36 elementi (piste e vie) sono **identici** a quelli di `4780565`, tutti bloccati; lunghezze invariate.
- Zona antenna: nessun rame, pista, via o riempimento dentro la zona vietata di U3, su F.Cu e B.Cu.
- `DEC-049`: GPIO1 è adatto a BUSY (verificato sul datasheet ESP32-C3 v2.4); R23 e il pull-down interno sono corretti.
- `DEC-046`: EPAD collegata a GND sul rame superiore, 9 aperture di pasta (52 % della piazzola), nessuna via.
- I 18 codici LCSC sono "Economic and Standard", a magazzino, senza radiografia.
- BOM JLC (18 righe), CPL (34 parti) e CPL alternativa coincidono con il PCB; le due CPL differiscono solo per la X di U3 (34,41 → 37,51 mm), che corrisponde al centro del corpo F.Fab.

Una riserva da decidere **prima dei Gerber**:

- **R3-001 (P2).** Il percorso di DISP_BUSY chiude in un'isola il piano GND del retro sotto U3. Insieme a `DEC-046`, il modulo non ha più un collegamento diretto al piano principale del retro. Non è un errore DRC e non è misurabile qui, ma peggiora la massa del modulo rispetto al layout approvato a vista. La correzione costa poche vie o un tratto di sbroglio. Va fatta, oppure accettata dal proprietario in modo esplicito.

I P3 (R3-002…R3-005) sono rischi senza effetto in V1 o pulizia della documentazione.

Restano aperti i gate **dell'ordine** già noti:

- `OPEN-028` (studio volumetrico), che può ancora cambiare sagoma o connettori;
- `OPEN-016` (modulo display ricevuto);
- `OPEN-021` (SPI sul cavetto);
- DFM JLC per J1;
- scorte da ricontrollare all'ordine;
- prova 1:1 dei JST PH e dell'header (FIN-011), consigliata da `docs/12` §6 **prima dei Gerber**.

| ID | Priorità | Titolo | Tipo |
|---|---|---|---|
| R3-001 | P2 | DISP_BUSY chiude in un'isola il piano GND del retro sotto U3; con la EPAD senza vie (`DEC-046`) il modulo arriva al piano principale del retro solo attraverso il rame superiore e due vie in serie | Fatto osservato + rischio non misurato |
| R3-002 | P3 | DISP_BUSY corre per circa 18 mm sul retro a 0,23 mm dalla zona antenna e sotto la fila superiore di piazzole di U3 | Fatto osservato; impatto RF solo in V2 |
| R3-003 | P3 | Isola GND del retro di 249 mm² (zona J2/passivi) collegata da una sola via; c'era già, con 195 mm², su `a2a62a3` | Fatto osservato (non segnalato nella seconda revisione) |
| R3-004 | P3 | Firmware: manca il vincolo "clock RTC lento sempre interno" (GPIO1 è anche XTAL_32K_N) | Documentazione |
| R3-005 | P3 | Residui nella documentazione dopo `DEC-046`/`DEC-049` | Fatto osservato |

## 2. Controlli eseguiti

| Controllo | Comando / fonte | Risultato |
|---|---|---|
| Base | `git merge --ff-only claude/hardware-schematic-4ff868` | Fast-forward `4780565` → `edcef25`, nessun conflitto |
| ERC | `kicad-cli sch erc --severity-all --exit-code-violations --format json` (anche `report`) | **0 violazioni**, codice d'uscita 0 → [erc.rpt](erc.rpt), [erc.json](erc.json) |
| DRC | `kicad-cli pcb drc --severity-all --all-track-errors --schematic-parity --refill-zones --exit-code-violations --format json` (anche `report`) | **0 / 0 / 0**, codice d'uscita 0 → [drc.rpt](drc.rpt), [drc.json](drc.json). Controlli ignorati: gli stessi tre di prima (pista non centrata sulla via, profili di accordatura, filtri footprint). Zone ricalcolate solo in memoria |
| Controllo meccanico | `python.exe hardware/scripts/verifica_meccanica_pcb.py --output …/verifica-meccanica.json` | **PASS** → [verifica-meccanica.json](verifica-meccanica.json). Unica eccezione J1. Margini minimi: U3 2,99, U2 5,05, R23 6,54, C2 6,65 mm. Courtyard di J2–J5 senza elementi fuori |
| Audit geometrico | [audit_finale.py](audit_finale.py) (copia dello script della seconda revisione) → [audit-finale.json](audit-finale.json) | 54 footprint, 62 vie (49 × 0,6/0,3, 12 × 0,7/0,35, 1 × 0,6/0,35), circa 1166 mm di piste |
| Netlist | `kicad-cli sch export netlist` (in una cartella temporanea) | J2.8 → `DISP_BUSY_C` → R23 → `DISP_BUSY` → U3.17 (IO1) + TP10; `/MCU/IO0` → U3.18 + TP9; nessun altro nodo |
| Confronto con `4780565` | Script pcbnew in sola lettura (scratchpad) | Coppia USB identica (36 elementi), 41 elementi bloccati in entrambi; vie 60 → 62; piste 1110,7 → 1166,3 mm |
| Piani GND | Riempimento in memoria, isole e vie per isola | §3, R3-001 e R3-003 |
| Zona antenna | Distanza di ogni pista, via e piazzola dalla zona vietata dell'impronta di U3 (141,51…152,51 × 96,5…124,5 sul foglio, F.Cu e B.Cu, tutto vietato) | Riempimenti nella zona: 0,000 mm². Più vicini: DISP_BUSY (B.Cu) e LCD_CS (F.Cu) a 0,23 mm, fuori dalla zona |
| Serigrafia | Audit dei testi | 17 testi su B.Silkscreen, tutti 1,0 mm / 0,15 mm |
| BOM/CPL ↔ PCB | Confronto e `diff` delle due CPL | §6 |
| Codici LCSC | Pagine `jlcpcb.com/partdetail/<codice>` nel browser, oggi | §7.3 |
| Pagine JLC | [capacità PCB](https://jlcpcb.com/capabilities/pcb-capabilities), [capacità assemblaggio](https://jlcpcb.com/capabilities/pcb-assembly-capabilities), [termini dell'assemblaggio](https://jlcpcb.com/help/article/Terms-and-Conditions-of-JLCPCB-Assembly-Service) ("Last updated on Sep 09, 2026"), [guida Gerber per KiCad 8](https://jlcpcb.com/help/article/how-to-generate-gerber-and-drill-files-in-kicad-8) ("Last updated on Sep 09, 2026") | §7 |
| Datasheet | [ESP32-C3 Series v2.4](https://documentation.espressif.com/esp32-c3_datasheet_en.pdf) (scaricato oggi): tab. 2-1, 2-2, 2-7, 3-1, 5-4. [ESP32-C3-WROOM-02 v1.7](https://documentation.espressif.com/esp32-c3-wroom-02_datasheet_en.pdf): tab. 3-1, fig. 9-1 con le note, fig. 11-1 | §4, §5 |
| `git status` dopo tutti i comandi | — | Solo questa cartella non tracciata |

## 3. Rilievi nuovi

### R3-001 — P2: DISP_BUSY chiude in un'isola il piano GND del retro sotto il modulo

**Fatto.** Coordinate del foglio KiCad; tra parentesi quelle di [docs/02](../../../02-architettura-hardware.md) §3.2, con origine (100; 100).

DISP_BUSY (67,5 mm, 2 vie) parte dalla via a (125,83; 100,99), sopra la fila superiore di piazzole di U3. Sul retro:

- corre lungo y = 101,15 da x = 126 a 139,5;
- scende lungo il lato destro del modulo, x ≈ 141,1, fino a y = 121;
- torna alla via (137,38; 120,45) vicino al pin 17;
- prosegue in diagonale sotto i pin 13/14 verso TP10.

Su tre lati, insieme alle piste già presenti sotto la fila inferiore di piazzole, racchiude la zona del retro sotto il modulo.

Piano GND riempito in memoria, prima e dopo `DEC-049`:

| Strato | `4780565` (= `a2a62a3`) | `edcef25` |
|---|---|---|
| B.Cu | piano principale 1035 mm² (comprende le 4 vie della EPAD e la via (139,5; 103,5)); isola 195 mm² con 1 via; isola 0,8 mm² | piano principale **900 mm²**; isola **95,4 mm² sotto U3** (x 129,6–140,3, y 101,4–117,9) con 2 sole vie: (139,5; 103,5) e la nuova (130,6; 108,0); isola 249 mm² con 1 via; isola 0,7 mm² |
| F.Cu | principale 1193 mm² (con la EPAD); isola 37,6 mm² con U3.9 e C6.2, collegata da (139,5; 103,5) | principale 1202 mm² (con la EPAD); isola 31,7 mm² con **U3.9 (GND) e C6.2**, collegata **solo** da (139,5; 103,5) |

Dopo `DEC-046` e `DEC-049` il modulo si collega al piano GND così:

- la EPAD (pad 19) arriva al riempimento F.Cu principale con piste da 0,4 mm che escono dal lato sinistro del modulo, fino a x = 127,78. Sotto il modulo non ci sono più vie;
- il pin 9 (GND) e il GND di C6 (100 nF sul 3V3) stanno in un'isola F.Cu. Questa passa dalla via (139,5; 103,5) all'isola del retro sotto U3 e da lì, con la via (130,6; 108,0), torna al rame superiore principale. Sono **due vie in serie** attraverso un'isola;
- prima, le 4 vie della EPAD e la via (139,5; 103,5) arrivavano direttamente al piano principale del retro, sotto la coppia USB e sotto le piste del 3V3 e di EN.

**Perché conta.** Non è una violazione DRC e la scheda funziona in continua. Peggiorano però tre percorsi di ritorno:

- **3V3 ed EN**: le piste +3V3 (C5/C6 → pin 1, circa 21 mm) ed EN (27 mm) passano sul rame superiore sotto il modulo. Ora il loro piano di riferimento è un'isola di 95 mm² collegata in due punti. Aggrava R2-005, che il proprietario ha accettato con il piano continuo.
- **USB**: il ritorno della coppia USB arriva sul retro fino ai pin 13/14, ma lì il piano principale non è più collegato al GND del modulo. Le vie GND più vicine sono (128,38; 124,76) e (139,99; 127,68), a 5–9 mm. Prima c'erano le vie della EPAD, a circa 8 mm. Per USB Full Speed l'effetto è piccolo.
- **Disaccoppiamento**: C5 (10 µF) e C6 (100 nF) sono su isole diverse.

`docs/10` §16 cita la via (30,6; 8,0) come ricucitura dell'isola, ma non descrive l'effetto combinato con `DEC-046`. Gli effetti si vedrebbero solo al banco (`VT-PCB-002`: 3V3 al pin 1, EN, enumerazione USB).

**Correzione proposta**, compatibile con `DEC-041`, `DEC-045` e `DEC-046`; da fare prima dei Gerber, con un nuovo DRC 0/0/0:

1. **Preferita: sbrogliare di nuovo solo DISP_BUSY** lungo il lato sinistro di U3. Da R23 si scende fra la colonna C5/C6/R8/R9 e il modulo (x ≈ 127) fino al tratto che già esiste verso TP10, vicino a (127,74; 123,5). Così sparisce l'anello di circa 40 mm sopra e a destra del modulo, il piano del retro sotto U3 torna unito a quello principale e si risolve anche R3-002. La zona `usb_coppia_retro` e le 41 piste bloccate non si toccano.
2. **In aggiunta o in alternativa**, se a sinistra non c'è spazio: aggiungere 3–4 vie GND 0,6/0,3 mm **fuori** dalla EPAD (≥ 0,5 mm dal bordo della piazzola, coperte dalla maschera). Vanno nel riempimento F.Cu sotto il modulo, ai lati della EPAD, e collegano il rame superiore principale all'isola del retro. Aggiungerne 1–2 nell'isola F.Cu di U3.9/C6.2, verso il pin 9. `DEC-046` vieta le vie **nella** piazzola, non accanto.
3. Dopo la modifica, ricontare le isole: nessuna isola del retro sotto il modulo con meno di 3 vie; isola di U3.9 con almeno 2 vie.

Se il proprietario sceglie di non correggere, va scritto in `docs/10` come rischio accettato, accanto a R2-005, e misurato in `VT-PCB-002`.

### R3-002 — P3: DISP_BUSY corre lungo la zona antenna e sotto la fila superiore di U3

**Fatto.** Sul retro DISP_BUSY corre per circa 18 mm a x = 141,06–141,19 mm, con larghezza 0,15–0,2 mm, a **0,23 mm** dal bordo della zona vietata (141,51 mm). Corre anche per 13,5 mm a y = 101,15 sotto le piazzole 2–8 di U3. È fuori dalla zona e quindi conforme a `DEC-045`. È la stessa situazione di LCD_CS (R2-004), che oggi è a 0,23 mm. Con la radio spenta (`DEC-012`) non ha effetti in V1.

**Correzione proposta.** Si risolve con la correzione 1 di R3-001. Altrimenti aggiungere DISP_BUSY alla nota V2 della [roadmap](../../../09-roadmap.md), che oggi cita solo LCD_CS.

### R3-003 — P3: isola GND del retro di 249 mm² con una sola via

**Fatto.** Sul retro un'isola di 249 mm² (x 109–128,8, y 101,8–130,6: zona di J2, colonne dei passivi, Q1, C9) è collegata al resto del GND solo dalla via (112,4; 104,3), vicino al pin 2 di J2. C'era già su `a2a62a3`, con 195 mm², e la seconda revisione non l'ha segnalata. Sopra passano SCLK/MOSI del display (10–20 MHz) e 3V3_DISP. Il ritorno di queste linee sul retro ha un solo punto di contatto, dal lato di J2. Il limite principale resta il cavetto Dupont (`OPEN-021`), quindi l'effetto è secondario.

**Correzione proposta.** Aggiungere 2–3 vie GND nell'isola, per esempio vicino a Q1/C9 e alla colonna R8/R9, a ≥ 2,5 mm dai corpi montati da JLC. Si può fare insieme a R3-001 e poi rifare `cucitura_gnd.py`.

### R3-004 — P3: vincolo firmware sul clock RTC lento

**Fatto.** Sul chip GPIO1 è anche XTAL_32K_N (datasheet ESP32-C3 v2.4, tab. 2-1 e 2-7). Se il firmware scegliesse il quarzo esterno da 32 kHz come clock RTC lento, IO1 smetterebbe di essere un GPIO. Il default di ESP-IDF è l'oscillatore RC interno, quindi oggi va bene. [docs/04](../../../04-specifiche-firmware.md) §4 però non lo dice. Lo stesso vale per ADC1_CH1, che non va usato.

**Correzione proposta.** Una riga in `docs/04`: "sorgente del clock RTC lento: RC interno (mai `CONFIG_RTC_CLK_SRC_EXT_CRYS`/`EXT_OSC`, GPIO0/GPIO1 sono usati come GPIO)".

### R3-005 — P3: residui nella documentazione

- [docs/02](../../../02-architettura-hardware.md) §3.2, punto "In alto a destra": "EPAD con 4 vie termiche 0,3/0,7 mm". Dopo `DEC-046` la EPAD non ha vie.
- [docs/10](../../../10-decisioni-aperte.md) `CAND-022`: "JST PH e header 1×7". Ora l'header è 1×8 (`DEC-049`).
- [docs/12](../../../12-selezione-componenti.md) riga 5: "`DEC-024`…`DEC-044`". Ora le decisioni arrivano a `DEC-049`. Alla riga 25 la scorta di C2934560 è quella del 2026-11-08 (13 113): oggi è 11 626.
- `policlock-main.kicad_dru`, solo nei commenti: "header 1x7" e "vie termiche della EPAD di U3 0,20". Le regole sono corrette. Il file è di progetto e va cambiato dalla sessione hardware.
- Nel registro manca `DEC-048`: si passa da `DEC-047` a `DEC-049` senza una nota. Basta una riga ("numero non usato") per la tracciabilità.
- `DEC-046` giustifica l'assenza di vie con la nota del datasheet ("Soldering the EPAD [...] is not a must"). Però non dice che la fig. 11-1 del datasheet WROOM-02 v1.7 disegna "Via for thermal pad". Conviene scrivere che si tratta di uno scostamento voluto dal land pattern Espressif.
- La serigrafia del retro "DISP 1=VCC" può restare. Volendo può diventare "DISP 1=VCC 8=BUSY", ma è facoltativo.

## 4. `DEC-049`: BUSY su IO1

| Controllo | Esito | Evidenza |
|---|---|---|
| Funzione di GPIO1 | Corretta | WROOM-02 v1.7 tab. 3-1: pin 17 = IO1 (GPIO1, ADC1_CH1, XTAL_32K_N). C3 v2.4 tab. 2-7: GPIO1 è **Priority 2** per tutte le periferiche, cioè "can be freely used without restrictions" |
| Strapping | No | C3 v2.4 §3, tab. 3-1: gli strapping sono GPIO2, GPIO8 e GPIO9 |
| Stato al reset e dopo il reset | Corretto | C3 v2.4 tab. 2-1, pin 5 XTAL_32K_N: nessuna impostazione "At Reset" né "After Reset", cioè niente IE, WPU o WPD. Il pin flotta con l'ingresso disabilitato: niente corrente e nessun conflitto con un'uscita esterna |
| Glitch all'accensione | Nessuno | C3 v2.4 tab. 2-2: solo MTCK, MTDO, GPIO10, U0RXD e GPIO18 |
| Quarzo da 32 kHz nel modulo | Assente | WROOM-02 v1.7: nel modulo c'è solo il quarzo da 40 MHz; quello da 32,768 kHz nello schema periferico è un'opzione esterna, che su questa scheda non c'è. Vincolo firmware in R3-004 |
| Livello con R23 e pull-down | Corretto | C3 v2.4 tab. 5-4: RPD = 45 kΩ (tipico), VIH ≥ 0,75 × VDD = 2,48 V. Con R23 1 kΩ in serie il livello alto letto vale 3,3 × 45/46 ≈ 3,23 V; anche con un pull-down di 30 kΩ sarebbe 3,19 V. Corrente di ingresso ≤ 50 nA |
| Con il GC9A01 | Corretto | Pin 8 libero: IO1 legge 0 con il pull-down. `docs/04` §4 dice di ignorarlo |
| Con il display spento da Q1 | Corretto | Con un e-paper spento e IO1 in ingresso non passa corrente. Con IO1 configurato per errore come uscita alta, la corrente è al massimo (3,3 − 0,6)/1 kΩ ≈ 2,7 mA attraverso i diodi del display: innocua |
| Schema | Corretto | Netlist: J2.8 → `DISP_BUSY_C` → R23 (1k, 0603, C21190) → `DISP_BUSY` → U3.17 + TP10. IO0 resta su TP9. ERC 0 |
| Posizione di J2 | Corretta | `PinHeader_1x08_P2.54mm_Horizontal` a (107,34; 102,9), rotazione 90°: pin 1 = 3V3_DISP (quadrato) … pin 7 = LCD_RST a 122,58, pin 8 = DISP_BUSY_C a 125,12, cioè dove era il pin 7. Fori 1,0 mm, piazzole 1,7 mm (anello 0,35 mm). Courtyard senza sovrapposizioni (DRC) |
| R23 | Corretta | (125,3; 105,45), 2,55 mm sotto J2.8: il tratto `DISP_BUSY_C` è di 2,8 mm su F.Cu, quindi la resistenza protegge tutta la pista lunga lato MCU. Margine dal bordo 6,54 mm |
| Sbroglio | Funziona, con riserve | 67,5 mm, 2 vie, 0,15–0,2 mm: il tracciato è descritto in R3-001 e R3-002 |

## 5. `DEC-046`: EPAD senza vie

- **Libreria e PCB.** `PoliClock:ESP32-C3-WROOM-02` e U3 sul PCB hanno il pad 19 SMD 2,9 × 2,9 mm su F.Cu/F.Mask, con zone connection "solid", e nessuna piazzola passante. Le 4 vie della seconda revisione sono state tolte (diff di `21f998c`, script `dec046_epad.py`).
- **Pasta.** 9 aperture 0,7 × 0,7 mm a passo 1,1 mm, in una matrice 3 × 3 centrata sulla EPAD: 4,41 mm² su 8,41 mm², cioè il **52 %**. La piazzola non ha pasta propria. È coerente con la nota Espressif (fig. 9-1 del datasheet WROOM-02 v1.7: la saldatura della EPAD "is not a must", ma la quantità di pasta va dosata perché troppa pasta solleva il modulo). Senza vie la pasta non può scendere nei fori.
- **GND sul rame superiore.** La EPAD è dentro il riempimento F.Cu principale (1202 mm²). Altre piste GND da 0,4 mm la collegano verso sinistra fino a x = 127,78. Nessun problema di continuità: il problema è la mancanza di un collegamento diretto al retro, R3-001.
- **Land pattern Espressif.** Le piazzole dei pin restano quelle della fig. 11-1, già verificate nella seconda revisione. La figura mostra "Via for thermal pad": togliere le vie è uno scostamento voluto e ammesso dalla nota sulla EPAD, ma va scritto (R3-005).

## 6. BOM e CPL

- **BOM JLC** (`policlock-main-bom-jlcpcb.csv`): 18 righe nel formato `Comment, Designator, Footprint, LCSC Part #, Qty`, con la nuova riga `"1k","R23","Resistor_SMD:R_0603_1608Metric","C21190","1"`. È UTF-8 per i simboli "Ω" di R3/R4/R5/R21 e R8/R9, come nella seconda revisione.
- **BOM completa**: 20 parti. J2 compare come "Header 1x8 2,54 mm THT" con `Montaggio` = "a mano, parte del proprietario", R23 come "JLC (PCBA)".
- **CPL** (`policlock-main-cpl-jlcpcb.csv`): 34 parti nel formato `Designator, Mid X, Mid Y, Layer, Rotation`, con l'origine nell'angolo in basso a sinistra (aux origin 100; 140). R23 è a (25,30; 34,55) mm, Top, 180°. Gli altri 33 componenti sono nella stessa posizione di prima (nessuna parte montata da JLC si è mossa).
- **CPL alternativa** (`…-u3-centro-corpo.csv`): `diff` con la CPL normale dà **una sola riga**, U3 a X 34,41 → 37,51 mm, con Y 29,50 mm e rotazione −90° invariate.
  - Corpo F.Fab di U3 sul foglio: x 127,46–147,56, y 101,45–119,55 (linee da 0,1 mm comprese). Il centro è a (137,51; 110,5), cioè (37,51; 29,50) rispetto all'origine della CPL.
  - Origine dell'impronta: (134,41; 110,5), cioè il centro delle due file di piazzole, che sono a y = 101,75 e 119,25. La differenza è 3,10 mm lungo x, verso l'antenna.
  - `cpl_centro_corpo.py` usa la stessa aux origin di `esporta.py`.
  - Le due CPL sono corrette. Quale usare lo dice l'anteprima JLC: va scelta quella in cui piazzole e modulo coincidono ([docs/12](../../../12-selezione-componenti.md) §7).
- **Tabella delle rotazioni** in `docs/12` §7, confrontata con le piazzole del PCB:
  - U1: pin 1 in (132,71; 127,51), in basso a sinistra verso J1;
  - U2: pin 1 = IN in (115,86; 132,55), in alto a sinistra;
  - Q1: G in basso a sinistra, S in basso a destra, D in alto.

  Tutto corrisponde: R2-001 è chiuso.

## 7. Regole JLCPCB e produzione (pagine lette oggi, 2026-11-09)

### 7.1 Assemblaggio

[Capacità di assemblaggio](https://jlcpcb.com/capabilities/pcb-assembly-capabilities), Economic PCBA:

- montaggio su un solo lato; 2, 4 o 6 strati; spessore 0,8–1,6 mm;
- scheda singola da 10 × 10 a 470 × 500 mm;
- bordi tecnici e fiducial "Not necessary";
- package minimo 0402, passo minimo dei pin dei CI 0,4 mm;
- radiografia solo per alcune parti (per esempio BGA).

La scheda (50,5 × 41,5 × 1,6 mm, 2 strati, un lato) rientra. Lo Standard chiede invece una scheda da almeno 70 × 70 mm.

[Termini dell'assemblaggio](https://jlcpcb.com/help/article/Terms-and-Conditions-of-JLCPCB-Assembly-Service) ("Last updated on Sep 09, 2026"), "Notes on DFM" punto 3: la distanza fra il corpo dei componenti e il bordo della scheda deve essere "equal or greater than 2.5mm". Nel progetto:

- è rispettata da tutte le parti montate da JLC tranne **J1**, l'unica eccezione di `DEC-045`, da far accettare nella DFM;
- J2–J5 sono saldati a mano e non rientrano nella regola;
- il controllo meccanico la verifica in modo automatico.

### 7.2 Fabbricazione

[Capacità PCB](https://jlcpcb.com/capabilities/pcb-capabilities), 2 strati:

| Regola JLC | Nella scheda |
|---|---|
| Via 0,15/0,25 mm minimo | Vie 0,6/0,3, 0,7/0,35 e 0,6/0,35 mm |
| Anello PTH: minimo assoluto 0,18 mm, raccomandato 0,25 mm | Regola nel `.kicad_dru`; asole di J1 0,20 mm, header J2 0,35 mm |
| Distanza PTH-pista ≥ 0,28 mm (0,35 raccomandata) | Rispettata |
| Asole metallizzate: larghezza ≥ 0,5 mm, lunghezza ≥ 2 × la larghezza | J1: 0,6 × 1,7 e 0,6 × 1,2 mm, quindi al limite di 2× nelle asole corte, come nella seconda revisione |
| Fori NPTH ≥ 0,50 mm | Pioli di J1 0,65 mm |
| Rame dal bordo fresato ≥ 0,2 mm | Progetto 0,3 mm |
| Serigrafia: testi ≥ 1,0 mm, tratto ≥ 0,15 mm | 17 testi sul retro a 1,0/0,15 mm |
| Ponte di maschera: 0,10 mm (verde) | Tabella di `docs/12` §7 |

[Guida Gerber per KiCad 8](https://jlcpcb.com/help/article/how-to-generate-gerber-and-drill-files-in-kicad-8): "Last updated on Sep 09, 2026", la stessa versione già confrontata con `esporta_gerber_jlc.py` nella seconda revisione. Lo script è cambiato solo nella checklist: contorno 50,5 × 41,5 mm, zona antenna, EPAD senza vie, 17 testi del retro.

### 7.3 Codici LCSC

Pagine `jlcpcb.com/partdetail/<codice>` lette oggi: tutte riportano "PCBA Type: **Economic and Standard**", nessuna chiede la radiografia (la pagina di C2934560 non menziona l'X-ray).

| Codice | Riferimenti | Parte | Tipo | Scorta |
|---|---|---|---|---:|
| C2934560 | U3 | ESP32-C3-WROOM-02-N4 | Extended | **11 626** |
| C165948 | J1 | TYPE-C-31-M-12 | Extended | 296 942 |
| C7519 | U1 | USBLC6-2SC6 | Extended | 33 503 |
| C404027 | U2 | TLV75533PDBVR | Extended | 93 007 |
| C2977522 | F1 | BSMD0805-050-12V | Extended | 58 626 |
| C15127 | Q1 | AO3401A | Basic | 1 692 654 |
| C15849 | C1, C7 | CL10A105KB8NNNC 1 µF | Basic | 12 635 622 |
| C19666 | C2 | CL10A475KO8NNNC 4,7 µF | Basic | 3 819 316 |
| C19702 | C3, C5, C9 | CL10A106KP8NNNC 10 µF | Basic | 10 043 308 |
| C14663 | C4, C6, C8, C10 | CC0603KRX7R9BB104 100 nF | Basic | 33 028 040 |
| C57112 | C11 | 0603B103K500NT 10 nF | Basic | 5 760 622 |
| C23186 | R1, R2 | 0603WAF5101T5E 5,1 kΩ | Basic | 20 107 413 |
| C21189 | R3, R4, R5, R21 | 0603WAF0000T5E 0 Ω | Basic | 18 783 185 |
| C25804 | R6, R7, R15, R16, R22 | 0603WAF1002T5E 10 kΩ | Basic | 46 833 353 |
| C23345 | R8, R9 | 0603WAF220JT5E 22 Ω | Basic | 5 896 427 |
| C25803 | R17 | 0603WAF1003T5E 100 kΩ | Basic | 15 913 491 |
| C23162 | R19, R20 | 0603WAF4701T5E 4,7 kΩ | Basic | 15 647 983 |
| C21190 | R23 | 0603WAF1001T5E 1 kΩ | Basic | 26 289 623 |

Restano 5 codici Extended, gli stessi della seconda revisione. Il modulo è sceso da 13 098 a 11 626 pezzi in un giorno: la scorta va ricontrollata all'ordine.

## 8. Chiusura dei rilievi precedenti

### 8.1 Seconda revisione (R2)

| Rilievo | Stato | Evidenza |
|---|---|---|
| R2-001 tabella delle rotazioni | **Chiuso** | `docs/12` §7 coincide con le piazzole di U1, U2 e Q1 (§6) |
| R2-002 checklist dello script Gerber | **Chiuso** | Docstring e messaggio finale di `esporta_gerber_jlc.py` aggiornati (contorno 50,5 × 41,5, zona antenna, EPAD senza vie, testi del retro); script non eseguito |
| R2-003 Q1 all'inserzione della USB | **Chiuso con riserva** | Osservazione di 3V3_DISP e `DISP_G` all'inserzione aggiunta a `VT-PWR-003`, attesa ≥ 2 ms in `docs/04` §4; resta da misurare |
| R2-004 piste vicino alla zona antenna | **Chiuso con riserva** | Nota V2 nella roadmap. Ora c'è anche DISP_BUSY (R3-002) |
| R2-005 disaccoppiamento e EN lontani | **Chiuso con riserva** | Misure in `VT-PCB-002`; testo di `docs/12` corretto (21 mm). **Aggravato** dall'isola GND sotto il modulo (R3-001) |
| R2-006 vie aperte nella EPAD | **Chiuso** | `DEC-046`: vie tolte (§5) |
| R2-007 residui nella documentazione | **Chiuso** | Sezioni di `docs/10` rinumerate, FIN-002 chiuso, `DEC-041` e `CAND-012` aggiornati. Nuovi residui in R3-005 |

### 8.2 Prima revisione (FIN)

| Rilievo | Stato | Nota |
|---|---|---|
| FIN-001 modulo "Standard Only" | **Chiuso** | WROOM-02-N4 "Economic and Standard", senza radiografia (oggi) |
| FIN-002 revisione a vista | **Chiuso** per `09200dc` | Le modifiche di `DEC-046`/`DEC-049` non hanno avuto una revisione a vista registrata: conviene un'occhiata a J2, R23 e DISP_BUSY insieme alla correzione di R3-001 |
| FIN-003 calo di 3V3 all'accensione del display | **Chiuso con riserva** | C11/R16 invariati; misura in `VT-PWR-003` |
| FIN-004 rotazioni nella CPL | **Chiuso con riserva** | Tabella corretta e CPL alternativa per U3; esito nell'anteprima JLC |
| FIN-005 testi della serigrafia | **Chiuso** | 17 testi a 1,0/0,15 mm |
| FIN-006 procedura Gerber | **Chiuso con riserva** | Script pronto, mai eseguito; serve l'autorizzazione del proprietario |
| FIN-007 regole DRC | **Chiuso con riserva** | Regola PTH attiva; commenti del `.kicad_dru` da aggiornare (R3-005) |
| FIN-008 cucitura GND | **Chiuso con riserva** | Cucitura rifatta (14 vie lungo il contorno). Le vie della EPAD non ci sono più (`DEC-046`) e restano isole del retro con 1–2 vie (R3-001, R3-003) |
| FIN-009 documenti ↔ PCB | **Chiuso** | Numeri di `docs/10` §16 verificati: 62 vie, 1166 mm, 67 mm con 2 vie, 0,22 mm, 41 elementi bloccati. Residui in R3-005 |
| FIN-010 linee esterne senza ESD | **Rischio accettato** | Invariato. Il pin 8 di J2 ha comunque R23 1 kΩ in serie |
| FIN-011 impronta JST PH | **Aperto** | Prova 1:1 del proprietario (JST PH e ora header 1×8) |

### 8.3 Revisione esterna (`docs/10` §15)

| Rilievo | Stato verificato |
|---|---|
| P1-01 centro di posa di U3 | **Risolto con procedura**: CPL alternativa corretta (§6); la scelta si fa nell'anteprima JLC |
| P1-02 linguette di J1 | **Risolto** con `DEC-047`: le 4 asole metallizzate (GND) hanno solo F.Mask/B.Mask, senza pasta; saldatura a mano nel bring-up (`VT-PCB-002`) |
| P1-03 J1 a filo del bordo | **Aperto**: DFM JLC (caricando i Gerber nel preventivo senza ordinare) |
| P1-04 Gerber e forature | **Voluto**: servono l'autorizzazione del proprietario |
| P2-01 vie nella EPAD | **Risolto** (`DEC-046`), con l'effetto collaterale di R3-001 |
| P2-05/06/07 maschera, fiducial, rotazioni | Checklist in `docs/12` §7 |
| P2-02/03/04/10 termica, disaccoppiamento, strapping, grafica | Nel piano di verifica |
| P2-08 ingombri | FIN-011 e `OPEN-028` aperti |
| P2-09 radio ed EMC | Nota V2; aggiungere DISP_BUSY (R3-002) |
| P3-01 stato unico | `docs/10` §15–§16, più la riga di questo rapporto |

## 9. Parti confermate corrette

- **Schema**: ERC 0. Pinout del WROOM-02 e strapping (IO2 pull-up 4,7 kΩ, IO8 con il pull-up I²C, IO9 10 kΩ verso 3V3 + TP11) invariati e conformi al datasheet v1.7. RC su EN 10 kΩ/1 µF. Rete BUSY corretta (§4). IO0 libero su TP9.
- **Alimentazione**: catena VBUS → F1 → C1 → TLV75533 → C3/C4/C5/C6, Q1 con R16 10 kΩ / R17 100 kΩ / C11 10 nF, invariata dalla seconda revisione.
- **USB**: coppia bloccata identica a `4780565` (36 elementi), U1 a passaggio diretto, zona `usb_coppia_retro` libera, R3/R4 0 Ω, CC 5,1 kΩ.
- **Antenna**: zona vietata dell'impronta su F.Cu e B.Cu (piste, vie, riempimenti, piazzole, footprint), riempimenti con area 0 nella zona; U3 a 2,99 mm dal bordo destro.
- **J2**: impronta 1×8 della libreria standard, pin 1–7 con lo stesso ordine (1 VCC … 7 RST), pin 8 BUSY, deroga della serigrafia nel `.kicad_dru` attiva su J2 (DRC 0).
- **J1**: asole metallizzate e pioli conformi ai minimi JLC; linguette senza pasta (`DEC-047`).
- **EPAD**: §5.
- **Fabbricazione**: tutti i valori del `.kicad_pro` e del `.kicad_dru` sopra i minimi JLC di oggi (§7.2). `.kicad_pro`, `.kicad_dru` e `verifica_meccanica_pcb.py` non sono cambiati dalla seconda revisione.
- **Assemblaggio**: Economic possibile (§7.1), 18 codici "Economic and Standard" a magazzino.
- **BOM/CPL**: formato JLC, coerenti con il PCB, CPL alternativa corretta (§6).
- **Documenti**: `docs/10` §16 descrive `DEC-049` con numeri esatti, e `docs/02`, `04`, `06`, `07`, `08`, `11` e `12` sono aggiornati per J2 1×8, BUSY, `DEC-046` e `DEC-047`. Fanno eccezione i residui di R3-005.

## 10. Decisioni e azioni del proprietario prima dei Gerber

1. **R3-001**: scegliere fra (a) sbrogliare di nuovo DISP_BUSY a sinistra di U3 e/o aggiungere vie GND accanto alla EPAD e nelle isole del retro (consigliato, poi ERC/DRC e controllo meccanico), oppure (b) accettare il rischio, scriverlo in `docs/10` e misurarlo in `VT-PCB-002`.
2. **Autorizzazione esplicita** a generare i Gerber con `python hardware/scripts/esporta_gerber_jlc.py --conferma-proprietario`, dopo la decisione su R3-001, da registrare in `docs/10`.
3. **FIN-011**: prova 1:1 dei JST PH e dell'header (ora 1×8, 20,3 mm), consigliata prima dei Gerber.
4. **`OPEN-028`**: se lo studio volumetrico può ancora cambiare sagoma o posizione dei connettori, conviene farlo prima dei Gerber, altrimenti andranno rigenerati.
5. Facoltativo, insieme a R3-001: R3-003 (vie nell'isola di 249 mm²), R3-004 (una riga in `docs/04`), R3-005 (residui).

Prima dell'ordine, invariati:

- scegliere la CPL nell'anteprima JLC e controllare le rotazioni con la tabella di `docs/12` §7;
- DFM di J1;
- scorte;
- `OPEN-016` e `OPEN-021`.

## 11. Evidenze e riproduzione

File in questa cartella:

- [erc.rpt](erc.rpt), [erc.json](erc.json);
- [drc.rpt](drc.rpt), [drc.json](drc.json);
- [verifica-meccanica.json](verifica-meccanica.json);
- [audit_finale.py](audit_finale.py), [audit-finale.json](audit-finale.json).

```powershell
$kicad = 'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe'
$py = 'C:\Program Files\KiCad\10.0\bin\python.exe'
$out = 'docs/revisioni/2026-11-09/revisione-finale-3'
& $kicad sch erc --severity-all --exit-code-violations --format json -o "$out/erc.json" hardware/policlock-main/policlock-main.kicad_sch
& $kicad pcb drc --severity-all --all-track-errors --schematic-parity --refill-zones --exit-code-violations --format json -o "$out/drc.json" hardware/policlock-main/policlock-main.kicad_pcb
& $py hardware/scripts/verifica_meccanica_pcb.py --output "$out/verifica-meccanica.json" hardware/policlock-main/policlock-main.kicad_pcb
& $py "$out/audit_finale.py"
git status --short   # se kicad-cli ha riscritto il .kicad_pro: git checkout -- hardware/policlock-main/policlock-main.kicad_pro
```

Le analisi delle isole GND, della zona antenna e del confronto con `4780565` sono state fatte con script pcbnew in sola lettura nella cartella temporanea della sessione. Riempiono le zone in memoria con `ZONE_FILLER` e non salvano mai il PCB. I numeri sono riportati qui sopra.

Nessuna prova su hardware fisico è stata eseguita: "stima", "analisi" e "rischio" non sono misure. Pagine JLC e scorte vanno ricontrollate all'ordine.
