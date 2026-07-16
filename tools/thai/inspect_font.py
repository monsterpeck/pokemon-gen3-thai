from pathlib import Path
import argparse

from PIL import Image


DEFAULT_FONT_PATH = Path("graphics/fonts/latin_normal.png")
OUTPUT_DIR = Path("tools/thai")

GLYPH_SIZE = 16
PREVIEW_SCALE = 16

THAI_SCAN_START = 0x118
THAI_SCAN_END = 0x1CF


def parse_glyph_id(value: str) -> int:
    """
    รับ Glyph ID เป็นเลขฐานสิบหก เช่น:
    118
    0x118
    BB
    0x00BB
    """
    cleaned = value.strip().lower()

    if cleaned.startswith("0x"):
        cleaned = cleaned[2:]

    try:
        glyph_id = int(cleaned, 16)
    except ValueError as error:
        raise argparse.ArgumentTypeError(
            f"'{value}' ไม่ใช่ Glyph ID ฐานสิบหกที่ถูกต้อง"
        ) from error

    if not 0 <= glyph_id <= 0x1FF:
        raise argparse.ArgumentTypeError(
            "Glyph ID ต้องอยู่ระหว่าง 0x000 ถึง 0x1FF"
        )

    return glyph_id


def validate_font_sheet(image: Image.Image, font_path: Path) -> None:
    """
    ตรวจสอบว่า Font Sheet มีขนาดที่แบ่งเป็นช่อง 16x16 ได้พอดี
    """
    if image.width % GLYPH_SIZE != 0:
        raise SystemExit(
            f"Font Sheet {font_path} มีความกว้าง {image.width} พิกเซล "
            f"ซึ่งหารด้วย {GLYPH_SIZE} ไม่ลงตัว"
        )

    if image.height % GLYPH_SIZE != 0:
        raise SystemExit(
            f"Font Sheet {font_path} มีความสูง {image.height} พิกเซล "
            f"ซึ่งหารด้วย {GLYPH_SIZE} ไม่ลงตัว"
        )


def get_glyph_box(
    glyph_id: int,
    columns: int,
) -> tuple[int, int, int, int]:
    """
    คำนวณกรอบพิกเซลของ Glyph ภายใน Font Sheet
    """
    column = glyph_id % columns
    row = glyph_id // columns

    pixel_x = column * GLYPH_SIZE
    pixel_y = row * GLYPH_SIZE

    return (
        pixel_x,
        pixel_y,
        pixel_x + GLYPH_SIZE,
        pixel_y + GLYPH_SIZE,
    )


def get_visible_pixel_positions(
    glyph_image: Image.Image,
    background_index: int,
) -> list[tuple[int, int]]:
    """
    คืนรายการพิกัดพิกเซลที่ไม่ใช่สีพื้นหลังภายใน Glyph
    """
    return [
        (x, y)
        for y in range(GLYPH_SIZE)
        for x in range(GLYPH_SIZE)
        if glyph_image.getpixel((x, y)) != background_index
    ]


def scan_range(
    image: Image.Image,
    start: int,
    end: int,
) -> None:
    """
    ตรวจสอบว่า Glyph ช่วงที่กำหนดเป็น EMPTY หรือ USED
    """
    columns = image.width // GLYPH_SIZE
    rows = image.height // GLYPH_SIZE
    total_glyphs = columns * rows

    if start < 0 or end >= total_glyphs or start > end:
        raise SystemExit(
            f"ช่วงสแกน 0x{start:03X}-0x{end:03X} "
            f"อยู่นอก Font Sheet 0x000-0x{total_glyphs - 1:03X}"
        )

    background_index = image.getpixel((0, 0))

    empty_glyphs: list[int] = []
    used_glyphs: list[int] = []

    for glyph_id in range(start, end + 1):
        box = get_glyph_box(glyph_id, columns)
        glyph_image = image.crop(box)

        visible_pixels = get_visible_pixel_positions(
            glyph_image,
            background_index,
        )

        if visible_pixels:
            used_glyphs.append(glyph_id)
        else:
            empty_glyphs.append(glyph_id)

    print("\n=== Glyph Range Scan ===")
    print(f"Range       : 0x{start:03X} - 0x{end:03X}")
    print(f"Total       : {end - start + 1}")
    print(f"Empty       : {len(empty_glyphs)}")
    print(f"Used        : {len(used_glyphs)}")

    print("\nUsed Glyph IDs:")

    if used_glyphs:
        print(
            " ".join(
                f"{glyph_id:03X}"
                for glyph_id in used_glyphs
            )
        )
    else:
        print("(none)")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "ตรวจสอบตำแหน่ง รูปร่าง และขอบเขตพิกเซล "
            "ของ Glyph ใน Font Sheet"
        )
    )

    parser.add_argument(
        "glyph_id",
        type=parse_glyph_id,
        help="Glyph ID ฐานสิบหก เช่น BB, 118 หรือ 0x118",
    )

    parser.add_argument(
        "--font",
        type=Path,
        default=DEFAULT_FONT_PATH,
        help=(
            "Font Sheet ที่ต้องการตรวจ "
            f"(ค่าเริ่มต้น: {DEFAULT_FONT_PATH})"
        ),
    )

    parser.add_argument(
        "--no-scan",
        action="store_true",
        help="ไม่สแกนช่วง Glyph ภาษาไทย 0x118-0x1CF",
    )

    args = parser.parse_args()

    font_path: Path = args.font

    if not font_path.exists():
        raise SystemExit(
            f"ไม่พบ Font Sheet: {font_path}"
        )

    image = Image.open(font_path)

    validate_font_sheet(image, font_path)

    columns = image.width // GLYPH_SIZE
    rows = image.height // GLYPH_SIZE
    total_glyphs = columns * rows

    glyph_id: int = args.glyph_id

    if glyph_id >= total_glyphs:
        raise SystemExit(
            f"Glyph 0x{glyph_id:03X} อยู่นอก Font Sheet "
            f"ซึ่งมี Glyph ทั้งหมด {total_glyphs} ช่อง "
            f"(0x000-0x{total_glyphs - 1:03X})"
        )

    column = glyph_id % columns
    row = glyph_id // columns

    pixel_x = column * GLYPH_SIZE
    pixel_y = row * GLYPH_SIZE

    box = get_glyph_box(glyph_id, columns)
    glyph_image = image.crop(box)

    background_index = image.getpixel((0, 0))

    visible_positions = get_visible_pixel_positions(
        glyph_image,
        background_index,
    )

    non_background_pixels = len(visible_positions)
    is_empty = non_background_pixels == 0

    print("=== Font Information ===")
    print(f"Font     : {font_path}")
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

    print("\n=== Glyph Content ===")
    print(f"Background index      : {background_index}")
    print(f"Non-background pixels : {non_background_pixels}")
    print(
        f"Status                : "
        f"{'EMPTY' if is_empty else 'USED'}"
    )

    print("\n=== Pixel Bounds ===")

    if is_empty:
        print("No visible pixels")
    else:
        min_x = min(x for x, _ in visible_positions)
        max_x = max(x for x, _ in visible_positions)
        min_y = min(y for _, y in visible_positions)
        max_y = max(y for _, y in visible_positions)

        content_width = max_x - min_x + 1
        content_height = max_y - min_y + 1

        print(f"Min X          : {min_x}")
        print(f"Max X          : {max_x}")
        print(f"Min Y          : {min_y}")
        print(f"Max Y          : {max_y}")
        print(f"Content width  : {content_width}")
        print(f"Content height : {content_height}")

    if not args.no_scan:
        scan_range(
            image,
            THAI_SCAN_START,
            THAI_SCAN_END,
        )

    preview = glyph_image.resize(
        (
            GLYPH_SIZE * PREVIEW_SCALE,
            GLYPH_SIZE * PREVIEW_SCALE,
        ),
        resample=Image.Resampling.NEAREST,
    )

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = (
        OUTPUT_DIR
        / f"glyph_{glyph_id:04X}_preview.png"
    )

    preview.save(output_path)

    print(f"\nPreview saved: {output_path}")


if __name__ == "__main__":
    main()