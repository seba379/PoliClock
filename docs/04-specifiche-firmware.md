# 04 — Specifiche firmware

**Versione:** 0.1 · **Stato:** architettura proposta, codice non ancora implementato · **Data:** 2026-11-07

## 1. Tecnologia

Proposta: **ESP-IDF** per ESP32-S3, con versione SDK **pinnata dopo il bring-up** e dipendenze deterministiche. In sviluppo si possono riutilizzare BSP/esempi Waveshare; evitare dipendenze non documentate o copiate senza licenza.

Il firmware V1 ha una funzione: mantenere il quadrante aggiornato e leggibile, minimizzando il consumo senza compromettere l'orologio. Bluetooth, servizi cloud, domotica, audio, GPS, SD e OTA non sono requisiti V1.

## 2. Architettura a componenti

```text
firmware/                      # struttura futura, non ancora generata
├── main/
│   └── app_main.c             # inizializzazione e supervisione
├── components/
│   ├── board_support/         # BSP Waveshare, periferiche e pin reali
│   ├── time_service/          # RTC, UTC, timezone, opzionale NTP
│   ├── climate_service/       # SHT40, validità dati e filtri
│   ├── power_service/         # AXP2101, USB, batteria, policy
│   ├── display_service/       # driver, backlight equivalente, refresh
│   ├── ui/                    # layout, widget, schermate
│   ├── input_service/         # touch ed eventi
│   ├── settings_service/      # NVS con schema/versione
│   └── diagnostics/           # logging e test di integrazione
└── test/                      # test unitari e banchi
```

**Separare il board support dalla logica prodotto**: il modulo Waveshare è candidato, e un eventuale cambio di scheda non deve imporre una riscrittura della UI o degli algoritmi di tempo/clima.

## 3. Contratti dati proposti

| Dato | Tipo logico | Origine | Regola |
|---|---|---|---|
| `time_utc` | timestamp UTC | RTC / NTP / impostazione manuale | Fonte unica per logica di tempo |
| `local_time` | ora locale derivata | TZ Europe/Rome | DST applicata dalla timezone, non modificando arbitrariamente RTC |
| `temp_c` | float/decimo °C | SHT40 | Marcato invalido se misura/CRC errore |
| `rh_pct` | float/%RH | SHT40 | Valido nell'intervallo fisico e dentro freschezza ammessa |
| `climate_timestamp` | monotonic timestamp | climate_service | Indica ultima misura valida |
| `usb_present` | boolean | PMU | Stato aggiornato su evento/poll calibrato |
| `battery_state` | enum | PMU + logica | Normal / Low / Critical / Charging / Unknown |
| `ui_mode` | enum | power/UI FSM | DIM / BRIGHT / WARNING / OFF |

Evitare accesso diretto ai registri della PMU dalla UI. La UI deve ricevere un modello immutabile coerente e un evento di aggiornamento.

## 4. Macchina a stati della luminosità

```mermaid
stateDiagram-v2
    [*] --> DIM: startup completato
    DIM --> BRIGHT: tocco valido
    BRIGHT --> BRIGHT: nuovo tocco / reset timer
    BRIGHT --> DIM: timeout interazione
    DIM --> WARNING: batteria critica o errore rilevante
    BRIGHT --> WARNING: batteria critica
    WARNING --> OFF: arresto controllato
    WARNING --> DIM: condizione ripristinata
    OFF --> DIM: nuovo avvio valido
```

- `DIM`: pagina principale in nero/blu scuro, luminosità bassa; **display acceso**.
- `BRIGHT`: stessa pagina con maggior luminosità per tempo configurabile (default sperimentale circa 20 s).
- `WARNING`: icona/messaggio non invasivo per condizioni gestibili; solo avvisi realmente critici devono impedire la pagina orologio.
- `OFF`: sistema in spegnimento controllato per batteria critica o comando power.

Lo stato `DIM` **non equivale** a deep sleep permanente: il display è attivo. Eventuali light-sleep/event wakeup dipendono da driver e interrupt verificati.

## 5. Inizializzazione raccomandata

1. Inizializzazione minima logging, watchdog e NVS.
2. Board-support, bus I²C e PMU; conferma di tensioni e alimentazioni.
3. RTC, validazione data/ora e preferenze utente.
4. Display e touch; presentazione schermata di boot breve, senza attendere rete.
5. Sensore SHT40 e primo campionamento valido.
6. Avvio servizi UI/tempo/alimentazione; ingresso in `DIM`.
7. Se abilitata, sincronizzazione NTP asincrona, con timeout e spegnimento Wi-Fi.

Errore su modulo non essenziale (Wi-Fi) non deve impedire il quadrante. Errore su RTC, batteria o display deve produrre stato diagnostico esplicito in log.

## 6. Tempo, RTC e sincronizzazione

- Riferimento interno in **UTC**.
- Presentazione configurata per **Europe/Rome**, con ora legale gestita correttamente; formato `HH:MM` 24h.
- Dopo cold boot, rilevare RTC mai inizializzato o dato palesemente invalido; **non mostrare un'ora inventata come corretta**.
- Percorso offline obbligatorio per impostazione tempo iniziale: menu touch o comando USB seriale di provisioning; almeno uno deve essere disponibile nella V1.
- NTP **opzionale**, con credenziali salvate in NVS e mai stampate nei log; l'assenza di rete non blocca i task.
- Aggiornare la cifra dei minuti al cambio minuto; rilevare cambi di data, DST e riavvio.
- Validare comportamento RTC con USB staccata e batteria presente; con batteria rimossa segnalare se l'orario deve essere reimpostato.

## 7. Misurazioni ambientali

- Lettura I²C SHT40 con timeout, verifica CRC prevista dal protocollo e retry limitati.
- Campionamento iniziale **ogni 60 s**, configurabile da 30 a 60 s dopo misura dei consumi.
- Coerenza valori e filtraggio leggero opzionale per non far oscillare la UI; non mascherare variazioni reali.
- Dati invalidi o vecchi oltre due periodi di acquisizione: mostrare `--` con indicazione di sensore non disponibile.
- Non usare temperatura MCU come sostituto di temperatura ambiente.
- Segnalare in diagnostica la frequenza errori I²C e l'età dell'ultima misura valida.

## 8. Power manager

- Centralizzare la lettura PMU e i comandi display/power in un solo servizio.
- Esportare **eventi** su presenza USB, battery low/critical, timer bright, campionamento, sync.
- Ridurre i wakeup non necessari: niente busy loop, timer periodici coerenti con le necessità della UI.
- Tracciare il profilo di consumo nello stesso firmware, distinguendo build di test e release.
- Monitor batteria a livelli finché una percentuale attendibile non sia stata calibrata.

## 9. Affidabilità, sicurezza e qualità

- Stato osservabile con log seriali; severità distinta INFO/WARN/ERROR e messaggi non eccessivi.
- Watchdog configurato per task potenzialmente bloccanti; timeout I²C/rete; niente blocchi infiniti su init non critica.
- Configurazioni NVS versionate con default sicuri; test di first-boot/reset preferenze.
- Niente password Wi-Fi nei log e niente endpoint di provisioning aperto permanentemente.
- Separare business logic dai driver: test unitari host per parsing/formatting tempo, DST, scadenza sensore, FSM UI e low-battery.
- Tenere uno strato di diagnostica minimale nel firmware release per indagini sul dispositivo assemblato.

## 10. Gate di completamento firmware

Tutti i test funzionali `VT-FUN-*`, `VT-FW-*` e `VT-PWR-*` previsti devono essere riproducibili; nessuna metrica di autonomia o consumo è accettata da log stimati senza misura strumentale. I requisiti di firmware devono sopravvivere a reset, USB plug/unplug, Wi-Fi assente, sensore scollegato, basso livello batteria e ora legale.
