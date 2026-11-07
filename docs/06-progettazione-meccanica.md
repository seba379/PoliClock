# 06 — Specifiche meccaniche e stampa 3D

**Versione:** 0.3 · **Stato:** geometria concettuale, CAD non ancora disponibile · **Data:** 2026-11-07

## 1. Intento estetico (CONF)

- Poliziotta in stile **chibi**, simpatica, moderna, proporzioni intenzionalmente caricaturali.
- Testa sovradimensionata rispetto a busto/gambe, cappello blu con dettagli caratteristici, capelli modellati e uniforme blu.
- Il **display circolare sostituisce il volto**: non esiste un viso umano stampato al centro.
- Posa stabile da scrivania; un braccio sul fianco o saluto è un'alternativa stilistica, non una specifica bloccata.
- Aspetto curato sia frontalmente (regalo) sia posteriormente: presa USB-C nella parte posteriore bassa, **sul sedere** (scelta ironica voluta, `DEC-018`), sportellino nascosto.
- Un **pulsante** fisico integrato in modo discreto nella statuetta (`DEC-017`, posizione in `OPEN-017`).

I render del concept sono **riferimenti estetici**, non modelli 3D quotati, né garanzia di stampabilità.

## 2. Layout fisico candidato

```text
                 CAPPELLO / TESTA
            +-----------------------+
            | display IPS 1,28"     | <-- apertura frontale
            | PCB custom rotondo    |
            | (MCU, caricatore, RTC)|
            +-----------+-----------+
                        |
                 BUSTO CAVO
              +---------+---------+
              | cablaggi / accesso| <-- sportello posteriore
              | prolunga USB-C    |
              | SHT40 ventilato   |
              +---------+---------+
                        |
                  BASE / GAMBE
              +-------------------+
              | batteria LiPo 1S  | <-- sede isolata, baricentro basso
              | presa USB-C       | <-- sul sedere, staffa avvitata
              +-------------------+

   SHT40: piccolo vano ventilato verso aria ambiente, lontano da display,
   PCB e dal punto in cui si concentra il calore della ricarica.
```

Il PCB custom rotondo sta dietro il display nella testa (collegamento FPC corto). Dalla testa scendono nel corpo: prolunga USB-C, cavo batteria, cavo SHT40 ed eventuale cavo del pulsante. Prevedere un passaggio cavi abbastanza largo per i connettori e fermacavi.

## 3. Dimensionamento e congelamento quote

- **Altezza statuetta indicativa**: 130–160 mm (CAND, non misura definitiva).
- Display: IPS rotondo **1,28"** (`DEC-016`), area attiva circa 32 mm di diametro (da verificare sul datasheet del pannello); vetro, cornice, FPC e PCB dietro sono più grandi.
- Il PCB rotondo va disegnato in KiCad **insieme** al CAD della testa: diametro, fori di fissaggio e posizione dei connettori sono quote condivise.
- Determinare ingombro reale di: pannello con FPC, PCB con componenti, connettori, prolunga USB-C e staffa, cavi, viti, batteria con connettore, mini-PCB SHT40, pulsante.
- Quote della batteria soltanto dopo selezione di una **specifica cella acquistabile**; evitare generici volumi '3000 mAh' privi di geometria.
- Definire tolleranze fit e gioco dei cablaggi su stampa test, non da aspettative teoriche della stampante.

Fonti quote: datasheet meccanico del pannello acquistato, file KiCad del PCB (esportazione STEP) e misure con calibro.

## 4. Sottogruppi CAD consigliati

1. `head_front`: frontale/testa con anello display e cappello, eventuale volume capelli.
2. `head_rear`: guscio posteriore testa con supporti PCB, accesso viti.
3. `body_shell`: busto cavo, braccia/gambe e passaggi cablaggio.
4. `base_insert`: vano batteria isolato, ferma-cavo e appoggio antiscivolo.
5. `usb_bracket`: supporto meccanico della presa USB-C femmina sul sedere.
6. `button_mount`: sede del pulsante, posizione da definire.
7. `sensor_carrier`: supporto SHT40 con finestre di aerazione, lontano da sorgenti calde.
8. `service_hatch`: sportellino removibile con viti nascoste o incastro affidabile.

La scomposizione è una proposta; può cambiare a seconda di vincoli di stampa, colorazione e cablaggio.

## 5. Supporto display

- Appoggio rigido e ripetibile per il PCB, senza carichi sulla parte attiva del display.
- Cornice che **non** copra le cifre: verificare l'area visibile sul pannello reale.
- Niente colla permanente sul display/PCB che impedisca la manutenzione.
- Nessuna vite a contatto con il vetro; se si usano inserti filettati termici, montarli prima di introdurre elettronica e cella.
- Punti di test e pad BOOT/RESET del PCB accessibili con sportellino aperto; il flashing normale avviene dalla USB-C posteriore.
- Definire protezione dei flessibili e del bordo del display da sfregamento con la stampa.

## 6. Porta USB-C posteriore (sul sedere)

- Montaggio **incassato** sul sedere della statuetta (`DEC-018`), invisibile frontalmente.
- Prolunga (indicativamente 15–25 cm) dalla testa alla base, fissata con staffa avvitata; nessuna sollecitazione diretta sul connettore del PCB.
- Apertura sufficientemente grande per connettori commerciali, ma non visivamente invasiva.
- Prova inserimento con differenti cavi, rispettando raggio di curvatura all'interno.
- Con la presa così in basso il cavo esce quasi a livello del piano: verificare che la statuetta resti dritta e stabile con il cavo inserito (eventuale incavo nella base per il passaggio del cavo) e con trazione accidentale leggera.

## 7. Gestione termica e aerazione sensore

- Sensore ambiente in sede raggiunta da ricambio d'aria, senza soffiare aria calda dal circuito principale.
- Non alloggiare SHT40 immediatamente dietro il display o contro PCB/batteria.
- Introdurre piccoli fori o feritoie discreti; evitare cavità totalmente chiusa se si richiede una misura rappresentativa della stanza.
- Valutare materiale della scocca e temperatura durante ricarica; **non** mettere una LiPo vicina a inserti filettati installati a caldo o superfici che la comprimano.
- Validare l'errore dovuto ad autosurriscaldamento con confronto su banco, prima e dopo chiusura scocca.

## 8. Stampa e finitura (proposta)

| Elemento | Proposta iniziale |
|---|---|
| Materiale | PLA per primi mockup dimensionali; PETG da valutare dopo le prove termiche |
| Colori | Blu scuro corpo/cappello, nero stivali, capelli a scelta, dettagli dorati/azzurri |
| Metodo | Parti separate per favorire finitura e montaggio |
| Fissaggi | Viti e sedi filettate/inserti compatibili, mai direttamente sulla batteria |
| Base | Fondo più pesante/stabile, feltrini o gommini antiscivolo |
| Display | Lasciare libera l'area attiva; eventuale vetrino/protezione da validare |
| Pulsante | Corsa e sensazione provate su stampa test |

L'adozione di PETG o PLA non elimina la necessità di un test termico: le temperature interne sono sconosciute finché non si misura il prototipo.

## 9. Test meccanici / criteri di accettazione

- Assemblaggio e disassemblaggio ripetuti senza deformazione o danno ai cavi.
- Nessuna pressione del frontale sul vetro o sul flessibile del display.
- Accesso a USB, BOOT/RESET e batteria secondo la strategia di service.
- Stabilità su piano, senza cavo e con cavo, anche premendo il pulsante.
- SHT40 esterno rileva condizioni della stanza con errore aggiuntivo dovuto al case valutato e documentato.
- Assenza di surriscaldamenti/contatti pericolosi nel vano batteria durante ricarica.

## 10. File CAD attesi in una milestone successiva

`mechanical/cad/` (sorgenti parametrici editabili), `mechanical/prints/` (STL/3MF esportati), `mechanical/drawings/` (quote principali e sezioni), `assets/renders/` (render estetici), più distinta elementi stampati e note di montaggio. Nessuno di questi è ancora considerato generato o verificato.
