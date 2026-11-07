# 09 — Roadmap di realizzazione

**Versione:** 0.1 · **Stato:** pianificazione per milestone, nessuna data promessa · **Data:** 2026-11-07

## Premessa

Le milestone sono **gate tecnici**, non stime temporali. Il prototipo deve evolvere da specifiche a prove di banco, poi a CAD, e solo infine a regalo finito. Un'eventuale richiesta estetica che modifica il vano testa o batteria deve essere valutata prima di stampare i componenti definitivi.

## M0 — Baseline documentale

**Output:** README, PRD, architettura candidata, specifica alimentazione, UI, meccanica, test plan, BOM, decision log.

**Criterio d'uscita:** tutte le decisioni confermate rappresentate; le incognite (`TBD`) identificate; nessuna BOM spacciata per acquistata. **Stato V0.1: documenti iniziali creati; approvazione del proprietario non ancora espressa.**

## M1 — Acquisto e validazione hardware da banco

**Input:** BOM-001…004 e documentazione ufficiale.

Attività:

1. Verificare schematico, tavola dimensionale e pinout effettivi del modulo Waveshare.
2. Selezionare LiPo protetta, misurarne ingombri e verificare connettore/polarità.
3. Collegare e leggere SHT40 senza conflitti sul bus.
4. Verificare display, touch, RTC e stato batteria PMU.
5. Misurare i consumi preliminari in DIM/BRIGHT e ricarica USB; registrare picchi e medie.

**Exit gate:** evidenza di bring-up, letture sensore valide, alimentazione e ricarica sicure; scheda e batteria **approvate o scartate** con motivazione.

## M2 — Firmware minimo affidabile

**Output:** progetto ESP-IDF versionato, BSP, RTC/setting ora offline, SHT40, UI principale, FSM DIM/BRIGHT, test unitari.

**Exit gate:** test `VT-FUN-001`, `VT-FUN-002`, `VT-FW-001`, `VT-FW-003`, `VT-UI-001` superati su hardware reale. Niente dipendenza di boot dal Wi-Fi.

## M3 — Ottimizzazione energetica e ricarica

**Output:** driver PMU, batteria low/critical, misurazione autonomia, profili energetici e rapporto termico su prototipo aperto.

**Exit gate:** test `VT-PWR-001`…`VT-PWR-004` eseguiti, autonomia reale documentata, decisione esplicita su target 48 h; nessun problema di ricarica da ignorare.

> Non far precedere la chiusura definitiva della scocca alla validazione elettrica della batteria.

## M4 — CAD e stampa 3D funzionale

**Output:** modello parametrico diviso in gusci, supporto display, vano batteria, supporto USB-C, alloggiamento sensore, sportello di servizio, prove di stampa.

**Exit gate:** test `VT-MEC-001`…`VT-MEC-004` superati su prototipo funzionale. La testa deve contenere realmente il display, senza pressioni sul vetro.

## M5 — Integrazione, finitura e regalo

**Output:** statuetta colorata/verniciata, componenti montati, cablaggi ordinati, firmware release, guida operativa breve, registro prove finale.

**Exit gate:** tutti i `MUST` approvati, prove di carica e calore completate con scocca chiusa, nessun test di sicurezza aperto, autonomia comunicata in modo corretto (misurata, non stimata).

## Backlog prioritizzato

| Priorità | Attività | Dipendenza |
|---|---|---|
| P0 | Verificare dimensioni e pinout modulo Waveshare reale | M1 acquisto |
| P0 | Verificare compatibilità PMU/batteria e protezioni | Datasheet cella + schema board |
| P0 | Misurare consumo AMOLED in DIM con ora visibile | Bring-up display |
| P0 | Implementare ora e impostazione offline | RTC funzionante |
| P0 | Posizionare SHT40 lontano dal calore | Misure termiche |
| P1 | Stabilire parametri luminosità e timeout | Test leggibilità/consumo |
| P1 | Realizzare head mount e vano USB-C | Dimensioni fisiche validate |
| P1 | Test 48 h e valutazione capacità batteria | Power manager stabile |
| P2 | Animazioni/transizioni UI | Dopo autonomia convalidata |
| P2 | Alternative estetiche (capelli, posa, colori) | Dopo CAD funzionale |

## Principali rischi e mitigazioni

| Rischio | Impatto | Mitigazione |
|---|---|---|
| Autonomia insufficiente con AMOLED acceso | Alto | Misurare DIM prima del CAD; modificare luminanza, radio, batteria o display |
| Ingombro modulo superiore alla testa desiderata | Alto | Disegno ufficiale + misure fisiche prima della stampa definitiva |
| SHT40 riscaldato internamente | Medio/alto | Vano ventilato e test comparativi a ricarica attiva |
| Batteria incompatibile o carica non sicura | Critico | Datasheet, controllo polarità/limiti e gate safety prima di alimentare |
| USB-C posteriore scomoda o fragile | Medio | Staffa, strain relief e prova con diversi cavi |
| RTC non impostabile offline | Medio | Menu touch o provisioning USB nella V1 |
| Burn-in AMOLED per quadrante statico | Medio | Fondo nero, bassa luminanza, minimo spostamento periodico elementi |

## Politica di milestone

Se un gate di sicurezza fallisce, la milestone successiva non parte come se nulla fosse. Un'eventuale modifica dell'obiettivo di autonomia è una decisione documentata e non un miglioramento cosmetico delle specifiche.
