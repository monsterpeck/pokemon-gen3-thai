from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[2]
GLYPH_DIR = ROOT / "graphics/fonts/thai/glyphs"
OUTPUT_DIR = ROOT / "tools/thai/generated/precomposed_mo_ma_scaled"

BASE_PATH = GLYPH_DIR / "0136_mo_ma.png"
SARA_I_PATH = GLYPH_DIR / "0143_sara_i.png"
MAI_EK_PATH = GLYPH_DIR / "0144_mai_ek.png"

SIZE = 16
SCALE = 12
BACKGROUND = 0


def load(path: Path) -> Image.Image:
    if not path.exists():
        raise SystemExit(f"ไม่พบไฟล์: {path}")

    with Image.open(path) as opened:
        image = opened.copy()

    if image.mode != "P":
        image = image.convert("P")

    if image.size != (SIZE, SIZE):
        raise SystemExit(
            f"{path.name} ต้องมีขนาด 16x16 แต่พบ {image.size}"
        )

    return image


def vertical_scale_to_bottom(
    base: Image.Image,
    target_height: int,
) -> Image.Image:
    """
    ย่อ Glyph ทั้งตัวในแนวตั้งและตรึงขอบล่างไว้ที่ Y=15
    ไม่แยกส่วนหัวกับลำตัว จึงไม่ทำให้เส้นขาดหรือซ้อนผิดรูป
    """
    bbox = base.getbbox()

    if bbox is None:
        raise SystemExit("Base glyph ว่างเปล่า")

    left, top, right, bottom = bbox
    content = base.crop((left, top, right, bottom))

    target_width = content.width

    resized = content.resize(
        (target_width, target_height),
        Image.Resampling.NEAREST,
    )

    result = Image.new(
        "P",
        (SIZE, SIZE),
        BACKGROUND,
    )
    result.putpalette(base.getpalette())

    target_x = left
    target_y = SIZE - target_height

    result.paste(
        resized,
        (target_x, target_y),
    )

    return result


def overlay(
    base: Image.Image,
    mark: Image.Image,
    offset_x: int,
    offset_y: int,
) -> Image.Image:
    result = base.copy()

    for y in range(SIZE):
        for x in range(SIZE):
            value = mark.getpixel((x, y))

            if value == BACKGROUND:
                continue

            target_x = x + offset_x
            target_y = y + offset_y

            if 0 <= target_x < SIZE and 0 <= target_y < SIZE:
                result.putpixel(
                    (target_x, target_y),
                    value,
                )

    return result


def enlarge(image: Image.Image) -> Image.Image:
    return image.resize(
        (SIZE * SCALE, SIZE * SCALE),
        Image.Resampling.NEAREST,
    ).convert("RGB")


def main() -> None:
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    base = load(BASE_PATH)
    sara_i = load(SARA_I_PATH)
    mai_ek = load(MAI_EK_PATH)

    settings = [
        # ชื่อ, ความสูงฐาน, X สระอิ, Y สระอิ, X ไม้เอก, Y ไม้เอก
        ("v07", 13, 0, 0, 1, 0),
        ("v08", 13, 1, 0, 2, 0),
        ("v09", 12, 0, 0, 1, 0),
        ("v10", 12, 1, 0, 2, 0),
        ("v11", 11, 0, 0, 1, 0),
        ("v12", 11, 1, 0, 2, 0),
    ]

    variants = []

    for (
        name,
        base_height,
        sara_x,
        sara_y,
        ek_x,
        ek_y,
    ) in settings:
        adjusted = vertical_scale_to_bottom(
            base,
            target_height=base_height,
        )

        mi = overlay(
            adjusted,
            sara_i,
            offset_x=sara_x,
            offset_y=sara_y,
        )

        mo_ma_ek = overlay(
            adjusted,
            mai_ek,
            offset_x=ek_x,
            offset_y=ek_y,
        )

        adjusted.save(
            OUTPUT_DIR / f"{name}_base.png"
        )
        mi.save(
            OUTPUT_DIR / f"{name}_mi.png"
        )
        mo_ma_ek.save(
            OUTPUT_DIR / f"{name}_mo_ma_ek.png"
        )

        variants.append(
            (
                name,
                base_height,
                adjusted,
                mi,
                mo_ma_ek,
            )
        )

    cell_width = 620
    cell_height = 240

    sheet = Image.new(
        "RGB",
        (
            cell_width,
            cell_height * len(variants),
        ),
        "white",
    )

    draw = ImageDraw.Draw(sheet)

    for row, (
        name,
        base_height,
        adjusted,
        mi,
        mo_ma_ek,
    ) in enumerate(variants):
        top = row * cell_height

        draw.text(
            (10, top + 7),
            f"{name} base height={base_height}",
            fill="black",
        )

        columns = [
            ("base", adjusted),
            ("mi", mi),
            ("mo_ma_ek", mo_ma_ek),
        ]

        for column, (label, image) in enumerate(columns):
            left = 10 + column * 200

            sheet.paste(
                enlarge(image),
                (left, top + 28),
            )

            draw.rectangle(
                (
                    left,
                    top + 28,
                    left + SIZE * SCALE,
                    top + 28 + SIZE * SCALE,
                ),
                outline="gray",
            )

            draw.text(
                (left, top + 220),
                label,
                fill="black",
            )

    comparison = OUTPUT_DIR / "comparison.png"
    sheet.save(comparison)

    print("=== Scaled Precomposed Variants Created ===")
    print(f"Output     : {OUTPUT_DIR}")
    print(f"Comparison : {comparison}")
    print("Variants   : V07–V12")


if __name__ == "__main__":
    main()
