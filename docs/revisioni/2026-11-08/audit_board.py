"""Read-only snapshot diagnostics; run from anywhere with KiCad 10's Python.

Requires the unchanged repository's sexp parser and kicad-cli. Writes only
board-audit.json beside this script. Does not run ERC/DRC or validate production.
"""
import collections
import csv
import hashlib
import heapq
import json
import math
import pathlib
import subprocess
import sys
import tempfile

import pcbnew as p

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'hardware/scripts'))
from sexp import parse, find, find1

def mm(n):
    return round(p.ToMM(n), 6)

def xy(v):
    return [mm(v.x), mm(v.y)]

board = p.LoadBoard(str(ROOT / 'hardware/policlock-main/policlock-main.kicad_pcb'))
fps = {f.GetReference(): f for f in board.GetFootprints()}
tracks = list(board.GetTracks())
pads = list(board.GetPads())

def pad(ref, n):
    return next(z for z in fps[ref].Pads() if z.GetNumber() == str(n))

summary = {'kicad': p.GetBuildVersion(), 'files': {}}
for f in (ROOT / 'hardware').rglob('*'):
    if f.is_file() and f.suffix in ('.kicad_pcb', '.kicad_pro', '.kicad_sch', '.kicad_mod', '.kicad_sym', '.csv'):
        summary['files'][str(f.relative_to(ROOT)).replace('\\', '/')] = hashlib.sha256(f.read_bytes()).hexdigest()
summary['thickness_mm'] = mm(board.GetDesignSettings().GetBoardThickness())
summary['outline'] = [[xy(s.GetStart()), xy(s.GetEnd())] for s in board.GetDrawings() if s.GetLayer() == p.Edge_Cuts]
summary['tracks'] = {'count': sum(t.GetClass() != 'PCB_VIA' for t in tracks),
    'vias': sum(t.GetClass() == 'PCB_VIA' for t in tracks),
    'widths_mm': dict(collections.Counter(mm(t.GetWidth()) for t in tracks if t.GetClass() != 'PCB_VIA')),
    'total_length_mm': round(sum(mm(t.GetLength()) for t in tracks if t.GetClass() != 'PCB_VIA'), 3)}
summary['via_geometries'] = dict(collections.Counter(str((mm(t.GetWidth(p.F_Cu)), mm(t.GetDrillValue()))) for t in tracks if t.GetClass() == 'PCB_VIA'))
summary['net_tracks'] = {}
for t in tracks:
    n = t.GetNetname()
    v = summary['net_tracks'].setdefault(n, {'length_mm': 0, 'vias': 0, 'widths_mm': set()})
    if t.GetClass() == 'PCB_VIA':
        v['vias'] += 1
    else:
        v['length_mm'] += mm(t.GetLength())
        v['widths_mm'].add(mm(t.GetWidth()))
for v in summary['net_tracks'].values():
    v['length_mm'] = round(v['length_mm'], 3)
    v['widths_mm'] = sorted(v['widths_mm'])

summary['footprints'] = {}
for ref, f in sorted(fps.items()):
    f.BuildCourtyardCaches()
    cy = f.GetCourtyard(p.F_CrtYd)
    bb = cy.BBox()
    libid = f.GetFPID()
    summary['footprints'][ref] = {'value': f.GetValue(), 'id': str(libid.GetLibNickname())+':'+str(libid.GetLibItemName()),
        'xy': xy(f.GetPosition()), 'rotation': f.GetOrientationDegrees(), 'side': f.GetLayerName(),
        'bom_excluded': f.IsExcludedFromBOM(), 'cpl_excluded': f.IsExcludedFromPosFiles(),
        'courtyard': [mm(bb.GetLeft()), mm(bb.GetTop()), mm(bb.GetRight()), mm(bb.GetBottom())] if cy.OutlineCount() else None,
        'pads': [{'n': z.GetNumber(), 'net': z.GetNetname(), 'xy': xy(z.GetPosition()),
            'size': xy(z.GetSize()), 'drill': xy(z.GetDrillSize()), 'attr': z.GetAttribute(),
            'paste': z.IsOnLayer(p.F_Paste)} for z in f.Pads()]}

# Compare component fields and pin nets in the freshly exported netlist and saved netlist.
def netlist(path):
    r = parse(path.read_text(encoding='utf-8'))[0]
    nets = {(find1(z, 'ref')[1], find1(z, 'pin')[1]): find1(n, 'name')[1]
            for n in find(find1(r, 'nets'), 'net') for z in find(n, 'node')}
    comps = {find1(c, 'ref')[1]: (find1(c, 'value')[1], find1(c, 'footprint')[1])
             for c in find(find1(r, 'components'), 'comp')}
    return nets, comps

with tempfile.TemporaryDirectory(prefix='policlock-netlist-') as temporary:
    freshfile = pathlib.Path(temporary) / 'fresh.net'
    cli = pathlib.Path(p.__file__).resolve().parents[2] / 'kicad-cli.exe'
    # pcbnew is installed under bin/Lib/site-packages.
    if not cli.exists():
        cli = pathlib.Path(sys.executable).parent / 'kicad-cli.exe'
    subprocess.run([str(cli), 'sch', 'export', 'netlist', '-o', str(freshfile),
        str(ROOT / 'hardware/policlock-main/policlock-main.kicad_sch')],
        check=True, capture_output=True)
    fresh, freshcomps = netlist(freshfile)
saved, savedcomps = netlist(ROOT / 'hardware/policlock-main/policlock-main.net')
summary['saved_netlist_matches'] = fresh == saved and freshcomps == savedcomps
summary['fresh_netlist_pad_mismatches'] = [(r, z.GetNumber(), z.GetNetname(), fresh.get((r,z.GetNumber())))
    for r,f in fps.items() for z in f.Pads() if (r,z.GetNumber()) in fresh and z.GetNetname() != fresh[(r,z.GetNumber())]]

# Pin centre to pin centre distance only: not an assertion about routed loop inductance.
summary['critical_distances_mm'] = {}
for r,n,s,m in [('U3',3,'C6',1), ('U3',3,'C5',1), ('U2',1,'C2',1), ('U2',5,'C3',1), ('U2',5,'C4',1), ('U1',5,'C1',1), ('U3',20,'R8',1), ('U3',21,'R9',1)]:
    summary['critical_distances_mm'][f'{r}.{n}-{s}.{m}'] = round(math.dist(xy(pad(r,n).GetPosition()), xy(pad(s,m).GetPosition())), 4)

# Summarize actual pad copper annuli; slotted holes use both axes.
summary['pth_annuli'] = []
for z in pads:
    if z.GetAttribute() == p.PAD_ATTRIB_PTH:
        sz, dr = xy(z.GetSize()), xy(z.GetDrillSize())
        summary['pth_annuli'].append({'ref':z.GetParentFootprint().GetReference(), 'pad': z.GetNumber(),
            'size':sz, 'drill':dr, 'annulus_mm':round(min((sz[0]-dr[0])/2, (sz[1]-dr[1])/2),4)})

summary['zones'] = [{'name':z.GetZoneName(), 'rule':z.GetIsRuleArea(), 'net':z.GetNetname(),
    'layers':z.GetLayerSet().FmtBin(), 'filled': z.IsFilled()} for z in board.Zones()]

# Actual USB copper graph, including the 0-ohm component length, without running the generator.
usbtracks = [t for t in tracks if 'USB_D' in t.GetNetname()]
graph = collections.defaultdict(list)
def node(pos, layer):
    # Hand-routed float coordinates can differ by 1 nm after KiCad serialization.
    return (round(pos.x/100)*100, round(pos.y/100)*100, layer)
def edge(a, b, length, vias=0):
    graph[a].append((b, length, vias))
    graph[b].append((a, length, vias))
for t in usbtracks:
    if t.GetClass() == 'PCB_VIA':
        edge(node(t.GetPosition(),p.F_Cu), node(t.GetPosition(),p.B_Cu), 1.6, 1)
    else:
        edge(node(t.GetStart(),t.GetLayer()),node(t.GetEnd(),t.GetLayer()),mm(t.GetLength()))
for ref in ('R3','R4'):
    a,b=pad(ref,1),pad(ref,2)
    edge(node(a.GetPosition(),p.F_Cu), node(b.GetPosition(),p.F_Cu),math.dist(xy(a.GetPosition()),xy(b.GetPosition())))
summary['usb_paths'] = {}
for src,dst in [('B7',26),('B6',27),('A7',26),('A6',27)]:
    start = node(pad('J1',src).GetPosition(),p.F_Cu)
    end = node(pad('U3',dst).GetPosition(),p.F_Cu)
    queue=[(0,0,start)]
    visited=set()
    while queue:
        length,vias,current=heapq.heappop(queue)
        if current in visited: continue
        visited.add(current)
        if current==end:
            summary['usb_paths'][f'J1.{src}-U3.{dst}']={'length_mm':round(length,4),'vias':vias}
            break
        for other,cost,nvia in graph[current]:
            if other not in visited:
                heapq.heappush(queue,(length+cost,vias+nvia,other))

# Stored CPL: coordinates and rotation must match the actual board origin.
cpl = list(csv.DictReader((ROOT / 'hardware/policlock-main/policlock-main-cpl-jlcpcb.csv').open(encoding='utf-8')))
bom = list(csv.DictReader((ROOT / 'hardware/policlock-main/policlock-main-bom-jlcpcb.csv').open(encoding='utf-8')))
origin=xy(board.GetDesignSettings().GetAuxOrigin())
summary['bom_cpl']={'origin':origin,'cpl_count':len(cpl),'bom_quantity':sum(int(r['Qty']) for r in bom),
    'bom_cpl_ref_difference':sorted(set(r['Designator'] for r in cpl)^set(z for r in bom for z in r['Designator'].split(','))),
    'coordinate_mismatches':[]}
for r in cpl:
    f=fps[r['Designator']]
    actual=xy(f.GetPosition())
    vals=(float(r['Mid X'].removesuffix('mm')),float(r['Mid Y'].removesuffix('mm')),float(r['Rotation']))
    expected=(actual[0]-origin[0],origin[1]-actual[1],f.GetOrientationDegrees())
    if any(abs(a-b)>0.00001 for a,b in zip(vals,expected)):
        summary['bom_cpl']['coordinate_mismatches'].append([r['Designator'],vals,expected])
out = ROOT / 'docs/revisioni/2026-11-08/board-audit.json'
out.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding='utf-8')
for k in ['tracks','via_geometries','critical_distances_mm','pth_annuli','saved_netlist_matches','fresh_netlist_pad_mismatches','usb_paths','bom_cpl']:
    print(k, summary[k])
