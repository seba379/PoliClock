# 10 — Decision log e questioni aperte

**Versione:** 0.1 · **Data:** 2026-11-07

## 1. Decisioni confermate (CONF)

| ID | Data | Decisione | Motivazione / impatto |
|---|---|---|---|
| `DEC-001` | 2026-11-07 | Prodotto come regalo: orologio da scrivania in statuetta stampata 3D | Focus su semplicità, estetica e funzionamento indipendente |
| `DEC-002` | 2026-11-07 | Personaggio: **poliziotta chibi/stilizzata**, con testa sproporzionata | Stile simpatico, riconoscibile e stampabile |
| `DEC-003` | 2026-11-07 | **Display circolare al posto del volto** | Vincolo primario CAD/display |
| `DEC-004` | 2026-11-07 | Funzioni V1: **ora, data, temperatura, umidità** | Esclude le funzioni opzionali del concept originale |
| `DEC-005` | 2026-11-07 | Dispositivo alimentato da **batteria ricaricabile** | Richiede PMU, layout vano, test autonomia/sicurezza |
| `DEC-006` | 2026-11-07 | Porta ricarica **USB sul retro**, formato **USB-C** (confermato in `DEC-011`) | Connettore nascosto/fruibile; necessaria staffa meccanica |
| `DEC-007` | 2026-11-07 | Modalità ibrida: **display attenuato**, luminosità aumentata dopo interazione | Requisito guida firmware/energia/UI |
| `DEC-008` | 2026-11-07 | Ricarica circa **ogni 2 giorni** accettabile; accettabile anche l'uso frequente con USB collegata sulla scrivania | Conferma il target 48 h come soglia d'uso; rende obbligatoria la verifica di funzionamento durante ricarica (`VT-PWR-002`) |
| `DEC-009` | 2026-11-07 | **Di notte il display può essere spento** (modalità notte) | Funzione aggiunta su richiesta del proprietario: riduce consumi e burn-in. Orari in `DEC-013`; comportamento al tocco in `CAND-009` |
| `DEC-010` | 2026-11-07 | Aspetto: **uniforme blu e cappello** | Vincolo estetico CAD/colori (`PR-UI-002`) |
| `DEC-011` | 2026-11-07 | Connettore di ricarica posteriore **USB-C** (non solo preferito) | Vincola `BOM-004` e staffa posteriore |
| `DEC-012` | 2026-11-07 | **Wi-Fi e sincronizzazione NTP esclusi dalla V1** | Ora impostata offline (touch o USB); meno consumi, configurazione e superficie d'errore. Rivalutabile in V2 |
| `DEC-013` | 2026-11-07 | Fascia notte di default **23:00–07:00**, configurabile | Chiude la parte orari di `CAND-009`; base di `VT-UI-003` |
| `DEC-014` | 2026-11-07 | Profilo d'uso di riferimento per l'autonomia: 16 h giorno in DIM + 8 h notte spento, **30 attivazioni BRIGHT/giorno** da 20 s, SHT40 ogni 60 s, radio spenta | Rende verificabile il target 48 h (`VT-PWR-003`) |

Le date sopra sono la data della formalizzazione nel documento delle scelte emerse nella conversazione, non un registro notarile degli eventi.

## 2. Proposte tecniche, NON decisioni definitive

| ID | Proposta | Stato | Come si decide |
|---|---|---|---|
| `CAND-001` | Waveshare ESP32-S3-Touch-AMOLED-1.75 standard SKU 31261 | Da validare | Pinout, quote, bring-up, consumi |
| `CAND-002` | SHT40 su breakout I²C | Da validare | Bus, alimentazione e precisione in scocca |
| `CAND-003` | LiPo protetta 1S da 2.500–3.000 mAh | Da validare | Limiti di carica, connettore, ingombro, target autonomia |
| `CAND-004` | USB-C da pannello con prolunga dati/power | Da validare | Geometria, fissaggio, flashing e perdite |
| `CAND-005` | ESP-IDF con moduli BSP/servizi/UI separati | Proposto | Bring-up ed ergonomia del codice |
| `CAND-006` | 20 s di luminosità BRIGHT dopo touch | Proposto | Test usabilità/consumi |
| `CAND-007` | Target 48 h autonomia | Obiettivo, NON prestazione | Misure complete su batteria reale |
| `CAND-008` | Altezza 130–160 mm | Indicativo | CAD basato su dimensioni reali |
| `CAND-009` | Modalità notte: un tocco mostra il quadrante attenuato per un timeout breve (proposto 10 s), poi torna spento (orari confermati in `DEC-013`) | Proposto | Test usabilità, consumo e `VT-UI-003` |
| `CAND-010` | Profilo d'uso di riferimento per autonomia | Confermato → `DEC-014` | — |
| `CAND-011` | SHT40 sul bus I²C principale (GPIO14/15, pad riservati) oppure su secondo bus via header H2 (GPIO17/18) | Proposto | Schematico verificato; da confermare su scheda reale |

## 3. Questioni aperte con priorità

| ID | Priorità | Questione | Evidenza/decisione necessaria |
|---|---|---|---|
| `OPEN-001` | P0 | La scheda candidata entra nella testa desiderata? | Disegno quotato + caliper sulla scheda reale |
| `OPEN-002` | P0 | Dove collegare SHT40 sul bus I²C della revisione acquistata? | Schematico 2025-07-28: bus su GPIO14/15 con pull-up 2,2 kΩ a 3,3 V e pad riservati (vedi `CAND-011`); resta da confermare su scheda reale e con scan degli indirizzi |
| `OPEN-003` | P0 | Quale LiPo specifica e quale polarità/connettore? | Datasheet, misure, test di sicurezza |
| `OPEN-004` | P0 | Quanta corrente consuma la modalità DIM con display acceso? | Misura di corrente media e picchi |
| `OPEN-005` | P0 | La board supporta uso/ricarica contemporanei nel montaggio? | Schema PMU + prova ricarica e temperatura |
| `OPEN-006` | P0 | Il target 48 h è realistico a estetica accettabile? | Profilo reale + misura autonomia |
| `OPEN-007` | P0 | Come impostare inizialmente ora/data offline? | Unico percorso in V1 (`DEC-012`); necessario anche dopo scarica completa (RTC senza batteria tampone propria). UI touch oppure provisioning USB robusto |
| `OPEN-008` | P1 | Posizione e tipo di sportello manutenzione? | CAD e prove assemblaggio |
| `OPEN-009` | P1 | Display attivato da touch a bassissimo consumo? | Validare driver/interrupt e corrente |
| `OPEN-010` | P1 | Soglie low/critical batteria e rappresentazione carica? | Parametri PMU/cella, scarica controllata |
| `OPEN-011` | P1 | SHT40 legge realmente l'aria stanza o il calore interno? | Test confronto con scocca e ricarica |
| `OPEN-012` | P2 | Colori capelli, posa braccia e finitura cappello? | Approvazione concept/campione stampa |
| `OPEN-013` | P0 | La temperatura della cella è sorvegliata durante la ricarica? | Lo schematico mostra il pin TS dell'AXP2101 collegato a un termistore 10 kΩ **sulla scheda**, non sulla cella: definire mitigazione (corrente di carica prudente, posizione cella, test termici) |
| `OPEN-014` | P1 | L'RTC conserva l'ora con sistema spento dalla PMU e dopo intervento della protezione cella? | RTC alimentato dall'AXP2101 (nessuna batteria tampone dedicata): prova di banco |

## 4. Come si chiude una decisione

Una questione aperta passa a `DEC-xxx` soltanto con: data, alternativa scelta, motivazione, vincoli, test/evidenza e file di specifica aggiornati. È ammesso respingere una proposta: non bisogna comprare componenti solo perché già presenti nel concept grafico.

## 5. Decisioni di sicurezza non negoziabili

Prima della chiusura della statuetta devono essere confermati compatibilità **batteria ↔ PMU**, corrente/tensione di carica, protezione cella, polarità e temperature. Nessun render o preventivo può sostituire questa evidenza.
