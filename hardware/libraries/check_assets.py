#!/usr/bin/env python3
"""Check native CAD asset identity and paths; no electrical qualification claim."""
import hashlib
import json
import math
from pathlib import Path
import re


def parse(text):
    tokens = re.findall(r'"(?:\\.|[^"\\])*"|[()]|[^\s()]+', text)
    stack, roots = [], []
    for token in tokens:
        if token == '(':
            node = []
            (stack[-1] if stack else roots).append(node)
            stack.append(node)
        elif token == ')':
            if not stack:
                raise ValueError('Unexpected closing parenthesis')
            stack.pop()
        else:
            if not stack:
                raise ValueError('Atom outside root')
            stack[-1].append(json.loads(token) if token.startswith('"') else token)
    if stack or len(roots) != 1:
        raise ValueError('Unbalanced or multiple roots')
    return roots[0]


def children(node, tag):
    return [x for x in node if isinstance(x, list) and x and x[0] == tag]


def one(node, tag):
    rows = children(node, tag)
    if len(rows) != 1:
        raise ValueError(f'Expected one {tag}, got {len(rows)}')
    return rows[0]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def copper_boxes(footprint):
    """Axis-aligned copper extents per pad: (number, xmin, xmax, ymin, ymax)."""
    boxes = []
    for pad in children(footprint, 'pad'):
        if not any(str(layer).endswith('.Cu') for layer in one(pad, 'layers')[1:]):
            continue
        at, size = one(pad, 'at'), one(pad, 'size')
        x, y = float(at[1]), float(at[2])
        angle = math.radians(float(at[3])) if len(at) > 3 else 0.0
        w, h = float(size[1]), float(size[2])
        c, s = abs(math.cos(angle)), abs(math.sin(angle))
        dx, dy = (w*c + h*s)/2, (w*s + h*c)/2
        boxes.append((str(pad[1]), x-dx, x+dx, y-dy, y+dy))
    return boxes


def shorted_pads(footprint, pin_names):
    """Overlapping copper of differently named pins; shared lands of one net are allowed."""
    boxes, shorts = copper_boxes(footprint), []
    for i, a in enumerate(boxes):
        for b in boxes[i+1:]:
            if a[0] == b[0] or (pin_names.get(a[0]) and pin_names.get(a[0]) == pin_names.get(b[0])):
                continue
            if a[1] < b[2]-1e-6 and b[1] < a[2]-1e-6 and a[3] < b[4]-1e-6 and b[3] < a[4]-1e-6:
                shorts.append((a[0], b[0]))
    return shorts


def check():
    here = Path(__file__).resolve().parent
    project = here.parent/'devboard/board/Yapogee-Devboard'
    index = json.loads((here/'components.json').read_text())
    library_path = here/index['symbol_library']
    assert digest(library_path) == index['symbol_library_sha256'], 'Update index after symbol review'
    symbols = children(parse(library_path.read_text()), 'symbol')
    names = [str(s[1]) for s in symbols]
    assert len(names) == len(set(names)), 'Duplicate symbols'
    indexed = {x['symbol']: x for x in index['components']}
    assert len(indexed) == len(index['components'])
    assert set(names) == set(indexed), 'Library/index mismatch'
    model_files, fp_files = set(), set()
    for symbol in symbols:
        name = str(symbol[1])
        record = indexed[name]
        assert not children(symbol, 'extends'), f'{name}: unresolved inheritance'
        properties = {x[1]: x[2] for x in children(symbol, 'property')}
        assert properties['Footprint'] == 'Yapogee:'+record['footprint']
        actual = []
        for unit in children(symbol, 'symbol'):
            for pin in children(unit, 'pin'):
                actual.append({'number':one(pin,'number')[1], 'name':one(pin,'name')[1],
                               'erc_type':pin[1], 'unit':unit[1]})
        assert actual == record['pins'], f'{name}: indexed pin map changed'
        numbers = [p['number'] for p in actual]
        assert len(numbers) == len(set(numbers)), f'{name}: repeated electrical pin'
        fp_path = here/index['footprint_library']/(record['footprint']+'.kicad_mod')
        fp_files.add(fp_path.name)
        assert digest(fp_path) == record['footprint_sha256'], f'{name}: footprint changed'
        footprint = parse(fp_path.read_text())
        copper = {str(p[1]) for p in children(footprint,'pad')
                  if p[1] and any(str(layer).endswith('.Cu') for layer in one(p,'layers')[1:])}
        assert set(numbers) == copper, f'{name}: symbol/pad mismatch {set(numbers)^copper}'
        shorts = shorted_pads(footprint, {p['number']: p['name'] for p in actual})
        assert not shorts, f'{name}: overlapping copper on different pins {shorts[:4]} ({len(shorts)} pairs)'
        paths = [str(m[1]) for m in children(footprint,'model')]
        expected = ['${KIPRJMOD}/../../../libraries/3dmodels/'+m['file'] for m in record['models']]
        assert paths == expected, f'{name}: model index mismatch'
        for model, path in zip(record['models'], paths):
            resolved = Path(path.replace('${KIPRJMOD}', str(project))).resolve()
            assert resolved == (here/'3dmodels'/model['file']).resolve()
            assert digest(resolved) == model['sha256'], f'{name}: model changed'
            prefix = resolved.read_bytes()[:100]
            assert b'ISO-10303-21' in prefix or prefix.startswith(b'#VRML V2.0'), f'{name}: model format'
            model_files.add(resolved.name)
    assert fp_files == {p.name for p in (here/index['footprint_library']).glob('*.kicad_mod')}
    assert model_files == {p.name for p in (here/'3dmodels').iterdir() if p.is_file()}
    for filename, target in [('sym-lib-table',here/index['symbol_library']),
                             ('fp-lib-table',here/index['footprint_library'])]:
        table = parse((project/filename).read_text())
        lib = next(x for x in children(table,'lib') if one(x,'name')[1]=='Yapogee')
        uri = one(lib,'uri')[1]
        assert Path(uri.replace('${KIPRJMOD}',str(project))).resolve() == target.resolve()
    print(f'{len(symbols)} symbols, {len(fp_files)} footprints, {len(model_files)} models: integrity checks passed')
    print('Unnumbered mechanical/paste pads are excluded from electrical-pin matching; copper of different pins must not overlap.')
    print('Circuit ERC, routed-board DRC, solder process and assembled fit remain pending.')


if __name__ == '__main__':
    check()
