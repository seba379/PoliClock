# 00 — Visione, scopo e perimetro

**Versione:** 0.1 · **Stato:** specifica preliminare · **Data:** 2026-11-07

## 1. Scopo

Realizzare un orologio da scrivania originale, affettivo e quotidianamente utile come regalo per una persona che lavora nella Polizia. La forma fisica è una **poliziotta chibi stampata in 3D**, con proporzioni da statuetta da collezione e **display circolare inserito nel volto**. La qualità dell'oggetto, della leggibilità e della finitura è tanto importante quanto il firmware.

## 2. Proposta di valore

1. **Personalità**: un personaggio riconoscibile e simpatico, non un comune orologio da tavolo.
2. **Semplicità**: quattro informazioni immediatamente leggibili, senza navigazione obbligatoria.
3. **Libertà di posizionamento**: batteria ricaricabile; nessun cavo necessario durante l'utilizzo normale.
4. **Manutenzione**: accesso posteriore alla ricarica e ai componenti senza rompere la stampa.
5. **Autonomia ragionevole**: modalità ibrida luminosità ridotta/intensa, con consumi da misurare.

## 3. Utilizzo di riferimento

- Su scrivania, comodino o mensola, in ambiente interno.
- Funzionamento statico su superficie piana, senza connessione USB permanente.
- Dopo il tocco/interazione, il quadrante si illumina, poi torna allo stato attenuato.
- Di notte il display è spento (modalità notte); un tocco permette di leggere l'ora.
- Ricarica circa ogni 2 giorni, oppure uso con USB collegata sulla scrivania.
- L'orologio funziona interamente offline (nessun Wi-Fi in V1): ora da RTC, misure ambientali dal sensore locale.
- Quando la batteria è quasi scarica, si riceve un'indicazione chiara prima dell'eventuale spegnimento controllato.

## 4. Perimetro funzionale V1 (CONF)

- Ora in formato `HH:MM` 24h.
- Data italiana, giorno della settimana e giorno/mese.
- Temperatura in °C rilevata localmente.
- Umidità relativa in %RH rilevata localmente.
- Ricarica via USB-C nella parte posteriore.
- Gestione batteria e schermata a luminosità ibrida.
- Modalità notte con display spento.
- Impostazione dell'ora offline (touch o USB).

## 5. Fuori perimetro V1

- Wi-Fi, sincronizzazione NTP, meteo via Internet, previsioni e servizi cloud.
- Domotica, notifiche smartphone, contapassi, audio e assistenti vocali.
- GPS e geolocalizzazione.
- App companion Bluetooth, OTA, dashboard statistiche e sensore CO₂.
- PCB proprietario dedicato alla prima iterazione.
- Repliche necessariamente identiche di distintivi o marchi ufficiali.

Queste funzioni **non sono requisiti mascherati**: possono essere considerate in una V2 senza compromettere la V1.

## 6. Vincoli progettuali

| ID | Vincolo | Stato |
|---|---|---|
| `SC-001` | Il display dev'essere circolare e sostituire il volto della statuetta | CONF |
| `SC-002` | Lo stile estetico dev'essere poliziotta chibi/stilizzata | CONF |
| `SC-003` | Funzionamento autonomo a batteria, ricarica USB-C posteriore | CONF |
| `SC-004` | Display attenuato in standby e temporaneamente più luminoso dopo interazione; spento di notte | CONF |
| `SC-005` | Scheda elettronica, batteria, connettori e sensore devono essere accessibili senza danneggiare la statuetta | CAND |
| `SC-006` | Altezza complessiva indicativa 130–160 mm; da rivedere in CAD | CAND |
| `SC-007` | Utilizzo per interni e non per ambienti bagnati o esposti al sole diretto | CAND |

## 7. Definizione di 'prototipo V1 riuscito'

Il prototipo è accettabile quando: tutte e quattro le informazioni sono corrette e leggibili; il display è fisicamente integrato nella testa; la batteria alimenta l'insieme; la USB-C posteriore ricarica in sicurezza; la meccanica è stabile e accessibile; i consumi e la temperatura del dispositivo sono stati misurati; i test critici di [verifica](07-piano-verifica.md) sono superati.

## 8. Gestione del cambiamento

Una modifica è *di perimetro* se introduce nuove funzioni, un diverso display, un'altra chimica di batteria, un circuito di carica diverso o un'altra geometria di testa. Documentarla in [decision log](10-decisioni-aperte.md), valutarne impatto su consumi/cablaggio/CAD/firmware e aggiornare requisito e test corrispondenti.
