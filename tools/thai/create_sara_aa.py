from pathlib import Path

from PIL import Image


FONT_PATH = Path(
    "graphics/fonts/latin_normal.png"
)

GLYPH_OUTPUT_PATH = Path(
    "graphics/fonts/thai/glyphs/011C_sara_aa.png"
)

GLYPH_ID = 0x11C
GLYPH_SIZE = 16

BACKGROUND = 0
MAIN_STROKE = 1
SHADOW = 2


# รูปสระ า แบบแคบ
#
# . = พื้นหลัง
# # = เส้นหลัก
#
# เป้าหมาย:
# - ลดส่วนยื่นด้านซ้าย
# - คงขาขวาไว้
# - ใช้พื้นที่ X=2 ถึง X=8
# - ให้ Width ใช้งานจริงเป็น 9
MAIN_PATTERN = [
    "................",  # 00
    "................",  # 01
    "...#####........",  # 02
    "..##...##.......",  # 03
    ".......##.......",  # 04
    ".......##.......",  # 05
    ".......##.......",  # 06
    ".......##.......",  # 07
    ".......##.......",  # 08
    ".......##.......",  # 09
    ".......##.......",  # 0A
    ".......##.......",  # 0B
    ".......##.......",  # 0C
    ".......##.......",  # 0D
    "................",  # 0E
    "................",  # 0F
]


def validate_pattern() -> None:
    if len(MAIN_PATTERN) != GLYPH_SIZE:
        raise SystemExit(
            f"MAIN_PATTERN ต้องมี {GLYPH_SIZE} แถว "
            f"แต่พบ {len(MAIN_PATTERN)}"
        )

    for row_number, row in enumerate(MAIN_PATTERN):
        if len(row) != GLYPH_SIZE:
            raise SystemExit(
                f"แถว {row_number:02X} ต้องมี "
                f"{GLYPH_SIZE} ตัว แต่พบ {len(row)}"
            )

        for character in row:
            if character not in {".", "#"}:
                raise SystemExit(
                    f"พบสัญลักษณ์ที่ไม่รองรับ {character!r} "
                    f"ในแถว {row_number:02X}"
                )


def main() -> None:
    validate_pattern()

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

    glyph = Image.new(
        mode="P",
        size=(GLYPH_SIZE, GLYPH_SIZE),
        color=BACKGROUND,
    )

    glyph.putpalette(palette)

    main_pixels: set[tuple[int, int]] = set()

    for y, row in enumerate(MAIN_PATTERN):
        for x, character in enumerate(row):
            if character == "#":
                main_pixels.add((x, y))

    shadow_pixels: set[tuple[int, int]] = set()

    # ใส่เงาเฉพาะด้านขวา
    # เพื่อไม่ให้สระ า กว้างและหนาเกินไป
    for x, y in main_pixels:
        shadow_x = x + 1
        shadow_y = y

        if shadow_x >= GLYPH_SIZE:
            continue

        if (shadow_x, shadow_y) not in main_pixels:
            shadow_pixels.add(
                (shadow_x, shadow_y)
            )

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

    GLYPH_OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    glyph.save(GLYPH_OUTPUT_PATH)

    print("=== Sara Aa Created ===")
    print(f"Glyph ID      : 0x{GLYPH_ID:03X}")
    print(f"Glyph file    : {GLYPH_OUTPUT_PATH}")
    print(f"Main pixels   : {len(main_pixels)}")
    print(f"Shadow pixels : {len(shadow_pixels)}")
    print("Palette used  : 0, 1, 2")


if __name__ == "__main__":
    main()