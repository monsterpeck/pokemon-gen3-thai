#!/usr/bin/env python3
"""Shared, side-effect-free support for the Thai font toolchain."""

from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
FONT_DIR = ROOT / "tools/thai/font"
REGISTRY_PATH = FONT_DIR / "glyph_registry.csv"
MASTER_PATH = FONT_DIR / "thai_master.png"
FONT_PATH = ROOT / "graphics/fonts/latin_normal.png"
WIDTHS_PATH = ROOT / "src/fonts.c"
CHARMAP_PATH = ROOT / "charmap.txt"
CELL_SIZE = 16
MASTER_COLUMNS = 16
MAX_GLYPH_ID = 0x1FF
VALID_TYPES = {"base", "vowel", "mark", "cluster", "punctuation"}
VALID_STATUSES = {"final", "draft", "unused"}
WIDTH_ARRAY_RE = re.compile(
    r"(ALIGNED\(4\) const u8 gFontNormalLatinGlyphWidths\[\] = \{\n)"
    r"(.*?)"
    r"(\n\};)",
    re.DOTALL,
)
RENDERER_FORBIDDEN = (
    "thaiBase",
    "hasThaiBase",
    "IsThaiBaseGlyph",
    "IsThaiCombiningMark",
    "Thai runtime probe",
    "Thai position probe",
)


class ThaiToolError(ValueError):
    pass


@dataclass(frozen=True)
class Glyph:
    glyph_id: int
    token: str
    display: str
    kind: str
    width: int
    status: str
    source: str

    @property
    def cell(self) -> tuple[int, int]:
        return self.glyph_id % MASTER_COLUMNS, self.glyph_id // MASTER_COLUMNS


def load_registry(path: Path = REGISTRY_PATH) -> list[Glyph]:
    required = {"glyph_id", "token", "display", "type", "width", "status", "source"}
    try:
        handle = path.open(newline="", encoding="utf-8")
    except OSError as error:
        raise ThaiToolError(f"cannot read registry {path}: {error}") from error
    with handle:
        reader = csv.DictReader(handle)
        if set(reader.fieldnames or ()) != required:
            raise ThaiToolError(
                f"registry columns must be {','.join(required)}; got {reader.fieldnames}"
            )
        glyphs: list[Glyph] = []
        for line, row in enumerate(reader, 2):
            try:
                glyph = Glyph(
                    glyph_id=int(row["glyph_id"], 0),
                    token=row["token"].strip(),
                    display=row["display"],
                    kind=row["type"].strip(),
                    width=int(row["width"]),
                    status=row["status"].strip(),
                    source=row["source"].strip(),
                )
            except (TypeError, ValueError) as error:
                raise ThaiToolError(f"{path}:{line}: invalid numeric field") from error
            glyphs.append(glyph)
    return glyphs


def registry_errors(glyphs: list[Glyph]) -> list[str]:
    errors: list[str] = []
    seen_ids: dict[int, Glyph] = {}
    seen_tokens: dict[str, Glyph] = {}
    seen_displays: dict[str, Glyph] = {}
    for glyph in glyphs:
        label = f"0x{glyph.glyph_id:03X}/{glyph.token or '<no token>'}"
        if not 0 <= glyph.glyph_id <= MAX_GLYPH_ID:
            errors.append(f"{label}: glyph ID outside 0x000..0x1FF")
        if not re.fullmatch(r"[A-Z][A-Z0-9_]*", glyph.token):
            errors.append(f"{label}: invalid or empty token")
        if not glyph.display:
            errors.append(f"{label}: empty display sequence")
        if glyph.kind not in VALID_TYPES:
            errors.append(f"{label}: invalid type {glyph.kind!r}")
        if glyph.status not in VALID_STATUSES:
            errors.append(f"{label}: invalid status {glyph.status!r}")
        if not 1 <= glyph.width <= CELL_SIZE:
            errors.append(f"{label}: width must be 1..16")
        if glyph.glyph_id in seen_ids:
            errors.append(f"duplicate glyph ID 0x{glyph.glyph_id:03X}")
        if glyph.token in seen_tokens:
            errors.append(f"duplicate token {glyph.token}")
        if glyph.display in seen_displays:
            errors.append(f"duplicate display sequence {glyph.display!r}")
        seen_ids[glyph.glyph_id] = glyph
        seen_tokens[glyph.token] = glyph
        seen_displays[glyph.display] = glyph
    if glyphs != sorted(glyphs, key=lambda item: item.glyph_id):
        errors.append("registry rows must be sorted by glyph_id")
    return errors


def open_indexed(path: Path) -> Image.Image:
    try:
        image = Image.open(path)
        image.load()
    except OSError as error:
        raise ThaiToolError(f"cannot read image {path}: {error}") from error
    if image.mode != "P":
        raise ThaiToolError(f"{path}: expected indexed mode P, got {image.mode}")
    return image


def tile_box(glyph_id: int) -> tuple[int, int, int, int]:
    x = (glyph_id % MASTER_COLUMNS) * CELL_SIZE
    y = (glyph_id // MASTER_COLUMNS) * CELL_SIZE
    return x, y, x + CELL_SIZE, y + CELL_SIZE


def read_widths(text: str) -> tuple[list[int], re.Match[str]]:
    match = WIDTH_ARRAY_RE.search(text)
    if not match:
        raise ThaiToolError("could not locate gFontNormalLatinGlyphWidths[]")
    widths = [int(value) for value in re.findall(r"\b\d+\b", match.group(2))]
    if len(widths) != 512:
        raise ThaiToolError(f"expected 512 font widths, found {len(widths)}")
    return widths, match


def format_widths(widths: list[int]) -> str:
    lines = []
    for start in range(0, len(widths), 16):
        lines.append("    " + ", ".join(f"{value:2d}" for value in widths[start:start + 16]) + ",")
    return "\n".join(lines)


def renderer_errors(root: Path = ROOT) -> list[str]:
    errors = []
    for relative in ("src/text.c", "include/text.h"):
        text = (root / relative).read_text(encoding="utf-8")
        for marker in RENDERER_FORBIDDEN:
            if marker.lower() in text.lower():
                errors.append(f"{relative}: forbidden renderer marker {marker!r}")
    return errors


def palette_signature(image: Image.Image) -> tuple[int, ...]:
    palette = image.getpalette()
    if palette is None:
        raise ThaiToolError("indexed image has no palette")
    return tuple(palette)
