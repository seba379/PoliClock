# 11 — Fonti, datasheet e riferimenti

**Versione:** 0.6 · **Aggiornato:** 2026-11-07

## Scheda Waveshare (scartata, `DEC-015`)

Fonti consultate durante la revisione v0.2, mantenute come riferimento storico e per il piano B.

1. [Waveshare — ESP32-S3-Touch-AMOLED-1.75, overview e specifiche](https://docs.waveshare.com/ESP32-S3-Touch-AMOLED-1.75). Conferma MCU ESP32-S3, AMOLED 466×466, 1,75", CO5300, CST9217, RTC PCF85063, PMU AXP2101, QMI8658, header batteria MX1.25.
2. [Waveshare — pagina prodotto standard/B/G](https://www.waveshare.com/product/esp32-s3-touch-amoled-1.75.htm). Descrizioni, varianti e interfaccia USB-C.
3. [Waveshare — schemi, disegni dimensionali, datasheet periferiche ed esempi](https://docs.waveshare.com/ESP32-S3-Touch-AMOLED-1.75/Resources-And-Documents). **Fonte primaria per definire pinout e ingombri: scaricare revisione corretta prima del CAD o dei cablaggi.**
4. [Waveshare — schematico ESP32-S3-Touch-AMOLED-1.75 (PDF)](https://files.waveshare.com/wiki/ESP32-S3-Touch-AMOLED-1.75/ESP32-S3-Touch-AMOLED-1.75.pdf) — versione consultata il 2026-11-07, creata 2025-07-28: bus I²C GPIO14/15 con pull-up 2,2 kΩ, header H2, TS AXP2101 su termistore di scheda, RTC alimentato da AXP2101. Non copiato nel repository (licenza non verificata).
5. [Waveshare — istruzioni ESP-IDF](https://docs.waveshare.com/ESP32-S3-Touch-AMOLED-1.75/Working-with-ESP-IDF) — guida BSP/esempi; verificare versione SDK usata dagli esempi rispetto alla futura versione pinnata.

## Sensore temperatura e umidità

6. [Sensirion — SHT40 official product page](https://sensirion.com/products/catalog/SHT40) — caratteristiche del sensore; accuratezza tipica dichiarata per RH ±1,8%.
7. [Sensirion — SHT4x datasheet V7.3 (PDF)](https://sensirion.com/media/documents/33FD6951/6A7C10A0/HT_DS_Datasheet_SHT4x_V7.3.pdf) — consultata il 2026-11-07 (il link alla revisione precedente non è più valido). Pin 1 SDA, 2 SCL, 3 VDD, 4 VSS (§5.4); die pad da non saldare e niente rame sotto il sensore (§5.3); indirizzo 0x44 per SHT40-AD1B. **Usare sempre la revisione vigente del datasheet al momento dell'acquisto.**

## Toolchain e progettazione

8. [Espressif — ESP-IDF Programming Guide](https://docs.espressif.com/projects/esp-idf/en/stable/esp32c3/) — infrastruttura firmware, driver, NVS, power management (scegliere la variante del chip definitivo).
9. [Espressif — ESP32-C3](https://www.espressif.com/en/products/socs/esp32-c3) e [ESP32-S3](https://www.espressif.com/en/products/socs/esp32-s3) — datasheet, design guidelines hardware e moduli.
10. [KiCad — documentazione](https://docs.kicad.org/) — progettazione schema e PCB; `kicad-cli` per ERC/DRC ed esportazioni.
11. [JLCPCB](https://jlcpcb.com/) — capacità di produzione, regole di assemblaggio e libreria componenti LCSC (verificare al momento dell'ordine).
12. [Blender — manuale](https://docs.blender.org/manual/en/latest/) — scultura e modellazione della chibi.
13. [build123d — documentazione](https://build123d.readthedocs.io/) — CAD parametrico in Python per le parti tecniche.

## Componenti dello schema (M2, consultati il 2026-11-07)

14. [Espressif — ESP32-C3-MINI-1 & MINI-1U datasheet v2.2](https://www.espressif.com/sites/default/files/documentation/esp32-c3-mini-1_datasheet_en.pdf) — tabella pin 3-1, strapping GPIO2/8/9 (tab. 4-1, 4-3), alimentazione 3,0–3,6 V con sorgente ≥ 0,5 A, RC su EN 10 kΩ/1 µF.
15. [Espressif — ESP32-C3 Series datasheet](https://www.espressif.com/sites/default/files/documentation/esp32-c3_datasheet_en.pdf) — funzioni IO_MUX (FSPI) e GPIO.
16. [STMicroelectronics — USBLC6-2 datasheet](https://www.st.com/resource/en/datasheet/usblc6-2.pdf) — pinout SOT23-6 (I/O1 pin 1/6, I/O2 pin 3/4, GND 2, VBUS 5) e layout consigliato.
17. [Advanced Monolithic Systems — AMS1117 datasheet](http://www.advanced-monolithic.com/pdf/ds1117.pdf) — pinout SOT-223 (1 GND, 2 VOUT, 3 VIN), dropout, caratterizzazione con 22 µF al tantalio.
18. [AOS — AO3400A datasheet](https://www.aosmd.com/res/datasheets/AO3400A.pdf) — VGS(th) 0,65–1,45 V.
19. [XKB — TS-1187A tact switch](https://www.lcsc.com/datasheet/C318884.pdf) — contatti A–B e C–D collegati (non più usato dopo `DEC-029` e `DEC-032`).
20. Pagine datasheet LCSC: [Korean Hroparts — TYPE-C-31-M-12](https://www.lcsc.com/datasheet/C165948.pdf), [JUSHUO — AFC01-S16FCA-00](https://www.lcsc.com/datasheet/C262665.pdf) / [AFC01-S18FCA-00](https://www.lcsc.com/datasheet/C262666.pdf), [JST — serie SH (SM04B/SM02B-SRSS-TB)](https://www.lcsc.com/datasheet/C160404.pdf), [BHFUSE — BSMD0805-050-12V](https://www.lcsc.com/datasheet/C2977522.pdf) — disegni meccanici da confrontare con i footprint nel layout.
21. [Adafruit — DS3231 Precision RTC Breakout (guida PDF)](https://cdn-learn.adafruit.com/downloads/pdf/adafruit-ds3231-precision-rtc-breakout.pdf) — versione STEMMA QT (prodotto 5188): Vin 2,3–5,5 V, pull-up 10 kΩ su SDA/SCL, pila CR1220, LED ON disattivabile con ponticello, indirizzo 0x68.
22. [SparkFun — Qwiic Connect System](https://www.sparkfun.com/qwiic) — connettore JST-SH 4 poli: 1 GND, 2 3,3 V, 3 SDA, 4 SCL (compatibile STEMMA QT).
23. [Waveshare — 1.28inch Touch LCD, schema](https://files.waveshare.com/upload/c/c8/1.28inch_Touch_LCD_Schematic.pdf) e [1.28inch LCD Module, schema](https://files.waveshare.com/upload/b/b4/1.28inch_LCD_Module_SchDoc.pdf) — **solo riferimento** per il pinout FPC dei pannelli GC9A01 1,28" con touch (18 poli) e senza (12 poli) e per il pilotaggio della retroilluminazione; non copiati nel repository.
24. [JLCPCB — catalogo parti](https://jlcpcb.com/parts) e [LCSC](https://www.lcsc.com/) — stato Basic/Extended, stock e prezzi letti il 2026-11-07 (variabili).
25. [easyeda2kicad](https://github.com/uPesy/easyeda2kicad.py) — importazione di simboli e footprint LCSC nella libreria di progetto.
26. [XUNPU — TS-1088-AR02016 tact switch 4×3 mm](https://www.lcsc.com/datasheet/C720477.pdf) — 2 pin, contatto tra 1 e 2, piazzole 5,5 × 2,0 mm (`DEC-029`).
27. [Espressif — ESP32-C3 Hardware Design Guidelines](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32c3/pcb-layout-design.html) — sezione layout: "antenna outside the base board", feed point vicino al bordo; posizionamento del modulo con l'antenna oltre il bordo della scheda (`DEC-031`).

Da aggiungere al momento della scelta: datasheet del pannello GC9A01 acquistato.

## Gerarchia delle evidenze

1. **Scheda tecnica del lotto acquistato** / datasheet dei componenti scelti.
2. **Misure strumentali del nostro prototipo** (corrente, temperatura, dimensioni).
3. Documentazione ufficiale del produttore.
4. Codice demo ed esempi terzi (utili per il bring-up, **non** equivalenti a validazione hardware o sicurezza).
5. Render e immagini concettuali (ispirazione estetica, non specifiche dimensionali).

## Regole di citazione nei documenti

- Dati elettronici identificabili devono indicare componente e fonte.
- Dati non verificati si marcano `TBD` / `CAND`; soglie progettuali `TGT`.
- I test reali devono riportare ambiente, strumenti, FW SHA, SKU/revisione e condizioni di alimentazione.
- Non copiare schematici, firmware di terzi o modelli 3D nel repository senza verificarne condizioni di licenza.
