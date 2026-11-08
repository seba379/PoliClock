# Revisione indipendente PoliClock rev 0.2

Data: 2026-11-08. Baseline locale esaminata: `4fb9200b8ce6cd744c4de031d9d9a3ed25d1fb57`, checkout in detached HEAD, inizialmente senza modifiche. Remote configurato: `https://github.com/seba379/PoliClock.git`; default remoto registrato: `origin/main`. Non è stato eseguito un fetch né verificato che questa sia l'ultima versione remota.

**Aggiornamento successivo:** su richiesta del proprietario sono stati corretti soltanto REV-001 (distanza dal bordo) e REV-003 (courtyard). Vedi [modifiche, verifiche e PCB da revisionare a vista](correzioni/README.md). Il presente rapporto e le sue evidenze conservano la baseline precedente alle correzioni.

## Esito

**Bozza elettricamente coerente e con ERC/DRC puliti; non ancora validabile per l'ordine o per il funzionamento del prodotto.** Non sono emersi errori di connessione o pinout nei blocchi verificati. Sono emersi un problema di distanza dal bordo per l'assemblaggio, limiti dei courtyard e del controllo automatico delle esportazioni, specifiche rimaste indietro rispetto alle decisioni e una verifica mancante dello spunto USB.

Le decisioni confermate, comprese quelle che superano decisioni precedenti, sono state considerate vincolanti. Nessuna decisione, schema, PCB, libreria, BOM, CPL o specifica esistente è stata modificata. Questa revisione aggiunge soltanto il rapporto, lo script diagnostico e le evidenze in questa cartella. Nessun ordine o file Gerber generato.

Priorità: **P1** da risolvere o qualificare prima dell'ordine; **P2** da correggere prima di usare il progetto come baseline operativa; **P3** chiarezza e manutenzione. Un rischio senza misura è distinto da un guasto osservato. Non sono stati eseguiti test su hardware fisico.

## Controlli eseguiti

Letti README, AGENTS, handoff storico, tutti i documenti `docs/00`–`12`, documentazione hardware/assets, generatori e script di esportazione. Esaminati i cinque fogli dello schema, progetto KiCad, PCB, libreria locale, netlist, BOM/CPL ed elaborati grafici. Confrontati i componenti critici con datasheet e disegni dei produttori, e le regole di fabbricazione/assemblaggio con le pagine JLCPCB consultate oggi.

| Verifica | Risultato |
|---|---|
| KiCad installato/usato | **10.0.6** |
| ERC, tutte le severità riportabili, codice di uscita sulle violazioni | **0 errori, 0 avvisi, 0 esclusioni riportate** |
| DRC, tutte le severità, tutti gli errori delle piste, zone ricalcolate in memoria | **0 violazioni, 0 elementi non connessi** |
| Parità schema ↔ PCB | **0 problemi** |
| Netlist riesportata ↔ netlist salvata | Connessioni e coppie valore/footprint dei componenti corrispondenti |
| Netlist riesportata ↔ reti delle piazzole PCB | Nessuna differenza rilevata |
| BOM riesportata ↔ BOM JLC salvata | Stesse righe; diversa terminazione delle righe nel file |
| BOM ↔ CPL ↔ PCB | **36 componenti**, stessi riferimenti; coordinate e rotazioni CPL corrispondenti al PCB |
| Montaggio | 36 componenti sopra; 11 test point sotto esclusi dal montaggio; 2 fori e 3 fiducial esclusi |
| Geometria scheda | 50 × 40 × 1,6 mm; intaglio da x = 42,16 mm a destra, fino a y = 20,18 mm |
| Rame | 530 segmenti, 55 vie, circa 935,362 mm di piste; larghezza minima osservata 0,15 mm |
| Anelli PTH di J1 | 0,20 mm nominali sui quattro fissaggi del guscio |
| Documentazione corrente | 65 link relativi verificati: nessun file mancante; nessun riferimento `DEC`/`OPEN`/`CAND` inesistente; tutti i requisiti attivi del PRD citati nel piano di verifica |

Il DRC pulito vale per le regole attualmente configurate. Non certifica automaticamente footprint corretti, assemblabilità JLC, prestazioni USB, termica o funzionamento. I controlli ignorati sono elencati integralmente in [erc.json](erc.json) e [drc.json](drc.json); fra quelli DRC non eseguiti figurano centratura pista/via, geometrie dei profili di accordatura e filtri footprint. La lista di esclusioni DRC del progetto è vuota.

Le prime esecuzioni in un profilo KiCad temporaneo vuoto segnalavano librerie standard mancanti. Dopo aver caricato le tabelle standard della stessa installazione sono risultate pulite. Questi avvisi di ambiente non sono stati classificati come difetti del progetto. L'ambiente ristretto segnala inoltre accessi negati a registro/cache utente e fontconfig; ERC, DRC ed esportazione netlist sono comunque terminati correttamente. Le zone non sono state salvate sul PCB originale.

## Rilievi

### REV-001 — P1: C7 non rispetta la distanza JLC dal bordo superiore

**Evidenza:** nel [PCB](../../../hardware/policlock-main/policlock-main.kicad_pcb), righe 5391–5394, C7 è a `(132,85; 102,25)` mm, con bordo superiore a y = 100 mm. Il corpo 0603 nominale, definito su F.Fab, è alto 0,8 mm: distanza dal corpo al bordo **2,25 − 0,40 = 1,85 mm**. Anche il courtyard dista meno di 2,5 mm. Non è un connettore che deve affacciarsi sul bordo.

I [termini ufficiali di assemblaggio JLCPCB](https://jlcpcb.com/help/article/terms-and-conditions-of-jlcpcb-assembly-service), sezione 2.3, indicano almeno **2,5 mm fra corpo e bordo**, senza limitare il requisito ai soli lati di trasporto. Il [generatore](../../../hardware/scripts/genera_pcb_main.py), righe 74–79 e 320–332, controlla il margine da 2,5 mm soltanto lungo x; lungo y usa 0,4 mm e si limita a stampare avvisi per i lati laterali.

**Impatto:** lo zero del DRC non dimostra il rispetto di questo requisito di assemblaggio. La distanza insufficiente di C7 si aggiunge alle eccezioni già documentate per i connettori superiori/inferiori e al modulo sopra l'intaglio.

**Chiusura:** mantenendo sagoma e scelte confermate, correggere il posizionamento oppure ottenere accettazione DFM della configurazione con pannellizzazione/bordi tecnici adeguati. Verificare tutti i bordi effettivi, intaglio compreso. Non reinterpretare `DEC-040` come deroga concessa da JLC: è una decisione di progetto, non un'accettazione del produttore.

### REV-002 — P1, rischio da qualificare: capacità e spunto all'ingresso USB

**Evidenza:** nello [schema USB/alimentazione](../../../hardware/policlock-main/usb_alimentazione.kicad_sch), C1 e C2 valgono entrambi 10 µF. Sono collegati a VBUS attraverso F1 e R5 = 0 Ω, **a monte** dell'LDO: 20 µF nominali, senza un circuito di controllo dello spunto su questa capacità. Il soft-start del TLV75533 agisce sulla sua uscita e non sulla carica di C1/C2.

Per il collegamento a una porta USB 2.0 di PC, il riferimento è la capacità effettivamente vista da VBUS e il comportamento all'inserzione; la [documentazione Microchip](https://onlinedocs.microchip.com/oxy/GUID-C6020E95-38E0-47B1-9EF9-A035ACD4168B-en-US-1/GUID-A66FB49A-520B-4013-B6FB-3D52AD226BF8.html) richiama il limite equivalente di 10 µF e la necessità di limitare lo spunto quando lo si supera. Anche [TI SLVA129](https://www.ti.com/lit/pdf/slva129) descrive il rischio di abbassamento della tensione della porta.

**Impatto:** non è dimostrata la compatibilità all'inserzione con PC/hub, prevista da `DEC-020` e `VT-FUN-004`. Un PTC da 0,5 A non equivale a una limitazione controllata del transitorio. **Non è stato misurato un superamento del limite:** capacità MLCC sotto bias, tolleranze, resistenze e rampa della sorgente vanno considerate; non basta sommare i valori nominali per dichiarare un guasto certo.

**Chiusura:** documentare il dimensionamento dell'ingresso e misurare corrente di inserzione e VBUS con la configurazione completa e cavi rappresentativi. Se necessario, adeguare i passivi o il trattamento dello spunto preservando USB-C, PTC, LDO e perimetro confermati. Integrare questa prova in `VT-PWR-001/003`; la sola corrente media a regime non la sostituisce.

### REV-003 — P2: courtyard incompleti nei connettori importati

**Evidenza:** il [footprint J2](../../../hardware/lib/PoliClock.pretty/HDR-SMD_7P-P2.54-H-M-W13.3-N.kicad_mod), righe 255–293, definisce il courtyard solo fra y = 3,6 e 6,1 mm. Le piazzole, centrate a y = 0 e lunghe 3,16 mm, sono interamente fuori da quel contorno. Nel [JST-SH 4 poli](../../../hardware/lib/PoliClock.pretty/CONN-SMD_4P-P1.00_SM04B-SRSS-TB-LF-SN.kicad_mod), righe 146–199, il limite y = −1,78 mm non include i contatti che arrivano a y = −2,715 mm; anche parte degli ancoraggi esce dal contorno. Analogo limite sul JST-SH a 2 poli. Mancano inoltre veri contorni del corpo su F.Fab per questi footprint importati.

**Impatto:** `missing_courtyard` è soddisfatto dalla presenza del poligono, ma `courtyards_overlap` non controlla correttamente l'intero ingombro. Le [convenzioni KiCad sui courtyard](https://klc.kicad.org/footprint/f5/f5.3/) richiamano l'inviluppo combinato di corpo e land pattern. Il generatore compensa in parte unendo piazzole e courtyard per il posizionamento automatico; ciò non corregge la libreria né protegge i futuri spostamenti manuali. Non è stata osservata una collisione fisica certa nel layout attuale.

**Chiusura:** completare courtyard e contorni F.Fab sui disegni dei produttori, aggiornare le istanze nel PCB e rieseguire DRC/controllo delle distanze. Il fatto che PCB e libreria locale coincidano non valida la geometria della libreria stessa.

### REV-004 — P2: lo script di esportazione può terminare con successo con DRC fallito

**Evidenza:** [esporta.py](../../../hardware/scripts/esporta.py), righe 46–49, esegue il DRC senza `--exit-code-violations`; non integra comunque il risultato nel booleano `ok`, usato alla riga 73. `ok` riflette l'ERC, non il DRC. Lo script prosegue con PDF, CPL e STEP anche in presenza di violazioni DRC.

**Impatto:** un'esecuzione conclusa con codice 0 non costituisce il gate ERC/DRC dichiarato. Una futura regressione del PCB potrebbe produrre esportazioni apparentemente riuscite. Il PCB attuale supera il DRC indipendente: questo rilievo riguarda la robustezza del processo.

**Chiusura:** richiedere il codice di errore sulle violazioni DRC e arrestare le esportazioni successive quando il controllo fallisce, verificando anche il fallimento operativo del comando. Aggiungere `--refill-zones` al controllo evita di dipendere da riempimenti salvati in precedenza.

### REV-005 — P2: specifiche firmware/UI incompatibili con DEC-034

**Evidenza:** [specifiche firmware](../../04-specifiche-firmware.md), righe 24 e 68–70, descrivono ancora PWM di retroilluminazione e NIGHT come sleep del pannello. [UI](../../05-interfaccia-utente.md), righe 65–66, assegna percentuali PWM a DIM/BRIGHT. Il modulo scelto non espone BLK: `DEC-034` prescrive attenuazione tramite grafica e spegnimento dell'alimentazione tramite Q1. Il medesimo documento UI descrive invece correttamente questa soluzione nella tabella degli stati, creando una contraddizione interna.

**Impatto:** il futuro firmware potrebbe implementare un controllo inesistente o lasciare la retroilluminazione accesa di notte. Non è sufficiente inviare sleep al controller se la retroilluminazione del modulo resta alimentata.

**Chiusura:** allineare i contratti a `DEC-034`: colori per DIM/BRIGHT, sequenza di alimentazione/reset/inizializzazione per NIGHT_PEEK, livelli dei cinque segnali quando il display è spento. Correggere anche `CAND-023` che parla ancora di PWM su IO20 e il diagramma alimentazione che include il touch.

Il diagramma firmware non mostra inoltre l'uscita `NIGHT_PEEK → DIM` alla fine della fascia notte: va definita per il caso di una pressione poco prima delle 07:00. Questo è un vuoto della specifica, non un bug di codice esistente: il firmware non è ancora presente e non è stato implementato durante la revisione.

### REV-006 — P3: revisione e annotazioni degli elaborati non allineate

Il [README principale](../../../README.md) presenta ancora schema rev 0.1; i cartigli dei cinque `.kicad_sch` riportano `rev "0.1"`, mentre note, PCB e documentazione tecnica parlano di rev 0.2. [schgen.py](../../../hardware/scripts/schgen.py), riga 227, fissa ancora la revisione a 0.1. Lo schema principale cita tasti RESET/BOOT rimossi con `DEC-039`.

Nel foglio MCU la nota di recupero contiene `\\n` letterali e si estende oltre il foglio: la procedura non è interamente leggibile nell'esportazione. Si sovrappongono inoltre alcune etichette attorno a IO8/IO9 e alla zona debug. L'ERC non verifica la leggibilità.

**Chiusura:** rendere coerenti cartigli, sommario e annotazioni; correggere gli a capo e l'impaginazione senza rigenerare automaticamente il progetto operativo. I generatori sovrascrivono i file e `genera_schemi.py` ricrea anche il `.kicad_pro`: non usarli come semplice aggiornamento del cartiglio.

### REV-007 — P3: residui storici ancora azionabili come istruzioni correnti

[CODEX_HANDOFF.md](../../../CODEX_HANDOFF.md) è la baseline storica v0.1 ma contiene ancora istruzioni operative e vincoli su batteria ricaricabile/Waveshare. Il contesto storico è riconoscibile dalla fase dichiarata, tuttavia manca un avviso iniziale che lo renda inequivocabilmente superato dalle decisioni attuali. Nella [roadmap](../../09-roadmap.md) il backlog richiede ancora pannello nudo/FPC, masse alternate e retroilluminazione bassa, superati dal modulo a 7 pin.

**Chiusura:** conservare la storia, marcando esplicitamente l'handoff come storico e aggiornando soltanto il backlog corrente. Nessuna decisione passata va cancellata o reintrodotta.

## Parti del progetto confermate dalla revisione

- **Alimentazione:** pinout DBV del TLV75533 coerente: IN 1, GND 2, EN 3 collegato a IN, NC 4 non collegato, OUT 5. Condensatori sulle reti corrette. Distanze geometriche pin/condensatore: ingresso 2,39 mm, uscita 2,38/2,24 mm. Stabilità con MLCC compatibile con il [datasheet TI SBVS320D](https://www.ti.com/lit/ds/symlink/tlv755p.pdf); non è una misura di stabilità o temperatura sulla scheda.
- **MCU:** assegnazione GPIO e pin del modulo coerente con il [datasheet Espressif v2.2](https://www.espressif.com/sites/default/files/documentation/esp32-c3-mini-1_datasheet_en.pdf). USB su 26/27, EN su 8, BOOT su 23, pull-up e RC presenti, NC separati, pad di massa connessi. C6 dista 2,37 mm dal pin 3V3. La rete EN conta circa 15 mm di piste e 3 vie: non emerge il precedente percorso da circa 60 mm.
- **Display:** Q1 ha source al 3V3, drain a 3V3_DISP, gate con R16 e pull-up R17; polarità del P-MOS corretta. R15 va alla tensione commutata. Il [datasheet AO3401A](https://www.aosmd.com/res/datasheets/AO3401A.pdf) specifica la conduzione anche a VGS = −2,5 V. Nessun touch o batteria di alimentazione reintrodotto.
- **I²C:** J3/J4 hanno 1 GND, 2 3V3_EXT, 3 SDA, 4 SCL; pull-up coerenti. Con 10 kΩ su ciascuno dei due moduli, 4,7 kΩ in parallelo diventano circa 2,42 kΩ. I pull-up del [modulo Adafruit](https://learn.adafruit.com/adafruit-ds3231-precision-rtc-breakout/pinouts) sono confermati; quelli dell'esatto breakout SHT40 restano da verificare. Il piano contiene già la prova degli strapping.
- **Footprint:** le quote principali dell'ESP32 coincidono con il land pattern del produttore; JST-SH hanno passo e piazzole coerenti con il [disegno JST](https://www.jst-mfg.com/product/pdf/eng/eSH.pdf). J1 coincide con il footprint standard KiCad ed è stato confrontato con il [disegno HRO](https://datasheet.lcsc.com/datasheet/pdf/9e56b777c022540fcce7c7f67825f55e.pdf?productCode=C165948). Questi riscontri non eliminano REV-003.
- **Header J2:** recuperato il [disegno Hanxia rev B del 2022-05-19 per C46061680](https://datasheet.lcsc.com/datasheet/pdf/52d5fe703899452f89e6a3fa48d69537.pdf?productCode=C46061680), che nei documenti era dichiarato non trovato. Conferma 7 poli, passo 2,54 mm e interasse totale 15,24 mm; piazzole raccomandate 1,02 × 3,20 mm, contro 1,02 × 3,16 mm nella libreria. La differenza di 0,04 mm va documentata/confrontata al DFM; non emerge un errore di passo o numero dei contatti. Ingombri e accoppiamento del campione restano da provare.

### Coppia USB: controllo indipendente sul PCB

Percorsi ricostruiti dal grafo dei segmenti e delle vie del PCB, includendo 1,6 mm per attraversamento di via e la distanza fra piazzole della resistenza serie. Non sono stati presi dai numeri stampati dal generatore.

| Percorso | D− | D+ | Vie per segnale | Differenza |
|---|---:|---:|---:|---:|
| B7/B6 → pin modulo | 14,6328 mm | 14,6328 mm | 0 | < 0,001 mm |
| A7/A6 → pin modulo | 19,3085 mm | 19,3085 mm | 2 | < 0,001 mm |

`DEC-041` risulta rispettata geometricamente. U1 collega correttamente i canali 1/6 e 3/4, con massa al 2 e VBUS al 5, come nel [datasheet ST](https://www.st.com/resource/en/datasheet/usblc6-2.pdf). La zona sotto la tratta principale è mantenuta libera da piste e vie sul retro.

La simmetria non prova un'impedenza di 90 Ω o la qualità del segnale. Il progetto dichiara l'impedenza non controllata; le [linee guida Espressif per USB](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32c3/pcb-layout-design.html#usb) raccomandano anche impedenza e riferimento continuo. Convalidare enumerazione, flash e configuratore nei due orientamenti della spina, con cavi e PC rappresentativi. Non è stato rilevato un malfunzionamento USB né svolto un eye test.

## Verifiche fisiche ancora necessarie

I gate già aperti restano tali: prototipo M1, modulo display reale (`OPEN-016`), SPI su cavetto (`OPEN-021`), studio volumetrico 1:1 (`OPEN-028`), revisione del proprietario in KiCad (`OPEN-027`), disponibilità/rotazioni JLC e revisione DFM. Lo STEP della sola scheda non dimostra il passaggio dei connettori, delle spine e dei cavetti nella statuetta.

Prima di considerare validata l'alimentazione occorrono anche queste osservazioni esplicite sul banco:

1. VBUS e 3V3 durante inserzione USB e transizioni Q1 spento/acceso, con il display effettivo: C9 e capacità del modulo possono produrre transitori, non valutabili con la sola corrente media. Accettazione: alimentazioni nei limiti, nessun brown-out o riavvio, USB stabile.
2. 3V3_DISP e segnali del display durante NIGHT, reset e download ROM. I livelli bassi richiesti al firmware non sono garantiti mentre esso non gira; GPIO6 ha un pull-up di reset nel caso JTAG predefinito ([configurazioni GPIO Espressif](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32c3/schematic-checklist.html#gpio)). Questo è un rischio di alimentazione parassita da misurare, non la dimostrazione che il display resti acceso.
3. Temperatura dell'LDO e degli altri componenti per 24 h a scocca chiusa. La targa 500 mA non garantisce 500 mA continui con 5 → 3,3 V in SOT-23; gli 80 mA citati restano una stima. Mantenere il vincolo del componente e qualificare il carico reale.
4. Quando si usa R21 per misurare/isolare la linea dei moduli, considerare che SDA/SCL restano collegati: togliere il ponticello di alimentazione non assicura l'assenza di alimentazione parassita attraverso I²C.

Tutte queste prove restano **NOT_RUN**. Nessun risultato automatico di questa revisione cambia tale stato.

## Evidenze e riproduzione

- [ERC leggibile](erc.rpt), [ERC JSON](erc.json).
- [DRC leggibile](drc.rpt), [DRC JSON](drc.json).
- [Misure geometriche, reti, BOM/CPL e hash dei file hardware](board-audit.json).
- [Script diagnostico in sola lettura](audit_board.py), da eseguire con il Python di KiCad 10; riscrive soltanto `board-audit.json` in questa cartella.

Comandi dalla root, con librerie standard KiCad 10 configurate e libreria di progetto disponibile:

```powershell
$kicad = 'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe'
& $kicad sch erc --severity-all --exit-code-violations --format json -o docs/revisioni/2026-11-08/erc.json hardware/policlock-main/policlock-main.kicad_sch
& $kicad pcb drc --severity-all --all-track-errors --schematic-parity --refill-zones --exit-code-violations --format json -o docs/revisioni/2026-11-08/drc.json hardware/policlock-main/policlock-main.kicad_pcb
& 'C:\Program Files\KiCad\10.0\bin\python.exe' docs/revisioni/2026-11-08/audit_board.py
```

Non aggiungere `--save-board` per una verifica in sola lettura. La ripetizione di questi comandi dopo modifiche al progetto produce nuove evidenze, non conserva automaticamente questa baseline. Per emettere una successiva approvazione servono chiusura dei rilievi applicabili e risultati dei gate, senza cambiare le decisioni confermate.
