from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import argparse
import re
import shutil

from PIL import Image


PROJECT_ROOT = Path(__file__).resolve().parents[2]

CHARMAP_PATH = PROJECT_ROOT / "charmap.txt"
FONTS_C_PATH = PROJECT_ROOT / "src/fonts.c"
STRINGS_C_PATH = PROJECT_ROOT / "src/strings.c"

BASE_FONT_PATH = PROJECT_ROOT / "graphics/fonts/latin_normal.png"
GLYPH_DIR = PROJECT_ROOT / "graphics/fonts/thai/glyphs"

BATCH_DIR = PROJECT_ROOT / "tools/thai/generated/consonant_batch"
MANIFEST_PATH = BATCH_DIR / "manifest.txt"

GLYPH_SIZE = 16


@dataclass(frozen=True)
class ManifestEntry:
    character: str
    glyph_id: int
    byte_value: int
    width: int
    source_path: Path


def parse_manifest() -> list[ManifestEntry]:
    if not MANIFEST_PATH.exists():
        raise SystemExit(
            f"ไม่พบ Manifest: {MANIFEST_PATH}\n"
            "ให้รัน preview_consonant_batch.py ก่อน"
        )

    entries: list[ManifestEntry] = []

    lines = MANIFEST_PATH.read_text(
        encoding="utf-8"
    ).splitlines()

    for line_number, raw_line in enumerate(
        lines,
        start=1,
    ):
        line = raw_line.strip()

        if not line or line.startswith("#"):
            continue

        parts = line.split("\t")

        if len(parts) < 6:
            raise SystemExit(
                "รูปแบบ Manifest ไม่ถูกต้องที่บรรทัด "
                f"{line_number}: {raw_line}"
            )

        character = parts[0]
        glyph_id = int(parts[1], 16)

        byte_match = re.fullmatch(
            r"F9 ([0-9A-Fa-f]{2})",
            parts[2],
        )

        if byte_match is None:
            raise SystemExit(
                "ค่า Mapping ไม่ถูกต้องที่บรรทัด "
                f"{line_number}: {parts[2]}"
            )

        width_match = re.fullmatch(
            r"width=(\d+)",
            parts[3],
        )

        if width_match is None:
            raise SystemExit(
                "ค่า Width ไม่ถูกต้องที่บรรทัด "
                f"{line_number}: {parts[3]}"
            )

        source_path = PROJECT_ROOT / parts[5]

        entries.append(
            ManifestEntry(
                character=character,
                glyph_id=glyph_id,
                byte_value=int(
                    byte_match.group(1),
                    16,
                ),
                width=int(
                    width_match.group(1)
                ),
                source_path=source_path,
            )
        )

    if not entries:
        raise SystemExit(
            "Manifest ไม่มีรายการ Glyph"
        )

    return entries


def validate_entries(
    entries: list[ManifestEntry],
) -> None:
    seen_characters: set[str] = set()
    seen_glyph_ids: set[int] = set()
    seen_bytes: set[int] = set()

    for entry in entries:
        if len(entry.character) != 1:
            raise SystemExit(
                f"ตัวอักษรไม่ถูกต้อง: {entry.character!r}"
            )

        if entry.character in seen_characters:
            raise SystemExit(
                f"พบตัวอักษรซ้ำ: {entry.character}"
            )

        if entry.glyph_id in seen_glyph_ids:
            raise SystemExit(
                f"พบ Glyph ID ซ้ำ: 0x{entry.glyph_id:03X}"
            )

        if entry.byte_value in seen_bytes:
            raise SystemExit(
                "พบ Mapping byte ซ้ำ: "
                f"F9 {entry.byte_value:02X}"
            )

        if not 1 <= entry.width <= 16:
            raise SystemExit(
                f"Width ของ {entry.character} "
                f"ไม่ถูกต้อง: {entry.width}"
            )

        if not entry.source_path.exists():
            raise SystemExit(
                f"ไม่พบ Glyph source: {entry.source_path}"
            )

        image = Image.open(
            entry.source_path
        )

        if image.mode != "P":
            raise SystemExit(
                f"{entry.source_path} ต้องเป็นโหมด P "
                f"แต่พบ {image.mode}"
            )

        if image.size != (
            GLYPH_SIZE,
            GLYPH_SIZE,
        ):
            raise SystemExit(
                f"{entry.source_path} ต้องมีขนาด "
                f"{GLYPH_SIZE}x{GLYPH_SIZE} "
                f"แต่พบ {image.size}"
            )

        seen_characters.add(
            entry.character
        )

        seen_glyph_ids.add(
            entry.glyph_id
        )

        seen_bytes.add(
            entry.byte_value
        )


def update_charmap(
    text: str,
    entries: list[ManifestEntry],
) -> str:
    result = text

    for entry in entries:
        mapping_line = (
            f"'{entry.character}' = "
            f"F9 {entry.byte_value:02X}"
        )

        pattern = re.compile(
            rf"^'{re.escape(entry.character)}'"
            rf"\s*=\s*F9\s+[0-9A-Fa-f]{{2}}\s*$",
            re.MULTILINE,
        )

        match = pattern.search(result)

        if match is not None:
            result = (
                result[:match.start()]
                + mapping_line
                + result[match.end():]
            )
        else:
            if not result.endswith("\n"):
                result += "\n"

            result += mapping_line + "\n"

    return result


def update_width_table(
    text: str,
    entries: list[ManifestEntry],
) -> str:
    match = re.search(
        r"(gFontNormalLatinGlyphWidths"
        r"\[\]\s*=\s*\{)"
        r"(.*?)"
        r"(\};)",
        text,
        re.S,
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

    for entry in entries:
        if entry.glyph_id >= len(widths):
            raise SystemExit(
                f"Glyph 0x{entry.glyph_id:03X} "
                f"อยู่นอกตาราง Width"
            )

        widths[entry.glyph_id] = (
            entry.width
        )

    lines: list[str] = []

    for index in range(
        0,
        len(widths),
        16,
    ):
        chunk = widths[
            index:index + 16
        ]

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


def copy_glyphs(
    entries: list[ManifestEntry],
) -> list[Path]:
    GLYPH_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    destinations: list[Path] = []

    for entry in entries:
        destination = (
            GLYPH_DIR
            / entry.source_path.name
        )

        shutil.copy2(
            entry.source_path,
            destination,
        )

        destinations.append(
            destination
        )

    return destinations


def build_font_sheet(
    entries: list[ManifestEntry],
) -> None:
    if not BASE_FONT_PATH.exists():
        raise SystemExit(
            f"ไม่พบ Font Sheet: {BASE_FONT_PATH}"
        )

    font_sheet = Image.open(
        BASE_FONT_PATH
    )

    if font_sheet.mode != "P":
        raise SystemExit(
            "Font Sheet ต้องเป็นโหมด P "
            f"แต่พบ {font_sheet.mode}"
        )

    columns = (
        font_sheet.width
        // GLYPH_SIZE
    )

    rows = (
        font_sheet.height
        // GLYPH_SIZE
    )

    total_glyphs = (
        columns * rows
    )

    for entry in entries:
        if entry.glyph_id >= total_glyphs:
            raise SystemExit(
                f"Glyph 0x{entry.glyph_id:03X} "
                "อยู่นอก Font Sheet"
            )

        glyph_path = (
            GLYPH_DIR
            / entry.source_path.name
        )

        glyph = Image.open(
            glyph_path
        )

        column = (
            entry.glyph_id
            % columns
        )

        row = (
            entry.glyph_id
            // columns
        )

        font_sheet.paste(
            glyph,
            (
                column * GLYPH_SIZE,
                row * GLYPH_SIZE,
            ),
        )

    font_sheet.save(
        BASE_FONT_PATH
    )


def update_test_string(
    text: str,
    entries: list[ManifestEntry],
) -> str:
    """
    ใช้พยัญชนะเพียง 6 ตัวแรกเป็นข้อความทดสอบ
    เพื่อไม่ให้ยาวเกินหน้าเมนู
    """
    test_text = "".join(
        entry.character
        for entry in entries[:6]
    )

    pattern = re.compile(
        r"const u8 "
        r"gText_MainMenuNewGame"
        r"\[\]\s*=\s*"
        r'_\(".*?"\);'
    )

    replacement = (
        "const u8 "
        "gText_MainMenuNewGame[] = "
        f'_("'
        f"{test_text}"
        f'");'
    )

    if pattern.search(text) is None:
        raise SystemExit(
            "ไม่พบ gText_MainMenuNewGame "
            "ใน src/strings.c"
        )

    return pattern.sub(
        replacement,
        text,
        count=1,
    )


def print_plan(
    entries: list[ManifestEntry],
) -> None:
    print(
        "=== Consonant Batch Install Plan ==="
    )

    print(
        f"Manifest       : {MANIFEST_PATH}"
    )

    print(
        f"Characters     : {len(entries)}"
    )

    print(
        "First Glyph ID : "
        f"0x{entries[0].glyph_id:03X}"
    )

    print(
        "Last Glyph ID  : "
        f"0x{entries[-1].glyph_id:03X}"
    )

    print("\nรายการ:")

    for entry in entries:
        print(
            f"{entry.character} "
            f"→ 0x{entry.glyph_id:03X} "
            f"→ F9 {entry.byte_value:02X} "
            f"→ width {entry.width}"
        )

    print("\nข้อความทดสอบ:")

    print(
        "".join(
            entry.character
            for entry in entries[:6]
        )
    )

    print("\nไฟล์ที่จะถูกแก้:")

    print(
        "- charmap.txt"
    )

    print(
        "- src/fonts.c"
    )

    print(
        "- src/strings.c"
    )

    print(
        "- graphics/fonts/latin_normal.png"
    )

    print(
        "- graphics/fonts/thai/glyphs/"
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "ติดตั้งพยัญชนะไทย "
            "จาก Batch Preview"
        )
    )

    mode = (
        parser.add_mutually_exclusive_group(
            required=True
        )
    )

    mode.add_argument(
        "--dry-run",
        action="store_true",
        help=(
            "ตรวจรายการเท่านั้น "
            "ไม่แก้ไฟล์"
        ),
    )

    mode.add_argument(
        "--apply",
        action="store_true",
        help=(
            "ติดตั้ง Glyph, Mapping, "
            "Width และข้อความทดสอบ"
        ),
    )

    args = parser.parse_args()

    entries = parse_manifest()

    validate_entries(
        entries
    )

    print_plan(
        entries
    )

    if args.dry_run:
        print(
            "\nDRY RUN: "
            "ไม่มีไฟล์ใดถูกแก้ไข"
        )
        return

    charmap_text = (
        CHARMAP_PATH.read_text(
            encoding="utf-8"
        )
    )

    fonts_c_text = (
        FONTS_C_PATH.read_text(
            encoding="utf-8"
        )
    )

    strings_c_text = (
        STRINGS_C_PATH.read_text(
            encoding="utf-8"
        )
    )

    updated_charmap = (
        update_charmap(
            charmap_text,
            entries,
        )
    )

    updated_fonts_c = (
        update_width_table(
            fonts_c_text,
            entries,
        )
    )

    updated_strings_c = (
        update_test_string(
            strings_c_text,
            entries,
        )
    )

    copied_files = copy_glyphs(
        entries
    )

    build_font_sheet(
        entries
    )

    CHARMAP_PATH.write_text(
        updated_charmap,
        encoding="utf-8",
    )

    FONTS_C_PATH.write_text(
        updated_fonts_c,
        encoding="utf-8",
    )

    STRINGS_C_PATH.write_text(
        updated_strings_c,
        encoding="utf-8",
    )

    print(
        "\n=== Batch Installation Completed ==="
    )

    print(
        f"Glyphs copied : {len(copied_files)}"
    )

    print(
        "Charmap       : updated"
    )

    print(
        "Width table   : updated"
    )

    print(
        "Font sheet    : updated"
    )

    print(
        "Test string   : updated"
    )

    print(
        "\nยังไม่ได้ Commit หรือ Push"
    )


if __name__ == "__main__":
    main()