from __future__ import annotations

import argparse
import re
import shutil
from dataclasses import dataclass
from pathlib import Path

from PIL import Image


PROJECT_ROOT = Path(__file__).resolve().parents[2]

CHARMAP_PATH = PROJECT_ROOT / "charmap.txt"
FONTS_C_PATH = PROJECT_ROOT / "src/fonts.c"
STRINGS_C_PATH = PROJECT_ROOT / "src/strings.c"
FONT_SHEET_PATH = PROJECT_ROOT / "graphics/fonts/latin_normal.png"

SOURCE_DIR = (
    PROJECT_ROOT
    / "tools/thai/generated/pixel_font_game_preview/glyphs"
)

DESTINATION_DIR = (
    PROJECT_ROOT
    / "graphics/fonts/thai/glyphs"
)

GLYPH_SIZE = 16


@dataclass(frozen=True)
class GlyphEntry:
    character: str
    glyph_id: int
    mapping: str
    width: int
    source_filename: str
    destination_filename: str


GLYPHS = [
    GlyphEntry(
        character="ก",
        glyph_id=0x118,
        mapping="F9 18",
        width=13,
        source_filename="118_ko_kai.png",
        destination_filename="0118_ko_kai.png",
    ),
    GlyphEntry(
        character="ข",
        glyph_id=0x119,
        mapping="F9 19",
        width=13,
        source_filename="119_kho_khai.png",
        destination_filename="0119_kho_khai.png",
    ),
    GlyphEntry(
        character="ค",
        glyph_id=0x11A,
        mapping="F9 1A",
        width=13,
        source_filename="11a_kho_khwai.png",
        destination_filename="011a_kho_khwai.png",
    ),
    GlyphEntry(
        character="ง",
        glyph_id=0x11B,
        mapping="F9 1B",
        width=12,
        source_filename="11b_ngo_ngu.png",
        destination_filename="011b_ngo_ngu.png",
    ),
    GlyphEntry(
        character="จ",
        glyph_id=0x11D,
        mapping="F9 1D",
        width=13,
        source_filename="11d_cho_chan.png",
        destination_filename="011d_cho_chan.png",
    ),
    GlyphEntry(
        character="ฉ",
        glyph_id=0x11E,
        mapping="F9 1E",
        width=14,
        source_filename="11e_cho_ching.png",
        destination_filename="011e_cho_ching.png",
    ),
]


def validate_files() -> None:
    required_paths = [
        CHARMAP_PATH,
        FONTS_C_PATH,
        STRINGS_C_PATH,
        FONT_SHEET_PATH,
    ]

    for path in required_paths:
        if not path.exists():
            raise SystemExit(f"ไม่พบไฟล์: {path}")

    for entry in GLYPHS:
        source_path = SOURCE_DIR / entry.source_filename

        if not source_path.exists():
            raise SystemExit(
                f"ไม่พบ Glyph: {source_path}"
            )

        with Image.open(source_path) as image:
            if image.size != (GLYPH_SIZE, GLYPH_SIZE):
                raise SystemExit(
                    f"{source_path.name} ต้องมีขนาด 16x16 "
                    f"แต่พบ {image.width}x{image.height}"
                )

            if image.mode != "P":
                raise SystemExit(
                    f"{source_path.name} ต้องเป็นโหมด P "
                    f"แต่พบ {image.mode}"
                )


def validate_charmap() -> None:
    text = CHARMAP_PATH.read_text(
        encoding="utf-8"
    )

    for entry in GLYPHS:
        pattern = re.compile(
            rf"^'{re.escape(entry.character)}'"
            rf"\s*=\s*{re.escape(entry.mapping)}\s*$",
            re.MULTILINE | re.IGNORECASE,
        )

        if pattern.search(text) is None:
            raise SystemExit(
                f"ไม่พบ Mapping ที่ถูกต้องของ "
                f"{entry.character}: {entry.mapping}"
            )


def update_width_table(text: str) -> str:
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
            "ไม่พบ gFontNormalLatinGlyphWidths[] "
            "ใน src/fonts.c"
        )

    widths = [
        int(value)
        for value in re.findall(
            r"\d+",
            match.group(2),
        )
    ]

    for entry in GLYPHS:
        if entry.glyph_id >= len(widths):
            raise SystemExit(
                f"Glyph 0x{entry.glyph_id:03X} "
                "อยู่นอก Width Table"
            )

        widths[entry.glyph_id] = entry.width

    formatted_lines: list[str] = []

    for index in range(0, len(widths), 16):
        chunk = widths[index:index + 16]

        formatted_lines.append(
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
        + "\n".join(formatted_lines)
        + "\n"
        + match.group(3)
    )

    return (
        text[:match.start()]
        + replacement
        + text[match.end():]
    )


def update_test_string(text: str) -> str:
    pattern = re.compile(
        r'const u8 gText_MainMenuNewGame'
        r'\[\]\s*=\s*_\(".*?"\);'
    )

    replacement = (
        'const u8 gText_MainMenuNewGame[] = '
        '_("กขคงจฉ");'
    )

    updated_text, count = pattern.subn(
        replacement,
        text,
        count=1,
    )

    if count != 1:
        raise SystemExit(
            "ไม่พบ gText_MainMenuNewGame "
            "ใน src/strings.c"
        )

    return updated_text


def install_font_sheet() -> None:
    with Image.open(FONT_SHEET_PATH) as image:
        font_sheet = image.copy()

    if font_sheet.mode != "P":
        raise SystemExit(
            "latin_normal.png ต้องเป็นโหมด P "
            f"แต่พบ {font_sheet.mode}"
        )

    columns = font_sheet.width // GLYPH_SIZE
    rows = font_sheet.height // GLYPH_SIZE
    total_glyphs = columns * rows

    for entry in GLYPHS:
        if entry.glyph_id >= total_glyphs:
            raise SystemExit(
                f"Glyph 0x{entry.glyph_id:03X} "
                "อยู่นอก Font Sheet"
            )

        source_path = SOURCE_DIR / entry.source_filename

        with Image.open(source_path) as image:
            glyph = image.copy()

        column = entry.glyph_id % columns
        row = entry.glyph_id // columns

        font_sheet.paste(
            glyph,
            (
                column * GLYPH_SIZE,
                row * GLYPH_SIZE,
            ),
        )

    font_sheet.save(FONT_SHEET_PATH)


def copy_glyph_files() -> None:
    DESTINATION_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    for entry in GLYPHS:
        source_path = SOURCE_DIR / entry.source_filename
        destination_path = (
            DESTINATION_DIR
            / entry.destination_filename
        )

        shutil.copy2(
            source_path,
            destination_path,
        )


def print_plan() -> None:
    print("=== Pixel Font Test Install Plan ===")
    print("")

    for entry in GLYPHS:
        print(
            f"{entry.character} "
            f"→ glyph 0x{entry.glyph_id:03X} "
            f"→ {entry.mapping} "
            f"→ width {entry.width}"
        )

    print("")
    print("ข้อความทดสอบ: กขคงจฉ")
    print("")
    print("ไฟล์ที่จะถูกแก้:")
    print("- src/fonts.c")
    print("- src/strings.c")
    print("- graphics/fonts/latin_normal.png")
    print("- graphics/fonts/thai/glyphs/")
    print("")
    print("charmap.txt จะถูกตรวจสอบ แต่ไม่ถูกแก้")


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

    validate_files()
    validate_charmap()
    print_plan()

    if args.dry_run:
        print("")
        print("DRY RUN: ไม่มีไฟล์ใดถูกแก้ไข")
        return

    fonts_text = FONTS_C_PATH.read_text(
        encoding="utf-8"
    )

    strings_text = STRINGS_C_PATH.read_text(
        encoding="utf-8"
    )

    updated_fonts = update_width_table(
        fonts_text
    )

    updated_strings = update_test_string(
        strings_text
    )

    copy_glyph_files()
    install_font_sheet()

    FONTS_C_PATH.write_text(
        updated_fonts,
        encoding="utf-8",
    )

    STRINGS_C_PATH.write_text(
        updated_strings,
        encoding="utf-8",
    )

    print("")
    print("=== Pixel Font Test Installed ===")
    print(f"Glyphs installed : {len(GLYPHS)}")
    print("Width table      : updated")
    print("Font sheet       : updated")
    print("Test string      : กขคงจฉ")
    print("")
    print("ยังไม่ได้ Commit หรือ Push")


if __name__ == "__main__":
    main()
