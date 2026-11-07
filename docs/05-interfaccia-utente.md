# 05 — Specifiche interfaccia utente (UI/UX)

**Versione:** 0.3 · **Stato:** wireframe testuale, non design grafico finale · **Data:** 2026-11-07

## 1. Obiettivo

L'interfaccia occupa il **volto circolare** della poliziotta: display IPS rotondo 1,28", **240×240** (`DEC-016`). Deve essere attraente e leggibile in modo passivo da scrivania. Il tema di base: **blu notte / quasi nero, bianco, accenti azzurro**, in armonia con la statuetta. La V1 è **un solo quadrante principale**, non una dashboard domotica.

## 2. Gerarchia dei contenuti

1. **Ora** (`HH:MM`) è il contenuto prioritario, il più grande.
2. **Data** in italiano sotto l'ora (`Sab 7 nov` o `Sabato 7 novembre` secondo spazio).
3. **Temperatura** (`22,4 °C`) e **umidità** (`48 %`) su riga secondaria con icone.
4. Piccoli indicatori opzionali **batteria/ricarica** e **segnalazioni** in area marginale.

Non mostrare meteo Internet: temperatura e umidità sono **misure ambientali locali**. Evitare di usare icone sole/pioggia che possano far intendere previsioni non presenti.

## 3. Wireframe concettuale

```text
          .----------------------.
       .-'    [batteria]           '-.
      /                                \
     |            17:42               |
     |        Sabato 7 novembre        |
     |                                 |
     |    [termometro] 22,4 °C         |
     |    [goccia]      48 %RH         |
      \                                /
       '-.__________________________.-'
```

Il wireframe **non** definisce dimensioni, allineamenti o margini in pixel. Il layout verrà adattato all'area effettivamente visibile del display, distinguendo diametro attivo e apertura meccanica della cornice.

## 4. Stati visuali

I primi quattro sono **modi di luminosità** (`display_mode` nel [firmware](04-specifiche-firmware.md)); gli altri sono **indicatori** sovrapposti (`ui_flags`) che compaiono in qualunque modo visibile.

| Stato | Aspetto desiderato | Trigger / uscita |
|---|---|---|
| `DIM` | Fondo nero, testo ridotto di luminanza, ora ben leggibile | Default di giorno quando non si interagisce |
| `BRIGHT` | Stessi dati, luminosità aumentata e accenti più evidenti | Pressione breve del pulsante; ritorno a DIM dopo timeout, es. 20 s proposti |
| `NIGHT` | Display e retroilluminazione spenti | Fascia notte, default 23:00–07:00 (`DEC-013`) |
| `NIGHT_PEEK` | Quadrante attenuato, nessun accento luminoso | Pressione breve di notte; ritorno a NIGHT dopo il timeout |
| `CHARGING` | Icona batteria/fulmine discreta | USB presente e ricarica confermata |
| `LOW_BATT` | Icona con evidenza adeguata; niente animazioni energivore | Soglia da validare sulla misura batteria scelta |
| `TIME_NOT_SET` | Messaggio chiaro e accesso a impostazione | RTC invalido/mai impostato |
| `SENSOR_ERROR` | `--` per T/RH e simbolo sensore | Timeout o misura non valida |

## 5. Interazioni V1 proposte

Un solo **pulsante** fisico (`DEC-017`), posizione nella statuetta da definire (`OPEN-017`).

- **Pressione breve**: di giorno aumenta la luminosità e ripristina il timer; di notte mostra l'ora attenuata (`NIGHT_PEEK`).
- **Pressione lunga** (es. 3 s, da tarare): entra nel menu di impostazione.
- **Configuratore da PC via USB** (metodo principale, `DEC-020`): si collega PoliClock al computer, si apre la pagina del configuratore e con un clic si sincronizza l'ora con quella del PC; dallo stesso strumento si impostano fascia notte e luminosità.
- **Menu di impostazione con un pulsante** (riserva, `OPEN-015`): il campo selezionato lampeggia; pressione breve = incrementa il valore, pressione lunga = conferma e passa al campo successivo (ora → minuti → giorno → mese → anno → inizio notte → fine notte). Uscita automatica senza salvare dopo un tempo di inattività.
- **Touch (predisposto, `DEC-019`)**: se montato, il tocco sul display equivale alla pressione breve; il pulsante resta comunque attivo.
- Nessun menu richiesto per visualizzare i quattro dati quotidiani.

Il risveglio dal light-sleep tramite pulsante va provato sul prototipo M1 prima di fissare il PCB.

## 6. Parametri iniziali di prototipo (TBD)

| Parametro | Valore iniziale di sperimentazione | Note |
|---|---|---|
| Luminosità DIM | 10–15% del PWM di retroilluminazione | Percentuale *non* equivale a cd/m² o potenza |
| Luminosità BRIGHT | 60–70% del PWM di retroilluminazione | Calibrare in ambiente reale |
| Timeout BRIGHT | 20 s | Ritriggerabile dal pulsante |
| Fascia notte | 23:00–07:00 | Display spento; configurabile (`DEC-013`) |
| Timeout NIGHT_PEEK | 10 s | Quadrante attenuato dopo pressione notturna |
| Pressione lunga | 3 s | Ingresso nel menu di impostazione |
| Aggiornamento ora | Al cambio minuto | Non eseguire full redraw continuo |
| Aggiornamento clima | 60 s | Da accordare a energia/reattività |
| Lingua | Italiano | Formato 24 h e data locale |

## 7. Leggibilità

- Test di lettura a **50–80 cm** in luce di scrivania, sia DIM che BRIGHT. Con 240×240 su circa 32 mm i caratteri dell'ora devono essere grandi: verificare sul display reale.
- Preferire font numerici leggibili e tabulari per evitare oscillazioni nella dimensione dell'ora.
- Su IPS il nero non è assoluto (retroilluminazione sempre accesa di giorno): il fondo scuro resta preferito per contrasto ed estetica, non per il consumo.
- Nessun rischio di burn-in con IPS: la mitigazione AMOLED non è più richiesta (`PR-UI-005` escluso).

## 8. Indicatori d'errore e significato

- `-- °C` / `-- %`: dato ambientale momentaneamente non valido.
- Batteria bassa: icona leggibile, senza percentuale fittizia; allerta prima del cutoff.
- Ora da impostare: evidenziare chiaramente che il valore non è affidabile.
- Nessun indicatore di rete: la V1 è interamente offline (`DEC-012`).

## 9. Deliverable grafici futuri

- UI screen mockup **240×240 px** coerente con il display selezionato, con area sicura circolare.
- Palette e font con licenze documentate; asset originali.
- Schermate DIM/BRIGHT/NIGHT_PEEK/CHARGING/LOW_BATT/TIME_NOT_SET/SENSOR_ERROR e flusso di impostazione ora/fascia notte.
- Screenshot dal display fisico verificati, non soltanto render di marketing.
