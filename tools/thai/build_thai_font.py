#!/usr/bin/env python3
"""Build the live font sheet, widths, charmap constants, and visual reports."""

from __future__ import annotations

import argparse
import os
import tempfile
from pathlib import Path

from PIL import Image

from thai_font import (
    CELL_SIZE,
    CHARMAP_PATH,
    FONT_PATH,
    MASTER_PATH,
    WIDTHS_PATH,
    ThaiToolError,
    format_widths,
    load_registry,
    open_indexed,
    palette_signature,
    read_widths,
    registry_errors,
    tile_box,
)

ROOT = FONT_PATH.parents[2]
GENERATED_DIR = ROOT / "tools/thai/generated"


def render_charmap(text: str, glyphs) -> str:
    tokens = {glyph.token for glyph in glyphs if glyph.status != "unused"}
    legacy = {
        "THAI_MI", "THAI_MO_MA_EK", "THAI_SARA_E",
        "THAI_RO_RUEA_SARA_I_MAI_EK", "THAI_SO_SUEA_THANTHAKHAT",
    }
    characters = {glyph.display for glyph in glyphs if glyph.status != "unused" and len(glyph.display) == 1}
    kept = []
    for line in text.splitlines():
        left = line.split("=", 1)[0].strip()
        if left in tokens | legacy or (len(left) == 3 and left[0] == chr(39) and left[2] == chr(39) and left[1] in characters):
            continue
        kept.append(line)
    while kept and not kept[-1].strip():
        kept.pop()
    constants = [
        f"{glyph.token} = F9 {glyph.glyph_id - 0x100:02X}"
        for glyph in glyphs if glyph.status != "unused"
    ]
    mappings = [
        f"'{glyph.display}' = F9 {glyph.glyph_id - 0x100:02X}"
        for glyph in glyphs if glyph.status != "unused" and len(glyph.display) == 1
    ]
    return "\n".join(kept) + "\n\n" + "\n".join(mappings) + "\n\n" + "\n".join(constants) + "\n"


def build_outputs(font_path=FONT_PATH, widths_path=WIDTHS_PATH, charmap_path=CHARMAP_PATH):
    glyphs = load_registry()
    errors = registry_errors(glyphs)
    if errors:
        raise ThaiToolError("\n".join(errors))
    master = open_indexed(MASTER_PATH)
    font = open_indexed(font_path)
    if master.size != font.size:
        raise ThaiToolError(f"master size {master.size} does not match font size {font.size}")
    if palette_signature(master) != palette_signature(font):
        raise ThaiToolError("master palette does not match latin_normal.png")
    output_font = font.copy()
    for glyph in glyphs:
        if glyph.status != "unused":
            output_font.paste(master.crop(tile_box(glyph.glyph_id)), tile_box(glyph.glyph_id)[:2])
    widths_text = widths_path.read_text(encoding="utf-8")
    widths, match = read_widths(widths_text)
    for glyph in glyphs:
        if glyph.status != "unused":
            widths[glyph.glyph_id] = glyph.width
    output_widths = widths_text[:match.start(2)] + format_widths(widths) + widths_text[match.end(2):]
    output_charmap = render_charmap(charmap_path.read_text(encoding="utf-8"), glyphs)
    return output_font, output_widths, output_charmap


def image_bytes(image: Image.Image) -> bytes:
    with tempfile.NamedTemporaryFile(suffix=".png") as handle:
        image.save(handle.name, optimize=False)
        return Path(handle.name).read_bytes()


def build_contact_sheet(master: Image.Image, glyphs) -> Image.Image:
    active = [glyph for glyph in glyphs if glyph.status != "unused"]
    rows = (len(active) + 15) // 16
    sheet = Image.new("P", (16 * CELL_SIZE, rows * CELL_SIZE), 0)
    sheet.putpalette(master.getpalette())
    for index, glyph in enumerate(active):
        x = (index % 16) * CELL_SIZE
        y = (index // 16) * CELL_SIZE
        sheet.paste(master.crop(tile_box(glyph.glyph_id)), (x, y))
    return sheet


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if generated outputs are stale")
    args = parser.parse_args()
    try:
        font, widths, charmap = build_outputs()
        glyphs = load_registry()
        master = open_indexed(MASTER_PATH)
        active = [glyph for glyph in glyphs if glyph.status != "unused"]
        outputs = {
            FONT_PATH: image_bytes(font),
            WIDTHS_PATH: widths.encode(),
            CHARMAP_PATH: charmap.encode(),
            GENERATED_DIR / "thai_contact_sheet.png": image_bytes(build_contact_sheet(master, glyphs)),
            GENERATED_DIR / "font_report.txt": (
                f"registered={len(active)}\n"
                f"final={sum(g.status == 'final' for g in active)}\n"
                f"draft={sum(g.status == 'draft' for g in active)}\n"
                f"remaining_slots={512 - (max(g.glyph_id for g in active) + 1)}\n"
            ).encode(),
        }
        stale = [path for path, data in outputs.items() if not path.exists() or path.read_bytes() != data]
        if args.check:
            if stale:
                raise ThaiToolError("stale generated output: " + ", ".join(str(path) for path in stale))
            print("Thai font outputs are up to date")
            return 0
        for path in stale:
            atomic_write(path, outputs[path])
            print(f"updated {path.relative_to(ROOT)}")
        if not stale:
            print("Thai font outputs already up to date")
        return 0
    except (OSError, ThaiToolError) as error:
        print(f"error: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
