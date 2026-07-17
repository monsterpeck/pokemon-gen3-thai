from pathlib import Path
import argparse
import re

from PIL import Image


DEFAULT_FONT_PATH = Path(
    "graphics/fonts/latin_normal.png"
)

DEFAULT_OUTPUT_DIR = Path(
    "graphics/fonts/thai/glyphs"
)

GLYPH_SIZE = 16

BACKGROUND = 0
MAIN_STROKE = 1
SHADOW = 2


def parse_glyph_id(value: str) -> int:
    """
    รับ Glyph ID เป็นเลขฐานสิบหก เช่น:
    11B
    0x11B
    """
    cleaned = value.strip().lower()

    if cleaned.startswith("0x"):
        cleaned = cleaned[2:]

    try:
        glyph_id = int(cleaned, 16)
    except ValueError as error:
        raise argparse.ArgumentTypeError(
            f"{value!r} ไม่ใช่ Glyph ID ฐานสิบหก"
        ) from error

    if not 0 <= glyph_id <= 0x1FF:
        raise argparse.ArgumentTypeError(
            "Glyph ID ต้องอยู่ระหว่าง 0x000 ถึง 0x1FF"
        )

    return glyph_id


def validate_name(value: str) -> str:
    """
    ชื่อไฟล์ใช้ได้เฉพาะภาษาอังกฤษ ตัวเลข _ และ -
    """
    if not re.fullmatch(r"[A-Za-z0-9_-]+", value):
        raise argparse.ArgumentTypeError(
            "ชื่อใช้ได้เฉพาะ A-Z, a-z, 0-9, _ และ -"
        )

    return value


def load_reference_grid(
    reference_path: Path,
    threshold: int,
) -> Image.Image:
    """
    โหลดภาพ Reference แล้วแปลงกลับเป็นกริด 16×16

    ภาพ Reference ของเราถูกบันทึกเป็น Preview ขนาดใหญ่
    จึงย่อด้วย NEAREST เพื่อรักษาตำแหน่งพิกเซล
    """
    if not reference_path.exists():
        raise SystemExit(
            f"ไม่พบภาพ Reference: {reference_path}"
        )

    reference = Image.open(
        reference_path
    ).convert("L")

    grid = reference.resize(
        (GLYPH_SIZE, GLYPH_SIZE),
        resample=Image.Resampling.NEAREST,
    )

    return grid.point(
        lambda value: (
            255 if value >= threshold else 0
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "สร้าง Glyph ภาษาไทยขนาด 16×16 "
            "จากภาพ Reference"
        )
    )

    parser.add_argument(
        "glyph_id",
        type=parse_glyph_id,
        help="Glyph ID ฐานสิบหก เช่น 11B หรือ 0x11B",
    )

    parser.add_argument(
        "reference",
        type=Path,
        help="พาธของภาพ Reference",
    )

    parser.add_argument(
        "--name",
        required=True,
        type=validate_name,
        help="ชื่อไฟล์ เช่น ngo_ngu",
    )

    parser.add_argument(
        "--font",
        type=Path,
        default=DEFAULT_FONT_PATH,
        help=(
            "Font Sheet สำหรับคัดลอก Palette "
            f"(ค่าเริ่มต้น: {DEFAULT_FONT_PATH})"
        ),
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=(
            "โฟลเดอร์เก็บ Glyph "
            f"(ค่าเริ่มต้น: {DEFAULT_OUTPUT_DIR})"
        ),
    )

    parser.add_argument(
        "--threshold",
        type=int,
        default=128,
        help="ค่า Threshold ระหว่าง 0–255 (ค่าเริ่มต้น: 128)",
    )

    parser.add_argument(
        "--shadow",
        choices=("right", "right-bottom", "none"),
        default="right-bottom",
        help=(
            "รูปแบบเงา: right, right-bottom หรือ none "
            "(ค่าเริ่มต้น: right-bottom)"
        ),
    )

    args = parser.parse_args()

    if not args.font.exists():
        raise SystemExit(
            f"ไม่พบ Font Sheet: {args.font}"
        )

    if not 0 <= args.threshold <= 255:
        raise SystemExit(
            "--threshold ต้องอยู่ระหว่าง 0 ถึง 255"
        )

    font_sheet = Image.open(args.font)

    if font_sheet.mode != "P":
        raise SystemExit(
            f"Font Sheet ต้องเป็นโหมด P "
            f"แต่พบโหมด {font_sheet.mode}"
        )

    palette = font_sheet.getpalette()

    if palette is None:
        raise SystemExit(
            f"ไม่พบ Palette ใน {args.font}"
        )

    mask = load_reference_grid(
        args.reference,
        args.threshold,
    )

    glyph = Image.new(
        mode="P",
        size=(GLYPH_SIZE, GLYPH_SIZE),
        color=BACKGROUND,
    )

    glyph.putpalette(palette)

    main_pixels: set[tuple[int, int]] = set()

    for y in range(GLYPH_SIZE):
        for x in range(GLYPH_SIZE):
            if mask.getpixel((x, y)) >= 128:
                main_pixels.add((x, y))

    if not main_pixels:
        raise SystemExit(
            "ไม่พบพิกเซลตัวอักษรในภาพ Reference"
        )

    shadow_offsets: tuple[tuple[int, int], ...]

    if args.shadow == "right":
        shadow_offsets = (
            (1, 0),
        )
    elif args.shadow == "right-bottom":
        shadow_offsets = (
            (1, 0),
            (0, 1),
        )
    else:
        shadow_offsets = ()

    shadow_pixels: set[tuple[int, int]] = set()

    for x, y in main_pixels:
        for offset_x, offset_y in shadow_offsets:
            shadow_x = x + offset_x
            shadow_y = y + offset_y

            if not (
                0 <= shadow_x < GLYPH_SIZE
                and 0 <= shadow_y < GLYPH_SIZE
            ):
                continue

            if (shadow_x, shadow_y) not in main_pixels:
                shadow_pixels.add(
                    (shadow_x, shadow_y)
                )

    # วาดเงาก่อน
    for x, y in shadow_pixels:
        glyph.putpixel(
            (x, y),
            SHADOW,
        )

    # วาดเส้นหลักทีหลัง
    for x, y in main_pixels:
        glyph.putpixel(
            (x, y),
            MAIN_STROKE,
        )

    args.output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = args.output_dir / (
        f"{args.glyph_id:04X}_{args.name}.png"
    )

    glyph.save(output_path)

    all_visible_pixels = main_pixels | shadow_pixels

    min_x = min(x for x, _ in all_visible_pixels)
    max_x = max(x for x, _ in all_visible_pixels)
    min_y = min(y for _, y in all_visible_pixels)
    max_y = max(y for _, y in all_visible_pixels)

    print("=== Thai Glyph Created ===")
    print(f"Glyph ID      : 0x{args.glyph_id:03X}")
    print(f"Name          : {args.name}")
    print(f"Reference     : {args.reference}")
    print(f"Output        : {output_path}")
    print(f"Shadow mode   : {args.shadow}")
    print(f"Main pixels   : {len(main_pixels)}")
    print(f"Shadow pixels : {len(shadow_pixels)}")
    print(
        f"Visible bounds: "
        f"X={min_x}-{max_x}, Y={min_y}-{max_y}"
    )
    print(
        f"Minimum width : {max_x + 1}"
    )


if __name__ == "__main__":
    main()