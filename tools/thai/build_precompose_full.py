#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_JSON = ROOT / 'tools/thai/precompose_input/thai_precompose_11x12_Shadow.json'
DEFAULT_CSV = ROOT / 'tools/thai/precompose_input/Precompose List.csv'
DEFAULT_PALETTE = ROOT / 'graphics/fonts/thai_shaped.png'
DEFAULT_OUT = ROOT / 'tools/thai/generated/precompose_full'
SRC_W, SRC_H = 11, 12
DST_W, DST_H = 16, 16
COLS = 16
SAMPLES = ('เริ่มเกมส์', 'กิ กี กี่ กุ กู', 'รู้ สู้ ผู้', 'ญี่ปุ่น', 'น้ำ')


def die(msg: str) -> None:
    raise SystemExit(f'ERROR: {msg}')


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def read_csv(path: Path) -> tuple[list[str], str]:
    raw = path.read_bytes()
    for enc in ('utf-8-sig', 'cp874', 'tis-620'):
        try:
            text = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    else:
        die('อ่าน CSV ไม่ได้ด้วย utf-8-sig, cp874 หรือ tis-620')
    rows = []
    for row in csv.reader(text.splitlines()):
        if row and row[0].strip():
            rows.append(row[0].strip())
    return rows, enc


def validate_rows(value: Any, name: str, field: str) -> list[str]:
    if not isinstance(value, list) or len(value) != SRC_H:
        die(f'{name!r} {field} ต้องมี {SRC_H} แถว')
    out = []
    for y, row in enumerate(value):
        if not isinstance(row, str) or len(row) != SRC_W:
            die(f'{name!r} {field}[{y}] ต้องกว้าง {SRC_W}')
        bad = set(row) - {'0', '1', '2'}
        if bad:
            die(f'{name!r} {field}[{y}] มีค่าไม่ถูกต้อง: {sorted(bad)}')
        out.append(row)
    return out


def merge(main: list[str], shadow: list[str]) -> list[str]:
    rows = []
    for a, b in zip(main, shadow):
        rows.append(''.join('1' if x == '1' else '2' if y == '2' else '0' for x, y in zip(a, b)))
    return rows


def bbox(rows: list[str]) -> list[int] | None:
    pts = [(x, y) for y, row in enumerate(rows) for x, value in enumerate(row) if value != '0']
    if not pts:
        return None
    xs, ys = zip(*pts)
    return [min(xs), min(ys), max(xs), max(ys)]


def palette_from(path: Path) -> list[int]:
    with Image.open(path) as im:
        pal = im.getpalette()
    if pal is None:
        die(f'{path} ไม่มี indexed palette')
    return (pal + [0] * 768)[:768]


def make_tile(rows: list[str], palette: list[int], embed_x: int, embed_y: int) -> Image.Image:
    tile = Image.new('P', (DST_W, DST_H), 0)
    tile.putpalette(palette)
    for sy, row in enumerate(rows):
        for sx, value in enumerate(row):
            if value != '0':
                tile.putpixel((embed_x + sx, embed_y + sy), int(value))
    return tile


def longest_match(text: str, names: set[str]) -> tuple[list[str], list[str]]:
    max_len = max(map(len, names))
    tokens, missing = [], []
    i = 0
    while i < len(text):
        if text[i].isspace():
            tokens.append(text[i])
            i += 1
            continue
        found = None
        for end in range(min(len(text), i + max_len), i, -1):
            part = text[i:end]
            if part in names:
                found = part
                break
        if found is None:
            missing.append(text[i])
            tokens.append(f'[MISSING:{text[i]}]')
            i += 1
        else:
            tokens.append(found)
            i += len(found)
    return tokens, missing


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument('--json', type=Path, default=DEFAULT_JSON)
    p.add_argument('--csv', type=Path, default=DEFAULT_CSV)
    p.add_argument('--palette-source', type=Path, default=DEFAULT_PALETTE)
    p.add_argument('--out-dir', type=Path, default=DEFAULT_OUT)
    p.add_argument('--embed-x', type=int, default=0)
    p.add_argument('--embed-y', type=int, default=2)
    p.add_argument('--strict-csv', action='store_true')
    a = p.parse_args()

    for path in (a.json, a.csv, a.palette_source):
        if not path.is_file():
            die(f'ไม่พบไฟล์: {path}')
    if a.embed_x < 0 or a.embed_y < 0 or a.embed_x + SRC_W > DST_W or a.embed_y + SRC_H > DST_H:
        die('Embed offset ทำให้ภาพ 11x12 หลุดกรอบ 16x16')

    data = json.loads(a.json.read_text(encoding='utf-8'))
    meta = data.get('meta', {})
    raw_glyphs = data.get('glyphs')
    if meta.get('cell_width') != SRC_W or meta.get('cell_height') != SRC_H:
        die(f"Source cell ต้องเป็น 11x12 แต่พบ {meta.get('cell_width')}x{meta.get('cell_height')}")
    if not isinstance(raw_glyphs, list):
        die('JSON ไม่มี glyphs')

    palette = palette_from(a.palette_source)
    items = []
    names, indices = [], []

    for pos, entry in enumerate(raw_glyphs):
        if not isinstance(entry, dict):
            die(f'glyphs[{pos}] ไม่ใช่ Object')
        name = entry.get('name')
        index = entry.get('target_index')
        width = entry.get('width')
        advance = entry.get('advance')
        left = entry.get('left', 0)
        if not isinstance(name, str) or not name:
            die(f'glyphs[{pos}] ไม่มี name')
        if not isinstance(index, int) or index < 0:
            die(f'{name!r} target_index ไม่ถูกต้อง')
        if not isinstance(width, int) or width < 0 or not isinstance(advance, int) or advance < 0 or not isinstance(left, int):
            die(f'{name!r} metrics ไม่ถูกต้อง')

        main_rows = validate_rows(entry.get('bitmap'), name, 'bitmap')
        shadow_rows = validate_rows(entry.get('shadow_bitmap'), name, 'shadow_bitmap')
        if entry.get('composite_bitmap') is None:
            rows, composite_source = merge(main_rows, shadow_rows), 'rebuilt'
        else:
            rows = validate_rows(entry.get('composite_bitmap'), name, 'composite_bitmap')
            composite_source = 'json'

        src_box = bbox(rows)
        dst_box = None if src_box is None else [src_box[0] + a.embed_x, src_box[1] + a.embed_y, src_box[2] + a.embed_x, src_box[3] + a.embed_y]
        items.append({
            'name': name,
            'target_index': index,
            'category': entry.get('category'),
            'source': entry.get('source'),
            'project_source': entry.get('project_source'),
            'locked': entry.get('locked'),
            'left': left,
            'width': width,
            'advance': advance,
            'source_bbox': src_box,
            'target_bbox': dst_box,
            'composite_source': composite_source,
            '_tile': make_tile(rows, palette, a.embed_x, a.embed_y),
        })
        names.append(name)
        indices.append(index)

    dup_names = [k for k, v in Counter(names).items() if v > 1]
    dup_indices = [k for k, v in Counter(indices).items() if v > 1]
    if dup_names or dup_indices:
        die(f'พบข้อมูลซ้ำ names={dup_names[:10]} indices={dup_indices[:10]}')
    if sorted(indices) != list(range(len(items))):
        die('target_index ต้องต่อเนื่อง 0..N-1')

    items.sort(key=lambda x: x['target_index'])
    rows_count = math.ceil(len(items) / COLS)
    atlas = Image.new('P', (COLS * DST_W, rows_count * DST_H), 0)
    atlas.putpalette(palette)
    map_items = []
    for item in items:
        idx = item['target_index']
        atlas.paste(item['_tile'], ((idx % COLS) * DST_W, (idx // COLS) * DST_H))
        map_items.append({k: v for k, v in item.items() if k != '_tile'})

    csv_items, csv_encoding = read_csv(a.csv)
    csv_unique = list(dict.fromkeys(csv_items))
    csv_only = sorted(set(csv_unique) - set(names))
    json_only = sorted(set(names) - set(csv_unique))
    if a.strict_csv and (csv_only or json_only):
        die(f'CSV/JSON ไม่ตรงกัน csv_only={len(csv_only)} json_only={len(json_only)}')

    samples = []
    for text in SAMPLES:
        tokens, missing = longest_match(text, set(names))
        samples.append({'text': text, 'tokens': tokens, 'missing': missing})

    a.out_dir.mkdir(parents=True, exist_ok=True)
    atlas_path = a.out_dir / 'thai_precompose_full.png'
    map_path = a.out_dir / 'thai_precompose_full_map.json'
    report_path = a.out_dir / 'thai_precompose_full_report.txt'
    atlas.save(atlas_path, optimize=False)

    output = {
        'format': 'pokemon-gen3-thai-precompose-full-v1',
        'source_name': meta.get('name'),
        'source_json': str(a.json.relative_to(ROOT)),
        'source_json_sha256': sha256(a.json),
        'source_csv': str(a.csv.relative_to(ROOT)),
        'source_csv_sha256': sha256(a.csv),
        'source_cell': [SRC_W, SRC_H],
        'destination_cell': [DST_W, DST_H],
        'embed_offset': [a.embed_x, a.embed_y],
        'atlas_columns': COLS,
        'atlas_rows': rows_count,
        'atlas_size': list(atlas.size),
        'glyph_count': len(map_items),
        'csv_encoding': csv_encoding,
        'csv_count': len(csv_items),
        'csv_unique_count': len(csv_unique),
        'csv_only': csv_only,
        'json_only': json_only,
        'samples': samples,
        'glyphs': map_items,
    }
    map_path.write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    report = [
        'THAI PRECOMPOSE FULL ATLAS REPORT',
        '=================================',
        f'Source name      : {meta.get("name")}',
        f'Source glyphs    : {len(map_items)}',
        f'Source cell      : {SRC_W}x{SRC_H}',
        f'Destination cell : {DST_W}x{DST_H}',
        f'Embed offset     : ({a.embed_x}, {a.embed_y})',
        f'Atlas size       : {atlas.size[0]}x{atlas.size[1]}',
        f'Atlas rows       : {rows_count}',
        f'CSV encoding     : {csv_encoding}',
        f'CSV rows         : {len(csv_items)}',
        f'CSV unique       : {len(csv_unique)}',
        f'CSV only         : {len(csv_only)}',
        f'JSON only        : {len(json_only)}',
        '', 'CSV ONLY', '--------', *(csv_only or ['(none)']),
        '', 'JSON ONLY', '---------', *(json_only or ['(none)']),
        '', 'LONGEST-MATCH SAMPLE CHECK', '--------------------------',
    ]
    for s in samples:
        report += [
            f"Text   : {s['text']}",
            'Tokens : ' + ' | '.join(s['tokens']),
            'Missing: ' + (', '.join(s['missing']) if s['missing'] else '(none)'),
            '',
        ]
    report += ['OUTPUTS', '-------', str(atlas_path.relative_to(ROOT)), str(map_path.relative_to(ROOT)), str(report_path.relative_to(ROOT))]
    report_path.write_text('\n'.join(report) + '\n', encoding='utf-8')

    print('========================================')
    print('THAI PRECOMPOSE FULL BUILD')
    print('========================================')
    print(f'Source glyphs : {len(map_items)}')
    print(f'Source cell   : {SRC_W}x{SRC_H}')
    print(f'Atlas         : {atlas.size[0]}x{atlas.size[1]} ({COLS} columns x {rows_count} rows)')
    print(f'Embed offset  : ({a.embed_x}, {a.embed_y})')
    print(f'CSV rows      : {len(csv_items)}')
    print(f'CSV only      : {len(csv_only)}')
    print(f'JSON only     : {len(json_only)}')
    print('\nSAMPLE CHECK')
    for s in samples:
        print(('PASS' if not s['missing'] else 'MISSING') + f": {s['text']} -> " + ' | '.join(s['tokens']))
    print('\nOUTPUTS')
    print(atlas_path.relative_to(ROOT))
    print(map_path.relative_to(ROOT))
    print(report_path.relative_to(ROOT))
    print('\nRESULT: FULL ATLAS BUILD PASSED')
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print('\nCancelled. ไม่มีการแก้ Production files', file=sys.stderr)
        raise SystemExit(130)
