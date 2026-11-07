# PoliClock

**Orologio da scrivania ricaricabile, integrato nel volto di una poliziotta chibi stampata in 3D.**

> Stato: **concept / specifiche preliminari (v0.3)** · Aggiornamento: 2026-11-07\
> Lingua progetto: italiano · Documentazione in Markdown · Hardware non ancora acquistato né validato.

## Il prodotto

PoliClock è un regalo personalizzato: una statuetta simpatica e stilizzata di una poliziotta, con un display **circolare integrato al posto del volto**. Durante il giorno il quadrante visualizza **ora, data, temperatura ambiente e umidità relativa**; di notte può spegnersi. È alimentato da **batteria ricaricabile**, con **USB-C sulla parte posteriore bassa** della statuetta (sul sedere, per ironia).

La modalità scelta è **ibrida**: quadrante normalmente attenuato ma leggibile; la pressione di un pulsante attiva temporaneamente la luminosità elevata. La priorità è la qualità estetica senza sacrificare sicurezza, autonomia e manutenzione.

## Decisioni già confermate

- Statuetta **poliziotta chibi**, volutamente sproporzionata, da stampare in 3D.
- Display **rotondo**, montato a filo/in incasso al posto del viso; non esterno o incollato.
- Schermata V1: **ora, data, temperatura e umidità**; niente funzioni domotiche o statistiche richieste.
- Funzionamento **a batteria**, con ricarica **USB-C** sulla parte posteriore bassa, collegata al PCB con prolunga.
- Schermo **attenuato in condizioni normali**, più luminoso dopo un'interazione.
- **Di notte il display è spento** (default 23:00–07:00, configurabile).
- Aspetto con **uniforme blu e cappello**.
- Ricarica circa **ogni 2 giorni** accettabile, così come l'uso frequente con USB collegata.
- **Nessun Wi-Fi/NTP nella V1**: l'ora si imposta offline.
- Elettronica su **PCB custom** (KiCad, prodotto e assemblato da JLCPCB).
- Display **IPS rotondo 1,28"** (240×240, GC9A01) e interazione con un **pulsante** fisico.

## Architettura candidata, NON ancora congelata

- PCB custom rotondo nella testa: modulo **ESP32-C3** (o S3), caricatore con power-path e NTC, regolatore 3,3 V, **RTC esterno con tampone**, USB-C, connettori.
- Sensore T/RH: **Sensirion SHT40** su mini-PCB, in vano ventilato, collegato con 4 fili.
- Batteria: **LiPo 1S protetta**, preferibilmente con NTC, 2.500–3.000 mAh da rivedere sui consumi misurati.
- Prima del PCB: **prototipo su banco** con moduli commerciali per validare consumi, ricarica e firmware.
- Firmware **ESP-IDF**.

**Importante:** il requisito di autonomia di **48 ore** è un *target di progettazione* non una prestazione dimostrata. La corrente media, la compatibilità della batteria, le impostazioni di ricarica e gli ingombri vanno misurati prima di consolidare la BOM.

## Documentazione

| Documento | Contenuto |
|---|---|
| [Visione e perimetro](docs/00-visione-perimetro.md) | Scopo, utenti, esclusioni, vincoli |
| [Requisiti di prodotto](docs/01-requisiti-prodotto.md) | Requisiti identificati, criteri di accettazione |
| [Architettura hardware](docs/02-architettura-hardware.md) | Moduli, collegamenti, selezione candidata |
| [Alimentazione e ricarica](docs/03-alimentazione-ricarica.md) | Batteria, USB-C, consumi, safety |
| [Specifiche firmware](docs/04-specifiche-firmware.md) | Componenti, stati, timekeeping, errori |
| [UI/UX](docs/05-interfaccia-utente.md) | Layout, luminosità, interazione, messaggi |
| [Progettazione meccanica](docs/06-progettazione-meccanica.md) | Testa, corpo, vano batteria, stampa 3D |
| [Verifiche e test](docs/07-piano-verifica.md) | Prove funzionali, elettriche e meccaniche |
| [BOM preliminare](docs/08-bom-preliminare.md) | Acquisti, alternative e controlli pre-ordine |
| [Roadmap](docs/09-roadmap.md) | Milestone, deliverable, gate |
| [Decisioni e questioni aperte](docs/10-decisioni-aperte.md) | Decision log e dubbi tecnici |
| [Fonti](docs/11-fonti.md) | Documenti ufficiali e risorse tecniche |

## Organizzazione di lavoro prevista

```text
PoliClock/
├── README.md
├── docs/                  # specifiche e verifiche
├── assets/                # concept, render, modelli di riferimento futuri
├── firmware/              # progetto ESP-IDF da avviare in M1/M4
├── hardware/              # progetto KiCad del PCB, BOM e file JLCPCB (M2)
└── mechanical/            # CAD, STL/3MF e tavole tecniche
```

Le ultime tre directory sono **previste**, non ancora presenti: non si pubblicano file placeholder che possano essere scambiati per firmware o modelli funzionanti.

## Convenzioni

- **CONF**: decisione espressamente confermata dall'utente.
- **CAND**: soluzione tecnica candidata, soggetta a verifica.
- **TGT**: obiettivo di progetto non ancora validato.
- **TBD**: scelta/misura ancora da definire.
- Ogni requisito ha un ID stabile (es. `PR-FUN-001`) e uno o più test di accettazione (`VT-...`).
- Nessun dato prestazionale ipotetico va descritto come misurato.

## Primo passo operativo

Milestone M1 della [roadmap](docs/09-roadmap.md): scegliere sui datasheet MCU, caricatore, RTC e cella, montare il **prototipo su banco** con moduli commerciali e misurare consumi e ricarica **prima** di disegnare il PCB e il CAD.

## Avvertenze

Progetto hobbistico per un regalo personale, non prodotto certificato per vendita. L'integrazione di una cella al litio richiede adeguata protezione elettrica, isolamento, fissaggio meccanico e verifica termica. L'estetica richiama una poliziotta, senza implicare affiliazione o approvazione ufficiale della Polizia di Stato.
