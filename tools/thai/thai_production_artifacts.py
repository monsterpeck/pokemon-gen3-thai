#!/usr/bin/env python3
"""Validate and visualize the final build-time Thai production system."""
from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont

from noto_thai import GENERATED, PROOF_LINES, ROOT
from production_shaping import bbox, clusters, role
from shape_thai_production import FONT_PNG, ISOLATION_LINES, encode_run, load_mapping, selected_run

FINAL = GENERATED / "thai_production_final_proof.png"
CELLS = GENERATED / "thai_production_cluster_cells.png"
PALETTE = GENERATED / "thai_production_palette_proof.png"
DIFFERENCE = GENERATED / "thai_production_difference_proof.png"
TRACE = GENERATED / "thai_production_trace.csv"
REPORT = GENERATED / "thai_production_report.md"
LATFONT = ROOT / "build/assets/graphics/fonts/thai_shaped.png.latfont"
ROM = ROOT / "pokeemerald.gba"
SAMPLES = ("เรม", "เริ่ม", "เกมส์", "เริ่มเกมส์", "โปเกมอน", "ผู้เล่น", "น้ำ เก็บไว้", "ญี่ปุ่น", "ความสามารถ")
FIELDS = (
    "sample_text", "cluster_number", "unicode_sequence", "base_character", "hb_glyph_id",
    "glyph_name", "original_compact_index", "selected_compact_index", "selected_variant",
    "upper_mark_count", "upper_mark_characters", "normal_combined_top", "normal_combined_bottom",
    "final_combined_top", "final_combined_bottom", "base_shift_y", "mark_adjust_x",
    "mark_adjust_y", "x_advance", "x_offset", "y_offset", "palette_index_1_count",
    "palette_index_2_count", "fit_result",
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def cell(sheet, index):
    x, y = index % 16 * 16, index // 16 * 16
    return sheet.crop((x, y, x + 16, y + 16))


def rgb(tile):
    return tile.convert("RGB")


def render(text, mapping, sheet, production=True):
    _encoded, records, _advance = encode_run(text, mapping)
    width = sum(r["x_advance"] for r in records) + 24
    canvas = Image.new("P", (width, 24), 0)
    canvas.putpalette(sheet.getpalette())
    pen = 6
    boundaries = []
    previous = None
    for record in records:
        if record["cluster"] != previous:
            boundaries.append(pen)
            previous = record["cluster"]
        index = record["selected_compact_index"] if production else record["original_compact_index"]
        tile = cell(sheet, index)
        dx = record["contextual_shift_x"] if production else 0
        dy = record["contextual_shift_y"] if production else 0
        x, y = pen + record["x_offset"] + dx, 4 + 12 + record["y_offset"] + dy
        canvas.paste(tile, (x, y), tile.point(lambda p: 255 if p else 0).convert("L"))
        pen += record["x_advance"]
    return canvas, records, boundaries


def trace_rows(mapping, sheet):
    output = []
    for text in SAMPLES:
        _encoded, records, _total = encode_run(text, mapping)
        groups = clusters(records)
        for record in records:
            group = next(group for group in groups if group[0]["cluster"] == record["cluster"])
            analysis = record["cluster_analysis"]
            base = next((r for r in group if r["is_base"]), None)
            tile = cell(sheet, record["selected_compact_index"])
            counts = Counter(tile.getdata())
            kind = role(record)
            output.append({
                "sample_text": text, "cluster_number": record["cluster_number"],
                "unicode_sequence": analysis["unicode_sequence"],
                "base_character": analysis["text"][0] if base else "",
                "hb_glyph_id": record["glyph_id"], "glyph_name": record["glyph_name"],
                "original_compact_index": record["original_compact_index"],
                "selected_compact_index": record["selected_compact_index"],
                "selected_variant": record["selected_variant"],
                "upper_mark_count": analysis["above_count"],
                "upper_mark_characters": "".join((*analysis["upper_marks"], *analysis["tones"])),
                "normal_combined_top": record["normal_combined_top"],
                "normal_combined_bottom": record["normal_combined_bottom"],
                "final_combined_top": record["final_combined_top"],
                "final_combined_bottom": record["final_combined_bottom"],
                "base_shift_y": record["contextual_shift_y"] if kind == "base" else 0,
                "mark_adjust_x": record["contextual_shift_x"] if kind in ("upper", "tone", "lower") else 0,
                "mark_adjust_y": record["contextual_shift_y"] if kind in ("upper", "tone", "lower") else 0,
                "x_advance": record["x_advance"], "x_offset": record["x_offset"],
                "y_offset": record["y_offset"], "palette_index_1_count": counts[1],
                "palette_index_2_count": counts[2], "fit_result": record["fit_result"],
            })
    return output


def validate(mapping, sheet):
    if sheet.mode != "P" or set(sheet.getdata()) - {0, 1, 2}:
        raise AssertionError("production sheet must be indexed and use only 0,1,2")
    if len({e["compact_index"] for e in mapping["glyphs"]}) != len(mapping["glyphs"]):
        raise AssertionError("contextual compact indexes are not unique")
    if {e["compact_index"] for e in mapping["glyphs"]} != set(range(len(mapping["glyphs"]))):
        raise AssertionError("compact indexes are not dense")
    for entry in mapping["glyphs"]:
        tile = cell(sheet, entry["compact_index"])
        if entry["glyph_name"] != "space" and 1 not in tile.getdata():
            raise AssertionError(f"{entry['compact_index']} lacks dark main pixels")
        if hashlib.sha256(bytes(tile.getdata())).hexdigest() != entry["production_bitmap_hash"]:
            raise AssertionError("glyph map bitmap hash is stale")
    for text in (*SAMPLES, *ISOLATION_LINES):
        _encoded, records, _total = encode_run(text, mapping)
        if any(r["final_combined_top"] < 0 or r["final_combined_bottom"] > 15 for r in records):
            raise AssertionError(f"clipped cluster in {text}")
    normal_81 = cell(sheet, int(mapping["hb_to_gba"]["81"]))
    normal_110 = cell(sheet, int(mapping["hb_to_gba"]["110"]))
    x_probe = {(i, i) for i in range(2, 14)} | {(15 - i, i) for i in range(2, 14)}
    square_probe = {(x, y) for x in range(2, 14) for y in range(2, 14) if x in (2, 13) or y in (2, 13)}
    if all(normal_81.getpixel(point) for point in x_probe):
        raise AssertionError("temporary X probe remains")
    if all(normal_110.getpixel(point) for point in square_probe):
        raise AssertionError("temporary square probe remains")
    if LATFONT.exists():
        expected_cells = sheet.width // 16 * sheet.height // 16
        if LATFONT.stat().st_size != expected_cells * 64:
            raise AssertionError(".latfont physical cell count differs from sheet")
        if ROM.exists() and ROM.stat().st_mtime >= LATFONT.stat().st_mtime and LATFONT.read_bytes() not in ROM.read_bytes():
            raise AssertionError("linked ROM does not contain exact .latfont")


def draw(mapping, sheet, rows):
    font = ImageFont.load_default()
    scale, row_h, width = 5, 150, 1180
    final = Image.new("RGB", (width, row_h * len(SAMPLES)), "white")
    d = ImageDraw.Draw(final)
    for number, text in enumerate(SAMPLES):
        normal, _records, _ = render(text, mapping, sheet, False)
        production, records, boundaries = render(text, mapping, sheet, True)
        y = number * row_h
        d.text((8, y + 4), text, font=font, fill="black")
        for label, image, yy in (("A Noto reference", normal, 20), ("B accepted proof", normal, 48),
                                 ("C production", production, 76)):
            d.text((110, y + yy), label, font=font, fill="black")
            final.paste(rgb(image), (260, y + yy - 4))
        enlarged = rgb(production).resize((production.width * scale, production.height * scale), Image.Resampling.NEAREST)
        final.paste(enlarged.crop((0, 0, width - 260, 48)), (260, y + 102))
        d.text((110, y + 110), "D enlarged + baseline/cluster boundaries", font=font, fill="black")
        d.line((260, y + 102 + 16 * scale, width - 8, y + 102 + 16 * scale), fill="red")
        for boundary in boundaries:
            x = 260 + boundary * scale
            d.line((x, y + 102, x, y + 149), fill="blue")
    final.save(FINAL)

    variants = mapping["glyphs"]
    cells = Image.new("RGB", (900, max(1, len(variants)) * 90), "white")
    dc = ImageDraw.Draw(cells)
    diffs = Image.new("RGB", (900, max(1, len(variants)) * 90), "white")
    dd = ImageDraw.Draw(diffs)
    for row, entry in enumerate(variants):
        y = row * 90
        source = cell(sheet, int(mapping["hb_to_gba"][str(entry["hb_glyph_id"])]))
        chosen = cell(sheet, entry["compact_index"])
        diff = ImageChops.difference(rgb(source), rgb(chosen))
        label = f"HB {entry['hb_glyph_id']} {entry['glyph_name']} {entry['variant']} compact {entry['compact_index']}"
        dc.text((8, y + 4), label, font=font, fill="black")
        dd.text((8, y + 4), label, font=font, fill="black")
        for target, images in ((cells, (source, chosen)), (diffs, (source, chosen, diff))):
            for col, image in enumerate(images):
                target.paste(rgb(image).resize((64, 64), Image.Resampling.NEAREST), (360 + col * 100, y + 20))
    cells.save(CELLS)
    diffs.save(DIFFERENCE)

    palette_proof = Image.new("RGB", (760, len(variants) * 70), "white")
    dp = ImageDraw.Draw(palette_proof)
    for row, entry in enumerate(variants):
        tile = cell(sheet, entry["compact_index"])
        y = row * 70
        dp.text((8, y + 4), f"{entry['compact_index']} {entry['variant']}", font=font, fill="black")
        for index, label in ((1, "dark main"), (2, "light shadow")):
            mask = tile.point(lambda p, wanted=index: 0 if p == wanted else 255).convert("RGB")
            x = 180 + index * 180
            palette_proof.paste(mask.resize((48, 48), Image.Resampling.NEAREST), (x, y + 16))
            dp.text((x + 52, y + 30), f"index {index} {label}", font=font, fill="black")
    palette_proof.save(PALETTE)


def write_report(mapping, rows):
    variants = Counter(entry["variant"] for entry in mapping["glyphs"])
    transformed = sorted({(row["glyph_name"], row["selected_variant"]) for row in rows if row["selected_variant"] != "normal"})
    rom_hash = digest(ROM) if ROM.exists() else "pending full build"
    lat_hash = digest(LATFONT) if LATFONT.exists() else "pending asset build"
    REPORT.write_text(f"""# Thai production contextual shaping report

## Architecture

Natural Unicode Thai is shaped by HarfBuzz during the build, analyzed by Unicode
cluster, fitted through the ordered production candidates, and encoded as compact
positioned-glyph commands. The unchanged runtime only draws the selected bitmap
with its precomputed offset and advance; it contains no Thai grammar.

## Fit and contextual selection

The solver renders proof-identical normal cells first, measures combined visible
bounds against rows 0–15, tests silhouette separation only where base and upper
mark pixels overlap horizontally, then tries base clearance, compact upper marks,
compact tones, and combined high-stack forms in increasing transformation order.
It fails rather than cropping an unsolved cluster. Tall bases use the permitted
one-row nearest-neighbor reduction before their contextual downshift.

Palette convention is fixed: index 0 transparent, index 1 dark main stroke, and
index 2 light shadow. The sheet remains indexed mode P.

## Generated variants

{dict(sorted(variants.items()))}

Applied transformations: {transformed}

The trace records every selected index, original index, bound, offset adjustment,
advance, and palette count. Normal cells remain proof-identical. Differences in
the difference proof occur only for selected contextual variants.

## Verification

- ROM SHA256: `{rom_hash}`
- linked font asset SHA256: `{lat_hash}`
- temporary X/square probes: absent
- menu source: natural Unicode `เริ่มเกมส์`
- known limitation: 16-pixel fitting requires controlled contextual bitmap forms;
  emulator visual review remains mandatory.

This milestone is not release-ready until the rebuilt ROM is reviewed in an
emulator screenshot.
""", encoding="utf-8")


def build(draw_outputs=True):
    mapping = load_mapping()
    sheet = Image.open(FONT_PNG)
    sheet.load()
    validate(mapping, sheet)
    rows = trace_rows(mapping, sheet)
    with TRACE.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    if draw_outputs:
        draw(mapping, sheet, rows)
    write_report(mapping, rows)
    return rows


if __name__ == "__main__":
    build()
    print(FINAL)
    print(TRACE)
    print(REPORT)
