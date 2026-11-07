# 11 — Fonti, datasheet e riferimenti

**Versione:** 0.3 · **Aggiornato:** 2026-11-07

## Scheda Waveshare (scartata, `DEC-015`)

Fonti consultate durante la revisione v0.2, mantenute come riferimento storico e per il piano B.

1. [Waveshare — ESP32-S3-Touch-AMOLED-1.75, overview e specifiche](https://docs.waveshare.com/ESP32-S3-Touch-AMOLED-1.75). Conferma MCU ESP32-S3, AMOLED 466×466, 1,75", CO5300, CST9217, RTC PCF85063, PMU AXP2101, QMI8658, header batteria MX1.25.
2. [Waveshare — pagina prodotto standard/B/G](https://www.waveshare.com/product/esp32-s3-touch-amoled-1.75.htm). Descrizioni, varianti e interfaccia USB-C.
3. [Waveshare — schemi, disegni dimensionali, datasheet periferiche ed esempi](https://docs.waveshare.com/ESP32-S3-Touch-AMOLED-1.75/Resources-And-Documents). **Fonte primaria per definire pinout e ingombri: scaricare revisione corretta prima del CAD o dei cablaggi.**
4. [Waveshare — schematico ESP32-S3-Touch-AMOLED-1.75 (PDF)](https://files.waveshare.com/wiki/ESP32-S3-Touch-AMOLED-1.75/ESP32-S3-Touch-AMOLED-1.75.pdf) — versione consultata il 2026-11-07, creata 2025-07-28: bus I²C GPIO14/15 con pull-up 2,2 kΩ, header H2, TS AXP2101 su termistore di scheda, RTC alimentato da AXP2101. Non copiato nel repository (licenza non verificata).
5. [Waveshare — istruzioni ESP-IDF](https://docs.waveshare.com/ESP32-S3-Touch-AMOLED-1.75/Working-with-ESP-IDF) — guida BSP/esempi; verificare versione SDK usata dagli esempi rispetto alla futura versione pinnata.

## Sensore temperatura e umidità

6. [Sensirion — SHT40 official product page](https://sensirion.com/products/catalog/SHT40) — caratteristiche del sensore; accuratezza tipica dichiarata per RH ±1,8%.
7. [Sensirion — SHT4x datasheet PDF](https://sensirion.com/media/documents/33FD6951/662A593A/HT_DS_Datasheet_SHT4x.pdf) — condizioni delle misure, formato protocollo e timing. **Usare sempre la revisione vigente del datasheet al momento dell'acquisto.**

## Toolchain e progettazione

8. [Espressif — ESP-IDF Programming Guide](https://docs.espressif.com/projects/esp-idf/en/stable/esp32c3/) — infrastruttura firmware, driver, NVS, power management (scegliere la variante del chip definitivo).
9. [Espressif — ESP32-C3](https://www.espressif.com/en/products/socs/esp32-c3) e [ESP32-S3](https://www.espressif.com/en/products/socs/esp32-s3) — datasheet, design guidelines hardware e moduli.
10. [KiCad — documentazione](https://docs.kicad.org/) — progettazione schema e PCB.
11. [JLCPCB](https://jlcpcb.com/) — capacità di produzione, regole di assemblaggio e libreria componenti LCSC (verificare al momento dell'ordine).

Da aggiungere al momento della scelta: datasheet di caricatore, regolatore, RTC, misura batteria, pannello GC9A01 acquistato e cella LiPo.

## Gerarchia delle evidenze

1. **Scheda tecnica del lotto acquistato** / schematico board e datasheet batteria.
2. **Misure strumentali del nostro prototipo** (corrente, autonomia, temperatura, dimensioni).
3. Documentazione ufficiale del produttore.
4. Codice demo ed esempi terzi (utili per il bring-up, **non** equivalenti a validazione hardware o sicurezza).
5. Render e immagini concettuali (ispirazione estetica, non specifiche dimensionali).

## Regole di citazione nei documenti

- Dati elettronici identificabili devono indicare componente e fonte.
- Dati non verificati si marcano `TBD` / `CAND`; soglie progettuali `TGT`.
- I test reali devono riportare ambiente, strumenti, FW SHA, SKU/revisione e condizioni di alimentazione.
- Non copiare schematici, firmware di terzi o modelli 3D nel repository senza verificarne condizioni di licenza.
