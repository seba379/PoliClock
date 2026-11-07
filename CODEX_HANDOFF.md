# Passaggio operativo a Codex - PoliClock

**Data del pacchetto:** 2026-11-07\
**Fase:** inizializzazione repository e baseline documentale v0.1 (M0)\
**Repository di destinazione:** https://github.com/seba379/PoliClock\
**Branch di riferimento storico:** `main` (ricontrollare prima di agire)

## Scopo di questo passaggio

Pubblicare nel repository la documentazione tecnica in questo pacchetto, verificandone consistenza e integrita'. Non serve implementare il firmware, progettare un PCB, acquistare componenti, creare schemi definitivi o generare modelli CAD in questo passaggio.

Il precedente tentativo di push da ChatGPT non e' riuscito per un problema del collegamento GitHub (`link_id must identify an eligible linked account`). I file sono stati preparati localmente e inseriti in questo ZIP. **Non presumere che siano gia' su GitHub.**

## Checklist operativa (nell'ordine)

1. Apri/clona `seba379/PoliClock` con le credenziali GitHub disponibili nel tuo ambiente. Verifica remote, branch predefinito, `git status` e i file gia' presenti. Il repository risultava vuoto alla verifica iniziale, ma potrebbe essere cambiato.
2. Estrai o integra **il contenuto di questo archivio nella root** del clone. Il pacchetto e' root-relative (contiene `README.md`, `AGENTS.md`, `CODEX_HANDOFF.md`, `docs/`, `assets/`, `.gitignore`). Evita cartelle annidate accidentalmente (`PoliClock/PoliClock/`).
3. Non sovrascrivere lavoro remoto o locale esistente. Se il repository non e' vuoto, confronta prima di applicare modifiche; in caso di conflitti crea branch `docs/initial-specifications-v0.1` e apri una PR invece di forzare `main`.
4. Leggi `README.md`, `AGENTS.md` e `docs/10-decisioni-aperte.md`; controlla che tutti i requisiti **CONF** siano preservati e che le scelte **CAND** non siano descritte come definitive.
5. Controlla che esistano tutti i documenti `docs/00` ... `docs/11`; verifica link Markdown relativi, riferimenti a test/requisiti, formattazione (`git diff --check`) e presenza di eventuali segreti prima del commit. L'immagine in `assets/concept/` e' solo un riferimento estetico: contiene elementi non appartenenti alla V1; vedi README nella cartella.
6. Effettua un commit descrittivo, ad esempio `docs: bootstrap PoliClock product specifications v0.1`.
7. Effettua push del branch corretto, **solo dopo** avere verificato che il delta contenga esclusivamente i file previsti. Se e' un branch separato, apri una PR. Non effettuare force push.
8. Comunica il risultato verificato: URL repository, branch, commit SHA o URL PR, numero di file aggiunti/modificati, esito validazioni e problemi residui.

## Vincoli di prodotto - decisioni confermate

- Statuetta stampata in 3D: **poliziotta stilizzata/chibi**, testa sproporzionata.
- Display **circolare integrato al posto del volto**.
- V1: visualizzare **ora, data, temperatura e umidita'**.
- Alimentazione a **batteria ricaricabile**; ingresso di ricarica USB sulla schiena, preferibilmente USB-C.
- Modalita' **ibrida**: schermata normalmente attenuata e leggibile, temporaneamente luminosa dopo interazione.

## Scelte ancora candidate / punti da NON spacciar per validati

- Board suggerita: Waveshare ESP32-S3-Touch-AMOLED-1.75 standard, non obbligatoria; verificare SKU, revisione, quote, pin, interfacce, consumi.
- SHT40 come sensore ambientale esterno; posizionamento in zona ventilata e lontana da sorgenti termiche.
- Cella LiPo 1S protetta da circa 2.500-3.000 mAh; protezione, polarita', connettore, limiti PMU, corrente di ricarica e collocazione devono essere validati.
- Firmware candidato: ESP-IDF, da avviare dopo bring-up hardware.
- **48 ore** di autonomia: target da misurare, non promessa di prestazione.
- Timeout bright di circa **20 secondi**: proposta da validare per usabilita' ed energia.

## Contenuto di consegna

- `README.md`: indice e sintesi progettuale.
- `AGENTS.md`: regole operative per gli agenti che lavorano nel repository.
- `docs/00` ... `docs/11`: specifiche, requisiti tracciati, firmware, energia, UI, meccanica, verifiche, distinta base, roadmap, decision log e fonti.
- `assets/concept/policlock-chibi-concept.png`: immagine generata a scopo illustrativo, non da trattare come disegno tecnico.
- `assets/README.md`, `.gitignore`.

## Fase successiva (non eseguire automaticamente durante questo handoff)

Milestone **M1**: studio delle risorse tecniche e selezione/bring-up hardware; solo dopo passare al firmware ESP-IDF e alla progettazione CAD quotata. Prima dell'acquisto devono essere verificati dimensioni fisiche della board, pin I2C disponibili, batteria e protezioni e fattibilita' del target di autonomia.

## Prompt breve da usare se alleghi lo ZIP a Codex

> Ti allego l'archivio PoliClock con documentazione v0.1. Apri il repository `https://github.com/seba379/PoliClock`, leggi `CODEX_HANDOFF.md` e `AGENTS.md`, confronta lo stato remoto e pubblica la baseline documentale seguendo la checklist. Non sovrascrivere lavoro esistente e non inventare caratteristiche hardware non validate. Dopo il push, comunicami branch, SHA e controlli effettuati.
