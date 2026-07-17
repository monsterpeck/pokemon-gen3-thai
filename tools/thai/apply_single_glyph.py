from pathlib import Path
from PIL import Image

BASE_FONT_PATH = Path("graphics/fonts/latin_normal.png")
GLYPH_PATH = Path("graphics/fonts/thai/glyphs/0136_mo_ma.png")

GLYPH_ID = 0x136
GLYPH_SIZE = 16


def main() -> None:
    if not BASE_FONT_PATH.exists():
        raise SystemExit(f"ไม่พบไฟล์: {BASE_FONT_PATH}")

    if not GLYPH_PATH.exists():
        raise SystemExit(f"ไม่พบไฟล์: {GLYPH_PATH}")

    font_sheet = Image.open(BASE_FONT_PATH)
    glyph = Image.open(GLYPH_PATH)

    if glyph.size != (GLYPH_SIZE, GLYPH_SIZE):
        raise SystemExit(
            f"ขนาด glyph ไม่ถูกต้อง: {glyph.size} (ต้องเป็น 16x16)"
        )

    columns = font_sheet.width // GLYPH_SIZE

    x = (GLYPH_ID % columns) * GLYPH_SIZE
    y = (GLYPH_ID // columns) * GLYPH_SIZE

    font_sheet.paste(glyph, (x, y))
    font_sheet.save(BASE_FONT_PATH)

    print("=== Single Glyph Applied ===")
    print(f"Glyph ID : 0x{GLYPH_ID:03X}")
    print(f"Source   : {GLYPH_PATH}")
    print(f"Target   : {BASE_FONT_PATH}")
    print(f"Position : X={x}, Y={y}")


if __name__ == "__main__":
    main()