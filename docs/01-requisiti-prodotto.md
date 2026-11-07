# 01 — Requisiti di prodotto (PRD)

**Versione:** 0.6 · **Stato:** baseline per prototipo, da approvare · **Data:** 2026-11-07

## 1. Convenzioni

- **MUST** = necessario per considerare V1 accettabile; **SHOULD** = desiderabile; **TGT** = obiettivo da validare sperimentalmente.
- Stato **CONF** = scelta dell'utente; **CAND** = proposta tecnica; **TBD** = dettaglio non stabilito; **ESCLUSO** = non applicabile alla V1 (ID mantenuto per tracciabilità).
- Le soglie non confermate sono indicate come **valori iniziali per prove**, non come prestazioni garantite.
- La tracciabilità requisito → test è registrata nel [piano di verifica](07-piano-verifica.md).

## 2. Requisiti funzionali

| ID | Priorità | Stato | Requisito / criterio verificabile |
|---|---|---|---|
| `PR-FUN-001` | MUST | CONF | Visualizzare `HH:MM` in formato 24 ore sulla schermata principale senza intervento dell'utente. |
| `PR-FUN-002` | MUST | CONF | Visualizzare data e giorno della settimana in italiano. |
| `PR-FUN-003` | MUST | CONF | Visualizzare la temperatura misurata dal sensore locale, in °C. |
| `PR-FUN-004` | MUST | CONF | Visualizzare l'umidità relativa misurata localmente, in %RH. |
| `PR-FUN-005` | — | ESCLUSO | ~~Funzionamento senza cavo USB~~: la V1 è alimentata solo da USB (`DEC-023`). |
| `PR-FUN-006` | MUST | CONF | Alimentare il dispositivo in continuo tramite la porta USB-C posteriore (`DEC-023`). |
| `PR-FUN-007` | MUST | CONF | In condizione normale mantenere l'orologio attenuato ma leggibile; dopo la pressione del pulsante aumentare la luminosità e poi ripristinarla. |
| `PR-FUN-008` | MUST | CONF | Consentire l'impostazione iniziale/correzione di ora e data senza connessione di rete: **configuratore da PC via USB** come metodo principale, menu con il pulsante come riserva (`DEC-020`). |
| `PR-FUN-009` | MUST | CAND | Conservare l'ora tramite RTC con alimentazione tampone anche quando il cavo USB è scollegato, per una durata dimensionata (`OPEN-014`). |
| `PR-FUN-010` | — | ESCLUSO | ~~Sincronizzazione NTP via Wi-Fi~~: esclusa dalla V1 (`DEC-012`). |
| `PR-FUN-011` | — | ESCLUSO | ~~Avviso di batteria bassa~~: nessuna batteria in V1 (`DEC-023`). |
| `PR-FUN-012` | MUST | CAND | In caso di errore sensore, indicare dato non disponibile senza mostrare valori vecchi come attuali. |
| `PR-FUN-013` | MUST | CONF | Modalità notte: in una fascia oraria configurabile il display è spento. Default 23:00–07:00 (`DEC-013`); comportamento al pulsante in `CAND-009`. |

## 3. Interfaccia e presentazione

| ID | Priorità | Stato | Requisito / criterio |
|---|---|---|---|
| `PR-UI-001` | MUST | CONF | La superficie attiva del display è circolare e occupa il volto: IPS rotondo 1,28", 240×240 (`DEC-016`). |
| `PR-UI-002` | MUST | CONF | L'aspetto complessivo è una poliziotta chibi riconoscibile con uniforme blu e cappello. |
| `PR-UI-003` | MUST | CAND | Tutti i dati essenziali sono leggibili da distanza di scrivania tipica (prova 50–80 cm in luce interna). |
| `PR-UI-004` | SHOULD | CAND | Prediligere fondo scuro, tipografia chiara e contrasto elevato. |
| `PR-UI-005` | — | ESCLUSO | ~~Mitigazione burn-in AMOLED~~: non necessaria con display IPS (`DEC-016`). |
| `PR-UI-006` | MUST | CAND | La visualizzazione deve rimanere coerente durante perdita temporanea del sensore e dopo riavvii per scollegamento del cavo. |
| `PR-UI-007` | MUST | CONF | Un **pulsante** fisico attiva la modalità luminosa e, di notte, mostra brevemente l'ora (`DEC-017`); posizione da definire (`OPEN-017`). |
| `PR-UI-008` | MUST | CONF | Il PCB è **predisposto per il touch** del display (connettore/footprint, GPIO INT e RST, componenti non montati) e il firmware gestisce l'input come eventi astratti, così il touch si attiva senza rifare il PCB (`DEC-019`). |

## 4. Alimentazione e sicurezza elettrica

| ID | Priorità | Stato | Requisito / criterio |
|---|---|---|---|
| `PR-PWR-001` | MUST | CONF | Alimentazione **solo da USB 5 V**, nessuna batteria nella V1 (`DEC-023`). |
| `PR-PWR-002` | MUST | CONF | Presa USB-C nella parte posteriore bassa della statuetta (sul sedere), utilizzabile senza disassemblare (`DEC-011`, `DEC-018`); connettore sulla scheda principale o prolunga secondo `DEC-021`. |
| `PR-PWR-003` | — | ESCLUSO | ~~Caricatore della cella~~: nessuna batteria in V1 (`DEC-023`). |
| `PR-PWR-004` | MUST | CAND | Ingresso USB protetto: fusibile/PTC, protezione ESD, resistenze CC 5,1 kΩ; cablaggi isolati e protetti da schiacciamento/strappo. |
| `PR-PWR-005` | MUST | CAND | Funzionamento **continuo 24/7** con temperature interne verificate a scocca chiusa (regolatore, MCU, retroilluminazione, materiale). |
| `PR-PWR-006` | — | ESCLUSO | ~~Autonomia ≥ 48 ore~~: nessuna batteria in V1 (`DEC-023`). |
| `PR-PWR-007` | — | ESCLUSO | ~~Stato di carica della batteria~~: nessuna batteria in V1 (`DEC-023`). |
| `PR-PWR-008` | MUST | CAND | Scollegamento e ricollegamento del cavo in qualunque momento senza corruzione della configurazione e con riavvio pulito (gestione brown-out). |
| `PR-PWR-009` | SHOULD | CAND | Assorbimento massimo compatibile con alimentatori USB comuni (obiettivo ≤ 500 mA, misurato) e consumo medio basso per limitare il riscaldamento interno. |

## 5. Meccanica e ambientale

| ID | Priorità | Stato | Requisito / criterio |
|---|---|---|---|
| `PR-MEC-001` | MUST | CONF | Display incassato in un alloggiamento stampato 3D, solidale al corpo/testa. |
| `PR-MEC-002` | MUST | CAND | Presenza di accesso posteriore ai componenti per manutenzione senza tagliare/incollare parti permanenti. |
| `PR-MEC-003` | MUST | CAND | Base stabile su piano orizzontale **con il cavo USB sempre collegato** (uscita del cavo guidata, eventuale zavorra nella base). |
| `PR-MEC-004` | MUST | CAND | Sensore T/RH in zona ventilata, lontano da calore di regolatore, MCU e retroilluminazione. |
| `PR-MEC-005` | — | ESCLUSO | ~~Fissaggio della batteria~~: nessuna batteria in V1 (`DEC-023`). |
| `PR-MEC-006` | SHOULD | CAND | Fissaggi riapribili (viti/inseriti) e tolleranze dimensionate sul componente reale. |

## 6. Affidabilità e manutenzione

| ID | Priorità | Stato | Requisito / criterio |
|---|---|---|---|
| `PR-REL-001` | MUST | CAND | Dopo power cycle la schermata torna operativa senza procedure manuali non documentate. |
| `PR-REL-002` | MUST | CONF | Il firmware V1 non dipende da alcuna rete; la radio Wi-Fi/BLE resta disattivata (`DEC-012`). |
| `PR-REL-003` | MUST | CAND | Firmware aggiornabile dalla USB-C posteriore senza aprire l'involucro. |
| `PR-REL-004` | MUST | CAND | La misura ambientale non deve essere confusa con la temperatura interna di ESP32 o regolatore. |
| `PR-REL-005` | SHOULD | CAND | I log seriali non devono mostrare segreti o dati personali. |
| `PR-REL-006` | MUST | CONF | Elettronica su **PCB custom** (KiCad, JLCPCB) con il minimo indispensabile (`DEC-015`): scheda principale separata dal display, schedina portadisplay collegata via cavo (`DEC-021`); SHT40 su modulo breakout commerciale (`DEC-028`); punti di test per il bring-up. |
| `PR-REL-007` | MUST | CONF | Dalla USB-C posteriore un **configuratore da PC** legge stato e versione e imposta ora/data (dall'orologio del PC), fascia notte e luminosità tramite un protocollo documentato e versionato (`DEC-020`). |

## 7. Criteri di rilascio

Il passaggio da **design** a **V1 prototipo completo** richiede: (a) approvazione delle scelte TBD; (b) PCB revisionato e bring-up superato; (c) alimentazione USB e protezioni verificate; (d) test dei quattro dati visualizzati; (e) verifiche di dimensioni, stabilità con cavo e accessibilità; (f) misure di consumo e temperature interne in funzionamento continuo; (g) registro dei test compilato.

## 8. Relazioni

Architettura: [02](02-architettura-hardware.md) · Alimentazione: [03](03-alimentazione-ricarica.md) · Firmware: [04](04-specifiche-firmware.md) · UI: [05](05-interfaccia-utente.md) · Verifica: [07](07-piano-verifica.md).
