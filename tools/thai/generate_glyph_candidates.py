#!/usr/bin/env python3
"""Generate six native-pixel candidate sets for the Thai menu draft glyphs."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

from thai_font import CELL_SIZE, MASTER_PATH, ROOT, open_indexed, tile_box


OUTPUT_DIR = ROOT / "tools/thai/generated/glyph_candidates"
SHEET_PATH = OUTPUT_DIR / "candidate_sheet.png"
VERSIONS = tuple(f"V{number:02d}" for number in range(1, 7))
TARGET_IDS = (0x145, 0x146, 0x147)
REFERENCE_IDS = (0x118, 0x136, 0x138, 0x13D)  # à¸ à¸¡ à¸£ à¸ª
WORD_IDS = (0x145, 0x146, 0x136, 0x145, 0x118, 0x136, 0x147)
TARGET_SCALE = 8
WORD_SCALE = 4


# Every added pixel is authored explicitly as (x, y, palette_index).
# Cluster patterns are painted only into empty pixels of an unchanged base tile.
PATTERNS = {
    "V01": {
        0x145: ((6, 4, 2), (7, 4, 1), (6, 5, 2), (7, 5, 1), (6, 6, 2), (7, 6, 1), (6, 7, 2), (7, 7, 1), (6, 8, 2), (7, 8, 1), (6, 9, 2), (7, 9, 1), (6, 10, 2), (7, 10, 1), (6, 11, 2), (7, 11, 1), (6, 12, 2), (7, 12, 1), (5, 13, 2), (6, 13, 2), (7, 13, 1)),
        0x146: ((7, 0, 2), (8, 0, 1), (9, 0, 1), (7, 1, 2), (10, 1, 1), (7, 2, 2), (8, 2, 1), (9, 2, 1), (11, 0, 2), (12, 0, 1), (12, 1, 1)),
        0x147: ((7, 0, 2), (8, 0, 1), (9, 0, 1), (10, 0, 1), (7, 1, 2), (10, 1, 1), (8, 2, 2), (9, 2, 1)),
    },
    "V02": {
        0x145: ((5, 4, 2), (6, 4, 1), (5, 5, 2), (6, 5, 1), (5, 6, 2), (6, 6, 1), (5, 7, 2), (6, 7, 1), (5, 8, 2), (6, 8, 1), (5, 9, 2), (6, 9, 1), (5, 10, 2), (6, 10, 1), (5, 11, 2), (6, 11, 1), (5, 12, 2), (6, 12, 1), (5, 13, 2), (6, 13, 1), (7, 13, 1)),
        0x146: ((6, 0, 2), (7, 0, 1), (8, 0, 1), (9, 0, 1), (6, 1, 2), (9, 1, 1), (7, 2, 2), (8, 2, 1), (10, 0, 2), (11, 0, 1), (11, 1, 1)),
        0x147: ((6, 0, 2), (7, 0, 1), (8, 0, 1), (9, 0, 1), (6, 1, 2), (9, 1, 1), (7, 2, 2), (8, 2, 1), (9, 2, 1)),
    },
    "V03": {
        0x145: ((6, 3, 2), (7, 3, 1), (6, 4, 2), (7, 4, 1), (6, 5, 2), (7, 5, 1), (6, 6, 2), (7, 6, 1), (6, 7, 2), (7, 7, 1), (6, 8, 2), (7, 8, 1), (6, 9, 2), (7, 9, 1), (6, 10, 2), (7, 10, 1), (6, 11, 2), (7, 11, 1), (6, 12, 2), (7, 12, 1), (5, 13, 2), (6, 13, 2), (7, 13, 1), (8, 13, 1)),
        0x146: ((7, 0, 2), (8, 0, 1), (9, 0, 1), (10, 0, 1), (7, 1, 2), (10, 1, 1), (8, 2, 2), (9, 2, 1), (11, 1, 2), (12, 1, 1), (12, 2, 1)),
        0x147: ((7, 0, 2), (8, 0, 1), (9, 0, 1), (10, 0, 1), (7, 1, 2), (10, 1, 1), (8, 2, 2), (9, 2, 1), (10, 2, 1)),
    },
    "V04": {
        0x145: ((7, 4, 2), (8, 4, 1), (7, 5, 2), (8, 5, 1), (7, 6, 2), (8, 6, 1), (7, 7, 2), (8, 7, 1), (7, 8, 2), (8, 8, 1), (7, 9, 2), (8, 9, 1), (7, 10, 2), (8, 10, 1), (7, 11, 2), (8, 11, 1), (7, 12, 2), (8, 12, 1), (6, 13, 2), (7, 13, 2), (8, 13, 1)),
        0x146: ((8, 0, 2), (9, 0, 1), (10, 0, 1), (8, 1, 2), (11, 1, 1), (8, 2, 2), (9, 2, 1), (10, 2, 1), (12, 0, 2), (13, 0, 1), (13, 1, 1)),
        0x147: ((8, 0, 2), (9, 0, 1), (10, 0, 1), (11, 0, 1), (8, 1, 2), (11, 1, 1), (9, 2, 2), (10, 2, 1)),
    },
    "V05": {
        0x145: ((5, 3, 2), (6, 3, 1), (5, 4, 2), (6, 4, 1), (5, 5, 2), (6, 5, 1), (5, 6, 2), (6, 6, 1), (5, 7, 2), (6, 7, 1), (5, 8, 2), (6, 8, 1), (5, 9, 2), (6, 9, 1), (5, 10, 2), (6, 10, 1), (5, 11, 2), (6, 11, 1), (5, 12, 2), (6, 12, 1), (5, 13, 2), (6, 13, 1), (7, 13, 1)),
        0x146: ((6, 0, 2), (7, 0, 1), (8, 0, 1), (9, 0, 1), (6, 1, 2), (9, 1, 1), (7, 2, 2), (8, 2, 1), (10, 1, 2), (11, 1, 1), (11, 2, 1)),
        0x147: ((6, 0, 2), (7, 0, 1), (8, 0, 1), (9, 0, 1), (10, 0, 1), (6, 1, 2), (10, 1, 1), (7, 2, 2), (8, 2, 1), (9, 2, 1)),
    },
    "V06": {
        0x145: ((6, 4, 2), (7, 4, 1), (8, 4, 1), (6, 5, 2), (7, 5, 1), (6, 6, 2), (7, 6, 1), (6, 7, 2), (7, 7, 1), (6, 8, 2), (7, 8, 1), (6, 9, 2), (7, 9, 1), (6, 10, 2), (7, 10, 1), (6, 11, 2), (7, 11, 1), (6, 12, 2), (7, 12, 1), (5, 13, 2), (6, 13, 2), (7, 13, 1), (8, 13, 1)),
        0x146: ((7, 0, 2), (8, 0, 1), (9, 0, 1), (10, 0, 1), (7, 1, 2), (10, 1, 1), (8, 2, 2), (9, 2, 1), (11, 0, 2), (12, 0, 1), (13, 0, 1), (12, 1, 1)),
        0x147: ((7, 0, 2), (8, 0, 1), (9, 0, 1), (10, 0, 1), (11, 0, 1), (7, 1, 2), (11, 1, 1), (8, 2, 2), (9, 2, 1), (10, 2, 1)),
    },
}


def blank_tile(master: Image.Image) -> Image.Image:
    tile = Image.new("P", (CELL_SIZE, CELL_SIZE), 0)
    tile.putpalette(master.getpalette())
    return tile


def add_explicit_pixels(tile: Image.Image, pattern) -> None:
    for x, y, color in pattern:
        if not (0 <= x < CELL_SIZE and 0 <= y < CELL_SIZE and color in (1, 2, 3)):
            raise ValueError(f"invalid explicit pixel {(x, y, color)}")
        # Never disturb a copied consonant pixel.
        if tile.getpixel((x, y)) == 0:
            tile.putpixel((x, y), color)


def candidate_set(version: str, master: Image.Image | None = None) -> dict[int, Image.Image]:
    if version not in PATTERNS:
        raise ValueError(f"unknown candidate {version}; choose one of {', '.join(VERSIONS)}")
    master = master or open_indexed(MASTER_PATH)
    result = {
        0x145: blank_tile(master),
        0x146: master.crop(tile_box(0x138)).copy(),
        0x147: master.crop(tile_box(0x13D)).copy(),
    }
    for glyph_id, pattern in PATTERNS[version].items():
        add_explicit_pixels(result[glyph_id], pattern)
    return result


def enlarge_pixels(image: Image.Image, scale: int) -> Image.Image:
    """Paint each source pixel as a solid rectangle; never resample artwork."""
    colors = image.convert("RGB")
    enlarged = Image.new("RGB", (image.width * scale, image.height * scale))
    draw = ImageDraw.Draw(enlarged)
    for y in range(image.height):
        for x in range(image.width):
            color = colors.getpixel((x, y))
            draw.rectangle((x * scale, y * scale, (x + 1) * scale - 1, (y + 1) * scale - 1), fill=color)
    return enlarged


def draw_grid_tile(sheet: Image.Image, tile: Image.Image, origin: tuple[int, int], scale: int) -> None:
    x0, y0 = origin
    scaled = enlarge_pixels(tile, scale)
    sheet.paste(scaled, origin)
    draw = ImageDraw.Draw(sheet)
    for line in range(CELL_SIZE + 1):
        x = x0 + line * scale
        y = y0 + line * scale
        draw.line((x, y0, x, y0 + CELL_SIZE * scale), fill="#4b5563")
        draw.line((x0, y, x0 + CELL_SIZE * scale, y), fill="#4b5563")


def compose_word(candidates: dict[int, Image.Image], master: Image.Image) -> Image.Image:
    word = Image.new("P", (len(WORD_IDS) * CELL_SIZE, CELL_SIZE), 0)
    word.putpalette(master.getpalette())
    for index, glyph_id in enumerate(WORD_IDS):
        tile = candidates.get(glyph_id, master.crop(tile_box(glyph_id)))
        word.paste(tile, (index * CELL_SIZE, 0))
    return word


def candidate_sheet(all_candidates: dict[str, dict[int, Image.Image]], master: Image.Image) -> Image.Image:
    margin = 16
    row_height = CELL_SIZE * TARGET_SCALE + 38
    header_height = 100
    target_width = 3 * (CELL_SIZE * TARGET_SCALE + margin)
    word_width = len(WORD_IDS) * CELL_SIZE * WORD_SCALE
    width = margin * 3 + target_width + word_width
    height = header_height + len(VERSIONS) * row_height
    sheet = Image.new("RGB", (width, height), "#191d23")
    draw = ImageDraw.Draw(sheet)
    draw.text((margin, 8), "Thai glyph candidates - native 16x16 coordinate patterns", fill="white")
    draw.text((margin, 24), "Targets: 0x145 E  |  0x146 RO+I+EK  |  0x147 SO+THANTHAKHAT", fill="#ffd166")
    draw.text((margin, 42), "References (unchanged): KO KAI / MO MA / RO RUEA / SO SUEA", fill="#9be564")
    ref_x = margin
    for glyph_id in REFERENCE_IDS:
        tile = enlarge_pixels(master.crop(tile_box(glyph_id)), 3)
        sheet.paste(tile, (ref_x, 50))
        draw.rectangle((ref_x, 50, ref_x + 48, 98), outline="#6b7280")
        ref_x += 56
    for row, version in enumerate(VERSIONS):
        y0 = header_height + row * row_height
        draw.text((margin, y0 + 2), version, fill="#ffcf56")
        x = margin + 34
        for glyph_id in TARGET_IDS:
            draw_grid_tile(sheet, all_candidates[version][glyph_id], (x, y0 + 20), TARGET_SCALE)
            draw.text((x, y0 + 4), f"0x{glyph_id:03X}", fill="white")
            x += CELL_SIZE * TARGET_SCALE + margin
        word = enlarge_pixels(compose_word(all_candidates[version], master), WORD_SCALE)
        word_x = margin * 2 + target_width
        sheet.paste(word, (word_x, y0 + 46))
        draw.text((word_x, y0 + 25), f"{version} full word: encoded E-RI-M-E-K-M-S", fill="#7dd3fc")
        draw.rectangle((word_x, y0 + 46, word_x + word_width, y0 + 46 + CELL_SIZE * WORD_SCALE), outline="#6b7280")
    return sheet


def generate_candidates(output_dir: Path = OUTPUT_DIR) -> Path:
    master = open_indexed(MASTER_PATH)
    output_dir.mkdir(parents=True, exist_ok=True)
    all_candidates = {}
    for version in VERSIONS:
        candidates = candidate_set(version, master)
        all_candidates[version] = candidates
        version_dir = output_dir / version
        version_dir.mkdir(parents=True, exist_ok=True)
        for glyph_id, tile in candidates.items():
            tile.save(version_dir / f"{glyph_id:04x}.png", optimize=False)
    sheet_path = output_dir / "candidate_sheet.png"
    candidate_sheet(all_candidates, master).save(sheet_path)
    print(f"generated {len(VERSIONS)} complete candidate sets")
    print(f"sheet: {sheet_path}")
    return sheet_path


if __name__ == "__main__":
    generate_candidates()

