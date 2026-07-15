from pathlib import Path
import argparse

from PIL import Image


FONT_PATH = Path("graphics/fonts/latin_normal.png")
OUTPUT_DIR = Path("tools/thai")
GLYPH_SIZE = 16
PREVIEW_SCALE = 16


def parse_glyph_id(value: str) -> int:
    """
    รับหมายเลข Glyph ได้หลายรูปแบบ เช่น:
    118
    0x118
    01A
    """
    cleaned = value.strip().lower()

    if cleaned.startswith("0x"):
        cleaned = cleaned[2:]

    try:
        glyph_id = int(cleaned, 16)
    except ValueError as error:
        raise argparse.ArgumentTypeError(
            f"'{value}' ไม่ใช่หมายเลขฐานสิบหกที่ถูกต้อง"
        ) from error

    if not 0 <= glyph_id <= 0x1FF:
        raise argparse.ArgumentTypeError(
            "Glyph ID ต้องอยู่ระหว่าง 0x000 ถึง 0x1FF"
        )

    return glyph_id


def main() -> None:
    parser = argparse.ArgumentParser(
        description="ตรวจสอบตำแหน่ง Glyph ใน latin_normal.png"
    )
    parser.add_argument(
        "glyph_id",
        type=parse_glyph_id,
        help="หมายเลข Glyph ฐานสิบหก เช่น 118 หรือ 0x118",
    )
    args = parser.parse_args()

    image = Image.open(FONT_PATH)
    
    scan_range(image, 0x118, 0x1CF)

    columns = image.width // GLYPH_SIZE
    rows = image.height // GLYPH_SIZE
    total_glyphs = columns * rows

    glyph_id = args.glyph_id

    if glyph_id >= total_glyphs:
        raise SystemExit(
            f"Glyph 0x{glyph_id:03X} อยู่นอก Font Sheet "
            f"ซึ่งมีทั้งหมด {total_glyphs} ช่อง"
        )

    column = glyph_id % columns
    row = glyph_id // columns

    pixel_x = column * GLYPH_SIZE
    pixel_y = row * GLYPH_SIZE

    print("=== Font Information ===")
    print(f"Size     : {image.width} x {image.height}")
    print(f"Mode     : {image.mode}")
    print(f"Columns  : {columns}")
    print(f"Rows     : {rows}")
    print(f"Total    : {total_glyphs}")

    print("\n=== Glyph Location ===")
    print(f"Glyph ID : 0x{glyph_id:03X}")
    print(f"Decimal  : {glyph_id}")
    print(f"Column   : {column}")
    print(f"Row      : {row}")
    print(f"Pixel X  : {pixel_x}")
    print(f"Pixel Y  : {pixel_y}")

    box = (
        pixel_x,
        pixel_y,
        pixel_x + GLYPH_SIZE,
        pixel_y + GLYPH_SIZE,
    )

    glyph_image = image.crop(box)

        # ตรวจว่าสีใดเป็นสีพื้นหลัง โดยใช้พิกเซลมุมซ้ายบนของ Font Sheet
    background_index = image.getpixel((0, 0))

    # ตรวจพิกเซลทุกจุดภายใน Glyph
    glyph_pixels = list(glyph_image.getdata())
    non_background_pixels = sum(
        pixel != background_index for pixel in glyph_pixels
    )

    is_empty = non_background_pixels == 0

    print("\n=== Glyph Content ===")
    print(f"Background index      : {background_index}")
    print(f"Non-background pixels : {non_background_pixels}")
    print(f"Status                : {'EMPTY' if is_empty else 'USED'}")

    preview = glyph_image.resize(
        (
            GLYPH_SIZE * PREVIEW_SCALE,
            GLYPH_SIZE * PREVIEW_SCALE,
        ),
        resample=Image.Resampling.NEAREST,
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    output_path = OUTPUT_DIR / f"glyph_{glyph_id:04X}_preview.png"
    preview.save(output_path)

    print(f"\nPreview saved: {output_path}")

def scan_range(image: Image.Image, start: int, end: int) -> None:
    columns = image.width // GLYPH_SIZE
    background_index = image.getpixel((0, 0))

    empty_glyphs = []
    used_glyphs = []

    for glyph_id in range(start, end + 1):
        column = glyph_id % columns
        row = glyph_id // columns

        pixel_x = column * GLYPH_SIZE
        pixel_y = row * GLYPH_SIZE

        box = (
            pixel_x,
            pixel_y,
            pixel_x + GLYPH_SIZE,
            pixel_y + GLYPH_SIZE,
        )

        glyph_image = image.crop(box)
        pixels = list(glyph_image.getdata())

        non_background_pixels = sum(
            pixel != background_index for pixel in pixels
        )

        if non_background_pixels == 0:
            empty_glyphs.append(glyph_id)
        else:
            used_glyphs.append(glyph_id)

    print("\n=== Glyph Range Scan ===")
    print(f"Range       : 0x{start:03X} - 0x{end:03X}")
    print(f"Total       : {end - start + 1}")
    print(f"Empty       : {len(empty_glyphs)}")
    print(f"Used        : {len(used_glyphs)}")

    print("\nEmpty Glyph IDs:")
    print(" ".join(f"{glyph_id:03X}" for glyph_id in empty_glyphs))

    print("\nUsed Glyph IDs:")
    print(" ".join(f"{glyph_id:03X}" for glyph_id in used_glyphs))

if __name__ == "__main__":
    main()