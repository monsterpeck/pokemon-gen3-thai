from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw


PROJECT_ROOT = Path(__file__).resolve().parents[2]

SOURCE_PATH = (
    PROJECT_ROOT
    / "tools/thai/source/thai_pixel_font_reference.png"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "tools/thai/generated/pixel_consonants"
)

GLYPH_DIR = OUTPUT_DIR / "glyphs"
CONTACT_SHEET_PATH = OUTPUT_DIR / "contact_sheet.png"
MANIFEST_PATH = OUTPUT_DIR / "manifest.txt"

GLYPH_SIZE = 16
PREVIEW_SCALE = 8
CONTACT_COLUMNS = 7

MAX_GLYPH_WIDTH = 12
MAX_GLYPH_HEIGHT = 14
THRESHOLD = 140

# พิกัดเส้นกริดของภาพต้นฉบับ 1024x1536
VERTICAL_LINES = [
    4, 61, 119, 177,
    237, 296, 354, 413,
    472, 532, 592, 653,
    712, 772, 832, 891,
    951,
]

HORIZONTAL_LINES = [
    5, 121, 238, 355,
    472, 589, 701, 821,
    938, 1055, 1186,
    1321, 1450,
]


@dataclass(frozen=True)
class ConsonantSpec:
    character: str
    name: str
    source_row: int
    source_column: int
    glyph_id: int
    mapping: str


# เก็บ Glyph ID เดิมทั้งหมดไว้
# ฆ ซึ่งขาดจากชุดก่อน ใช้ช่องใหม่ 0x142
CONSONANTS = [
    ConsonantSpec("ก", "ko_kai",         6,  0, 0x118, "F9 18"),
    ConsonantSpec("ข", "kho_khai",       6,  1, 0x119, "F9 19"),
    ConsonantSpec("ค", "kho_khwai",      6,  3, 0x11A, "F9 1A"),
    ConsonantSpec("ง", "ngo_ngu",        6,  6, 0x11B, "F9 1B"),

    ConsonantSpec("จ", "cho_chan",       6,  7, 0x11D, "F9 1D"),
    ConsonantSpec("ฉ", "cho_ching",      6,  8, 0x11E, "F9 1E"),
    ConsonantSpec("ช", "cho_chang",      6,  9, 0x11F, "F9 1F"),
    ConsonantSpec("ซ", "so_so",          6, 10, 0x120, "F9 20"),
    ConsonantSpec("ฌ", "cho_choe",       6, 11, 0x121, "F9 21"),
    ConsonantSpec("ญ", "yo_ying",        6, 12, 0x122, "F9 22"),
    ConsonantSpec("ฎ", "do_chada",       6, 13, 0x123, "F9 23"),
    ConsonantSpec("ฏ", "to_patak",       6, 14, 0x124, "F9 24"),
    ConsonantSpec("ฐ", "tho_than",       6, 15, 0x125, "F9 25"),

    ConsonantSpec("ฑ", "tho_nangmontho", 7,  0, 0x126, "F9 26"),
    ConsonantSpec("ฒ", "tho_phuthao",    7,  1, 0x127, "F9 27"),
    ConsonantSpec("ณ", "no_nen",         7,  2, 0x128, "F9 28"),
    ConsonantSpec("ด", "do_dek",         7,  3, 0x129, "F9 29"),
    ConsonantSpec("ต", "to_tao",         7,  4, 0x12A, "F9 2A"),
    ConsonantSpec("ถ", "tho_thung",      7,  5, 0x12B, "F9 2B"),
    ConsonantSpec("ท", "tho_thahan",     7,  6, 0x12C, "F9 2C"),
    ConsonantSpec("ธ", "tho_thong",      7,  7, 0x12D, "F9 2D"),
    ConsonantSpec("น", "no_nu",          7,  8, 0x12E, "F9 2E"),
    ConsonantSpec("บ", "bo_baimai",      7,  9, 0x12F, "F9 2F"),
    ConsonantSpec("ป", "po_pla",         7, 10, 0x130, "F9 30"),
    ConsonantSpec("ผ", "pho_phueng",     7, 11, 0x131, "F9 31"),
    ConsonantSpec("ฝ", "fo_fa",          7, 12, 0x132, "F9 32"),
    ConsonantSpec("พ", "pho_phan",       7, 13, 0x133, "F9 33"),
    ConsonantSpec("ฟ", "fo_fan",         7, 14, 0x134, "F9 34"),
    ConsonantSpec("ภ", "pho_samphao",    7, 15, 0x135, "F9 35"),

    ConsonantSpec("ม", "mo_ma",          8,  0, 0x136, "F9 36"),
    ConsonantSpec("ย", "yo_yak",         8,  1, 0x137, "F9 37"),
    ConsonantSpec("ร", "ro_ruea",        8,  2, 0x138, "F9 38"),
    ConsonantSpec("ล", "lo_ling",        8,  3, 0x139, "F9 39"),
    ConsonantSpec("ว", "wo_waen",        8,  4, 0x13A, "F9 3A"),
    ConsonantSpec("ศ", "so_sala",        8,  5, 0x13B, "F9 3B"),
    ConsonantSpec("ษ", "so_ruesi",       8,  6, 0x13C, "F9 3C"),
    ConsonantSpec("ส", "so_suea",        8,  7, 0x13D, "F9 3D"),
    ConsonantSpec("ห", "ho_hip",         8,  8, 0x13E, "F9 3E"),
    ConsonantSpec("ฬ", "lo_chula",       8,  9, 0x13F, "F9 3F"),
    ConsonantSpec("อ", "o_ang",          8, 10, 0x140, "F9 40"),
    ConsonantSpec("ฮ", "ho_nokhuk",      8, 11, 0x141, "F9 41"),

    ConsonantSpec("ฆ", "kho_rakhang",    6,  5, 0x142, "F9 42"),
]


def extract_mask(
    image: Image.Image,
    row: int,
    column: int,
) -> Image.Image:
    left = VERTICAL_LINES[column]
    right = VERTICAL_LINES[column + 1]

    top = HORIZONTAL_LINES[row]
    bottom = HORIZONTAL_LINES[row + 1]

    cell = image.crop(
        (
            left + 3,
            top + 3,
            right - 2,
            bottom - 2,
        )
    ).convert("L")

    mask = cell.point(
        lambda value: 255 if value < THRESHOLD else 0
    )

    bounds = mask.getbbox()

    if bounds is None:
        raise RuntimeError(
            f"ไม่พบตัวอักษรที่ row={row}, column={column}"
        )

    return mask.crop(bounds)


def fit_into_glyph(source: Image.Image) -> Image.Image:
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

    target_x = (GLYPH_SIZE - width) // 2
    target_y = GLYPH_SIZE - height - 1

    # source เป็นพื้นดำ 0 / ตัวอักษรขาว 255
    # แปลงเป็นตัวอักษรดำบนพื้นขาว
    rendered = resized.point(
        lambda value: 0 if value >= 128 else 255
    )

    glyph.paste(
        rendered,
        (target_x, target_y),
    )

    return glyph


def visible_bounds(
    glyph: Image.Image,
) -> tuple[int, int, int, int]:
    pixels = [
        (x, y)
        for y in range(GLYPH_SIZE)
        for x in range(GLYPH_SIZE)
        if glyph.getpixel((x, y)) < 128
    ]

    if not pixels:
        raise RuntimeError("Glyph ไม่มีพิกเซล")

    return (
        min(x for x, _ in pixels),
        max(x for x, _ in pixels),
        min(y for _, y in pixels),
        max(y for _, y in pixels),
    )


def create_contact_sheet(
    records: list[
        tuple[ConsonantSpec, Image.Image]
    ],
) -> None:
    cell_width = 155
    cell_height = 180

    rows = (
        len(records) + CONTACT_COLUMNS - 1
    ) // CONTACT_COLUMNS

    sheet = Image.new(
        "RGB",
        (
            CONTACT_COLUMNS * cell_width,
            rows * cell_height,
        ),
        "white",
    )

    draw = ImageDraw.Draw(sheet)

    for index, (spec, glyph) in enumerate(records):
        column = index % CONTACT_COLUMNS
        row = index // CONTACT_COLUMNS

        x = column * cell_width
        y = row * cell_height

        preview = glyph.resize(
            (
                GLYPH_SIZE * PREVIEW_SCALE,
                GLYPH_SIZE * PREVIEW_SCALE,
            ),
            resample=Image.Resampling.NEAREST,
        ).convert("RGB")

        sheet.paste(
            preview,
            (x + 8, y + 8),
        )

        draw.rectangle(
            (
                x + 8,
                y + 8,
                x + 136,
                y + 136,
            ),
            outline="gray",
        )

        bounds = visible_bounds(glyph)

        draw.text(
            (x + 8, y + 143),
            (
                f"U+{ord(spec.character):04X} "
                f"glyph=0x{spec.glyph_id:03X}"
            ),
            fill="black",
        )

        draw.text(
            (x + 8, y + 159),
            (
                f"X={bounds[0]}..{bounds[1]} "
                f"Y={bounds[2]}..{bounds[3]}"
            ),
            fill="black",
        )

    sheet.save(CONTACT_SHEET_PATH)


def main() -> None:
    if not SOURCE_PATH.exists():
        raise SystemExit(
            f"ไม่พบภาพต้นฉบับ: {SOURCE_PATH}"
        )

    with Image.open(SOURCE_PATH) as opened:
        image = opened.convert("RGB")

    if image.size != (1024, 1536):
        raise SystemExit(
            "ภาพต้องมีขนาด 1024x1536 "
            f"แต่พบ {image.width}x{image.height}"
        )

    GLYPH_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    records: list[
        tuple[ConsonantSpec, Image.Image]
    ] = []

    manifest_lines = [
        (
            "# character\tname\tglyph_id\tmapping"
            "\tsource_row\tsource_column\tfilename"
        )
    ]

    for spec in CONSONANTS:
        source = extract_mask(
            image,
            spec.source_row,
            spec.source_column,
        )

        glyph = fit_into_glyph(source)

        filename = (
            f"{spec.glyph_id:03x}_"
            f"{spec.name}.png"
        )

        output_path = GLYPH_DIR / filename
        glyph.save(output_path)

        bounds = visible_bounds(glyph)

        manifest_lines.append(
            "\t".join(
                [
                    spec.character,
                    spec.name,
                    f"0x{spec.glyph_id:03X}",
                    spec.mapping,
                    str(spec.source_row),
                    str(spec.source_column),
                    filename,
                ]
            )
        )

        records.append((spec, glyph))

        print(
            f"{spec.character} "
            f"glyph=0x{spec.glyph_id:03X} "
            f"source={source.width}x{source.height} "
            f"bounds=X{bounds[0]}..{bounds[1]},"
            f"Y{bounds[2]}..{bounds[3]}"
        )

    MANIFEST_PATH.write_text(
        "\n".join(manifest_lines) + "\n",
        encoding="utf-8",
    )

    create_contact_sheet(records)

    print("")
    print("=== Pixel Consonants Created ===")
    print(f"Characters    : {len(records)}")
    print(f"Glyphs        : {GLYPH_DIR}")
    print(f"Manifest      : {MANIFEST_PATH}")
    print(f"Contact sheet : {CONTACT_SHEET_PATH}")
    print("")
    print("ยังไม่มีการแก้ Font Sheet หรือไฟล์เกม")


if __name__ == "__main__":
    main()
