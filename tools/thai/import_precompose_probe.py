#!/usr/bin/env python3
"""
Import a small Thai precompose probe from thai_precompose_11x12_Shadow.json.

This script is intentionally non-destructive:
- It never edits production font files.
- It writes only into the output directory passed with --out-dir.
- It validates the requested word can be segmented entirely from JSON glyph names.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw


PALETTE = [
    255, 255, 255,  # 0 transparent/background in previews
    0, 0, 0,        # 1 main glyph
    160, 160, 160,  # 2 shadow
] + [0] * (768 - 9)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", required=True, type=Path, help="Path to thai_precompose_11x12_Shadow.json")
    parser.add_argument("--out-dir", required=True, type=Path, help="Directory for generated probe files")
    parser.add_argument("--word", default="เริ่มเกมส์", help="Thai probe word")
    parser.add_argument("--embed-x", type=int, default=0, help="X offset when embedding 11x12 into 16x16")
    parser.add_argument("--embed-y", type=int, default=2, help="Y offset when embedding 11x12 into 16x16")
    return parser.parse_args()


def fail(message: str) -> "NoReturn":
    raise SystemExit(f"ERROR: {message}")


def load_source(path: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    if not path.is_file():
        fail(f"JSON file not found: {path}")

    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        fail(f"Cannot read JSON: {exc}")

    if not isinstance(data, dict) or "meta" not in data or "glyphs" not in data:
        fail("JSON must contain top-level 'meta' and 'glyphs'")

    meta = data["meta"]
    glyphs = data["glyphs"]

    if meta.get("cell_width") != 11 or meta.get("cell_height") != 12:
        fail(
            "Expected source cells 11x12, got "
            f"{meta.get('cell_width')}x{meta.get('cell_height')}"
        )

    if not isinstance(glyphs, list) or not glyphs:
        fail("'glyphs' must be a non-empty list")

    expected = meta.get("built_count")
    if expected is not None and expected != len(glyphs):
        fail(f"built_count={expected}, actual glyph count={len(glyphs)}")

    return meta, glyphs


def validate_glyph(glyph: dict[str, Any]) -> None:
    name = glyph.get("name")
    rows = glyph.get("composite_bitmap")

    if not isinstance(name, str) or not name:
        fail("Found a glyph with an invalid name")

    if not isinstance(rows, list) or len(rows) != 12:
        fail(f"{name!r}: composite_bitmap must contain 12 rows")

    for row_number, row in enumerate(rows):
        if not isinstance(row, str) or len(row) != 11:
            fail(f"{name!r}: row {row_number} must be 11 characters")
        if set(row) - {"0", "1", "2"}:
            fail(f"{name!r}: row {row_number} contains values outside 0/1/2")

    for key in ("width", "advance"):
        if not isinstance(glyph.get(key), int):
            fail(f"{name!r}: missing integer {key!r}")


def longest_match_segment(word: str, names: set[str]) -> list[str]:
    ordered = sorted(names, key=lambda value: (-len(value), value))
    result: list[str] = []
    index = 0

    while index < len(word):
        match = next((name for name in ordered if word.startswith(name, index)), None)
        if match is None:
            codepoint = f"U+{ord(word[index]):04X}"
            fail(f"Cannot segment at position {index}: {word[index]!r} ({codepoint})")
        result.append(match)
        index += len(match)

    return result


def source_tile(glyph: dict[str, Any]) -> Image.Image:
    tile = Image.new("P", (11, 12), 0)
    tile.putpalette(PALETTE)

    for y, row in enumerate(glyph["composite_bitmap"]):
        for x, value in enumerate(row):
            tile.putpixel((x, y), int(value))

    return tile


def embed_tile(source: Image.Image, embed_x: int, embed_y: int) -> Image.Image:
    if embed_x < 0 or embed_y < 0:
        fail("Embedding offsets cannot be negative")
    if embed_x + source.width > 16 or embed_y + source.height > 16:
        fail(
            f"Source {source.width}x{source.height} at "
            f"({embed_x},{embed_y}) does not fit in 16x16"
        )

    tile = Image.new("P", (16, 16), 0)
    tile.putpalette(PALETTE)
    tile.paste(source, (embed_x, embed_y))
    return tile


def nonzero_bbox(tile: Image.Image) -> list[int] | None:
    points = [
        (x, y)
        for y in range(tile.height)
        for x in range(tile.width)
        if tile.getpixel((x, y)) != 0
    ]
    if not points:
        return None

    xs = [point[0] for point in points]
    ys = [point[1] for point in points]
    return [min(xs), min(ys), max(xs), max(ys)]


def build_atlas(
    unique_names: list[str],
    glyph_by_name: dict[str, dict[str, Any]],
    embed_x: int,
    embed_y: int,
) -> tuple[Image.Image, dict[str, int], dict[str, Image.Image]]:
    atlas = Image.new("P", (256, 16), 0)
    atlas.putpalette(PALETTE)

    index_by_name: dict[str, int] = {}
    tile_by_name: dict[str, Image.Image] = {}

    for atlas_index, name in enumerate(unique_names):
        glyph = glyph_by_name[name]
        tile = embed_tile(source_tile(glyph), embed_x, embed_y)
        x = atlas_index * 16
        atlas.paste(tile, (x, 0))
        index_by_name[name] = atlas_index
        tile_by_name[name] = tile

    return atlas, index_by_name, tile_by_name


def build_proof(
    word: str,
    clusters: list[str],
    glyph_by_name: dict[str, dict[str, Any]],
    tile_by_name: dict[str, Image.Image],
) -> Image.Image:
    margin = 4
    total_advance = sum(glyph_by_name[name]["advance"] for name in clusters)
    canvas = Image.new("P", (max(1, total_advance + margin * 2), 20), 0)
    canvas.putpalette(PALETTE)

    pen_x = margin
    for name in clusters:
        canvas.paste(tile_by_name[name], (pen_x, 0))
        pen_x += glyph_by_name[name]["advance"]

    scale = 12
    proof = canvas.resize(
        (canvas.width * scale, canvas.height * scale),
        Image.Resampling.NEAREST,
    ).convert("RGB")

    draw = ImageDraw.Draw(proof)

    # Grid for the 16-pixel glyph cell region.
    for y in range(0, 17):
        draw.line((0, y * scale, proof.width, y * scale), fill=(225, 225, 225), width=1)

    # Candidate common baseline: embedded source row 10 -> destination y=12.
    baseline_y = 12 * scale
    draw.line((0, baseline_y, proof.width, baseline_y), fill=(200, 0, 0), width=2)

    return proof


def main() -> int:
    args = parse_args()
    meta, glyphs = load_source(args.json)

    for glyph in glyphs:
        validate_glyph(glyph)

    names = [glyph["name"] for glyph in glyphs]
    duplicates = sorted({name for name in names if names.count(name) > 1})
    if duplicates:
        fail(f"Duplicate glyph names: {duplicates[:10]}")

    glyph_by_name = {glyph["name"]: glyph for glyph in glyphs}
    clusters = longest_match_segment(args.word, set(glyph_by_name))

    # Preserve first-use order, so repeated clusters reuse one atlas cell.
    unique_names = list(dict.fromkeys(clusters))

    if len(unique_names) > 16:
        fail("Probe atlas supports at most 16 unique clusters")

    args.out_dir.mkdir(parents=True, exist_ok=True)

    atlas, index_by_name, tile_by_name = build_atlas(
        unique_names,
        glyph_by_name,
        args.embed_x,
        args.embed_y,
    )

    atlas_path = args.out_dir / "precompose_start_game_atlas.png"
    proof_path = args.out_dir / "precompose_start_game_proof.png"
    map_path = args.out_dir / "precompose_start_game_map.json"
    report_path = args.out_dir / "precompose_start_game_report.txt"

    atlas.save(atlas_path, optimize=False)
    build_proof(args.word, clusters, glyph_by_name, tile_by_name).save(proof_path)

    mapping_entries = []
    for name in unique_names:
        source = glyph_by_name[name]
        tile = tile_by_name[name]
        mapping_entries.append(
            {
                "name": name,
                "atlas_index": index_by_name[name],
                "source_target_index": source.get("target_index"),
                "category": source.get("category"),
                "source_width": source["width"],
                "source_advance": source["advance"],
                "source_auto_bbox": source.get("auto_bbox"),
                "embedded_bbox": nonzero_bbox(tile),
                "embed_x": args.embed_x,
                "embed_y": args.embed_y,
            }
        )

    mapping = {
        "format": "pokemon-gen3-thai-precompose-probe-v1",
        "source_name": meta.get("name"),
        "source_cell": [meta["cell_width"], meta["cell_height"]],
        "destination_cell": [16, 16],
        "embed_offset": [args.embed_x, args.embed_y],
        "word": args.word,
        "clusters": clusters,
        "encoded_atlas_indices": [index_by_name[name] for name in clusters],
        "total_advance": sum(glyph_by_name[name]["advance"] for name in clusters),
        "glyphs": mapping_entries,
    }

    map_path.write_text(
        json.dumps(mapping, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    report_lines = [
        "THAI PRECOMPOSE PROBE",
        "=====================",
        f"Source JSON      : {args.json}",
        f"Source name      : {meta.get('name')}",
        f"Source glyphs    : {len(glyphs)}",
        f"Source cell      : {meta['cell_width']}x{meta['cell_height']}",
        "Destination cell : 16x16",
        f"Embed offset     : ({args.embed_x}, {args.embed_y})",
        f"Probe word       : {args.word}",
        f"Clusters         : {' | '.join(clusters)}",
        f"Unique glyphs    : {' | '.join(unique_names)}",
        "Atlas indices    : " + ", ".join(str(index_by_name[name]) for name in clusters),
        f"Total advance    : {mapping['total_advance']}",
        "",
        "GLYPH DETAILS",
        "-------------",
    ]

    for entry in mapping_entries:
        report_lines.append(
            f"{entry['name']}: atlas={entry['atlas_index']} "
            f"source_target={entry['source_target_index']} "
            f"width={entry['source_width']} "
            f"advance={entry['source_advance']} "
            f"embedded_bbox={entry['embedded_bbox']}"
        )

    report_lines.extend(
        [
            "",
            "OUTPUTS",
            "-------",
            str(atlas_path),
            str(proof_path),
            str(map_path),
        ]
    )

    report_path.write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    print(report_path.read_text(encoding="utf-8"), end="")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("Cancelled.", file=sys.stderr)
        raise SystemExit(130)
