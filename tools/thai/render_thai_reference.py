from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


CHARACTER = "ก"

OUTPUT_DIR = Path("tools/thai/generated/reference")

FONTS = {
    "tahoma": Path("/mnt/c/Windows/Fonts/tahoma.ttf"),
    "leelawadee": Path("/mnt/c/Windows/Fonts/leelawad.ttf"),
}

# ทดลองหลายขนาดเพื่อดูว่าขนาดใดเหมาะกับกริด 16×16
FONT_SIZES = [12, 14, 16, 18]

CANVAS_SIZE = 32
TARGET_SIZE = 16
PREVIEW_SCALE = 16


def render_character(
    font_path: Path,
    font_size: int,
) -> Image.Image:
    """
    วาดตัวอักษรลง Canvas ขนาดใหญ่ก่อน แล้วตัดขอบพื้นที่ว่างออก
    """
    font = ImageFont.truetype(
        str(font_path),
        font_size,
    )

    canvas = Image.new(
        mode="L",
        size=(CANVAS_SIZE, CANVAS_SIZE),
        color=0,
    )

    draw = ImageDraw.Draw(canvas)

    bbox = draw.textbbox(
        (0, 0),
        CHARACTER,
        font=font,
    )

    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = (CANVAS_SIZE - text_width) // 2 - bbox[0]
    y = (CANVAS_SIZE - text_height) // 2 - bbox[1]

    draw.text(
        (x, y),
        CHARACTER,
        font=font,
        fill=255,
    )

    visible_bbox = canvas.getbbox()

    if visible_bbox is None:
        raise RuntimeError(
            f"ไม่สามารถวาดอักษร {CHARACTER} "
            f"ด้วยฟอนต์ {font_path}"
        )

    return canvas.crop(visible_bbox)


def fit_into_16x16(source: Image.Image) -> Image.Image:
    """
    ย่อรูปให้อยู่ภายในกริด 16×16 โดยรักษาสัดส่วน
    """
    max_width = 12
    max_height = 14

    scale = min(
        max_width / source.width,
        max_height / source.height,
    )

    new_width = max(1, round(source.width * scale))
    new_height = max(1, round(source.height * scale))

    resized = source.resize(
        (new_width, new_height),
        resample=Image.Resampling.LANCZOS,
    )

    target = Image.new(
        mode="L",
        size=(TARGET_SIZE, TARGET_SIZE),
        color=0,
    )

    x = (TARGET_SIZE - new_width) // 2
    y = (TARGET_SIZE - new_height) // 2

    target.paste(
        resized,
        (x, y),
    )

    return target


def create_binary_version(
    image: Image.Image,
    threshold: int,
) -> Image.Image:
    """
    แปลงภาพขาวดำแบบ Anti-alias ให้กลายเป็น Pixel ทึบ
    """
    return image.point(
        lambda value: 255 if value >= threshold else 0,
        mode="1",
    ).convert("L")


def save_preview(
    image: Image.Image,
    output_path: Path,
) -> None:
    """
    ขยายภาพด้วย NEAREST เพื่อให้เห็นพิกเซลชัดเจน
    """
    preview = image.resize(
        (
            image.width * PREVIEW_SCALE,
            image.height * PREVIEW_SCALE,
        ),
        resample=Image.Resampling.NEAREST,
    )

    preview.save(output_path)


def main() -> None:
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    print("=== Thai Glyph Reference Generator ===")
    print(f"Character : {CHARACTER}")
    print(f"Output    : {OUTPUT_DIR}")

    for font_name, font_path in FONTS.items():
        if not font_path.exists():
            print(f"SKIP: ไม่พบ {font_path}")
            continue

        for font_size in FONT_SIZES:
            rendered = render_character(
                font_path,
                font_size,
            )

            fitted = fit_into_16x16(rendered)

            grayscale_path = (
                OUTPUT_DIR
                / f"{font_name}_{font_size}_grayscale.png"
            )

            save_preview(
                fitted,
                grayscale_path,
            )

            for threshold in (64, 128, 192):
                binary = create_binary_version(
                    fitted,
                    threshold,
                )

                binary_path = (
                    OUTPUT_DIR
                    / (
                        f"{font_name}_{font_size}"
                        f"_threshold_{threshold}.png"
                    )
                )

                save_preview(
                    binary,
                    binary_path,
                )

            print(
                f"Created: {font_name}, size {font_size}, "
                f"source {rendered.width}x{rendered.height}"
            )

    print("\nเสร็จแล้ว")
    print(f"เปิดดูภาพได้ที่: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()