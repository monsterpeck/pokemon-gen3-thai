#!/usr/bin/env python3
"""Validate the canonical Thai font sources and generated integration."""

from __future__ import annotations

import csv
import hashlib

from thai_font import (
    CELL_SIZE,
    CHARMAP_PATH,
    FONT_PATH,
    MASTER_COLUMNS,
    MASTER_PATH,
    ROOT,
    WIDTHS_PATH,
    load_registry,
    open_indexed,
    palette_signature,
    read_widths,
    registry_errors,
    renderer_errors,
    tile_box,
)


def validate() -> list[str]:
    glyphs = load_registry()
    errors = registry_errors(glyphs)
    try:
        master = open_indexed(MASTER_PATH)
        font = open_indexed(FONT_PATH)
    except ValueError as error:
        return errors + [str(error)]
    if master.width != MASTER_COLUMNS * CELL_SIZE or master.height % CELL_SIZE:
        errors.append("master must have 16 columns of 16x16 cells")
    if master.size != font.size:
        errors.append("master and latin_normal.png dimensions differ")
    if palette_signature(master) != palette_signature(font):
        errors.append("master and latin_normal.png palettes differ")
    allowed_pixels = set(font.getdata())
    if not set(master.getdata()) <= allowed_pixels:
        errors.append("master uses palette indexes absent from latin_normal.png")
    background = master.getpixel((0, 0))
    for glyph in glyphs:
        if glyph.glyph_id >= (master.width // CELL_SIZE) * (master.height // CELL_SIZE):
            errors.append(f"{glyph.token}: missing master-sheet cell")
            continue
        tile = master.crop(tile_box(glyph.glyph_id))
        drawn = [(x, y) for y in range(CELL_SIZE) for x in range(CELL_SIZE)
                 if tile.getpixel((x, y)) != background]
        if glyph.status == "final" and not drawn:
            errors.append(f"{glyph.token}: final glyph is blank")
        if drawn and glyph.kind in {"base", "cluster"}:
            right = max(x for x, _ in drawn) + 1
            if glyph.width < right:
                errors.append(f"{glyph.token}: width {glyph.width} does not cover pixel column {right}")
        if glyph.status != "unused" and list(tile.getdata()) != list(font.crop(tile_box(glyph.glyph_id)).getdata()):
            errors.append(f"{glyph.token}: generated font tile differs from master")
    widths, _ = read_widths(WIDTHS_PATH.read_text(encoding="utf-8"))
    for glyph in glyphs:
        if glyph.status != "unused" and widths[glyph.glyph_id] != glyph.width:
            errors.append(f"{glyph.token}: src/fonts.c width is {widths[glyph.glyph_id]}, expected {glyph.width}")
    charmap = CHARMAP_PATH.read_text(encoding="utf-8")
    for glyph in glyphs:
        if glyph.status != "unused":
            expected = f"{glyph.token} = F9 {glyph.glyph_id - 0x100:02X}"
            if charmap.count(expected) != 1:
                errors.append(f"{glyph.token}: charmap constant missing, duplicated, or inconsistent")
    hash_path = ROOT / "tools/thai/font/consonant_hashes.csv"
    with hash_path.open(newline="", encoding="ascii") as handle:
        expected_hashes = {int(row["glyph_id"], 0): row["sha256"] for row in csv.DictReader(handle)}
    if len(expected_hashes) != 42:
        errors.append(f"consonant preservation manifest has {len(expected_hashes)} entries, expected 42")
    for glyph_id, expected in expected_hashes.items():
        actual = hashlib.sha256(bytes(master.crop(tile_box(glyph_id)).getdata())).hexdigest()
        if actual != expected:
            errors.append(f"0x{glyph_id:03X}: preserved consonant pixels changed")
    return errors


def main() -> int:
    try:
        errors = validate()
    except (OSError, ValueError) as error:
        errors = [str(error)]
    if errors:
        print("Thai font validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    glyphs = load_registry()
    active = sum(g.status != "unused" for g in glyphs)
    print(f"Thai font validation passed: {active} registered glyphs, {512 - (max(g.glyph_id for g in glyphs) + 1)} free slots")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
