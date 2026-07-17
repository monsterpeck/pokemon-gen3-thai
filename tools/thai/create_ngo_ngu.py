from pathlib import Path
from PIL import Image

OUTPUT_PATH = Path("graphics/fonts/thai/glyphs/011B_ngo_ngu.png")
FONT_PATH = Path("graphics/fonts/latin_normal.png")

GLYPH_SIZE = 16

BACKGROUND = 0
FG_DARK = 1
FG_LIGHT = 2
FG_WHITE = 3

def put_pixels(image, coords, color):
    for x, y in coords:
        image.putpixel((x, y), color)

def main():
    font_sheet = Image.open(FONT_PATH)

    image = Image.new("P", (GLYPH_SIZE, GLYPH_SIZE), BACKGROUND)

    palette = font_sheet.getpalette()
    if palette is None:
        raise SystemExit("ไม่พบ palette ใน latin_normal.png")

    image.putpalette(palette)

    # ===== โครงตัว ง =====

    dark_pixels = [
        # ด้านบนซ้าย
        (7, 1), (8, 1), (9, 1),
        (7, 2),
        (7, 3), (8, 3),

        # จุดเว้าด้านบน
        (8, 2),

        # ลำตัวด้านขวา
        (9, 3),
        (9, 4),
        (9, 5),
        (9, 6),
        (9, 7),
        (9, 8),
        (9, 9),
        (9, 10),
        (9, 11),
        (9, 12),

        # หัวซ้ายกลาง
        (6, 4), (7, 4),
        (6, 5), (7, 5), (8, 5),

        # หางซ้ายเฉียงลง
        (3, 6),
        (3, 7), (4, 7),
        (4, 8), (5, 8),
        (5, 9), (6, 9),
        (6, 10), (7, 10),
        (7, 11), (8, 11),
    ]

    light_pixels = [
        # ไฮไลต์บนหัว
        (8, 1), (9, 1), (10, 1),
        (9, 2), (10, 2),

        # ไฮไลต์ด้านขวา
        (10, 3),
        (10, 4),
        (10, 5),
        (10, 6),
        (10, 7),
        (10, 8),
        (10, 9),
        (10, 10),
        (10, 11),
        (10, 12),

        # ไฮไลต์ปลายหาง
        (4, 6),
        (5, 7),
        (6, 8),
        (7, 9),
        (8, 10),
    ]

    white_pixels = [
        # กลางหัว
        (8, 2), (9, 2),

        # เว้าด้านในบน
        (8, 4),

        # ด้านในลำตัว
        (8, 6),
        (8, 7),
        (8, 8),
        (8, 9),
    ]

    put_pixels(image, dark_pixels, FG_DARK)
    put_pixels(image, light_pixels, FG_LIGHT)
    put_pixels(image, white_pixels, FG_WHITE)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    image.save(OUTPUT_PATH)

    print(f"Glyph created : {OUTPUT_PATH}")
    print(f"Size          : {image.width} x {image.height}")
    print(f"Mode          : {image.mode}")

if __name__ == "__main__":
    main()