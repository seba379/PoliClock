# 12 — Selezione componenti per lo schema (M2)

**Versione:** 0.6 · **Stato:** schema rev 0.1 disegnato, **non validato** (manca il prototipo M1) · **Data:** 2026-11-07

Questo documento motiva i componenti usati nello schema KiCad in [`hardware/`](../hardware/README.md). Tutte le scelte restano `CAND` finché non superano il prototipo su banco (M1) e la revisione visiva del proprietario; le decisioni del proprietario prese durante il disegno sono registrate in [10](10-decisioni-aperte.md) (`DEC-024`…`DEC-027`).

## 1. Criterio di scelta

- **Vincolo del proprietario:** componenti **facilmente reperibili e montabili direttamente da JLCPCB** (libreria LCSC), **connettori inclusi**. Preferenza: parti **Basic** (nessun costo di setup), poi **Preferred**, poi **Extended** solo se necessario.
- Pinout e funzioni verificati sui **datasheet ufficiali** (vedi [fonti](11-fonti.md), sezione "Componenti dello schema"). Simboli e footprint delle parti specifiche importati da LCSC/EasyEDA con `easyeda2kicad` e poi corretti (tipi elettrici dei pin, campo `LCSC`, die pad dell'SHT40).
- Stock e prezzi letti dal catalogo JLCPCB/LCSC il **2026-11-07**: cambiano ogni giorno, vanno **ricontrollati prima dell'ordine**.

## 2. Scheda principale (`hardware/policlock-main`)

| Rif. | Funzione | Componente | Produttore | LCSC | Libreria JLC | Stock* | Prezzo* | Note di verifica |
|---|---|---|---|---|---|---:|---:|---|
| U3 | MCU | **ESP32-C3-MINI-1-N4** | Espressif | C2838502 | Extended | 12 652 | 3,05 $ | Pin e strapping dal datasheet v2.2 (tab. 3-1, 4-1, 4-3). Alimentazione 3,0–3,6 V, sorgente ≥ 0,5 A |
| J1 | USB-C 2.0 | **TYPE-C-31-M-12** (16P) | Korean Hroparts | C165948 | Extended | 308 225 | 0,19 $ | Ricettacolo più diffuso su JLC; solo D+/D-, CC, VBUS, GND |
| R1, R2 | CC sink | 5,1 kΩ 0603 1 % | Uni-Royal | C23186 | **Basic** | 20 M | — | Rd 5,1 kΩ su CC1 e CC2: 5 V senza USB-PD |
| F1 | Protezione VBUS | **BSMD0805-050-12V** PTC 0805 | BHFUSE | C2977522 | Extended | 58 790 | 0,05 $ | Hold 0,5 A / trip 1 A, 12 V. Nessun fusibile/PTC tra le parti Basic |
| U1 | ESD D+/D-/VBUS | **USBLC6-2SC6** | STMicroelectronics | C7519 | Extended | 25 615 | 0,16 $ | Pinout SOT23-6: 1/6 I/O1, 3/4 I/O2, 2 GND, 5 VBUS. Alternativa compatibile più economica: UMW C2687116 |
| R3, R4 | Serie D+/D- | 0 Ω 0603 | Uni-Royal | C21189 | **Basic** | 19 M | — | Isolamento/sostituibili con 22 Ω se il bring-up lo richiede |
| U2 | LDO 5 V → 3,3 V | **AMS1117-3.3** SOT-223 | AMS | C6186 | **Basic** | 1,6 M | 0,21 $ | 1 A; pin 1 GND, 2 VOUT, 3 VIN. Dropout ~1 V: a 4,75 V di VBUS resta margine. Cout 22 µF: il datasheet caratterizza con tantalio → stabilità con MLCC da verificare (`OPEN-025`) |
| C3 | Uscita LDO | 22 µF 0805 X5R 25 V | Samsung | C45783 | **Basic** | 3,4 M | — | |
| C1, C2, C5 | Bulk | 10 µF 0603 X5R 10 V | Samsung | C19702 | **Basic** | 10 M | — | |
| C4, C6, C8 | Disaccoppiamento / antirimbalzo | 100 nF 0603 X7R | Yageo | C14663 | **Basic** | 34 M | — | |
| C7 | RC su EN | 1 µF 0603 | Samsung | C15849 | **Basic** | 13 M | — | Espressif: R 10 kΩ + C 1 µF |
| SW1, SW2 | RESET, BOOT | **TS-1088-AR02016** 4×3 mm, 2 pin | XUNPU | C720477 | **Basic** | 509 240 | — | `DEC-029`: scelto per ridurre l'ingombro; datasheet XUNPU: contatto tra pin 1 e 2 |
| Q1 | Retroilluminazione | **AO3400A** N-MOS SOT-23 | AOS | C20917 | **Basic** | 1 M | 0,09 $ | VGS(th) max 1,45 V: pilotabile a 3,3 V |
| R16, R17, R18 | Gate, pull-down, limitazione LED | 100 Ω / 100 kΩ / 10 Ω 0603 | Uni-Royal | C22775 / C25803 / C22859 | **Basic** | — | — | R18 = 10 Ω come nello schema di riferimento Waveshare: **TBD** dal datasheet del pannello acquistato (`OPEN-024`) |
| R8, R9 | Smorzamento SCLK/MOSI | 22 Ω 0603 | Uni-Royal | C23345 | **Basic** | 6 M | — | Valore da confermare con la prova sul cavo reale (`OPEN-021`) |
| J2 | Cavo display | **AFC01-S16FCA-00** FFC 16P 0,5 mm, ZIF a sportello, contatti in basso, H 2,0 mm | JUSHUO | C262665 | Extended | 59 810 | 0,10 $ | `DEC-026`. Footprint EasyEDA da confrontare col disegno JUSHUO nel layout |
| J3, J4 | Modulo SHT40, modulo RTC | **SM04B-SRSS-TB** JST-SH 4P 1,0 mm | JST | C160404 | Extended | 45 700 | 0,21 $ | Pinout Qwiic/STEMMA QT: 1 GND, 2 3V3, 3 SDA, 4 SCL |
| J5 | Pulsante remoto | **SM02B-SRSS-TB** JST-SH 2P | JST | C160402 | Extended | 67 085 | 0,13 $ | `DEC-027`, `DEC-032`: unico ingresso del pulsante |
| R6, R7, R15, R22 | Pull-up EN, IO9, LCD_RST, pulsante | 10 kΩ 0603 | Uni-Royal | C25804 | **Basic** | 43 M | — | |
| R19, R20 | Pull-up I²C | 4,7 kΩ 0603 | Uni-Royal | C23162 | **Basic** | 16 M | — | Tengono alti anche gli strapping IO2 e IO8 |
| R5, R10, R21 | Isolamento blocchi | 0 Ω 0603 | Uni-Royal | C21189 | **Basic** | 19 M | — | 5 V → LDO, 3,3 V → display, 3,3 V → moduli esterni |
| R11–R14 | Predisposizione touch | 0 Ω / 10 kΩ 0603 | Uni-Royal | C21189 / C25804 | **Basic** | — | — | **DNP** (non montati, `DEC-019`) |
| TP1–TP8 | Punti di test | Pad Ø 1,5 mm | — | — | — | — | — | Non assemblati |

\* Stock e prezzo unitario (fascia più bassa) dal catalogo JLCPCB il 2026-11-07; "M" = milioni.

**Parti Extended sulla scheda principale:** 7 codici distinti (C2838502, C165948, C7519, C2977522, C262665, C160404, C160402). JLC applica un costo fisso per ogni codice Extended distinto per ordine: l'importo esatto va letto sul preventivo (`BOM-001`).

### 2.1 Assegnazione GPIO (ESP32-C3-MINI-1)

Il modulo espone 15 GPIO (IO0–IO10, IO18–IO21). La V1 ne usa 14 per le funzioni più IO21 su un punto di test: **non serve l'ESP32-S3**. Non resta alcun GPIO libero: un'eventuale funzione aggiuntiva richiederebbe di rinunciare al touch (IO0/IO1) o di passare all'S3.

| GPIO | Pin modulo | Segnale | Note |
|---|---:|---|---|
| IO0 | 12 | TP_INT | Ingresso interrupt touch (predisposto); risveglio da deep-sleep possibile (GPIO0–5) |
| IO1 | 13 | TP_RST | Reset touch (predisposto) |
| IO2 | 5 | I2C_SDA | Strapping: Espressif raccomanda pull-up → R19 4,7 kΩ |
| IO3 | 6 | BTN_USER | Pulsante (attivo basso), risveglio da deep-sleep possibile |
| IO4 | 18 | LCD_DC | |
| IO5 | 19 | LCD_RST | Pull-up 10 kΩ (R15) |
| IO6 | 20 | LCD_SCLK | Pin IO_MUX di FSPICLK |
| IO7 | 21 | LCD_MOSI | Pin IO_MUX di FSPID |
| IO8 | 22 | I2C_SCL | Strapping: deve valere 1 per il download → R20 4,7 kΩ |
| IO9 | 23 | BOOT | Strapping (1 = avvio da flash), pull-up 10 kΩ + tasto BOOT |
| IO10 | 16 | LCD_CS | Pin IO_MUX di FSPICS0 |
| IO18 / IO19 | 26 / 27 | USB D- / D+ | USB Serial/JTAG nativa: flash, log, configuratore (`DEC-020`) |
| IO20 (RXD0) | 30 | LCD_BL | PWM (LEDC) retroilluminazione; all'avvio la ROM non lo pilota e R17 tiene spento il LED |
| IO21 (TXD0) | 31 | UART_TX | Solo punto di test (log ROM di riserva) |

## 3. Schedina portadisplay (`hardware/policlock-display`)

| Rif. | Funzione | Componente | LCSC | Libreria | Stock* | Note |
|---|---|---|---|---|---:|---|
| J1 | Cavo verso la scheda principale | AFC01-S16FCA-00 | C262665 | Extended | 59 810 | Stesso pinout di J2 della scheda principale (pin n → pin n; orientamento del cavo `OPEN-023`) |
| J2 | Pannello GC9A01 con touch (FPC 18 poli) | **AFC01-S18FCA-00** FPC 18P 0,5 mm | C262666 | Extended | 24 180 | `DEC-025`. **Passo, lato contatti e pinout da confermare sul datasheet del pannello acquistato** (`OPEN-016`) |
| C1 / C2, C3 | Bulk / VDD LCD e touch | 10 µF / 100 nF 0603 | C19702 / C14663 | Basic | — | |
| R1 | Anodo retroilluminazione | 0 Ω 0603 | C21189 | Basic | — | Sostituibile da resistenza se il pannello la richiede (`OPEN-024`) |

Pinout del pannello usato nello schema (fonte: schema del modulo Waveshare *1.28inch Touch LCD*, GC9A01 + CST816S): 1 GND, 2 TP_INT, 3 TP_SCL, 4 TP_SDA, 5 TP_RST, 6 TP_VDD, 7 GND, 8 LCD_VDD, 9 D/C, 10 SDA (MOSI), 11 SDO (non collegato), 12 SCL (SCLK), 13 CS, 14 RST, 15 GND, 16 LEDK, 17 LEDA, 18 GND. È un **riferimento**, non il datasheet del pannello: il layout della portadisplay non va ordinato prima di averlo confermato.

## 4. Sensore SHT40 su modulo commerciale

Il mini-PCB SHT40 previsto inizialmente è stato **eliminato** (`DEC-028`): il proprietario ha scelto un modulo breakout commerciale (es. "SHT40 modulo sensore di umidità e temperatura I²C, 3V 5V, nero, con pin"), collegato a J3 della scheda principale.

- **Alimentazione a 3,3 V** dal pin 2 di J3 (`3V3_EXT`). I moduli "3V 5V" di solito hanno regolatore e adattatori di livello; a 3,3 V funzionano comunque perché l'SHT40 accetta 1,08–3,6 V (datasheet V7.3). Verificare sul modulo acquistato.
- **Cavo**: JST-SH 4 poli lato scheda (1 GND, 2 3V3, 3 SDA, 4 SCL) → jumper femmina 2,54 mm sui pin del modulo, oppure fili saldati direttamente. L'**ordine dei pin del modulo va letto sulla sua serigrafia** (`OPEN-002`): non è standard.
- **LED**: se il modulo ha un LED di accensione, rimuoverlo o tagliarne il ponticello: scalderebbe il sensore.
- **Pull-up**: quelli del modulo restano in parallelo a R19/R20 (4,7 kΩ); se anche il modulo SHT40 monta 10 kΩ, con quelli del DS3231 si arriva a circa 2,4 kΩ, ancora entro i limiti I²C a 3,3 V.
- Posizione: vano ventilato lontano da scheda principale, regolatore e retroilluminazione (`OPEN-011`).

## 5. Elementi fuori dal montaggio JLC

| Elemento | Scelta | Stato | Note |
|---|---|---|---|
| RTC con tampone | **Adafruit DS3231 Precision RTC – STEMMA QT** (prodotto 5188) + pila **CR1220** | CONF (`DEC-024`) | DS3231 con oscillatore compensato in temperatura; I²C 0x68; pull-up 10 kΩ verso Vin sul modulo; LED "ON" disattivabile tagliando il ponticello (consigliato: meno calore). Collegato a J4 con cavo JST-SH 4 poli |
| Pannello display | GC9A01 1,28" 240×240 **con touch** CST816S, FPC 18 poli | CAND (`DEC-025`, `OPEN-016`) | Acquistare solo con datasheet/pinout FPC |
| Cavo display | FFC 16 poli passo 0,5 mm, lunghezza dal CAD | CAND | Tipo (contatti stesso lato/opposti) da fissare col layout (`OPEN-023`) |
| Sensore T/RH | Modulo breakout SHT40 commerciale con header 2,54 mm | CAND (`DEC-028`) | Vedi §4 |
| Cavetti | JST-SH 4 poli Qwiic (RTC), JST-SH 4 poli → jumper femmina (SHT40), JST-SH 2 poli (pulsante) | CAND | Lunghezze dal CAD |

### 5.1 Perché l'RTC non è sulla scheda

Il candidato iniziale **RV-3028-C7** risulta a **stock 0** su LCSC/JLC (C3019759, C2829066) e non è montabile. Le alternative sul PCB valutate (RV-3032-C7 Extended; PCF85063A + quarzo; PCF8563T Preferred) sono state presentate al proprietario, che ha scelto il **modulo esterno via cavo** (`DEC-024`): niente tampone da dimensionare sul PCB, pila CR1220 con durata di anni invece di giorni, precisione ±2 ppm adatta a un orologio senza NTP. La pila a bottone serve **solo** all'RTC e non contraddice `DEC-023` (nessuna batteria di alimentazione).

## 6. Rischi residui

- **AMS1117 con MLCC** (`OPEN-025`): se il bring-up mostra oscillazioni, sostituire con un LDO stabile con ceramici (es. ME6211C33M5G-N C82942 o AP2112K-3.3, Extended, footprint diverso → da decidere prima del layout).
- **Pannello**: senza datasheet del pannello acquistato, J2 della portadisplay, R18 e l'alimentazione di LEDA restano provvisori.
- **Footprint EasyEDA**: vanno confrontati con i disegni dei produttori durante il layout (in particolare FFC 16P e USB-C).
