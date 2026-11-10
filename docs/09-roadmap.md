# 09 — Roadmap di realizzazione

**Versione:** 0.7 · **Stato:** pianificazione per milestone, nessuna data promessa · **Data:** 2026-11-07

## Premessa

Le milestone sono **gate tecnici**, non stime temporali. Il percorso è: specifiche → prototipo su banco con moduli e bozza CAD a volumi → PCB custom → firmware → alimentazione e temperature → CAD definitivo → regalo finito. Un'eventuale richiesta estetica che modifica la testa o la base deve essere valutata prima di stampare i componenti definitivi.

La V1 è alimentata **solo da USB** (`DEC-023`): le attività di batteria, ricarica e autonomia sono state rimosse.

## M0 — Baseline documentale

**Output:** README, PRD, architettura, alimentazione, UI, meccanica, test plan, BOM, decision log.

**Criterio d'uscita:** tutte le decisioni confermate rappresentate; incognite (`TBD`) identificate; nessuna BOM spacciata per acquistata. **Stato: specifiche riviste e decisioni `DEC-001`…`DEC-023` registrate.**

## M1 — Prototipo su banco con moduli

**Input:** `PRO-001`…`PRO-008` ([BOM](08-bom-preliminare.md)).

Attività:

1. Scegliere MCU (ESP32-C3 o S3), RTC e tampone, regolatore 3,3 V sui datasheet.
2. Montare su breadboard dev board, display GC9A01, RTC, SHT40 e pulsante.
3. Verificare flash e log USB; collegare il display con un **cavo di lunghezza reale** e trovare la frequenza SPI stabile (`OPEN-021`).
4. Firmware di bring-up: display (modulo a 7 pin, `DEC-034`), pulsante, RTC, SHT40.
5. Primo protocollo del configuratore e prova di sincronizzazione dell'ora dal PC.
6. Misurare la corrente USB in DIM/BRIGHT/NIGHT (compresa la corrente del modulo display) e la durata del tampone RTC a cavo scollegato.
7. **Bozza a volumi in Blender** con le misure reali di display e ingombro stimato della scheda: decidere la posizione della scheda principale, il percorso del cavo display e l'uscita del cavo USB (`OPEN-020`). **Fatto in bozza il 2026-11-09**: scheda nella base (`DEC-048`), studio build123d e blockout Blender in [06](06-progettazione-meccanica.md) §12.

**Exit gate:** architettura confermata con misure; componenti del PCB scelti con motivazione; posizione della scheda principale decisa.

## M2 — Progettazione PCB (KiCad)

**Output:** progetto KiCad 10 versionato in `hardware/`: schema e layout della scheda principale (unico PCB custom dopo `DEC-034`), BOM e file di posizionamento per JLC, STEP per il CAD, checklist di revisione compilata. Schema e layout preparati da Claude, rivisti a vista dal proprietario in KiCad.

**Stato (2026-11-07):** schema e PCB rev 0.2 della scheda principale (50 × 40 mm, 2 strati, un lato; dal 2026-11-08 50,5 × 41,5 mm senza intaglio, `DEC-045`) dopo la revisione tecnica indipendente, posizionati e sbrogliati in bozza con report ERC/DRC salvati ([hardware](../hardware/README.md), [02](02-architettura-hardware.md) §3.2, [12](12-selezione-componenti.md)). Il 2026-11-08 è stata fatta una revisione con Codex; Claude l'ha verificata ([docs/10](10-decisioni-aperte.md) §7–8): corretti la distanza dal bordo e i courtyard; chiusi poi lo spunto all'ingresso USB (`DEC-042`), il controllo DRC in `esporta.py`, l'allineamento delle specifiche firmware/UI a `DEC-034`, i cartigli e i residui storici. Restano inoltre: studio volumetrico 1:1 (`OPEN-028`), verifica del modulo display ricevuto (`OPEN-016`), prototipo M1 e DFM JLC. La **revisione visiva del proprietario** in KiCad è stata fatta il 2026-11-08 ed è positiva (`OPEN-027` chiusa). Nessun test hardware eseguito.

**Exit gate:** `VT-PCB-001` superato (ERC/DRC puliti, revisione schema, disponibilità LCSC, quote compatibili con il CAD); preventivo JLC accettato.

## M3 — Ordine e bring-up PCB

**Output:** PCB assemblati, report di bring-up.

**Exit gate:** `VT-PCB-002` e `VT-PCB-003` superati (alimentazione, USB, flash, display sul cavo reale, pulsante, I²C). Errori bloccanti → revisione PCB documentata prima di proseguire.

## M4 — Firmware minimo affidabile

**Output:** progetto ESP-IDF versionato, BSP del PCB, RTC, SHT40, UI principale, FSM DIM/BRIGHT/NIGHT, protocollo del configuratore, **configuratore da PC** (`tools/configurator/`), menu pulsante di riserva, test unitari.

**Exit gate:** `VT-FUN-001`, `VT-FUN-002`, `VT-FUN-003`, `VT-FW-001`, `VT-FW-002`, `VT-FW-003`, `VT-FW-006`, `VT-FW-007`, `VT-UI-001`, `VT-UI-003` superati su hardware reale. Nessuna radio inizializzata (`DEC-012`).

## M5 — Alimentazione e temperature

**Output:** misure di corrente, durata del tampone RTC, rapporto termico in funzionamento continuo.

**Exit gate:** `VT-PWR-001`…`VT-PWR-004` superati.

## M6 — CAD e stampa 3D funzionale

**Output:** modello parametrico diviso in gusci, supporto del modulo display, supporto della scheda principale nella base con la USB-C sul retro (`DEC-048`), uscita guidata del cavo, zavorra nella base, alloggiamento sensore, pulsante, sportello di servizio, prove di stampa.

**Exit gate:** `VT-MEC-001`…`VT-MEC-004` superati su prototipo funzionale.

## M7 — Integrazione, finitura e regalo

**Output:** statuetta colorata/verniciata, componenti montati, cablaggi ordinati, firmware release, alimentatore e cavo USB-C abbinati, guida operativa breve, registro prove finale.

**Exit gate:** tutti i `MUST` approvati, prove termiche a scocca chiusa completate, nessun test di sicurezza aperto.

## Backlog prioritizzato

| Priorità | Attività | Dipendenza |
|---|---|---|
| P0 | Ricevere il modulo GC9A01 a 7 pin e verificarne pinout e corrente (`OPEN-016`, `DEC-034`) | Fornitore |
| P1 | Verificare la durata del tampone RTC (DS3231 con CR1220, `DEC-024`, `OPEN-014`) | Prototipo M1 |
| P0 | Bozza Blender a volumi e posizione della scheda principale | Misure display, scheda |
| P0 | Implementare ora e impostazione offline | RTC funzionante |
| P0 | Posizionare SHT40 lontano dal calore | Misure termiche |
| P1 | Posizione del pulsante nella statuetta | Concept CAD |
| P1 | Stabilire palette DIM/BRIGHT e timeout (solo grafica, `DEC-034`) | Test leggibilità |
| P1 | Uscita del cavo USB e stabilità con zavorra | Quote CAD |
| P1 | Misurare spunto USB all'inserzione e transitori del modulo display (`OPEN-029`, `VT-PWR-001/003`) | PCB assemblato |
| P2 | Animazioni/transizioni UI | Dopo firmware stabile |
| P2 | Alternative estetiche (capelli, posa, colori) | Dopo CAD funzionale |
| V2 | Se si attiva la radio: allontanare di almeno 1–2 mm le piste dal bordo della zona antenna di U3 (LCD_CS oggi a 0,3–0,4 mm), rivalutare +3V3/EN sotto il modulo, il piano GND e la cucitura vicino all'antenna (R2-004) | Decisione di riattivare Wi-Fi/BLE (oggi `DEC-012`) |

## Principali rischi e mitigazioni

| Rischio | Impatto | Mitigazione |
|---|---|---|
| Errore nel PCB che richiede una seconda revisione | Alto | Prototipo M1, checklist di revisione, punti di test, 0 Ω per isolare blocchi |
| Costo del PCB custom superiore alle attese | Medio | Preventivo completo prima dell'ordine; parti "basic"; piano B scheda pronta |
| Modulo display senza documentazione affidabile | Medio | Pinout dalla serigrafia del modulo ricevuto, verifica su banco prima di collegarlo a J2 (`OPEN-016`) |
| Scheda principale non entra nel busto | Medio | Bozza CAD in M1; opzione B con scheda nella testa e prolunga |
| Display instabile sul cavo nel collo | Medio | Frequenza SPI ridotta, R8/R9 22 Ω in serie, cavetto corto, prova `VT-PCB-003` (`OPEN-021`) |
| SHT40 riscaldato dal calore interno permanente | Medio/alto | Vano ventilato e lontano da LDO e display, test comparativi a regime (la retroilluminazione è fissa, `DEC-034`) |
| Statuetta instabile con il cavo sempre inserito | Medio | Uscita guidata nella base, zavorra, cavo flessibile |
| USB-C posteriore fragile | Medio | Scheda avvitata alla scocca, prova con diversi cavi |
| Ora persa con cavo scollegato a lungo | Basso | Tampone RTC dimensionato; configuratore per reimpostarla |
| Impostazione ora scomoda con un solo pulsante | Basso | Configuratore da PC come metodo principale (`OPEN-015`) |

## Politica di milestone

Se un gate di sicurezza fallisce, la milestone successiva non parte come se nulla fosse. Un'eventuale reintroduzione della batteria è una decisione di perimetro documentata.
