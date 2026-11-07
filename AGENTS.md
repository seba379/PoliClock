# PoliClock - istruzioni per agenti di sviluppo

Queste istruzioni valgono per l'intero repository. Leggere `README.md` e i documenti in `docs/` prima di proporre o modificare l'architettura.

## Prodotto e perimetro

PoliClock V1 e' un orologio da scrivania a batteria, in una statuetta 3D di una poliziotta chibi. Il display rotondo coincide con il volto. Requisiti confermati: ora, data, temperatura, umidita', quadrante normalmente attenuato con luminosita' temporaneamente aumentata dopo interazione, display spento di notte, ricarica USB-C sul retro, uniforme blu e cappello. La V1 e' interamente offline: niente Wi-Fi/NTP. Non aggiungere domotica, CO2, meteo da Internet, audio o altre funzionalita' non richieste.

## Autorita' delle specifiche

- `CONF`: decisione del proprietario, da preservare.
- `CAND`: componente/proposta da verificare, NON scelta vincolante.
- `TGT`: obiettivo progettuale non ancora misurato (in particolare 48 ore di autonomia).
- `TBD`: informazione mancante, da verificare e documentare.
- La grafica in `assets/concept/` e' illustrativa: non e' una fonte per cablaggi, pinout, BOM, quote o funzionalita'.
- Registrare nuove decisioni in `docs/10-decisioni-aperte.md` e mantenere coerenti requisiti, verifiche, BOM e roadmap.

## Qualita' e sicurezza

- Preferire documentazione ufficiale del produttore, datasheet corretti per SKU/revisione e misure di banco; non inventare pinout, autonomia, soglie PMU o dimensioni.
- Batteria LiPo: non dare per scontata la compatibilita' con caricatore, connettore, polarita' e protezioni. Le verifiche di sicurezza precedono l'assemblaggio definitivo.
- Firmware futuro in ESP-IDF, architettura modulare, codice testabile, nessuna modifica al firmware senza richiesta esplicita.
- Per le sole modifiche documentali verificare collegamenti Markdown, coerenza dei riferimenti e `git diff --check`.
- Non pubblicare credenziali, file privati o asset di terzi privi di licenza verificata.

## Flusso Git

- Esaminare prima `git status`, remote, branch di default e contenuto esistente: non sovrascrivere modifiche dell'utente.
- Se il repository e' vuoto, effettuare un commit iniziale documentale sul branch di default (`main` se esistente). Se contiene gia' lavoro, integrare con prudenza; in caso di conflitto usare branch dedicato e PR.
- Riportare commit SHA e URL verificati dopo un push realmente riuscito; non affermare di aver pubblicato se l'autenticazione impedisce l'operazione.
