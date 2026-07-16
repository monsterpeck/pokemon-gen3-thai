from pathlib import Path
import re

from PIL import Image


BASE_FONT_PATH = Path("graphics/fonts/latin_normal.png")
GLYPHS_DIR = Path("graphics/fonts/thai/glyphs")
OUTPUT_PATH = Path(
    "tools/thai/generated/latin_normal_thai_preview.png"
)

GLYPH_SIZE = 16

# รูปแบบชื่อไฟล์:
# 0118_ko_kai.png
GLYPH_FILENAME_PATTERN = re.compile(
    r"^([0-9A-Fa-f]{4})_.+\.png$"
)


def read_glyph_id(path: Path) -> int:
    match = GLYPH_FILENAME_PATTERN.match(path.name)

    if match is None:
        raise ValueError(
            f"ชื่อไฟล์ไม่ถูกต้อง: {path.name}\n"
            "รูปแบบที่ถูกต้อง เช่น 0118_ko_kai.png"
        )

    return int(match.group(1), 16)


def main() -> None:
    if not BASE_FONT_PATH.exists():
        raise SystemExit(
            f"ไม่พบ Font Sheet หลัก: {BASE_FONT_PATH}"
        )

    if not GLYPHS_DIR.exists():
        raise SystemExit(
            f"ไม่พบโฟลเดอร์ Glyph: {GLYPHS_DIR}"
        )

    font_sheet = Image.open(BASE_FONT_PATH)

    if font_sheet.mode != "P":
        raise SystemExit(
            f"Font Sheet ต้องเป็นโหมด P แต่พบ {font_sheet.mode}"
        )

    columns = font_sheet.width // GLYPH_SIZE
    rows = font_sheet.height // GLYPH_SIZE
    total_glyphs = columns * rows

    glyph_files = sorted(GLYPHS_DIR.glob("*.png"))

    if not glyph_files:
        raise SystemExit(
            f"ไม่พบไฟล์ PNG ใน {GLYPHS_DIR}"
        )

    imported_count = 0

    print("=== Thai Font Builder ===")
    print(f"Base font    : {BASE_FONT_PATH}")
    print(f"Glyph folder : {GLYPHS_DIR}")
    print(f"Glyph files  : {len(glyph_files)}")
    print()

    for glyph_path in glyph_files:
        try:
            glyph_id = read_glyph_id(glyph_path)
        except ValueError as error:
            raise SystemExit(str(error)) from error

        if glyph_id >= total_glyphs:
            raise SystemExit(
                f"{glyph_path.name}: Glyph ID 0x{glyph_id:03X} "
                f"อยู่นอกช่วง 0x000–0x{total_glyphs - 1:03X}"
            )

        glyph_image = Image.open(glyph_path)

        if glyph_image.size != (GLYPH_SIZE, GLYPH_SIZE):
            raise SystemExit(
                f"{glyph_path.name}: ขนาดต้องเป็น 16x16 "
                f"แต่พบ {glyph_image.width}x{glyph_image.height}"
            )

        if glyph_image.mode != "P":
            raise SystemExit(
                f"{glyph_path.name}: ต้องเป็นโหมด P "
                f"แต่พบ {glyph_image.mode}"
            )

        column = glyph_id % columns
        row = glyph_id // columns

        pixel_x = column * GLYPH_SIZE
        pixel_y = row * GLYPH_SIZE

        font_sheet.paste(
            glyph_image,
            (pixel_x, pixel_y),
        )

        imported_count += 1

        print(
            f"Imported {glyph_path.name} "
            f"→ Glyph 0x{glyph_id:03X} "
            f"at ({pixel_x}, {pixel_y})"
        )

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    font_sheet.save(OUTPUT_PATH)

    print()
    print(f"Imported glyphs : {imported_count}")
    print(f"Output saved    : {OUTPUT_PATH}")
    print("Original latin_normal.png was not modified.")


if __name__ == "__main__":
    main()