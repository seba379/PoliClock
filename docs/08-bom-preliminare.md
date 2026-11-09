# 08 — BOM preliminare e procurement

**Versione:** 0.9 · **Stato:** candidati, schema e PCB rev 0.2 con codici LCSC, nessun acquisto confermato · **Data:** 2026-11-09

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
| `PRO-002` | 1 | **Modulo display GC9A01 1,28" a 7 pin** (lo stesso del prodotto, `DEC-034`), es. [AliExpress 1005009766462228](https://it.aliexpress.com/item/1005009766462228.html) | CONF | Driver, leggibilità, corrente della retroilluminazione, pinout (`OPEN-016`) |
| `PRO-004` | 1 | **Modulo breakout SHT40** (es. "SHT40 modulo I²C 3V 5V, nero, con pin"): lo stesso del prodotto (`DEC-028`) | CAND | Lettura, posizionamento, presenza di LED/regolatore |
| `PRO-005` | 1 | **Adafruit DS3231 Precision RTC – STEMMA QT** (5188) + pila CR1220: lo stesso modulo del prodotto (`DEC-024`) | CONF | Mantenimento ora a cavo scollegato, deriva |
| `PRO-006` | 1 | Pulsante tattile, breadboard, cavetti | TBD | Interazione |
| `PRO-007` | 1 | Cavetti Dupont femmina-femmina 7 fili, lunghezza simile a quella prevista nel collo | CAND | Prova SPI sul cavo reale (`OPEN-021`) |
| `PRO-008` | 1 | Misuratore di corrente USB (tester in linea) | TBD | Consumi DIM/BRIGHT/NIGHT |

(`PRO-003`, breakout del caricatore, rimosso con `DEC-023`.)

## 3. Prodotto V1

| ID | Q.tà | Candidato / specifica | Stato | Gate di approvazione |
|---|---:|---|---|---|
| `BOM-001` | 2 assemblate (5 PCB) | **PCB custom** KiCad rev 0.2, assemblato JLCPCB: **solo la scheda principale** (50,5 × 41,5 mm, 2 strati, componenti su un lato; `DEC-030`, `DEC-045`). I connettori J2–J5 a foro passante non sono montati da JLC: li salda a mano il proprietario (`BOM-014`, `DEC-043`). Componenti e codici LCSC in [12](12-selezione-componenti.md); BOM e CPL di assemblaggio in `hardware/policlock-main/` | CAND | Prototipo M1, studio volumetrico (`OPEN-028`), revisione sbroglio (`OPEN-027`), stock LCSC, preventivo (§8) |
| `BOM-002` | 1 | **Modulo breakout SHT40** commerciale con header 2,54 mm (es. "SHT40 modulo I²C 3V 5V, nero, con pin"), alimentato a 3,3 V (`DEC-028`). **Verifica all'arrivo (revisione P1-09):** presenza di LED di accensione (da rimuovere o disattivare) e di un regolatore; corrente a riposo misurata; ordine dei pin sulla serigrafia | CAND | Pinout, indirizzo 0x44, LED/regolatore, meccanica, errore termico |
| `BOM-004` | 0–1 | **Prolunga USB-C maschio-femmina da pannello**, dati USB 2.0: **solo per l'opzione B** (scheda nella testa, `DEC-021`) | CAND | Ingombro, fissaggio, flash via prolunga |
| `BOM-005` | 1 | **Modulo display GC9A01 1,28" a 7 pin** (IPS a colori 240×240, senza touch, retroilluminazione fissa), es. [AliExpress SZHJW 1005009766462228](https://it.aliexpress.com/item/1005009766462228.html), ~4,24 € (2026-11-07) (`DEC-016`, `DEC-034`) | CONF | Pinout sulla serigrafia, corrente, quote (`OPEN-016`) |
| `BOM-006` | 1 | **Pulsante remoto** collegato al connettore J5 (JST PH 4 poli, pin 1–2; `DEC-043`); nessun tasto USER sulla scheda (`DEC-017`, `DEC-032`) | TBD | Posizione nella statuetta, corsa, sensazione |
| `BOM-007` | 1 set | Cavetti **JST PH 2,0 mm** (`DEC-043`): spina **PHR-4** con contatti a crimpare (serie SPH-002T) oppure cavetti PH 4 poli già pronti. SHT40: PH 4 poli → jumper femmina 2,54 mm. RTC: PH 4 poli → JST-SH 4 poli (STEMMA QT del modulo) oppure fili sulle piazzole 2,54 mm del modulo. Pulsante: PHR-4 con i soli pin 1–2. Fermacavi | TBD | Polarità e ordine dei pin (adattatori PH → SH da verificare filo per filo), lunghezze, ritenuta |
| `BOM-008` | 1 set | Gusci/statuetta 3D (PLA prototipo, PETG da valutare) | CAND | CAD e quote reali; prove di stampa |
| `BOM-009` | 1 set | Viti, inserti, gommini antiscivolo, **zavorra** per la base | TBD | Stabilità con cavo collegato |
| `BOM-010` | 1 | **Alimentatore USB 5 V** di qualità (obbligatorio: l'orologio funziona solo collegato) | TBD | Corrente adeguata all'assorbimento misurato |
| `BOM-011` | 1 | **Cavetto display** Dupont femmina-femmina 7 fili dritto sui pin 1–7 di J2 (pin 1 = VCC), lunghezza dal CAD. J2 è un header 1×8 dal `DEC-049`: il pin 8 (BUSY) serve solo a un eventuale e-paper, che userebbe 8 fili; va bene anche con J2 a foro passante (`DEC-043`), sia a 90° sia diritto | CAND | Prova `VT-PCB-003`, raggio di curvatura nel collo |
| `BOM-012` | 1 | **Cavo USB-C** di lunghezza e colore adatti alla scrivania (es. 1–2 m, colore coordinato) | TBD | Estetica, flessibilità, stabilità della statuetta |
| `BOM-013` | 1 | **Adafruit DS3231 Precision RTC – STEMMA QT** (prodotto 5188) + pila **CR1220**; LED "ON" disattivato tagliando il ponticello. Verifica all'arrivo come per `BOM-002` (LED, corrente) | CONF (`DEC-024`) | Alloggiamento accessibile per la pila (`OPEN-026`), deriva misurata |

| `BOM-014` | 1 set | **Connettori saldati a mano** (`DEC-043`): 3 × **JST PH B4B-PH-K-S** (J3 SHT40, J4 RTC, J5 pulsante) e 1 × header maschio **1×8 2,54 mm** a 90° (J2, `DEC-049`: pin 8 = BUSY; negli stessi fori va bene anche diritto; da una striscia divisibile se in scorta c'è solo il 1×7). Nella BOM completa con `Montaggio` = "a mano, parte del proprietario", fuori da BOM JLC e CPL. Dopo l'assemblaggio si saldano a mano anche le 4 linguette del guscio della USB-C J1 (`DEC-047`) | CONF (scorta del proprietario) | Saldatura dopo l'assemblaggio JLC; lunghezza dei piedini sotto la scheda (`OPEN-028`) |

(`BOM-003`, batteria LiPo, rimossa con `DEC-023`.)

## 4. Opzioni V1 NON necessarie

- Batteria, caricatore, misura batteria: rimandati a versioni successive (`DEC-023`).
- Scheda Waveshare ESP32-S3-Touch-AMOLED-1.75: scartata per costo (`DEC-015`).
- Display AMOLED e touch: sostituiti da modulo IPS senza touch e pulsante (`DEC-016`, `DEC-017`, `DEC-034`).
- Schedina portadisplay, cavo FFC, pannello nudo: eliminati con `DEC-034`.
- Sensore CO₂, audio, microSD, IMU, GPS: fuori perimetro.

## 5. Fonti prodotto

- Sensirion: [SHT40 ufficiale](https://sensirion.com/products/catalog/SHT40).
- Datasheet dei componenti dello schema: [fonti](11-fonti.md), sezione "Componenti dello schema". Il modulo display non ha datasheet: pinout dalla foto dell'inserzione, da verificare.

## 6. Check-list prima dell'ordine PCB

- [ ] Prototipo M1 completato e consumi misurati.
- [ ] Modulo display ricevuto e verificato: pinout e corrente (`OPEN-016`, `VT-PCB-005`).
- [x] RTC e tampone scelti (`DEC-024`); durata del tampone da verificare (`OPEN-014`).
- [ ] Disponibilità LCSC di tutti i componenti assemblati, con alternative (verificata il 2026-11-07, da ripetere all'ordine).
- [ ] ERC/DRC puliti (report salvati in `hardware/policlock-main/`, rieseguibili con `esporta.py`) e checklist di revisione schema compilata.
- [ ] Sagoma della scheda principale, posizione della USB-C e dei connettori confrontate con lo studio volumetrico 1:1 (`OPEN-020`, `OPEN-028`).
- [x] Punti di test e possibilità di isolare i blocchi (0 Ω/jumper) a schema.
- [ ] Preventivo JLC completo (PCB, assemblaggio, spedizione, IVA) confrontato con l'alternativa pronta.

## 7. Tabella acquisti da completare

| ID BOM | Fornitore | Codice reale | Prezzo | Link acquisto | Ordinato | Ricevuto | Verificato |
|---|---|---|---|---|---|---|---|
| BOM-001 | JLCPCB | TBD | TBD | TBD | no | no | no |
| BOM-005 | AliExpress (SZHJW) | 1005009766462228 | 4,24 € | [link](https://it.aliexpress.com/item/1005009766462228.html) | no | no | no |
| BOM-010 | TBD | TBD alimentatore | TBD | TBD | no | no | no |
| BOM-012 | TBD | TBD cavo USB-C | TBD | TBD | no | no | no |
| BOM-013 | Adafruit o distributore | 5188 + CR1220 | TBD | TBD | no | no | no |
| BOM-002 | TBD (es. Amazon/AliExpress) | modulo SHT40 | TBD | TBD | no | no | no |

## 8. Stima dei costi (ordine di grandezza, da confermare col preventivo)

Ipotesi: **un solo PCB custom** (dopo `DEC-034`), 5 PCB prodotti e **2 assemblati** con il servizio JLCPCB "Economic", componenti solo sul lato superiore. Tariffe dalla [pagina prezzi assemblaggio JLCPCB](https://jlcpcb.com/help/article/pcb-assembly-price) e prezzi componenti dal catalogo, letti il 2026-11-07.

| Voce | Base di calcolo | Stima |
|---|---|---:|
| PCB 2 strati 50,5 × 41,5 mm, 5 pezzi | Tariffa promozionale tipica per schede piccole, da verificare | ~2–5 $ |
| Setup assemblaggio Economic | Tariffa JLC. Possibile perché il modulo ESP32-C3-WROOM-02-N4 (C2934560) è "Economic and Standard" senza radiografia (`DEC-044`); con l'H4X ("Standard Only") sarebbe servito lo Standard da 25,56 $ (pagina prezzi JLC aggiornata il 2026-10-22), circa 17 $ in più, più i bordi tecnici | 8,18 $ |
| Stencil | Tariffa JLC | 1,53 $ |
| Parti Extended | 5 codici distinti × 3,07 $ (C2934560, C165948, C2977522, C7519, C404027; il modulo WROOM-02 sostituisce C41349510); con `DEC-043` spariscono le Extended di J2 (C46061680), J3/J4 (C160404) e J5 (C160402), −9,21 $ | 15,35 $ |
| Saldature | ~119 giunti per scheda (2 di R23, `DEC-049`; senza tasti, `DEC-039`, e senza i 24 giunti di J2–J5, `DEC-043`) × 2 × (0,016 + 0,0016) $ | ~4 $ |
| Componenti per 2 schede | Somma dalla BOM JLC (`costi` del 2026-11-07); il modulo ESP32 pesa circa 6,6 $ (WROOM-02 ~3,31 $ l'uno contro 3,10 $ dell'H4X); senza i tasti RESET/BOOT e senza J2–J5 (−1,38 $); C11 10 nF (C57112, Basic), R16 da 10 kΩ (FIN-003) e R23 1 kΩ (C21190, Basic, `DEC-049`) costano centesimi | ~8,3 $ |
| **Subtotale JLC** | | **~39–42 $** |
| Spedizione verso l'Italia e IVA | Dipendono dal corriere scelto al checkout | da aggiungere |

Fuori da JLC (prezzi indicativi, da verificare all'acquisto): connettori J2–J5 già in scorta (`BOM-014`); modulo display ~4,24 € (`BOM-005`); modulo Adafruit DS3231 + CR1220 (`BOM-013`); breakout SHT40 (`BOM-002`); cavetti (`BOM-007`, `BOM-011`); alimentatore e cavo USB-C (`BOM-010`, `BOM-012`); stampa 3D (`BOM-008`). Per un regalo in un solo esemplare il costo fisso (setup, Extended, spedizione) pesa più dei componenti: il confronto con il Piano B resta valido.

## 9. Piano B

Se il PCB custom non supera i gate (errori di revisione, consumi, temperature) o i tempi diventano incompatibili con il regalo, usare una scheda commerciale con ESP32 e display rotondo 1,28" integrato, mantenendo firmware e UI (il board-support è separato dalla logica prodotto).
