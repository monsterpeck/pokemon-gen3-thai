from collections import Counter
from pathlib import Path
import argparse

from PIL import Image


GLYPH_SIZE = 16
DEFAULT_FONT_PATH = Path("graphics/fonts/latin_normal.png")


def parse_hex(value: str) -> int:
    cleaned = value.strip().lower()

    if cleaned.startswith("0x"):
        cleaned = cleaned[2:]

    try:
        return int(cleaned, 16)
    except ValueError as error:
        raise argparse.ArgumentTypeError(
            f"Glyph ID '{value}' ไม่ใช่เลขฐานสิบหกที่ถูกต้อง"
        ) from error


def main() -> None:
    parser = argparse.ArgumentParser(
        description="วิเคราะห์ Palette index ของ Glyph ขนาด 16x16"
    )

    parser.add_argument(
        "glyph_id",
        type=parse_hex,
        help="Glyph ID ฐานสิบหก เช่น BB หรือ 118",
    )

    parser.add_argument(
        "--font",
        type=Path,
        default=DEFAULT_FONT_PATH,
        help=f"Font Sheet (default: {DEFAULT_FONT_PATH})",
    )

    args = parser.parse_args()

    if not args.font.exists():
        raise SystemExit(f"ไม่พบไฟล์: {args.font}")

    image = Image.open(args.font)

    if image.mode != "P":
        raise SystemExit(
            f"Font Sheet ต้องเป็นโหมด P แต่พบโหมด {image.mode}"
        )

    if image.width % GLYPH_SIZE != 0:
        raise SystemExit(
            f"ความกว้าง {image.width} หารด้วย {GLYPH_SIZE} ไม่ลงตัว"
        )

    if image.height % GLYPH_SIZE != 0:
        raise SystemExit(
            f"ความสูง {image.height} หารด้วย {GLYPH_SIZE} ไม่ลงตัว"
        )

    columns = image.width // GLYPH_SIZE
    rows = image.height // GLYPH_SIZE
    total_glyphs = columns * rows

    glyph_id = args.glyph_id

    if not 0 <= glyph_id < total_glyphs:
        raise SystemExit(
            f"Glyph 0x{glyph_id:03X} อยู่นอกช่วง "
            f"0x000-0x{total_glyphs - 1:03X}"
        )

    column = glyph_id % columns
    row = glyph_id // columns

    left = column * GLYPH_SIZE
    top = row * GLYPH_SIZE

    glyph = image.crop(
        (
            left,
            top,
            left + GLYPH_SIZE,
            top + GLYPH_SIZE,
        )
    )

    counts = Counter(glyph.getdata())

    print("=== Glyph Palette Analysis ===")
    print(f"Font       : {args.font}")
    print(f"Glyph ID   : 0x{glyph_id:03X}")
    print(f"Column     : {column}")
    print(f"Row        : {row}")
    print(f"Total px   : {GLYPH_SIZE * GLYPH_SIZE}")

    print("\nPalette index counts:")

    for palette_index in sorted(counts):
        print(
            f"Index {palette_index:3d} : "
            f"{counts[palette_index]:3d} pixels"
        )

    print("\nPixel grid:")
    print("    " + " ".join(f"{x:X}" for x in range(GLYPH_SIZE)))

    for y in range(GLYPH_SIZE):
        values = []

        for x in range(GLYPH_SIZE):
            palette_index = glyph.getpixel((x, y))
            values.append(f"{palette_index:X}")

        print(f"{y:02X}  " + " ".join(values))


if __name__ == "__main__":
    main()