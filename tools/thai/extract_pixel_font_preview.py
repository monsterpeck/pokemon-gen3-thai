from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw


SOURCE_PATH = Path(
    "tools/thai/source/thai_pixel_font_reference.png"
)

OUTPUT_DIR = Path(
    "tools/thai/generated/pixel_font_preview"
)

GLYPH_DIR = OUTPUT_DIR / "glyphs"
CONTACT_SHEET_PATH = OUTPUT_DIR / "contact_sheet.png"

COLUMNS = 16
ROWS = 12

# พยัญชนะไทยแถวแรกอยู่แถวที่ 7 ของภาพ
# เมื่อนับแบบ Python จะเป็น index 6
SOURCE_ROW_INDEX = 6

CHARACTERS = [
    "ก", "ข", "ฃ", "ค",
    "ฅ", "ฆ", "ง", "จ",
    "ฉ", "ช", "ซ", "ฌ",
    "ญ", "ฎ", "ฏ", "ฐ",
]

GLYPH_SIZE = 16
MAX_GLYPH_WIDTH = 12
MAX_GLYPH_HEIGHT = 14
THRESHOLD = 140

PREVIEW_SCALE = 8
CONTACT_COLUMNS = 8


def is_grid_pixel(
    red: int,
    green: int,
    blue: int,
) -> bool:
    """
    เส้นกริดเป็นสีเทาอ่อน:
    ค่า RGB ใกล้กันและไม่ขาวสนิท
    """
    channel_difference = max(
        red,
        green,
        blue,
    ) - min(
        red,
        green,
        blue,
    )

    brightness = (
        red + green + blue
    ) // 3

    return (
        channel_difference <= 8
        and 185 <= brightness <= 245
    )


def find_vertical_grid_lines(
    image: Image.Image,
) -> list[int]:
    """
    พิกัดเส้นกริดจริงของภาพต้นฉบับขนาด 1024x1536
    """
    if image.size != (1024, 1536):
        raise RuntimeError(
            "ภาพต้นฉบับต้องมีขนาด 1024x1536 "
            f"แต่พบ {image.width}x{image.height}"
        )

    return [
        4, 61, 119, 177,
        237, 296, 354, 413,
        472, 532, 592, 653,
        712, 772, 832, 891,
        951,
    ]


def find_horizontal_grid_lines(
    image: Image.Image,
) -> list[int]:
    """
    พิกัดเส้นกริดจริงของภาพต้นฉบับขนาด 1024x1536
    """
    if image.size != (1024, 1536):
        raise RuntimeError(
            "ภาพต้นฉบับต้องมีขนาด 1024x1536 "
            f"แต่พบ {image.width}x{image.height}"
        )

    return [
        5, 121, 238, 355,
        472, 589, 701, 821,
        938, 1055, 1186,
        1321, 1450,
    ]


def extract_character_mask(
    image: Image.Image,
    left: int,
    top: int,
    right: int,
    bottom: int,
) -> Image.Image:
    """
    ตัดขอบเส้นกริดออก 3 พิกเซล
    แล้วเลือกเฉพาะพิกเซลสีเข้มของตัวอักษร
    """
    cell = image.crop(
        (
            left + 3,
            top + 3,
            right - 2,
            bottom - 2,
        )
    ).convert("L")

    mask = cell.point(
        lambda value: (
            255
            if value < THRESHOLD
            else 0
        )
    )

    bounds = mask.getbbox()

    if bounds is None:
        raise RuntimeError(
            "ไม่พบพิกเซลตัวอักษรในช่อง"
        )

    return mask.crop(bounds)


def fit_into_16x16(
    source: Image.Image,
) -> Image.Image:
    scale = min(
        MAX_GLYPH_WIDTH / source.width,
        MAX_GLYPH_HEIGHT / source.height,
    )

    width = max(
        1,
        round(source.width * scale),
    )

    height = max(
        1,
        round(source.height * scale),
    )

    resized = source.resize(
        (width, height),
        resample=Image.Resampling.NEAREST,
    )

    glyph = Image.new(
        "L",
        (GLYPH_SIZE, GLYPH_SIZE),
        255,
    )

    target_x = (
        GLYPH_SIZE - width
    ) // 2

    # วางชิด baseline ด้านล่างเล็กน้อย
    target_y = (
        GLYPH_SIZE - height - 1
    )

    glyph.paste(
        Image.eval(
            resized,
            lambda value: 0
            if value >= 128
            else 255,
        ),
        (target_x, target_y),
    )

    return glyph


def enlarge(
    glyph: Image.Image,
) -> Image.Image:
    return glyph.resize(
        (
            GLYPH_SIZE * PREVIEW_SCALE,
            GLYPH_SIZE * PREVIEW_SCALE,
        ),
        resample=Image.Resampling.NEAREST,
    )


def create_contact_sheet(
    records: list[
        tuple[str, Image.Image]
    ],
) -> None:
    cell_width = (
        GLYPH_SIZE * PREVIEW_SCALE
        + 24
    )

    cell_height = (
        GLYPH_SIZE * PREVIEW_SCALE
        + 45
    )

    contact_rows = (
        len(records)
        + CONTACT_COLUMNS - 1
    ) // CONTACT_COLUMNS

    sheet = Image.new(
        "RGB",
        (
            cell_width * CONTACT_COLUMNS,
            cell_height * contact_rows,
        ),
        "white",
    )

    draw = ImageDraw.Draw(sheet)

    for index, (
        character,
        glyph,
    ) in enumerate(records):
        column = (
            index % CONTACT_COLUMNS
        )

        row = (
            index // CONTACT_COLUMNS
        )

        x = column * cell_width
        y = row * cell_height

        preview = enlarge(
            glyph
        ).convert("RGB")

        sheet.paste(
            preview,
            (x + 8, y + 8),
        )

        draw.rectangle(
            (
                x + 8,
                y + 8,
                x + 8
                + GLYPH_SIZE * PREVIEW_SCALE,
                y + 8
                + GLYPH_SIZE * PREVIEW_SCALE,
            ),
            outline="gray",
        )

        draw.text(
            (x + 8, y + 140),
            (
                f"{character} "
                f"U+{ord(character):04X}"
            ),
            fill="black",
        )

    sheet.save(
        CONTACT_SHEET_PATH
    )


def main() -> None:
    if not SOURCE_PATH.exists():
        raise SystemExit(
            f"ไม่พบภาพต้นฉบับ: {SOURCE_PATH}"
        )

    image = Image.open(
        SOURCE_PATH
    ).convert("RGB")

    vertical_lines = (
        find_vertical_grid_lines(image)
    )

    horizontal_lines = (
        find_horizontal_grid_lines(image)
    )

    print(
        "Vertical grid:",
        vertical_lines,
    )

    print(
        "Horizontal grid:",
        horizontal_lines,
    )

    if len(vertical_lines) != 17:
        raise SystemExit(
            "ตรวจพบเส้นแนวตั้งไม่ครบ 17 เส้น"
        )

    if len(horizontal_lines) != 13:
        raise SystemExit(
            "ตรวจพบเส้นแนวนอนไม่ครบ 13 เส้น"
        )

    GLYPH_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    records: list[
        tuple[str, Image.Image]
    ] = []

    top = horizontal_lines[
        SOURCE_ROW_INDEX
    ]

    bottom = horizontal_lines[
        SOURCE_ROW_INDEX + 1
    ]

    for column, character in enumerate(
        CHARACTERS
    ):
        left = vertical_lines[column]
        right = vertical_lines[
            column + 1
        ]

        source_mask = (
            extract_character_mask(
                image,
                left,
                top,
                right,
                bottom,
            )
        )

        glyph = fit_into_16x16(
            source_mask
        )

        output_path = (
            GLYPH_DIR
            / (
                f"{column:02d}_"
                f"u{ord(character):04x}.png"
            )
        )

        glyph.save(output_path)

        records.append(
            (character, glyph)
        )

        print(
            f"{column:02d} "
            f"{character} "
            f"source={source_mask.width}"
            f"x{source_mask.height} "
            f"output={output_path}"
        )

    create_contact_sheet(
        records
    )

    print(
        "\n=== Pixel Font Preview Created ==="
    )

    print(
        f"Glyphs        : {GLYPH_DIR}"
    )

    print(
        f"Contact sheet : {CONTACT_SHEET_PATH}"
    )

    print(
        "ยังไม่มีการแก้ไฟล์เกม"
    )


if __name__ == "__main__":
    main()
