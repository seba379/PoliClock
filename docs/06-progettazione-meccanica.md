# 06 — Specifiche meccaniche e stampa 3D

**Versione:** 1.2 · **Stato:** concept 3D a cubetti v2 (2026-11-10), parametrico in build123d; da rivedere con il proprietario · **Data:** 2026-11-10

## 1. Intento estetico (CONF)

- Poliziotta in stile **chibi**, simpatica, moderna, proporzioni intenzionalmente caricaturali.
- Testa sovradimensionata rispetto a busto/gambe, cappello blu con dettagli caratteristici, capelli modellati e uniforme blu.
- Il **display circolare sostituisce il volto**: non esiste un viso umano stampato al centro.
- **In piedi su una base d'appoggio** (`DEC-051`); un braccio sul fianco o saluto è un'alternativa stilistica, non una specifica bloccata.
- Aspetto curato sia frontalmente (regalo) sia posteriormente: presa USB-C nella parte posteriore bassa, **sul retro della base** che contiene la scheda (`DEC-048`), sportello di servizio sul fondo. La battuta "sul sedere" di `DEC-018` non si tiene (`DEC-051`).
- **Stile "a cubetti" (voxel)** dal riferimento del proprietario ([`assets/concept/riferimento-stile-chibi-voxel.webp`](../assets/concept/riferimento-stile-chibi-voxel.webp), solo illustrativo): testa a cubo con il display come volto, cappello blu notte, capelli castani con coda laterale, camicia blu notte a maniche corte con spalline e tasche, cintura con fondina, pantaloni azzurri con banda rossa, stivali neri (§13).
- **Insegne stilizzate** (`DEC-053`, scelta del proprietario): sul cappello un fregio dorato generico a pixel (non l'aquila ufficiale), sul petto la scritta "POLIZIA" e una toppa tricolore in piccolo rilievo. Evocano la divisa senza copiare insegne ufficiali ([00](00-visione-perimetro.md) §5).
- **Testa piccola, il display è tutto il volto** (`DEC-054`): incorniciato solo da capelli e cappello, così il firmware può anche disegnare una faccia emoji ([05](05-interfaccia-utente.md) §10). Busto e gambe più lunghi, braccia leggibili.
- Un **pulsante** fisico integrato in modo discreto nella statuetta (`DEC-017`, posizione in `OPEN-017`).

I render del concept sono **riferimenti estetici**, non modelli 3D quotati, né garanzia di stampabilità.

## 2. Layout fisico candidato

```text
                 CAPPELLO / TESTA
            +-----------------------+
            | display IPS 1,28"     | <-- volto (DEC-003)
            | modulo display 7 pin  |
            +-----------+-----------+
                        |  cavetto Dupont 7 fili, 10 cm
              BUSTO, GIACCA, GAMBE
              +-------------------+
              | canale 21 x 6 mm  | <-- dalla testa al piano della base
              +---------+---------+
                        |
     BASE D'APPOGGIO (DEC-048), circa 78,5 x 76,3 x 24,1 mm
  +--------------------------------------------------+
  | scheda principale     | DS3231, pila verso fondo | <-- USB-C sul retro
  | (antenna a sinistra)  | camera SHT40 ventilata   |
  | zavorra nella striscia anteriore                 |
  | fondo apribile = sportello di servizio           |
  +--------------------------------------------------+
```

Nella testa c'è solo il modulo display a 7 pin (`DEC-034`), con il cavetto che scende nel corpo. La scheda principale è separata (`DEC-021`) e sta **nella base d'appoggio** (`DEC-048`, chiude `OPEN-020`): la USB-C saldata sul bordo si affaccia all'apertura sul retro della base, senza prolunga. Nella base stanno anche il modulo RTC, il sensore SHT40 in una camera ventilata e la **zavorra** che tiene la statuetta stabile con il cavo sempre collegato (senza batteria, `DEC-023`). Il corpo deve lasciare passare il cavetto del display con il suo connettore Dupont a 7 vie (circa 18 × 2,5 mm). Quote e verifiche nel §12.

## 3. Dimensionamento e congelamento quote

- **Altezza statuetta indicativa**: 130–160 mm; dal blockout **circa 150 mm** (`CAND-008`, il proprietario ha chiesto di ricavarla dal volume; da confermare sui render).
- Display: modulo IPS rotondo **1,28"** (`DEC-016`, `DEC-034`), area attiva circa 32 mm di diametro; la schedina del modulo con i 7 piedini è più grande del vetro: misurare il modulo ricevuto (`OPEN-016`).
- La scheda principale si disegna in KiCad **insieme** al CAD: sagome, fori di fissaggio, posizione di USB-C e connettori sono quote condivise (STEP esportato da KiCad).
- Determinare ingombro reale di: modulo display con cavetto, scheda principale con componenti, cavo display e connettori, eventuale prolunga USB-C e staffa, viti, zavorra, modulo SHT40 (`DEC-028`), modulo RTC DS3231 (`DEC-024`), pulsante, spina del cavo USB-C.
- **Scheda principale (rev 0.2, `DEC-045`)**: **50,5 × 41,5 × 1,6 mm**, rettangolare, **senza intaglio** (prima 50 × 40 con intaglio, `DEC-036`): il modulo **ESP32-C3-WROOM-02** (`DEC-044`, 18 × 20 × **3,2 mm**, più alto del MINI-1 da 2,4 mm) sta tutto sulla scheda, con l'antenna verso il bordo destro a 2,99 mm e una zona senza rame sotto e attorno (nessun materiale conduttivo né viti metalliche vicino all'antenna; con la radio attiva Espressif chiede 15 mm liberi attorno nella custodia, irrilevante in V1, `DEC-012`). Quote dall'**angolo in basso a sinistra**, che non è cambiato: USB-C a filo del bordo inferiore (centro a 33,7 mm dal bordo sinistro, guscio sporgente 0,4 mm), due fori **M2** a (24,2; 3,5) e (43,7; 3,5) mm dal bordo sinistro e da quello inferiore, per avvitare la scheda e scaricare lo sforzo del cavo. Header display **1×8** a 90° a foro passante sul bordo superiore (pin da x = 7,3 a 25,1 mm, `DEC-043`; dal `DEC-049` ha un pin in più, BUSY, e inizia 2,54 mm più a sinistra: lungo 20,3 mm invece di 17,8; il cavetto del GC9A01 resta a 7 fili sui pin 1–7, un e-paper ne userebbe 8): i **piedini sporgono di circa 5,7 mm oltre il bordo** e il connettore Dupont aggiunge altri ~14 mm, da prevedere nel CAD; con un header diritto negli stessi fori il cavo esce invece verso l'alto. **JST PH B4B-PH-K-S** (J3, J4, J5) sul lato sinistro, a circa 0,6 mm dal bordo: connettori **alti circa 6 mm, con ingresso del cavo dall'alto** (la spina PHR-4 aggiunge altezza, da prevedere nel CAD). Retro senza componenti, ma con i **piedini a foro passante di J2–J5 che sporgono sotto la scheda** (lunghezza dopo la saldatura da misurare, eventualmente da accorciare): serve luce sotto la scheda o un appoggio solo sui bordi e sui fori M2 (`OPEN-028`). Studio volumetrico 1:1 della base fatto il 2026-11-09 (§12): 3,5 mm di luce sotto la scheda, appoggio sui fori M2 e sugli angoli anteriori. Quote: STEP della scheda `hardware/policlock-main/policlock-main-scheda.step` (dettagli in [02](02-architettura-hardware.md) §3.2).
- Definire tolleranze fit e gioco dei cablaggi su stampa test, non da aspettative teoriche della stampante.

Fonti quote: datasheet meccanico del pannello acquistato, file KiCad del PCB (esportazione STEP) e misure con calibro.

## 4. Sottogruppi CAD consigliati

1. `head_front`: frontale/testa con anello display e cappello, eventuale volume capelli.
2. `head_rear`: guscio posteriore testa con supporto del modulo display, passaggio cavo, accesso viti.
3. `body_shell`: busto cavo, braccia/gambe e passaggi cablaggio.
4. `base_guscio` (studio: `mechanical/cad/studio_base.py`): pareti e piano superiore della base, apertura USB-C sul retro, colonnine della scheda, culla del DS3231, camera SHT40 con feritoie, fori per le viti del corpo.
5. `base_fondo`: fondo apribile che fa da sportello di servizio, con la vasca della zavorra, gli appoggi della scheda e i gommini antiscivolo.
6. `button_mount`: sede del pulsante, posizione da scegliere (`OPEN-017`).
7. `sensor_carrier`: supporto dell'SHT40 nella camera ventilata (dipende dal modulo reale).
8. `body_shell`: oltre ai gusci, il canale del cavetto display dalle gambe al collo.

La scomposizione dei gusci della chibi dipende dal servizio di stampa (`DEC-052`, `OPEN-032`).

La scomposizione è una proposta; può cambiare a seconda di vincoli di stampa, colorazione e cablaggio.

## 5. Supporto display

- Appoggio rigido e ripetibile per il PCB, senza carichi sulla parte attiva del display.
- Cornice che **non** copra le cifre: verificare l'area visibile sul pannello reale.
- Niente colla permanente sul display/PCB che impedisca la manutenzione.
- Nessuna vite a contatto con il vetro; se si usano inserti filettati termici, montarli prima di introdurre l'elettronica.
- Punti di test e pad BOOT/RESET del PCB accessibili con sportellino aperto; il flashing normale avviene dalla USB-C posteriore.
- Definire protezione dei flessibili e del bordo del display da sfregamento con la stampa.

## 6. Porta USB-C posteriore (retro della base)

- Montaggio **incassato** sul retro della base d'appoggio (`DEC-048`), invisibile frontalmente.
- Scheda principale avvitata a due colonnine della base, in modo che lo sforzo del cavo vada sulle viti e sulla scocca, non sulle saldature della USB-C (le linguette di J1 sono saldate a mano, `DEC-047`).
- Apertura di 13,4 × 7,6 mm in cui entra il sovrastampo della spina: grande abbastanza per i cavi comuni, ma non invasiva (§12).
- Prova di inserimento con cavi diversi (forma e lunghezza del sovrastampo).
- La presa è a circa 9 mm dal piano e il cavo esce quasi a livello del tavolo: verificare che la statuetta resti dritta e stabile con il cavo inserito e con una trazione accidentale leggera (`OPEN-022`, `VT-MEC-003`).

## 7. Gestione termica e aerazione sensore

- Sensore ambiente in sede raggiunta da ricambio d'aria, senza soffiare aria calda dal circuito principale.
- Non alloggiare SHT40 immediatamente dietro il display o contro la scheda principale.
- Introdurre piccoli fori o feritoie discreti; evitare cavità totalmente chiusa se si richiede una misura rappresentativa della stanza.
- Valutare materiale della scocca e temperatura interna in funzionamento continuo (alimentazione 24/7).
- Validare l'errore dovuto ad autosurriscaldamento con confronto su banco, prima e dopo chiusura scocca.

## 8. Stampa e finitura (proposta)

| Elemento | Proposta iniziale |
|---|---|
| Materiale | PLA per primi mockup dimensionali; PETG da valutare dopo le prove termiche |
| Colori | Blu scuro corpo/cappello, nero stivali, capelli a scelta, dettagli dorati/azzurri |
| Metodo | Parti separate per favorire finitura e montaggio |
| Fissaggi | Viti e sedi filettate/inserti compatibili |
| Base | Fondo più pesante/stabile, feltrini o gommini antiscivolo |
| Display | Lasciare libera l'area attiva; eventuale vetrino/protezione da validare |
| Pulsante | Corsa e sensazione provate su stampa test |

L'adozione di PETG o PLA non elimina la necessità di un test termico: le temperature interne sono sconosciute finché non si misura il prototipo.

## 9. Test meccanici / criteri di accettazione

- Assemblaggio e disassemblaggio ripetuti senza deformazione o danno ai cavi.
- Nessuna pressione del frontale sul vetro o sul flessibile del display.
- Accesso a USB e BOOT/RESET secondo la strategia di service.
- Stabilità su piano, senza cavo e con cavo, anche premendo il pulsante.
- SHT40 esterno rileva condizioni della stanza con errore aggiuntivo dovuto al case valutato e documentato.
- Assenza di surriscaldamenti nella scocca in funzionamento continuo.

## 10. Strumenti CAD (`DEC-022`)

- **Blender**: forma della chibi (testa, capelli, cappello, corpo, posa), booleane finali con le parti tecniche, divisione in pezzi stampabili, render. Bozza a volumi semplici anche via script; scultura artistica a mano.
- **CAD a codice** (build123d, `CAND-021`): parti tecniche interne parametriche (supporti, vani, staffe, sportello), legate allo STEP delle schede esportato da KiCad; esportazione STEP/STL.
- **Servizio di stampa online** (`DEC-052`, servizio da scegliere in `OPEN-032`): orientamento, supporti e tolleranze secondo le sue regole. Non c'è una stampante del proprietario.

## 11. File CAD

Presenti dal 2026-11-09 (istruzioni in [mechanical/README.md](../mechanical/README.md)):

- `mechanical/cad/parametri.py`, `studio_base.py`: studio volumetrico parametrico della base (build123d), con il rapporto generato `studio_base_rapporto.txt`.
- `mechanical/prints/base-guscio.stl`, `base-fondo.stl`: base dello studio, per una **prova dimensionale 1:1** con la scheda reale (non il pezzo finale); `studio-volumi-base.step`: assieme con gli ingombri.
- `mechanical/blender/blockout_chibi.py`, `policlock_blockout.blend`: blockout della chibi a volumi semplici, punto di partenza della scultura a mano.
- `assets/renders/blockout-*.png`: render del blockout.

Da fare in una milestone successiva: `mechanical/drawings/` (quote principali e sezioni), distinta degli elementi stampati e note di montaggio.

## 12. Studio volumetrico 1:1 e blockout (2026-11-09)

Primo studio dopo `DEC-048` (scheda nella base). Nessuna parte è ancora definitiva: le quote sono **proposte** (`CAND-026`) da confermare con i render e con una stampa di prova sulla scheda reale. Display e SHT40 sono segnaposto (`OPEN-016`).

**Riferimento.** X verso destra guardando la statuetta da davanti, Y verso il retro, Z verso l'alto, tavolo a Z = 0. Origine in pianta sull'asse del connettore display J2, che è anche l'asse del corpo. La scheda è ruotata di 180°: bordo della USB-C verso il retro, header J2 verso il fronte, antenna a sinistra (−X).

### 12.1 Base d'appoggio

| Voce | Valore proposto | Note |
|---|---|---|
| Ingombro esterno | **78,5 × 76,3 × 24,1 mm** (larghezza × profondità × altezza), X −39,0…39,5 | Forma a "D": retro piatto per la USB-C (raggi 5 mm), fronte arrotondato (raggi 18 mm); nel concept a cubetti raggi di 5 e 4 mm (§13). Pareti 2 mm, piano superiore 2,5 mm, fondo 2,5 mm |
| Minimo della sola scheda | 57,5 × 47,7 × 17,2 mm | Senza moduli, zavorra, piedi e pieghe dei cavi JST. La base cresce a destra per DS3231 e SHT40, davanti per piedi e zavorra, in altezza per le spine JST PH con il cavo dall'alto (14 mm sopra la scheda, da verificare con la prova 1:1 FIN-011) |
| Scheda | X −35,5…15,0; Y −4,4…37,1; lato inferiore a Z 6,0 (asse del corpo sul centro dei pin 1–7 di J2, header 1×8 dal `DEC-049`) | 3,5 mm di luce sotto la scheda per i piedini di J2–J5 (1,81 mm) e le teste delle viti |
| Fissaggio della scheda | Due colonnine Ø 5,5 mm che scendono dal piano superiore ai fori M2 (X −9,20 e −28,70, Y 33,6); viti M2 dal basso | Lo sforzo del cavo USB va sulla scocca. Due colonnine Ø 4 mm sul fondo sostengono gli angoli anteriori della scheda quando si innesta il cavetto display |
| USB-C | Asse a X −18,70, **Z 9,1 mm** dal tavolo; apertura 13,4 × 7,6 mm (raggi 1,5) nella parete posteriore | Il sovrastampo della spina (segnaposto 12,4 × 6,5 mm) entra nell'apertura fino alla presa |
| DS3231 (Adafruit 5188) | Culla con due guide sotto il piano, angolo posteriore destro (X 18,5…36,3, Y 11,4…36,8) | **Pila CR1220 rivolta verso il fondo**: si cambia togliendo il fondo, senza staccare cavi (`OPEN-026`). Quote 25,4 × 17,8 × 7,8 mm dalla pagina Adafruit (2026-11-09) |
| SHT40 | Camera separata sul lato destro (interno X 17,5…37,5, Y −16…8), modulo in piedi contro la parete con 6 feritoie da 1,6 mm; 4 feritoie nel fondo | Lontano dal display (testa) e a circa 25 mm dall'LDO (`OPEN-011`). Con il cavetto Dupont il modulo occupa quasi tutta la camera: valutare fili saldati direttamente sul modulo, scelta del proprietario |
| Zavorra | Vasca nella striscia anteriore del fondo (Y −34…−19,5), circa **15 cm³**: circa 69 g di pallini d'acciaio o circa 118 g di piastrine | Oltre 15 mm dall'antenna (18,1 mm). Vasca chiusa (coperchio o resina); 0,8 mm di gioco dalla parete della camera SHT40 (correzione del 2026-11-10) |
| Sportello di servizio | Il fondo stesso: 2 viti M2,5 davanti, 2 linguette dietro | Accesso al retro della scheda (TP6/TP11 per il recupero, `DEC-039`), alle viti, alla pila e alla zavorra (`OPEN-008`) |
| Fissaggio del corpo | 2 viti M3 dal basso negli stivali (X ±10, Y −12) | Accessibili togliendo il fondo |
| Massa stimata | Base in PLA circa 56 g se piena (meno con il riempimento reale); statuetta completa circa 200–260 g con la zavorra | Da pesare sul prototipo |

**Controlli automatici** (`studio_base.py`, rapporto in `mechanical/cad/studio_base_rapporto.txt`):

- Interferenze fra le parti stampate e gli ingombri (scheda dallo STEP di KiCad, componenti alti misurati sullo STEP completo, spine, moduli, zavorra): **PASS**, nessun volume in comune.
- Metallo ad almeno **15 mm dall'antenna** del WROOM-02 (DEC-012, R2-004): **PASS**. Minimo 15,1 mm (vite M2 del foro H2); zavorra 18,1 mm; viti del corpo 18,6 e 36,2 mm; viti del fondo 22,4 e 56,7 mm (valori con J2 1×8, rieseguiti il 2026-11-10). Per avere margine si possono usare viti in nylon sul foro H2.
- Il modello 3D della USB-C (HRO TYPE-C-31-M-12) non è nella libreria di KiCad 10: nello studio è un blocco con le quote del disegno HRO (8,94 × 7,35 × 3,16 mm).

### 12.2 Header J2 e cavetto display

- **Header diritto (consigliato, `CAND-027`)**: con J2 1×8 (`DEC-049`) il corpo dell'header va da X −11,4 a 8,9 (resta sotto il piano della base); la spina Dupont a 7 vie sui pin 1–7 sale in verticale da Z 10,1 a Z 24,1 e arriva al piano superiore della base. I fili entrano direttamente nel canale del corpo, che misura **21 × 6 mm** e va dal piano della base al collo passando per le gambe unite e il busto. La sezione del canale lascia passare una spina Dupont a 7 vie: il cavetto si infila anche senza dividere il corpo in due gusci.
- **Header a 90° (quello del progetto KiCad)**: piedini fino a 5,64 mm oltre il bordo, spina orizzontale fino a Y −24 e piega dei fili. Servirebbero **circa 25 mm di base in più** davanti alla scheda, oppure gambe più avanti rispetto alla base.
- La scelta spetta al proprietario, che salda l'header (`OPEN-031`).
- **Lunghezza**: dalla spina sulla scheda a quella sul modulo display (pin vicino al bordo inferiore dell'aletta, Z circa 79, spina orizzontale verso il retro) il percorso è di circa 65 mm. Un **cavetto Dupont da 10 cm** lascia circa 35 mm di gioco per montare la testa a parte (`OPEN-021`: la prova SPI va fatta con questo cavetto).

### 12.3 Blockout della chibi (Blender)

Volumi semplici per proporzioni e ingombri (`mechanical/blender/blockout_chibi.py`). Base importata dallo studio build123d e chibi **in piedi** (`DEC-051`). Il blockout usa uniforme e cappello generici, senza fregi ufficiali.

| Parte | Quote (Z dal tavolo) |
|---|---|
| Base | 0…24,1 |
| Stivali / gambe unite | 24…34 / 33…50 |
| Busto con giacca svasata, braccia | 46…80 |
| Testa (forma squadrata e arrotondata) | 68 × 56 × 70 mm, Z 65…135 |
| Display | Centro a Z 103; vetro Ø 37,5 mm (segnaposto), area attiva Ø 32,4 |
| Cappello con visiera | Fino a circa Z 150 |

- **Vincolo trovato sulla testa**: con il modulo segnaposto 38 × 45,5 mm e l'aletta dei pin in basso, una testa di 64 mm con spigoli molto arrotondati fa uscire l'aletta sotto il mento. Servono una testa alta circa 70 mm con il volto piatto di almeno 46 × 48 mm (raccordi ≤ 11 mm), oppure il modulo ruotato di 180° (aletta in alto, immagine ruotata dal firmware con il registro MADCTL del GC9A01). Si decide sul modulo misurato (`OPEN-016`).
- Proporzioni: testa 70 mm su circa 150 mm totali (circa 47 %), coerente con lo stile chibi; la base è un piedistallo ben visibile (24 mm), da caratterizzare nello stile (fascia, targhetta generica).

### 12.4 Pulsante (`OPEN-017`), stabilità (`OPEN-022`)

- **A, sommità del cappello**: si preme verso il basso, lungo l'asse della statuetta, senza momento di ribaltamento. Il cavo J5 (2 fili) sale nello stesso canale fino alla testa, lungo circa 20 cm.
- **B, fronte della base**: cavo corto; la spinta orizzontale a circa 12 mm dal tavolo spinge la base all'indietro, con 76 mm di profondità di appoggio.
- **Sconsigliato sul petto**: con una massa di circa 220 g e il baricentro a circa 41 mm dal bordo anteriore della base, una spinta a 65 mm di altezza ribalta la statuetta già con circa 1,4 N. Un tasto tattile comune richiede 1,6–2,5 N.
- **Cavo USB**: con l'asse a 9,1 mm dal tavolo e circa 35 mm fra baricentro e bordo posteriore, servono circa 8 N di trazione all'indietro per ribaltarla. Il rischio maggiore è lo scivolamento: gommini antiscivolo e zavorra. Da provare con `VT-MEC-003`.

### 12.5 Domande aperte per il proprietario

Header J2 diritto o a 90° (`OPEN-031`); posizione del pulsante, A o B (`OPEN-017`); fondo come sportello (`OPEN-008`); DS3231 nella culla con la pila verso il fondo (`OPEN-026`); cavo dell'SHT40 saldato o con spina Dupont; servizio e tecnologia di stampa (`OPEN-032`); commenti estetici sui render e riferimenti di stile; chiusura di `OPEN-028` per la parte scheda (il PCB non richiede modifiche).

## 13. Concept 3D a cubetti, versione 2 (2026-11-10)

Concept dello stile scelto dal proprietario, **parametrico in build123d** (`mechanical/cad/concept_voxel.py`), con Blender solo per colori, luci e render (`mechanical/blender/render_concept.py`). Non è ancora il modello da stampare: proporzioni, colori e divisione dei pezzi aspettano il parere del proprietario.

La **versione 1** (commit `1afd055`) aveva una testa di 70 × 64 × 70 mm, una larga cornice di pelle attorno al display e un'altezza di 167 mm. Sul parere del proprietario la **versione 2** (`DEC-054`) ha busto e gambe più lunghi e una testa piccola in cui **il display è tutto il volto**.

**Render** (`assets/renders/`):
- con il quadrante: `concept-fronte.png`, `concept-tre-quarti.png`;
- con la faccia emoji (idea del proprietario, [05](05-interfaccia-utente.md) §10): `concept-fronte-emoji.png`, `concept-tre-quarti-emoji.png`;
- `concept-lato.png`, `concept-retro.png` (USB-C), `concept-esploso.png`, `concept-sezione.png` (scheda, cavetto, aletta del display nel busto).

**File**: una STL per parte in `mechanical/prints/concept/` (26 parti) e l'assieme `mechanical/prints/concept-statuetta.step`; rapporto in `mechanical/cad/concept_rapporto.txt`.

### 13.1 Quote

| Voce | Valore |
|---|---|
| Altezza totale | **153 mm**, dentro i 130–160 indicativi di `SC-006` (v1: 167 mm) |
| Ingombro in pianta | 78,5 × 76,3 mm: è la base, la figura non sporge |
| Base | 78,5 × 76,3 × 24,1 mm, dallo studio del §12 con spigoli "a blocco" (raggi 5/4 mm) |
| Testa | Cubo **48 × 40 × 48 mm**, Z 90,1…138,1; cappello fino a Z 153,1. Testa e cappello sono il 41 % dell'altezza (2,4 teste, come il riferimento) |
| Volto | Il display: finestra Ø 38 mm, centro a Z 111,1, in una piastra di pelle larga 40 mm (1 mm ai lati della finestra, 2 mm sotto); capelli di 4 mm ai lati e frangia sopra |
| Corpo | Stivali Z 24,1…34,1; pantaloni …58,1 (24 mm, v1: 16); cintura …62,1; busto …90,1 (28 mm, v1: 23); braccia con manica corta, risvolto e avambraccio fino a Z 56 |
| Cavetto display | Canale 21 × 6 mm libero dalla base alla cavità del busto; percorso fra le spine circa 68 mm, Dupont da 10 cm con circa 30 mm di gioco |

### 13.2 Il display scende nel busto

Per avere una testa piccola, la parte tonda del modulo (segnaposto Ø 38 mm, spesso 4,8 mm) resta dietro la finestra del volto. **L'aletta dei pin** (segnaposto largo 26 mm, `P.DISPLAY_ALETTA_L`) e **la spina Dupont** scendono da un foro a "T" nel pavimento della testa in una cavità in cima al busto: l'aletta arriva 5,8 mm sotto la testa (Z 84,3), la spina va da Y −9,2 a 7,3 a Z 86,8. Il busto è spostato in avanti (Y −16…12) perché il volto e il fronte del busto coincidono.

- **Montaggio**: si collega il cavetto al modulo, si infila il modulo da dietro nella cornice del volto, si chiude la testa con `testa_retro` e si appoggia la testa sul busto. Aletta e spina entrano nella cavità e due spine Ø 3 mm (X ±14, Y 2) allineano la testa.
- **Manutenzione**: la testa si sfila verso l'alto; il cavetto ha gioco nel busto.
- **Fermo del modulo**: da definire sul modulo reale (fori del PCB, se presenti, o una cornice premuta da `testa_retro`). Anche aletta e posizione dei pin vanno misurate (`OPEN-016`).
- **Alternativa**: fili saldati direttamente sui pin del modulo invece della spina Dupont, se la spina non entra con il modulo reale.

**Controlli automatici:** nessuna sovrapposizione fra le 26 parti, compreso guscio/fondo della base. Modulo (tondo + aletta) e spina senza interferenze. Canale libero. Le verifiche della base (interferenze, antenna) sono quelle del §12.

### 13.3 Parti per colore (proposta)

| Gruppo | Parti | Note di stampa |
|---|---|---|
| Base | `base_guscio` (grigio), `base_fondo` (grigio scuro) | Guscio capovolto; il fondo è lo sportello |
| Gambe | `stivale_dx`, `stivale_sx` (nero), `pantaloni` (azzurro), `banda_dx/sx` (rosso, 0,8 mm) | Gli stivali hanno mezzo canale ciascuno e l'inserto M3 della vite dalla base |
| Vita | `cintura` con fondina e tasca (nero), `fibbia` (grigio) | Anello attraversato dalle spine |
| Busto | `busto` con maniche, risvolti, colletto e taschini (blu notte), `braccio_dx/sx` (pelle), `spallina_dx/sx` (rosso), `grado_dx/sx` (oro, 0,6 mm) | Busto in piedi, con la cavità per l'aletta del display |
| Insegne (`DEC-053`) | `targhetta` + `scritta_polizia` (lettere 0,5 mm), `toppa_verde/bianco/rosso`, `fregio` a pixel 1,4 mm | Dettagli piccoli: stampa multicolore o pittura |
| Testa | `testa_retro` con la coda e `testa_fronte` (castano), `volto` con la finestra (pelle, 2 mm) | Retro con la nuca sul piatto, supporti sotto la coda; fronte e retro uniti con viti M2 dal pavimento |
| Cappello | `cappello` cavo, pareti 2,5 mm (blu notte) | Capovolto: la fascia sporge di 2–5 mm |

**Giunzioni del concept:** spine di allineamento Ø 3 mm (fori Ø 3,2, profondi 4 mm) a X ±14 fra stivali, pantaloni, cintura e busto, e a (±14; 2) fra busto, testa e cappello; braccia su spine Ø 3 sotto le maniche; viti M3 dalla base negli stivali. Gioco fra le parti incastrate 0,2 mm: valore di partenza.

**Base (§12)**: resta 78,5 × 76,3 × 24,1 mm. La larghezza dipende dalla scheda (minimo 57,5 mm) più la zona di DS3231 e SHT40 sul lato destro; la profondità dipende dalla zavorra davanti agli stivali. Si potrebbe stringere solo spostando DS3231 o SHT40, cioè con un nuovo studio: proposta da valutare con il proprietario, non applicata.

### 13.4 Scelte aperte per il proprietario

- **Proporzioni**: 153 mm con testa 48 mm; il pannello resta segnaposto finché non arriva il modulo (`OPEN-016`).
- **Colori**: tonalità di blu della camicia e dei pantaloni, castano dei capelli, grigio della base.
- **Tecnologia e servizio** (`OPEN-032`): FDM multicolore (parti nei loro colori, dettagli fino a circa 0,4 mm), SLS/MJF in nylon (monocolore o tinto, poi pittura; pareti ≥ 0,8–1 mm), resina (dettagli fini, da dipingere). Tolleranze tipiche da verificare sulle pagine del servizio: circa 0,2–0,3 mm in FDM, 0,3–0,4 mm in SLS/MJF, 0,1–0,2 mm in resina.
- **Dettagli sottili**: bande, gradi e lettere sotto 1 mm vanno ingrossati per SLS/MJF o dipinti.
- **Parti piene**: busto e pantaloni si possono svuotare per ridurre costo e peso con i servizi che fanno pagare il volume.
- **Faccia emoji** e quadrante: domande in [05](05-interfaccia-utente.md) §10.
- Restano le domande del §12.5 (header J2, pulsante, sportello, DS3231, cavo SHT40).
