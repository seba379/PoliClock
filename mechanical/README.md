# Meccanica di PoliClock

Stato (2026-11-10): **primo concept 3D a cubetti**, parametrico in build123d, da rivedere con il proprietario; prima ancora studio volumetrico della base e blockout neutro. Quote, verifiche e domande aperte in [docs/06](../docs/06-progettazione-meccanica.md) §12–13; decisioni `DEC-048` (scheda nella base, USB-C sul retro), `DEC-051` (chibi in piedi), `DEC-052` (stampa con un servizio online) e `DEC-053` (stile a cubetti, insegne stilizzate) in [docs/10](../docs/10-decisioni-aperte.md).

## Contenuto

| Percorso | Cosa contiene |
|---|---|
| `cad/parametri.py` | Quote condivise, ognuna con la sua fonte (STEP di KiCad, PCB, documentazione, pagina del produttore, segnaposto) |
| `cad/studio_base.py` | Studio parametrico della base in build123d: guscio, fondo apribile, ingombri, controlli di interferenza e di distanza dall'antenna, rapporto ed esportazioni |
| `cad/studio_base_rapporto.txt` | Rapporto generato: quote della base, volumi, interferenze, distanze dall'antenna |
| `prints/base-guscio.stl`, `prints/base-fondo.stl` | Base dello studio per una **prova dimensionale 1:1** con la scheda reale (non pezzi finali) |
| `prints/studio-volumi-base.step` | Assieme con base e ingombri, da aprire in un CAD o in OCP CAD Viewer |
| `cad/concept_voxel.py` | **Concept a cubetti** parametrico: 27 parti per colore (base dallo studio), controlli di sovrapposizione, modulo display e canale del cavetto |
| `cad/concept_rapporto.txt` | Rapporto generato del concept: quote, parti, volumi, controlli |
| `prints/concept/*.stl`, `prints/concept-statuetta.step` | Parti del concept (una STL per parte) e assieme; **non** pronte per la stampa |
| `blender/render_concept.py`, `blender/policlock_concept.blend` | Colori, luci e render del concept in `assets/renders/concept-*.png` |
| `blender/blockout_chibi.py` | Blockout della chibi a volumi semplici e render in `assets/renders/` |
| `blender/policlock_blockout.blend` | File Blender generato dallo script, punto di partenza per la scultura a mano |
| `cad/out/` | Ingombri in STL per Blender, rigenerati dallo studio (non versionati) |

## Come rigenerare

Dalla radice del repository, con il venv `.venv-cad` (fuori dal repository) e Blender 5.2:

```bash
../.venv-cad/Scripts/python.exe mechanical/cad/studio_base.py
```

```bash
"C:/Program Files/Blender Foundation/Blender 5.2/blender.exe" --background --python mechanical/blender/blockout_chibi.py
```

Per il concept a cubetti:

```bash
../.venv-cad/Scripts/python.exe mechanical/cad/concept_voxel.py
```

```bash
"C:/Program Files/Blender Foundation/Blender 5.2/blender.exe" --background --python mechanical/blender/render_concept.py
```

Lo studio della base rigenera STL, STEP, rapporto e ingombri; il blockout importa la base e gli ingombri, salva il `.blend` e i render. Il concept rigenera le parti e i dati per Blender in `cad/out/concept/`; il render le colora e salva `policlock_concept.blend`. Con `--viewer` lo studio mostra il modello in OCP CAD Viewer (VS Code).

## Avvertenze

- Display GC9A01 e modulo SHT40 sono **segnaposto** finché non arrivano i moduli reali (`OPEN-016`); il DS3231 usa le quote della pagina Adafruit 5188.
- Giochi e spessori (0,3 mm, pareti 2 mm) sono valori di partenza: vanno adattati alle regole del servizio di stampa scelto (`OPEN-032`).
- Insegne solo stilizzate (`DEC-053`): fregio generico a pixel, scritta "POLIZIA", toppa tricolore; nessuna insegna o marchio ufficiale.
