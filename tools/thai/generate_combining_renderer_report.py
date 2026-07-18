#!/usr/bin/env python3
"""Append canonical glyph and anchor tables to the combining-renderer report."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / "tools/thai/generated/thai_combining_renderer_report.md"
GLYPHS = ROOT / "tools/thai/font/thai_glyph_metadata.csv"
BASES = ROOT / "tools/thai/font/thai_base_metrics.csv"
MARKER = "## Complete glyph allocation table"


def table(headers, rows):
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    lines.extend("| " + " | ".join(row) + " |" for row in rows)
    return "\n".join(lines)


def main():
    text = REPORT.read_text(encoding="utf-8")
    if MARKER in text:
        text = text.split(MARKER, 1)[0].rstrip() + "\n"
    with GLYPHS.open(newline="", encoding="utf-8") as handle:
        glyphs = list(csv.DictReader(handle))
    with BASES.open(newline="", encoding="utf-8") as handle:
        bases = list(csv.DictReader(handle))
    glyph_rows = [[row[key] or "—" for key in ("glyph_id", "char", "class", "advance", "mark_x", "mark_y", "second_level_y", "component_id")]
                  for row in glyphs]
    base_rows = [[row[key] for key in ("glyph_id", "advance", "upper_x", "upper_y", "lower_x", "lower_y", "tone_x", "tone_y", "shape_group")]
                 for row in bases]
    text += "\n" + MARKER + "\n\n"
    text += table(["ID", "Character", "Class", "Advance", "Offset X", "Offset Y", "Second-level Y", "Component"], glyph_rows)
    text += "\n\n## Complete per-base anchor metrics\n\n"
    text += table(["ID", "Advance", "Upper X", "Upper Y", "Lower X", "Lower Y", "Tone X", "Tone Y", "Shape"], base_rows)
    text += "\n"
    REPORT.write_text(text, encoding="utf-8")
    print(f"wrote {REPORT}")


if __name__ == "__main__":
    main()
