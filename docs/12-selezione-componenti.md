# 12 — Selezione componenti per lo schema (M2)

**Versione:** 0.9 · **Stato:** schema rev 0.2 dopo la revisione tecnica indipendente, **non validato** (manca il prototipo M1) · **Data:** 2026-11-09

Questo documento motiva i componenti dello schema KiCad in [`hardware/`](../hardware/README.md). Tutte le scelte restano `CAND` finché non superano il prototipo su banco (M1) e la revisione visiva del proprietario; le decisioni del proprietario sono in [10](10-decisioni-aperte.md) (`DEC-024`…`DEC-044`). Tutti i componenti montati da JLC sono nella libreria LCSC/JLC e il progetto segue le regole JLCPCB (`SC-008`, `DEC-040`); i connettori J2–J5 a foro passante li salda a mano il proprietario (`DEC-043`).

**Novità della rev 0.2** (revisione tecnica indipendente del 2026-11-07, esito "NOT APPROVED FOR FABRICATION" sulla rev 0.1):

- LDO **TLV75533** stabile con condensatori ceramici al posto dell'AMS1117 (P0-04, `DEC-037`);
- modulo **ESP32-C3-MINI-1-H4X** ("Recommended") al posto dell'N4 (NRND) (P1-05, `DEC-035`), poi sostituito dall'**ESP32-C3-WROOM-02-N4** per l'assemblaggio Economic (`DEC-044`);
- display su **modulo GC9A01 a 7 pin** pronto per breadboard: niente pannello nudo, schedina portadisplay, cavo FFC e touch (P0-02/P0-03 superati, `DEC-034`);
- USB-C con il **footprint della libreria KiCad** ricavato dal disegno HRO (P1-08).

## 1. Criterio di scelta

- **Vincolo del proprietario:** componenti **facilmente reperibili e montabili direttamente da JLCPCB** (libreria LCSC), **connettori inclusi** (eccezione `DEC-043`: J2–J5 a foro passante, dalla scorta del proprietario e saldati a mano). Preferenza: parti **Basic** (nessun costo di setup), poi **Preferred**, poi **Extended** solo se necessario.
- Pinout e funzioni verificati sui **datasheet ufficiali** (vedi [fonti](11-fonti.md), sezione "Componenti dello schema").
- Footprint: libreria ufficiale KiCad dove esiste (passivi, SOT, USB-C HRO, header di test); altrimenti importati da LCSC/EasyEDA con `easyeda2kicad` e **confrontati**: JST-SH identici alla libreria KiCad (scarti ≤ 0,004 mm); USB-C EasyEDA **scartato** perché diverso dal disegno HRO. Con `DEC-043` J2–J5 usano direttamente le impronte standard di KiCad 10 (`Connector_PinHeader_2.54mm`, `Connector_JST`).
- Stock e prezzi letti dal catalogo JLCPCB/LCSC il **2026-11-07**: cambiano ogni giorno, vanno **ricontrollati prima dell'ordine**.

## 2. Scheda principale (`hardware/policlock-main`)

| Rif. | Funzione | Componente | Produttore | LCSC | Libreria JLC | Stock* | Prezzo* | Note di verifica |
|---|---|---|---|---|---|---:|---:|---|
| U3 | MCU | **ESP32-C3-WROOM-02-N4** | Espressif | C2934560 | Extended | 13 113 | ~3,31 $ | `DEC-044` (supera `DEC-035`). Pagina JLC (2026-11-08): **PCBA "Economic and Standard"**, nessuna radiografia richiesta (l'H4X C41349510 è "Standard Only" con radiografia, FIN-001). Selettore prodotti Espressif (2026-11-08): **Mass Production**, chip v0.x; nessuna variante "X" con chip v1.1 per il WROOM-02. Datasheet v1.7: chip v0.4, 4 MB, −40…85 °C, 18 × 20 × 3,2 mm, 19 pin (EPAD = 19, GND), antenna 6 mm a un'estremità. ESP-IDF v6.0/v6.1 (C:\esp) supporta v0.4 (`ESP32C3_REV_MIN` predefinito v0.3). Impronta `PoliClock:ESP32-C3-WROOM-02` (§1) |
| J1 | USB-C 2.0 | **TYPE-C-31-M-12** (16P) | Korean Hroparts | C165948 | Extended | 308 225 | 0,19 $ | Footprint della libreria KiCad (`USB_C_Receptacle_HRO_TYPE-C-31-M-12`, dal disegno HRO), serigrafia frontale tolta perché il guscio sporge 0,4 mm dal bordo |
| R1, R2 | CC sink | 5,1 kΩ 0603 1 % | Uni-Royal | C23186 | **Basic** | 20 M | — | Rd 5,1 kΩ su CC1 e CC2: 5 V senza USB-PD |
| F1 | Protezione VBUS | **BSMD0805-050-12V** PTC 0805 | BHFUSE | C2977522 | Extended | 58 790 | 0,05 $ | Hold 0,5 A / trip 1 A, 12 V |
| U1 | ESD D+/D-/VBUS | **USBLC6-2SC6** | STMicroelectronics | C7519 | Extended | 25 615 | 0,16 $ | Pinout SOT23-6: 1/6 I/O1, 3/4 I/O2, 2 GND, 5 VBUS. Passaggio diretto: I/O1 su D-, I/O2 su D+ (`DEC-041`); sull'asse della coppia, a circa 4 mm dai contatti del connettore |
| R3, R4 | Serie D+/D- | 0 Ω 0603 | Uni-Royal | C21189 | **Basic** | 19 M | — | Isolamento; sostituibili con 22 Ω se il bring-up lo richiede |
| U2 | LDO 5 V → 3,3 V | **TLV75533PDBVR** SOT-23-5 | Texas Instruments | C404027 | Extended | 94 177 | 0,12 $ | `DEC-037`. Datasheet SBVS320D: 500 mA, pin 1 IN, 2 GND, 3 EN, 4 NC, 5 OUT; **stabile con MLCC ≥ 1 µF** (capacità effettiva > 0,47 µF); RθJA 231 °C/W JEDEC, 100,8 °C/W sulla scheda di valutazione TI. EN collegato a IN |
| C2 / C3, C4 | Ingresso / uscita LDO | **4,7 µF 0603 X5R 16 V** (CL10A475KO8NNNC) / 10 µF + 100 nF 0603 | Samsung / Yageo | **C19666** / C19702, C14663 | **Basic** (C19666 Basic e a magazzino, pagina JLC consultata il 2026-11-08) | — | — | A 2,4–2,8 mm dai pin di U2, ritorno a GND sul piano. C2 ridotto da 10 a 4,7 µF per lo spunto USB (`OPEN-029`); TLV75533 stabile con ≥ 1 µF |
| C1 | Ingresso +5 V dopo il PTC | **1 µF 0603** (era 10 µF) | Samsung | **C15849** | **Basic** | 13 M | — | C1 + C2 = 5,7 µF nominali su VBUS, sotto i 10 µF ammessi all'inserzione USB (`OPEN-029`) |
| C5 | 3V3 modulo | 10 µF 0603 X5R 10 V | Samsung | C19702 | **Basic** | 10 M | — | C5 + C6 (100 nF) sul pin 3V3 del modulo come nello schema di riferimento Espressif |
| C6, C8, C10 | Disaccoppiamento / antirimbalzo | 100 nF 0603 X7R | Yageo | C14663 | **Basic** | 34 M | — | C6 a 2,4 mm dal pin 3 (3V3) del modulo |
| C7 | RC su EN | 1 µF 0603 | Samsung | C15849 | **Basic** | 13 M | — | Espressif: R 10 kΩ + C 1 µF, pista EN corta. Nessun tasto RESET/BOOT (`DEC-039`): punti di test TP6 (EN) e TP11 (IO9) |
| J2 | Modulo display | **Header maschio 1×8 2,54 mm a foro passante** (`DEC-049`), a 90° (negli stessi fori va bene anche diritto); impronta `PinHeader_1x08_P2.54mm_Horizontal` | generico | — | **a mano** (`DEC-043`) | scorta del proprietario | — | `DEC-034`: un cavetto Dupont femmina-femmina a 7 fili collega il modulo display sui pin 1–7; pin 8 = BUSY per un eventuale e-paper (`DEC-049`). Prima (fino a `DEC-043`): HX PZ2.54-1x7P WT SMD, C46061680, Extended. Pin 1 = VCC (3V3_DISP) |
| Q1 | Interruttore alimentazione display | **AO3401A** P-MOS SOT-23 | AOS | C15127 | **Basic** | 1,7 M | — | Spegne del tutto il modulo display di notte (`DEC-009`); VGS(th) −0,5…−1,3 V, pilotabile a 3,3 V |
| R16 / R17 | Gate di Q1 | **10 kΩ** / 100 kΩ 0603 | Uni-Royal | **C25804** / C25803 | **Basic** | — | — | FIN-003: R16 da 1 k a 10 k. R17 tiene Q1 spento durante reset e boot; con IO20 basso il gate va a 3,3 × 10/110 ≈ 0,3 V, quindi V_GS ≈ −3,0 V (AO3401A: R_DS(on) specificata già a −2,5 V) |
| C11 | Rampa di accensione del display | **10 nF** 0603 X7R 50 V (0603B103K500NT) | FH | **C57112** | **Basic** (pagina JLC 2026-11-08, Economic e Standard) | — | — | FIN-003: fra gate (DISP_G) e drain (3V3_DISP) di Q1, montato. Con R16 10 kΩ la tensione su 3V3_DISP sale in circa 0,2–0,3 ms invece di pochi µs: lo spunto verso C9 e il modulo display non fa crollare il 3V3 del modulo (stima, da misurare in `VT-PWR-003`) |
| C9 | Bulk 3V3_DISP | 10 µF 0603 | Samsung | C19702 | **Basic** | — | — | Vicino a J2 |
| R8, R9 | Smorzamento SCLK/MOSI | 22 Ω 0603 | Uni-Royal | C23345 | **Basic** | 6 M | — | Valore da confermare con la prova sul cavo reale (`OPEN-021`) |
| R15 | Pull-up RST display | 10 kΩ 0603 | Uni-Royal | C25804 | **Basic** | — | — | Verso 3V3_DISP: niente corrente nel modulo spento |
| R23 | Serie su BUSY (`DEC-049`) | 1 kΩ 0603 1 % (0603WAF1001T5E) | Uni-Royal | C21190 | **Basic** (pagina JLC 2026-11-09, Economic e Standard) | — | — | Fra J2 pin 8 e IO1: limita la corrente verso un modulo spento o in caso di conflitto; livello definito dal pull-down interno di IO1 |
| J3, J4 | Modulo SHT40, modulo RTC | **B4B-PH-K-S** JST PH 4P 2,0 mm, verticale (ingresso dall'alto), a foro passante; impronta `JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical` | JST | — | **a mano** (`DEC-043`) | scorta del proprietario | — | Stesso pinout di prima: 1 GND, 2 3V3, 3 SDA, 4 SCL. Prima: SM04B-SRSS-TB JST-SH, C160404, Extended |
| J5 | Pulsante remoto | **B4B-PH-K-S** JST PH 4P (stesso connettore di J3/J4) | JST | — | **a mano** (`DEC-043`) | scorta del proprietario | — | Pin 1 BTN_USER, pin 2 GND, pin 3–4 non collegati (NC espliciti nello schema). `DEC-027`, `DEC-032`. Prima: SM02B-SRSS-TB, C160402, Extended |
| R6, R7, R22 | Pull-up EN, IO9, pulsante | 10 kΩ 0603 | Uni-Royal | C25804 | **Basic** | 43 M | — | |
| R19, R20 | Pull-up I²C | 4,7 kΩ 0603 | Uni-Royal | C23162 | **Basic** | 16 M | — | Tengono alti anche gli strapping IO2 e IO8 (prova di boot in `VT-PCB-004`) |
| R5, R21 | Isolamento blocchi | 0 Ω 0603 | Uni-Royal | C21189 | **Basic** | 19 M | — | 5 V → LDO, 3,3 V → moduli esterni |
| TP1–TP11 | Punti di test | Pad Ø 1,5 mm sul retro | — | — | — | — | — | Non assemblati; etichetta con riferimento e nome della rete |

\* Stock e prezzo unitario (fascia più bassa) dal catalogo JLCPCB il 2026-11-07; "M" = milioni.

**Parti Extended:** 5 codici distinti (C2934560, C165948, C2977522, C7519, C404027). Rispetto alla rev 0.1 sparisce il connettore FFC ed entra l'LDO; con `DEC-043` escono anche header e JST-SH (C46061680, C160404, C160402), sostituiti da connettori a foro passante saldati a mano. Costi in [08](08-bom-preliminare.md) §8.

### 2.1 Assegnazione GPIO (ESP32-C3-WROOM-02-N4, `DEC-044`)

Il modulo espone 15 GPIO (IO0–IO10, IO18–IO21). Senza touch restavano liberi IO0 e IO1. Dal `DEC-049` IO1 legge il BUSY di un eventuale e-paper e **IO0 resta libero** su TP9; la verifica dei due pin sui datasheet Espressif è in [10](10-decisioni-aperte.md) §16.

| GPIO | Pin modulo | Segnale | Note |
|---|---:|---|---|
| IO0 | 18 | libero | Punto di test TP9; risveglio da deep-sleep possibile (GPIO0–5) |
| IO1 | 17 | DISP_BUSY | J2 pin 8 attraverso R23 1 kΩ; ingresso con pull-down interno (firmware); punto di test TP10. Non è strapping e non ha glitch all'accensione (`DEC-049`) |
| IO2 | 16 | I2C_SDA | Strapping: Espressif raccomanda pull-up → R19 4,7 kΩ |
| IO3 | 15 | BTN_USER | Pulsante (attivo basso), risveglio da deep-sleep possibile |
| IO4 | 3 | LCD_DC | |
| IO5 | 4 | LCD_RST | Pull-up 10 kΩ (R15) verso 3V3_DISP |
| IO6 | 5 | LCD_SCLK | Pin IO_MUX di FSPICLK, 22 Ω in serie |
| IO7 | 6 | LCD_MOSI | Pin IO_MUX di FSPID, 22 Ω in serie |
| IO8 | 7 | I2C_SCL | Strapping: deve valere 1 per il download → R20 4,7 kΩ |
| IO9 | 8 | BOOT | Strapping (1 = avvio da flash), pull-up 10 kΩ; punto di test TP11 per forzare il download (`DEC-039`) |
| IO10 | 10 | LCD_CS | Pin IO_MUX di FSPICS0 |
| IO18 / IO19 | 13 / 14 | USB D- / D+ | USB Serial/JTAG nativa: flash, log, configuratore (`DEC-020`) |
| IO20 (RXD) | 11 | DISP_EN_N | Basso = modulo display alimentato; all'avvio la ROM non lo pilota e R17 tiene il display spento |
| IO21 (TXD) | 12 | UART_TX | Solo punto di test (log ROM di riserva) |

## 3. Modulo display (fuori dal montaggio JLC)

`DEC-034`: modulo **GC9A01 1,28" 240×240 IPS a colori** su schedina con 7 piedini a passo 2,54 mm, provabile su breadboard. Esempio scelto dal proprietario: [AliExpress, SZHJW Technology Store, articolo 1005009766462228](https://it.aliexpress.com/item/1005009766462228.html), circa 4,24 € (prezzo letto il 2026-11-07).

- **Piedini** (dalla foto dell'inserzione, dall'alto): RST, CS, DC, SDA, SCL, GND, VCC. Sulla scheda principale J2 ha l'ordine inverso (1 VCC, 2 GND, 3 SCL, 4 SDA, 5 DC, 6 CS, 7 RST), così un cavetto dritto a 7 fili collega pin 1 → VCC. Il pin 8 di J2 (BUSY, `DEC-049`) serve solo a un eventuale e-paper: con il GC9A01 resta libero. **Da verificare sulla serigrafia del modulo ricevuto** prima del primo collegamento.
- **Niente touch e niente pin BLK**: la retroilluminazione è sempre accesa quando il modulo è alimentato. Di notte Q1 toglie l'alimentazione al modulo (display spento, `DEC-009`); di giorno l'attenuazione si fa solo con colori più scuri (modifica di `DEC-007`).
- Il modulo ha regolatore o resistenze a bordo non documentati: alimentato a 3,3 V da J2. Corrente e tensione della retroilluminazione si misurano su banco (M1).
- Con il modulo spento il firmware porta a livello basso SCLK, MOSI, DC, CS e RST, per non alimentarlo attraverso gli ingressi.

## 4. Sensore SHT40 su modulo commerciale

`DEC-028`: modulo breakout commerciale (es. "SHT40 modulo sensore di umidità e temperatura I²C, 3V 5V, nero, con pin") collegato a J3.

- **Alimentazione a 3,3 V** dal pin 2 di J3 (`3V3_EXT`). L'SHT40 accetta 1,08–3,6 V (datasheet V7.3).
- **Cavo**: JST PH 4 poli lato scheda (J3, `DEC-043`: 1 GND, 2 3V3, 3 SDA, 4 SCL) → jumper femmina 2,54 mm sui pin del modulo. L'**ordine dei pin del modulo va letto sulla sua serigrafia** (`OPEN-002`).
- **LED e regolatore del breakout (P1-09)**: controllare sul modulo ricevuto se c'è un LED di accensione (da rimuovere o disattivare) e un regolatore; annotare la corrente a riposo misurata. Vedi `BOM-002`.
- **Pull-up**: quelli del modulo restano in parallelo a R19/R20 (4,7 kΩ); con 10 kΩ sia sul modulo SHT40 sia sul DS3231 si arriva a circa 2,4 kΩ, entro i limiti I²C a 3,3 V.

## 5. Elementi fuori dal montaggio JLC

| Elemento | Scelta | Stato | Note |
|---|---|---|---|
| Display | Modulo GC9A01 1,28" 7 pin (§3) | CONF (`DEC-034`) | Pinout da verificare sul modulo ricevuto |
| Cavo display | Cavetto Dupont femmina-femmina 7 fili | CAND | Lunghezza dal CAD; prova SPI sul cavo reale (`OPEN-021`) |
| RTC con tampone | **Adafruit DS3231 Precision RTC – STEMMA QT** (5188) + pila **CR1220** | CONF (`DEC-024`) | I²C 0x68; pull-up 10 kΩ verso Vin; LED "ON" disattivabile tagliando il ponticello |
| Sensore T/RH | Modulo breakout SHT40 | CAND (`DEC-028`) | §4 |
| Connettori J2–J5 | Header 1×8 2,54 mm a foro passante (`DEC-049`), 3 × JST PH B4B-PH-K-S | CONF (`DEC-043`) | Saldati a mano dal proprietario dopo l'assemblaggio JLC; nella BOM completa con `Montaggio` = "a mano, parte del proprietario" |
| Cavetti | JST PH 4 poli → JST-SH 4 poli o fili (RTC), JST PH 4 poli → jumper femmina (SHT40), JST PH con i pin 1–2 (pulsante) | CAND | Lunghezze dal CAD; spina PHR-4 con contatti a crimpare o cavetti PH pronti (`BOM-007`) |

### 5.1 Perché l'RTC non è sulla scheda

Il candidato iniziale **RV-3028-C7** risulta a **stock 0** su LCSC/JLC (C3019759, C2829066). Il proprietario ha scelto il **modulo esterno via cavo** (`DEC-024`): pila CR1220 con durata di anni, precisione ±2 ppm. La pila serve **solo** all'RTC e non contraddice `DEC-023`.

## 6. Rischi residui

- **Modulo display senza datasheet**: pinout dalla foto dell'inserzione, corrente della retroilluminazione ignota: verifica su banco prima del montaggio finale.
- **Termica dell'LDO**: SOT-23-5 a 231 °C/W (JEDEC); con ~80 mA stimati la dissipazione è ~0,14 W (+14…32 °C). Da misurare a scocca chiusa (`VT-PWR-002`).
- **ESP32-C3-WROOM-02-N4** (`DEC-044`): chip v0.4 (circa 10 KB di RAM utente in meno del v1.1, irrilevante qui); fissare nel firmware `CONFIG_ESP32C3_REV_MIN` ≤ v0.4. Il pin 3V3 è sul lato del bordo superiore, vicino all'antenna: C5/C6 stanno a circa 16 mm in linea d'aria e la pista fino al pin 1 è di circa 21 mm (0,4 mm, in parte sotto il modulo); EN è di circa 27 mm con 2 vie; il modulo ha 10 µF + 1 µF + 0,1 µF interni. Scorte da ricontrollare all'ordine.
- **Linee esterne senza ESD (FIN-010, rischio accettato)**: BTN_USER (J5, pulsante remoto) e I²C/3V3_EXT (J3/J4) escono dalla scheda protette solo da R22 10 kΩ / C8 100 nF e dai pull-up. Il proprietario non ha scelto la resistenza da 1 kΩ in serie proposta dalla revisione finale: rischio basso per un oggetto da scrivania al chiuso, accettato in modo esplicito.
- **Impronta JST PH (FIN-011)**: non ancora confrontata con il disegno JST (PDF cifrato). Il proprietario ha già i B4B-PH-K-S: prima dei Gerber conviene stampare il layout 1:1 (`policlock-main-layout.pdf`, scala 1:1) e provare l'innesto di un connettore e dell'header, oppure provarli sulla prima scheda nuda.
- **Connettori a foro passante (`DEC-043`)**: J2–J5 si saldano a mano dopo l'assemblaggio JLC; i piedini sporgono sotto la scheda (luce da prevedere, `OPEN-028`). Il rischio dell'header SMD Hanxia (piazzole 1,02 × 3,16 mm contro 3,20 mm del disegno) è superato.

## 7. Verifica di rotazioni e origini nell'anteprima JLC (FIN-004)

La CPL (`policlock-main-cpl-jlcpcb.csv`) riporta posizioni e rotazioni native di KiCad, senza correzioni a priori. All'ordine si controlla **ogni parte orientata** nell'anteprima 2D/3D di JLC; si corregge solo dove serve, caricando una CPL corretta, e si annota qui la correzione per poterla ripetere.

| Rif. | Package | Rotazione CPL | Origine dell'impronta | Cosa controllare nell'anteprima JLC | Correzione applicata |
|---|---|---:|---|---|---|
| U1 | SOT-23-6 (USBLC6-2SC6) | 90° | centro del package | vista dall'alto: pin 1 (USB_DN_C) **in basso a sinistra**, lato verso J1; pin 4–6 in alto (pin 5 = +5V al centro) | da compilare all'ordine |
| U2 | SOT-23-5 (TLV75533) | 0° | centro del package | vista dall'alto: pin 1 = IN **in alto a sinistra** (pin 1-2-3 sulla colonna sinistra, dall'alto in basso); pin 5 = OUT in alto a destra, pin 4 = NC in basso a destra | da compilare all'ordine |
| Q1 | SOT-23 (AO3401A) | 90° | centro del package | vista dall'alto: due pin in basso, pin 1 = G **a sinistra** e pin 2 = S (+3V3) **a destra**; pin 3 = D (3V3_DISP) da solo **in alto** | da compilare all'ordine |
| U3 | ESP32-C3-WROOM-02-N4 | −90° (270°) | **centro delle file di piazzole**, non del corpo: il corpo con l'antenna è spostato di 3,1 mm verso l'antenna (+x). Pronta la **CPL alternativa** `policlock-main-cpl-jlcpcb-u3-centro-corpo.csv` con U3 al centro del corpo (X 37,51 invece di 34,41 mm): caricare quella con cui, nell'anteprima, piazzole e modulo coincidono | antenna sulla scheda verso il bordo destro (`DEC-045`), pin 1 in alto vicino all'antenna; corpo tutto dentro il contorno; EPAD senza vie (`DEC-046`): controllare le 9 aperture di pasta nell'anteprima DFM | da compilare all'ordine |
| J1 | USB-C TYPE-C-31-M-12 | 0° | centro del corpo F.Fab | apertura verso il bordo inferiore, guscio 0,4 mm oltre il bordo; pioli nei fori NPTH; ponti di maschera fra i contatti (min 0,10 mm in verde); eccezione al bordo da far accettare nella DFM. Le 4 linguette del guscio le salda a mano il proprietario (`DEC-047`) | da compilare all'ordine |
| C, R, F1 | 0603 / 0805 | 0° / 90° / 180° (R23) | centro | nessuna polarità; solo posizione | — |

**Altri controlli nell'anteprima e nella DFM JLC** (revisione esterna del 2026-11-08, [docs/10](10-decisioni-aperte.md) §15):

- i tre fiducial, con apertura della maschera e distanza dal bordo;
- la zona antenna senza rame;
- le asole metallizzate di J1, che non devono diventare fori tondi;
- J2–J5 assenti dal montaggio.

Esito e correzioni da annotare in questa tabella.
