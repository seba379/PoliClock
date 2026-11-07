# 06 — Specifiche meccaniche e stampa 3D

**Versione:** 0.1 · **Stato:** geometria concettuale, CAD non ancora disponibile · **Data:** 2026-11-07

## 1. Intento estetico (CONF)

- Poliziotta in stile **chibi**, simpatica, moderna, proporzioni intenzionalmente caricaturali.
- Testa sovradimensionata rispetto a busto/gambe, cappello blu con dettagli caratteristici, capelli modellati e uniforme blu.
- Il **display circolare sostituisce il volto**: non esiste un viso umano stampato al centro.
- Posa stabile da scrivania; un braccio sul fianco o saluto è un'alternativa stilistica, non una specifica bloccata.
- Aspetto curato sia frontalmente (regalo) sia posteriormente (porta USB-C e sportellino nascosti).

I render del concept sono **riferimenti estetici**, non modelli 3D quotati, né garanzia di stampabilità.

## 2. Layout fisico candidato

```text
                 CAPPELLO / TESTA
            +-----------------------+
            | area di alloggiamento |
            | AMOLED circolare      | <-- apertura frontale
            | scheda/driver         |
            +-----------+-----------+
                        |
                 BUSTO CAVO
              +---------+---------+
              | cablaggi / accesso| <-- sportello posteriore
              | PMU integrata     |
              | USB-C posteriore  | <-- connettore fissato alla scocca
              +---------+---------+
                        |
                  BASE / GAMBE
              +-------------------+
              | batteria LiPo 1S  | <-- sede isolata, baricentro basso
              +-------------------+

   SHT40: piccolo vano ventilato verso aria ambiente, lontano da display,
   MCU, PMU e dal punto in cui si concentra il calore della ricarica.
```

La reale distribuzione dei componenti dipende dal posizionamento delle porte sulla scheda Waveshare. Può essere necessario alloggiare tutto il modulo dietro la testa, riservando al busto la batteria/il passaggio dei cablaggi.

## 3. Dimensionamento e congelamento quote

- **Altezza statuetta indicativa**: 130–160 mm (CAND, non misura definitiva).
- Display candidato: **1,75" di diagonale/diametro attivo nominale**, ma PCB, cornice, raggi e connector area vanno rilevati dalla tavola meccanica e dal modulo fisico.
- Non assumere una testata di 1,75" di diametro esterno: apertura e sottostruttura sono necessariamente più grandi.
- Determinare ingombro reale di: modulo completo, USB-C originale, connettore batteria, pettine GPIO, cavi, viti, batteria con linguette/connettore, breakout SHT40.
- Quote della batteria soltanto dopo selezione di una **specifica cella acquistabile**; evitare generici volumi '3000 mAh' privi di geometria.
- Definire tolleranze fit e gioco dei cablaggi su stampa test, non da aspettative teoriche della stampante.

Fonte tavole ufficiali: [Waveshare — risorse e disegni di ingombro](https://docs.waveshare.com/ESP32-S3-Touch-AMOLED-1.75/Resources-And-Documents).

## 4. Sottogruppi CAD consigliati

1. `head_front`: frontale/testa con anello display e cappello, eventuale volume capelli.
2. `head_rear`: guscio posteriore testa con supporti modulo, accesso viti.
3. `body_shell`: busto cavo, braccia/gambe e passaggi cablaggio.
4. `base_insert`: vano batteria isolato, ferma-cavo e appoggio antiscivolo.
5. `usb_bracket`: supporto meccanico della presa USB-C femmina posteriore.
6. `sensor_carrier`: supporto SHT40 con finestre di aerazione, lontano da sorgenti calde.
7. `service_hatch`: sportellino removibile con viti nascoste o incastro affidabile.

La scomposizione è una proposta; può cambiare a seconda di vincoli di stampa, colorazione e cablaggio.

## 5. Supporto display

- Appoggio rigido e ripetibile per il PCB, senza carichi sulla parte attiva del display.
- Cornice che **non** copra cifre o target touch.
- Niente colla permanente sul display/PCB che impedisca la manutenzione.
- Nessuna vite a contatto con il vetro; se si usano inserti filettati termici, montarli prima di introdurre elettronica e cella.
- Verificare accessibilità al tasto PWR e a BOOT (almeno con sportellino aperto) e alla porta USB per il flashing.
- Definire protezione dei flessibili e del bordo del display da sfregamento con la stampa.

## 6. Porta USB-C sul retro

- Montaggio **incassato**, preferibilmente nella parte inferiore del busto, per invisibilità frontale.
- Prolunga corta supportata tramite staffa con viti; nessuna sollecitazione diretta sulla USB della Waveshare.
- Apertura sufficientemente grande per connettori commerciali, ma non visivamente invasiva.
- Prova inserimento con differenti cavi, rispettando raggio di curvatura all'interno.
- Controllo del ribaltamento con cavo inserito e trazione accidentale leggera, senza forzare connettori.

## 7. Gestione termica e aerazione sensore

- Sensore ambiente in sede raggiunta da ricambio d'aria, senza soffiare aria calda dal circuito principale.
- Non alloggiare SHT40 immediatamente dietro il display AMOLED o contro PMU/batteria.
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
| Superfici touch | Lasciare libera la superficie attiva, salvo protezione compatibile validata |

L'adozione di PETG o PLA non elimina la necessità di un test termico: le temperature interne sono sconosciute finché non si misura il prototipo.

## 9. Test meccanici / criteri di accettazione

- Assemblaggio e disassemblaggio ripetuti senza deformazione o danno ai cavi.
- Nessuna pressione del frontale sul vetro o sul flessibile del display.
- Accesso a USB, PWR/BOOT e batteria secondo la strategia di service.
- Stabilità su piano, senza cavo e con cavo, a normale interazione touch.
- SHT40 esterno rileva condizioni della stanza con errore aggiuntivo dovuto al case valutato e documentato.
- Assenza di surriscaldamenti/contatti pericolosi nel vano batteria durante ricarica.

## 10. File CAD attesi in una milestone successiva

`mechanical/cad/` (sorgenti parametrici editabili), `mechanical/prints/` (STL/3MF esportati), `mechanical/drawings/` (quote principali e sezioni), `assets/renders/` (render estetici), più distinta elementi stampati e note di montaggio. Nessuno di questi è ancora considerato generato o verificato.
