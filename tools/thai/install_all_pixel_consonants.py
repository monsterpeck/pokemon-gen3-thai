from __future__ import annotations

import argparse
import re
import shutil
from dataclasses import dataclass
from pathlib import Path

from PIL import Image


PROJECT_ROOT = Path(__file__).resolve().parents[2]

MANIFEST_PATH = (
    PROJECT_ROOT
    / "tools/thai/generated/pixel_consonants_game/manifest.txt"
)

SOURCE_GLYPH_DIR = (
    PROJECT_ROOT
    / "tools/thai/generated/pixel_consonants_game/glyphs"
)

DESTINATION_GLYPH_DIR = (
    PROJECT_ROOT
    / "graphics/fonts/thai/glyphs"
)

CHARMAP_PATH = PROJECT_ROOT / "charmap.txt"
FONTS_C_PATH = PROJECT_ROOT / "src/fonts.c"
STRINGS_C_PATH = PROJECT_ROOT / "src/strings.c"

FONT_SHEET_PATH = (
    PROJECT_ROOT
    / "graphics/fonts/latin_normal.png"
)

GLYPH_SIZE = 16
TEST_TEXT = "กขคงจฉ"


@dataclass(frozen=True)
class GlyphEntry:
    character: str
    name: str
    glyph_id: int
    mapping: str
    width: int
    filename: str


def parse_manifest() -> list[GlyphEntry]:
    if not MANIFEST_PATH.exists():
        raise SystemExit(
            f"ไม่พบ Manifest: {MANIFEST_PATH}"
        )

    entries: list[GlyphEntry] = []

    for line_number, raw_line in enumerate(
        MANIFEST_PATH.read_text(
            encoding="utf-8"
        ).splitlines(),
        start=1,
    ):
        line = raw_line.strip()

        if not line or line.startswith("#"):
            continue

        parts = line.split("\t")

        if len(parts) != 6:
            raise SystemExit(
                f"Manifest ผิดรูปแบบบรรทัด {line_number}: "
                f"{raw_line}"
            )

        entries.append(
            GlyphEntry(
                character=parts[0],
                name=parts[1],
                glyph_id=int(parts[2], 16),
                mapping=parts[3],
                width=int(parts[4]),
                filename=parts[5],
            )
        )

    if len(entries) != 42:
        raise SystemExit(
            f"ควรมี 42 Glyph แต่พบ {len(entries)}"
        )

    return entries


def validate_entries(
    entries: list[GlyphEntry],
) -> None:
    character_set: set[str] = set()
    glyph_id_set: set[int] = set()
    mapping_set: set[str] = set()

    for entry in entries:
        if entry.character in character_set:
            raise SystemExit(
                f"ตัวอักษรซ้ำ: {entry.character}"
            )

        if entry.glyph_id in glyph_id_set:
            raise SystemExit(
                f"Glyph ID ซ้ำ: 0x{entry.glyph_id:03X}"
            )

        normalized_mapping = entry.mapping.upper()

        if normalized_mapping in mapping_set:
            raise SystemExit(
                f"Mapping ซ้ำ: {entry.mapping}"
            )

        if not 1 <= entry.width <= 16:
            raise SystemExit(
                f"Width ของ {entry.character} "
                f"ไม่ถูกต้อง: {entry.width}"
            )

        source_path = (
            SOURCE_GLYPH_DIR / entry.filename
        )

        if not source_path.exists():
            raise SystemExit(
                f"ไม่พบ Glyph: {source_path}"
            )

        with Image.open(source_path) as image:
            if image.size != (
                GLYPH_SIZE,
                GLYPH_SIZE,
            ):
                raise SystemExit(
                    f"{entry.filename} ไม่ใช่ 16x16"
                )

            if image.mode != "P":
                raise SystemExit(
                    f"{entry.filename} ต้องเป็นโหมด P "
                    f"แต่พบ {image.mode}"
                )

        character_set.add(entry.character)
        glyph_id_set.add(entry.glyph_id)
        mapping_set.add(normalized_mapping)


def update_charmap(
    text: str,
    entries: list[GlyphEntry],
) -> str:
    result = text

    for entry in entries:
        replacement = (
            f"'{entry.character}' = {entry.mapping}"
        )

        pattern = re.compile(
            rf"^'{re.escape(entry.character)}'"
            rf"\s*=\s*(?:[0-9A-Fa-f]{{2}}\s*)+$",
            re.MULTILINE,
        )

        if pattern.search(result):
            result = pattern.sub(
                replacement,
                result,
                count=1,
            )
        else:
            if not result.endswith("\n"):
                result += "\n"

            result += replacement + "\n"

    return result


def update_width_table(
    text: str,
    entries: list[GlyphEntry],
) -> str:
    match = re.search(
        r"(gFontNormalLatinGlyphWidths"
        r"\[\]\s*=\s*\{)"
        r"(.*?)"
        r"(\};)",
        text,
        re.DOTALL,
    )

    if match is None:
        raise SystemExit(
            "ไม่พบ gFontNormalLatinGlyphWidths[]"
        )

    widths = [
        int(value)
        for value in re.findall(
            r"\d+",
            match.group(2),
        )
    ]

    for entry in entries:
        if entry.glyph_id >= len(widths):
            raise SystemExit(
                f"Glyph 0x{entry.glyph_id:03X} "
                "อยู่นอก Width Table"
            )

        widths[entry.glyph_id] = entry.width

    lines: list[str] = []

    for index in range(
        0,
        len(widths),
        16,
    ):
        chunk = widths[index:index + 16]

        lines.append(
            "    "
            + ", ".join(
                f"{value:2d}"
                for value in chunk
            )
            + ","
        )

    replacement = (
        match.group(1)
        + "\n"
        + "\n".join(lines)
        + "\n"
        + match.group(3)
    )

    return (
        text[:match.start()]
        + replacement
        + text[match.end():]
    )


def update_test_string(
    text: str,
) -> str:
    pattern = re.compile(
        r'const u8 gText_MainMenuNewGame'
        r'\[\]\s*=\s*_\(".*?"\);'
    )

    replacement = (
        "const u8 gText_MainMenuNewGame[] = "
        f'_("'
        f"{TEST_TEXT}"
        f'");'
    )

    updated_text, count = pattern.subn(
        replacement,
        text,
        count=1,
    )

    if count != 1:
        raise SystemExit(
            "ไม่พบ gText_MainMenuNewGame"
        )

    return updated_text


def build_updated_font_sheet(
    entries: list[GlyphEntry],
) -> Image.Image:
    if not FONT_SHEET_PATH.exists():
        raise SystemExit(
            f"ไม่พบ Font Sheet: {FONT_SHEET_PATH}"
        )

    with Image.open(FONT_SHEET_PATH) as opened:
        font_sheet = opened.copy()

    if font_sheet.mode != "P":
        raise SystemExit(
            "latin_normal.png ต้องเป็นโหมด P"
        )

    columns = font_sheet.width // GLYPH_SIZE
    rows = font_sheet.height // GLYPH_SIZE
    total_glyphs = columns * rows

    for entry in entries:
        if entry.glyph_id >= total_glyphs:
            raise SystemExit(
                f"Glyph 0x{entry.glyph_id:03X} "
                "อยู่นอก Font Sheet"
            )

        source_path = (
            SOURCE_GLYPH_DIR / entry.filename
        )

        with Image.open(source_path) as opened:
            glyph = opened.copy()

        column = entry.glyph_id % columns
        row = entry.glyph_id // columns

        font_sheet.paste(
            glyph,
            (
                column * GLYPH_SIZE,
                row * GLYPH_SIZE,
            ),
        )

    return font_sheet


def copy_glyphs(
    entries: list[GlyphEntry],
) -> None:
    DESTINATION_GLYPH_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    for entry in entries:
        source_path = (
            SOURCE_GLYPH_DIR / entry.filename
        )

        destination_path = (
            DESTINATION_GLYPH_DIR
            / entry.filename
        )

        shutil.copy2(
            source_path,
            destination_path,
        )


def print_plan(
    entries: list[GlyphEntry],
) -> None:
    print(
        "=== All Pixel Consonants Install Plan ==="
    )
    print(f"Characters  : {len(entries)}")
    print(
        f"First Glyph : 0x{entries[0].glyph_id:03X}"
    )
    print(
        "Highest ID  : "
        f"0x{max(entry.glyph_id for entry in entries):03X}"
    )
    print(f"Test text   : {TEST_TEXT}")
    print("")

    for entry in entries:
        print(
            f"{entry.character} "
            f"→ 0x{entry.glyph_id:03X} "
            f"→ {entry.mapping} "
            f"→ width {entry.width}"
        )

    print("")
    print("ไฟล์ที่จะถูกแก้:")
    print("- charmap.txt")
    print("- src/fonts.c")
    print("- src/strings.c")
    print("- graphics/fonts/latin_normal.png")
    print("- graphics/fonts/thai/glyphs/")


def main() -> None:
    parser = argparse.ArgumentParser()

    mode = parser.add_mutually_exclusive_group(
        required=True
    )

    mode.add_argument(
        "--dry-run",
        action="store_true",
    )

    mode.add_argument(
        "--apply",
        action="store_true",
    )

    args = parser.parse_args()

    entries = parse_manifest()
    validate_entries(entries)
    print_plan(entries)

    if args.dry_run:
        print("")
        print("DRY RUN: ไม่มีไฟล์ใดถูกแก้ไข")
        return

    charmap_text = CHARMAP_PATH.read_text(
        encoding="utf-8"
    )

    fonts_text = FONTS_C_PATH.read_text(
        encoding="utf-8"
    )

    strings_text = STRINGS_C_PATH.read_text(
        encoding="utf-8"
    )

    updated_charmap = update_charmap(
        charmap_text,
        entries,
    )

    updated_fonts = update_width_table(
        fonts_text,
        entries,
    )

    updated_strings = update_test_string(
        strings_text
    )

    updated_font_sheet = build_updated_font_sheet(
        entries
    )

    copy_glyphs(entries)

    CHARMAP_PATH.write_text(
        updated_charmap,
        encoding="utf-8",
    )

    FONTS_C_PATH.write_text(
        updated_fonts,
        encoding="utf-8",
    )

    STRINGS_C_PATH.write_text(
        updated_strings,
        encoding="utf-8",
    )

    updated_font_sheet.save(
        FONT_SHEET_PATH
    )

    print("")
    print("=== All Pixel Consonants Installed ===")
    print(f"Glyphs installed : {len(entries)}")
    print("Charmap          : updated")
    print("Width table      : updated")
    print("Font sheet       : updated")
    print(f"Test string      : {TEST_TEXT}")
    print("")
    print("ยังไม่ได้ Commit หรือ Push")


if __name__ == "__main__":
    main()
