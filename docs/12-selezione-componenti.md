# 12 — Selezione componenti per lo schema (M2)

**Versione:** 0.7 · **Stato:** schema rev 0.2 dopo la revisione tecnica indipendente, **non validato** (manca il prototipo M1) · **Data:** 2026-11-07

Questo documento motiva i componenti dello schema KiCad in [`hardware/`](../hardware/README.md). Tutte le scelte restano `CAND` finché non superano il prototipo su banco (M1) e la revisione visiva del proprietario; le decisioni del proprietario sono in [10](10-decisioni-aperte.md) (`DEC-024`…`DEC-040`). Tutti i componenti montati sono nella libreria LCSC/JLC e il progetto segue le regole JLCPCB (`SC-008`, `DEC-040`).

**Novità della rev 0.2** (revisione tecnica indipendente del 2026-11-07, esito "NOT APPROVED FOR FABRICATION" sulla rev 0.1):

- LDO **TLV75533** stabile con condensatori ceramici al posto dell'AMS1117 (P0-04, `DEC-037`);
- modulo **ESP32-C3-MINI-1-H4X** ("Recommended") al posto dell'N4 (NRND) (P1-05, `DEC-035`);
- display su **modulo GC9A01 a 7 pin** pronto per breadboard: niente pannello nudo, schedina portadisplay, cavo FFC e touch (P0-02/P0-03 superati, `DEC-034`);
- USB-C con il **footprint della libreria KiCad** ricavato dal disegno HRO (P1-08).

## 1. Criterio di scelta

- **Vincolo del proprietario:** componenti **facilmente reperibili e montabili direttamente da JLCPCB** (libreria LCSC), **connettori inclusi**. Preferenza: parti **Basic** (nessun costo di setup), poi **Preferred**, poi **Extended** solo se necessario.
- Pinout e funzioni verificati sui **datasheet ufficiali** (vedi [fonti](11-fonti.md), sezione "Componenti dello schema").
- Footprint: libreria ufficiale KiCad dove esiste (passivi, SOT, USB-C HRO, header di test); altrimenti importati da LCSC/EasyEDA con `easyeda2kicad` e **confrontati**: JST-SH identici alla libreria KiCad (scarti ≤ 0,004 mm); USB-C EasyEDA **scartato** perché diverso dal disegno HRO.
- Stock e prezzi letti dal catalogo JLCPCB/LCSC il **2026-11-07**: cambiano ogni giorno, vanno **ricontrollati prima dell'ordine**.

## 2. Scheda principale (`hardware/policlock-main`)

| Rif. | Funzione | Componente | Produttore | LCSC | Libreria JLC | Stock* | Prezzo* | Note di verifica |
|---|---|---|---|---|---|---:|---:|---|
| U3 | MCU | **ESP32-C3-MINI-1-H4X** | Espressif | C41349510 | Extended | 2 822 | 3,10 $ | `DEC-035`. Datasheet v2.2 tab. 1-1: H4X "Recommended", chip v1.1, 4 MB, −40…105 °C, 13,2 × 16,6 × 2,4 mm come l'N4 (stesso footprint e pinout). L'N4X (C50390200) ha stock 0. Richiede ESP-IDF con supporto della revisione v1.1 |
| J1 | USB-C 2.0 | **TYPE-C-31-M-12** (16P) | Korean Hroparts | C165948 | Extended | 308 225 | 0,19 $ | Footprint della libreria KiCad (`USB_C_Receptacle_HRO_TYPE-C-31-M-12`, dal disegno HRO), serigrafia frontale tolta perché il guscio sporge 0,4 mm dal bordo |
| R1, R2 | CC sink | 5,1 kΩ 0603 1 % | Uni-Royal | C23186 | **Basic** | 20 M | — | Rd 5,1 kΩ su CC1 e CC2: 5 V senza USB-PD |
| F1 | Protezione VBUS | **BSMD0805-050-12V** PTC 0805 | BHFUSE | C2977522 | Extended | 58 790 | 0,05 $ | Hold 0,5 A / trip 1 A, 12 V |
| U1 | ESD D+/D-/VBUS | **USBLC6-2SC6** | STMicroelectronics | C7519 | Extended | 25 615 | 0,16 $ | Pinout SOT23-6: 1/6 I/O1, 3/4 I/O2, 2 GND, 5 VBUS. Passaggio diretto: I/O1 su D-, I/O2 su D+ (`DEC-041`); sull'asse della coppia, a circa 4 mm dai contatti del connettore |
| R3, R4 | Serie D+/D- | 0 Ω 0603 | Uni-Royal | C21189 | **Basic** | 19 M | — | Isolamento; sostituibili con 22 Ω se il bring-up lo richiede |
| U2 | LDO 5 V → 3,3 V | **TLV75533PDBVR** SOT-23-5 | Texas Instruments | C404027 | Extended | 94 177 | 0,12 $ | `DEC-037`. Datasheet SBVS320D: 500 mA, pin 1 IN, 2 GND, 3 EN, 4 NC, 5 OUT; **stabile con MLCC ≥ 1 µF** (capacità effettiva > 0,47 µF); RθJA 231 °C/W JEDEC, 100,8 °C/W sulla scheda di valutazione TI. EN collegato a IN |
| C2 / C3, C4 | Ingresso / uscita LDO | 10 µF 0603 X5R / 10 µF + 100 nF 0603 | Samsung / Yageo | C19702 / C14663 | **Basic** | — | — | A 2,4–2,8 mm dai pin di U2, ritorno a GND sul piano |
| C1, C5 | Bulk +5 V / 3V3 modulo | 10 µF 0603 X5R 10 V | Samsung | C19702 | **Basic** | 10 M | — | C5 + C6 (100 nF) sul pin 3V3 del modulo come nello schema di riferimento Espressif |
| C6, C8, C10 | Disaccoppiamento / antirimbalzo | 100 nF 0603 X7R | Yageo | C14663 | **Basic** | 34 M | — | C6 a 2,4 mm dal pin 3 (3V3) del modulo |
| C7 | RC su EN | 1 µF 0603 | Samsung | C15849 | **Basic** | 13 M | — | Espressif: R 10 kΩ + C 1 µF, pista EN corta. Nessun tasto RESET/BOOT (`DEC-039`): punti di test TP6 (EN) e TP11 (IO9) |
| J2 | Modulo display | **HX PZ2.54-1x7P WT** header maschio 1×7 2,54 mm SMD a 90° | hanxia | C46061680 | Extended | 9 029 | 0,14 $ | `DEC-034`: un cavetto Dupont femmina-femmina a 7 fili collega il modulo display. Pin 1 = VCC (3V3_DISP) |
| Q1 | Interruttore alimentazione display | **AO3401A** P-MOS SOT-23 | AOS | C15127 | **Basic** | 1,7 M | — | Spegne del tutto il modulo display di notte (`DEC-009`); VGS(th) −0,5…−1,3 V, pilotabile a 3,3 V |
| R16 / R17 | Gate di Q1 | 1 kΩ / 100 kΩ 0603 | Uni-Royal | C21190 / C25803 | **Basic** | — | — | R17 tiene Q1 spento durante reset e boot |
| C9 | Bulk 3V3_DISP | 10 µF 0603 | Samsung | C19702 | **Basic** | — | — | Vicino a J2 |
| R8, R9 | Smorzamento SCLK/MOSI | 22 Ω 0603 | Uni-Royal | C23345 | **Basic** | 6 M | — | Valore da confermare con la prova sul cavo reale (`OPEN-021`) |
| R15 | Pull-up RST display | 10 kΩ 0603 | Uni-Royal | C25804 | **Basic** | — | — | Verso 3V3_DISP: niente corrente nel modulo spento |
| J3, J4 | Modulo SHT40, modulo RTC | **SM04B-SRSS-TB** JST-SH 4P 1,0 mm | JST | C160404 | Extended | 45 700 | 0,21 $ | Pinout Qwiic/STEMMA QT: 1 GND, 2 3V3, 3 SDA, 4 SCL; footprint identico alla libreria KiCad |
| J5 | Pulsante remoto | **SM02B-SRSS-TB** JST-SH 2P | JST | C160402 | Extended | 67 085 | 0,13 $ | `DEC-027`, `DEC-032` |
| R6, R7, R22 | Pull-up EN, IO9, pulsante | 10 kΩ 0603 | Uni-Royal | C25804 | **Basic** | 43 M | — | |
| R19, R20 | Pull-up I²C | 4,7 kΩ 0603 | Uni-Royal | C23162 | **Basic** | 16 M | — | Tengono alti anche gli strapping IO2 e IO8 (prova di boot in `VT-PCB-004`) |
| R5, R21 | Isolamento blocchi | 0 Ω 0603 | Uni-Royal | C21189 | **Basic** | 19 M | — | 5 V → LDO, 3,3 V → moduli esterni |
| TP1–TP11 | Punti di test | Pad Ø 1,5 mm sul retro | — | — | — | — | — | Non assemblati; etichetta con riferimento e nome della rete |

\* Stock e prezzo unitario (fascia più bassa) dal catalogo JLCPCB il 2026-11-07; "M" = milioni.

**Parti Extended:** 8 codici distinti (C41349510, C165948, C2977522, C7519, C404027, C46061680, C160404, C160402): rispetto alla rev 0.1 sparisce il connettore FFC ed entrano LDO e header. Costi in [08](08-bom-preliminare.md) §8.

### 2.1 Assegnazione GPIO (ESP32-C3-MINI-1-H4X)

Il modulo espone 15 GPIO (IO0–IO10, IO18–IO21). Senza touch restano **liberi IO0 e IO1**, portati su punti di test.

| GPIO | Pin modulo | Segnale | Note |
|---|---:|---|---|
| IO0 / IO1 | 12 / 13 | liberi | Punti di test TP9/TP10; risveglio da deep-sleep possibile (GPIO0–5) |
| IO2 | 5 | I2C_SDA | Strapping: Espressif raccomanda pull-up → R19 4,7 kΩ |
| IO3 | 6 | BTN_USER | Pulsante (attivo basso), risveglio da deep-sleep possibile |
| IO4 | 18 | LCD_DC | |
| IO5 | 19 | LCD_RST | Pull-up 10 kΩ (R15) verso 3V3_DISP |
| IO6 | 20 | LCD_SCLK | Pin IO_MUX di FSPICLK, 22 Ω in serie |
| IO7 | 21 | LCD_MOSI | Pin IO_MUX di FSPID, 22 Ω in serie |
| IO8 | 22 | I2C_SCL | Strapping: deve valere 1 per il download → R20 4,7 kΩ |
| IO9 | 23 | BOOT | Strapping (1 = avvio da flash), pull-up 10 kΩ; punto di test TP11 per forzare il download (`DEC-039`) |
| IO10 | 16 | LCD_CS | Pin IO_MUX di FSPICS0 |
| IO18 / IO19 | 26 / 27 | USB D- / D+ | USB Serial/JTAG nativa: flash, log, configuratore (`DEC-020`) |
| IO20 (RXD0) | 30 | DISP_EN_N | Basso = modulo display alimentato; all'avvio la ROM non lo pilota e R17 tiene il display spento |
| IO21 (TXD0) | 31 | UART_TX | Solo punto di test (log ROM di riserva) |

## 3. Modulo display (fuori dal montaggio JLC)

`DEC-034`: modulo **GC9A01 1,28" 240×240 IPS a colori** su schedina con 7 piedini a passo 2,54 mm, provabile su breadboard. Esempio scelto dal proprietario: [AliExpress, SZHJW Technology Store, articolo 1005009766462228](https://it.aliexpress.com/item/1005009766462228.html), circa 4,24 € (prezzo letto il 2026-11-07).

- **Piedini** (dalla foto dell'inserzione, dall'alto): RST, CS, DC, SDA, SCL, GND, VCC. Sulla scheda principale J2 ha l'ordine inverso (1 VCC, 2 GND, 3 SCL, 4 SDA, 5 DC, 6 CS, 7 RST), così un cavetto dritto a 7 fili collega pin 1 → VCC. **Da verificare sulla serigrafia del modulo ricevuto** prima del primo collegamento.
- **Niente touch e niente pin BLK**: la retroilluminazione è sempre accesa quando il modulo è alimentato. Di notte Q1 toglie l'alimentazione al modulo (display spento, `DEC-009`); di giorno l'attenuazione si fa solo con colori più scuri (modifica di `DEC-007`).
- Il modulo ha regolatore o resistenze a bordo non documentati: alimentato a 3,3 V da J2. Corrente e tensione della retroilluminazione si misurano su banco (M1).
- Con il modulo spento il firmware porta a livello basso SCLK, MOSI, DC, CS e RST, per non alimentarlo attraverso gli ingressi.

## 4. Sensore SHT40 su modulo commerciale

`DEC-028`: modulo breakout commerciale (es. "SHT40 modulo sensore di umidità e temperatura I²C, 3V 5V, nero, con pin") collegato a J3.

- **Alimentazione a 3,3 V** dal pin 2 di J3 (`3V3_EXT`). L'SHT40 accetta 1,08–3,6 V (datasheet V7.3).
- **Cavo**: JST-SH 4 poli lato scheda (1 GND, 2 3V3, 3 SDA, 4 SCL) → jumper femmina 2,54 mm sui pin del modulo. L'**ordine dei pin del modulo va letto sulla sua serigrafia** (`OPEN-002`).
- **LED e regolatore del breakout (P1-09)**: controllare sul modulo ricevuto se c'è un LED di accensione (da rimuovere o disattivare) e un regolatore; annotare la corrente a riposo misurata. Vedi `BOM-002`.
- **Pull-up**: quelli del modulo restano in parallelo a R19/R20 (4,7 kΩ); con 10 kΩ sia sul modulo SHT40 sia sul DS3231 si arriva a circa 2,4 kΩ, entro i limiti I²C a 3,3 V.

## 5. Elementi fuori dal montaggio JLC

| Elemento | Scelta | Stato | Note |
|---|---|---|---|
| Display | Modulo GC9A01 1,28" 7 pin (§3) | CONF (`DEC-034`) | Pinout da verificare sul modulo ricevuto |
| Cavo display | Cavetto Dupont femmina-femmina 7 fili | CAND | Lunghezza dal CAD; prova SPI sul cavo reale (`OPEN-021`) |
| RTC con tampone | **Adafruit DS3231 Precision RTC – STEMMA QT** (5188) + pila **CR1220** | CONF (`DEC-024`) | I²C 0x68; pull-up 10 kΩ verso Vin; LED "ON" disattivabile tagliando il ponticello |
| Sensore T/RH | Modulo breakout SHT40 | CAND (`DEC-028`) | §4 |
| Cavetti | JST-SH 4 poli Qwiic (RTC), JST-SH 4 poli → jumper femmina (SHT40), JST-SH 2 poli (pulsante) | CAND | Lunghezze dal CAD |

### 5.1 Perché l'RTC non è sulla scheda

Il candidato iniziale **RV-3028-C7** risulta a **stock 0** su LCSC/JLC (C3019759, C2829066). Il proprietario ha scelto il **modulo esterno via cavo** (`DEC-024`): pila CR1220 con durata di anni, precisione ±2 ppm. La pila serve **solo** all'RTC e non contraddice `DEC-023`.

## 6. Rischi residui

- **Modulo display senza datasheet**: pinout dalla foto dell'inserzione, corrente della retroilluminazione ignota: verifica su banco prima del montaggio finale.
- **Termica dell'LDO**: SOT-23-5 a 231 °C/W (JEDEC); con ~80 mA stimati la dissipazione è ~0,14 W (+14…32 °C). Da misurare a scocca chiusa (`VT-PWR-002`).
- **ESP32-C3 H4X**: stock limitato (~2 800 pezzi) e richiede ESP-IDF recente; ricontrollare la disponibilità all'ordine.
- **Header SMD a 90°**: footprint EasyEDA non confrontato con un disegno ufficiale del produttore (non trovato); verificare passo 2,54 mm e lunghezza dei piedini sul primo campione.
