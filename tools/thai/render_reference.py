from pathlib import Path
import argparse
import re

from PIL import Image, ImageDraw, ImageFont


DEFAULT_FONT_PATH = Path(
    "/mnt/c/Windows/Fonts/leelawad.ttf"
)

DEFAULT_OUTPUT_DIR = Path(
    "tools/thai/generated/reference"
)

SOURCE_CANVAS_SIZE = 32
GLYPH_SIZE = 16
PREVIEW_SCALE = 16

DEFAULT_FONT_SIZE = 18
DEFAULT_THRESHOLD = 128

MAX_WIDTH = 12
MAX_HEIGHT = 14


def validate_character(value: str) -> str:
    """
    ตรวจสอบว่าผู้ใช้ส่งอักษรมาเพียงหนึ่งตัว
    เช่น ก, ข, ค
    """
    if len(value) != 1:
        raise argparse.ArgumentTypeError(
            "ต้องระบุตัวอักษรเพียงหนึ่งตัว เช่น ก หรือ ข"
        )

    return value


def validate_name(value: str) -> str:
    """
    ชื่อไฟล์อนุญาตเฉพาะ:
    a-z, A-Z, 0-9, _ และ -
    """
    if not re.fullmatch(r"[A-Za-z0-9_-]+", value):
        raise argparse.ArgumentTypeError(
            "ชื่อไฟล์ใช้ได้เฉพาะตัวอักษรอังกฤษ ตัวเลข _ และ -"
        )

    return value


def render_character(
    character: str,
    font_path: Path,
    font_size: int,
) -> Image.Image:
    """
    วาดตัวอักษรบน Canvas ขนาดใหญ่ แล้วครอปเฉพาะพื้นที่ที่มีตัวอักษร
    """
    font = ImageFont.truetype(
        str(font_path),
        font_size,
    )

    source = Image.new(
        mode="L",
        size=(SOURCE_CANVAS_SIZE, SOURCE_CANVAS_SIZE),
        color=0,
    )

    draw = ImageDraw.Draw(source)

    bbox = draw.textbbox(
        (0, 0),
        character,
        font=font,
    )

    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    draw_x = (
        (SOURCE_CANVAS_SIZE - text_width) // 2
        - bbox[0]
    )

    draw_y = (
        (SOURCE_CANVAS_SIZE - text_height) // 2
        - bbox[1]
    )

    draw.text(
        (draw_x, draw_y),
        character,
        font=font,
        fill=255,
    )

    visible_bbox = source.getbbox()

    if visible_bbox is None:
        raise SystemExit(
            f"ไม่สามารถวาดตัวอักษร {character!r} "
            f"ด้วยฟอนต์ {font_path}"
        )

    return source.crop(visible_bbox)


def fit_into_glyph(
    source: Image.Image,
) -> tuple[Image.Image, int, int, int, int]:
    """
    ย่อภาพให้อยู่ภายในพื้นที่สูงสุด 12×14
    แล้ววางตรงกลางช่อง Glyph 16×16
    """
    scale = min(
        MAX_WIDTH / source.width,
        MAX_HEIGHT / source.height,
    )

    new_width = max(
        1,
        round(source.width * scale),
    )

    new_height = max(
        1,
        round(source.height * scale),
    )

    resized = source.resize(
        (new_width, new_height),
        resample=Image.Resampling.LANCZOS,
    )

    glyph = Image.new(
        mode="L",
        size=(GLYPH_SIZE, GLYPH_SIZE),
        color=0,
    )

    target_x = (
        GLYPH_SIZE - new_width
    ) // 2

    target_y = (
        GLYPH_SIZE - new_height
    ) // 2

    glyph.paste(
        resized,
        (target_x, target_y),
    )

    return (
        glyph,
        new_width,
        new_height,
        target_x,
        target_y,
    )


def make_binary(
    image: Image.Image,
    threshold: int,
) -> Image.Image:
    """
    แปลงภาพระดับสีเทาให้เป็นภาพขาวดำตามค่า Threshold
    """
    return image.point(
        lambda value: (
            255 if value >= threshold else 0
        )
    )


def make_preview(
    image: Image.Image,
) -> Image.Image:
    """
    ขยายกริด 16×16 เป็น 256×256 เพื่อให้ดูพิกเซลง่าย
    """
    return image.resize(
        (
            GLYPH_SIZE * PREVIEW_SCALE,
            GLYPH_SIZE * PREVIEW_SCALE,
        ),
        resample=Image.Resampling.NEAREST,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "สร้างภาพอ้างอิงตัวอักษรไทยสำหรับออกแบบ "
            "Glyph ขนาด 16×16"
        )
    )

    parser.add_argument(
        "character",
        type=validate_character,
        help="ตัวอักษรหนึ่งตัว เช่น ก, ข หรือ ค",
    )

    parser.add_argument(
        "--name",
        required=True,
        type=validate_name,
        help="ชื่อภาษาอังกฤษสำหรับใช้ตั้งชื่อไฟล์ เช่น kho_khai",
    )

    parser.add_argument(
        "--font",
        type=Path,
        default=DEFAULT_FONT_PATH,
        help=(
            "ไฟล์ฟอนต์ TTF "
            f"(ค่าเริ่มต้น: {DEFAULT_FONT_PATH})"
        ),
    )

    parser.add_argument(
        "--font-size",
        type=int,
        default=DEFAULT_FONT_SIZE,
        help=f"ขนาดฟอนต์ต้นทาง (ค่าเริ่มต้น: {DEFAULT_FONT_SIZE})",
    )

    parser.add_argument(
        "--threshold",
        type=int,
        default=DEFAULT_THRESHOLD,
        help=(
            "ค่า Threshold ระหว่าง 0–255 "
            f"(ค่าเริ่มต้น: {DEFAULT_THRESHOLD})"
        ),
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=(
            "โฟลเดอร์ผลลัพธ์ "
            f"(ค่าเริ่มต้น: {DEFAULT_OUTPUT_DIR})"
        ),
    )

    args = parser.parse_args()

    if not args.font.exists():
        raise SystemExit(
            f"ไม่พบฟอนต์: {args.font}"
        )

    if args.font_size <= 0:
        raise SystemExit(
            "--font-size ต้องมากกว่า 0"
        )

    if not 0 <= args.threshold <= 255:
        raise SystemExit(
            "--threshold ต้องอยู่ระหว่าง 0 ถึง 255"
        )

    rendered = render_character(
        character=args.character,
        font_path=args.font,
        font_size=args.font_size,
    )

    (
        fitted,
        fitted_width,
        fitted_height,
        target_x,
        target_y,
    ) = fit_into_glyph(rendered)

    binary = make_binary(
        fitted,
        args.threshold,
    )

    preview = make_preview(binary)

    args.output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    font_name = args.font.stem.lower()

    output_path = args.output_dir / (
        f"{args.name}_{font_name}_"
        f"{args.font_size}_threshold_{args.threshold}.png"
    )

    preview.save(output_path)

    print("=== Thai Reference Created ===")
    print(f"Character   : {args.character}")
    print(f"Name        : {args.name}")
    print(f"Unicode     : U+{ord(args.character):04X}")
    print(f"Font        : {args.font}")
    print(f"Font size   : {args.font_size}")
    print(
        f"Source size : "
        f"{rendered.width} x {rendered.height}"
    )
    print(
        f"Glyph size  : "
        f"{fitted_width} x {fitted_height}"
    )
    print(
        f"Position    : "
        f"X={target_x}, Y={target_y}"
    )
    print(f"Threshold   : {args.threshold}")
    print(f"Output      : {output_path}")


if __name__ == "__main__":
    main()