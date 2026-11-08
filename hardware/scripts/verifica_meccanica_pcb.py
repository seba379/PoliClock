"""Verifica in sola lettura di margini dal bordo e courtyard della scheda principale.

Usare il Python di KiCad 10. Il corpo e' ricavato dalle geometrie F.Fab, senza
testi e senza lo spessore del tratto grafico. Supporta il contorno ortogonale
attuale. J1 a bordo e U3 sopra l'intaglio richiedono ancora accettazione DFM;
sono eccezioni esplicite, non parti dichiarate conformi al margine di 2,5 mm.

La regola JLC dei 2,5 mm corpo-bordo vale solo per le parti montate da JLC. Le parti
saldate a mano dal proprietario (DEC-043: J2-J5, attributo "escluso dai file di
posizionamento", quindi assenti dalla CPL) non hanno margine dal bordo, ma il loro
courtyard si controlla comunque. Le regole di fabbricazione (distanze, anelli, rame-bordo)
valgono per tutte le piazzole e sono verificate dal DRC.
"""
import argparse
import json
import math
from pathlib import Path

import pcbnew

PCB = Path(__file__).resolve().parents[1] / 'policlock-main/policlock-main.kicad_pcb'
MARGINE = 2.5
ECCEZIONI_DFM = {
    'J1': 'USB-C affacciata al bordo inferiore: accettazione DFM aperta',
    'U3': 'Modulo ESP32 sopra intaglio antenna: accettazione DFM aperta',
}
CONNETTORI = ('J2', 'J3', 'J4', 'J5')


def mm(value):
    return pcbnew.ToMM(value)


def corpo_bbox(fp):
    boxes = []
    for item in fp.GraphicalItems():
        if not isinstance(item, pcbnew.PCB_SHAPE) or item.GetLayer() != pcbnew.F_Fab:
            continue
        box = item.GetBoundingBox()
        stroke = item.GetWidth() / 2
        boxes.append((box.GetLeft() + stroke, box.GetTop() + stroke,
                      box.GetRight() - stroke, box.GetBottom() - stroke))
    if not boxes:
        return None
    return tuple(mm(v) for v in (min(b[0] for b in boxes), min(b[1] for b in boxes),
                                max(b[2] for b in boxes), max(b[3] for b in boxes)))


def distanza(box, edge):
    x0, y0, x1, y1 = box
    ax, ay, bx, by = edge
    if ax == bx:
        dx = max(x0 - ax, 0, ax - x1)
        dy = max(y0 - max(ay, by), 0, min(ay, by) - y1)
    elif ay == by:
        dx = max(x0 - max(ax, bx), 0, min(ax, bx) - x1)
        dy = max(y0 - ay, 0, ay - y1)
    else:
        raise ValueError('Contorno non ortogonale: aggiornare la verifica meccanica')
    return math.hypot(dx, dy)


def dentro_scheda(x, y, edges):
    inside = False
    for ax, ay, bx, by in edges:
        if (ay > y) != (by > y) and x < ax + (bx - ax) * (y - ay) / (by - ay):
            inside = not inside
    return inside


def controlla(board):
    edges = []
    for shape in board.GetDrawings():
        if shape.GetLayer() != pcbnew.Edge_Cuts:
            continue
        if shape.GetShape() != pcbnew.SHAPE_T_SEGMENT:
            raise ValueError('Contorno con archi: aggiornare la verifica meccanica')
        a, b = shape.GetStart(), shape.GetEnd()
        edges.append((mm(a.x), mm(a.y), mm(b.x), mm(b.y)))
    if not edges:
        raise ValueError('Contorno scheda assente')

    result = {'kicad': pcbnew.GetBuildVersion(), 'margine_minimo_mm': MARGINE,
              'eccezioni_dfm_aperte': ECCEZIONI_DFM, 'margini_corpi_mm': {},
              'montaggio_a_mano': [], 'copertura_courtyard': {}, 'errori': []}
    for fp in board.GetFootprints():
        ref = fp.GetReference()
        if fp.IsDNP():
            continue
        # parti saldate a mano: campo Montaggio (DEC-043); devono essere fuori dalla CPL di JLC
        a_mano = fp.HasField('Montaggio') and 'mano' in fp.GetFieldText('Montaggio')
        if a_mano:
            result['montaggio_a_mano'].append(ref)
            if not fp.IsExcludedFromPosFiles():
                result['errori'].append(f'{ref}: montata a mano ma non esclusa dai file di posizionamento')
        # margine di 2,5 mm solo per le parti nella CPL (montate da JLC); punti di test, fori e fiducial esclusi
        if ref not in ECCEZIONI_DFM and not fp.IsExcludedFromPosFiles():
            box = corpo_bbox(fp)
            if box is None:
                result['errori'].append(f'{ref}: contorno del corpo F.Fab assente')
            else:
                margin = min(distanza(box, e) for e in edges)
                result['margini_corpi_mm'][ref] = round(margin, 4)
                if not all(dentro_scheda(x, y, edges)
                           for x in (box[0], box[2]) for y in (box[1], box[3])):
                    result['errori'].append(f'{ref}: corpo fuori dal contorno scheda')
                if margin < MARGINE - 0.0001:
                    result['errori'].append(f'{ref}: corpo-bordo {margin:.4f} mm < {MARGINE}')
        if ref not in CONNETTORI:
            continue
        fp.BuildCourtyardCaches()
        courtyard = fp.GetCourtyard(pcbnew.F_CrtYd)
        failures = []
        fab = [i for i in fp.GraphicalItems()
               if isinstance(i, pcbnew.PCB_SHAPE) and i.GetLayer() == pcbnew.F_Fab]
        if not fab:
            failures.append('F.Fab assente')
        if not courtyard.OutlineCount():
            failures.append('courtyard assente')
        else:
            items = list(fp.Pads()) + fab
            for item in items:
                bb = item.GetBoundingBox()
                corners = [(bb.GetLeft(), bb.GetTop()), (bb.GetRight(), bb.GetTop()),
                           (bb.GetRight(), bb.GetBottom()), (bb.GetLeft(), bb.GetBottom())]
                if not all(courtyard.Contains(pcbnew.VECTOR2I(x, y)) for x, y in corners):
                    label = 'pad ' + item.GetNumber() if isinstance(item, pcbnew.PAD) else 'F.Fab'
                    failures.append(label)
        result['copertura_courtyard'][ref] = {'ok': not failures, 'elementi_fuori': failures}
        if failures:
            result['errori'].append(f'{ref}: elementi fuori dal courtyard: {failures}')
    result['esito'] = 'FAIL' if result['errori'] else 'PASS'
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pcb', nargs='?', type=Path, default=PCB)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = controlla(pcbnew.LoadBoard(str(args.pcb.resolve())))
    encoded = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        args.output.write_text(encoded + '\n', encoding='utf-8')
    print(encoded)
    return 1 if result['errori'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
