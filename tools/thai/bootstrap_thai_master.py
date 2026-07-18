#!/usr/bin/env python3
"""One-time/recovery utility: seed the Thai master from the installed font."""

from pathlib import Path

from PIL import Image

from thai_font import (
    CELL_SIZE,
    FONT_PATH,
    MASTER_COLUMNS,
    MASTER_PATH,
    ThaiToolError,
    load_registry,
    open_indexed,
    registry_errors,
    tile_box,
)


def build_master(font_path: Path = FONT_PATH, output: Path = MASTER_PATH) -> None:
    glyphs = load_registry()
    errors = registry_errors(glyphs)
    if errors:
        raise ThaiToolError("\n".join(errors))
    font = open_indexed(font_path)
    if font.width // CELL_SIZE != MASTER_COLUMNS or font.height % CELL_SIZE:
        raise ThaiToolError("installed font must use 16 columns of 16x16 cells")
    master = Image.new("P", font.size, 0)
    master.putpalette(font.getpalette())
    for glyph in glyphs:
        master.paste(font.crop(tile_box(glyph.glyph_id)), tile_box(glyph.glyph_id)[:2])
    output.parent.mkdir(parents=True, exist_ok=True)
    master.save(output, optimize=False)
    print(f"wrote {output} with {len(glyphs)} registered cells")


if __name__ == "__main__":
    try:
        build_master()
    except ThaiToolError as error:
        raise SystemExit(f"error: {error}") from error
