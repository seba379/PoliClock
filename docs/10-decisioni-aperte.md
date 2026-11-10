# 10 — Decision log e questioni aperte

**Versione:** 1.0 · **Data:** 2026-11-09

## 1. Decisioni confermate (CONF)

Le decisioni superate restano nel registro per tracciabilità, con lo stato indicato.

| ID | Data | Decisione | Motivazione / impatto |
|---|---|---|---|
| `DEC-001` | 2026-11-07 | Prodotto come regalo: orologio da scrivania in statuetta stampata 3D | Focus su semplicità, estetica e funzionamento indipendente |
| `DEC-002` | 2026-11-07 | Personaggio: **poliziotta chibi/stilizzata**, con testa sproporzionata | Stile simpatico, riconoscibile e stampabile |
| `DEC-003` | 2026-11-07 | **Display circolare al posto del volto** | Vincolo primario CAD/display |
| `DEC-004` | 2026-11-07 | Funzioni V1: **ora, data, temperatura, umidità** | Esclude le funzioni opzionali del concept originale |
| `DEC-005` | 2026-11-07 | ~~Dispositivo alimentato da batteria ricaricabile~~ — **superata da `DEC-023`** per la V1 | — |
| `DEC-006` | 2026-11-07 | Porta **USB sul retro**, formato **USB-C** (confermato in `DEC-011`) | Connettore nascosto/fruibile |
| `DEC-007` | 2026-11-07 | Modalità ibrida: **display attenuato**, luminosità aumentata dopo interazione | Requisito guida firmware/UI |
| `DEC-008` | 2026-11-07 | ~~Ricarica ogni 2 giorni accettabile~~ — **superata da `DEC-023`** | — |
| `DEC-009` | 2026-11-07 | **Di notte il display è spento** (modalità notte) | Funzione aggiunta su richiesta del proprietario: riduce consumi e calore. Orari in `DEC-013`; comportamento al pulsante in `CAND-009` |
| `DEC-010` | 2026-11-07 | Aspetto: **uniforme blu e cappello** | Vincolo estetico CAD/colori (`PR-UI-002`) |
| `DEC-011` | 2026-11-07 | Connettore posteriore **USB-C** (non solo preferito) | Vincola foro e supporto posteriore |
| `DEC-012` | 2026-11-07 | **Wi-Fi e sincronizzazione NTP esclusi dalla V1** | Ora impostata offline (configuratore o pulsante); meno configurazione e superficie d'errore. Rivalutabile in V2 |
| `DEC-013` | 2026-11-07 | Fascia notte di default **23:00–07:00**, configurabile | Base di `VT-UI-003` |
| `DEC-014` | 2026-11-07 | ~~Profilo d'uso per l'autonomia 48 h~~ — **superata da `DEC-023`**; il ciclo DIM/BRIGHT/NIGHT resta il riferimento per le misure di consumo e calore | — |
| `DEC-015` | 2026-11-07 | **PCB custom** progettato in KiCad e prodotto/assemblato da JLCPCB, con il minimo indispensabile; scartata la scheda Waveshare (ex `CAND-001`) | Costo della scheda pronta giudicato eccessivo dal proprietario, consapevole che per un solo esemplare il custom non costa necessariamente meno. Riconfermata dopo il confronto con le dev board FireBeetle 2, usabili come riferimento di progetto (senza copiarne schema/layout prima di verificarne la licenza) |
| `DEC-016` | 2026-11-07 | Display **IPS rotondo 1,28"**, 240×240, driver GC9A01 | Economico e documentato; nessun burn-in |
| `DEC-017` | 2026-11-07 | Interazione principale con **pulsante** fisico; posizione da definire | Più semplice ed economico; posizione in `OPEN-017`. Touch predisposto in `DEC-019`, poi escluso da `DEC-034` |
| `DEC-018` | 2026-11-07 | Presa USB-C nella **parte posteriore bassa** della statuetta (sul sedere, per ironia); collegamento al PCB in `DEC-021`. *Posizione aggiornata da `DEC-048`: retro della base d'appoggio; la battuta del sedere non si tiene (`DEC-051`)* | Vincola foro, fissaggio e stabilità con cavo inserito |
| `DEC-019` | 2026-11-07 | ~~**Predisposizione touch** sul PCB~~ — **superata da `DEC-034`** (niente touch). Testo originale: predisposizione touch sul PCB (connettore/footprint, GPIO INT e RST riservati, componenti non montati); pulsante sempre presente; pannello scelto tra modelli disponibili con e senza touch a parità di ingombro | Il touch si potrà attivare senza rifare il PCB; decisione dopo la prova sul prototipo M1 (`OPEN-018`) |
| `DEC-020` | 2026-11-07 | **Configuratore da PC via USB** come metodo principale per impostare ora, data e fascia notte; menu con il pulsante come riserva | La USB nativa dell'MCU espone una porta seriale; protocollo documentato (`CAND-017`); configuratore web con Web Serial (`CAND-018`) |
| `DEC-021` | 2026-11-07 | **Scheda principale rettangolare separata dal display**, collegata a una **schedina portadisplay** nella testa con cavo (FFC o JST-SH) attraverso il collo; SHT40 su mini-PCB (superato da `DEC-028`: modulo commerciale); tutte nello stesso pannello JLC. Posizione della scheda principale decisa con la bozza CAD (`OPEN-020`): preferita nel busto/base con **USB-C saldata sulla scheda** affacciata al sedere; prolunga solo se la scheda va nella testa. *Posizione decisa da `DEC-048`: scheda nella base, USB-C saldata sulla scheda (opzione A), nessuna prolunga* | Layout più semplice e sicuro, schema e PCB realizzabili da Claude con revisione visiva del proprietario; testa libera dai vincoli del PCB |
| `DEC-022` | 2026-11-07 | Strumenti: **KiCad 10** (`kicad-cli`), **VS Code + ESP-IDF** (v6.x, versione da fissare al bring-up), **Blender** per la chibi, **CAD a codice** (build123d) per le parti tecniche | Strumenti gratuiti e automatizzabili; scultura artistica a mano in Blender |
| `DEC-023` | 2026-11-07 | **V1 senza batteria: alimentazione continua da cavo USB-C.** RTC esterno con tampone mantenuto. Batteria rimandata a eventuali versioni successive, da ridiscutere | Rimuove la parte più complessa e rischiosa (cella, caricatore, NTC, autonomia, gate di sicurezza della cella); semplifica PCB, firmware e CAD; accettato che l'orologio funzioni solo collegato. Supera `DEC-005`, `DEC-008`, `DEC-014` |
| `DEC-024` | 2026-11-07 | **RTC su modulo esterno via cavo: Adafruit DS3231 Precision RTC – STEMMA QT** (prodotto 5188) con pila **CR1220**, collegato con cavo JST-SH 4 poli (Qwiic) al connettore J4 della scheda principale; nessun RTC sul PCB. *Connettore lato scheda JST PH dalla `DEC-043`* | RV-3028-C7 a stock 0 su LCSC/JLC; scelto dal proprietario fra RTC sul PCB (RV-3032-C7, PCF85063A, PCF8563T) e moduli esterni. DS3231 compensato in temperatura (±2 ppm), tampone di anni, modulo documentato. La pila serve solo all'RTC (compatibile con `DEC-023`). Supera `CAND-014` |
| `DEC-025` | 2026-11-07 | **Superata da `DEC-034`.** Schedina portadisplay disegnata per il **pannello GC9A01 1,28" con touch** (CST816S, FPC **18 poli**); si acquista sempre la versione touch, il touch resta inattivo finché non viene abilitato | Un solo footprint rispetta la predisposizione `DEC-019`. Pinout preso dallo schema di riferimento Waveshare, da confermare sul pannello acquistato (`OPEN-016`) |
| `DEC-026` | 2026-11-07 | **Superata da `DEC-034`.** Cavo display **FFC 16 poli passo 0,5 mm** con connettori ZIF SMD JUSHUO AFC01-S16FCA-00 su entrambe le schede | 10 segnali (con touch) + 2×3,3 V + 4×GND alternati; connettore molto disponibile a JLC. Supera `CAND-020` (resta da validare la stabilità SPI, `OPEN-021`) |
| `DEC-028` | 2026-11-07 | **SHT40 su modulo breakout commerciale** (es. "SHT40 modulo I²C 3V 5V, nero, con pin") collegato al connettore J3 con cavo JST-SH 4 poli → jumper femmina; eliminato il mini-PCB SHT40. *Connettore lato scheda JST PH dalla `DEC-043`* | Scelta del proprietario: un PCB in meno da progettare e ordinare. Alimentato a 3,3 V; LED del modulo da rimuovere se presente; pinout dalla serigrafia del modulo acquistato. Supera la parte "SHT40 su mini-PCB" di `DEC-021` e `CAND-002` |
| `DEC-029` | 2026-11-07 | **Superata da `DEC-039`** (tasti tolti). Tasti **RESET e BOOT 4×3 mm** (XUNPU TS-1088-AR02016, LCSC C720477, Basic) al posto dei 5,1×5,1 mm | Scelta del proprietario per ridurre l'ingombro senza costi aggiuntivi |
| `DEC-030` | 2026-11-07 | Scheda principale **a 2 strati** con componenti **solo sul lato superiore** | Scelta del proprietario: assemblaggio JLC economico; dimensioni in `DEC-033` |
| `DEC-032` | 2026-11-07 | **Tolto il tasto USER dalla scheda principale**: il pulsante è solo quello remoto su J5 | Scelta del proprietario: il tasto su scheda era un doppione per il collaudo; libera spazio (scheda da 35 × 27 a 35 × 26 mm). Per il collaudo si cortocircuitano i pin di J5. Supera la parte "tasto su scheda" di `DEC-027` |
| `DEC-031` | 2026-11-07 | **Antenna del modulo ESP32 fuori dalla scheda base** (la parte "intaglio" è superata da `DEC-045`: antenna sulla scheda con zona vietata) (con il WROOM-02 di `DEC-044` l'intaglio si allarga a 8,5 × 20,2 mm) (dalla rev 0.2 sopra un intaglio, dentro l'ingombro: `DEC-036`); in origine sporgente oltre il bordo della scheda principale | Scelta del proprietario: disposizione raccomandata da Espressif, risparmia circa 13 × 6 mm di scheda; radio non usata in V1 (`DEC-012`) ma non compromessa per il futuro |
| `DEC-033` | 2026-11-07 | **Dimensione superata da `DEC-036`.** Scheda principale **40 × 30 mm** invece della più piccola possibile, per uno sbroglio completo e affidabile | Indicazione del proprietario ("non ci serve per forza la versione più piccola possibile"). A 35 × 26 mm Freerouting lasciava 10 connessioni aperte; 40 × 30 è la dimensione più piccola provata che si sbroglia completamente con DRC pulito |
| `DEC-034` | 2026-11-07 | **Display su modulo GC9A01 1,28" a 7 pin** (IPS a colori 240×240, piedini 2,54 mm provabili su breadboard), es. [AliExpress SZHJW 1005009766462228](https://it.aliexpress.com/item/1005009766462228.html); **niente touch**, retroilluminazione sempre accesa con il modulo alimentato; sulla scheda principale header 1×7 2,54 mm SMD (*a foro passante dalla `DEC-043`*) e interruttore P-MOS sull'alimentazione del modulo | Scelta del proprietario dopo la revisione indipendente: risparmiare sul display e provarlo su breadboard. Elimina pannello nudo, schedina portadisplay, cavo FFC e il problema dell'orientamento FFC (P0-02, P0-03). Supera `DEC-019`, `DEC-025`, `DEC-026` e la parte "portadisplay" di `DEC-021`; modifica `DEC-007` (attenuazione solo via grafica, nessun PWM della retroilluminazione); `DEC-009` mantenuta spegnendo il modulo di notte. Il proprietario aveva anche scelto un pinout FFC simmetrico, non più necessario |
| `DEC-035` | 2026-11-07 | **Superata da `DEC-044`.** Modulo **ESP32-C3-MINI-1-H4X** (C41349510) al posto dell'N4 | Revisione P1-05: N4 è NRND; la variante raccomandata N4X ha stock 0 su JLC/LCSC, la H4X è anch'essa "Recommended" (chip v1.1, 105 °C), stesso footprint, ~3,10 $. Scelta del proprietario |
| `DEC-036` | 2026-11-07 | **Superata da `DEC-045`.** Scheda principale **50 × 40 mm** (sostituisce `DEC-033` per la dimensione; confermata con il modulo WROOM-02 di `DEC-044`), con l'antenna del modulo dentro l'ingombro sopra un intaglio senza PCB | Parole del proprietario: "per il primo prototipo è meglio stare larghi e confermare 50x40". L'intaglio mantiene l'antenna fuori dalla scheda base come raccomanda Espressif, senza sporgere dall'ingombro (aggiorna `DEC-031`) |
| `DEC-037` | 2026-11-07 | LDO **TI TLV75533PDBVR** (C404027, 500 mA, stabile con MLCC ≥ 1 µF) al posto dell'AMS1117-3.3 | Revisione P0-04: AMS1117 qualificato con 22 µF al tantalio e C3 a 26 mm dal regolatore. Scelto dal proprietario fra TPS73733, TLV75533 e AP2112K; condensatori di ingresso e uscita a 2,4–2,8 mm dai pin. Supera `CAND-015` e chiude `OPEN-025` |
| `DEC-038` | 2026-11-07 | Riconferme dopo la revisione indipendente: **V1 senza batteria** (P0-01, `DEC-023`) e **display 1,28"** (P1-10, `DEC-016`) | Decisioni esplicite del proprietario, già registrate; il test di leggibilità 1:1 a 50–80 cm resta in `VT-UI-001` |
| `DEC-039` | 2026-11-08 | **Tolti i tasti RESET e BOOT** dalla scheda principale: restano i punti di test **TP6 (EN)** e **TP11 (IO9)** sul retro, con pull-up 10 kΩ su IO9 e RC 10 kΩ/1 µF su EN | Scelta del proprietario ("Sì, toglili"): flash e reset passano dalla USB nativa; per il recupero si collega IO9 a GND durante l'accensione. Libera spazio attorno al modulo. Supera `DEC-029` |
| `DEC-040` | 2026-11-08 | **Regole JLCPCB nel progetto** (vincolo `SC-008`): DRC di KiCad impostato con i minimi di fabbricazione JLC 2 strati con margine (pista e distanza ≥ 0,15 mm, vie 0,6/0,3 mm, foro-foro ≥ 0,25 mm, foro-rame ≥ 0,3 mm, rame-bordo ≥ 0,3 mm); assemblaggio "Economic" su un solo lato (confermato da `DEC-044`: modulo WROOM-02 montabile in Economic); **corpo dei componenti ≥ 2,5 mm da tutto il contorno, intaglio compreso** (errata del 2026-11-08: la prima stesura limitava la regola ai lati sinistro e destro, ma i termini JLC non fanno questa distinzione; vedi §8); eccezioni esplicite da far accettare al DFM: J1 e J2 a filo dei lati inferiore e superiore, U3 sopra l'intaglio (dalla `DEC-043` J2 non è più montato da JLC; **dalla `DEC-045` l'unica eccezione è J1**); 3 fiducial; BOM e CPL nel formato JLC | Vincolo del proprietario `SC-008`. Valori letti il 2026-11-08 sulle pagine ufficiali [capacità PCB](https://jlcpcb.com/capabilities/pcb-capabilities), [capacità assemblaggio](https://jlcpcb.com/capabilities/pcb-assembly-capabilities), [termini dell'assemblaggio](https://jlcpcb.com/help/article/Terms-and-Conditions-of-JLCPCB-Assembly-Service); da ricontrollare all'ordine. Da confermare con la revisione DFM di JLC: i connettori sui lati superiore e inferiore sono a meno di 2,5 mm dal bordo per necessità (USB-C, header) |
| `DEC-041` | 2026-11-08 | **Coppia USB D+/D- simmetrica, tracciata a mano** (ridisegnata per i pin 13/14 del WROOM-02 con gli stessi criteri, `DEC-044`) (`hardware/scripts/usb_coppia.py`, piste bloccate che Freerouting non tocca): connettore J1, USBLC6 (U1), R3/R4 e pin del modulo (oggi 13/14 del WROOM-02; in origine 26/27 del MINI-1) sullo stesso asse; percorso principale B7/B6 → modulo speculare e senza vie; contatti interni A6/A7 incrociati con **2 vie per rete**; percorsi completi contatto → modulo **uguali** su entrambe le facce della spina; U1 a passaggio diretto (D- sui pin 1/6, D+ sui pin 3/4, canali scambiati nello schema), +5V del pin 5 sotto il corpo di R4 senza vie; retro libero da piste e vie sotto la coppia fra U1 e il modulo | Richiesta del proprietario: "ora che di spazio ne abbiamo, non voglio asimmetrie su D- e D+ dell'USB". Con i contatti del connettore nell'ordine D-, D+, D-, D+ un incrocio è inevitabile su 2 strati: va sui rami corti dei contatti interni, con lo stesso numero di vie su D+ e D-. Lunghezze e vie in [02](02-architettura-hardware.md) §3.2 |
| `DEC-042` | 2026-11-08 | **Capacità d'ingresso USB sotto 10 µF**: C1 (+5 V dopo il PTC) da 10 a **1 µF** (C15849) e C2 (ingresso LDO) da 10 a **4,7 µF** (C19666, X5R 16 V, Basic). Totale su VBUS 5,7 µF nominali, al massimo 6,3 µF | Scelta del proprietario sul rilievo REV-002 (`OPEN-029`): rientrare nei 10 µF ammessi all'inserzione USB senza aggiungere un limitatore di spunto. Il TLV75533 è stabile con ≥ 1 µF; stessa impronta 0603, nessuna modifica al rame. Spunto all'inserzione da misurare comunque in `VT-PWR-001` |
| `DEC-043` | 2026-11-08 | **Connettori J2–J5 a foro passante, saldati a mano dal proprietario**: J3 (SHT40), J4 (RTC) e J5 (pulsante) diventano **JST PH B4B-PH-K-S** (2,0 mm, verticali, impronta KiCad `JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical`; pinout 1 GND, 2 3V3_EXT, 3 SDA, 4 SCL; su J5 pin 1 BTN_USER, pin 2 GND, pin 3–4 non collegati); J2 diventa un **header 1×7 2,54 mm a foro passante** (`PinHeader_1x07_P2.54mm_Horizontal`, a 90° con i piedini oltre il bordo superiore; negli stessi fori va bene un header diritto), stesso pinout (1 VCC … 7 RST). JLC monta tutto il resto, J1 compreso. J2–J5 hanno il campo `Montaggio` = "a mano, parte del proprietario", nessun codice LCSC e l'attributo "escluso dai file di posizionamento": fuori da BOM JLC e CPL, presenti nella BOM completa | Scelta del proprietario: parti già in scorta, meno parti Extended a JLC (spariscono C46061680, C160404 e C160402: da 8 a 5 codici Extended, circa −9 $ di setup). Il margine JLC di 2,5 mm vale solo per le parti montate da JLC; le regole di fabbricazione (`DEC-040`) valgono anche per le piazzole a foro passante. Modifica e verifiche in §10; aggiorna la parte "connettore lato scheda" di `DEC-024`, `DEC-027`, `DEC-028` e `DEC-034` |
| `DEC-044` | 2026-11-08 | **Modulo ESP32-C3-WROOM-02-N4 (C2934560) al posto dell'ESP32-C3-MINI-1-H4X**; supera `DEC-035` e aggiorna `DEC-031`, `DEC-036` (intaglio 8,5 × 20,2 mm, scheda sempre 50 × 40) e `DEC-041` (coppia ridisegnata sui pin 13/14 con gli stessi criteri). Applicate con la stessa modifica le correzioni approvate della revisione finale: FIN-003, FIN-005, FIN-006, FIN-007, FIN-008, FIN-009 (§11) | Scelta del proprietario sul rilievo FIN-001: l'H4X a JLC è "Standard Only" con radiografia, mentre `DEC-040` prevede l'Economic. Il WROOM-02-N4 è "Economic and Standard" senza radiografia (pagina JLC 2026-11-08, 13 113 a magazzino, ~3,31 $): si resta sull'Economic, circa −17 $ di setup (Standard 25,56 $ contro Economic 8,18 $, pagina JLC "pcb-assembly-price" aggiornata il 2026-10-22) e niente bordi tecnici. Fase 0 (2026-11-08): stato "Mass Production" nel selettore Espressif, chip v0.4 supportato da ESP-IDF v6.0/v6.1, pinout e land pattern dal datasheet v1.7; nessuna variante con chip v1.1. Dettagli in [02](02-architettura-hardware.md) §3.2 e [12](12-selezione-componenti.md) |
| `DEC-045` | 2026-11-08 | **Regola JLC dei 2,5 mm corpo-bordo per tutte le parti montate da JLC, unica eccezione J1** (USB-C a filo del bordo inferiore, da far accettare alla DFM di JLC, senza bordo tecnico). Scheda **50,5 × 41,5 mm rettangolare, senza intaglio**: cresce di 0,5 mm a destra e 1,5 mm in alto, angolo in basso a sinistra fisso (J1, H1/H2, coppia USB e origine della CPL invariati). **Antenna di U3 sulla scheda**, verso il bordo destro, con zona vietata su entrambi gli strati (niente rame, piste, vie, riempimenti, piazzole né componenti) sotto l'antenna e 5 mm oltre i suoi lati, come la zona dell'impronta di U3 ricavata dal datasheet. Supera `DEC-036` e la parte "intaglio" di `DEC-031` | Parole del proprietario: "dobbiamo rispettare non arbitrariamente le regole di stampa di JLC PCB [...] per questo prototipo allunga la scheda da quel lato, in modo da farci stare i componenti che mancano, rispettando le regole di JLC". Radio non usata in V1 (`DEC-012`): l'antenna sulla scheda è un compromesso accettato. Margine minimo 2,99 mm (U3); dettagli in [02](02-architettura-hardware.md) §3.2 |
| `DEC-046` | 2026-11-08 | **EPAD di U3 senza vie**: tolte le 4 vie termiche 0,3/0,7 mm dalla piazzola di massa (pad 19) del WROOM-02, in libreria e sul PCB; la EPAD resta collegata a GND sul rame superiore e mantiene le 9 aperture di pasta | Approvata dal proprietario sulla revisione esterna `PoliClock_report_validazione_rev02_2026-11-08.md` del proprietario (P2-01) e R2-006: le vie aperte nella piazzola possono assorbire stagno al reflow; il datasheet Espressif dice che la saldatura della EPAD non è obbligatoria e con la radio spenta (`DEC-012`) la dissipazione è minima. È uno **scostamento voluto** dal land pattern Espressif: la fig. 11-1 del datasheet WROOM-02 v1.7 disegna "Via for thermal pad". Vie GND accanto alla piazzola, non dentro, dopo la terza revisione (§17). Script `hardware/scripts/dec046_epad.py` |
| `DEC-047` | 2026-11-08 | **Linguette del guscio di J1 saldate a mano**: le 4 linguette metallizzate a foro passante della USB-C (C165948, "SMT Assembly" su JLC, senza pasta nei fori) le salda il proprietario dal retro dopo l'assemblaggio, insieme a J2–J5. Nessuna pasta aggiunta nei fori | Approvata dal proprietario sulla revisione esterna `PoliClock_report_validazione_rev02_2026-11-08.md` del proprietario (P1-02): il reflow salda i contatti SMD ma non garantisce le linguette, necessarie per la tenuta meccanica di una presa usata spesso. In alternativa la conferma scritta di JLC nella DFM |
| `DEC-048` | 2026-11-09 | **Scheda principale nella base d'appoggio della statuetta, presa USB-C sul retro della base.** Parole del proprietario: "inserire la scheda main in una base d'appoggio, e sul retro di questa base d'appoggio del chibi, ci sarà anche la presa usb". Chiude `OPEN-020`; realizza l'opzione A di `DEC-021` (USB-C saldata sulla scheda, nessuna prolunga: `CAND-004` ritirata); aggiorna la posizione di `DEC-018` e `SC-003`: la presa resta posteriore e bassa, sul retro della base invece che "sul sedere" | Nella base c'è lo spazio che manca al busto della chibi. La scheda rev 0.2 ci entra senza modifiche al PCB (studio volumetrico in [06](06-progettazione-meccanica.md) §12). Dalla testa scende solo il cavetto display. Nella base stanno anche RTC, SHT40 e zavorra, con il baricentro basso |
| `DEC-049` | 2026-11-09 | **Pin BUSY su J2 per un eventuale display e-paper**: J2 diventa un header **1×8** 2,54 mm a foro passante, sempre saldato a mano (`DEC-043`); pin 1–7 invariati (1 VCC … 7 RST), **pin 8 = BUSY** → R23 1 kΩ in serie (C21190, Basic) → **IO1** (pin 17 del WROOM-02), che resta sul punto di test TP10. Nessun pull esterno: il firmware abilita il pull-down interno di IO1; con il GC9A01 a 7 pin il pin 8 resta libero e IO1 legge 0. IO0 resta libero su TP9 | Parole del proprietario: "fai aggiungere il pin BUSY, verificando che IO0 e IO1 effettivamente possano essere configurati come BUSY per SPI". Verifica sui datasheet Espressif in §16: GPIO0 e GPIO1 sono GPIO ordinari (non sono strapping, non hanno glitch all'accensione e il modulo non ha un quarzo da 32 kHz su quei pin); BUSY è un ingresso GPIO e non usa funzioni della periferica SPI. Sul PCB J2 si sposta di 2,54 mm a sinistra, perché il pin 8 a destra cadrebbe sotto U3; il cavetto a 7 fili si infila ancora sui pin 1–7 |
| `DEC-051` | 2026-11-09 | **Chibi in piedi sulla base**: la battuta della presa "sul sedere" non si tiene | Scelta estetica del proprietario fra chibi seduta sul bordo della base (con la presa subito sotto il sedere) e chibi in piedi. Aggiorna l'intento estetico di [06](06-progettazione-meccanica.md) §1 |
| `DEC-052` | 2026-11-09 | **Stampa 3D tramite un servizio di stampa online**, non con una stampante del proprietario. Servizio, tecnologia e materiali sono da scegliere (`OPEN-032`) | Risposta del proprietario: "mi affiderò ad un servizio di stampa online". Tolleranze, spessori minimi e divisione dei pezzi seguono le regole del servizio scelto, da leggere sulle sue pagine al momento dell'ordine |
| `DEC-027` | 2026-11-07 | Pulsante utente: **connettore JST-SH 2 poli** (*JST PH 4 poli sui pin 1–2 dalla `DEC-043`*) per un pulsante remoto **e** tasto tattile sulla scheda in parallelo (tasto su scheda tolto con `DEC-032`) | La posizione nella statuetta (`OPEN-017`) si decide col CAD senza rifare il PCB; il tasto su scheda serve al bring-up |

Le date sopra sono la data della formalizzazione nel documento delle scelte emerse nella conversazione, non un registro notarile degli eventi.

## 2. Proposte tecniche, NON decisioni definitive

| ID | Proposta | Stato | Come si decide |
|---|---|---|---|
| `CAND-001` | Waveshare ESP32-S3-Touch-AMOLED-1.75 | **Scartata** (`DEC-015`) | — |
| `CAND-002` | SHT40 su mini-PCB dedicato senza LED, nello stesso pannello JLC | **Superata** da `DEC-028` (modulo commerciale) | — |
| `CAND-003` | LiPo protetta 1S | **Ritirata** (`DEC-023`) | — |
| `CAND-004` | Prolunga USB-C da pannello con dati USB 2.0 | **Ritirata** (`DEC-048`: scheda nella base, USB-C sulla scheda) | — |
| `CAND-005` | ESP-IDF con moduli BSP/servizi/UI separati | Proposto | Bring-up ed ergonomia del codice |
| `CAND-006` | 20 s di luminosità BRIGHT dopo pressione del pulsante | Proposto | Test usabilità |
| `CAND-007` | Target 48 h autonomia | **Ritirato** (`DEC-023`) | — |
| `CAND-008` | Altezza 130–160 mm; dal blockout del 2026-11-09 **circa 150 mm** (base 24, testa 70 con il modulo display, cappello). Il proprietario ha chiesto di ricavarla dal volume | Proposto | Approvazione dei render, modulo display reale (`OPEN-016`) |
| `CAND-009` | Modalità notte: una pressione del pulsante mostra il quadrante attenuato per un timeout breve (proposto 10 s), poi torna spento | Proposto | Test usabilità e `VT-UI-003` |
| `CAND-010` | Profilo d'uso di riferimento | Confermato → `DEC-014`, poi superato | — |
| `CAND-011` | SHT40 sui pin I²C della Waveshare | **Superata** (`DEC-015`) | — |
| `CAND-012` | MCU: modulo ESP32-C3 (in origine MINI-1 consigliato, oppure ESP32-S3-MINI-1). **Superato**: modulo scelto ESP32-C3-WROOM-02-N4 (`DEC-044`) | Superato da `DEC-044` | Pin necessari (budget migliorato senza batteria), prezzo/disponibilità LCSC, prototipo M1 |
| `CAND-013` | Caricatore con power-path e NTC | **Ritirato** (`DEC-023`) | — |
| `CAND-014` | RTC esterno a bassissimo consumo con tampone (es. RV-3028-C7 o PCF85063A + supercondensatore/pila) | **Superata** da `DEC-024` (RV-3028-C7 non disponibile) | — |
| `CAND-015` | Regolatore 3,3 V da 5 V USB: LDO AMS1117-3.3 | **Superata** da `DEC-037` (TLV75533) | — |
| `CAND-016` | Misura batteria | **Ritirata** (`DEC-023`) | — |
| `CAND-017` | Protocollo di configurazione testuale a righe sulla porta seriale USB, versionato (vedi [firmware](04-specifiche-firmware.md) §6.1) | Proposto | Prototipo M1 e test `VT-FW-007` |
| `CAND-018` | Configuratore come **pagina web statica** con Web Serial (Chrome/Edge desktop), nessuna installazione; alternativa script Python | Proposto | Prova su Windows con la dev board; compatibilità browser |
| `CAND-019` | Posizione scheda principale: **A** busto/base con USB-C sulla scheda (preferita) o **B** testa con prolunga | **Scelta A** (`DEC-048`, nella base) | — |
| `CAND-020` | Cavo display FFC | **Superata** da `DEC-034` (modulo a 7 pin con cavetto Dupont) | — |
| `CAND-021` | CAD a codice con **build123d** (alternativa CadQuery) | Proposto | Prima parte tecnica modellata ed esportata in STEP/STL |
| `CAND-022` | Componenti dello schema rev 0.2 e codici LCSC come in [12](12-selezione-componenti.md) (ESP32-C3-WROOM-02-N4, TYPE-C-31-M-12, USBLC6-2SC6, PTC BSMD0805-050-12V, TLV75533, AO3401A; JST PH e header 1×8 a foro passante saldati a mano, `DEC-043`, `DEC-049`) | Proposto | Prototipo M1, revisione schema, stock al momento dell'ordine |
| `CAND-023` | Assegnazione GPIO dell'ESP32-C3 (modulo WROOM-02, vedi [02](02-architettura-hardware.md) §3.1): ESP32-C3 sufficiente, S3 non necessario | Proposto | Prova sulla dev board M1 (strapping IO2/IO8/IO9, `DISP_EN_N` su IO20 per Q1; niente PWM, `DEC-034`) |
| `CAND-025` | Scheda principale rev 0.2 **50,5 × 41,5 mm** (`DEC-045`) posizionata e sbrogliata in bozza (vedi [02](02-architettura-hardware.md) §3.2) | Proposto | Studio volumetrico 1:1 (`OPEN-028`); sbroglio approvato a vista dal proprietario (`OPEN-027` chiusa) |
| `CAND-024` | Un solo PCB custom (scheda principale); display, SHT40 e RTC su moduli commerciali | Proposto | Preventivo JLC |
| `CAND-026` | **Base a "D"** 78,5 × 76,3 × 24,1 mm (retro piatto con la USB-C, fronte arrotondato): guscio con piano superiore e **fondo apribile** come sportello di servizio; scheda appesa a due colonnine con viti M2 dal basso; DS3231 in una culla sotto il piano con la pila verso il fondo; camera SHT40 ventilata sul lato destro; zavorra nella striscia anteriore (vedi [06](06-progettazione-meccanica.md) §12) | Proposto | Render e stampa di prova 1:1 con la scheda reale |
| `CAND-027` | **Header J2 diritto** negli stessi fori (ammesso da `DEC-043`): la spina Dupont sale in verticale nel canale del cavo sopra la base | Proposto (`OPEN-031`) | Scelta del proprietario, che salda l'header |

## 3. Questioni aperte con priorità

| ID | Priorità | Questione | Evidenza/decisione necessaria |
|---|---|---|---|
| `OPEN-001` | P0 | Display + portadisplay entrano nella testa desiderata? | Quote del pannello e della schedina, CAD |
| `OPEN-002` | P1 | Cavo per il modulo SHT40: lunghezza, percorso nel corpo, ordine dei pin del modulo acquistato? | Connettore lato scheda deciso (J3, JST PH 4 poli, `DEC-043`); serigrafia del modulo, CAD |
| `OPEN-003` | — | ~~Quale LiPo~~ | Chiusa da `DEC-023` |
| `OPEN-004` | P1 | Quanta corrente assorbe il dispositivo in DIM/BRIGHT/NIGHT? | Misura su banco (M1); serve per calore e scelta del regolatore |
| `OPEN-005` | — | ~~Quale caricatore~~ | Chiusa da `DEC-023` |
| `OPEN-006` | — | ~~Target 48 h~~ | Chiusa da `DEC-023` |
| `OPEN-007` | P0 | Come impostare inizialmente ora/data offline? | Risolto in progetto: configuratore da PC via USB (`DEC-020`), menu pulsante come riserva; da verificare in `VT-FW-007` |
| `OPEN-008` | P1 | Posizione e tipo di sportello manutenzione? | **Proposta** (2026-11-09): il fondo della base è lo sportello (2 viti M2,5 davanti e 2 linguette dietro). Aperto dà accesso al retro della scheda (TP6/TP11 per il recupero), alle viti, alla pila del DS3231 e alla zavorra ([06](06-progettazione-meccanica.md) §12). Da approvare e provare (`VT-MEC-002`) |
| `OPEN-009` | P2 | Serve il light-sleep? Se sì, il pulsante risveglia l'MCU in modo affidabile? | Misure termiche M1/M5 |
| `OPEN-010` | — | ~~Soglie batteria~~ | Chiusa da `DEC-023` |
| `OPEN-011` | P1 | SHT40 legge realmente l'aria stanza o il calore interno (permanente con alimentazione continua)? | Test di confronto a regime con scocca chiusa. Proposta dello studio: camera separata sul lato destro della base, con feritoie sulla parete e nel fondo, a circa 25 mm dall'LDO |
| `OPEN-012` | P2 | Colori capelli, posa braccia e finitura cappello? | Approvazione concept/campione stampa |
| `OPEN-013` | — | ~~Temperatura della cella in carica~~ | Chiusa da `DEC-023` |
| `OPEN-014` | P2 | Per quanto tempo l'ora sopravvive a cavo scollegato? | Tampone scelto: pila CR1220 del modulo DS3231 (`DEC-024`), durata attesa di anni secondo Adafruit; verificare con `VT-FW-001` passo 5 |
| `OPEN-015` | P2 | Il menu con **un solo pulsante** è sufficientemente usabile come riserva? | Prototipo dell'interazione; il metodo principale è il configuratore (`DEC-020`) |
| `OPEN-016` | P1 | Il modulo display ricevuto ha il pinout atteso (RST, CS, DC, SDA, SCL, GND, VCC) e quanta corrente assorbe la retroilluminazione? Quali sono le quote reali del modulo (PCB, aletta dei pin, spessore)? | Modulo scelto (`DEC-034`); verifica della serigrafia e misura su banco prima del collegamento a J2. Il blockout usa un segnaposto di 38 × 45,5 × 4,8 mm con l'aletta in basso: la testa va confermata sul modulo misurato ([06](06-progettazione-meccanica.md) §12) |
| `OPEN-017` | P1 | Dove posizionare il pulsante nella statuetta? | Proposte (2026-11-09, [06](06-progettazione-meccanica.md) §12): **A** sulla sommità del cappello (si preme verso il basso, nessun rischio di ribaltamento); **B** sul fronte della base (cavo corto). Sconsigliato sul petto: la spinta a circa 65 mm d'altezza può ribaltare la statuetta. Scelta del proprietario |
| `OPEN-018` | — | ~~Montare il touch nella V1?~~ | Chiusa da `DEC-034` (niente touch) |
| `OPEN-019` | — | ~~GPIO e connettore per il touch~~ | Chiusa da `DEC-034`; IO0 libero su TP9; IO1 legge il BUSY di un eventuale e-paper dal `DEC-049` (TP10) |
| `OPEN-020` | — | ~~Dove va la scheda principale (busto/base o testa)?~~ | **Chiusa da `DEC-048`** (2026-11-09): nella base, USB-C sul retro della base, nessuna prolunga |
| `OPEN-021` | P1 | Il SPI del display è stabile sul cavetto Dupont a 7 fili della lunghezza reale? | Prova M1 con cavetto reale e frequenza scelta (10–20 MHz); R8/R9 22 Ω. Lunghezza dal blockout: percorso fra le due spine di circa 65 mm, quindi **cavetto Dupont da 10 cm** ([06](06-progettazione-meccanica.md) §12) |
| `OPEN-022` | P1 | Come esce il cavo USB dal retro della base (`DEC-048`) senza far ribaltare la statuetta? | Proposta dello studio ([06](06-progettazione-meccanica.md) §12): asse della USB-C a 9,1 mm dal piano, apertura 13,4 × 7,6 mm in cui entra il sovrastampo della spina, scheda appesa a due colonnine con viti M2 (lo sforzo va sulla scocca), zavorra anteriore da 75 a 128 g. Dal calcolo servono circa 8 N di trazione all'indietro per ribaltarla; resta da provare con `VT-MEC-003` |
| `OPEN-023` | — | ~~Orientamento del cavo FFC~~ | Chiusa da `DEC-034` (niente FFC); J2 ha pin 1 = VCC serigrafato sul retro |
| `OPEN-024` | — | ~~Corrente della retroilluminazione LEDA/LEDK~~ | Chiusa da `DEC-034`: la retroilluminazione è gestita dal modulo; misura della corrente in `OPEN-016` |
| `OPEN-025` | — | ~~Stabilità AMS1117 con MLCC~~ | Chiusa da `DEC-037` (TLV75533) |
| `OPEN-027` | — | ~~Lo sbroglio automatico (Freerouting) della rev 0.2 è adeguato?~~ | **Chiusa il 2026-11-08**: il proprietario ha rivisto il PCB a vista in KiCad e l'ha approvato (rev 0.2 con coppia USB simmetrica e correzioni del 2026-11-08), §9 |
| `OPEN-028` | P0 | **Base: PASS nello studio del 2026-11-09** (scheda invariata, nessuna interferenza, metallo ad almeno 15 mm dall'antenna, [06](06-progettazione-meccanica.md) §12). Restano il modulo display reale (`OPEN-016`), l'SHT40 reale e la prova 1:1 dei connettori (FIN-011). La chiusura del gate per l'ordine del PCB spetta al proprietario. Domanda originale: studio volumetrico 1:1 (revisione P0-05): scheda 50,5 × 41,5 mm (`DEC-045`), modulo display, cavetti, USB-C e spina, RTC, SHT40 e zavorra entrano nella statuetta? Con `DEC-043`: connettori JST PH alti circa 6 mm con ingresso dall'alto e piedini a foro passante di J2–J5 sotto la scheda (serve luce sotto) | Bozza CAD quotata con lo STEP della scheda; gate aperto prima dell'ordine |
| `OPEN-030` | — | ~~Il layout dopo `DEC-043`, `DEC-044` e `DEC-045` è accettabile? (FIN-002)~~ | **Chiusa il 2026-11-08**: il proprietario ha rivisto a vista in KiCad il commit `09200dc` e approva le modifiche (§13) |
| `OPEN-026` | P2 | Dove alloggiare il modulo DS3231 (quote dal disegno Adafruit, cavo JST PH → JST-SH, `DEC-043`) nella statuetta, accessibile per cambiare la pila CR1220? | **Proposta** (2026-11-09): culla con due guide sotto il piano della base, nell'angolo posteriore destro, con la pila rivolta verso il fondo apribile. La pila si cambia togliendo il fondo, senza staccare cavi ([06](06-progettazione-meccanica.md) §12). Quote del modulo: 25,4 × 17,8 × 7,8 mm (pagina Adafruit 5188, letta il 2026-11-09). Da approvare |
| `OPEN-031` | P1 | Header J2 **diritto o a 90°**? | Con l'header diritto la spina sale in verticale nel canale sopra la base. Con quello a 90° spina e piega dei fili richiedono circa 25 mm di base in più davanti alla scheda. Lo studio consiglia il diritto (`CAND-027`); decide il proprietario, che salda l'header |
| `OPEN-032` | P1 | Quale **servizio di stampa online** (`DEC-052`), con quale tecnologia (FDM, SLS/MJF in nylon, resina) e quali materiali e colori? | Regole del servizio (spessori minimi, tolleranze, colori, finitura) da leggere sulle sue pagine. Decidono come dividere i pezzi e i giochi, oggi 0,3 mm come segnaposto |
| `OPEN-029` | — | ~~La capacità d'ingresso a monte dell'LDO (C1 + C2 = 20 µF nominali su VBUS, senza limitazione dello spunto) è accettabile per le porte USB di PC e hub? | Rilievo REV-002 della [revisione del 2026-11-08](revisioni/2026-11-08/README.md). Scelta del proprietario: ridurre i condensatori d'ingresso fino a ≤ 10 µF effettivi, oppure misurare la corrente d'inserzione e VBUS (`VT-PWR-001/003`)~~ | Chiusa da `DEC-042`; la misura resta in `VT-PWR-001` |

## 4. Come si chiude una decisione

Una questione aperta passa a `DEC-xxx` soltanto con: data, alternativa scelta, motivazione, vincoli, test/evidenza e file di specifica aggiornati. È ammesso respingere una proposta: non bisogna comprare componenti solo perché già presenti nel concept grafico.

## 5. Decisioni di sicurezza non negoziabili

Prima della chiusura della statuetta devono essere confermati: protezione dell'ingresso USB (fusibile/PTC, ESD), temperature interne in funzionamento continuo, fissaggio di connettori e cavi. Se in una versione futura verrà reintrodotta una batteria, tornano obbligatorie le verifiche di compatibilità cella ↔ caricatore, cutoff termico, protezione e polarità. Nessun render o preventivo può sostituire questa evidenza.

## 6. Revisione tecnica indipendente del 2026-11-07

Esito sulla rev 0.1: **NOT APPROVED FOR FABRICATION** (file del proprietario, non nel repository). Stato dei rilievi nella rev 0.2:

| Rilievo | Stato | Dove |
|---|---|---|
| P0-01 batteria | Confermato dal proprietario: V1 senza batteria | `DEC-038` |
| P0-02 pannello display | Superato: modulo a 7 pin scelto; pinout da verificare sul modulo ricevuto | `DEC-034`, `OPEN-016` |
| P0-03 orientamento FFC e portadisplay | Superato: niente FFC né portadisplay | `DEC-034` |
| P0-04 AMS1117 + MLCC | Corretto: TLV75533, condensatori a 2,4–2,8 mm dai pin | `DEC-037` |
| P0-05 studio volumetrico | **Aperto** (gate prima dell'ordine) | `OPEN-028` |
| P1-01 disaccoppiamento ed EN | Corretto nel layout rev 0.2; tasti RESET/BOOT tolti (`DEC-039`) | [02](02-architettura-hardware.md) §3.2 |
| P1-02 USB D+/D- | Corretto: coppia simmetrica tracciata a mano (`DEC-041`), ESD a passaggio diretto vicino al connettore, stesse lunghezze e stesse vie su D+ e D-, piano GND sul retro libero sotto la coppia fra ESD e modulo | [02](02-architettura-hardware.md) §3.2 |
| P1-03 GND e antenna | Corretto: piani GND su due strati, zona antenna senza rame sopra l'intaglio (poi antenna sulla scheda con zona vietata, `DEC-045`) | [02](02-architettura-hardware.md) §3.2 |
| P1-04 retroilluminazione | Superato (gestita dal modulo); corrente da misurare | `OPEN-016` |
| P1-05 variante ESP32 | Corretto: H4X | `DEC-035` |
| P1-06 strapping I²C | Prova di boot aggiunta | [07](07-piano-verifica.md) `VT-PCB-004` |
| P1-07 serigrafia e punti di test | Corretto: 0 avvisi DRC, etichette con nome della rete | [02](02-architettura-hardware.md) §3.2 |
| P1-08 footprint e controlli DRC | Corretto: controlli courtyard riabilitati, USB-C dalla libreria KiCad, JST-SH confrontati | [12](12-selezione-componenti.md) §1 |
| P1-09 LED/regolatori dei breakout | Verifica aggiunta in BOM | [08](08-bom-preliminare.md) `BOM-002` |
| P1-10 leggibilità 1,28" | Confermato dal proprietario; test 1:1 in `VT-UI-001` | `DEC-038` |
| Regole JLCPCB (vincolo `SC-008` aggiunto dopo la revisione) | Impostate nel DRC e nel posizionamento | `DEC-040`, `PR-REL-008` |
| P2 README, stato documenti, costi | Aggiornati; "report salvati" distinti da "test eseguiti" | [hardware](../hardware/README.md), [08](08-bom-preliminare.md) §8 |

## 7. Correzioni richieste dopo la revisione del 2026-11-08

Il proprietario ha richiesto esclusivamente la correzione della distanza dal bordo (REV-001) e dei courtyard incompleti (REV-003), con documentazione e **senza commit prima della verifica visiva**. Le decisioni `CONF` restano invariate; non si introduce una nuova decisione di prodotto.

- C7 spostato di 0,75 mm verso l'interno, corpo-bordo da 1,85 a **2,60 mm**; ritoccati i raccordi locali EN/GND e una via EN.
- Courtyard e contorni F.Fab dell'header e dei due JST-SH completati in libreria e nelle istanze J2–J5; pad e pinout conservati.
- FID1 e la sua zona di rispetto spostati di 1,5 mm per liberare il courtyard completo di J5.
- Controllo geometrico aggiuntivo su tutto il contorno e sulle piazzole nei courtyard; ERC/DRC e parità schema/PCB senza violazioni. J1/J2/U3 rimangono eccezioni da sottoporre al DFM JLC.

Stato: **correzioni preparate e commit successivamente autorizzato dal proprietario** sul nuovo ramo `codex/pcb-edge-courtyard-fixes`. Gli altri rilievi restano rinviati; i gate di approvazione alla produzione rimangono aperti. [Nota completa, evidenze e file da aprire](revisioni/2026-11-08/correzioni/README.md). Nessun ordine eseguito.

## 8. Verifica indipendente delle correzioni Codex e chiusura dei rilievi (2026-11-08)

Verifica svolta da Claude sul commit `16f9bf7`, confrontato con `4fb9200`. Esito: le correzioni di REV-001 e REV-003 sono **confermate**.

- ERC, DRC con zone ricalcolate e parità rieseguiti: tutti a 0. Il controllo meccanico risulta PASS.
- Spostati solo C7 e FID1, ritoccate solo le reti EN e GND. La coppia USB è identica e le piazzole J2–J5 sono invariate.
- Rilievo nuovo **VER-001**: il testo di `DEC-040` limitava i 2,5 mm ai lati sinistro e destro. Ora è allineato a tutto il contorno.

Poi, su richiesta del proprietario, sono stati chiusi gli altri rilievi:

| Rilievo | Correzione |
|---|---|
| REV-002 spunto USB | `DEC-042`: C1 1 µF, C2 4,7 µF, 5,7 µF nominali su VBUS; prova aggiunta a `VT-PWR-001` |
| REV-004 `esporta.py` | Si ferma su ERC/DRC con violazioni o su controllo meccanico fallito; DRC con zone ricalcolate |
| REV-005 firmware/UI | [04](04-specifiche-firmware.md) e [05](05-interfaccia-utente.md) senza PWM: DIM/BRIGHT solo con i colori della grafica, NIGHT con Q1 spento, sequenze di accensione e spegnimento, transizione `NIGHT_PEEK → DIM`; corretti `CAND-023` e il diagramma di [03](03-alimentazione-ricarica.md) |
| REV-006 schema | Cartigli rev 0.2, nota di recupero leggibile, niente tasti RESET/BOOT nel sommario, etichette IO9_BOOT e TP11 senza sovrapposizioni, riferimenti dei punti di test separati dai valori |
| REV-007 residui storici | `CODEX_HANDOFF.md` marcato come storico; backlog e rischi della [roadmap](09-roadmap.md) aggiornati |

Restano solo le verifiche fisiche e i gate già noti, cioè `OPEN-016`, `OPEN-021`, `OPEN-028` e la DFM JLC (la revisione a vista è chiusa, §9). Restano anche alcune sovrapposizioni puramente estetiche di testi negli altri fogli dello schema (U1, U2, F1, J3–J5), senza effetti elettrici. Dettagli nella [verifica di Claude](revisioni/2026-11-08/verifica-claude.md).

## 9. Revisione visiva del proprietario (2026-11-08)

- **PCB approvato a vista** dal proprietario in KiCad: rev 0.2 con coppia USB simmetrica (`DEC-041`), correzioni del bordo e dei courtyard e condensatori d'ingresso di `DEC-042`. `OPEN-027` è chiusa.
- **Sovrapposizioni estetiche dello schema** (U1, U2, F1, J3–J5 e altre) **corrette dal proprietario** in KiCad. Prima del commit, Claude ha verificato che sono solo grafiche: netlist esportata identica (53 reti, stessi componenti e valori), ERC 0, DRC 0/0/0 con parità e controllo meccanico PASS.
- Il salvataggio da KiCad ha scritto nel `.kicad_pro` le impostazioni predefinite di ERC e schema, oltre alla revisione `0.2`, senza cambiare le regole DRC.
- Il ramo `codex/pcb-edge-courtyard-fixes` è stato unito, su richiesta del proprietario, nel ramo `claude/hardware-schematic-4ff868`: le prossime modifiche hardware partono da lì. Nessun push e nessun merge in `main`.

Restano prima dell'ordine: studio volumetrico 1:1 (`OPEN-028`), verifica del modulo display ricevuto (`OPEN-016`), prototipo M1 con SPI sul cavetto (`OPEN-021`), disponibilità LCSC e DFM JLC (eccezioni J1/J2/U3), poi Gerber e preventivo con approvazione esplicita del proprietario.

## 10. Connettori a foro passante saldati a mano (`DEC-043`, 2026-11-08)

Modifica richiesta dal proprietario: J3, J4 e J5 diventano JST PH B4B-PH-K-S, J2 un header 1×7 2,54 mm a foro passante; li salda a mano il proprietario, JLC monta il resto (J1 compreso). Schema e PCB modificati direttamente nei file KiCad, che sono la fonte (i generatori non sono stati rieseguiti).

- **Schema**: nuovi simboli `PoliClock:B4B-PH-K-S` e `PoliClock:PinHeader_1x07_P2.54_THT` (stessa geometria dei pin 1–4 e 1–7, collegamenti invariati); J5 spostato di 2,54 mm per allineare i pin 1–2, pin 3–4 con NC espliciti; tolte le piazzole di montaggio 5/6 dei JST-SH e i loro NC; campo `Montaggio`, nessun campo LCSC. Netlist identica salvo le reti delle piazzole di montaggio tolte.
- **PCB**: impronte standard di KiCad 10, attributi "a foro passante" ed "escluso dai file di posizionamento". J2 con la fila dei fori a 4,4 mm dal bordo superiore (pin 1 = VCC ora a sinistra), J3/J4/J5 sul lato sinistro, pin 1 a x = 3 mm e y = 9 / 15 / 21 mm. Spostati R15, R19, R20, R21 e C8; etichette del retro aggiornate. Tolte le piste delle reti toccate e risbrogliate solo le connessioni mancanti (`sbroglia_main.py --conserva`): coppia USB (`DEC-041`), CC, VBUS/+5V ed EN invariati.
- **Gate**: `esporta.py` toglie dalla BOM JLC le parti con `Montaggio` a mano e controlla che BOM JLC e CPL abbiano gli stessi designatori; `verifica_meccanica_pcb.py` applica il margine di 2,5 mm solo alle parti nella CPL e controlla comunque i courtyard di J2–J5. Regola DRC in `policlock-main.kicad_dru`: ignorata solo la serigrafia di J2 oltre il bordo (non stampata).
- **Esito**: ERC 0; DRC con zone ricalcolate, tutte le severità e parità: 0 violazioni, 0 connessioni aperte, 0 problemi di parità; controllo meccanico PASS. BOM JLC 17 righe (senza J2–J5), CPL 32 componenti (erano 36), 44 vie, circa 972 mm di piste.
- **Eccezioni DFM residue**: J1 a filo del bordo inferiore e U3 sopra l'intaglio. J2 non è più un'eccezione JLC.

Restano aperti i gate già noti (`OPEN-016`, `OPEN-021`, `OPEN-028` con la luce sotto la scheda per i piedini a foro passante, DFM JLC). Nessun file Gerber e nessun ordine; serve una nuova revisione a vista del proprietario in KiCad.

## 11. Modulo WROOM-02 ed esito della revisione finale (`DEC-044`, 2026-11-08)

La [revisione finale pre-Gerber](revisioni/2026-11-08/revisione-finale/README.md) (commit `cd2505b`): esito **NON PRONTO** per FIN-001 e FIN-002. Il proprietario ha scelto il modulo ESP32-C3-WROOM-02-N4 (`DEC-044`) e approvato le correzioni sotto.

| Rilievo | Stato | Cosa è cambiato |
|---|---|---|
| FIN-001 modulo "Standard Only" | **Risolto** con `DEC-044` | WROOM-02-N4 (C2934560) "Economic and Standard", senza radiografia; `DEC-040` resta "Economic" |
| FIN-002 revisione a vista dopo `DEC-043` | **Chiuso** (`OPEN-030`, §13) | Revisione a vista del proprietario sul layout `09200dc` positiva |
| FIN-003 calo di 3V3 all'accensione del display | **Corretto** | R16 da 1 k a 10 k (C25804), C11 10 nF (C57112, Basic) fra gate e drain di Q1, montato; V_GS in conduzione ≈ −3,0 V con R17 100 k. Misura comunque in `VT-PWR-003` |
| FIN-004 rotazioni CPL | **Procedura** | Tabella di controllo parte per parte in [12](12-selezione-componenti.md) §7; CPL non modificata a priori |
| FIN-005 testi della serigrafia | **Corretto** | Testi del retro a 1,0 mm con tratto 0,15 mm, etichette accorciate; `min_text_height` 1,0 mm e `min_text_thickness` 0,15 mm nel `.kicad_pro` |
| FIN-006 procedura Gerber | **Corretto** | `hardware/scripts/esporta_gerber_jlc.py`, eseguibile solo con `--conferma-proprietario`; **non eseguito**. Impostazioni dalla guida JLC per KiCad (2026-09-09) e controlli da fare dopo nel visualizzatore |
| FIN-007 regole DRC e minimi JLC | **Corretto** | Regola in `.kicad_dru`: anello delle piazzole PTH ≥ 0,18 mm. Linee di serigrafia delle impronte standard a 0,12 mm: lasciate come in libreria (cambiarle renderebbe le impronte diverse dalla libreria); JLC le stampa al proprio minimo, da guardare nell'anteprima |
| FIN-008 cucitura GND | **Corretto** | 4 vie termiche nella EPAD (poi tolte, `DEC-046`), 15 vie di cucitura lungo il contorno e vicino all'intaglio con `cucitura_gnd.py`, nessuna nella zona USB |
| FIN-009 documenti ↔ PCB | **Corretto** | Larghezze delle alimentazioni (0,3–0,4 mm), vie, posizioni dei passivi, tolto "0,10 mm fra le piazzole USB-C", tolti dal `.kicad_pro` e da `sbroglia_main.py` i modelli di rete `*LCD_LEDK`/`*BL_D` |
| FIN-010 linee esterne senza ESD | **Rischio accettato** | Il proprietario non ha scelto la 1 kΩ in serie sul pulsante: documentato in [12](12-selezione-componenti.md) §6 |
| FIN-011 impronta JST PH | **Nota per il proprietario** | Prova 1:1 con i suoi B4B-PH-K-S prima dei Gerber, [12](12-selezione-componenti.md) §6 |

**Verifiche (2026-11-08, nessun test su hardware):** ERC 0; DRC con zone ricalcolate, tutte le severità, tutti gli errori delle piste e parità schema ↔ PCB: 0 violazioni, 0 connessioni aperte, 0 problemi di parità; controllo meccanico PASS (eccezioni DFM J1 e U3); `esporta.py` completo. BOM JLC 17 righe, CPL 33 componenti (C11 in più). Coppia USB: percorsi completi 13,73/13,73 mm (faccia B) e 18,41/18,41 mm (faccia A), 2 vie per rete sui rami dei contatti interni.

**Punti per la revisione a vista (`OPEN-030`):** posizione del modulo e dell'intaglio; uscita dei pin del lato superiore sotto il modulo; collegamento C5/C6 → pin 3V3 (circa 16 mm, 0,4 mm); EN (circa 27 mm, 2 vie); coppia USB fra i pin 13/14 e R3/R4; colonna di passivi a sinistra del modulo; cucitura GND; etichette del retro a 1,0 mm. Restano i gate già noti (`OPEN-016`, `OPEN-021`, `OPEN-028`, DFM JLC con le eccezioni J1/U3, anteprima delle rotazioni) e l'approvazione esplicita per generare i Gerber.

## 12. Contorno rettangolare e regola dei 2,5 mm senza eccezioni tranne J1 (`DEC-045`, 2026-11-08)

- **Contorno**: 50,5 × 41,5 mm, nessun intaglio; angolo in basso a sinistra fisso. U3 resta dove era (pin 13/14 sull'asse di J1): il bordo destro passa a x = 150,5 e quello superiore a y = 98,5 nel foglio KiCad.
- **Antenna**: sulla scheda, verso il bordo destro; zona vietata dell'impronta di U3 da x = 141,51 al bordo destro e da y = 98,5 a 124,5 (foglio), su F.Cu e B.Cu.
- **Spostati**: solo J2 (1,5 mm verso l'alto) e le piste delle sue reti; piani GND, fasce "bordo" e cucitura GND rifatti; una via GND vicino a J2 pin 2. Nessun componente montato da JLC si è mosso: CPL identica.
- **Controlli**: ERC 0; DRC con zone ricalcolate, tutte le severità e parità 0/0/0; controllo meccanico PASS con J1 unica eccezione; margine minimo dei corpi 2,99 mm (U3), poi U2 5,05 mm; `esporta.py` completo con lo STEP del nuovo contorno.
- La revisione a vista del proprietario (`OPEN-030`) è stata fatta il 2026-11-08 con esito positivo (§13). Nessun file Gerber.

## 13. Approvazione a vista del layout finale e seconda revisione (2026-11-08)

- Il proprietario ha rivisto in KiCad il commit `09200dc` (modulo ESP32-C3-WROOM-02-N4, scheda 50,5 × 41,5 mm senza intaglio con antenna sulla scheda, J2–J5 a foro passante, correzioni FIN della revisione finale) e **approva le modifiche**: `OPEN-030` / FIN-002 chiusi.
- Su richiesta del proprietario segue una **nuova revisione completa pre-Gerber** del revisore indipendente su questo layout: vincoli circuitali ed elettrici, PCB, regole JLCPCB, coerenza con decisioni e documentazione. I Gerber restano da generare solo dopo il suo esito e un'approvazione esplicita del proprietario.
- [Seconda revisione finale pre-Gerber](revisioni/2026-11-08/revisione-finale-2/README.md) su `a2a62a3`: esito **PRONTO CON RISERVE**, nessun P1; P2 R2-001 (tabella rotazioni U2/Q1 in [12](12-selezione-componenti.md) §7) e R2-002 (checklist di `esporta_gerber_jlc.py`), da correggere prima dell'ordine.

## 14. Chiusura delle riserve della seconda revisione (2026-11-08)

Su richiesta del proprietario sono state chiuse le riserve della [seconda revisione](revisioni/2026-11-08/revisione-finale-2/README.md). Si tratta solo di documentazione e testi dello script. Schema, PCB, BOM e CPL sono invariati.

| Rilievo | Esito |
|---|---|
| R2-001 (P2) tabella delle rotazioni | **Corretta** in [12](12-selezione-componenti.md) §7, con le posizioni dei pin lette dal PCB: U1 pin 1 in basso a sinistra; U2 pin 1 = IN in alto a sinistra; Q1 G in basso a sinistra, S in basso a destra, D in alto |
| R2-002 (P2) checklist di `esporta_gerber_jlc.py` | **Corretta**: contorno 50,5 × 41,5 mm rettangolare, zona antenna senza rame su F.Cu/B.Cu, vie della EPAD, testi del retro. Script non eseguito |
| R2-003 (P3) Q1 all'inserzione della USB | Osservazione di 3V3_DISP e `DISP_G` all'inserzione aggiunta a `VT-PWR-003`; attesa di almeno 2 ms dopo `DISP_EN_N` basso in [04](04-specifiche-firmware.md) §4 |
| R2-004 (P3) piste vicino alla zona antenna | Nessun impatto in V1 (radio spenta); nota per una V2 nel backlog della [roadmap](09-roadmap.md) |
| R2-005 (P3) disaccoppiamento 3V3 e EN lontani | Compromesso approvato a vista; misure di 3V3 al pin 1 e di EN aggiunte a `VT-PCB-002`; testo di [12](12-selezione-componenti.md) §6 corretto (pista di circa 21 mm) |
| R2-006 (P3) vie aperte nella EPAD | Controllo della EPAD nell'anteprima DFM aggiunto alla tabella di [12](12-selezione-componenti.md) §7 e alla checklist dei Gerber |
| R2-007 (P3) residui documentali | Corretti: sezioni rinumerate (§13), FIN-002 chiuso, `DEC-041` e `CAND-012` aggiornati, nota sull'intaglio in §6, impronta MINI-1 segnata come storica nel README hardware |

Restano i gate dell'**ordine**: studio volumetrico (`OPEN-028`), modulo display (`OPEN-016`), SPI sul cavetto (`OPEN-021`), prova 1:1 dei JST PH e dell'header (FIN-011, consigliata prima dei Gerber), DFM JLC per J1, scorte all'ordine. I Gerber si generano solo con l'approvazione esplicita del proprietario.

## 15. Revisione esterna del 2026-11-08 e azioni prima dei Gerber

Il proprietario ha fatto rivedere il progetto da un revisore esterno (`PoliClock_report_validazione_rev02_2026-11-08.md`). Esito: schema senza errori bloccanti e sbroglio da non rifare, ma **NO-GO all'ordine PCBA nello stato attuale** per tre punti di montaggio. Il revisore non disponeva di `kicad-cli`: ERC e DRC sono stati rieseguiti qui (0/0/0, controllo meccanico PASS).

| Rilievo | Esito |
|---|---|
| P1-01 centro di posa di U3 | **Fondato**: l'origine dell'impronta è il centro delle file di piazzole, mentre il corpo è spostato di 3,1 mm. `esporta.py` genera ora una **CPL alternativa**, `policlock-main-cpl-jlcpcb-u3-centro-corpo.csv`, con U3 a X 37,51 / Y 29,50 mm invece di 34,41 / 29,50. All'ordine si sceglie nell'anteprima JLC quella in cui piazzole e modulo coincidono ([12](12-selezione-componenti.md) §7) |
| P1-02 linguette di J1 senza saldatura garantita | **Fondato** (C165948 è "SMT Assembly"): `DEC-047`, saldatura a mano dal retro |
| P1-03 J1 a filo del bordo | Eccezione già prevista da `DEC-045`: la conferma arriva dalla DFM JLC, caricando i Gerber nel preventivo **senza ordinare** |
| P1-04 Gerber e forature assenti | Voluto: si generano solo con l'approvazione esplicita del proprietario (`esporta_gerber_jlc.py --conferma-proprietario`) |
| P2-01 vie aperte nella EPAD | **Corretto** con `DEC-046`: vie tolte, DRC 0/0/0, EPAD collegata a GND |
| P2-05 ponti di maschera fra i contatti USB-C, P2-06 fiducial, P2-07 rotazioni | Checklist dell'anteprima JLC in [12](12-selezione-componenti.md) §7 |
| P2-02, P2-03, P2-04, P2-10 termica dell'LDO, disaccoppiamento, strapping, attenuazione grafica | Misure già nel piano di verifica (`VT-PWR-002/003`, `VT-PCB-002/004`, `VT-UI-001`) |
| P2-08 ingombri dei connettori saldati a mano | Prova 1:1 consigliata prima dei Gerber (FIN-011) e studio volumetrico `OPEN-028` |
| P2-09 radio ed EMC | Nessun effetto in V1 (`DEC-012`); nota per la V2 nella [roadmap](09-roadmap.md) |
| P3-01 stato approvativo unico | Lo stato aggiornato è questa sezione. Restano: prova 1:1 dei connettori, approvazione dei Gerber, DFM JLC senza ordine, poi i gate dell'ordine (`OPEN-028`, `OPEN-016`, `OPEN-021`) |

## 16. Pin BUSY su J2 per un eventuale display e-paper (`DEC-049`, 2026-11-09)

Richiesta del proprietario: aggiungere il pin BUSY, dopo aver verificato che IO0 o IO1 possano servire allo scopo. I moduli e-paper hanno VCC, GND, CLK, DIN, CS, DC, RST e BUSY. BUSY è un'uscita del display e un ingresso per l'MCU.

**Verifica di GPIO0 e GPIO1** (datasheet Espressif letti il 2026-11-09: [ESP32-C3 Series v2.4](https://documentation.espressif.com/esp32-c3_datasheet_en.pdf) del 2026-05-06 e [ESP32-C3-WROOM-02 v1.7](https://documentation.espressif.com/esp32-c3-wroom-02_datasheet_en.pdf) del 2026-03-05):

| Controllo | Esito | Fonte |
|---|---|---|
| Funzioni del pin | GPIO0 e GPIO1 hanno come funzione IO_MUX F0 il GPIO (I/O/T). Le funzioni analogiche XTAL_32K_P/N e ADC1_CH0/CH1 si attivano solo se configurate | C3 v2.4, tab. 2-4 e 2-6 |
| Pin di strapping | **No**: gli strapping sono GPIO2, GPIO8 e GPIO9 | C3 v2.4 §3; WROOM-02 v1.7 §4.1, tab. 4-1 |
| Restrizioni d'uso | "Priority 2": si possono usare senza restrizioni, con qualunque periferica, attraverso la matrice GPIO. Non sono fra i pin JTAG, USB, UART0 o flash | C3 v2.4 §2.3.3, §2.3.4, tab. 2-7 |
| Stato al reset e dopo il reset | Nessuna impostazione predefinita: niente IE, niente WPU/WPD. Finché il firmware non lo configura, il pin flotta con l'ingresso disabilitato, quindi non consuma e non va in conflitto con un'uscita esterna | C3 v2.4, tab. 2-1 |
| Glitch all'accensione | **Nessuno**: la tabella elenca solo MTCK, MTDO, GPIO10, U0RXD e GPIO18 | C3 v2.4, tab. 2-2 |
| Quarzo da 32 kHz | Il modulo ha solo il quarzo da 40 MHz; GPIO0 e GPIO1 vanno diretti ai pin 18 e 17. Il quarzo da 32,768 kHz compare solo nello schema periferico, come opzione esterna non montata ("NC"), e su questa scheda non c'è | WROOM-02 v1.7, tab. 3-1, fig. 8-1 e 9-1 |
| Funzione SPI | **Non serve**: BUSY non è un segnale della periferica SPI. È un ingresso GPIO che il firmware legge per livello o per interruzione | — |
| Livelli | VIH ≥ 0,75 × VDD, VIL ≤ 0,25 × VDD; pull-up e pull-down interni da circa 45 kΩ | C3 v2.4, tab. 5-4 |

**Scelta: IO1** (pin 17), come proposto. Per questo uso i due pin sono equivalenti; così IO0 resta libero su TP9 e TP10 resta su IO1 per misurare BUSY.

**Circuito.** J2 pin 8 (`DISP_BUSY_C`) → R23 1 kΩ → `DISP_BUSY` → IO1.
- **R23 1 kΩ** (C21190 Uni-Royal 0603WAF1001T5E, Basic, "Economic and Standard", [pagina JLC](https://jlcpcb.com/partdetail/C21190) letta il 2026-11-09; il codice non era ancora nella BOM). Limita la corrente in due casi: IO1 configurato per errore come uscita mentre il display pilota BUSY, oppure modulo spento da Q1 con IO1 alto. Al massimo circa 2,7 mA, invece di decine di mA attraverso i diodi di protezione del display.
- **Livello definito: pull-down interno di IO1**, che il firmware abilita. Con R23 in serie il livello alto letto vale circa 3,3 × 45/46 ≈ 3,2 V, ben sopra VIH (2,5 V).
- **Perché pull-down e non pull-up**: con il modulo spento o assente non passa corrente verso il display, e con il GC9A01 (pin 8 libero) IO1 legge 0.
- **Perché nessun pull esterno**: è un componente in meno, e prima della configurazione l'ingresso è disabilitato, quindi non importa che il pin flotti.
- **Polarità di BUSY**: dipende dal controller e-paper (in molti controller alto = occupato, in altri basso). La gestisce il firmware, sempre con un timeout ([04](04-specifiche-firmware.md) §4).

**PCB.**
- **J2**: impronta `PinHeader_1x08_P2.54mm_Horizontal`, stessa fila e stessa rotazione. Con il pin 1 fermo, il pin 8 cadrebbe a x = 27,66 mm (coordinate di [02](02-architettura-hardware.md) §3.2), cioè sotto il corpo di U3, che inizia a 27,51 mm. Perciò l'header si sposta di un passo (2,54 mm) a sinistra:
  - pin 1 passa da x = 9,88 a **7,34 mm**;
  - pin 8 prende il posto del vecchio pin 7 (25,12 mm);
  - il cavetto Dupont a 7 fili si infila sui pin 1–7 come prima (pin 1 = VCC, piazzola quadrata).
- **R23** è sotto J2 pin 8, a (25,3; 5,45) mm.
- **Piste tolte e risbrogliate**: 92 tra piste e vie (quelle delle reti di J2 e quelle in conflitto con le nuove piazzole), poi `sbroglia_main.py --conserva`.
- **DISP_BUSY**: 67 mm con 2 vie.
  - Passa sul retro sotto la fila superiore di piazzole di U3 e scende lungo il lato destro del modulo, a 0,22 mm dalla zona antenna ma fuori dalla zona.
  - È la stessa situazione di LCD_CS in R2-004: nessun effetto in V1, con la radio spenta.
  - Una prova con una zona vietata temporanea lungo l'antenna dava 76 mm e violazioni: scartata.
- **Via GND** a (30,6; 8,0) mm sotto U3: ricollega al piano un'isola GND del retro che la nuova pista aveva chiuso.
- **LCD_SCLK_C**: pista fra le piazzole di C5 riportata a 0,15 mm.
- **Cucitura GND** rifatta (14 vie).
- **Cosa non cambia**: nessun componente montato da JLC si è spostato, e nella CPL c'è solo la nuova riga di R23. Coppia USB (41 piste bloccate, identiche), J1, U1, R3, R4, U3, zona antenna e contorno sono invariati.
- **Totale**: 62 vie, circa 1166 mm di piste.
- **Script**: `hardware/scripts/dec049_schema.py` e `dec049_pcb.py` (ritocchi descritti nel docstring).

**Controlli.**
- ERC: 0.
- DRC con zone ricalcolate, tutte le severità e parità: **0/0/0**.
- Controllo meccanico: PASS, con J1 unica eccezione; margine minimo 2,99 mm (U3), R23 a 6,5 mm.
- `esporta.py`: completo (BOM JLC 18 righe, CPL 34 componenti, CPL alternativa con U3 al centro del corpo).
- Nessun Gerber.

**Per il CAD (`OPEN-028`).**
- J2 è più lungo di un pin: 8 × 2,54 = 20,3 mm invece di 17,8.
- La fila parte 2,54 mm più a sinistra: pin da x = 7,3 a 25,1 mm dal bordo sinistro.
- Un e-paper avrebbe bisogno di un cavetto a 8 fili ([06](06-progettazione-meccanica.md)).

## 17. Correzioni dopo la terza revisione (2026-11-09)

La terza revisione pre-Gerber su `edcef25` ha dato esito **PRONTO CON RISERVE**, con un P2 e quattro P3. Il rapporto è nel ramo del revisore `claude/revisione-finale-ea91f4`, commit `f9853b6`, file `docs/revisioni/2026-11-09/revisione-finale-3/README.md`; questo ramo non lo contiene. Il proprietario ha chiesto la correzione ("Sì, correggi").

| Rilievo | Esito |
|---|---|
| R3-001 (P2) isola GND del retro sotto U3 | **Corretto con vie GND**, cioè la correzione 2 del rapporto, prevista se a sinistra di U3 non c'è spazio. Sbrogliare di nuovo DISP_BUSY a sinistra del modulo non è possibile senza spostare altre reti (dettagli sotto la tabella). Aggiunte 5 vie GND 0,6/0,3 mm coperte dalla maschera: 4 accanto alla EPAD (a ≥ 0,5 mm dal bordo della piazzola, fuori dalla piazzola come chiede `DEC-046`) fra il rame superiore principale e il retro sotto U3, e 1 verso il pin 9 nell'isola del rame superiore di U3.9/C6.2 |
| R3-002 (P3) DISP_BUSY vicino alla zona antenna | **Non risolto**: il percorso resta, perché lo sbroglio a sinistra non è possibile. DISP_BUSY è aggiunta alla nota V2 della [roadmap](09-roadmap.md) accanto a LCD_CS. Nessun effetto in V1 (`DEC-012`) |
| R3-003 (P3) isola del retro di 249 mm² con una via | **Corretto**: 3 vie GND (vicino a R16/Q1, a C9 e sotto TP3), fuori dai courtyard; con la via verso il pin 9 di U3 l'isola ha ora 5 vie |
| R3-004 (P3) clock RTC lento | **Corretto** in [04](04-specifiche-firmware.md) §4: sorgente `CONFIG_RTC_CLK_SRC_INT_RC`, mai `CONFIG_RTC_CLK_SRC_EXT_CRYS` né `CONFIG_RTC_CLK_SRC_EXT_OSC`; nomi verificati in `components/esp_hw_support/port/esp32c3/Kconfig.rtc` di ESP-IDF v6.0 e v6.1, dove l'RC interno è il valore predefinito. Niente ADC su IO1 |
| R3-005 (P3) residui | **Corretti**: EPAD senza vie in [02](02-architettura-hardware.md) §3.2; `CAND-022` con l'header 1×8; [12](12-selezione-componenti.md) con le decisioni fino a `DEC-049` e la scorta di C2934560 letta dal revisore il 2026-11-09 (11 626); commenti di `policlock-main.kicad_dru`; nota su `DEC-048` non usato (numero poi assegnato alla scheda nella base, ramo della modellazione 3D); `DEC-046` dichiara lo scostamento dalla fig. 11-1 del datasheet. La serigrafia "DISP 1=VCC" resta com'è (modifica facoltativa) |

**Perché DISP_BUSY non passa a sinistra di U3.** R23 sta in alto a sinistra del modulo, il pin 17 e TP10 in basso a destra. Fra i due punti il retro è attraversato senza interruzioni da:
- la diagonale +3V3 da 0,4 mm, da (125; 124) a (140,41; 108,59), che prosegue a sinistra verso TP3 e x = 122,4;
- il fascio parallelo IO0 / I2C_SDA / BTN_USER;
- DISP_EN_N (verticale a x = 125,66 e orizzontale a y = 118,82) e LCD_MOSI (via (126,70; 118,22) e verticale a x = 129,53).

Sul rame superiore, fra la colonna C5/C6/R8/R9 e il modulo, ci sono le piste GND e +3V3 da 0,4 mm. Il tratto esistente di DISP_BUSY (via di IO1) è il più esterno del fascio, quindi va raggiunto attraversando tutte le altre reti. Due prove con Freerouting (`--conserva` e zone vietate temporanee sopra e a destra del modulo) non hanno trovato un percorso a sinistra, oppure ne hanno trovato uno di 83 mm che passa vicino a J1: scartate. Il percorso a sinistra richiederebbe di sbrogliare di nuovo anche DISP_EN_N, LCD_MOSI e il +3V3 del retro, cioè una modifica più ampia di quella richiesta.

**Vie aggiunte** (coordinate del foglio KiCad; tra parentesi quelle di [02](02-architettura-hardware.md) §3.2):

| Via | Collega | Rilievo |
|---|---|---|
| (131,4; 111,6) = (31,4; 11,6), a sinistra della EPAD | rame superiore principale ↔ retro sotto U3 | R3-001 |
| (134,2; 108,4) = (34,2; 8,4), sopra la EPAD | rame superiore principale ↔ retro sotto U3 | R3-001 |
| (136,7; 110,8) = (36,7; 10,8), a destra della EPAD | rame superiore principale ↔ retro sotto U3 | R3-001 |
| (133,2; 114,1) = (33,2; 14,1), sotto la EPAD | rame superiore principale ↔ retro sotto U3 | R3-001 |
| (127,2; 102,6) = (27,2; 2,6), vicino al pin 9 | isola superiore U3.9/C6.2 ↔ isola del retro di 249 mm² | R3-001 |
| (119,3; 112,3) = (19,3; 12,3) | rame superiore principale ↔ isola del retro di 249 mm² | R3-003 |
| (121,0; 121,5) = (21,0; 21,5) | rame superiore principale ↔ isola del retro di 249 mm² | R3-003 |
| (123,5; 128,5) = (23,5; 28,5) | rame superiore principale ↔ isola del retro di 249 mm² | R3-003 |

**Isole del piano GND** (riempimento in memoria con il Python di KiCad, come nel rapporto; le vie della cucitura sono contate nel piano principale):

| Isola | `edcef25` | Dopo la correzione |
|---|---|---|
| Retro sotto U3 (x 129,6–140,3, y 101,4–117,9; 95,4 mm²) | 2 vie: (139,5; 103,5) e (130,6; 108,0) | **6 vie**: le 2 di prima e 4 nuove accanto alla EPAD |
| Rame superiore U3.9/C6.2 (x 125–140,8, y 100–108,3; 31,7 mm²) | 1 via: (139,5; 103,5) | **2 vie**: (139,5; 103,5) verso il retro sotto U3 e (127,2; 102,6) verso l'isola di 249 mm² |
| Retro zona J2/passivi (x 109–128,8, y 101,8–130,6; 249 mm²) | 1 via: (112,4; 104,3) | **5 vie**: (112,4; 104,3), 3 nuove dal rame superiore principale e (127,2; 102,6) |
| Piano principale del retro | 900 mm², 20 collegamenti | invariato |
| Piano principale del rame superiore | 1202 mm², 37 collegamenti | 1202 mm², 44 collegamenti |

Le piste non sono cambiate: DISP_BUSY resta di 67,5 mm con 2 vie. Coppia USB (41 piste bloccate), `usb_coppia_retro`, J1, U1, R3, R4, U3, zona antenna, contorno, BOM e CPL sono invariati. Totale **70 vie** (62 + 8), circa 1166 mm di piste.

**Controlli:**
- ERC 0;
- DRC con zone ricalcolate, tutte le severità e parità: **0/0/0**;
- controllo meccanico PASS (J1 unica eccezione, margine minimo 2,99 mm);
- `esporta.py` completo (BOM JLC 18 righe, CPL 34 componenti, CPL alternativa).

Nessun Gerber.

## 18. Scheda nella base, studio volumetrico e blockout (2026-11-09)

- **Decisioni del proprietario**: `DEC-048` (scheda nella base d'appoggio, USB-C sul retro della base), `DEC-051` (chibi in piedi, niente battuta del sedere), `DEC-052` (stampa con un servizio online). L'altezza si ricava dal volume (`CAND-008`, circa 150 mm). Il proprietario manderà riferimenti di stile: fino ad allora il blockout resta neutro.
- **Studio volumetrico** con build123d (`mechanical/cad/studio_base.py`): base 78,5 × 76,3 × 24,1 mm, scheda rev 0.2 invariata, nessuna interferenza, metallo ad almeno 15 mm dall'antenna (minimo 15,1 mm, vite M2 di H2). Rapporto in `mechanical/cad/studio_base_rapporto.txt`, dettagli in [06](06-progettazione-meccanica.md) §12.
- **Blockout** in Blender (`mechanical/blender/blockout_chibi.py`), render in `assets/renders/`. Il modulo display segnaposto richiede una testa di circa 68 × 56 × 70 mm.
- **Domande al proprietario**: header J2 diritto o a 90° (`OPEN-031`), posizione del pulsante (`OPEN-017`), sportello sul fondo (`OPEN-008`), alloggio del DS3231 (`OPEN-026`), servizio di stampa (`OPEN-032`), chiusura di `OPEN-028` per la parte scheda, commenti sui render.
