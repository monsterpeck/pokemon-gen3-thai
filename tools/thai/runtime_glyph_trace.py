#!/usr/bin/env python3
"""Verify and reconstruct the production positioned-glyph stream."""
from __future__ import annotations

import argparse
import hashlib
import json
import struct
from pathlib import Path

from PIL import Image

from noto_thai import GENERATED, ROOT, THAI
from shape_thai_text import COMMAND_SIZE, CMD_BEGIN, CMD_THAI_POSITIONED, encode_run, load_mapping

TEXT = "เริ่มเกมส์"
SHEET = ROOT / "graphics/fonts/thai_shaped.png"
LATFONT = ROOT / "build/assets/graphics/fonts/thai_shaped.png.latfont"
TRACE = GENERATED / "start_game_runtime_glyph_trace.md"
RECONSTRUCTION = GENERATED / "start_game_runtime_reconstruction.png"
WORDS_PER_GLYPH = 0x20
BYTES_PER_GLYPH = WORDS_PER_GLYPH * 2


def signed(value: int) -> int:
    return value - 256 if value >= 128 else value


def decode(data: bytes):
    records = []
    for offset in range(0, len(data), COMMAND_SIZE):
        command = data[offset:offset + COMMAND_SIZE]
        if len(command) != COMMAND_SIZE or command[:2] != bytes((CMD_BEGIN, CMD_THAI_POSITIONED)):
            raise ValueError(f"invalid positioned-glyph command at byte {offset}")
        records.append(dict(
            command=command,
            glyph_index=command[2] | command[3] << 8,
            x_offset=signed(command[4]),
            y_offset=signed(command[5]),
            x_advance=command[6],
            flags=command[7],
        ))
    return records


def bbox(cell: Image.Image):
    points = [(x, y) for y in range(16) for x in range(16) if cell.getpixel((x, y))]
    if not points:
        return None
    xs, ys = zip(*points)
    return min(xs), min(ys), max(xs) + 1, max(ys) + 1


def reconstruct(records, sheet):
    width = sum(r["x_advance"] for r in records) + 24
    canvas = Image.new("P", (width, 28), 0)
    canvas.putpalette(sheet.getpalette())
    pen_x = 4
    for record in records:
        index = record["glyph_index"]
        cell = sheet.crop(((index % 16) * 16, (index // 16) * 16,
                           (index % 16 + 1) * 16, (index // 16 + 1) * 16))
        # Mirrors RenderThaiPositionedGlyph: currentX + s8 xOffset and
        # currentY + 12 + s8 yOffset. Index zero is transparent.
        draw_x = max(0, pen_x + record["x_offset"])
        draw_y = max(0, 4 + 12 + record["y_offset"])
        canvas.paste(cell, (draw_x, draw_y), cell.point(lambda p: 255 if p else 0).convert("L"))
        pen_x += record["x_advance"]
    canvas.save(RECONSTRUCTION, optimize=False)


def verify_and_generate():
    mapping = load_mapping()
    encoded, shaped, _ = encode_run(TEXT, mapping)
    decoded = decode(encoded)
    if len(decoded) != len(shaped):
        raise AssertionError("encoder/decoder record count mismatch")
    sheet = Image.open(SHEET)
    sheet.load()
    if sheet.mode != "P" or sheet.width != 256 or sheet.height % 16:
        raise AssertionError("shaped sheet must be a 256-wide indexed 16x16 grid")
    glyph_count = len(mapping["glyphs"])
    if LATFONT.stat().st_size % BYTES_PER_GLYPH:
        raise AssertionError(".latfont size is not a whole number of 16x16 glyphs")
    stored_count = LATFONT.stat().st_size // BYTES_PER_GLYPH
    if stored_count < glyph_count:
        raise AssertionError(".latfont contains fewer cells than the compact map")

    rows = []
    for position, (runtime, shaped_record) in enumerate(zip(decoded, shaped)):
        hb_id = shaped_record["glyph_id"]
        compact = int(shaped_record["selected_compact_index"])
        if runtime["glyph_index"] != compact or compact >= glyph_count:
            raise AssertionError(f"glyph {position}: compact/runtime index mismatch")
        byte_start = compact * BYTES_PER_GLYPH
        byte_end = byte_start + BYTES_PER_GLYPH
        if byte_end > LATFONT.stat().st_size:
            raise AssertionError(f"glyph {position}: source read escapes .latfont")
        cell = sheet.crop(((compact % 16) * 16, (compact // 16) * 16,
                           (compact % 16 + 1) * 16, (compact // 16 + 1) * 16))
        rows.append((runtime, shaped_record, compact, cell, byte_start))

    if next(c for r, s, c, _, _ in rows if s["glyph_id"] == 81) != int(mapping["upper_clearance_hb_to_gba"]["81"]):
        raise AssertionError("ร must decode to its clearance compact index")
    if next(c for r, s, c, _, _ in rows if s["glyph_id"] == 110) != int(mapping["upper_clearance_hb_to_gba"]["110"]):
        raise AssertionError("ส must decode to its clearance compact index")

    lines = [
        "# เริ่มเกมส์ production runtime glyph trace", "",
        f"The production stream contains `{len(rows)}` fixed-size commands. The `.latfont` is `{LATFONT.stat().st_size}` bytes: "
        f"`{stored_count}` physical cells × `{BYTES_PER_GLYPH}` bytes (`{WORDS_PER_GLYPH}` u16 words). "
        "Each glyph is four 8×8 2-bpp tiles, matching `DecompressGlyphTile` and the Latin 16×16 path.", "",
        "| # | source cluster | Unicode | HB ID | glyph name | compact index | cell | command bytes | decoded index | u16 offset | xOffset | yOffset | xAdvance | bitmap SHA256 | bbox |",
        "|---:|---|---|---:|---|---:|---|---|---:|---:|---:|---:|---:|---|---|",
    ]
    for i, (runtime, shaped_record, compact, cell, byte_start) in enumerate(rows):
        start = shaped_record["cluster"]
        following = [s[1]["cluster"] for s in rows[i + 1:] if s[1]["cluster"] != start]
        end = min(following) if following else len(TEXT)
        cluster = TEXT[start:end]
        unicode_seq = " ".join(f"U+{ord(ch):04X}" for ch in cluster)
        digest = hashlib.sha256(cell.tobytes()).hexdigest()
        box = bbox(cell)
        command_hex = " ".join(f"{b:02X}" for b in runtime["command"])
        lines.append(
            f"| {i} | {cluster} | {unicode_seq} | {shaped_record['glyph_id']} | {shaped_record['glyph_name']} | "
            f"{compact} | ({compact % 16},{compact // 16}) | `{command_hex}` | {runtime['glyph_index']} | "
            f"0x{byte_start // 2:04X} | {runtime['x_offset']} | {runtime['y_offset']} | "
            f"{runtime['x_advance']} | `{digest}` | `{box}` |"
        )
    lines += ["", "The HB ID, compact map index, encoded index, and runtime-decoded index are independently checked above.", ""]
    TRACE.write_text("\n".join(lines), encoding="utf-8")
    reconstruct(decoded, sheet)
    return rows


if __name__ == "__main__":
    verify_and_generate()
    print(TRACE)
    print(RECONSTRUCTION)
