from pathlib import Path

from PIL import Image


REFERENCE_PATH = Path(
    "tools/thai/generated/reference/"
    "leelawadee_18_threshold_128.png"
)

FONT_PATH = Path(
    "graphics/fonts/latin_normal.png"
)

OUTPUT_PATH = Path(
    "graphics/fonts/thai/glyphs/0118_ko_kai.png"
)

GLYPH_SIZE = 16

BACKGROUND = 0
MAIN_STROKE = 1
SHADOW = 2


def load_reference_grid() -> Image.Image:
    """
    ภาพ Reference ที่บันทึกไว้เป็น Preview ขนาด 256×256
    แต่ต้นทางจริงคือกริด 16×16

    จึงย่อกลับเป็น 16×16 ด้วย NEAREST เพียงครั้งเดียว
    และไม่ครอปหรือเปลี่ยนสัดส่วนเพิ่มเติม
    """
    if not REFERENCE_PATH.exists():
        raise SystemExit(
            f"ไม่พบภาพอ้างอิง: {REFERENCE_PATH}"
        )

    reference = Image.open(
        REFERENCE_PATH
    ).convert("L")

    grid = reference.resize(
        (GLYPH_SIZE, GLYPH_SIZE),
        resample=Image.Resampling.NEAREST,
    )

    binary = grid.point(
        lambda value: 255 if value >= 128 else 0
    )

    return binary


def main() -> None:
    if not FONT_PATH.exists():
        raise SystemExit(
            f"ไม่พบ Font Sheet: {FONT_PATH}"
        )

    font_sheet = Image.open(FONT_PATH)

    if font_sheet.mode != "P":
        raise SystemExit(
            f"Font Sheet ต้องเป็นโหมด P "
            f"แต่พบโหมด {font_sheet.mode}"
        )

    palette = font_sheet.getpalette()

    if palette is None:
        raise SystemExit(
            f"ไม่พบ Palette ใน {FONT_PATH}"
        )

    mask = load_reference_grid()

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
            "ไม่พบพิกเซลตัวอักษรในภาพอ้างอิง"
        )

    shadow_pixels: set[tuple[int, int]] = set()

    # เพิ่มเงาเฉพาะด้านขวา
    # ไม่เพิ่มด้านล่าง เพื่อลดความอ้วนของ Glyph
    for x, y in main_pixels:
        shadow_position = (x + 1, y)

        if x + 1 >= GLYPH_SIZE:
            continue

        if shadow_position not in main_pixels:
            shadow_pixels.add(shadow_position)

    # วาดเงาก่อน
    for x, y in shadow_pixels:
        glyph.putpixel(
            (x, y),
            SHADOW,
        )

    # วาดเส้นหลักทับ
    for x, y in main_pixels:
        glyph.putpixel(
            (x, y),
            MAIN_STROKE,
        )

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    glyph.save(OUTPUT_PATH)

    min_x = min(x for x, _ in main_pixels)
    max_x = max(x for x, _ in main_pixels)
    min_y = min(y for _, y in main_pixels)
    max_y = max(y for _, y in main_pixels)

    print("=== Ko Kai Glyph Created ===")
    print(f"Reference     : {REFERENCE_PATH}")
    print(f"Output        : {OUTPUT_PATH}")
    print(f"Size          : {glyph.width} x {glyph.height}")
    print(f"Main pixels   : {len(main_pixels)}")
    print(f"Shadow pixels : {len(shadow_pixels)}")
    print(f"Main bounds   : X={min_x}-{max_x}, Y={min_y}-{max_y}")
    print("Palette used  : 0, 1, 2")


if __name__ == "__main__":
    main()