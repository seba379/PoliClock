# 06 — Specifiche meccaniche e stampa 3D

**Versione:** 0.4 · **Stato:** geometria concettuale, CAD non ancora disponibile · **Data:** 2026-11-07

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
            | schedina portadisplay |
            | (solo connettori)     |
            +-----------+-----------+
                        |
                 BUSTO CAVO
              +---------+---------+
              | cavo display (FFC)| <-- attraversa il collo
              | scheda principale | <-- opzione A (o nella testa, B)
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

Nella testa c'è solo il display sulla schedina portadisplay. La scheda principale è separata (`DEC-021`) e la sua posizione si decide con la bozza Blender (`OPEN-020`):

- **Opzione A (preferita)**: scheda nel busto/base, vicino alla batteria, con la USB-C saldata sul bordo e affacciata al foro sul sedere; dalla testa scende solo il cavo display.
- **Opzione B**: scheda nella testa dietro il portadisplay; scendono prolunga USB-C, cavo batteria e cavo SHT40.

In una chibi la cavità più grande è la testa, mentre il busto è stretto: la bozza deve verificare che scheda principale e cella entrino nel busto/base. Il collo deve lasciare passare il cavo display con i connettori e un raggio di curvatura adeguato.

## 3. Dimensionamento e congelamento quote

- **Altezza statuetta indicativa**: 130–160 mm (CAND, non misura definitiva).
- Display: IPS rotondo **1,28"** (`DEC-016`), area attiva circa 32 mm di diametro (da verificare sul datasheet del pannello); vetro, cornice, FPC e PCB dietro sono più grandi.
- Schedina portadisplay e scheda principale si disegnano in KiCad **insieme** al CAD: sagome, fori di fissaggio, posizione di USB-C e connettori sono quote condivise (STEP esportato da KiCad).
- Determinare ingombro reale di: pannello con FPC, portadisplay, scheda principale con componenti, cavo display e connettori, eventuale prolunga USB-C e staffa, viti, batteria con connettore, mini-PCB SHT40, pulsante.
- Quote della batteria soltanto dopo selezione di una **specifica cella acquistabile**; evitare generici volumi '3000 mAh' privi di geometria.
- Definire tolleranze fit e gioco dei cablaggi su stampa test, non da aspettative teoriche della stampante.

Fonti quote: datasheet meccanico del pannello acquistato, file KiCad del PCB (esportazione STEP) e misure con calibro.

## 4. Sottogruppi CAD consigliati

1. `head_front`: frontale/testa con anello display e cappello, eventuale volume capelli.
2. `head_rear`: guscio posteriore testa con supporto del portadisplay, passaggio cavo, accesso viti.
3. `body_shell`: busto cavo, braccia/gambe e passaggi cablaggio.
4. `base_insert`: vano batteria isolato, ferma-cavo e appoggio antiscivolo.
5. `usb_bracket` / `main_board_mount`: supporto avvitato della scheda principale con la USB-C allineata al foro sul sedere (opzione A) o staffa della prolunga (opzione B).
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
- Opzione A: scheda principale avvitata alla scocca in modo che lo sforzo del cavo vada sulle viti e sulla scocca, non sulle saldature della USB-C. Opzione B: prolunga fissata con staffa avvitata.
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

## 10. Strumenti CAD (`DEC-022`)

- **Blender**: forma della chibi (testa, capelli, cappello, corpo, posa), booleane finali con le parti tecniche, divisione in pezzi stampabili, render. Bozza a volumi semplici anche via script; scultura artistica a mano.
- **CAD a codice** (build123d, `CAND-021`): parti tecniche interne parametriche (supporti, vani, staffe, sportello), legate allo STEP delle schede esportato da KiCad; esportazione STEP/STL.
- **Slicer** della stampante del proprietario (modello da indicare): orientamento, supporti, tolleranze.

## 11. File CAD attesi in una milestone successiva

`mechanical/cad/` (sorgenti parametrici editabili), `mechanical/prints/` (STL/3MF esportati), `mechanical/drawings/` (quote principali e sezioni), `assets/renders/` (render estetici), più distinta elementi stampati e note di montaggio. Nessuno di questi è ancora considerato generato o verificato.
