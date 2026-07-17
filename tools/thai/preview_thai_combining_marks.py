from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw


PROJECT_ROOT = Path(__file__).resolve().parents[2]

CONSONANT_DIR = (
    PROJECT_ROOT
    / "tools/thai/generated/pixel_consonants/glyphs"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "tools/thai/generated/combining_mark_preview"
)

OUTPUT_PATH = OUTPUT_DIR / "comparison.png"

GLYPH_SIZE = 16
SCALE = 12

BACKGROUND = 255
FOREGROUND = 0


CONSONANTS = {
    "ม": "136_mo_ma.png",
    "ฝ": "132_fo_fa.png",
    "ฟ": "134_fo_fan.png",
    "ผ": "131_pho_phueng.png",
    "ภ": "135_pho_samphao.png",
    "ญ": "122_yo_ying.png",
    "ฐ": "125_tho_than.png",
}


TESTS = [
    ("ม่", "ม", "mai_ek"),
    ("ฝ่", "ฝ", "mai_ek"),
    ("ฟ้", "ฟ", "mai_tho"),
    ("ผิ", "ผ", "sara_i"),
    ("ภู", "ภ", "sara_u"),
    ("ญุ", "ญ", "sara_u"),
    ("ฐิ", "ฐ", "sara_i"),
]


def load_consonant(character: str) -> Image.Image:
    path = CONSONANT_DIR / CONSONANTS[character]

    if not path.exists():
        raise SystemExit(f"ไม่พบ Glyph: {path}")

    with Image.open(path) as opened:
        image = opened.convert("L")

    if image.size != (GLYPH_SIZE, GLYPH_SIZE):
        raise SystemExit(
            f"{path.name} ต้องมีขนาด 16x16 "
            f"แต่พบ {image.size}"
        )

    return image


def draw_mark(
    mark_name: str,
) -> Image.Image:
    """
    สร้าง Mark จำลองเพื่อทดสอบพื้นที่เท่านั้น
    ยังไม่ใช่ Glyph Final
    """
    mark = Image.new(
        "L",
        (GLYPH_SIZE, GLYPH_SIZE),
        BACKGROUND,
    )

    pixels: set[tuple[int, int]] = set()

    if mark_name == "mai_ek":
        # ไม้เอกขนาดเล็ก 1x3
        pixels = {
            (7, 0),
            (7, 1),
            (7, 2),
        }

    elif mark_name == "mai_tho":
        # ไม้โทจำลองแบบ 3x3
        pixels = {
            (6, 0),
            (7, 0),
            (8, 0),
            (8, 1),
            (7, 2),
        }

    elif mark_name == "sara_i":
        # สระอิจำลองเหนือพยัญชนะ
        pixels = {
            (5, 1),
            (6, 0),
            (7, 0),
            (8, 0),
            (9, 1),
        }

    elif mark_name == "sara_u":
        # สระอุจำลองด้านล่าง
        pixels = {
            (7, 14),
            (7, 15),
            (8, 15),
        }

    else:
        raise ValueError(
            f"ไม่รู้จัก Mark: {mark_name}"
        )

    for x, y in pixels:
        mark.putpixel(
            (x, y),
            FOREGROUND,
        )

    return mark


def combine(
    consonant: Image.Image,
    mark: Image.Image,
) -> Image.Image:
    result = consonant.copy()

    for y in range(GLYPH_SIZE):
        for x in range(GLYPH_SIZE):
            if mark.getpixel((x, y)) < 128:
                result.putpixel(
                    (x, y),
                    FOREGROUND,
                )

    return result


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
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    cell_width = 215
    cell_height = 250

    sheet = Image.new(
        "RGB",
        (
            cell_width * len(TESTS),
            cell_height,
        ),
        "white",
    )

    draw = ImageDraw.Draw(sheet)

    for index, (
        label,
        consonant_character,
        mark_name,
    ) in enumerate(TESTS):
        consonant = load_consonant(
            consonant_character
        )

        mark = draw_mark(
            mark_name
        )

        combined = combine(
            consonant,
            mark,
        )

        output_path = (
            OUTPUT_DIR
            / (
                f"{index:02d}_"
                f"u{ord(consonant_character):04x}_"
                f"{mark_name}.png"
            )
        )

        combined.save(output_path)

        x = index * cell_width

        preview = enlarge(
            combined
        ).convert("RGB")

        sheet.paste(
            preview,
            (x + 10, 10),
        )

        # กรอบ 16x16
        draw.rectangle(
            (
                x + 10,
                10,
                x + 10 + GLYPH_SIZE * SCALE,
                10 + GLYPH_SIZE * SCALE,
            ),
            outline="gray",
        )

        # เส้นแบ่งโซนด้านบน Y=3
        draw.line(
            (
                x + 10,
                10 + 3 * SCALE,
                x + 10 + GLYPH_SIZE * SCALE,
                10 + 3 * SCALE,
            ),
            fill="gray",
        )

        # Baseline โดยประมาณ Y=14
        draw.line(
            (
                x + 10,
                10 + 14 * SCALE,
                x + 10 + GLYPH_SIZE * SCALE,
                10 + 14 * SCALE,
            ),
            fill="gray",
        )

        draw.text(
            (x + 10, 210),
            label,
            fill="black",
        )

        draw.text(
            (x + 10, 228),
            f"{consonant_character} + {mark_name}",
            fill="black",
        )

    sheet.save(
        OUTPUT_PATH
    )

    print("=== Combining Mark Preview Created ===")
    print(f"Output : {OUTPUT_PATH}")
    print("")
    print("เส้นบนในช่อง  : ขอบโซนวรรณยุกต์ Y=0..2")
    print("เส้นล่างในช่อง: Baseline โดยประมาณ Y=14")
    print("")
    print("ยังไม่มีการแก้ Glyph หรือไฟล์เกม")


if __name__ == "__main__":
    main()
