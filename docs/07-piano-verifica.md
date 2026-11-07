# 07 — Piano di verifica e validazione (V&V)

**Versione:** 0.5 · **Stato:** pianificato, nessun test eseguito · **Data:** 2026-11-07

## 1. Principi

- Distingue **verifica** (la realizzazione rispetta i requisiti) e **validazione** (è un regalo gradevole/utile).
- Ogni test richiede: ID, revisione HW, SHA firmware, strumenti, precondizioni, passi, evidenze, risultato e data.
- Risultato ammesso: `PASS`, `FAIL`, `BLOCKED`, `NOT_RUN`.
- **Tutti i test sono NOT_RUN**: non presentare numeri ipotetici come risultati.
- I test legati alla batteria sono stati rimossi con `DEC-023`; gli ID `VT-PWR-*` sono stati riassegnati all'alimentazione USB.

## 2. Tracciabilità requisito → test

| ID test | Requisiti | Livello | Metodo / accettazione |
|---|---|---|---|
| `VT-FUN-001` | PR-FUN-001, PR-FUN-002 | Sistema | Ora 24h e data/giorno corretti dopo configurazione, trascorrere minuti e cambio giorno |
| `VT-FUN-002` | PR-FUN-003, PR-FUN-004 | Sistema | Valori locali visualizzati, unità corrette e aggiornamento periodico |
| `VT-FUN-003` | PR-PWR-008, PR-UI-006, PR-REL-001 | Sistema | Almeno 50 cicli di scollegamento/ricollegamento del cavo in momenti diversi (anche durante scritture di configurazione): riavvio pulito, configurazione integra, ora corretta |
| `VT-FUN-004` | PR-FUN-006, PR-PWR-001, PR-PWR-002 | Sistema | Alimentazione dalla USB-C sul sedere con alimentatore 5 V comune e con porta USB di un PC; connettore accessibile |
| `VT-UI-001` | PR-FUN-007, PR-UI-003, PR-UI-007 | Sistema | DIM leggibile, pulsante→BRIGHT, timeout→DIM, prova a 50–80 cm |
| `VT-UI-002` | PR-UI-004 | Ispezione | Contrasto e leggibilità del fondo scuro su IPS |
| `VT-UI-003` | PR-FUN-013 | Sistema | Ingresso/uscita fascia notte (anche a cavallo della mezzanotte), display e retroilluminazione spenti, pulsante → NIGHT_PEEK → NIGHT |
| `VT-UI-004` | PR-UI-008 | Progetto + sistema | Footprint/connettore touch e GPIO INT/RST presenti sul PCB; prova del modulo touch sul prototipo M1 (evento → BRIGHT) |
| `VT-FW-001` | PR-FUN-008, PR-FUN-009 | Firmware + sistema | Impostazione ora offline e mantenimento a cavo scollegato |
| `VT-FW-002` | PR-REL-002 | Firmware | Build release senza inizializzazione radio; nessuna dipendenza di rete |
| `VT-FW-003` | PR-FUN-012, PR-REL-004, PR-UI-006 | Firmware | Distacco SHT40/CRC errato → dato invalidato e segnalazione, niente valore stale |
| `VT-FW-004` | PR-REL-001 | Sistema | Riavvio ripristina servizio e configurazione, senza fault persistenti |
| `VT-FW-005` | PR-REL-003, PR-REL-005 | Firmware | Flash e log dalla USB-C posteriore, log privi di segreti |
| `VT-FW-006` | PR-FUN-008, PR-UI-007 | Sistema | Impostazione di ora, data e fascia notte con il solo pulsante (riserva) |
| `VT-FW-007` | PR-FUN-008, PR-REL-007 | Sistema | Configuratore da PC dalla USB-C posteriore: connessione, `HELLO`, sincronizzazione dell'ora dal PC (scarto < 2 s), fascia notte e luminosità salvate e mantenute dopo riavvio; comandi invalidi rifiutati |
| `VT-PWR-001` | PR-PWR-004 | Elettrico | Fusibile/PTC, ESD e resistenze CC verificati a schema e su banco; nessun danno con cortocircuito simulato a valle del fusibile |
| `VT-PWR-002` | PR-PWR-005 | Elettrico/termico | Funzionamento continuo ≥ 24 h a scocca chiusa: temperature di regolatore, MCU, retroilluminazione e materiale entro i limiti dei datasheet |
| `VT-PWR-003` | PR-PWR-009 | Elettrico | Corrente USB media e di picco misurata in DIM, BRIGHT, NIGHT |
| `VT-PWR-004` | PR-FUN-009 | Elettrico | Durata del tampone RTC a cavo scollegato misurata o stimata da corrente misurata; ora corretta al ricollegamento |
| `VT-MEC-001` | PR-MEC-001, PR-UI-001 | Meccanico | Display realmente circolare incassato al posto del volto, senza interferenze |
| `VT-MEC-002` | PR-MEC-002, PR-MEC-006 | Meccanico | Apertura sportello/estrazione componenti senza danno |
| `VT-MEC-003` | PR-MEC-003 | Meccanico | Stabilità su piano con cavo USB sempre inserito sul sedere, cavo tirato leggermente e pressione del pulsante |
| `VT-MEC-004` | PR-MEC-004 | Meccanico/termico | SHT40 ventilato, errore termico dovuto alla scocca misurato |
| `VT-PCB-001` | PR-REL-006 | Progetto | ERC/DRC puliti, checklist di revisione schema/layout, revisione visiva del proprietario in KiCad, disponibilità LCSC, sagome e connettori compatibili con il CAD |
| `VT-PCB-002` | PR-REL-006, PR-PWR-004 | Elettrico | Bring-up: alimentazione con limitazione di corrente, assenza di cortocircuiti, 3,3 V corretta, enumerazione USB, flash, display, pulsante, scan I²C |
| `VT-PCB-003` | PR-REL-006, PR-UI-001 | Elettrico | Display stabile sul cavo reale nel collo: nessun artefatto per almeno 24 h alla frequenza SPI scelta |
| `VT-VAL-001` | Visione prodotto, PR-UI-002 | Utente | Aspetto chibi coerente, leggibilità percepita e comodità d'uso approvate |

## 3. Casi test dettagliati iniziali

### VT-PWR-002 — Funzionamento continuo e temperature

**Precondizioni:** scocca rappresentativa chiusa, firmware release, alimentatore USB 5 V comune. **Procedura:** 24 h di funzionamento con il ciclo reale DIM/BRIGHT/NIGHT; misurare con sonde o termocamera regolatore, MCU, retroilluminazione, interno scocca e vano sensore. **Accettazione:** temperature entro i limiti dei **datasheet** dei componenti e del materiale di stampa; soglie numeriche definite sui componenti effettivi, non inventate in anticipo.

### VT-FW-001 — Ora offline

1. Avviare con RTC inizialmente non valido; deve essere indicato `TIME_NOT_SET`.
2. Impostare l'ora con il configuratore da PC (metodo principale) e, in una seconda prova, con il menu del pulsante.
3. Verificare cambio minuto/giorno.
4. Provare transizioni ora legale/solare Europa/Roma con clock simulato nei test unitari.
5. Scollegare il cavo: l'ora deve sopravvivere grazie al tampone dell'RTC per la durata dimensionata; a tampone esaurito atteso `TIME_NOT_SET` (`OPEN-014`).
6. Misurare la deriva dell'RTC su almeno 7 giorni senza correzioni (nessun NTP in V1).

### VT-FW-003 — Guasto sensore

1. Rilevare una lettura valida.
2. Scollegare SHT40 in condizioni controllate; dopo la finestra di freschezza la UI deve mostrare `--`.
3. Ripristinare il sensore; acquisizione corretta senza reboot necessario, se supportato.
4. Iniettare CRC e timeout errati via test/mocks; nessun valore vecchio deve sembrare attuale.

### VT-MEC-004 — Errore termico sensore

Confrontare SHT40 montato nello chassis e sensore di riferimento **co-locato** nelle stesse condizioni in almeno due scenari: DIM a regime (dopo alcune ore) e BRIGHT prolungato. Registrare tempi di assestamento e differenza di temperatura/RH; accettabilità dell'errore aggiuntivo da definire prima del test. Con alimentazione continua il riscaldamento interno è permanente: è il test più importante per la credibilità della misura.

## 4. Test unitari software consigliati

- Formatting ora, date e locale.
- DST Italia: 02:00 e 03:00 nei cambi previsti, gap/ora ripetuta.
- FSM DIM/BRIGHT/NIGHT/NIGHT_PEEK con timeout, pressioni ripetute e fascia notte a cavallo della mezzanotte.
- Lettura SHT40: CRC, retry e stale data.
- Gestione pulsante: antirimbalzo, pressione breve/lunga, menu di impostazione.
- Parser del protocollo del configuratore (§6.1 firmware) con input invalidi, versioni incompatibili e limiti dei parametri.
- Reset NVS, migrazione schema configurazione, ora mai impostata, scrittura interrotta.

## 5. Strumentazione minima

Multimetro affidabile, misuratore di corrente USB (anche dinamico), alimentatore USB 5 V affidabile, alimentatore da banco con limitazione di corrente per il bring-up, termometro/sonde o termocamera, un riferimento T/RH per confronto, calibro, computer per log ESP-IDF.

## 6. Registro risultati (modello)

```text
Test ID:
Data / esecutore:
HW revision:
Firmware SHA / configurazione:
Alimentatore USB usato:
Strumenti e riferimenti:
Condizioni ambientali:
Passi svolti:
Misure (con unità):
Evidenze (foto, log, csv):
Risultato: NOT_RUN | PASS | FAIL | BLOCKED
Difetto riscontrato / issue:
```

## 7. Gate di rilascio

Non consegnare il dispositivo assemblato se i test di protezione ingresso, temperatura in funzionamento continuo e stabilità con cavo sono `FAIL`, `BLOCKED` o `NOT_RUN`. I test estetici devono essere valutati esplicitamente.
