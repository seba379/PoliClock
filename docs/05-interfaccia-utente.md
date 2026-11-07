# 05 — Specifiche interfaccia utente (UI/UX)

**Versione:** 0.1 · **Stato:** wireframe testuale, non design grafico finale · **Data:** 2026-11-07

## 1. Obiettivo

L'interfaccia occupa il **volto circolare** della poliziotta. Deve essere attraente e leggibile in modo passivo da scrivania. Il tema di base: **blu notte / quasi nero, bianco, accenti azzurro**, in armonia con la statuetta. La V1 è **un solo quadrante principale**, non una dashboard domotica.

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
| `BRIGHT` | Stessi dati, luminosità aumentata e accenti più evidenti | Tocco; ritorno a DIM dopo timeout, es. 20 s proposti |
| `NIGHT` | Display spento | Fascia notte, default proposto 23:00–07:00 (`CAND-009`) |
| `NIGHT_PEEK` | Quadrante attenuato, nessun accento luminoso | Tocco di notte; ritorno a NIGHT dopo il timeout |
| `CHARGING` | Icona batteria/fulmine discreta | USB presente e ricarica confermata |
| `LOW_BATT` | Icona con evidenza adeguata; niente animazioni energivore | Soglia da validare con PMU |
| `TIME_NOT_SET` | Messaggio chiaro e accesso a impostazione | RTC invalido/mai impostato |
| `SENSOR_ERROR` | `--` per T/RH e simbolo sensore | Timeout o misura non valida |

## 5. Interazioni V1 proposte

- **Tocco breve** sul quadrante: aumenta luminosità, ripristina timer.
- **Pressione prolungata / gesto** (da validare sulle capacità del driver touch): apre configurazione ora oppure menu essenziale.
- **Impostazione ora offline** (unico metodo in V1, nessun NTP): flusso semplice per ora, minuti e data; prevedere annulla/conferma. Se non implementabile in tempo, garantire provisioning USB prima della consegna. Lo stesso percorso imposta la fascia notte.
- Nessun menu richiesto per visualizzare i quattro dati quotidiani.

Se il touch non può risvegliare in modo affidabile un assetto a basso consumo, mantenere un polling leggero e documentare l'impatto energetico. Non promettere touch wakeup da deep-sleep senza prova.

## 6. Parametri iniziali di prototipo (TBD)

| Parametro | Valore iniziale di sperimentazione | Note |
|---|---|---|
| Luminosità DIM | 10–15% del comando software disponibile | Percentuale *non* equivale a cd/m² o potenza |
| Luminosità BRIGHT | 60–70% del comando software disponibile | Calibrare in ambiente reale |
| Timeout BRIGHT | 20 s | Ritriggerabile da touch |
| Fascia notte | 23:00–07:00 | Display spento; configurabile (`CAND-009`) |
| Timeout NIGHT_PEEK | 10 s | Quadrante attenuato dopo tocco notturno |
| Aggiornamento ora | Al cambio minuto | Non eseguire full redraw continuo |
| Aggiornamento clima | 60 s | Da accordare a energia/reattività |
| Lingua | Italiano | Formato 24 h e data locale |

## 7. Leggibilità e burn-in

- Test di lettura a **50–80 cm** in luce di scrivania, sia DIM che BRIGHT.
- Preferire font numerici leggibili e tabulari per evitare oscillazioni nella dimensione dell'ora.
- Ridurre i pixel accesi non necessari nell'AMOLED.
- **Obbligatorio** (`PR-UI-005`): lievi spostamenti periodici dei contenuti fissi (pixel shift di pochi pixel, es. a ogni cambio minuto o ora), senza far saltare visibilmente i numeri; misurare la leggibilità. La modalità notte riduce ulteriormente le ore di accensione.
- Evitare loghi statici grandi e luminosi accesi per giorni.

## 8. Indicatori d'errore e significato

- `-- °C` / `-- %`: dato ambientale momentaneamente non valido.
- Batteria bassa: icona leggibile, senza percentuale fittizia; allerta prima del cutoff.
- Ora da impostare: evidenziare chiaramente che il valore non è affidabile.
- Nessun indicatore di rete: la V1 è interamente offline (`DEC-012`).

## 9. Deliverable grafici futuri

- UI screen mockup **466×466 px** coerente con il display selezionato, con area sicura circolare.
- Palette e font con licenze documentate; asset originali.
- Schermate DIM/BRIGHT/NIGHT_PEEK/CHARGING/LOW_BATT/TIME_NOT_SET/SENSOR_ERROR e flusso di impostazione ora/fascia notte.
- Screenshot dal display fisico verificati, non soltanto render di marketing.
