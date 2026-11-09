# Verifica delle correzioni della terza revisione

**Data:** 2026-11-09 · **Revisore:** Claude (sola lettura del progetto) · **Base:** `e365648` (ramo `claude/hardware-schematic-4ff868`), unito nel ramo `claude/revisione-finale-ea91f4` con il merge `30114c1`. KiCad 10.0.6.

Addendum al [rapporto della terza revisione](README.md). Non è una revisione completa: controlla solo le modifiche fatte da `edcef25` in poi, più i gate globali (ERC, DRC, controllo meccanico, BOM/CPL).

Non ho modificato nessun file di progetto, non ho generato Gerber e non ho fatto push. `kicad-cli` non ha riscritto il `.kicad_pro`.

L'unione ha dato un conflitto solo in `docs/10`, dove il ramo hardware aveva aggiunto la sua §17 "Correzioni dopo la terza revisione" nello stesso punto della mia riga. Ho tenuto entrambe le parti: la §17 del ramo hardware resta invariata e la mia sezione diventa la **§18**.

## 1. Esito

### **PRONTO PER GERBER**

Non restano rilievi P1 o P2:

- R3-001 è corretto con le vie GND (correzione 2 del rapporto), con criteri verificati in modo indipendente;
- R3-003, R3-004 e R3-005 sono corretti;
- R3-002 resta aperto come P3 accettato per la V1.

I Gerber si generano con `esporta_gerber_jlc.py --conferma-proprietario` **solo dopo l'autorizzazione esplicita del proprietario**. Prima conviene chiudere le azioni che toccano al proprietario e non al progetto:

- la prova 1:1 dei JST PH e dell'header 1×8 (FIN-011), che `docs/12` consiglia prima dei Gerber;
- lo studio volumetrico `OPEN-028`, se può ancora cambiare la scheda.

Restano invariati i gate dell'ordine: DFM di J1, scelta della CPL nell'anteprima JLC, scorte, `OPEN-016` e `OPEN-021`.

## 2. Comandi e risultati

| Controllo | Comando / fonte | Risultato |
|---|---|---|
| Diff `edcef25..e365648` | `git diff` | PCB: **solo 8 blocchi `(via …)` aggiunti** (GND, 0,6/0,3 mm, F.Cu–B.Cu), nessuna riga tolta o cambiata: nessun footprint, pista, zona o contorno toccato. `.kicad_dru`: solo i due commenti di R3-005. Documenti: `docs/02`, `04`, `09`, `10`, `12`, `hardware/README.md`. Render, PDF e STEP rigenerati. BOM e CPL invariate |
| ERC | `kicad-cli sch erc --severity-all --exit-code-violations` | **0 violazioni**, codice d'uscita 0 → [correzioni-erc.rpt](correzioni-erc.rpt), [correzioni-erc.json](correzioni-erc.json) |
| DRC | `kicad-cli pcb drc --severity-all --all-track-errors --schematic-parity --refill-zones --exit-code-violations` | **0 / 0 / 0**, codice d'uscita 0 → [correzioni-drc.rpt](correzioni-drc.rpt), [correzioni-drc.json](correzioni-drc.json). Ignorati gli stessi tre controlli di prima |
| Controllo meccanico | `verifica_meccanica_pcb.py` | **PASS**, J1 unica eccezione, U3 2,99 mm → [correzioni-verifica-meccanica.json](correzioni-verifica-meccanica.json) |
| Coppia USB, piste | Confronto pcbnew con `edcef25` | 36 elementi della coppia **identici**, 41 elementi bloccati in entrambe le versioni, piste 1166,3 mm in entrambe; vie 62 → 70 |
| Zona antenna e `usb_coppia_retro` | Distanza delle 8 vie nuove | Nessuna dentro: la più vicina alla zona antenna è a 4,52 mm (via 136,7; 110,8), tutte oltre 5 mm da `usb_coppia_retro` |
| BOM e CPL | Footprint invariati (diff) | BOM JLC 18 righe, CPL 34 parti e CPL alternativa ancora coerenti con il PCB; nessun file CSV cambiato |
| Isole GND | Riempimento in memoria, vie per isola | §3 |
| ESP-IDF | `C:\esp\v6.0` e `v6.1`: `components/esp_hw_support/port/esp32c3/Kconfig.rtc` | §4 |

## 3. Le vie nuove

Coordinate del foglio KiCad, misurate bordo-bordo sul rame. Tutte le vie sono 0,6/0,3 mm, GND, **coperte dalla maschera su entrambi i lati** (`IsTented` F/B = sì).

| Via | Distanza dalla EPAD | Foro-foro minimo | Rame di altra rete più vicino | Note |
|---|---|---|---|---|
| (136,7; 110,8) | 0,75 mm | 3,17 mm | +3V3 0,57 mm | sotto U3 |
| (134,2; 108,4) | 1,32 mm | 2,16 mm | EN 1,57 mm | sotto U3 |
| (131,4; 111,6) | 1,07 mm | 1,95 mm | LCD_MOSI 1,48 mm | sotto U3 |
| (133,2; 114,1) | 0,90 mm | 2,78 mm | +3V3 0,71 mm | sotto U3 |
| (127,2; 102,6) | — | 1,66 mm | DISP_BUSY 0,56 mm | 0,47 mm dal pad 9 di U3 (GND, stessa rete), fuori dal courtyard di U3 |
| (119,3; 112,3) | — | 0,83 mm | DISP_EN_N 0,53 mm | 0,93 mm da R16.1 |
| (121,0; 121,5) | — | 1,24 mm | +3V3 0,87 mm | 1,8 mm da C9 |
| (123,5; 128,5) | — | 1,02 mm | +3V3 0,67 mm | 0,76 mm dal punto di test TP9 sul retro |

Esito per ciascun criterio:

- **`DEC-046`.** Nessuna via nella EPAD. Le 4 vie vicine sono a 0,75–1,32 mm dal bordo della piazzola, quindi oltre gli 0,5 mm richiesti.
- **Regole JLC lette oggi.** Foro-foro: minimo 0,83 mm contro gli 0,2 mm chiesti fra vie. Via-pista: minimo 0,53 mm contro 0,2 mm. Diametro uguale al foro + 0,3 mm, oltre la regola "foro + 0,1 mm". Il DRC con le regole del progetto dà 0.
- **Saldatura.**
  - Le 4 vie sotto U3 sono coperte dalla maschera, fuori dalla EPAD e dalle aperture di pasta: non possono assorbire stagno. Il modulo appoggia sulle piazzole e la copertura della via non interferisce.
  - La via a 0,47 mm dal pad 9 è sulla stessa rete ed è coperta: non c'è rischio di ponte. Sotto le parti montate da JLC non ci sono altre vie.
  - La via vicino a TP9 non ostacola la punta del puntale, perché TP9 resta scoperto.

**Isole GND ricontate** (riempimento in memoria, isole scollegate rimosse "always"):

| Isola | `edcef25` | `e365648` | Criterio del rapporto | Esito |
|---|---|---|---|---|
| Retro sotto U3, 95,4 mm² | 2 vie | **6 vie**: (139,5; 103,5), (130,6; 108,0) e le 4 nuove accanto alla EPAD | ≥ 3 | **OK** |
| Rame superiore U3.9/C6.2, 31,7 mm² | 1 via | **2 vie**: (139,5; 103,5) e (127,2; 102,6) | ≥ 2 | **OK** |
| Retro zona J2/passivi, 249,1 mm² | 1 via | **5 vie**: (112,4; 104,3), (127,2; 102,6) e 3 nuove | (R3-003) almeno 2–3 in più | **OK** |
| Rame superiore principale, 1202,1 mm² | 18 vie | 25 vie, EPAD inclusa | — | — |
| Retro principale, 899,8 mm² | 17 vie | invariato | — | — |

I numeri coincidono con quelli della sessione hardware.

Il retro sotto il modulo resta separato dal piano principale del retro, perché DISP_BUSY non è stato spostato. Però è collegato in 4 punti, a 1–2 mm dalla EPAD, al rame superiore principale, che contiene la EPAD ed è cucito al retro principale con 17 vie. Il ritorno di +3V3 ed EN sotto il modulo ha di nuovo un piano ben collegato, e il pin 9 ha due strade. Per la V1 basta: R3-001 è **chiuso**. Le misure di `VT-PCB-002` (3V3 al pin 1, EN, USB) restano come per R2-005.

## 4. R3-002 e R3-004

- **R3-002, aperto e accettabile per la V1.** DISP_BUSY è un ingresso statico ed è fuori dalla zona antenna (0,23 mm, DRC 0). Con la radio spenta (`DEC-012`) non ha effetti. La spiegazione in `docs/10` §17 è coerente con il PCB: fra R23 e il pin 17 il retro è attraversato dalla diagonale +3V3 e dal fascio IO0/I2C_SDA/BTN_USER, quindi spostare la pista richiederebbe di sbrogliare di nuovo DISP_EN_N, LCD_MOSI e +3V3. La nota V2 nella [roadmap](../../../09-roadmap.md) ora cita anche DISP_BUSY (0,22 mm per circa 18 mm). Se si riattiva la radio, va rivisto insieme a LCD_CS.
- **R3-004, corretto.** In ESP-IDF v6.0 e v6.1 il file `components/esp_hw_support/port/esp32c3/Kconfig.rtc` ha `choice RTC_CLK_SRC` con `default RTC_CLK_SRC_INT_RC` ("Internal 136 kHz RC oscillator") e le opzioni `RTC_CLK_SRC_EXT_CRYS` ("External 32 kHz crystal"), `RTC_CLK_SRC_EXT_OSC` ("External 32 kHz oscillator at 32K_XP pin") e `RTC_CLK_SRC_INT_8MD256`. I simboli `CONFIG_RTC_CLK_SRC_INT_RC`, `…_INT_8MD256`, `…_EXT_CRYS` e `…_EXT_OSC` citati in [docs/04](../../../04-specifiche-firmware.md) §4, punto 5, sono quindi esatti, e anche il divieto dell'ADC su IO1 è corretto.

## 5. Chiusura dei rilievi della terza revisione

| Rilievo | Stato | Evidenza |
|---|---|---|
| R3-001 (P2) isola GND sotto U3 | **Chiuso** | 8 vie GND, criteri ≥ 3 / ≥ 2 rispettati (§3), `DEC-046` rispettata, DRC 0/0/0 |
| R3-002 (P3) DISP_BUSY vicino all'antenna | **Aperto, accettato per la V1** | Nota V2 nella roadmap; nessun effetto con la radio spenta |
| R3-003 (P3) isola del retro di 249 mm² | **Chiuso** | 5 vie (§3) |
| R3-004 (P3) clock RTC lento | **Chiuso** | `docs/04` §4 punto 5, simboli verificati in ESP-IDF v6.0/v6.1 |
| R3-005 (P3) residui nella documentazione | **Chiuso** | `docs/02` EPAD senza vie; `CAND-022` con l'header 1×8; `docs/12` con le decisioni fino a `DEC-049` e la scorta di oggi; commenti del `.kicad_dru`; riga `DEC-048` "numero non usato"; `DEC-046` dichiara lo scostamento dalla fig. 11-1 del datasheet. Serigrafia "DISP 1=VCC" invariata (era facoltativa) |

**Nuovi rilievi:** nessuno.

Una nota di contesto: `docs/10` §17 dice che il rapporto della terza revisione è "nel ramo del revisore […] questo ramo non lo contiene". Dopo l'unione dei due rami il rapporto e la sezione stanno insieme; la frase si può aggiornare quando i rami confluiscono in `main`.

## 6. Riproduzione

```powershell
$kicad = 'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe'
$py = 'C:\Program Files\KiCad\10.0\bin\python.exe'
$out = 'docs/revisioni/2026-11-09/revisione-finale-3'
git diff edcef25 e365648 -- hardware/policlock-main/policlock-main.kicad_pcb
& $kicad sch erc --severity-all --exit-code-violations --format json -o "$out/correzioni-erc.json" hardware/policlock-main/policlock-main.kicad_sch
& $kicad pcb drc --severity-all --all-track-errors --schematic-parity --refill-zones --exit-code-violations --format json -o "$out/correzioni-drc.json" hardware/policlock-main/policlock-main.kicad_pcb
& $py hardware/scripts/verifica_meccanica_pcb.py --output "$out/correzioni-verifica-meccanica.json" hardware/policlock-main/policlock-main.kicad_pcb
git status --short   # se kicad-cli ha riscritto il .kicad_pro: git checkout -- hardware/policlock-main/policlock-main.kicad_pro
```

Le distanze delle vie, le isole GND e il confronto con `edcef25` vengono da script pcbnew in sola lettura nella cartella temporanea della sessione. Le zone sono riempite solo in memoria e il PCB non viene mai salvato. Nessuna prova su hardware fisico.
