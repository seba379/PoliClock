# 11 — Fonti, datasheet e riferimenti

**Versione:** 0.1 · **Aggiornato:** 2026-11-07

## Documentazione ufficiale della scheda candidata

1. [Waveshare — ESP32-S3-Touch-AMOLED-1.75, overview e specifiche](https://docs.waveshare.com/ESP32-S3-Touch-AMOLED-1.75). Conferma MCU ESP32-S3, AMOLED 466×466, 1,75", CO5300, CST9217, RTC PCF85063, PMU AXP2101, QMI8658, header batteria MX1.25.
2. [Waveshare — pagina prodotto standard/B/G](https://www.waveshare.com/product/esp32-s3-touch-amoled-1.75.htm). Descrizioni, varianti e interfaccia USB-C.
3. [Waveshare — schemi, disegni dimensionali, datasheet periferiche ed esempi](https://docs.waveshare.com/ESP32-S3-Touch-AMOLED-1.75/Resources-And-Documents). **Fonte primaria per definire pinout e ingombri: scaricare revisione corretta prima del CAD o dei cablaggi.**
4. [Waveshare — istruzioni ESP-IDF](https://docs.waveshare.com/ESP32-S3-Touch-AMOLED-1.75/Working-with-ESP-IDF) — guida BSP/esempi; verificare versione SDK usata dagli esempi rispetto alla futura versione pinnata.

## Sensore temperatura e umidità

5. [Sensirion — SHT40 official product page](https://sensirion.com/products/catalog/SHT40) — caratteristiche del sensore; accuratezza tipica dichiarata per RH ±1,8%.
6. [Sensirion — SHT4x datasheet PDF](https://sensirion.com/media/documents/33FD6951/662A593A/HT_DS_Datasheet_SHT4x.pdf) — condizioni delle misure, formato protocollo e timing. **Usare sempre la revisione vigente del datasheet al momento dell'acquisto.**

## Toolchain e progettazione

7. [Espressif — ESP-IDF Programming Guide](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/) — infrastruttura firmware, driver, NVS, networking e power management.
8. [Espressif — ESP32-S3 hardware](https://www.espressif.com/en/products/socs/esp32-s3) — MCU e reference manual (la scheda Waveshare resta riferimento per pinout effettivo).

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
