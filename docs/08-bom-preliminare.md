# 08 — BOM preliminare e procurement

**Versione:** 0.3 · **Stato:** candidati, nessun acquisto confermato · **Data:** 2026-11-07

## 1. Regole

- Prezzi, disponibilità e tempi di consegna **non sono fissati** in questa BOM; vanno aggiornati con preventivi reali (JLCPCB/LCSC e fornitori del display).
- Per l'assemblaggio JLC preferire parti della libreria "basic": ogni parte "extended" aggiunge un costo fisso.
- Nessuna parte è in stato `APPROVATO` finché non sono stati verificati connettori, quote e alimentazione.
- Il PCB custom **non** riduce il costo del singolo esemplare rispetto a una scheda pronta: la stima va confrontata con un preventivo reale prima dell'ordine.

## 2. Prototipo su banco (M1)

Moduli commerciali economici per validare architettura, consumi e firmware **prima** di disegnare il PCB.

| ID | Q.tà | Candidato / specifica | Stato | Scopo |
|---|---:|---|---|---|
| `PRO-001` | 1 | Dev board con lo stesso MCU scelto (ESP32-C3 o S3) e USB nativa | CAND | Firmware, light-sleep, USB attraverso prolunga |
| `PRO-002` | 1 | Modulo display rotondo 1,28" GC9A01 240×240 | CAND | Driver, leggibilità, consumo retroilluminazione |
| `PRO-003` | 1 | Breakout del caricatore candidato (power-path + NTC) | CAND | Carica, power-path, cutoff termico |
| `PRO-004` | 1 | Breakout SHT40 senza LED (o con LED rimosso) | CAND | Lettura e posizionamento |
| `PRO-005` | 1 | Breakout RTC candidato con tampone | CAND | Mantenimento ora a cella scollegata |
| `PRO-006` | 1 | Pulsante tattile, breadboard, cavetti | TBD | Interazione |

## 3. Prodotto V1

| ID | Q.tà | Candidato / specifica | Stato | Gate di approvazione |
|---|---:|---|---|---|
| `BOM-001` | 1 (min. ordine JLC) | **PCB custom** KiCad, assemblato JLCPCB: MCU, caricatore, regolatore, RTC, USB-C, connettori (vedi [02](02-architettura-hardware.md) §3) | CAND | Prototipo M1 superato, ERC/DRC, revisione schema, disponibilità LCSC |
| `BOM-002` | 1 | **SHT40** su mini-PCB nello stesso pannello JLC, senza LED | CAND | Indirizzo, meccanica, errore termico |
| `BOM-003` | 1 | **LiPo 1S protetta**, preferibilmente con NTC, 2.500–3.000 mAh (da rivedere sui consumi) | CAND | Datasheet, limite carica, polarità, ingombro, protezioni |
| `BOM-004` | 1 | **Prolunga USB-C maschio-femmina da pannello**, 15–25 cm, dati USB 2.0 (`DEC-011`, `DEC-018`) | CAND | Ingombro, fissaggio, flash via prolunga |
| `BOM-005` | 1 | **Display IPS rotondo 1,28" GC9A01**, pannello con FPC e datasheet disponibile (`DEC-016`) | CAND | Pinout FPC, retroilluminazione, quote |
| `BOM-006` | 1 | **Pulsante** (tattile su PCB o remoto con cavo, `DEC-017`) | TBD | Posizione nella statuetta, corsa, sensazione |
| `BOM-007` | 1 set | Cavi e connettori batteria/SHT40/pulsante, fermacavi | TBD | Polarità, lunghezze, ritenuta |
| `BOM-008` | 1 set | Gusci/statuetta 3D (PLA prototipo, PETG da valutare) | CAND | CAD e quote reali; prove di stampa |
| `BOM-009` | 1 set | Viti, inserti, gommini antiscivolo | TBD | Vano manutenzione, sicurezza cella |
| `BOM-010` | 1 | Alimentatore USB 5 V di qualità, se non già disponibile | TBD | Corrente adeguata alla carica scelta |

## 4. Opzioni V1 NON necessarie

- Scheda Waveshare ESP32-S3-Touch-AMOLED-1.75: scartata per costo (`DEC-015`).
- Display AMOLED e touch: sostituiti da IPS e pulsante (`DEC-016`, `DEC-017`).
- Sensore CO₂, audio, microSD, IMU, GPS: fuori perimetro.
- Secondo caricatore (es. TP4056) in parallelo al caricatore del PCB.

## 5. Fonti prodotto

- Sensirion: [SHT40 ufficiale](https://sensirion.com/products/catalog/SHT40).
- Datasheet di caricatore, RTC, regolatore, modulo ESP32 e pannello display: da aggiungere in [fonti](11-fonti.md) al momento della scelta.

## 6. Check-list prima dell'ordine PCB

- [ ] Prototipo M1 completato e consumi misurati.
- [ ] Datasheet del pannello display acquistato, con pinout FPC.
- [ ] Caricatore scelto: corrente di carica, NTC, power-path verificati su datasheet e su banco.
- [ ] Cella scelta sul datasheet; polarità del connettore confrontata con il PCB.
- [ ] Disponibilità LCSC di tutti i componenti assemblati, con alternative.
- [ ] ERC/DRC puliti e checklist di revisione schema compilata.
- [ ] Footprint e quote del PCB rotondo confrontati con il diametro interno della testa.
- [ ] Punti di test e possibilità di isolare i blocchi (0 Ω/jumper).
- [ ] Preventivo JLC completo (PCB, assemblaggio, spedizione, IVA) confrontato con l'alternativa pronta.

## 7. Tabella acquisti da completare

| ID BOM | Fornitore | Codice reale | Prezzo | Link acquisto | Ordinato | Ricevuto | Verificato |
|---|---|---|---|---|---|---|---|
| BOM-001 | JLCPCB | TBD | TBD | TBD | no | no | no |
| BOM-003 | TBD | TBD battery | TBD | TBD | no | no | no |
| BOM-004 | TBD | TBD cable | TBD | TBD | no | no | no |
| BOM-005 | TBD | TBD display | TBD | TBD | no | no | no |

## 8. Piano B

Se il PCB custom non supera i gate (errori di revisione, consumi, ricarica) o i tempi diventano incompatibili con il regalo, usare una scheda commerciale con ESP32 e display rotondo 1,28" integrato, mantenendo firmware e UI (il board-support è separato dalla logica prodotto).
