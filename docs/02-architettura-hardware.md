# 02 — Architettura hardware

**Versione:** 0.5 · **Stato:** architettura PCB custom candidata, non validata · **Data:** 2026-11-07

## 1. Strategia

La V1 usa un **PCB custom progettato in KiCad e prodotto/assemblato da JLCPCB** (`DEC-015`), con il minimo indispensabile per le funzioni richieste. La scheda integrata Waveshare ESP32-S3-Touch-AMOLED-1.75 (ex `CAND-001`) è stata scartata per costo e per i componenti superflui.

L'elettronica è divisa in **schede separate** (`DEC-021`):

1. **Scheda principale** rettangolare, **separata dal display**: MCU, protezioni USB, regolatore 3,3 V, RTC con tampone, USB-C, connettori. **Nessuna batteria** nella V1 (`DEC-023`). Posizione nella statuetta da decidere con la bozza CAD (busto/base o testa, `OPEN-020`).
2. **Schedina portadisplay** rotonda nella testa: solo il connettore del pannello, i condensatori di disaccoppiamento e il connettore del cavo verso la scheda principale.
3. **Mini-PCB SHT40** nel vano ventilato.

Scheda principale e portadisplay sono collegate da un **cavo piatto FFC** (o cavetto JST-SH) che attraversa il collo (`CAND-020`). Tutte le schede si ordinano nello **stesso pannello JLC**.

Il PCB custom **non** è più economico per un solo esemplare (costi fissi di assemblaggio, spedizione, possibile seconda revisione): la scelta è motivata da controllo del progetto, minimo indispensabile e integrazione nella statuetta.

Per ridurre il rischio di una revisione sbagliata, prima del disegno si valida l'architettura **su banco con moduli commerciali economici**, con cavi display della stessa lunghezza prevista (vedi [roadmap](09-roadmap.md), M1).

Non confondere la disponibilità di una funzione nel datasheet con il suo corretto funzionamento nel nostro montaggio.

## 2. Schema a blocchi

```mermaid
flowchart LR
    subgraph HEAD["Testa"]
        DISP["Display IPS rotondo 1,28''<br/>GC9A01 (+ touch predisposto)"]
        CARR["Schedina portadisplay"]
        DISP --- CARR
    end
    subgraph MAIN["Scheda principale (posizione: OPEN-020)"]
        CONN["USB-C"]
        ESD["ESD + fusibile/PTC"]
        REG["Regolatore 3,3 V (LDO)"]
        MCU["Modulo ESP32"]
        RTC["RTC + tampone"]
        CONN --> ESD -->|"5 V"| REG --> MCU
        REG --> RTC
        ESD -->|"D+/D-"| MCU
        MCU <-->|"I2C"| RTC
    end
    USB["Cavo USB-C sempre collegato<br/>(sul sedere)"] -.->|"connettore diretto (A) o prolunga (B)"| CONN
    CARR <-->|"cavo FFC nel collo"| MCU
    SHT["SHT40 su mini-PCB<br/>vano ventilato"] <-->|"I2C, 4 fili"| MCU
    BTN["Pulsante"] --> MCU
```

Il diagramma descrive funzioni logiche: non sostituisce lo schema elettrico KiCad.

## 3. Blocchi funzionali e candidati

Tutti i codici sono **CAND**: da verificare su datasheet, disponibilità e prezzo LCSC/JLCPCB (preferire parti "basic" per ridurre i costi fissi di assemblaggio).

| Blocco | Funzione | Requisiti | Candidati (CAND) |
|---|---|---|---|
| MCU | Logica, UI | Supporto ESP-IDF, USB nativa per flash/log/configuratore, SPI + I²C + PWM, GPIO per pulsante e touch | Modulo **ESP32-C3-MINI-1** (consigliato) o ESP32-S3-MINI-1; modulo certificato con antenna/flash integrate |
| Display | Volto | Rotondo, IPS, **1,28"**, **240×240**, driver **GC9A01**, SPI 4 fili (`DEC-016`) | Pannello nudo con FPC, disponibile con e senza touch (`DEC-019`) |
| Portadisplay | Interfaccia pannello ↔ cavo | Connettore FPC del pannello, condensatori vicino al pannello, connettore del cavo; sagoma e fori per il fissaggio nella testa | Schedina rotonda a 2 strati, nessun componente attivo |
| Collegamento display | Testa ↔ scheda principale | Circa **12 conduttori**: 3,3 V, GND (più di uno, alternati ai segnali), SCLK, MOSI, CS, DC, RST, BL; touch: SDA, SCL, INT, RST. Lunghezza indicativa 5–15 cm | **FFC** passo 0,5 mm con connettori ZIF (consigliato) o cavetto JST-SH; SPI a **10–20 MHz** da validare in M1 (`CAND-020`) |
| Retroilluminazione | DIM/BRIGHT/NIGHT | PWM, spegnibile del tutto di notte | MOSFET/transistor + resistenza; valori dal datasheet del pannello |
| Interazione | Accendere/impostare | **Pulsante** fisico (`DEC-017`), posizione da definire | Pulsante su scheda o remoto via cavo; pull-up e antirimbalzo; GPIO con risveglio |
| Touch (predisposto) | Opzione futura (`DEC-019`) | Controller del pannello su I²C + **INT** (GPIO con risveglio) + **RST** portati nel cavo; componenti non montati se non serve | Controller tipico dei pannelli 1,28" (es. famiglia CST816), da confermare sul datasheet |
| USB | **Alimentazione**, flash, configuratore (`DEC-020`, `DEC-023`) | USB-C 2.0, CC 5,1 kΩ, ESD, fusibile/PTC; D+/D- alla USB nativa dell'MCU secondo le design guideline Espressif | Ricettacolo USB-C sulla scheda principale; ESD tipo USBLC6-2 |
| Regolatore 3,3 V | Alimentare MCU, display, sensori da 5 V USB | Corrente massima con margine sui picchi MCU; dissipazione accettabile; bassa rumorosità | LDO 5 V → 3,3 V (`CAND-015`) |
| RTC | Ora anche a cavo scollegato | Bassissimo consumo, tampone (supercondensatore o pila) dimensionato per alcuni giorni, I²C | RV-3028-C7 o PCF85063A + tampone (`CAND-014`) |
| Sensore T/RH | Misure ambiente | **SHT40** su mini-PCB senza LED, 4 fili | Mini-PCB nello stesso pannello JLC |
| Connettori | SHT40, pulsante | Polarizzati, con ritenuta, polarità serigrafata | JST-PH 2,0 o JST-SH 1,0 |
| Debug | Bring-up | Punti di test VBUS, 3,3 V, tampone RTC, GND; BOOT/RESET | — |

**Budget dei pin (ESP32-C3):** SPI display 5, retroilluminazione 1, I²C 2, touch INT/RST 2, pulsante 1, USB 2: circa 13 GPIO, compatibili con i GPIO liberi del modulo (da verificare sul datasheet, inclusi i pin di boot). Senza batteria non servono più ADC, abilitazione partitore e stato caricatore.

![Schema a blocchi di PoliClock](../assets/concept/policlock-schema-blocchi.svg)

## 4. Collegamento display su cavo

- Il SPI del GC9A01 su un cavo di qualche centimetro è affidabile se: frequenza moderata (10–20 MHz iniziali), **masse alternate** ai segnali veloci (soprattutto SCLK), eventuali resistenze serie di smorzamento vicino all'MCU, condensatori di disaccoppiamento **sul portadisplay**.
- A 20 MHz un'immagine completa 240×240 a 16 bit (circa 115 kB) richiede circa 50 ms: più che sufficiente per un orologio che aggiorna il minuto.
- La retroilluminazione è la corrente maggiore che passa nel cavo: dimensionare i conduttori di alimentazione (più pin in parallelo se necessario).
- Il cavo deve piegarsi nel collo senza tensione sui connettori; fissarlo con fermacavo.

## 5. Sensore temperatura/umidità

**Sensirion SHT40** è la scelta candidata. Specifica tipica: ±1,8 %RH; la temperatura ha accuratezza tipica dichiarata dal costruttore in condizioni specificate dal datasheet. Vedere [pagina prodotto](https://sensirion.com/products/catalog/SHT40).

- Montato su un **mini-PCB** prodotto insieme alle altre schede: niente LED, niente regolatore, pull-up I²C sulla scheda principale.
- Posizionamento **separato fisicamente** dalle sorgenti di calore (scheda principale, regolatore, retroilluminazione), con feritoie verso l'aria ambiente.
- Cavo a 4 fili con connettore polarizzato e fermacavo.
- Indirizzo tipico `0x44`: verificare assenza di conflitti con RTC, touch e fuel gauge.
- Campionamento iniziale consigliato **30–60 s** (parametro firmware).

## 6. Scelte intenzionalmente escluse

Non servono per V1: audio, microSD, IMU, GPS, touch montato (solo predisposto, `DEC-019`), sensore CO₂, sensore luce, Wi-Fi/BLE (`DEC-012`), convertitore USB-seriale esterno, batteria e circuiti di carica (`DEC-023`).

## 7. Interfacce e verifiche prima dell'ordine PCB

| Interfaccia | Uso previsto | Verifica obbligatoria |
|---|---|---|
| USB-C | Alimentazione continua, flash, configuratore | Opzione A: connettore sul bordo della scheda allineato al foro sul sedere. Opzione B: enumerazione attraverso la prolunga provata su banco |
| Display su cavo | GC9A01 via SPI | Pinout FPC dal datasheet del pannello **acquistato**; prova su banco con cavo di lunghezza reale e frequenza scelta |
| I²C | RTC, SHT40, touch, eventuale fuel gauge | Indirizzi, pull-up unici, lunghezze cavo |
| Pulsante | Illuminazione UI e menu | Antirimbalzo e pressione breve/lunga provati sulla dev board |
| Touch (predisposto) | Opzione futura | Pinout touch del pannello; GPIO INT/RST con risveglio (`OPEN-019`) |
| USB dati / configuratore | Impostazioni da PC | Porta seriale e comandi funzionanti in tutti i modi (DIM/BRIGHT/NIGHT) |
| RTC | Unica fonte di tempo in V1 | Mantenimento a cavo scollegato grazie al tampone; durata misurata |

## 8. Alternative e rischi

- **Prima revisione PCB con errori**: probabile. Mitigazione: prototipo M1, revisione schema con checklist, punti di test, 0 Ω/jumper per isolare i blocchi, revisione visiva del proprietario in KiCad.
- **Disturbi sul cavo display**: frequenza SPI ridotta, masse alternate, prova su banco con cavo reale.
- **Pannello senza datasheet affidabile**: acquistare solo pannelli con pinout FPC documentato.
- **Componenti non disponibili a JLC**: verificare LCSC prima del layout; alternative compatibili a pin.
- **Spazio nel busto insufficiente** per la scheda: decidere la posizione con la bozza Blender (`OPEN-020`).
- **Piano B**: schede commerciali con ESP32 e display rotondo 1,28" integrato.

## 9. Gate di conferma hardware

Il PCB diventa `APPROVATO` solo dopo: revisione schema e layout (ERC/DRC puliti, checklist, revisione visiva del proprietario in KiCad), bring-up delle alimentazioni con limitazione di corrente, flash e configuratore via USB-C posteriore, display stabile sul cavo reale, pulsante, lettura SHT40 e RTC, protezioni dell'ingresso USB verificate, durata del tampone RTC, misura dell'assorbimento in DIM, BRIGHT, NIGHT e temperature in funzionamento continuo.
