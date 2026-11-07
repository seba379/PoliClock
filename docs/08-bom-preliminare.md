# 08 — BOM preliminare e procurement

**Versione:** 0.1 · **Stato:** candidati, nessun acquisto confermato · **Data:** 2026-11-07

## 1. Regole

- Prezzi, disponibilità e tempi di consegna **non sono fissati** in questa BOM; vanno aggiornati con preventivi reali.
- Una scheda dichiarata supportare la ricarica non implica compatibilità automatica con qualunque batteria.
- Nessuna parte è in stato `APPROVATO` finché non sono stati verificati connettori, quote e alimentazione.

## 2. Componenti principali

| ID | Q.tà | Candidato / specifica | Stato | Gate di approvazione |
|---|---:|---|---|---|
| `BOM-001` | 1 | **Waveshare ESP32-S3-Touch-AMOLED-1.75**, SKU standard **31261** | CAND | Pinout, dimensioni, bring-up, consumi, carica |
| `BOM-002` | 1 | **SHT40**, breakout I²C 3,3 V, **senza LED di alimentazione** (o rimovibile) | CAND | 3,3 V, indirizzo, meccanica, errore termico |
| `BOM-003` | 1 | **LiPo 1S protetta**, capacità esplorativa 2.500–3.000 mAh | CAND | Datasheet, limite carica, polarità MX1.25, ingombro, protezioni |
| `BOM-004` | 1 | **USB-C maschio-femmina da pannello**, corta, con dati USB 2.0 (USB-C confermato, `DEC-011`) | CAND | Ingombro, trazione, dati flash, compatibilità con porta scheda |
| `BOM-005` | 1 | Cablaggio e connettore SHT40 con fermacavo e isolamento | TBD | Schema, pinout, lunghezza, interferenza |
| `BOM-006` | 1 set | Gusci/statuetta 3D (PLA prototipo, PETG da valutare) | CAND | CAD e quote reali; prove di stampa |
| `BOM-007` | 1 set | Viti, supporti, inserti, gommini antiscivolo | TBD | Vano manutenzione, resistenza e sicurezza cella |
| `BOM-008` | 1 | Alimentatore USB 5 V di qualità, se non già disponibile | TBD | Corrente e cavo adeguati all'assorbimento verificato |

## 3. Opzioni V1 NON necessarie

- SCD41/altro sensore CO₂: più costoso e non richiesto.
- DS3231 aggiuntivo: il modulo candidato integra già PCF85063.
- TP4056: non aggiungere un secondo caricabatteria in presenza di AXP2101 senza un progetto elettrico diverso e motivato.
- Speaker, microfono, GPS, microSD: fuori perimetro. L'altoparlante 8 Ω incluso con la scheda non va montato.
- PCB custom: rimandato dopo il primo prototipo riuscito.

## 4. Fonti prodotto

- Waveshare: [scheda prodotto ESP32-S3-Touch-AMOLED-1.75](https://www.waveshare.com/product/esp32-s3-touch-amoled-1.75.htm).
- Waveshare: [documentazione hardware, schemi e disegni](https://docs.waveshare.com/ESP32-S3-Touch-AMOLED-1.75/Resources-And-Documents).
- Sensirion: [SHT40 ufficiale](https://sensirion.com/products/catalog/SHT40).

## 5. Check-list preordine

- [ ] Confermare la variante **senza GPS e senza custodia**, SKU 31261.
- [ ] Scaricare schematico e drawing delle dimensioni della revisione corretta.
- [ ] Localizzare pad I²C disponibili per SHT40 e controllare tensione e pull-up (schematico 2025-07-28: GPIO14/15, pull-up 2,2 kΩ già presenti; confermare sulla revisione acquistata).
- [ ] Consultare le caratteristiche di **AXP2101** e lo schema board: ricarica con USB e carico attivo.
- [ ] Scegliere la LiPo **sul datasheet**, controllando connettore e polarità prima di qualsiasi collegamento.
- [ ] Valutare dimensioni dell'insieme modulo+batteria e geometria preliminare testa/corpo.
- [ ] Selezionare prolunga USB-C che conservi dati e abbia staffa di montaggio.
- [ ] Valutare capacità di passare da 3.000 a 2.500 mAh o rivedere la scocca, se necessario.

## 6. Tabella acquisti da completare

| ID BOM | Fornitore | Codice reale | Prezzo | Link acquisto | Ordinato | Ricevuto | Verificato |
|---|---|---|---|---|---|---|---|
| BOM-001 | TBD | SKU 31261 | TBD | link ufficiale sopra | no | no | no |
| BOM-002 | TBD | TBD breakout SHT40 | TBD | TBD | no | no | no |
| BOM-003 | TBD | TBD battery | TBD | TBD | no | no | no |
| BOM-004 | TBD | TBD cable | TBD | TBD | no | no | no |

## 7. Piano B

Se la scheda AMOLED candidata non supera il gate energetico o non entra nella testa senza compromettere il design, valutare display IPS circolare con MCU separata **solo dopo** confronto quantitativo di autonomia, ingombro e complessità. La sola risoluzione più alta non è un motivo sufficiente per scegliere una scheda.
