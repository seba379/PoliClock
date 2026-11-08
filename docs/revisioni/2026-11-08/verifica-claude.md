# Verifica indipendente delle correzioni Codex

Data: 2026-11-08. Oggetto: commit `16f9bf7` sul ramo `codex/pcb-edge-courtyard-fixes` ([revisione](README.md) e [correzioni](correzioni/README.md) preparate con Codex), confrontato con la base `4fb9200`. Verifica svolta da Claude (Claude Code) **senza modificare** schema, PCB, librerie o script. Nessun test su hardware fisico.

> **Aggiornamento dello stesso giorno:** su richiesta del proprietario sono stati poi chiusi anche REV-002 e REV-004…007. Vedi [§ Chiusura dei rilievi](#chiusura-dei-rilievi-2026-11-08). La tabella "Stato dei rilievi" qui sotto fotografa la situazione al momento della verifica.

## Esito

**Le correzioni REV-001 e REV-003 sono confermate.** Le modifiche al PCB sono esattamente quelle dichiarate, e i controlli automatici sono puliti anche rieseguiti in modo indipendente. Restano aperti i rilievi REV-002 e REV-004…007, tutti confermati come fondati. Si aggiunge un rilievo nuovo, VER-001: il testo di `DEC-040` non era allineato. È corretto con questa verifica.

## Controlli rieseguiti

| Controllo | Risultato |
|---|---|
| ERC, tutte le severità, codice d'uscita sulle violazioni | **0 violazioni** |
| DRC con zone ricalcolate (`--refill-zones`), tutte le severità e tutti gli errori delle piste, parità schema ↔ PCB | **0 violazioni, 0 non connessi, 0 problemi di parità**, 0 errori di footprint |
| `hardware/scripts/verifica_meccanica_pcb.py` | **PASS** (codice d'uscita 0) |
| Footprint, PCB 4fb9200 → 16f9bf7 | Spostati solo **C7** (y 102,25 → 103,00) e **FID1** (y 131,0 → 132,5); nessun altro componente spostato o ruotato |
| Rame, PCB 4fb9200 → 16f9bf7 | Cambiano solo segmenti delle reti `/MCU/EN` e `GND`; spostata una sola via EN, (134,037; 103,557) → (134,55; 103,25); vie totali 55 → 55, segmenti 530 → 537 |
| Coppia USB e reti CC/5V_LDO | Lunghezze identiche alla base: USB_DN_C 14,707 mm, USB_DP_C 13,907 mm, USB_DN/USB_DP 3,418 mm; `DEC-041` intatta |
| Rete EN | 15,06 → **15,89 mm**, 3 vie (come dichiarato) |
| Librerie J2–J5 | **Piazzole identiche** alla base nei tre footprint; aggiunti solo courtyard completi e disegni F.Fab |
| Schema, `.kicad_pro`, BOM JLC | Nessuna modifica |
| CPL | Cambia solo la riga di C7 (Y 37,75 → 37,00 mm), coerente con lo spostamento |
| `git diff --check` | Pulito |
| Regola JLC dei 2,5 mm | Ricontrollata sui [termini di assemblaggio JLCPCB](https://jlcpcb.com/help/article/terms-and-conditions-of-jlcpcb-assembly-service): §2, punto 3, distanza corpo–bordo ≥ 2,5 mm **senza limitarla ai lati di trasporto**. L'interpretazione di Codex è corretta. |

## Stato dei rilievi

| Rilievo | Valutazione di Claude | Stato |
|---|---|---|
| REV-001 C7 a 1,85 mm dal bordo | Corretto: corpo a 2,60 mm. Il controllo copre ora tutto il contorno, intaglio incluso. | **Chiuso** (geometria); J1, J2 e U3 restano eccezioni da far accettare alla revisione DFM di JLC |
| REV-002 capacità a monte dell'LDO (C1 + C2 = 20 µF nominali su VBUS) | Fondato. Per una porta USB conviene restare ≤ 10 µF all'inserzione, oppure limitare lo spunto. Serve una scelta del proprietario: ridurre i condensatori d'ingresso oppure qualificare con una misura. | **Aperto** → `OPEN-029` |
| REV-003 courtyard incompleti | Corretto: libreria e istanze J2–J5 aggiornate e piazzole invariate. Il DRC sulle sovrapposizioni dei courtyard ora è significativo. | **Chiuso** |
| REV-004 `esporta.py` prosegue anche se il DRC fallisce | Confermato: manca `--exit-code-violations` e l'esito non ferma le esportazioni. Correzione semplice, solo nello script. | **Aperto** |
| REV-005 firmware/UI ancora con PWM della retroilluminazione | Confermato: [04](../../04-specifiche-firmware.md) righe 24 e 68–70, [05](../../05-interfaccia-utente.md) righe 65–66, `CAND-023` e il diagramma in [03](../../03-alimentazione-ricarica.md) con il touch. Contraddicono `DEC-034`. Correzione solo documentale. | **Aperto** |
| REV-006 cartigli rev 0.1, nota MCU con `\n` letterali, etichette sovrapposte | Confermato: i 5 fogli e il README principale riportano ancora rev 0.1. | **Aperto** |
| REV-007 `CODEX_HANDOFF.md` senza avviso di documento storico, backlog della roadmap superato | Confermato. | **Aperto** |
| **VER-001 (nuovo)** `DEC-040` diceva "2,5 mm dai lati sinistro e destro (lati di trasporto)" | [docs/02](../../02-architettura-hardware.md) e [hardware/README](../../../hardware/README.md) erano già corretti, il registro decisioni no. | **Corretto** con questa verifica: testo di `DEC-040` allineato, con la nota dell'errata |

## Osservazioni per il seguito

- **Rami.** Il ramo `codex/pcb-edge-courtyard-fixes` parte da `4fb9200` e lo supera. Il ramo `claude/hardware-schematic-4ff868` (worktree della sessione hardware) è fermo a `4fb9200`. Prima di altre modifiche hardware bisogna lavorare a partire da `16f9bf7`, altrimenti le correzioni di Codex andrebbero perse o creerebbero conflitti. Nessun ramo è ancora unito a `main` né pubblicato.
- **Generatori.** `genera_pcb_main.py` ora impone 2,5 mm su tutti i bordi e richiama il controllo meccanico. Non è stato rieseguito da nessuno, e rigenerandolo si perderebbe lo sbroglio a mano. Resta valida la regola già documentata: dopo i ritocchi manuali, la fonte è il `.kicad_pcb`.
- **Header J2.** Le piazzole sono 1,02 × 3,16 mm in libreria, contro 1,02 × 3,20 mm del disegno Hanxia. La differenza è trascurabile: è da segnalare alla revisione DFM e da provare sul campione.
- I gate già aperti restano tali: `OPEN-016`, `OPEN-021`, `OPEN-027`, `OPEN-028`, revisione visiva del proprietario in KiCad e DFM JLC. Nessun file Gerber e nessun ordine.

## Chiusura dei rilievi (2026-11-08)

Interventi di Claude sul ramo `codex/pcb-edge-courtyard-fixes`, richiesti dal proprietario. Nessun file Gerber e nessun ordine.

| Rilievo | Intervento | Verifica |
|---|---|---|
| REV-002 spunto USB | C1 10 → **1 µF** (C15849, già in BOM per C7); C2 10 → **4,7 µF** (CL10A475KO8NNNC, **C19666**, X5R 16 V 0603). La pagina JLCPCB, consultata il 2026-11-08, lo indica come Basic e a magazzino. Totale su VBUS 5,7 µF nominali, al massimo 6,3 µF. Stessa impronta 0603: cambiano solo i campi Valore/LCSC in schema e PCB. Decisione `DEC-042`; nota nello schema; spunto da misurare in `VT-PWR-001`. | BOM JLC: C1+C7 1 µF, C2 4,7 µF, C3/C5/C9 10 µF. Rame e posizioni invariati; CPL identica. |
| REV-004 `esporta.py` | DRC con `--exit-code-violations --refill-zones --all-track-errors`. Poi `verifica_meccanica_pcb.py`. Lo script si ferma prima delle esportazioni del PCB se ERC, DRC o controllo meccanico falliscono. | Eseguito: ERC 0, DRC 0/0/0, controllo meccanico PASS, CPL 36 componenti, codice d'uscita 0 |
| REV-005 firmware/UI | [04](../../04-specifiche-firmware.md) v0.7: DIM/BRIGHT come palette grafiche, NIGHT con modulo spento tramite Q1. Aggiunte le sequenze di spegnimento (segnali bassi, poi Q1 aperto) e di accensione (Q1, reset, inizializzazione), la transizione `NIGHT_PEEK → DIM` e il rischio di alimentazione parassita durante boot/ROM. Aggiornati [05](../../05-interfaccia-utente.md) §6, `CAND-023`, il diagramma di [03](../../03-alimentazione-ricarica.md) e `VT-PWR-003`. | Solo documentazione: il firmware non esiste ancora e non è stato toccato |
| REV-006 schema | Cartigli dei 5 fogli in rev 0.2, data 2026-11-08 (`schgen.py` allineato). Nota di recupero del foglio MCU con veri a capo, su tre righe, dentro il riquadro. Sommario senza tasti RESET/BOOT (`DEC-039`). Etichetta IO9_BOOT spostata via dall'etichetta I2C_SCL. TP11 nella fila degli altri punti di test, nota Debug più in basso. Riferimenti TPx 2,54 mm sopra il valore in tutti i fogli. Nota sui pull-up I²C con il caso SHT40 (~2,4 k). `genera_schemi.py` allineato. | ERC 0, parità 0; controllo a vista sulle esportazioni SVG del foglio MCU |
| REV-007 residui storici | `CODEX_HANDOFF.md` con avviso iniziale di documento superato. README principale aggiornato a rev 0.2. Backlog e rischi della [roadmap](../../09-roadmap.md) allineati al modulo a 7 pin. | Collegamenti Markdown verificati |

Esportazioni rigenerate con `esporta.py`: PDF dello schema, BOM, PDF di layout e render 3D `-top`/`-bottom`, ora di nuovo aggiornati grazie ai modelli 3D locali (non versionati). Lo STEP della sola scheda non è cambiato (sagoma invariata).

**Residui non bloccanti (aggiornamento: corretti dal proprietario in KiCad il 2026-11-08, netlist invariata; vedi [docs/10](../../10-decisioni-aperte.md) §9):** negli altri fogli restavano alcune sovrapposizioni estetiche di testi, ad esempio riferimento e valore di U1/U2, campi di F1 e i gruppi di etichette di J3–J5. Non hanno effetti elettrici. Restano aperti i gate fisici: `OPEN-016`, `OPEN-021`, `OPEN-028`, la DFM JLC con le eccezioni J1/J2/U3 e il prototipo M1. La revisione a vista del proprietario è positiva (`OPEN-027` chiusa).
