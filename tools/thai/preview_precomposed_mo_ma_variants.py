from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[2]
GLYPH_DIR = ROOT / "graphics/fonts/thai/glyphs"
OUTPUT_DIR = ROOT / "tools/thai/generated/precomposed_mo_ma_variants"

BASE_PATH = GLYPH_DIR / "0136_mo_ma.png"
SARA_I_PATH = GLYPH_DIR / "0143_sara_i.png"
MAI_EK_PATH = GLYPH_DIR / "0144_mai_ek.png"

SIZE = 16
SCALE = 12


def load(path: Path) -> Image.Image:
    if not path.exists():
        raise SystemExit(f"ไม่พบไฟล์: {path}")

    image = Image.open(path).convert("P")

    if image.size != (SIZE, SIZE):
        raise SystemExit(f"{path} ต้องมีขนาด 16x16")

    return image


def move_upper_part(
    base: Image.Image,
    split_y: int,
    move_down: int,
) -> Image.Image:
    """
    ย้ายเฉพาะพิกเซลส่วนบนลงด้านล่าง
    ส่วนฐานล่างคงตำแหน่งเดิมเพื่อไม่ให้ baseline เปลี่ยน
    """
    result = base.copy()

    # ล้างพื้นที่ส่วนบนเดิม
    for y in range(split_y):
        for x in range(SIZE):
            result.putpixel((x, y), 0)

    # นำพิกเซลส่วนบนกลับมาวางต่ำลง
    for y in range(split_y):
        for x in range(SIZE):
            value = base.getpixel((x, y))

            if value == 0:
                continue

            target_y = y + move_down

            if 0 <= target_y < SIZE:
                result.putpixel((x, target_y), value)

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

            if value == 0:
                continue

            target_x = x + offset_x
            target_y = y + offset_y

            if 0 <= target_x < SIZE and 0 <= target_y < SIZE:
                result.putpixel((target_x, target_y), value)

    return result


def enlarge(image: Image.Image) -> Image.Image:
    return image.resize(
        (SIZE * SCALE, SIZE * SCALE),
        Image.Resampling.NEAREST,
    ).convert("RGB")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    base = load(BASE_PATH)
    sara_i = load(SARA_I_PATH)
    mai_ek = load(MAI_EK_PATH)

    variants = []

    variant_number = 1

    for split_y in (3, 4, 5):
        for move_down in (2, 3):
            adjusted = move_upper_part(
                base,
                split_y=split_y,
                move_down=move_down,
            )

            mi = overlay(
                adjusted,
                sara_i,
                offset_x=0,
                offset_y=0,
            )

            mo_ma_ek = overlay(
                adjusted,
                mai_ek,
                offset_x=1,
                offset_y=0,
            )

            name = (
                f"v{variant_number:02d}"
                f"_split{split_y}"
                f"_down{move_down}"
            )

            mi_path = OUTPUT_DIR / f"{name}_mi.png"
            ek_path = OUTPUT_DIR / f"{name}_mo_ma_ek.png"

            mi.save(mi_path)
            mo_ma_ek.save(ek_path)

            variants.append(
                (name, adjusted, mi, mo_ma_ek)
            )

            variant_number += 1

    cell_width = 620
    cell_height = 235

    sheet = Image.new(
        "RGB",
        (
            cell_width,
            cell_height * len(variants),
        ),
        "white",
    )

    draw = ImageDraw.Draw(sheet)

    for row, (name, adjusted, mi, mo_ma_ek) in enumerate(variants):
        top = row * cell_height

        draw.text(
            (10, top + 8),
            name,
            fill="black",
        )

        images = [
            ("base", adjusted),
            ("mi", mi),
            ("mo_ma_ek", mo_ma_ek),
        ]

        for column, (label, image) in enumerate(images):
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
                (left, top + 218),
                label,
                fill="black",
            )

    sheet_path = OUTPUT_DIR / "comparison.png"
    sheet.save(sheet_path)

    print("=== Precomposed Mo Ma Variants Created ===")
    print(f"Output directory : {OUTPUT_DIR}")
    print(f"Comparison       : {sheet_path}")
    print(f"Variants         : {len(variants)}")


if __name__ == "__main__":
    main()
