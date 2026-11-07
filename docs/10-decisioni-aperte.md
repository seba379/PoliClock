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
| `DEC-006` | 2026-11-07 | Porta ricarica **USB sul retro**; formato USB-C preferito ma da validare | Connettore nascosto/fruibile; necessaria staffa meccanica |
| `DEC-007` | 2026-11-07 | Modalità ibrida: **display attenuato**, luminosità aumentata dopo interazione | Requisito guida firmware/energia/UI |

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

## 3. Questioni aperte con priorità

| ID | Priorità | Questione | Evidenza/decisione necessaria |
|---|---|---|---|
| `OPEN-001` | P0 | La scheda candidata entra nella testa desiderata? | Disegno quotato + caliper sulla scheda reale |
| `OPEN-002` | P0 | Dove collegare SHT40 sul bus I²C della revisione acquistata? | Schema e test di indirizzamento/alimentazione |
| `OPEN-003` | P0 | Quale LiPo specifica e quale polarità/connettore? | Datasheet, misure, test di sicurezza |
| `OPEN-004` | P0 | Quanta corrente consuma la modalità DIM con display acceso? | Misura di corrente media e picchi |
| `OPEN-005` | P0 | La board supporta uso/ricarica contemporanei nel montaggio? | Schema PMU + prova ricarica e temperatura |
| `OPEN-006` | P0 | Il target 48 h è realistico a estetica accettabile? | Profilo reale + misura autonomia |
| `OPEN-007` | P1 | Come impostare inizialmente ora/data offline? | UI touch oppure provisioning USB robusto |
| `OPEN-008` | P1 | Posizione e tipo di sportello manutenzione? | CAD e prove assemblaggio |
| `OPEN-009` | P1 | Display attivato da touch a bassissimo consumo? | Validare driver/interrupt e corrente |
| `OPEN-010` | P1 | Soglie low/critical batteria e rappresentazione carica? | Parametri PMU/cella, scarica controllata |
| `OPEN-011` | P1 | SHT40 legge realmente l'aria stanza o il calore interno? | Test confronto con scocca e ricarica |
| `OPEN-012` | P2 | Colori capelli, posa braccia e finitura cappello? | Approvazione concept/campione stampa |

## 4. Come si chiude una decisione

Una questione aperta passa a `DEC-xxx` soltanto con: data, alternativa scelta, motivazione, vincoli, test/evidenza e file di specifica aggiornati. È ammesso respingere una proposta: non bisogna comprare componenti solo perché già presenti nel concept grafico.

## 5. Decisioni di sicurezza non negoziabili

Prima della chiusura della statuetta devono essere confermati compatibilità **batteria ↔ PMU**, corrente/tensione di carica, protezione cella, polarità e temperature. Nessun render o preventivo può sostituire questa evidenza.
