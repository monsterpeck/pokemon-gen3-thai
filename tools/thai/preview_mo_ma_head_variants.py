from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw


PROJECT_ROOT = Path(__file__).resolve().parents[2]

SOURCE_PATH = (
    PROJECT_ROOT
    / "graphics/fonts/thai/glyphs/0136_mo_ma.png"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "tools/thai/generated/mo_ma_head_variants"
)

CONTACT_SHEET_PATH = OUTPUT_DIR / "comparison.png"

GLYPH_SIZE = 16
SCALE = 12

BACKGROUND = 0
MAIN_STROKE = 1
SHADOW = 2


def load_source() -> tuple[Image.Image, list[int]]:
    if not SOURCE_PATH.exists():
        raise SystemExit(
            f"ไม่พบ Glyph ม: {SOURCE_PATH}"
        )

    with Image.open(SOURCE_PATH) as opened:
        image = opened.copy()

    if image.mode != "P":
        raise SystemExit(
            f"Glyph ต้องเป็นโหมด P แต่พบ {image.mode}"
        )

    if image.size != (GLYPH_SIZE, GLYPH_SIZE):
        raise SystemExit(
            f"Glyph ต้องมีขนาด 16x16 แต่พบ {image.size}"
        )

    palette = image.getpalette()

    if palette is None:
        raise SystemExit("Glyph ไม่มี Palette")

    return image, palette


def get_main_pixels(
    image: Image.Image,
) -> set[tuple[int, int]]:
    return {
        (x, y)
        for y in range(GLYPH_SIZE)
        for x in range(GLYPH_SIZE)
        if image.getpixel((x, y)) == MAIN_STROKE
    }


def build_glyph(
    main_pixels: set[tuple[int, int]],
    palette: list[int],
) -> Image.Image:
    shadow_pixels: set[tuple[int, int]] = set()

    for x, y in main_pixels:
        for offset_x, offset_y in (
            (1, 0),
            (0, 1),
        ):
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

    glyph = Image.new(
        mode="P",
        size=(GLYPH_SIZE, GLYPH_SIZE),
        color=BACKGROUND,
    )

    glyph.putpalette(palette)

    for x, y in shadow_pixels:
        glyph.putpixel(
            (x, y),
            SHADOW,
        )

    for x, y in main_pixels:
        glyph.putpixel(
            (x, y),
            MAIN_STROKE,
        )

    return glyph


def move_selected_pixels_up(
    pixels: set[tuple[int, int]],
    *,
    min_x: int,
    max_x: int,
    min_y: int,
    max_y: int,
    amount: int = 1,
) -> set[tuple[int, int]]:
    result: set[tuple[int, int]] = set()

    for x, y in pixels:
        should_move = (
            min_x <= x <= max_x
            and min_y <= y <= max_y
        )

        if should_move:
            new_y = max(
                0,
                y - amount,
            )

            result.add(
                (x, new_y)
            )
        else:
            result.add(
                (x, y)
            )

    return result


def create_variant_a(
    pixels: set[tuple[int, int]],
) -> set[tuple[int, int]]:
    """
    ยกเฉพาะหัวซ้ายส่วนบนขึ้น 1 px
    เป็นการแก้แบบเบาที่สุด
    """
    return move_selected_pixels_up(
        pixels,
        min_x=3,
        max_x=6,
        min_y=1,
        max_y=5,
        amount=1,
    )


def create_variant_b(
    pixels: set[tuple[int, int]],
) -> set[tuple[int, int]]:
    """
    ยกหัวซ้ายและช่วงเชื่อมด้านบนขึ้น 1 px
    พื้นที่กว้างกว่าแบบ A
    """
    return move_selected_pixels_up(
        pixels,
        min_x=3,
        max_x=8,
        min_y=1,
        max_y=6,
        amount=1,
    )


def create_variant_c(
    pixels: set[tuple[int, int]],
) -> set[tuple[int, int]]:
    """
    ยกส่วนบนเกือบทั้งหมดของ ม ขึ้น 1 px
    แต่ไม่แตะขาและฐานด้านล่าง
    """
    return move_selected_pixels_up(
        pixels,
        min_x=3,
        max_x=11,
        min_y=1,
        max_y=6,
        amount=1,
    )


def enlarge(
    image: Image.Image,
) -> Image.Image:
    return image.resize(
        (
            GLYPH_SIZE * SCALE,
            GLYPH_SIZE * SCALE,
        ),
        resample=Image.Resampling.NEAREST,
    )


def main() -> None:
    source, palette = load_source()
    original_pixels = get_main_pixels(source)

    variants = [
        (
            "Original",
            source,
            "ม ปัจจุบัน",
        ),
        (
            "Variant A",
            build_glyph(
                create_variant_a(original_pixels),
                palette,
            ),
            "ยกหัวซ้ายเล็กน้อย",
        ),
        (
            "Variant B",
            build_glyph(
                create_variant_b(original_pixels),
                palette,
            ),
            "ยกหัวและช่วงเชื่อม",
        ),
        (
            "Variant C",
            build_glyph(
                create_variant_c(original_pixels),
                palette,
            ),
            "ยกส่วนบนเกือบทั้งหมด",
        ),
    ]

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    cell_width = 225
    cell_height = 245

    sheet = Image.new(
        "RGB",
        (
            cell_width * len(variants),
            cell_height,
        ),
        "white",
    )

    draw = ImageDraw.Draw(sheet)

    for index, (
        name,
        glyph,
        description,
    ) in enumerate(variants):
        output_path = (
            OUTPUT_DIR
            / f"{index}_{name.lower().replace(' ', '_')}.png"
        )

        glyph.save(output_path)

        x = index * cell_width

        preview = enlarge(
            glyph
        ).convert("RGB")

        sheet.paste(
            preview,
            (x + 12, 12),
        )

        draw.rectangle(
            (
                x + 12,
                12,
                x + 12 + GLYPH_SIZE * SCALE,
                12 + GLYPH_SIZE * SCALE,
            ),
            outline="gray",
        )

        draw.text(
            (x + 12, 212),
            name,
            fill="black",
        )

        draw.text(
            (x + 12, 228),
            description,
            fill="black",
        )

    sheet.save(CONTACT_SHEET_PATH)

    print("=== ม Head Variants Created ===")
    print(f"Source     : {SOURCE_PATH}")
    print(f"Comparison : {CONTACT_SHEET_PATH}")
    print("")
    print("0 = Original")
    print("1 = Variant A")
    print("2 = Variant B")
    print("3 = Variant C")
    print("")
    print("ยังไม่มีการแก้ Font Sheet หรือ Glyph ตัวจริง")


if __name__ == "__main__":
    main()
