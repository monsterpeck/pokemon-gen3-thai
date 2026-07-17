from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


CHARACTER = "ข"

FONT_PATH = Path(
    "/mnt/c/Windows/Fonts/leelawad.ttf"
)

OUTPUT_PATH = Path(
    "tools/thai/generated/reference/"
    "kho_khai_leelawadee_18_threshold_128.png"
)

FONT_SIZE = 18

SOURCE_CANVAS_SIZE = 32
GLYPH_SIZE = 16
MAX_WIDTH = 12
MAX_HEIGHT = 14
THRESHOLD = 128
PREVIEW_SCALE = 16


def main() -> None:
    if not FONT_PATH.exists():
        raise SystemExit(
            f"ไม่พบฟอนต์: {FONT_PATH}"
        )

    font = ImageFont.truetype(
        str(FONT_PATH),
        FONT_SIZE,
    )

    source = Image.new(
        mode="L",
        size=(SOURCE_CANVAS_SIZE, SOURCE_CANVAS_SIZE),
        color=0,
    )

    draw = ImageDraw.Draw(source)

    bbox = draw.textbbox(
        (0, 0),
        CHARACTER,
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
        CHARACTER,
        font=font,
        fill=255,
    )

    visible_bbox = source.getbbox()

    if visible_bbox is None:
        raise SystemExit(
            f"ไม่สามารถวาดตัวอักษร {CHARACTER}"
        )

    cropped = source.crop(visible_bbox)

    scale = min(
        MAX_WIDTH / cropped.width,
        MAX_HEIGHT / cropped.height,
    )

    new_width = max(
        1,
        round(cropped.width * scale),
    )

    new_height = max(
        1,
        round(cropped.height * scale),
    )

    resized = cropped.resize(
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

    binary = glyph.point(
        lambda value: (
            255 if value >= THRESHOLD else 0
        )
    )

    preview = binary.resize(
        (
            GLYPH_SIZE * PREVIEW_SCALE,
            GLYPH_SIZE * PREVIEW_SCALE,
        ),
        resample=Image.Resampling.NEAREST,
    )

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    preview.save(OUTPUT_PATH)

    print("=== Kho Khai Reference Created ===")
    print(f"Character   : {CHARACTER}")
    print(f"Font        : {FONT_PATH}")
    print(f"Font size   : {FONT_SIZE}")
    print(
        f"Source size : "
        f"{cropped.width} x {cropped.height}"
    )
    print(
        f"Glyph size  : "
        f"{new_width} x {new_height}"
    )
    print(f"Position    : X={target_x}, Y={target_y}")
    print(f"Threshold   : {THRESHOLD}")
    print(f"Output      : {OUTPUT_PATH}")


if __name__ == "__main__":
    main()