from pathlib import Path

from PIL import Image


FONT_PATH = Path("graphics/fonts/latin_normal.png")
OUTPUT_PATH = Path(
    "graphics/fonts/thai/glyphs/0118_ko_kai.png"
)

GLYPH_SIZE = 16
BACKGROUND_INDEX = 0


# รูปร่างตัว ก รุ่นทดสอบ
# แต่ละคู่คือพิกัด (x, y) ภายในพื้นที่ 16x16
KO_KAI_PIXELS = [
    # ส่วนหัว
    (5, 3), (6, 3), (7, 3), (8, 3), (9, 3),
    (4, 4), (10, 4),

    # เส้นตั้งด้านซ้าย
    (4, 5), (4, 6), (4, 7), (4, 8),
    (4, 9), (4, 10), (4, 11),

    # ส่วนด้านขวา
    (10, 5), (10, 6), (10, 7),
    (9, 8), (8, 8),

    # เส้นฐาน
    (5, 11), (6, 11), (7, 11),
    (8, 11), (9, 11),

    # หาง
    (9, 9), (10, 10), (11, 11),
]


def main() -> None:
    # เปิด Font Sheet หลัก เพื่อคัดลอก Palette เดิม
    font_sheet = Image.open(FONT_PATH)

    palette = font_sheet.getpalette()

    if palette is None:
        raise SystemExit(
            "ไม่พบ Palette ใน graphics/fonts/latin_normal.png"
        )

    # ดูว่า Font Sheet ใช้ Palette index อะไรอยู่บ้าง
    used_indices = sorted(set(font_sheet.getdata()))

    foreground_candidates = [
        index
        for index in used_indices
        if index != BACKGROUND_INDEX
    ]

    if not foreground_candidates:
        raise SystemExit(
            "ไม่พบ Palette index สำหรับสีตัวอักษร"
        )

    foreground_index = foreground_candidates[0]

    # สร้างภาพ Glyph ขนาด 16x16
    image = Image.new(
        mode="P",
        size=(GLYPH_SIZE, GLYPH_SIZE),
        color=BACKGROUND_INDEX,
    )

    # ใช้ Palette ชุดเดียวกับ Font Sheet
    image.putpalette(palette)

    # วาดพิกเซลตัว ก
    for x, y in KO_KAI_PIXELS:
        image.putpixel((x, y), foreground_index)

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    image.save(OUTPUT_PATH)

    print(f"Glyph created     : {OUTPUT_PATH}")
    print(f"Size              : {image.width} x {image.height}")
    print(f"Mode              : {image.mode}")
    print(f"Palette indices   : {used_indices}")
    print(f"Background index  : {BACKGROUND_INDEX}")
    print(f"Foreground index  : {foreground_index}")


if __name__ == "__main__":
    main()