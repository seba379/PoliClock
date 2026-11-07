# 10 — Decision log e questioni aperte

**Versione:** 0.3 · **Data:** 2026-11-07

## 1. Decisioni confermate (CONF)

| ID | Data | Decisione | Motivazione / impatto |
|---|---|---|---|
| `DEC-001` | 2026-11-07 | Prodotto come regalo: orologio da scrivania in statuetta stampata 3D | Focus su semplicità, estetica e funzionamento indipendente |
| `DEC-002` | 2026-11-07 | Personaggio: **poliziotta chibi/stilizzata**, con testa sproporzionata | Stile simpatico, riconoscibile e stampabile |
| `DEC-003` | 2026-11-07 | **Display circolare al posto del volto** | Vincolo primario CAD/display |
| `DEC-004` | 2026-11-07 | Funzioni V1: **ora, data, temperatura, umidità** | Esclude le funzioni opzionali del concept originale |
| `DEC-005` | 2026-11-07 | Dispositivo alimentato da **batteria ricaricabile** | Richiede caricatore, layout vano, test autonomia/sicurezza |
| `DEC-006` | 2026-11-07 | Porta ricarica **USB sul retro**, formato **USB-C** (confermato in `DEC-011`) | Connettore nascosto/fruibile; necessaria staffa meccanica |
| `DEC-007` | 2026-11-07 | Modalità ibrida: **display attenuato**, luminosità aumentata dopo interazione | Requisito guida firmware/energia/UI |
| `DEC-008` | 2026-11-07 | Ricarica circa **ogni 2 giorni** accettabile; accettabile anche l'uso frequente con USB collegata sulla scrivania | Conferma il target 48 h come soglia d'uso; impone power-path e verifica di funzionamento durante ricarica (`VT-PWR-002`) |
| `DEC-009` | 2026-11-07 | **Di notte il display può essere spento** (modalità notte) | Funzione aggiunta su richiesta del proprietario: riduce i consumi. Orari in `DEC-013`; comportamento al pulsante in `CAND-009` |
| `DEC-010` | 2026-11-07 | Aspetto: **uniforme blu e cappello** | Vincolo estetico CAD/colori (`PR-UI-002`) |
| `DEC-011` | 2026-11-07 | Connettore di ricarica posteriore **USB-C** (non solo preferito) | Vincola `BOM-004` e staffa posteriore |
| `DEC-012` | 2026-11-07 | **Wi-Fi e sincronizzazione NTP esclusi dalla V1** | Ora impostata offline (pulsante o USB); meno consumi, configurazione e superficie d'errore. Rivalutabile in V2 |
| `DEC-013` | 2026-11-07 | Fascia notte di default **23:00–07:00**, configurabile | Base di `VT-UI-003` |
| `DEC-014` | 2026-11-07 | Profilo d'uso di riferimento per l'autonomia: 16 h giorno in DIM + 8 h notte spento, **30 attivazioni BRIGHT/giorno** da 20 s, SHT40 ogni 60 s, radio spenta | Rende verificabile il target 48 h (`VT-PWR-003`) |
| `DEC-015` | 2026-11-07 | **PCB custom** progettato in KiCad e prodotto/assemblato da JLCPCB, con il minimo indispensabile; scartata la scheda Waveshare (ex `CAND-001`) | Costo della scheda pronta giudicato eccessivo dal proprietario, consapevole che per un solo esemplare il custom non costa necessariamente meno. Aggiunge le milestone di prototipo su banco, progettazione e bring-up PCB. Decisione "per ora": rivedibile con il piano B |
| `DEC-016` | 2026-11-07 | Display **IPS rotondo 1,28"**, 240×240, driver GC9A01 | Economico e documentato; nessun burn-in; retroilluminazione da gestire per i consumi |
| `DEC-017` | 2026-11-07 | Interazione principale con **pulsante** fisico; posizione da definire | Più semplice ed economico; posizione in `OPEN-017`. Touch predisposto in `DEC-019` |
| `DEC-018` | 2026-11-07 | Presa USB-C collegata con **prolunga**, nella **parte posteriore bassa** della statuetta (sul sedere, per ironia) | Vincola percorso prolunga dalla testa alla base, staffa e stabilità con cavo inserito |
| `DEC-019` | 2026-11-07 | **Predisposizione touch** sul PCB (connettore/footprint, GPIO INT e RST riservati, componenti non montati); pulsante sempre presente; pannello scelto tra modelli disponibili con e senza touch a parità di ingombro | Il touch si potrà attivare senza rifare il PCB; decisione di montarlo dopo la prova sul prototipo M1 con modulo touch (`OPEN-018`) |
| `DEC-020` | 2026-11-07 | **Configuratore da PC via USB** come metodo principale per impostare ora, data e fascia notte; menu con il pulsante come riserva | La USB nativa dell'MCU espone una porta seriale; protocollo di comandi documentato (`CAND-017`); configuratore web con Web Serial (`CAND-018`) |

Le date sopra sono la data della formalizzazione nel documento delle scelte emerse nella conversazione, non un registro notarile degli eventi.

## 2. Proposte tecniche, NON decisioni definitive

| ID | Proposta | Stato | Come si decide |
|---|---|---|---|
| `CAND-001` | Waveshare ESP32-S3-Touch-AMOLED-1.75 | **Scartata** (`DEC-015`) | — |
| `CAND-002` | SHT40 su mini-PCB dedicato senza LED, nello stesso pannello JLC | Da validare | Bus, posizione e precisione in scocca |
| `CAND-003` | LiPo protetta 1S da 2.500–3.000 mAh, preferibilmente con NTC | Da validare | Limiti di carica, connettore, ingombro, consumi misurati |
| `CAND-004` | Prolunga USB-C da pannello con dati USB 2.0 | Confermata come soluzione (`DEC-018`); modello da scegliere | Lunghezza, fissaggio, flash attraverso la prolunga |
| `CAND-005` | ESP-IDF con moduli BSP/servizi/UI separati | Proposto | Bring-up ed ergonomia del codice |
| `CAND-006` | 20 s di luminosità BRIGHT dopo pressione del pulsante | Proposto | Test usabilità/consumi |
| `CAND-007` | Target 48 h autonomia | Obiettivo, NON prestazione | Misure complete su batteria reale |
| `CAND-008` | Altezza 130–160 mm | Indicativo | CAD basato su dimensioni reali (display 1,28" consente una testa più piccola) |
| `CAND-009` | Modalità notte: una pressione del pulsante mostra il quadrante attenuato per un timeout breve (proposto 10 s), poi torna spento | Proposto | Test usabilità, consumo e `VT-UI-003` |
| `CAND-010` | Profilo d'uso di riferimento per autonomia | Confermato → `DEC-014` | — |
| `CAND-011` | SHT40 sui pin I²C della Waveshare | **Superata** (`DEC-015`) | — |
| `CAND-012` | MCU: modulo **ESP32-C3-MINI-1** (consigliato) o ESP32-S3-MINI-1 | Proposto | Consumi in light-sleep, prezzo/disponibilità LCSC, prototipo M1 |
| `CAND-013` | Caricatore con power-path e NTC (es. BQ24074) | Proposto | Datasheet, disponibilità LCSC, prova su banco |
| `CAND-014` | RTC esterno a bassissimo consumo con tampone (es. RV-3028-C7 o PCF85063A + supercondensatore/pila) | Proposto | Datasheet, consumo, mantenimento ora a cella scollegata |
| `CAND-015` | Regolatore 3,3 V: LDO a bassa Iq oppure buck-boost | Proposto | Consumo a riposo, picchi MCU, sfruttamento cella |
| `CAND-016` | Misura batteria: partitore commutato su ADC oppure fuel gauge I²C | Proposto | Precisione richiesta vs costo/consumo |
| `CAND-017` | Protocollo di configurazione testuale a righe sulla porta seriale USB, versionato (vedi [firmware](04-specifiche-firmware.md) §6.1) | Proposto | Prototipo M1 e test `VT-FW-007` |
| `CAND-018` | Configuratore come **pagina web statica** con Web Serial (Chrome/Edge desktop), nessuna installazione; alternativa script Python | Proposto | Prova su Windows con la dev board; compatibilità browser |

## 3. Questioni aperte con priorità

| ID | Priorità | Questione | Evidenza/decisione necessaria |
|---|---|---|---|
| `OPEN-001` | P0 | PCB rotondo + display entrano nella testa desiderata? | Quote del pannello e del PCB, CAD |
| `OPEN-002` | P1 | Connettore e cavo per SHT40 remoto? | Scelta connettore, lunghezza, percorso nel corpo |
| `OPEN-003` | P0 | Quale LiPo specifica, con quale connettore/polarità e NTC? | Datasheet, misure, test di sicurezza |
| `OPEN-004` | P0 | Quanta corrente consuma la modalità DIM con retroilluminazione bassa? | Misura su banco (M1) |
| `OPEN-005` | P0 | Quale caricatore e quale corrente di carica? | `CAND-013`, datasheet cella, prova su banco |
| `OPEN-006` | P0 | Il target 48 h è realistico a estetica accettabile? | Profilo reale + misura autonomia |
| `OPEN-007` | P0 | Come impostare inizialmente ora/data offline? | Risolto in progetto: configuratore da PC via USB (`DEC-020`), menu pulsante come riserva; da verificare in `VT-FW-007` |
| `OPEN-008` | P1 | Posizione e tipo di sportello manutenzione? | CAD e prove assemblaggio |
| `OPEN-009` | P1 | Il pulsante risveglia l'MCU dal light-sleep in modo affidabile? | Prova su dev board |
| `OPEN-010` | P1 | Soglie low/critical batteria e rappresentazione carica? | Misura batteria scelta, scarica controllata |
| `OPEN-011` | P1 | SHT40 legge realmente l'aria stanza o il calore interno? | Test confronto con scocca e ricarica |
| `OPEN-012` | P2 | Colori capelli, posa braccia e finitura cappello? | Approvazione concept/campione stampa |
| `OPEN-013` | P0 | La temperatura della cella è sorvegliata durante la ricarica? | Risolvibile con PCB custom: caricatore con ingresso NTC collegato alla cella (`CAND-013`); da provare su banco |
| `OPEN-014` | P1 | L'ora sopravvive a una scarica completa? | RTC con tampone dedicato (`CAND-014`); prova di banco |
| `OPEN-015` | P2 | Il menu con **un solo pulsante** è sufficientemente usabile come riserva? | Prototipo dell'interazione (pressione breve/lunga); il metodo principale è il configuratore (`DEC-020`) |
| `OPEN-016` | P0 | Quale pannello GC9A01 acquistare, con datasheet e pinout FPC affidabili? | Ricerca fornitori, datasheet |
| `OPEN-017` | P1 | Dove posizionare il pulsante nella statuetta? | Proposte estetiche/ergonomiche e CAD |
| `OPEN-018` | P1 | Montare il touch nella V1? | Prova sul prototipo M1: usabilità, consumo del controller in sleep, interazione con la cornice stampata |
| `OPEN-019` | P1 | Quali GPIO e quale connettore per il touch? | Datasheet del pannello scelto (pinout FPC display e touch) e pin liberi dell'MCU |

## 4. Come si chiude una decisione

Una questione aperta passa a `DEC-xxx` soltanto con: data, alternativa scelta, motivazione, vincoli, test/evidenza e file di specifica aggiornati. È ammesso respingere una proposta: non bisogna comprare componenti solo perché già presenti nel concept grafico.

## 5. Decisioni di sicurezza non negoziabili

Prima della chiusura della statuetta devono essere confermati compatibilità **batteria ↔ caricatore**, corrente/tensione di carica, cutoff termico (NTC), protezione cella, polarità e temperature. Nessun render o preventivo può sostituire questa evidenza.
