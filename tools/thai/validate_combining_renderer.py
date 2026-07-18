#!/usr/bin/env python3
"""Validate Thai renderer metadata, mappings, source strings, and preserved pixels."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path

from thai_font import CHARMAP_PATH, ROOT, load_registry, open_indexed, tile_box

GLYPH_METADATA = ROOT / "tools/thai/font/thai_glyph_metadata.csv"
BASE_METRICS = ROOT / "tools/thai/font/thai_base_metrics.csv"
ACCEPTANCE = ("เริ่มเกมส์", "โปเกมอน", "ผู้เล่น", "น้ำ เก็บไว้", "ญี่ปุ่น", "ความสามารถ")
REQUIRED_CHARS = set("\u0e30\u0e31\u0e32\u0e33\u0e34\u0e35\u0e36\u0e37\u0e38\u0e39\u0e40\u0e41\u0e42\u0e43\u0e44\u0e47\u0e48\u0e49\u0e4a\u0e4b\u0e4c\u0e4d\u0e46\u0e2f\u0e3f")
VALID_CLASSES = {"BASE", "LEADING_VOWEL", "SPACING_VOWEL", "UPPER_VOWEL", "LOWER_VOWEL", "TONE", "THAN_THAKHAT", "NIKHAHIT", "SARA_AM", "PUNCTUATION"}


def validate() -> list[str]:
    errors: list[str] = []
    glyphs = [glyph for glyph in load_registry() if glyph.status != "unused"]
    with GLYPH_METADATA.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        expected_fields = {"glyph_id", "char", "class", "advance", "mark_x", "mark_y", "second_level_y", "component_id"}
        if set(reader.fieldnames or ()) != expected_fields:
            errors.append("glyph metadata schema is incomplete")
        metadata = list(reader)
    by_char = {row["char"]: row for row in metadata}
    if len(by_char) != len(metadata):
        errors.append("every registered glyph must have exactly one character and class")
    if REQUIRED_CHARS - set(by_char):
        errors.append(f"required standalone mappings missing: {sorted(REQUIRED_CHARS - set(by_char))!r}")
    for row in metadata:
        if row["class"] not in VALID_CLASSES:
            errors.append(f"{row['char']}: invalid Thai class {row['class']!r}")
    mapped_ids = {int(row["glyph_id"], 0) for row in metadata}
    if mapped_ids != {glyph.glyph_id for glyph in glyphs}:
        errors.append("metadata must cover exactly all active registry glyphs")
    for text in ACCEPTANCE:
        missing = {char for char in text if "\u0e00" <= char <= "\u0e7f" and char not in by_char}
        if missing:
            errors.append(f"{text}: unmapped Thai characters {sorted(missing)!r}")
    combining = {"UPPER_VOWEL", "LOWER_VOWEL", "TONE", "THAN_THAKHAT", "NIKHAHIT"}
    for row in metadata:
        if row["class"] in combining and int(row["advance"]):
            errors.append(f"{row['char']}: combining glyph has nonzero advance")
        if row["class"] in {"LEADING_VOWEL", "SPACING_VOWEL", "PUNCTUATION"} and int(row["advance"]) <= 0:
            errors.append(f"{row['char']}: spacing glyph must have positive advance")
    with BASE_METRICS.open(newline="", encoding="utf-8") as handle:
        metric_ids = {int(row["glyph_id"], 0) for row in csv.DictReader(handle)}
    base_ids = {int(row["glyph_id"], 0) for row in metadata if row["class"] == "BASE"}
    if metric_ids != base_ids:
        errors.append("base metrics must cover exactly the BASE glyphs")
    charmap = CHARMAP_PATH.read_text(encoding="utf-8")
    for row in metadata:
        expected = f"'{row['char']}' = F9 {int(row['glyph_id'], 0) - 0x100:02X}"
        if charmap.count(expected) != 1:
            errors.append(f"missing or duplicate direct mapping: {expected}")
    source = (ROOT / "src/strings.c").read_text(encoding="utf-8")
    birch = (ROOT / "data/text/birch_speech.inc").read_text(encoding="utf-8")
    if chr(0xE40)+chr(0xE23)+chr(0xE34)+chr(0xE48)+chr(0xE21)+chr(0xE40)+chr(0xE01)+chr(0xE21)+chr(0xE2A)+chr(0xE4C) not in source:
        errors.append("New Game source is not natural Unicode Thai")
    for text in ACCEPTANCE:
        if text not in source + birch:
            errors.append(f"acceptance text absent from controlled in-game source: {text}")
    if "{THAI_RO_RUEA_SARA_I_MAI_EK}" in source or "{THAI_SO_SUEA_THANTHAKHAT}" in source:
        errors.append("normal game source still uses precomposed Thai cluster constants")
    master = open_indexed(ROOT / "tools/thai/font/thai_master.png")
    with (ROOT / "tools/thai/font/consonant_hashes.csv").open(newline="", encoding="ascii") as handle:
        hashes = {int(row["glyph_id"], 0): row["sha256"] for row in csv.DictReader(handle)}
    if len(hashes) != 42:
        errors.append("consonant preservation manifest must contain 42 glyphs")
    for glyph_id, expected in hashes.items():
        actual = hashlib.sha256(bytes(master.crop(tile_box(glyph_id)).getdata())).hexdigest()
        if actual != expected:
            errors.append(f"0x{glyph_id:03X}: preserved consonant pixels changed")
    required = {
        "src/text.c": ("RenderThaiGlyph", "ResetThaiTextState", "GetThaiGlyphInfo"),
        "include/text.h": ("struct ThaiTextState", "baseGlyphId", "upperStackLevel"),
        "src/thai_text.c": ("gThaiGlyphInfo", "gThaiBaseMetrics", "GetThaiBaseMetrics"),
    }
    for relative, markers in required.items():
        text = (ROOT / relative).read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                errors.append(f"{relative}: missing {marker}")
    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("Thai combining renderer validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Thai combining renderer validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
