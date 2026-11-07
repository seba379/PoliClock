# 01 — Requisiti di prodotto (PRD)

**Versione:** 0.1 · **Stato:** baseline per prototipo, da approvare · **Data:** 2026-11-07

## 1. Convenzioni

- **MUST** = necessario per considerare V1 accettabile; **SHOULD** = desiderabile; **TGT** = obiettivo da validare sperimentalmente.
- Stato **CONF** = scelta dell'utente; **CAND** = proposta tecnica; **TBD** = dettaglio non stabilito.
- Le soglie non confermate sono indicate come **valori iniziali per prove**, non come prestazioni garantite.
- La tracciabilità requisito → test è registrata nel [piano di verifica](07-piano-verifica.md).

## 2. Requisiti funzionali

| ID | Priorità | Stato | Requisito / criterio verificabile |
|---|---|---|---|
| `PR-FUN-001` | MUST | CONF | Visualizzare `HH:MM` in formato 24 ore sulla schermata principale senza intervento dell'utente. |
| `PR-FUN-002` | MUST | CONF | Visualizzare data e giorno della settimana in italiano. |
| `PR-FUN-003` | MUST | CONF | Visualizzare la temperatura misurata dal sensore locale, in °C. |
| `PR-FUN-004` | MUST | CONF | Visualizzare l'umidità relativa misurata localmente, in %RH. |
| `PR-FUN-005` | MUST | CONF | Permettere il funzionamento senza cavo USB collegato. |
| `PR-FUN-006` | MUST | CONF | Consentire la ricarica tramite porta USB-C posteriore. |
| `PR-FUN-007` | MUST | CONF | In condizione normale mantenere l'orologio attenuato ma leggibile; dopo un'interazione aumentare la luminosità e poi ripristinarla. |
| `PR-FUN-008` | MUST | CAND | Consentire l'impostazione iniziale/correzione dell'ora anche senza connessione Internet. |
| `PR-FUN-009` | MUST | CAND | Conservare l'ora durante il normale funzionamento a batteria tramite RTC, anche senza Wi-Fi. |
| `PR-FUN-010` | SHOULD | CAND | Consentire sincronizzazione NTP facoltativa quando configurato il Wi-Fi. |
| `PR-FUN-011` | MUST | CAND | Esporre uno stato chiaro di batteria bassa e avvertire prima dello spegnimento. |
| `PR-FUN-012` | MUST | CAND | In caso di errore sensore, indicare dato non disponibile senza mostrare valori vecchi come attuali. |

## 3. Interfaccia e presentazione

| ID | Priorità | Stato | Requisito / criterio |
|---|---|---|---|
| `PR-UI-001` | MUST | CONF | La superficie attiva del display è circolare e occupa il volto. |
| `PR-UI-002` | MUST | CONF | L'aspetto complessivo è una poliziotta chibi riconoscibile con uniforme blu e cappello. |
| `PR-UI-003` | MUST | CAND | Tutti i dati essenziali sono leggibili da distanza di scrivania tipica (prova 50–80 cm in luce interna). |
| `PR-UI-004` | SHOULD | CAND | Prediligere fondo scuro, tipografia chiara e contrasto elevato. |
| `PR-UI-005` | SHOULD | CAND | Limitare permanenza di contenuti AMOLED ad alta luminanza in posizioni fisse (mitigazione burn-in). |
| `PR-UI-006` | MUST | CAND | La visualizzazione deve rimanere coerente durante perdita temporanea del sensore, mancanza Wi-Fi e ricarica. |
| `PR-UI-007` | SHOULD | CAND | Il display touch, se disponibile, deve permettere attivazione della modalità luminosa. |

## 4. Elettrico, batteria e sicurezza

| ID | Priorità | Stato | Requisito / criterio |
|---|---|---|---|
| `PR-PWR-001` | MUST | CONF | Alimentazione tramite batteria ricaricabile integrata. |
| `PR-PWR-002` | MUST | CONF | Porta di ricarica USB-C esterna sul retro, senza disassemblare la statuetta. |
| `PR-PWR-003` | MUST | CAND | Ricarica gestita da circuito idoneo alla chimica/cella selezionata, con limiti di corrente, tensione e temperatura verificati. |
| `PR-PWR-004` | MUST | CAND | Batteria con adeguata protezione e polarità verificata; cablaggi isolati e protetti da schiacciamento/strappo. |
| `PR-PWR-005` | MUST | CAND | Funzionamento e ricarica simultanei consentiti solo dopo verifica del circuito reale e test termici. |
| `PR-PWR-006` | TGT | CAND | Obiettivo autonomia iniziale: **≥48 ore** a profilo d'uso dichiarato; non ancora dimostrato. |
| `PR-PWR-007` | SHOULD | CAND | Misura/rappresentazione dello stato batteria evitando di inventare percentuali da tensione grezza non calibrata. |
| `PR-PWR-008` | MUST | CAND | Condizione di scarica critica gestita in modo da evitare ripetuti cicli di riavvio e danni alla cella. |

## 5. Meccanica e ambientale

| ID | Priorità | Stato | Requisito / criterio |
|---|---|---|---|
| `PR-MEC-001` | MUST | CONF | Display incassato in un alloggiamento stampato 3D, solidale al corpo/testa. |
| `PR-MEC-002` | MUST | CAND | Presenza di accesso posteriore ai componenti per manutenzione senza tagliare/incollare parti permanenti. |
| `PR-MEC-003` | MUST | CAND | Base stabile su piano orizzontale con cavo collegato e scollegato. |
| `PR-MEC-004` | MUST | CAND | Sensore T/RH in zona ventilata, lontano da calore di PMU, MCU, display e batteria. |
| `PR-MEC-005` | MUST | CAND | Batteria bloccata meccanicamente senza compressione, punzonature o contatto con spigoli. |
| `PR-MEC-006` | SHOULD | CAND | Fissaggi riapribili (viti/inseriti) e tolleranze dimensionate sul componente reale. |

## 6. Affidabilità e manutenzione

| ID | Priorità | Stato | Requisito / criterio |
|---|---|---|---|
| `PR-REL-001` | MUST | CAND | Dopo power cycle la schermata torna operativa senza procedure manuali non documentate. |
| `PR-REL-002` | MUST | CAND | Wi-Fi assente non impedisce il funzionamento della schermata principale. |
| `PR-REL-003` | SHOULD | CAND | Firmware aggiornabile via USB-C senza aprire l'involucro. |
| `PR-REL-004` | MUST | CAND | La misura ambientale non deve essere confusa con la temperatura interna di ESP32 o PMU. |
| `PR-REL-005` | SHOULD | CAND | I log seriali non devono mostrare password Wi-Fi né altri segreti. |

## 7. Criteri di rilascio

Il passaggio da **V0.1 design** a **V1 prototipo completo** richiede: (a) approvazione delle scelte TBD; (b) prova dell'alimentazione e ricarica reale; (c) test dei quattro dati visualizzati; (d) verifiche di dimensioni e accessibilità; (e) evidenza delle misure di autonomia e temperatura; (f) registro dei test compilato. Il target di 48 ore va discusso con dati strumentali: non si abbassa tacitamente per dichiarare completato il progetto.

## 8. Relazioni

Architettura: [02](02-architettura-hardware.md) · Energia: [03](03-alimentazione-ricarica.md) · Firmware: [04](04-specifiche-firmware.md) · UI: [05](05-interfaccia-utente.md) · Verifica: [07](07-piano-verifica.md).
