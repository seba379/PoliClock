# 09 — Roadmap di realizzazione

**Versione:** 0.4 · **Stato:** pianificazione per milestone, nessuna data promessa · **Data:** 2026-11-07

## Premessa

Le milestone sono **gate tecnici**, non stime temporali. Il percorso è: specifiche → prototipo su banco con moduli e bozza CAD a volumi → PCB custom → firmware → energia → CAD definitivo → regalo finito. Un'eventuale richiesta estetica che modifica il vano testa o batteria deve essere valutata prima di stampare i componenti definitivi.

## M0 — Baseline documentale

**Output:** README, PRD, architettura, alimentazione, UI, meccanica, test plan, BOM, decision log.

**Criterio d'uscita:** tutte le decisioni confermate rappresentate; incognite (`TBD`) identificate; nessuna BOM spacciata per acquistata. **Stato: specifiche riviste e decisioni `DEC-001`…`DEC-018` registrate.**

## M1 — Prototipo su banco con moduli

**Input:** `PRO-001`…`PRO-007` ([BOM](08-bom-preliminare.md)), LiPo candidata.

Attività:

1. Scegliere MCU (ESP32-C3 o S3), caricatore, RTC, regolatore e misura batteria sui datasheet.
2. Montare su breadboard dev board, display GC9A01, caricatore, RTC, SHT40 e pulsante.
3. Verificare flash e log USB; collegare il display con un **cavo di lunghezza reale** e trovare la frequenza SPI stabile (`OPEN-021`).
4. Firmware di bring-up: display, pulsante, touch del modulo, RTC, SHT40, light-sleep.
5. Primo protocollo del configuratore e prova di sincronizzazione dell'ora dal PC.
6. Misurare i consumi in DIM/BRIGHT/NIGHT e in ricarica (con e senza controller touch attivo); registrare picchi e medie.
7. Provare carica, power-path e cutoff NTC del caricatore con la cella scelta.
8. **Bozza a volumi in Blender** con le misure reali di cella, display e ingombro stimato della scheda: decidere la posizione della scheda principale e se serve la prolunga (`OPEN-020`).

**Exit gate:** architettura confermata con misure; componenti del PCB scelti con motivazione; cella approvata o scartata; posizione della scheda principale decisa.

## M2 — Progettazione PCB (KiCad)

**Output:** progetto KiCad 10 versionato in `hardware/`: schema e layout di scheda principale, schedina portadisplay e mini-PCB SHT40 in un pannello unico, BOM e file di posizionamento per JLC, STEP per il CAD, checklist di revisione compilata. Schema e layout preparati da Claude, rivisti a vista dal proprietario in KiCad.

**Exit gate:** `VT-PCB-001` superato (ERC/DRC puliti, revisione schema, disponibilità LCSC, quote compatibili con la testa); preventivo JLC accettato.

## M3 — Ordine e bring-up PCB

**Output:** PCB assemblati, report di bring-up.

**Exit gate:** `VT-PCB-002` e `VT-PCB-003` superati (alimentazioni, USB, flash, display sul cavo reale, pulsante, I²C). Errori bloccanti → revisione PCB documentata prima di proseguire.

## M4 — Firmware minimo affidabile

**Output:** progetto ESP-IDF versionato, BSP del PCB, RTC, SHT40, UI principale, FSM DIM/BRIGHT/NIGHT, protocollo del configuratore, **configuratore da PC** (`tools/configurator/`), menu pulsante di riserva, test unitari.

**Exit gate:** `VT-FUN-001`, `VT-FUN-002`, `VT-FW-001`, `VT-FW-002`, `VT-FW-003`, `VT-FW-006`, `VT-FW-007`, `VT-UI-001`, `VT-UI-003` superati su hardware reale. Nessuna radio inizializzata (`DEC-012`).

## M5 — Energia e ricarica

**Output:** gestione batteria low/critical, misurazione autonomia, rapporto termico su prototipo aperto.

**Exit gate:** `VT-PWR-001`…`VT-PWR-004` eseguiti, autonomia reale documentata, decisione esplicita su target 48 h.

> Non far precedere la chiusura definitiva della scocca alla validazione elettrica della batteria.

## M6 — CAD e stampa 3D funzionale

**Output:** modello parametrico diviso in gusci, supporto display/PCB, vano batteria, staffa USB-C posteriore bassa, alloggiamento sensore, pulsante, sportello di servizio, prove di stampa.

**Exit gate:** `VT-MEC-001`…`VT-MEC-004` superati su prototipo funzionale.

## M7 — Integrazione, finitura e regalo

**Output:** statuetta colorata/verniciata, componenti montati, cablaggi ordinati, firmware release, guida operativa breve, registro prove finale.

**Exit gate:** tutti i `MUST` approvati, prove di carica e calore completate con scocca chiusa, nessun test di sicurezza aperto, autonomia comunicata come misurata.

## Backlog prioritizzato

| Priorità | Attività | Dipendenza |
|---|---|---|
| P0 | Scegliere la cella LiPo (dimensioni, NTC, connettore) | Datasheet |
| P0 | Scegliere caricatore power-path + NTC e provarlo su banco | M1 |
| P0 | Trovare pannello GC9A01 con datasheet e pinout FPC | Fornitore |
| P0 | Misurare consumo IPS in DIM e NIGHT | M1 |
| P0 | Implementare ora e impostazione offline | RTC funzionante |
| P0 | Posizionare SHT40 lontano dal calore | Misure termiche |
| P1 | Posizione del pulsante nella statuetta | Concept CAD |
| P1 | Stabilire parametri luminosità e timeout | Test leggibilità/consumo |
| P0 | Bozza Blender a volumi e posizione della scheda principale | Misure cella, display, scheda |
| P1 | Fissaggio scheda/USB-C sul sedere (o staffa prolunga) | Quote CAD |
| P1 | Test 48 h e valutazione capacità batteria | Firmware energia stabile |
| P2 | Animazioni/transizioni UI | Dopo autonomia convalidata |
| P2 | Alternative estetiche (capelli, posa, colori) | Dopo CAD funzionale |

## Principali rischi e mitigazioni

| Rischio | Impatto | Mitigazione |
|---|---|---|
| Errore nel PCB che richiede una seconda revisione | Alto | Prototipo M1, checklist di revisione, punti di test, 0 Ω per isolare blocchi |
| Costo del PCB custom superiore alle attese | Medio | Preventivo completo prima dell'ordine; parti "basic"; piano B scheda pronta |
| Ricarica non sicura (progetto nostro) | Critico | Caricatore con NTC e power-path, prove su banco, gate di sicurezza |
| Autonomia insufficiente per retroilluminazione | Alto | Misurare DIM su banco in M1; regolare PWM, notte, capacità cella |
| Pannello display senza documentazione affidabile | Alto | Acquistare solo pannelli con datasheet e pinout FPC |
| Scheda principale e cella non entrano nel busto | Alto | Bozza CAD in M1; opzione B con scheda nella testa e prolunga |
| Display instabile sul cavo nel collo | Medio | Frequenza SPI ridotta, masse alternate, prova `VT-PCB-003` |
| SHT40 riscaldato internamente | Medio/alto | Vano ventilato e test comparativi a ricarica attiva |
| USB-C posteriore scomoda o fragile | Medio | Staffa, fermacavo e prova con diversi cavi |
| Impostazione ora scomoda con un solo pulsante | Medio | Provisioning USB come metodo di riserva (`OPEN-015`) |

## Politica di milestone

Se un gate di sicurezza fallisce, la milestone successiva non parte come se nulla fosse. Un'eventuale modifica dell'obiettivo di autonomia è una decisione documentata e non un miglioramento cosmetico delle specifiche.
