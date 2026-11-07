# 10 — Decision log e questioni aperte

**Versione:** 0.6 · **Data:** 2026-11-07

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
| `DEC-017` | 2026-11-07 | Interazione principale con **pulsante** fisico; posizione da definire | Più semplice ed economico; posizione in `OPEN-017`. Touch predisposto in `DEC-019` |
| `DEC-018` | 2026-11-07 | Presa USB-C nella **parte posteriore bassa** della statuetta (sul sedere, per ironia); collegamento al PCB in `DEC-021` | Vincola foro, fissaggio e stabilità con cavo inserito |
| `DEC-019` | 2026-11-07 | **Predisposizione touch** sul PCB (connettore/footprint, GPIO INT e RST riservati, componenti non montati); pulsante sempre presente; pannello scelto tra modelli disponibili con e senza touch a parità di ingombro | Il touch si potrà attivare senza rifare il PCB; decisione dopo la prova sul prototipo M1 (`OPEN-018`) |
| `DEC-020` | 2026-11-07 | **Configuratore da PC via USB** come metodo principale per impostare ora, data e fascia notte; menu con il pulsante come riserva | La USB nativa dell'MCU espone una porta seriale; protocollo documentato (`CAND-017`); configuratore web con Web Serial (`CAND-018`) |
| `DEC-021` | 2026-11-07 | **Scheda principale rettangolare separata dal display**, collegata a una **schedina portadisplay** nella testa con cavo (FFC o JST-SH) attraverso il collo; SHT40 su mini-PCB; tutte nello stesso pannello JLC. Posizione della scheda principale decisa con la bozza CAD (`OPEN-020`): preferita nel busto/base con **USB-C saldata sulla scheda** affacciata al sedere; prolunga solo se la scheda va nella testa | Layout più semplice e sicuro, schema e PCB realizzabili da Claude con revisione visiva del proprietario; testa libera dai vincoli del PCB |
| `DEC-022` | 2026-11-07 | Strumenti: **KiCad 10** (`kicad-cli`), **VS Code + ESP-IDF** (v6.x, versione da fissare al bring-up), **Blender** per la chibi, **CAD a codice** (build123d) per le parti tecniche | Strumenti gratuiti e automatizzabili; scultura artistica a mano in Blender |
| `DEC-023` | 2026-11-07 | **V1 senza batteria: alimentazione continua da cavo USB-C.** RTC esterno con tampone mantenuto. Batteria rimandata a eventuali versioni successive, da ridiscutere | Rimuove la parte più complessa e rischiosa (cella, caricatore, NTC, autonomia, gate di sicurezza della cella); semplifica PCB, firmware e CAD; accettato che l'orologio funzioni solo collegato. Supera `DEC-005`, `DEC-008`, `DEC-014` |
| `DEC-024` | 2026-11-07 | **RTC su modulo esterno via cavo: Adafruit DS3231 Precision RTC – STEMMA QT** (prodotto 5188) con pila **CR1220**, collegato con cavo JST-SH 4 poli (Qwiic) al connettore J4 della scheda principale; nessun RTC sul PCB | RV-3028-C7 a stock 0 su LCSC/JLC; scelto dal proprietario fra RTC sul PCB (RV-3032-C7, PCF85063A, PCF8563T) e moduli esterni. DS3231 compensato in temperatura (±2 ppm), tampone di anni, modulo documentato. La pila serve solo all'RTC (compatibile con `DEC-023`). Supera `CAND-014` |
| `DEC-025` | 2026-11-07 | Schedina portadisplay disegnata per il **pannello GC9A01 1,28" con touch** (CST816S, FPC **18 poli**); si acquista sempre la versione touch, il touch resta inattivo finché non viene abilitato | Un solo footprint rispetta la predisposizione `DEC-019`. Pinout preso dallo schema di riferimento Waveshare, da confermare sul pannello acquistato (`OPEN-016`) |
| `DEC-026` | 2026-11-07 | Cavo display **FFC 16 poli passo 0,5 mm** con connettori ZIF SMD JUSHUO AFC01-S16FCA-00 su entrambe le schede | 10 segnali (con touch) + 2×3,3 V + 4×GND alternati; connettore molto disponibile a JLC. Supera `CAND-020` (resta da validare la stabilità SPI, `OPEN-021`) |
| `DEC-027` | 2026-11-07 | Pulsante utente: **connettore JST-SH 2 poli** per un pulsante remoto **e** tasto tattile sulla scheda in parallelo | La posizione nella statuetta (`OPEN-017`) si decide col CAD senza rifare il PCB; il tasto su scheda serve al bring-up |

Le date sopra sono la data della formalizzazione nel documento delle scelte emerse nella conversazione, non un registro notarile degli eventi.

## 2. Proposte tecniche, NON decisioni definitive

| ID | Proposta | Stato | Come si decide |
|---|---|---|---|
| `CAND-001` | Waveshare ESP32-S3-Touch-AMOLED-1.75 | **Scartata** (`DEC-015`) | — |
| `CAND-002` | SHT40 su mini-PCB dedicato senza LED, nello stesso pannello JLC | Da validare | Bus, posizione e precisione in scocca |
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
| `CAND-015` | Regolatore 3,3 V da 5 V USB: LDO **AMS1117-3.3** (LCSC C6186, Basic) con 22 µF in uscita | Proposto (schema rev 0.1) | Misura dissipazione in M1/M3; stabilità con MLCC (`OPEN-025`); alternativa ME6211C33/AP2112K |
| `CAND-016` | Misura batteria | **Ritirata** (`DEC-023`) | — |
| `CAND-017` | Protocollo di configurazione testuale a righe sulla porta seriale USB, versionato (vedi [firmware](04-specifiche-firmware.md) §6.1) | Proposto | Prototipo M1 e test `VT-FW-007` |
| `CAND-018` | Configuratore come **pagina web statica** con Web Serial (Chrome/Edge desktop), nessuna installazione; alternativa script Python | Proposto | Prova su Windows con la dev board; compatibilità browser |
| `CAND-019` | Posizione scheda principale: **A** busto/base con USB-C sulla scheda (preferita) o **B** testa con prolunga | Proposto | Bozza Blender (`OPEN-020`) |
| `CAND-020` | Cavo display: **FFC passo 0,5 mm** con connettori ZIF (preferito) o cavetto JST-SH; SPI 10–20 MHz | Confermato → `DEC-026` (16 poli); frequenza SPI ancora da provare | Prova su banco con cavo di lunghezza reale (M1) |
| `CAND-021` | CAD a codice con **build123d** (alternativa CadQuery) | Proposto | Prima parte tecnica modellata ed esportata in STEP/STL |
| `CAND-022` | Componenti dello schema rev 0.1 e codici LCSC come in [12](12-selezione-componenti.md) (ESP32-C3-MINI-1-N4, TYPE-C-31-M-12, USBLC6-2SC6, PTC BSMD0805-050-12V, AMS1117-3.3, AO3400A, JST-SH, JUSHUO AFC01, SHT40-AD1B-R2) | Proposto | Prototipo M1, revisione schema, stock al momento dell'ordine |
| `CAND-023` | Assegnazione GPIO dell'ESP32-C3-MINI-1 (vedi [02](02-architettura-hardware.md) §3.1): ESP32-C3 sufficiente, S3 non necessario | Proposto | Prova sulla dev board M1 (strapping IO2/IO8/IO9, PWM su IO20) |
| `CAND-024` | Tre progetti KiCad separati (principale, portadisplay, SHT40), pannellizzati per l'ordine JLC | Proposto | Preventivo JLC e strumenti di pannellizzazione al layout |

## 3. Questioni aperte con priorità

| ID | Priorità | Questione | Evidenza/decisione necessaria |
|---|---|---|---|
| `OPEN-001` | P0 | Display + portadisplay entrano nella testa desiderata? | Quote del pannello e della schedina, CAD |
| `OPEN-002` | P1 | Connettore e cavo per SHT40 remoto? | Scelta connettore, lunghezza, percorso nel corpo |
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
| `OPEN-016` | P0 | Quale pannello GC9A01 **con touch, FPC 18 poli** (`DEC-025`) acquistare, con datasheet e pinout FPC affidabili? | Ricerca fornitori, datasheet; confermare passo, lato contatti e pinout di J2 della portadisplay prima del layout |
| `OPEN-017` | P1 | Dove posizionare il pulsante nella statuetta? | Proposte estetiche/ergonomiche e CAD |
| `OPEN-018` | P1 | Montare il touch nella V1? | Prova sul prototipo M1: usabilità e interazione con la cornice stampata |
| `OPEN-019` | P2 | Quali GPIO e quale connettore per il touch? | Proposta nello schema rev 0.1: TP_INT su IO0, TP_RST su IO1, I²C condiviso tramite R11/R12 0 Ω DNP, segnali nel cavo FFC (`CAND-023`); da confermare con il datasheet del pannello |
| `OPEN-020` | P0 | Dove va la scheda principale (busto/base o testa)? | Bozza a volumi in Blender con scheda, display e passaggio cavi; decide anche se serve la prolunga USB |
| `OPEN-021` | P1 | Il SPI del display è stabile sul cavo reale? | Prova M1 con cavo di lunghezza reale e frequenza scelta |
| `OPEN-022` | P1 | Come esce il cavo USB dal sedere senza far ribaltare la statuetta? | Bozza CAD con incavo/guida nella base e zavorra; prova `VT-MEC-003` |
| `OPEN-023` | P1 | Orientamento del cavo FFC: contatti sullo stesso lato o opposti, in modo che il pin n della scheda principale arrivi al pin n della portadisplay? | Layout delle due schede e percorso nel collo; scegliere il tipo di cavo FFC di conseguenza |
| `OPEN-024` | P1 | Corrente della retroilluminazione: LEDA a 3,3 V con R18 = 10 Ω (riferimento Waveshare) è adeguata? | Datasheet del pannello (Vf, corrente nominale); misura in M1 |
| `OPEN-025` | P2 | L'AMS1117-3.3 è stabile con condensatori ceramici (il datasheet usa 22 µF al tantalio)? | Bring-up: oscilloscopio sull'uscita 3,3 V con carico variabile; in alternativa LDO stabile con MLCC prima del layout |
| `OPEN-026` | P2 | Dove alloggiare il modulo DS3231 (quote dal disegno Adafruit, cavo JST-SH) nella statuetta, accessibile per cambiare la pila CR1220? | Bozza CAD (`OPEN-020`) |

## 4. Come si chiude una decisione

Una questione aperta passa a `DEC-xxx` soltanto con: data, alternativa scelta, motivazione, vincoli, test/evidenza e file di specifica aggiornati. È ammesso respingere una proposta: non bisogna comprare componenti solo perché già presenti nel concept grafico.

## 5. Decisioni di sicurezza non negoziabili

Prima della chiusura della statuetta devono essere confermati: protezione dell'ingresso USB (fusibile/PTC, ESD), temperature interne in funzionamento continuo, fissaggio di connettori e cavi. Se in una versione futura verrà reintrodotta una batteria, tornano obbligatorie le verifiche di compatibilità cella ↔ caricatore, cutoff termico, protezione e polarità. Nessun render o preventivo può sostituire questa evidenza.
