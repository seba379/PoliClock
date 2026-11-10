# Assets di progetto

- `concept/policlock-concept-prodotto.svg` — concept del prodotto finito (fronte e retro con USB-C sul sedere, posizione superata da `DEC-048`: retro della base), **illustrativo**: proporzioni, colori e dettagli non sono quote CAD.
- `concept/policlock-schema-blocchi.svg` — schema a blocchi dei componenti e dei collegamenti (v0.5, senza batteria); la fonte normativa resta `docs/02-architettura-hardware.md`.
- `concept/policlock-chibi-concept.png` — **riferimento visivo NON normativo**, generato durante il brainstorming. Mostra la poliziotta chibi con display rotondo al posto del volto. Alcuni dettagli del pannello grafico (funzioni domotiche, CO2, statistiche o schede hardware specifiche) sono **esempi estetici**, non requisiti della V1 e non componenti approvati.
- `concept/riferimento-stile-chibi-voxel.webp` — **riferimento di stile del proprietario** (chibi a cubetti), salvato con il suo consenso il 2026-11-10. Solo illustrativo: non è una fonte per quote, cablaggi o funzioni. Insegne, scritte e bandiera dell'immagine **non** si copiano: nel modello ci sono solo le versioni stilizzate di `DEC-053`.
- `renders/concept-*.png` — render del **concept a cubetti v2** (2026-11-10, `DEC-054`) da `mechanical/blender/render_concept.py` sulla geometria di `mechanical/cad/concept_voxel.py`: fronte e tre quarti con il quadrante e con la faccia emoji (`*-emoji.png`), lato, retro con la USB-C, esploso e sezione con scheda, cavetto e aletta del display nel busto. Quadrante ed emoji sono illustrativi. Il concept v1 è nella storia Git (commit `1afd055`).
- `renders/blockout-*.png` — render del **blockout a volumi semplici** (2026-11-09) generati da `mechanical/blender/blockout_chibi.py`: fronte, lato, retro con la USB-C, vista di tre quarti e sezione della base con gli ingombri. Proporzioni e ingombri di studio, non la scultura finale; display e SHT40 sono segnaposto.
- `ui/` — futuri mockup e risorse grafiche originali del firmware.

Per il prodotto V1 valgono `README.md` e `docs/01-requisiti-prodotto.md`: **ora, data, temperatura, umidita', alimentazione continua da USB-C posteriore (nessuna batteria), display attenuato con aumento temporaneo di luminosita', spento di notte**.

Non utilizzare il concept come prova di assemblabilita', misure dimensionali, schema elettrico o BOM definitiva. Verificare prima di riusarlo pubblicamente eventuali stemmi/loghi riconducibili a enti ufficiali.
