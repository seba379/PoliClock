# 10 — Decision log e questioni aperte

**Versione:** 0.9 · **Data:** 2026-11-08

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
| `DEC-018` | 2026-11-07 | Presa USB-C nella **parte posteriore bassa** della statuetta (sul sedere, per ironia); collegamento al PCB in `DEC-021` | Vincola foro, fissaggio e stabilità con cavo inserito |
| `DEC-019` | 2026-11-07 | ~~**Predisposizione touch** sul PCB~~ — **superata da `DEC-034`** (niente touch). Testo originale: predisposizione touch sul PCB (connettore/footprint, GPIO INT e RST riservati, componenti non montati); pulsante sempre presente; pannello scelto tra modelli disponibili con e senza touch a parità di ingombro | Il touch si potrà attivare senza rifare il PCB; decisione dopo la prova sul prototipo M1 (`OPEN-018`) |
| `DEC-020` | 2026-11-07 | **Configuratore da PC via USB** come metodo principale per impostare ora, data e fascia notte; menu con il pulsante come riserva | La USB nativa dell'MCU espone una porta seriale; protocollo documentato (`CAND-017`); configuratore web con Web Serial (`CAND-018`) |
| `DEC-021` | 2026-11-07 | **Scheda principale rettangolare separata dal display**, collegata a una **schedina portadisplay** nella testa con cavo (FFC o JST-SH) attraverso il collo; SHT40 su mini-PCB (superato da `DEC-028`: modulo commerciale); tutte nello stesso pannello JLC. Posizione della scheda principale decisa con la bozza CAD (`OPEN-020`): preferita nel busto/base con **USB-C saldata sulla scheda** affacciata al sedere; prolunga solo se la scheda va nella testa | Layout più semplice e sicuro, schema e PCB realizzabili da Claude con revisione visiva del proprietario; testa libera dai vincoli del PCB |
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
| `DEC-041` | 2026-11-08 | **Coppia USB D+/D- simmetrica, tracciata a mano** (ridisegnata per i pin 13/14 del WROOM-02 con gli stessi criteri, `DEC-044`) (`hardware/scripts/usb_coppia.py`, piste bloccate che Freerouting non tocca): connettore J1, USBLC6 (U1), R3/R4 e pin 26/27 del modulo sullo stesso asse; percorso principale B7/B6 → modulo speculare e senza vie; contatti interni A6/A7 incrociati con **2 vie per rete**; percorsi completi contatto → modulo **uguali** su entrambe le facce della spina; U1 a passaggio diretto (D- sui pin 1/6, D+ sui pin 3/4, canali scambiati nello schema), +5V del pin 5 sotto il corpo di R4 senza vie; retro libero da piste e vie sotto la coppia fra U1 e il modulo | Richiesta del proprietario: "ora che di spazio ne abbiamo, non voglio asimmetrie su D- e D+ dell'USB". Con i contatti del connettore nell'ordine D-, D+, D-, D+ un incrocio è inevitabile su 2 strati: va sui rami corti dei contatti interni, con lo stesso numero di vie su D+ e D-. Lunghezze e vie in [02](02-architettura-hardware.md) §3.2 |
| `DEC-042` | 2026-11-08 | **Capacità d'ingresso USB sotto 10 µF**: C1 (+5 V dopo il PTC) da 10 a **1 µF** (C15849) e C2 (ingresso LDO) da 10 a **4,7 µF** (C19666, X5R 16 V, Basic). Totale su VBUS 5,7 µF nominali, al massimo 6,3 µF | Scelta del proprietario sul rilievo REV-002 (`OPEN-029`): rientrare nei 10 µF ammessi all'inserzione USB senza aggiungere un limitatore di spunto. Il TLV75533 è stabile con ≥ 1 µF; stessa impronta 0603, nessuna modifica al rame. Spunto all'inserzione da misurare comunque in `VT-PWR-001` |
| `DEC-043` | 2026-11-08 | **Connettori J2–J5 a foro passante, saldati a mano dal proprietario**: J3 (SHT40), J4 (RTC) e J5 (pulsante) diventano **JST PH B4B-PH-K-S** (2,0 mm, verticali, impronta KiCad `JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical`; pinout 1 GND, 2 3V3_EXT, 3 SDA, 4 SCL; su J5 pin 1 BTN_USER, pin 2 GND, pin 3–4 non collegati); J2 diventa un **header 1×7 2,54 mm a foro passante** (`PinHeader_1x07_P2.54mm_Horizontal`, a 90° con i piedini oltre il bordo superiore; negli stessi fori va bene un header diritto), stesso pinout (1 VCC … 7 RST). JLC monta tutto il resto, J1 compreso. J2–J5 hanno il campo `Montaggio` = "a mano, parte del proprietario", nessun codice LCSC e l'attributo "escluso dai file di posizionamento": fuori da BOM JLC e CPL, presenti nella BOM completa | Scelta del proprietario: parti già in scorta, meno parti Extended a JLC (spariscono C46061680, C160404 e C160402: da 8 a 5 codici Extended, circa −9 $ di setup). Il margine JLC di 2,5 mm vale solo per le parti montate da JLC; le regole di fabbricazione (`DEC-040`) valgono anche per le piazzole a foro passante. Modifica e verifiche in §10; aggiorna la parte "connettore lato scheda" di `DEC-024`, `DEC-027`, `DEC-028` e `DEC-034` |
| `DEC-044` | 2026-11-08 | **Modulo ESP32-C3-WROOM-02-N4 (C2934560) al posto dell'ESP32-C3-MINI-1-H4X**; supera `DEC-035` e aggiorna `DEC-031`, `DEC-036` (intaglio 8,5 × 20,2 mm, scheda sempre 50 × 40) e `DEC-041` (coppia ridisegnata sui pin 13/14 con gli stessi criteri). Applicate con la stessa modifica le correzioni approvate della revisione finale: FIN-003, FIN-005, FIN-006, FIN-007, FIN-008, FIN-009 (§11) | Scelta del proprietario sul rilievo FIN-001: l'H4X a JLC è "Standard Only" con radiografia, mentre `DEC-040` prevede l'Economic. Il WROOM-02-N4 è "Economic and Standard" senza radiografia (pagina JLC 2026-11-08, 13 113 a magazzino, ~3,31 $): si resta sull'Economic, circa −17 $ di setup (Standard 25,56 $ contro Economic 8,18 $, pagina JLC "pcb-assembly-price" aggiornata il 2026-10-22) e niente bordi tecnici. Fase 0 (2026-11-08): stato "Mass Production" nel selettore Espressif, chip v0.4 supportato da ESP-IDF v6.0/v6.1, pinout e land pattern dal datasheet v1.7; nessuna variante con chip v1.1. Dettagli in [02](02-architettura-hardware.md) §3.2 e [12](12-selezione-componenti.md) |
| `DEC-045` | 2026-11-08 | **Regola JLC dei 2,5 mm corpo-bordo per tutte le parti montate da JLC, unica eccezione J1** (USB-C a filo del bordo inferiore, da far accettare alla DFM di JLC, senza bordo tecnico). Scheda **50,5 × 41,5 mm rettangolare, senza intaglio**: cresce di 0,5 mm a destra e 1,5 mm in alto, angolo in basso a sinistra fisso (J1, H1/H2, coppia USB e origine della CPL invariati). **Antenna di U3 sulla scheda**, verso il bordo destro, con zona vietata su entrambi gli strati (niente rame, piste, vie, riempimenti, piazzole né componenti) sotto l'antenna e 5 mm oltre i suoi lati, come la zona dell'impronta di U3 ricavata dal datasheet. Supera `DEC-036` e la parte "intaglio" di `DEC-031` | Parole del proprietario: "dobbiamo rispettare non arbitrariamente le regole di stampa di JLC PCB [...] per questo prototipo allunga la scheda da quel lato, in modo da farci stare i componenti che mancano, rispettando le regole di JLC". Radio non usata in V1 (`DEC-012`): l'antenna sulla scheda è un compromesso accettato. Margine minimo 2,99 mm (U3); dettagli in [02](02-architettura-hardware.md) §3.2 |
| `DEC-027` | 2026-11-07 | Pulsante utente: **connettore JST-SH 2 poli** (*JST PH 4 poli sui pin 1–2 dalla `DEC-043`*) per un pulsante remoto **e** tasto tattile sulla scheda in parallelo (tasto su scheda tolto con `DEC-032`) | La posizione nella statuetta (`OPEN-017`) si decide col CAD senza rifare il PCB; il tasto su scheda serve al bring-up |

Le date sopra sono la data della formalizzazione nel documento delle scelte emerse nella conversazione, non un registro notarile degli eventi.

## 2. Proposte tecniche, NON decisioni definitive

| ID | Proposta | Stato | Come si decide |
|---|---|---|---|
| `CAND-001` | Waveshare ESP32-S3-Touch-AMOLED-1.75 | **Scartata** (`DEC-015`) | — |
| `CAND-002` | SHT40 su mini-PCB dedicato senza LED, nello stesso pannello JLC | **Superata** da `DEC-028` (modulo commerciale) | — |
| `CAND-003` | LiPo protetta 1S | **Ritirata** (`DEC-023`) | — |
| `CAND-004` | Prolunga USB-C da pannello con dati USB 2.0 | Solo se la scheda principale va nella testa (opzione B, `DEC-021`) | Lunghezza, fissaggio, flash attraverso la prolunga |
| `CAND-005` | ESP-IDF con moduli BSP/servizi/UI separati | Proposto | Bring-up ed ergonomia del codice |
| `CAND-006` | 20 s di luminosità BRIGHT dopo pressione del pulsante | Proposto | Test usabilità |
| `CAND-007` | Target 48 h autonomia | **Ritirato** (`DEC-023`) | — |
| `CAND-008` | Altezza 130–160 mm | Indicativo | CAD basato su dimensioni reali |
| `CAND-009` | Modalità notte: una pressione del pulsante mostra il quadrante attenuato per un timeout breve (proposto 10 s), poi torna spento | Proposto | Test usabilità e `VT-UI-003` |
| `CAND-010` | Profilo d'uso di riferimento | Confermato → `DEC-014`, poi superato | — |
| `CAND-011` | SHT40 sui pin I²C della Waveshare | **Superata** (`DEC-015`) | — |
| `CAND-012` | MCU: modulo **ESP32-C3-MINI-1** (consigliato) o ESP32-S3-MINI-1 | Proposto | Pin necessari (budget migliorato senza batteria), prezzo/disponibilità LCSC, prototipo M1 |
| `CAND-013` | Caricatore con power-path e NTC | **Ritirato** (`DEC-023`) | — |
| `CAND-014` | RTC esterno a bassissimo consumo con tampone (es. RV-3028-C7 o PCF85063A + supercondensatore/pila) | **Superata** da `DEC-024` (RV-3028-C7 non disponibile) | — |
| `CAND-015` | Regolatore 3,3 V da 5 V USB: LDO AMS1117-3.3 | **Superata** da `DEC-037` (TLV75533) | — |
| `CAND-016` | Misura batteria | **Ritirata** (`DEC-023`) | — |
| `CAND-017` | Protocollo di configurazione testuale a righe sulla porta seriale USB, versionato (vedi [firmware](04-specifiche-firmware.md) §6.1) | Proposto | Prototipo M1 e test `VT-FW-007` |
| `CAND-018` | Configuratore come **pagina web statica** con Web Serial (Chrome/Edge desktop), nessuna installazione; alternativa script Python | Proposto | Prova su Windows con la dev board; compatibilità browser |
| `CAND-019` | Posizione scheda principale: **A** busto/base con USB-C sulla scheda (preferita) o **B** testa con prolunga | Proposto | Bozza Blender (`OPEN-020`) |
| `CAND-020` | Cavo display FFC | **Superata** da `DEC-034` (modulo a 7 pin con cavetto Dupont) | — |
| `CAND-021` | CAD a codice con **build123d** (alternativa CadQuery) | Proposto | Prima parte tecnica modellata ed esportata in STEP/STL |
| `CAND-022` | Componenti dello schema rev 0.2 e codici LCSC come in [12](12-selezione-componenti.md) (ESP32-C3-WROOM-02-N4, TYPE-C-31-M-12, USBLC6-2SC6, PTC BSMD0805-050-12V, TLV75533, AO3401A; JST PH e header 1×7 a foro passante saldati a mano, `DEC-043`) | Proposto | Prototipo M1, revisione schema, stock al momento dell'ordine |
| `CAND-023` | Assegnazione GPIO dell'ESP32-C3 (modulo WROOM-02, vedi [02](02-architettura-hardware.md) §3.1): ESP32-C3 sufficiente, S3 non necessario | Proposto | Prova sulla dev board M1 (strapping IO2/IO8/IO9, `DISP_EN_N` su IO20 per Q1; niente PWM, `DEC-034`) |
| `CAND-025` | Scheda principale rev 0.2 **50,5 × 41,5 mm** (`DEC-045`) posizionata e sbrogliata in bozza (vedi [02](02-architettura-hardware.md) §3.2) | Proposto | Studio volumetrico 1:1 (`OPEN-028`); sbroglio approvato a vista dal proprietario (`OPEN-027` chiusa) |
| `CAND-024` | Un solo PCB custom (scheda principale); display, SHT40 e RTC su moduli commerciali | Proposto | Preventivo JLC |

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
| `OPEN-008` | P1 | Posizione e tipo di sportello manutenzione? | CAD e prove assemblaggio |
| `OPEN-009` | P2 | Serve il light-sleep? Se sì, il pulsante risveglia l'MCU in modo affidabile? | Misure termiche M1/M5 |
| `OPEN-010` | — | ~~Soglie batteria~~ | Chiusa da `DEC-023` |
| `OPEN-011` | P1 | SHT40 legge realmente l'aria stanza o il calore interno (permanente con alimentazione continua)? | Test di confronto a regime con scocca chiusa |
| `OPEN-012` | P2 | Colori capelli, posa braccia e finitura cappello? | Approvazione concept/campione stampa |
| `OPEN-013` | — | ~~Temperatura della cella in carica~~ | Chiusa da `DEC-023` |
| `OPEN-014` | P2 | Per quanto tempo l'ora sopravvive a cavo scollegato? | Tampone scelto: pila CR1220 del modulo DS3231 (`DEC-024`), durata attesa di anni secondo Adafruit; verificare con `VT-FW-001` passo 5 |
| `OPEN-015` | P2 | Il menu con **un solo pulsante** è sufficientemente usabile come riserva? | Prototipo dell'interazione; il metodo principale è il configuratore (`DEC-020`) |
| `OPEN-016` | P1 | Il modulo display ricevuto ha il pinout atteso (RST, CS, DC, SDA, SCL, GND, VCC) e quanta corrente assorbe la retroilluminazione? | Modulo scelto (`DEC-034`); verifica della serigrafia e misura su banco prima del collegamento a J2 |
| `OPEN-017` | P1 | Dove posizionare il pulsante nella statuetta? | Proposte estetiche/ergonomiche e CAD |
| `OPEN-018` | — | ~~Montare il touch nella V1?~~ | Chiusa da `DEC-034` (niente touch) |
| `OPEN-019` | — | ~~GPIO e connettore per il touch~~ | Chiusa da `DEC-034`; IO0 e IO1 liberi su punti di test |
| `OPEN-020` | P0 | Dove va la scheda principale (busto/base o testa)? | Bozza a volumi in Blender con scheda, display e passaggio cavi; decide anche se serve la prolunga USB |
| `OPEN-021` | P1 | Il SPI del display è stabile sul cavetto Dupont a 7 fili della lunghezza reale? | Prova M1 con cavetto reale e frequenza scelta (10–20 MHz); R8/R9 22 Ω |
| `OPEN-022` | P1 | Come esce il cavo USB dal sedere senza far ribaltare la statuetta? | Bozza CAD con incavo/guida nella base e zavorra; prova `VT-MEC-003` |
| `OPEN-023` | — | ~~Orientamento del cavo FFC~~ | Chiusa da `DEC-034` (niente FFC); J2 ha pin 1 = VCC serigrafato sul retro |
| `OPEN-024` | — | ~~Corrente della retroilluminazione LEDA/LEDK~~ | Chiusa da `DEC-034`: la retroilluminazione è gestita dal modulo; misura della corrente in `OPEN-016` |
| `OPEN-025` | — | ~~Stabilità AMS1117 con MLCC~~ | Chiusa da `DEC-037` (TLV75533) |
| `OPEN-027` | — | ~~Lo sbroglio automatico (Freerouting) della rev 0.2 è adeguato?~~ | **Chiusa il 2026-11-08**: il proprietario ha rivisto il PCB a vista in KiCad e l'ha approvato (rev 0.2 con coppia USB simmetrica e correzioni del 2026-11-08), §9 |
| `OPEN-028` | P0 | Studio volumetrico 1:1 (revisione P0-05): scheda 50,5 × 41,5 mm (`DEC-045`), modulo display, cavetti, USB-C e spina, RTC, SHT40 e zavorra entrano nella statuetta? Con `DEC-043`: connettori JST PH alti circa 6 mm con ingresso dall'alto e piedini a foro passante di J2–J5 sotto la scheda (serve luce sotto) | Bozza CAD quotata con lo STEP della scheda; gate aperto prima dell'ordine |
| `OPEN-030` | — | ~~Il layout dopo `DEC-043`, `DEC-044` e `DEC-045` è accettabile? (FIN-002)~~ | **Chiusa il 2026-11-08**: il proprietario ha rivisto a vista in KiCad il commit `09200dc` e approva le modifiche (§12) |
| `OPEN-026` | P2 | Dove alloggiare il modulo DS3231 (quote dal disegno Adafruit, cavo JST PH → JST-SH, `DEC-043`) nella statuetta, accessibile per cambiare la pila CR1220? | Bozza CAD (`OPEN-020`) |
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
| P1-03 GND e antenna | Corretto: piani GND su due strati, zona antenna senza rame sopra l'intaglio | [02](02-architettura-hardware.md) §3.2 |
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

La revisione finale pre-Gerber (`docs/revisioni/2026-11-08/revisione-finale/README.md`) è sul ramo `claude/revisione-finale-ea91f4` (commit `cd2505b`, non unito): esito **NON PRONTO** per FIN-001 e FIN-002. Il proprietario ha scelto il modulo ESP32-C3-WROOM-02-N4 (`DEC-044`) e approvato le correzioni sotto.

| Rilievo | Stato | Cosa è cambiato |
|---|---|---|
| FIN-001 modulo "Standard Only" | **Risolto** con `DEC-044` | WROOM-02-N4 (C2934560) "Economic and Standard", senza radiografia; `DEC-040` resta "Economic" |
| FIN-002 revisione a vista dopo `DEC-043` | **Aperto** → `OPEN-030` | Serve una revisione a vista del nuovo layout (modulo, intaglio, coppia USB, passivi, sbroglio, cucitura) |
| FIN-003 calo di 3V3 all'accensione del display | **Corretto** | R16 da 1 k a 10 k (C25804), C11 10 nF (C57112, Basic) fra gate e drain di Q1, montato; V_GS in conduzione ≈ −3,0 V con R17 100 k. Misura comunque in `VT-PWR-003` |
| FIN-004 rotazioni CPL | **Procedura** | Tabella di controllo parte per parte in [12](12-selezione-componenti.md) §7; CPL non modificata a priori |
| FIN-005 testi della serigrafia | **Corretto** | Testi del retro a 1,0 mm con tratto 0,15 mm, etichette accorciate; `min_text_height` 1,0 mm e `min_text_thickness` 0,15 mm nel `.kicad_pro` |
| FIN-006 procedura Gerber | **Corretto** | `hardware/scripts/esporta_gerber_jlc.py`, eseguibile solo con `--conferma-proprietario`; **non eseguito**. Impostazioni dalla guida JLC per KiCad (2026-09-09) e controlli da fare dopo nel visualizzatore |
| FIN-007 regole DRC e minimi JLC | **Corretto** | Regola in `.kicad_dru`: anello delle piazzole PTH ≥ 0,18 mm. Linee di serigrafia delle impronte standard a 0,12 mm: lasciate come in libreria (cambiarle renderebbe le impronte diverse dalla libreria); JLC le stampa al proprio minimo, da guardare nell'anteprima |
| FIN-008 cucitura GND | **Corretto** | 4 vie termiche 0,3/0,7 mm nella EPAD del modulo (nell'impronta), 15 vie di cucitura lungo il contorno e vicino all'intaglio con `cucitura_gnd.py`, nessuna nella zona USB |
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
- La revisione a vista del proprietario (`OPEN-030`) è stata fatta il 2026-11-08 con esito positivo (§12). Nessun file Gerber.

## 12. Approvazione a vista del layout finale (2026-11-08)

- Il proprietario ha rivisto in KiCad il commit `09200dc` (modulo ESP32-C3-WROOM-02-N4, scheda 50,5 × 41,5 mm senza intaglio con antenna sulla scheda, J2–J5 a foro passante, correzioni FIN della revisione finale) e **approva le modifiche**: `OPEN-030` / FIN-002 chiusi.
- Su richiesta del proprietario segue una **nuova revisione completa pre-Gerber** del revisore indipendente su questo layout: vincoli circuitali ed elettrici, PCB, regole JLCPCB, coerenza con decisioni e documentazione. I Gerber restano da generare solo dopo il suo esito e un'approvazione esplicita del proprietario.
