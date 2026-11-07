# 00 — Visione, scopo e perimetro

**Versione:** 0.5 · **Stato:** specifica preliminare · **Data:** 2026-11-07

## 1. Scopo

Realizzare un orologio da scrivania originale, affettivo e quotidianamente utile come regalo per una persona che lavora nella Polizia. La forma fisica è una **poliziotta chibi stampata in 3D**, con proporzioni da statuetta da collezione e **display circolare inserito nel volto**. La qualità dell'oggetto, della leggibilità e della finitura è tanto importante quanto il firmware.

## 2. Proposta di valore

1. **Personalità**: un personaggio riconoscibile e simpatico, non un comune orologio da tavolo.
2. **Semplicità**: quattro informazioni immediatamente leggibili, senza navigazione obbligatoria.
3. **Nessuna manutenzione energetica**: alimentato in continuo da USB, niente ricariche da ricordare (`DEC-023`).
4. **Manutenzione**: accesso posteriore ai componenti senza rompere la stampa.
5. **Ora sempre affidabile**: RTC con tampone, l'ora resta salva anche se il cavo viene staccato.

## 3. Utilizzo di riferimento

- Su scrivania, comodino o mensola, in ambiente interno, vicino a una presa o a un alimentatore USB.
- **Cavo USB-C sempre collegato** sul retro basso (sul sedere): senza cavo l'orologio è spento.
- Premendo il pulsante il quadrante si illumina, poi torna allo stato attenuato.
- Di notte il display è spento (modalità notte); una pressione del pulsante permette di leggere l'ora.
- Se si stacca il cavo (per spostarlo), al ricollegamento riparte con l'ora corretta grazie al tampone dell'RTC.
- L'orologio funziona interamente offline (nessun Wi-Fi in V1): ora da RTC, misure ambientali dal sensore locale.

## 4. Perimetro funzionale V1 (CONF)

- Ora in formato `HH:MM` 24h.
- Data italiana, giorno della settimana e giorno/mese.
- Temperatura in °C rilevata localmente.
- Umidità relativa in %RH rilevata localmente.
- **Alimentazione continua da USB-C** nella parte posteriore bassa (sul sedere), **senza batteria** (`DEC-023`).
- Schermata a luminosità ibrida e modalità notte con display spento.
- Impostazione dell'ora offline (configuratore da PC via USB, pulsante come riserva).
- Elettronica su PCB custom (KiCad, JLCPCB): scheda principale separata e collegata via cavo al display IPS rotondo 1,28".

## 5. Fuori perimetro V1

- **Batteria ricaricabile** e funzionamento senza cavo: rimandati a eventuali versioni successive (`DEC-023`).
- Wi-Fi, sincronizzazione NTP, meteo via Internet, previsioni e servizi cloud.
- Domotica, notifiche smartphone, contapassi, audio e assistenti vocali.
- GPS e geolocalizzazione.
- App companion Bluetooth, OTA, dashboard statistiche e sensore CO₂.
- Repliche necessariamente identiche di distintivi o marchi ufficiali.

Queste funzioni **non sono requisiti mascherati**: possono essere considerate in una V2 senza compromettere la V1.

## 6. Vincoli progettuali

| ID | Vincolo | Stato |
|---|---|---|
| `SC-001` | Il display dev'essere circolare e sostituire il volto della statuetta | CONF |
| `SC-002` | Lo stile estetico dev'essere poliziotta chibi/stilizzata | CONF |
| `SC-003` | Alimentazione continua da USB-C posteriore bassa (sul sedere), nessuna batteria in V1 (`DEC-023`) | CONF |
| `SC-004` | Display attenuato in standby e temporaneamente più luminoso dopo interazione; spento di notte | CONF |
| `SC-005` | Scheda elettronica, connettori e sensore devono essere accessibili senza danneggiare la statuetta | CAND |
| `SC-006` | Altezza complessiva indicativa 130–160 mm; da rivedere in CAD | CAND |
| `SC-007` | Utilizzo per interni e non per ambienti bagnati o esposti al sole diretto | CAND |

## 7. Definizione di 'prototipo V1 riuscito'

Il prototipo è accettabile quando: tutte e quattro le informazioni sono corrette e leggibili; il display è fisicamente integrato nella testa; l'alimentazione USB è stabile e protetta; l'ora sopravvive allo scollegamento del cavo; la statuetta è stabile con il cavo collegato; la meccanica è accessibile; consumi e temperature interne sono stati misurati; i test critici di [verifica](07-piano-verifica.md) sono superati.

## 8. Gestione del cambiamento

Una modifica è *di perimetro* se introduce nuove funzioni, un diverso display, una batteria, un'altra geometria di testa. Documentarla in [decision log](10-decisioni-aperte.md), valutarne impatto su consumi/cablaggio/CAD/firmware e aggiornare requisito e test corrispondenti.
