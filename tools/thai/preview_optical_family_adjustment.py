from pathlib import Path

from PIL import Image, ImageDraw


PROJECT_ROOT = Path(__file__).resolve().parents[2]

SOURCE_DIR = (
    PROJECT_ROOT
    / "tools/thai/generated/pixel_consonants/glyphs"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "tools/thai/generated/optical_family_preview"
)

OUTPUT_PATH = OUTPUT_DIR / "comparison.png"

GLYPH_SIZE = 16
SCALE = 10

FILES = {
    "ผ": "131_pho_phueng.png",
    "พ": "133_pho_phan.png",
    "ภ": "135_pho_samphao.png",
    "ม": "136_mo_ma.png",
    "ฝ": "132_fo_fa.png",
    "ฟ": "134_fo_fan.png",
}


def load(character: str) -> Image.Image:
    path = SOURCE_DIR / FILES[character]

    if not path.exists():
        raise SystemExit(f"ไม่พบไฟล์: {path}")

    with Image.open(path) as image:
        return image.convert("L")


def remove_pixel(
    image: Image.Image,
    x: int,
    y: int,
) -> None:
    if 0 <= x < GLYPH_SIZE and 0 <= y < GLYPH_SIZE:
        image.putpixel((x, y), 255)


def optical_adjust(
    character: str,
    source: Image.Image,
) -> Image.Image:
    result = source.copy()

    # เปิดพื้นที่ว่างภายในเล็กน้อย
    # โดยไม่เปลี่ยนกรอบนอกหรือขนาดรวม
    adjustments = {
        "ผ": [
            (6, 5),
            (7, 5),
            (6, 6),
        ],
        "พ": [
            (7, 5),
            (8, 5),
            (7, 6),
        ],
        "ภ": [
            (6, 5),
            (7, 5),
            (6, 6),
        ],
        "ม": [
            (7, 6),
            (8, 6),
            (7, 7),
        ],
    }

    for x, y in adjustments.get(character, []):
        remove_pixel(result, x, y)

    return result


def enlarge(image: Image.Image) -> Image.Image:
    return image.resize(
        (GLYPH_SIZE * SCALE, GLYPH_SIZE * SCALE),
        resample=Image.Resampling.NEAREST,
    )


def main() -> None:
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    characters = ["ผ", "พ", "ภ", "ม", "ฝ", "ฟ"]

    cell_width = 180
    cell_height = 390

    sheet = Image.new(
        "RGB",
        (len(characters) * cell_width, cell_height),
        "white",
    )

    draw = ImageDraw.Draw(sheet)

    for index, character in enumerate(characters):
        original = load(character)

        if character in "ผพภม":
            adjusted = optical_adjust(
                character,
                original,
            )
        else:
            adjusted = original.copy()

        x = index * cell_width

        sheet.paste(
            enlarge(original).convert("RGB"),
            (x + 10, 10),
        )

        sheet.paste(
            enlarge(adjusted).convert("RGB"),
            (x + 10, 205),
        )

        draw.text(
            (x + 10, 174),
            f"{character} original",
            fill="black",
        )

        draw.text(
            (x + 10, 369),
            f"{character} adjusted",
            fill="black",
        )

    sheet.save(OUTPUT_PATH)

    print("=== Optical Family Preview Created ===")
    print(f"Output: {OUTPUT_PATH}")
    print("บน = ต้นฉบับ")
    print("ล่าง = หลังเปิดพื้นที่ว่างภายใน")
    print("ยังไม่มีการแก้ Glyph ในเกม")


if __name__ == "__main__":
    main()
