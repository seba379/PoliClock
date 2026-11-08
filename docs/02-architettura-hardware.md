# 02 — Architettura hardware

**Versione:** 0.7 · **Stato:** schema e PCB rev 0.2 della scheda principale in bozza (dopo la revisione tecnica indipendente), non validati · **Data:** 2026-11-08

## 1. Strategia

La V1 usa un **PCB custom progettato in KiCad e prodotto/assemblato da JLCPCB** (`DEC-015`), con il minimo indispensabile per le funzioni richieste, nel rispetto delle **regole di fabbricazione e assemblaggio JLCPCB** (vincolo `SC-008`, `DEC-040`, `PR-REL-008`).

Dalla rev 0.2 c'è **un solo PCB custom**, la scheda principale. Tutto il resto sono **moduli commerciali** collegati con cavetti:

1. **Scheda principale** 50 × 40 mm (`DEC-036`): MCU, protezioni USB, regolatore 3,3 V, USB-C, connettori. **Nessuna batteria** (`DEC-023`, riconfermata in `DEC-038`). Posizione nella statuetta da decidere con la bozza CAD (`OPEN-020`, studio volumetrico `OPEN-028`).
2. **Modulo display GC9A01 1,28" a 7 pin** (`DEC-034`): IPS a colori 240×240 su schedina con piedini 2,54 mm, provabile su breadboard; senza touch. Sostituisce pannello nudo, schedina portadisplay e cavo FFC della rev 0.1.
3. **Modulo breakout SHT40** nel vano ventilato (`DEC-028`).
4. **Modulo RTC Adafruit DS3231 STEMMA QT** con pila CR1220 (`DEC-024`).

Il PCB custom **non** è più economico per un solo esemplare (costi fissi di assemblaggio, spedizione, possibile seconda revisione): la scelta è motivata da controllo del progetto, minimo indispensabile e integrazione nella statuetta. Stima dei costi in [08](08-bom-preliminare.md) §8.

Prima dell'ordine si valida l'architettura **su banco con i moduli commerciali** (vedi [roadmap](09-roadmap.md), M1). Non confondere la disponibilità di una funzione nel datasheet con il suo corretto funzionamento nel nostro montaggio.

## 2. Schema a blocchi

```mermaid
flowchart LR
    subgraph HEAD["Testa"]
        DISP["Modulo display GC9A01 1,28''<br/>7 pin, senza touch"]
    end
    subgraph MAIN["Scheda principale 50 × 40 mm (posizione: OPEN-020)"]
        CONN["USB-C"]
        ESD["ESD + PTC"]
        REG["LDO TLV75533"]
        MCU["ESP32-C3-MINI-1-H4X"]
        SW["Q1: alimentazione display"]
        CONN --> ESD -->|"5 V"| REG --> MCU
        ESD -->|"D+/D-"| MCU
        REG --> SW
    end
    RTC["Modulo RTC DS3231<br/>+ pila CR1220"] <-->|"I2C, JST-SH 4 poli"| MCU
    USB["Cavo USB-C sempre collegato<br/>(sul sedere)"] -.->|"connettore diretto (A) o prolunga (B)"| CONN
    MCU -->|"SPI, cavetto 7 fili nel collo"| DISP
    SW -->|"3,3 V commutati"| DISP
    SHT["Modulo SHT40<br/>vano ventilato"] <-->|"I2C, JST-SH 4 poli"| MCU
    BTN["Pulsante remoto"] -->|"JST-SH 2 poli"| MCU
```

Il diagramma descrive funzioni logiche: non sostituisce lo schema elettrico KiCad.

## 3. Blocchi funzionali

Componenti e codici LCSC in [12 — Selezione componenti](12-selezione-componenti.md); tutti `CAND` fino al prototipo M1.

| Blocco | Funzione | Requisiti | Soluzione (rev 0.2) |
|---|---|---|---|
| MCU | Logica, UI | ESP-IDF, USB nativa per flash/log/configuratore, SPI + I²C | **ESP32-C3-MINI-1-H4X** (`DEC-035`), variante "Recommended", chip v1.1 |
| Display | Volto | Rotondo, IPS, **1,28"**, 240×240, GC9A01, SPI 4 fili (`DEC-016`) | **Modulo a 7 pin** (VCC, GND, SCL, SDA, DC, CS, RST), senza touch e senza pin per la retroilluminazione (`DEC-034`) |
| Collegamento display | Testa ↔ scheda principale | 7 conduttori, lunghezza dal CAD | Header maschio 1×7 2,54 mm SMD a 90° (J2) + cavetto Dupont femmina-femmina dritto; R8/R9 22 Ω in serie su SCLK/MOSI; SPI 10–20 MHz da provare (`OPEN-021`) |
| Display: notte e luminosità | DIM/BRIGHT/NIGHT | Display spento di notte (`DEC-009`) | P-MOS **AO3401A** (Q1) sull'alimentazione del modulo, comandato da IO20; DIM/BRIGHT solo con i colori della grafica (retroilluminazione fissa, `DEC-034`) |
| Interazione | Accendere/impostare | **Pulsante** fisico (`DEC-017`) | Pulsante remoto su JST-SH 2 poli (`DEC-032`); pull-up 10 kΩ e 100 nF; IO3 con risveglio |
| USB | **Alimentazione**, flash, configuratore (`DEC-020`, `DEC-023`) | USB-C 2.0, CC 5,1 kΩ, ESD, PTC | TYPE-C-31-M-12 (footprint KiCad dal disegno HRO), USBLC6-2SC6 vicino al connettore, PTC 0,5 A |
| Regolatore 3,3 V | Alimentare MCU, display e moduli | ≥ 0,5 A (richiesta Espressif), stabile con condensatori ceramici | **TLV75533** 500 mA (`DEC-037`), condensatori a 2,2–2,4 mm dai pin |
| Reset e boot | Flash e recupero | EN con RC, strapping IO9 | Nessun tasto (`DEC-039`): RC 10 kΩ/1 µF su EN, pull-up 10 kΩ su IO9, punti di test TP6 (EN) e TP11 (IO9) vicino ai pin |
| RTC | Ora anche a cavo scollegato | Tampone e precisione senza NTP | Modulo esterno DS3231 su J4 (`DEC-024`) |
| Sensore T/RH | Misure ambiente | SHT40 lontano dal calore | Modulo breakout su J3 (`DEC-028`) |
| Connettori | SHT40, RTC, pulsante | Polarizzati, con ritenuta | JST-SH 1,0 mm, 4 poli con pinout Qwiic/STEMMA QT, 2 poli per il pulsante |
| Debug | Bring-up | Punti di test, isolamento dei blocchi | 11 punti di test sul retro con etichetta; resistenze 0 Ω per isolare il regolatore e i moduli esterni |

**Budget dei pin (ESP32-C3):** SPI display 4 + RST 1, alimentazione display 1, I²C 2, pulsante 1, USB 2, BOOT 1: 12 GPIO; IO0 e IO1 liberi su punti di test, IO21 (TXD0) su punto di test. Verificato sul datasheet ESP32-C3-MINI-1 v2.2, strapping inclusi.

### 3.1 Assegnazione dei pin (schema rev 0.2)

| GPIO | Pin modulo | Segnale | Note |
|---|---:|---|---|
| IO0 / IO1 | 12 / 13 | liberi | TP9/TP10 |
| IO2 | 5 | I2C_SDA | Strapping: pull-up 4,7 kΩ raccomandato da Espressif (prova di boot `VT-PCB-004`) |
| IO3 | 6 | BTN_USER | Attivo basso, pull-up 10 kΩ, risveglio da deep-sleep |
| IO4 | 18 | LCD_DC | |
| IO5 | 19 | LCD_RST | Pull-up 10 kΩ verso 3V3_DISP |
| IO6 | 20 | LCD_SCLK | IO_MUX FSPICLK, 22 Ω in serie |
| IO7 | 21 | LCD_MOSI | IO_MUX FSPID, 22 Ω in serie |
| IO8 | 22 | I2C_SCL | Strapping: = 1 per il download, pull-up 4,7 kΩ |
| IO9 | 23 | BOOT | Strapping: pull-up 10 kΩ; TP11 per forzare il download |
| IO10 | 16 | LCD_CS | IO_MUX FSPICS0 |
| IO18 / IO19 | 26 / 27 | USB D- / D+ | USB Serial/JTAG nativa |
| IO20 (RXD0) | 30 | DISP_EN_N | Basso = display alimentato; R17 tiene il display spento al boot |
| IO21 (TXD0) | 31 | UART_TX | Punto di test TP5 |

Bus I²C condiviso: SHT40 `0x44`, DS3231 `0x68`.

![Schema a blocchi di PoliClock](../assets/concept/policlock-schema-blocchi.svg)

*(Lo schema a blocchi illustrativo in `assets/` precede la rev 0.2: il display è ora un modulo a 7 pin senza schedina portadisplay.)*

### 3.2 PCB della scheda principale rev 0.2 (2026-11-08)

File: `hardware/policlock-main/policlock-main.kicad_pcb` (render, PDF, BOM, CPL e STEP nella stessa cartella). **Bozza completa**: posizionamento e sbroglio automatico con Freerouting, da rivedere a vista prima dell'ordine (`OPEN-027`).

| Parametro | Valore | Motivazione |
|---|---|---|
| Dimensioni scheda | **50 × 40 mm**, con **intaglio** di circa 7,8 × 20,2 mm nell'angolo in alto a destra | `DEC-036` ("per il primo prototipo è meglio stare larghi e confermare 50x40"). Lo sbroglio completo con le regole JLC è riuscito a 50 × 40, senza bisogno di ingrandire |
| Ingombro totale | **50 × 40 mm**; oltre il contorno sporgono solo i **piedini dell'header display (~5,6 mm sopra il bordo superiore)** e il guscio USB-C (0,4 mm sotto) | L'antenna sta dentro l'ingombro, sopra l'intaglio, con la punta a 2,5 mm dal bordo destro |
| Strati / spessore | 2 strati, 1,6 mm (`DEC-030`) | Circuito semplice, nessuna radio attiva; piani GND su entrambi i lati |
| Montaggio | Solo lato superiore, servizio JLC "Economic" | Sul retro solo pad di test nudi e legenda |
| Regole di fabbricazione (JLC, `DEC-040`) | Distanza 0,15 mm (0,10 mm fra le piazzole USB-C a passo 0,5 mm), piste 0,2 mm (alimentazioni 0,4 mm), vie 0,6/0,3 mm (0,7/0,35 mm sulle alimentazioni), foro-foro ≥ 0,25 mm, foro-rame ≥ 0,3 mm, rame-bordo ≥ 0,3 mm più una fascia di 0,45 mm vietata a piste e vie lungo il contorno | Minimi JLC 2 strati con margine (pagina capacità JLCPCB, consultata il 2026-11-08) |
| Regole di assemblaggio (JLC, `DEC-040`) | Corpo dei componenti **≥ 2,5 mm dai lati sinistro e destro**; connettori a filo solo sui lati superiore (header) e inferiore (USB-C); 3 fiducial da 1 mm con zona di rispetto | Termini di assemblaggio JLCPCB; i lati sinistro e destro sono quelli di trasporto e degli eventuali bordi tecnici |
| Spaziatura | 0,5 mm in più fra i courtyard dei componenti piazzati automaticamente | Spazio per piste e vie |

Disposizione (vista dall'alto, origine nell'angolo in alto a sinistra):

- **In alto a destra**: modulo ESP32-C3-MINI-1-H4X ruotato di 270°, centro a (36,5; 12,6) mm, con 6 mm liberi sopra per EN, 3V3 e le uscite dei segnali. L'antenna sta **sopra l'intaglio** (nessun PCB né rame sotto, linee guida Espressif) e una zona senza rame di 3 mm prosegue sotto l'intaglio.
- **Bordo superiore**: header J2 del display (centro x = 17,5 mm), pin 1 = VCC a destra, piedini verso l'esterno; Q1 con R16/R17/C9/C10 accanto al pin 1.
- **Bordo inferiore** (verso il sedere, opzione A): USB-C J1 (centro x = 32,0 mm), affiancata da **due fori M2** (Ø 2,2 mm, pad a GND) a (22,5; 36,5) e (42,0; 36,5) mm, che scaricano sulla scocca lo sforzo d'inserimento del cavo. ESD U1 tra connettore e modulo, R3/R4 allineate ai pin USB del modulo.
- **In basso a sinistra**: PTC, LDO U2 con C2 (ingresso) e C3/C4 (uscita) a 2,2–2,4 mm dai pin.
- **Lato sinistro**: JST-SH J3 (SHT40), J4 (RTC), J5 (pulsante), rientrati in modo che il corpo stia a 2,5 mm dal bordo.
- **Retro**: 11 punti di test con etichetta "riferimento + rete"; TP6 (EN) e TP11 (IO9) sotto i rispettivi pin del modulo, gli altri in due file.

**Verifiche (report salvati, nessun test hardware):** DRC con `kicad-cli` e tutte le severità, con i controlli su courtyard, fori, serigrafia e footprint riabilitati: **0 violazioni, 0 connessioni aperte**. Disaccoppiamento: C6 0,1 µF a 2,4 mm dal pin 3V3 del modulo. EN: 10 mm con 1 via (era 60 mm prima di spostare TP6). USB: D+ circa 17,7 mm senza vie, D- circa 18,0 mm con 2 vie (inevitabili per unire i contatti A7/B7 del connettore), USBLC6 a 2,6–3,8 mm dai contatti: adeguato alla USB full-speed. Nessuna pista sotto 0,15 mm (lo script riallarga a 0,15 mm le strozzature che Freerouting crea vicino alle piazzole fini, se la distanza lo consente); 51 vie, circa 950 mm di piste. Restano da rivedere a vista: percorsi, continuità dei piani GND sotto modulo e USB, eventuali vie di cucitura GND aggiuntive.

**Come si rigenera:** `hardware/scripts/genera_pcb_main.py` (posizionamento; posizioni in `posizioni_main.py`), poi `hardware/scripts/sbroglia_main.py` (Freerouting 2.5.0, vedi [hardware](../hardware/README.md)). KiCad non ha un autorouter.

## 4. Collegamento display su cavetto

- Il SPI del GC9A01 su un cavetto di qualche centimetro funziona se: frequenza moderata (10–20 MHz iniziali), cavetto corto e fissato, resistenze serie di smorzamento vicino all'MCU (R8/R9).
- Il cavetto Dupont a 7 fili non ha masse alternate ai segnali (il modulo ha un solo GND): tenerlo corto e provarlo con la lunghezza reale (`OPEN-021`, `VT-PCB-003`).
- A 20 MHz un'immagine completa 240×240 a 16 bit (circa 115 kB) richiede circa 50 ms: più che sufficiente per un orologio che aggiorna il minuto.
- Con il modulo spento (Q1 aperto) il firmware porta SCLK, MOSI, DC, CS e RST a livello basso.
- Il cavetto deve piegarsi nel collo senza tensione sui connettori; fissarlo con fermacavo.

## 5. Sensore temperatura/umidità

**Sensirion SHT40** su **modulo breakout commerciale** (`DEC-028`), alimentato a **3,3 V** dal connettore J3. Specifica tipica: ±1,8 %RH ([pagina prodotto](https://sensirion.com/products/catalog/SHT40)).

- Verificare sul modulo ricevuto LED, regolatore e corrente (revisione P1-09, `BOM-002`); i pull-up del modulo restano in parallelo a quelli da 4,7 kΩ della scheda.
- Collegamento: cavo JST-SH 4 poli → jumper femmina 2,54 mm; ordine dei pin dalla **serigrafia del modulo acquistato** (`OPEN-002`).
- Posizionamento **separato fisicamente** dalle sorgenti di calore (scheda principale, regolatore, modulo display), con feritoie verso l'aria ambiente.
- Indirizzo `0x44`: nessun conflitto con il DS3231 (`0x68`).
- Campionamento iniziale consigliato **30–60 s** (parametro firmware).

## 6. Scelte intenzionalmente escluse

Non servono per V1: audio, microSD, IMU, GPS, touch (`DEC-034`), sensore CO₂, sensore luce, Wi-Fi/BLE (`DEC-012`), convertitore USB-seriale esterno, batteria e circuiti di carica (`DEC-023`), tasti RESET/BOOT (`DEC-039`).

## 7. Interfacce e verifiche prima dell'ordine PCB

| Interfaccia | Uso previsto | Verifica obbligatoria |
|---|---|---|
| USB-C | Alimentazione continua, flash, configuratore | Opzione A: connettore sul bordo inferiore allineato al foro sul sedere; studio volumetrico (`OPEN-028`) |
| Display su cavetto | GC9A01 via SPI | Pinout del modulo ricevuto (`OPEN-016`, `VT-PCB-005`); prova su banco con cavetto di lunghezza reale (`VT-PCB-003`) |
| I²C | RTC e SHT40 su moduli esterni | Indirizzi; pull-up; avvio con tutti i moduli collegati (`VT-PCB-004`) |
| Pulsante | Illuminazione UI e menu | Antirimbalzo e pressione breve/lunga provati sulla dev board |
| USB dati / configuratore | Impostazioni da PC | Porta seriale e comandi funzionanti in tutti i modi (DIM/BRIGHT/NIGHT) |
| RTC | Unica fonte di tempo in V1 | Modulo DS3231 su J4; mantenimento a cavo scollegato con la pila CR1220; deriva misurata |
| Produzione JLC | Fabbricazione e assemblaggio | DRC con regole JLC pulito, revisione DFM di JLC all'ordine, controllo delle rotazioni nell'anteprima di assemblaggio JLC (`VT-PCB-001`) |

## 8. Alternative e rischi

- **Prima revisione PCB con errori**: probabile. Mitigazione: prototipo M1, revisione schema con checklist, punti di test, 0 Ω per isolare i blocchi, revisione visiva del proprietario in KiCad.
- **Disturbi sul cavetto display**: frequenza SPI ridotta, cavetto corto, prova su banco.
- **Modulo display senza datasheet**: pinout e corrente da verificare sul modulo ricevuto.
- **Componenti non disponibili a JLC**: verificare LCSC prima dell'ordine; alternative compatibili a pin (già successo con l'RV-3028-C7 e con l'ESP32-C3-MINI-1-N4X).
- **Connettori sui bordi superiore e inferiore**: a meno di 2,5 mm dal bordo per necessità; da confermare con la revisione DFM di JLC (`DEC-040`).
- **Spazio nel busto insufficiente** per la scheda 50 × 40: decidere la posizione con la bozza Blender (`OPEN-020`, `OPEN-028`).
- **Piano B**: schede commerciali con ESP32 e display rotondo 1,28" integrato.

## 9. Gate di conferma hardware

Il PCB diventa `APPROVATO` solo dopo: revisione schema e layout (ERC/DRC puliti con le regole JLC, checklist, revisione visiva del proprietario in KiCad), studio volumetrico 1:1, verifica del modulo display, bring-up delle alimentazioni con limitazione di corrente, flash e configuratore via USB-C posteriore, display stabile sul cavetto reale, pulsante, lettura SHT40 e RTC, protezioni dell'ingresso USB verificate, durata del tampone RTC, misura dell'assorbimento in DIM, BRIGHT, NIGHT e temperature in funzionamento continuo.
