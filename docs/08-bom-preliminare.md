# 08 — BOM preliminare e procurement

**Versione:** 0.6 · **Stato:** candidati, schema rev 0.1 con codici LCSC, nessun acquisto confermato · **Data:** 2026-11-07

## 1. Regole

- Prezzi, disponibilità e tempi di consegna **non sono fissati** in questa BOM; vanno aggiornati con preventivi reali (JLCPCB/LCSC e fornitori del display).
- Per l'assemblaggio JLC preferire parti della libreria "basic": ogni parte "extended" aggiunge un costo fisso.
- Nessuna parte è in stato `APPROVATO` finché non sono stati verificati connettori, quote e alimentazione.
- Il PCB custom **non** riduce il costo del singolo esemplare rispetto a una scheda pronta: la stima va confrontata con un preventivo reale prima dell'ordine.
- La V1 **non ha batteria** (`DEC-023`): nessuna cella, caricatore o misura batteria.

## 2. Prototipo su banco (M1)

Moduli commerciali economici per validare architettura, consumi e firmware **prima** di disegnare il PCB.

| ID | Q.tà | Candidato / specifica | Stato | Scopo |
|---|---:|---|---|---|
| `PRO-001` | 1 | Dev board con lo stesso MCU scelto (ESP32-C3 o S3) e USB nativa | CAND | Firmware, USB, configuratore |
| `PRO-002` | 1 | Modulo display rotondo 1,28" GC9A01 240×240 **con touch** | CAND | Driver, leggibilità, consumo retroilluminazione, prova touch (`DEC-019`) |
| `PRO-004` | 1 | **Modulo breakout SHT40** (es. "SHT40 modulo I²C 3V 5V, nero, con pin"): lo stesso del prodotto (`DEC-028`) | CAND | Lettura, posizionamento, presenza di LED/regolatore |
| `PRO-005` | 1 | **Adafruit DS3231 Precision RTC – STEMMA QT** (5188) + pila CR1220: lo stesso modulo del prodotto (`DEC-024`) | CONF | Mantenimento ora a cavo scollegato, deriva |
| `PRO-006` | 1 | Pulsante tattile, breadboard, cavetti | TBD | Interazione |
| `PRO-007` | 1 | Cavo FFC **16 poli** 0,5 mm + due adattatori FFC→pin, lunghezza simile a quella prevista nel collo | CAND | Prova SPI su cavo reale (`OPEN-021`) |
| `PRO-008` | 1 | Misuratore di corrente USB (tester in linea) | TBD | Consumi DIM/BRIGHT/NIGHT |

(`PRO-003`, breakout del caricatore, rimosso con `DEC-023`.)

## 3. Prodotto V1

| ID | Q.tà | Candidato / specifica | Stato | Gate di approvazione |
|---|---:|---|---|---|
| `BOM-001` | 1 (min. ordine JLC) | **PCB custom** KiCad, assemblato JLCPCB: scheda principale (MCU, protezioni USB, regolatore 3,3 V, USB-C, connettori), schedina portadisplay. Componenti e codici LCSC in [12](12-selezione-componenti.md); BOM di assemblaggio esportate in `hardware/*/*-bom-jlcpcb.csv` | CAND | Prototipo M1 superato, ERC/DRC, revisione schema, disponibilità LCSC, costo delle parti Extended nel preventivo |
| `BOM-002` | 1 | **Modulo breakout SHT40** commerciale con header 2,54 mm (es. "SHT40 modulo I²C 3V 5V, nero, con pin"), alimentato a 3,3 V; LED rimosso se presente (`DEC-028`) | CAND | Pinout sulla serigrafia, indirizzo 0x44, meccanica, errore termico |
| `BOM-004` | 0–1 | **Prolunga USB-C maschio-femmina da pannello**, dati USB 2.0: **solo per l'opzione B** (scheda nella testa, `DEC-021`) | CAND | Ingombro, fissaggio, flash via prolunga |
| `BOM-005` | 1 | **Display IPS rotondo 1,28" GC9A01 con touch** (CST816S), FPC **18 poli**, datasheet disponibile (`DEC-016`, `DEC-019`, `DEC-025`) | CAND | Pinout FPC (passo, lato contatti), retroilluminazione, quote (`OPEN-016`) |
| `BOM-006` | 1 | **Pulsante**: tasto tattile sulla scheda (TS-1187A, C318884) e connettore JST-SH 2 poli per un pulsante remoto (`DEC-017`, `DEC-027`) | CAND | Posizione nella statuetta, corsa, sensazione |
| `BOM-007` | 1 set | Cavetto JST-SH 4 poli Qwiic (RTC), cavetto JST-SH 4 poli → jumper femmina 2,54 mm (SHT40), JST-SH 2 poli (pulsante), fermacavi | TBD | Polarità, lunghezze, ritenuta |
| `BOM-008` | 1 set | Gusci/statuetta 3D (PLA prototipo, PETG da valutare) | CAND | CAD e quote reali; prove di stampa |
| `BOM-009` | 1 set | Viti, inserti, gommini antiscivolo, **zavorra** per la base | TBD | Stabilità con cavo collegato |
| `BOM-010` | 1 | **Alimentatore USB 5 V** di qualità (obbligatorio: l'orologio funziona solo collegato) | TBD | Corrente adeguata all'assorbimento misurato |
| `BOM-011` | 1 | **Cavo display** FFC **16 poli** passo 0,5 mm, lunghezza dal CAD, tipo di cavo secondo `OPEN-023` | CAND | Prova `VT-PCB-003`, raggio di curvatura nel collo |
| `BOM-012` | 1 | **Cavo USB-C** di lunghezza e colore adatti alla scrivania (es. 1–2 m, colore coordinato) | TBD | Estetica, flessibilità, stabilità della statuetta |
| `BOM-013` | 1 | **Adafruit DS3231 Precision RTC – STEMMA QT** (prodotto 5188) + pila **CR1220**; LED "ON" disattivato tagliando il ponticello | CONF (`DEC-024`) | Alloggiamento accessibile per la pila (`OPEN-026`), deriva misurata |

(`BOM-003`, batteria LiPo, rimossa con `DEC-023`.)

## 4. Opzioni V1 NON necessarie

- Batteria, caricatore, misura batteria: rimandati a versioni successive (`DEC-023`).
- Scheda Waveshare ESP32-S3-Touch-AMOLED-1.75: scartata per costo (`DEC-015`).
- Display AMOLED e touch montato: sostituiti da IPS e pulsante (`DEC-016`, `DEC-017`).
- Sensore CO₂, audio, microSD, IMU, GPS: fuori perimetro.

## 5. Fonti prodotto

- Sensirion: [SHT40 ufficiale](https://sensirion.com/products/catalog/SHT40).
- Datasheet dei componenti dello schema: [fonti](11-fonti.md), sezione "Componenti dello schema"; pannello display ancora da scegliere.

## 6. Check-list prima dell'ordine PCB

- [ ] Prototipo M1 completato e consumi misurati.
- [ ] Datasheet del pannello display acquistato, con pinout FPC.
- [x] RTC e tampone scelti (`DEC-024`); durata del tampone da verificare (`OPEN-014`).
- [ ] Disponibilità LCSC di tutti i componenti assemblati, con alternative (verificata il 2026-11-07, da ripetere all'ordine).
- [ ] ERC/DRC puliti e checklist di revisione schema compilata.
- [ ] Sagome di scheda principale e portadisplay, posizione della USB-C e dei connettori confrontate con la bozza CAD (`OPEN-020`).
- [x] Punti di test e possibilità di isolare i blocchi (0 Ω/jumper) a schema.
- [ ] Preventivo JLC completo (PCB, assemblaggio, spedizione, IVA) confrontato con l'alternativa pronta.

## 7. Tabella acquisti da completare

| ID BOM | Fornitore | Codice reale | Prezzo | Link acquisto | Ordinato | Ricevuto | Verificato |
|---|---|---|---|---|---|---|---|
| BOM-001 | JLCPCB | TBD | TBD | TBD | no | no | no |
| BOM-005 | TBD | TBD display | TBD | TBD | no | no | no |
| BOM-010 | TBD | TBD alimentatore | TBD | TBD | no | no | no |
| BOM-012 | TBD | TBD cavo USB-C | TBD | TBD | no | no | no |
| BOM-013 | Adafruit o distributore | 5188 + CR1220 | TBD | TBD | no | no | no |
| BOM-002 | TBD (es. Amazon/AliExpress) | modulo SHT40 | TBD | TBD | no | no | no |

## 8. Piano B

Se il PCB custom non supera i gate (errori di revisione, consumi, temperature) o i tempi diventano incompatibili con il regalo, usare una scheda commerciale con ESP32 e display rotondo 1,28" integrato, mantenendo firmware e UI (il board-support è separato dalla logica prodotto).
