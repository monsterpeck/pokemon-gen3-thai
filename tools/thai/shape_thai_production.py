#!/usr/bin/env python3
"""Production front end for contextual Thai build-time shaping."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from PIL import Image

import shape_thai_text as legacy
from noto_thai import *
from production_shaping import VARIANT_ORDER, analyze, bbox, bitmap_hash, clusters, select, solve, variant_tile
from render_thai_proof import GlyphRasterizer, rasterize_shaped_cell, shape_text

CMD_BEGIN = legacy.CMD_BEGIN
CMD_THAI_POSITIONED = legacy.CMD_THAI_POSITIONED
COMMAND_SIZE = legacy.COMMAND_SIZE
MAP_PATH = legacy.MAP_PATH
FONT_PNG = legacy.FONT_PNG
TRACE_PATH = legacy.TRACE_PATH
THAI_RE = legacy.THAI_RE
STRING_RE = legacy.STRING_RE
ISOLATION_LINES = ("เรม", "เริ่ม", "เกมส์", "ริ", "รี่", "ริน", "สน", "ส์")
PRODUCTION_LINES = tuple(dict.fromkeys((*ISOLATION_LINES, *PROOF_LINES)))


def palette():
    values = sum(spec()["palette_rgb"], [])
    return values + [0] * (768 - len(values))


def shape_run(text, mapping=None):
    records, total = legacy.shape_run(text, mapping)
    data, upem, _order = legacy.load_context()
    _font, items = shape_text(text, data, upem)
    analyses = analyze(text, items)
    raster = GlyphRasterizer(FONT, upem, spec()["logical_scale"], spec()["oversample"])
    for record in records:
        record["normal_tile"] = rasterize_shaped_cell(raster, record["glyph_id"], palette())["tile"]
        record["cluster_analysis"] = analyses[record["cluster"]]
    return records, total


def selected_run(text, mapping=None):
    records, total = shape_run(text, mapping)
    return select(records), total


def encode_run(text, mapping):
    records, total = selected_run(text, mapping)
    lookup = {(int(entry["hb_glyph_id"]), entry["variant"]): int(entry["compact_index"])
              for entry in mapping["glyphs"]}
    output = []
    for record in records:
        original = int(mapping["hb_to_gba"][str(record["glyph_id"])])
        key = (record["glyph_id"], record["selected_variant"])
        if key not in lookup:
            raise ValueError(f"missing {key[1]} variant for HB {key[0]}")
        selected = lookup[key]
        record["original_compact_index"] = original
        record["selected_compact_index"] = selected
        x = record["x_offset"] + record["contextual_shift_x"]
        y = record["y_offset"] + record["contextual_shift_y"]
        flags = 1 if record["cluster_start"] else 0
        output += [CMD_BEGIN, CMD_THAI_POSITIONED, selected & 255, selected >> 8,
                   x & 255, y & 255, record["x_advance"], flags]
    return bytes(output), records, total


def entry(index, gid, name, variant, source, tile):
    pixels = list(tile.getdata())
    return {
        "compact_index": index, "gba_glyph_id": index, "hb_glyph_id": gid,
        "glyph_name": name, "variant": variant,
        "source_cluster_class": "base" if variant.startswith("upper_clearance") else "mark" if variant.startswith("compact") else "normal",
        "source_bitmap_hash": bitmap_hash(source), "production_bitmap_hash": bitmap_hash(tile),
        "palette_index_1_count": pixels.count(1), "palette_index_2_count": pixels.count(2),
        "bitmap_bbox": bbox(tile), "baseline": spec()["target_baseline"],
        "contextual_shift_x": 0, "contextual_shift_y": 0,
    }


def build_font():
    data, upem, order = legacy.load_context()
    required, normal_tiles = set(), {}
    for text in PRODUCTION_LINES:
        records, _ = shape_run(text)
        for record in records:
            normal_tiles[record["glyph_id"]] = record["normal_tile"]
            required.add((record["glyph_id"], "normal"))
        for cluster in clusters(records):
            choices, _normal, _final = solve(cluster)
            for record, (variant, _dx, _dy) in zip(cluster, choices):
                required.add((record["glyph_id"], variant))
    ordered = sorted(required, key=lambda pair: (VARIANT_ORDER[pair[1]], pair[0]))
    sheet = Image.new("P", (256, ((len(ordered) + 15) // 16) * 16), 0)
    sheet.putpalette(palette())
    entries, hb_to_gba = [], {}
    for index, (gid, variant) in enumerate(ordered):
        source = normal_tiles[gid]
        tile = variant_tile(source, variant)
        used = set(tile.getdata())
        if used - {0, 1, 2} or (gid != 111 and 1 not in used):
            raise ValueError(f"invalid palette/body for HB {gid} {variant}")
        sheet.paste(tile, ((index % 16) * 16, (index // 16) * 16))
        entries.append(entry(index, gid, order[gid], variant, source, tile))
        if variant == "normal":
            hb_to_gba[str(gid)] = index
    mapping = {
        "format_version": 3, "font_sha256": EXPECTED_SHA256, "units_per_em": upem,
        "scale": spec()["logical_scale"], "baseline": spec()["target_baseline"],
        "palette_convention": {"0": "transparent", "1": "dark main", "2": "light shadow"},
        "command_begin": CMD_BEGIN, "command_id": CMD_THAI_POSITIONED,
        "command_size": COMMAND_SIZE, "hb_to_gba": hb_to_gba, "glyphs": entries,
    }
    if sheet.mode != "P" or set(sheet.getdata()) - {0, 1, 2}:
        raise ValueError("invalid production sheet palette")
    sheet.save(FONT_PNG, optimize=False)
    MAP_PATH.write_text(json.dumps(mapping, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return mapping


def load_mapping():
    return json.loads(MAP_PATH.read_text(encoding="utf-8"))


def check_trace(mapping):
    legacy.check_trace(mapping)
    for text in PRODUCTION_LINES:
        encode_run(text, mapping)


def transform_literal(literal, mapping):
    return '"' + THAI_RE.sub(lambda match: legacy.brace_bytes(encode_run(match.group(0), mapping)[0]), literal[1:-1]) + '"'


def transform_source(source, mapping):
    def replace(match):
        if not THAI_RE.search(match.group(0)):
            return match.group(0)
        prefix = source[:match.start()]
        line_prefix = prefix[prefix.rfind("\n") + 1:]
        project = bool(re.search(r"_\s*\([^)]*$", prefix[-4096:], re.S))
        assembly = bool(re.search(r"\.(?:string|ascii)\s*$", line_prefix))
        return transform_literal(match.group(0), mapping) if project or assembly else match.group(0)
    return STRING_RE.sub(replace, source)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--build-font", action="store_true")
    parser.add_argument("--filter-source", nargs="?", const="-")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--encode")
    args = parser.parse_args()
    mapping = build_font() if args.build_font else load_mapping()
    if args.check:
        check_trace(mapping)
    if args.encode:
        encoded, records, total = encode_run(args.encode, mapping)
        print(encoded.hex(" "))
        print(json.dumps({"advance": total, "glyphs": [{k: v for k, v in record.items() if k not in ("bitmap", "normal_tile")} for record in records]}, ensure_ascii=False, indent=2))
    if args.filter_source is not None:
        source = sys.stdin.read() if args.filter_source == "-" else Path(args.filter_source).read_text(encoding="utf-8")
        sys.stdout.write(transform_source(source, mapping))


if __name__ == "__main__":
    main()
