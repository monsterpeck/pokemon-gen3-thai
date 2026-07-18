#!/usr/bin/env python3
"""Install native standalone Thai vowel/mark assets and migrate the registry."""

from __future__ import annotations

import csv
import shutil
from pathlib import Path

from PIL import Image

from thai_font import MASTER_PATH, REGISTRY_PATH, ROOT, load_registry, open_indexed, tile_box


BACKUP = ROOT / "tools/thai/font/recovery/thai_master_before_combining_renderer.png"
GLYPH_DIR = ROOT / "graphics/fonts/thai/glyphs"

# Explicit native-resolution coordinate artwork. No source glyph is resized or transformed.
PIXELS = {
    0x143: ((0,0,2),(1,0,1),(2,0,1),(3,0,1),(0,1,2),(3,1,1),(0,2,2),(3,2,1)),
    0x144: ((0,0,2),(1,0,1),(1,1,1)),
    0x145: ((5,3,2),(6,3,1),(5,4,2),(6,4,1),(5,5,2),(6,5,1),(5,6,2),(6,6,1),(5,7,2),(6,7,1),(5,8,2),(6,8,1),(5,9,2),(6,9,1),(5,10,2),(6,10,1),(5,11,2),(6,11,1),(5,12,2),(6,12,1),(5,13,2),(6,13,1),(7,13,1)),
    0x146: ((0,0,2),(1,0,1),(2,0,1),(3,0,1),(0,1,2),(3,1,1),(0,2,2),(3,2,1),(1,3,2),(2,3,1)),
    0x147: ((0,0,2),(1,0,1),(2,0,1),(3,0,1),(0,1,2),(3,1,1),(0,2,2),(1,2,1),(2,2,1),(3,2,1),(1,3,2),(2,3,1)),
    0x148: ((0,0,2),(1,0,1),(2,0,1),(3,0,1),(4,0,1),(0,1,2),(4,1,1),(0,2,2),(4,2,1),(1,3,2),(2,3,1),(3,3,1)),
    0x149: ((0,0,2),(1,0,1),(2,0,1),(0,1,2),(2,1,1),(1,2,1),(1,3,1)),
    0x14A: ((0,0,2),(1,0,1),(2,0,1),(3,0,1),(0,1,2),(3,1,1),(1,2,2),(2,2,1),(2,3,1)),
    0x14B: ((0,0,2),(1,0,1),(2,0,1),(3,0,1),(3,1,1),(2,2,1)),
    0x14C: ((0,0,2),(1,0,1),(2,0,1),(1,1,1)),
    0x14D: ((3,3,2),(4,3,1),(8,3,2),(9,3,1),(3,4,2),(4,4,1),(8,4,2),(9,4,1),(3,5,2),(4,5,1),(8,5,2),(9,5,1),(3,6,2),(4,6,1),(8,6,2),(9,6,1),(3,7,2),(4,7,1),(8,7,2),(9,7,1),(3,8,2),(4,8,1),(8,8,2),(9,8,1),(3,9,2),(4,9,1),(8,9,2),(9,9,1),(3,10,2),(4,10,1),(8,10,2),(9,10,1),(3,11,2),(4,11,1),(8,11,2),(9,11,1),(3,12,2),(4,12,1),(8,12,2),(9,12,1),(3,13,2),(4,13,1),(8,13,2),(9,13,1)),
    0x14E: ((5,2,2),(6,2,1),(7,2,1),(5,3,2),(8,3,1),(5,4,2),(8,4,1),(6,5,2),(7,5,1),(7,6,1),(7,7,1),(7,8,1),(7,9,1),(7,10,1),(7,11,1),(7,12,1),(6,13,2),(7,13,1)),
    0x14F: ((4,2,2),(5,2,1),(6,2,1),(7,2,1),(4,3,2),(8,3,1),(5,4,2),(8,4,1),(6,5,2),(7,5,1),(7,6,1),(7,7,1),(7,8,1),(7,9,1),(7,10,1),(7,11,1),(7,12,1),(6,13,2),(7,13,1)),
    0x150: ((4,2,2),(5,2,1),(6,2,1),(7,2,1),(8,2,1),(4,3,2),(8,3,1),(5,4,2),(7,4,1),(6,5,2),(7,5,1),(7,6,1),(7,7,1),(7,8,1),(7,9,1),(7,10,1),(7,11,1),(7,12,1),(6,13,2),(7,13,1)),
    0x151: ((0,1,2),(1,0,1),(2,0,1),(3,1,1),(2,2,1),(1,2,1)),
    0x152: ((0,0,2),(1,0,1),(1,1,1),(2,2,1)),
    0x153: ((0,0,2),(1,0,1),(2,0,1),(0,1,2),(2,1,1),(1,2,1)),
    0x154: ((0,0,2),(1,0,1),(2,0,1),(3,0,1),(1,1,2),(2,1,1),(1,2,1)),
    0x155: ((0,0,2),(1,0,1),(2,0,1),(3,0,1),(0,1,2),(3,1,1),(1,2,2),(2,2,1)),
    0x156: ((0,0,2),(1,0,1),(2,0,1),(0,1,2),(2,1,1),(1,2,1)),
    0x157: ((3,5,2),(4,4,1),(5,4,1),(6,5,1),(6,6,1),(5,7,1),(3,7,2),(4,8,1),(5,8,1),(6,9,1)),
    0x158: ((4,6,2),(5,5,1),(6,5,1),(7,6,1),(7,7,1),(6,8,1),(5,8,1),(4,7,2),(6,10,1)),
    0x159: ((5,3,2),(6,3,1),(7,3,1),(8,4,1),(5,5,2),(6,5,1),(7,5,1),(8,6,1),(5,7,2),(6,7,1),(7,7,1),(5,8,2),(5,9,2),(6,10,1),(7,10,1),(8,9,1)),
    0x15A: ((4,7,2),(5,6,1),(6,6,1),(7,7,1),(7,8,1),(6,9,1),(5,9,1),(4,8,2)),
}

REGISTRY_ROWS = {
    0x143: ("THAI_SARA_I", "ิ", "mark", 4), 0x144: ("THAI_MAI_EK", "่", "mark", 3),
    0x145: ("THAI_SARA_E", "เ", "vowel", 7), 0x146: ("THAI_SARA_II", "ี", "mark", 4),
    0x147: ("THAI_SARA_UE", "ึ", "mark", 4), 0x148: ("THAI_SARA_UEE", "ื", "mark", 5),
    0x149: ("THAI_SARA_U", "ุ", "mark", 3), 0x14A: ("THAI_SARA_UU", "ู", "mark", 4),
    0x14B: ("THAI_MAI_HAN_AKAT", "ั", "mark", 4), 0x14C: ("THAI_SARA_AM", "ำ", "vowel", 10),
    0x14D: ("THAI_SARA_AE", "แ", "vowel", 12), 0x14E: ("THAI_SARA_O", "โ", "vowel", 8),
    0x14F: ("THAI_SARA_AI_MUAN", "ใ", "vowel", 9), 0x150: ("THAI_SARA_AI_MAIMALAI", "ไ", "vowel", 9),
    0x151: ("THAI_MAI_TAIKHU", "็", "mark", 4), 0x152: ("THAI_MAI_THO", "้", "mark", 3),
    0x153: ("THAI_MAI_TRI", "๊", "mark", 3), 0x154: ("THAI_MAI_CHATTAWA", "๋", "mark", 4),
    0x155: ("THAI_THANTHAKHAT", "์", "mark", 4), 0x156: ("THAI_NIKHAHIT", "ํ", "mark", 3),
    0x157: ("THAI_MAIYAMOK", "ๆ", "vowel", 8), 0x158: ("THAI_PAIYANNOI", "ฯ", "vowel", 7),
    0x159: ("THAI_BAHT", "฿", "vowel", 10), 0x15A: ("THAI_SARA_A", "ะ", "vowel", 8),
}


def make_tile(master: Image.Image, pixels) -> Image.Image:
    tile = Image.new("P", (16, 16), 0)
    tile.putpalette(master.getpalette())
    for x, y, color in pixels:
        tile.putpixel((x, y), color)
    return tile


def migrate_registry() -> None:
    existing = [glyph for glyph in load_registry() if glyph.glyph_id < 0x143]
    with REGISTRY_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(("glyph_id", "token", "display", "type", "width", "status", "source"))
        for glyph in existing:
            writer.writerow((f"0x{glyph.glyph_id:03X}", glyph.token, glyph.display, glyph.kind, glyph.width, glyph.status, glyph.source))
        for glyph_id, (token, display, kind, width) in REGISTRY_ROWS.items():
            writer.writerow((f"0x{glyph_id:03X}", token, display, kind, width, "draft", "combining-renderer-native"))


def main() -> None:
    master = open_indexed(MASTER_PATH)
    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    if not BACKUP.exists():
        shutil.copy2(MASTER_PATH, BACKUP)
    GLYPH_DIR.mkdir(parents=True, exist_ok=True)
    for glyph_id, pixels in PIXELS.items():
        tile = make_tile(master, pixels)
        master.paste(tile, tile_box(glyph_id)[:2])
        tile.save(GLYPH_DIR / f"{glyph_id:04x}_{REGISTRY_ROWS[glyph_id][0].lower()}.png", optimize=False)
    master.save(MASTER_PATH, optimize=False)
    migrate_registry()
    print(f"installed {len(PIXELS)} native Thai vowel/mark assets; backup: {BACKUP}")


if __name__ == "__main__":
    main()
