# 07 — Piano di verifica e validazione (V&V)

**Versione:** 0.4 · **Stato:** pianificato, nessun test eseguito · **Data:** 2026-11-07

## 1. Principi

- Distingue **verifica** (la realizzazione rispetta i requisiti) e **validazione** (è un regalo gradevole/utile).
- Ogni test richiede: ID, revisione HW, SHA firmware, strumenti, precondizioni, passi, evidenze, risultato e data.
- Risultato ammesso: `PASS`, `FAIL`, `BLOCKED`, `NOT_RUN`.
- In questa V0.1 **tutti i test sono NOT_RUN**: non presentare numeri ipotetici come risultati.

## 2. Tracciabilità requisito → test

| ID test | Requisiti | Livello | Metodo / accettazione |
|---|---|---|---|
| `VT-FUN-001` | PR-FUN-001, PR-FUN-002 | Sistema | Ora 24h e data/giorno corretti dopo configurazione, trascorrere minuti e cambio giorno |
| `VT-FUN-002` | PR-FUN-003, PR-FUN-004 | Sistema | Valori locali visualizzati, unità corrette e aggiornamento periodico |
| `VT-FUN-003` | PR-FUN-005, PR-PWR-001 | Sistema | USB rimossa, dispositivo continua a funzionare con batteria |
| `VT-FUN-004` | PR-FUN-006, PR-PWR-002 | Sistema | Cavo USB-C inserito nel retro, ricarica rilevata e connettore accessibile |
| `VT-UI-001` | PR-FUN-007, PR-UI-003, PR-UI-007 | Sistema | DIM leggibile, pulsante→BRIGHT, timeout→DIM, prova a 50–80 cm |
| `VT-UI-002` | PR-UI-004 | Ispezione | Contrasto e leggibilità del fondo scuro su IPS (PR-UI-005 escluso, `DEC-016`) |
| `VT-UI-003` | PR-FUN-013 | Sistema | Ingresso/uscita fascia notte (anche a cavallo della mezzanotte), display e retroilluminazione spenti, pulsante → NIGHT_PEEK → NIGHT, consumo `P3 NIGHT` misurato |
| `VT-FW-001` | PR-FUN-008, PR-FUN-009 | Firmware + sistema | Impostazione ora offline e mantenimento senza Wi-Fi |
| `VT-FW-002` | PR-REL-002 | Firmware | Build release senza inizializzazione radio; nessuna dipendenza di rete al boot o a regime (PR-FUN-010 escluso, `DEC-012`) |
| `VT-FW-003` | PR-FUN-012, PR-REL-004, PR-UI-006 | Firmware | Distacco SHT40/CRC errato → dato invalidato e segnalazione, niente valore stale |
| `VT-FW-004` | PR-REL-001 | Sistema | Riavvio ripristina servizio e configurazione, senza fault persistenti |
| `VT-FW-005` | PR-REL-003, PR-REL-005 | Firmware | Flash e log dalla USB-C posteriore (anche attraverso la prolunga, se presente), log privi di segreti |
| `VT-FW-006` | PR-FUN-008, PR-UI-007 | Sistema | Impostazione di ora, data e fascia notte con il solo pulsante (riserva) |
| `VT-FW-007` | PR-FUN-008, PR-REL-007 | Sistema | Configuratore da PC dalla USB-C posteriore: connessione, `HELLO`, sincronizzazione dell'ora dal PC (scarto < 2 s), fascia notte e luminosità salvate e mantenute dopo riavvio; comandi invalidi rifiutati |
| `VT-UI-004` | PR-UI-008 | Progetto + sistema | Footprint/connettore touch e GPIO INT/RST presenti sul PCB; prova del modulo touch sul prototipo M1 (evento -> BRIGHT, consumo in sleep misurato) |
| `VT-PWR-001` | PR-PWR-003, PR-PWR-004 | Elettrico | Protezioni, polarità, cella/caricatore compatibili e verificati a schema e banco; corrente di carica misurata; **cutoff NTC** provato scaldando/raffreddando la sonda |
| `VT-PWR-002` | PR-PWR-005 | Elettrico/termico | Uso durante ricarica senza anomalie di tensione, corrente e temperatura |
| `VT-PWR-003` | PR-PWR-006 | Elettrico | Ciclo completo a profilo V1, autonomia reale confrontata con target 48 h |
| `VT-PWR-004` | PR-PWR-007, PR-PWR-008, PR-FUN-011 | Elettrico | Avviso low-battery, cutoff, no boot-loop, recovery USB |
| `VT-MEC-001` | PR-MEC-001, PR-UI-001 | Meccanico | Display realmente circolare incassato al posto del volto, senza interferenze |
| `VT-MEC-002` | PR-MEC-002, PR-MEC-006 | Meccanico | Apertura sportello/estrazione componenti senza danno |
| `VT-MEC-003` | PR-MEC-003 | Meccanico | Stabilità su piano, pressione del pulsante e cavo USB inserito sul sedere |
| `VT-MEC-004` | PR-MEC-004, PR-MEC-005 | Meccanico/termico | SHT40 ventilato, batteria fissata e isolata, nessuna interferenza termica anomala |
| `VT-PCB-001` | PR-REL-006 | Progetto | ERC/DRC puliti, checklist di revisione schema/layout, revisione visiva del proprietario in KiCad, disponibilità LCSC, sagome e connettori compatibili con il CAD |
| `VT-PCB-003` | PR-REL-006, PR-UI-001 | Elettrico | Display stabile sul cavo reale nel collo: nessun artefatto per almeno 24 h di funzionamento alla frequenza SPI scelta, anche con ricarica attiva |
| `VT-PCB-002` | PR-REL-006, PR-PWR-003 | Elettrico | Bring-up: alimentazioni con limitazione di corrente, assenza di cortocircuiti, 3,3 V corretta, enumerazione USB, flash, display, pulsante, scan I²C |
| `VT-VAL-001` | Visione prodotto, PR-UI-002 | Utente | Aspetto chibi coerente, leggibilità percepita e comodità d'uso approvate |

## 3. Casi test dettagliati iniziali

### VT-PWR-003 — Autonomia batteria

**Precondizioni:** batteria identificata e caricata secondo procedura del produttore, firmware release con medesima configurazione del regalo, scocca rappresentativa, profilo d'uso `DEC-014`. **Procedura:** avviare a ora nota, USB scollegata; applicare il profilo (16 h `DIM`, 8 h `NIGHT`, 30 attivazioni `BRIGHT`/giorno da 20 s, SHT40 ogni 60 s, radio spenta), registrando gli eventi effettivi; registrare corrente e tensione batteria. **Accettazione:** autonomia reale riportata in ore, confronto esplicito con target **48 h**. Nessun `PASS` senza misura fino al cutoff definito e verifica di sicurezza.

### VT-PWR-002 — Ricarica durante funzionamento

**Precondizioni:** conferma di carica, polarità e corrente compatibile. **Procedura:** misurare alimentazione USB/batteria e temperature con DIM, BRIGHT, varie fasi della carica, portellino aperto e scocca chiusa secondo sicurezza; includere una prova prolungata (almeno 24 h) con USB sempre collegata e batteria carica, perché è un uso previsto (`DEC-008`). **Accettazione:** nessuna anomalia elettrica/termica; temperatura entro i limiti dei **datasheet** di cella, caricatore, regolatore, display e materiale. Soglie numeriche da definire sui componenti effettivi, non inventate in anticipo.

### VT-FW-001 — Ora offline

1. Avviare senza rete e con RTC inizialmente non valido; deve essere indicato `TIME_NOT_SET`.
2. Impostare l'ora con il configuratore da PC (metodo principale) e, in una seconda prova, con il menu del pulsante.
3. Rimuovere USB con batteria collegata; verificare ora e cambio minuto/giorno.
4. Provare transizioni ora legale/solare Europa/Roma con clock simulato nei test unitari.
5. Scollegare la cella e la USB: l'ora deve sopravvivere grazie al tampone dell'RTC per il tempo dichiarato dal suo dimensionamento; a tampone esaurito atteso `TIME_NOT_SET` (`OPEN-014`).
6. Misurare la deriva dell'RTC su almeno 7 giorni senza correzioni (nessun NTP in V1).

### VT-FW-003 — Guasto sensore

1. Rilevare una lettura valida.
2. Scollegare SHT40 in condizioni controllate; dopo la finestra di freschezza la UI deve mostrare `--`.
3. Ripristinare il sensore; acquisizione corretta senza reboot necessario, se supportato.
4. Iniettare CRC e timeout errati via test/mocks; nessun valore vecchio deve sembrare attuale.

### VT-MEC-004 — Errore termico sensore

Confrontare SHT40 montato nello chassis e sensore di riferimento **co-locato** nelle stesse condizioni in almeno tre scenari: USB scollegata a regime, ricarica attiva a regime, BRIGHT prolungato. Registrare tempi di assestamento e differenza di temperatura/RH; accettabilità dell'errore aggiuntivo da definire prima del test.

## 4. Test unitari software consigliati

- Formatting ora, date e locale.
- DST Italia: 02:00 e 03:00 nei cambi previsti, gap/ora ripetuta.
- FSM DIM/BRIGHT/NIGHT/NIGHT_PEEK con timeout, tocchi ripetuti e fascia notte a cavallo della mezzanotte.
- Lettura SHT40: CRC, retry e stale data.
- Conversione misura batteria in livelli: limiti, incognite, nessuna percentuale fittizia.
- Gestione pulsante: antirimbalzo, pressione breve/lunga, menu di impostazione.
- Parser del protocollo del configuratore (§6.1 firmware) con input invalidi, versioni incompatibili e limiti dei parametri.
- Reset NVS, migrazione schema configurazione e ora mai impostata.

## 5. Strumentazione minima

Multimetro affidabile, strumento per acquisizione corrente (anche dinamica), alimentatore USB 5 V affidabile, termometro/sonda per batteria e caricatore, alimentatore da banco con limitazione di corrente per il bring-up, un riferimento T/RH per confronto, calibro, computer per log ESP-IDF e strumento di verifica continuità/polarità. Se possibile, termocamera per analisi a ricarica attiva.

## 6. Registro risultati (modello)

```text
Test ID:
Data / esecutore:
HW revision / scheda SKU:
Firmware SHA / configurazione:
Batteria: marca/modello/capacità/età:
Strumenti e riferimenti:
Condizioni ambientali:
Passi svolti:
Misure (con unità):
Evidenze (foto, log, csv):
Risultato: NOT_RUN | PASS | FAIL | BLOCKED
Difetto riscontrato / issue:
```

## 7. Gate di rilascio

Non consegnare il dispositivo assemblato se i test batteria/ricarica/polarità/temperatura sono `FAIL`, `BLOCKED` o `NOT_RUN`. I test estetici e la durata nominale devono essere valutati esplicitamente, senza spacciare gli obiettivi per esiti sperimentali.
