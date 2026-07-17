from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


FONT_PATH = Path("/mnt/c/Windows/Fonts/leelawad.ttf")
FONT_SHEET_PATH = Path("graphics/fonts/latin_normal.png")

OUTPUT_DIR = Path(
    "tools/thai/generated/consonant_batch"
)

GLYPH_OUTPUT_DIR = OUTPUT_DIR / "glyphs"
CONTACT_SHEET_PATH = OUTPUT_DIR / "contact_sheet.png"
MANIFEST_PATH = OUTPUT_DIR / "manifest.txt"

SOURCE_CANVAS_SIZE = 32
GLYPH_SIZE = 16
PREVIEW_SCALE = 8

FONT_SIZE = 18
THRESHOLD = 128

MAX_WIDTH = 12
MAX_HEIGHT = 14

BACKGROUND = 0
MAIN_STROKE = 1
SHADOW = 2

FIRST_GLYPH_ID = 0x11D


@dataclass(frozen=True)
class ThaiCharacter:
    character: str
    name: str


# ก ข ค ง และ า ทำไปแล้ว จึงไม่อยู่ในรายการนี้
CHARACTERS = [
    ThaiCharacter("จ", "cho_chan"),
    ThaiCharacter("ฉ", "cho_ching"),
    ThaiCharacter("ช", "cho_chang"),
    ThaiCharacter("ซ", "so_so"),
    ThaiCharacter("ฌ", "cho_choe"),
    ThaiCharacter("ญ", "yo_ying"),
    ThaiCharacter("ฎ", "do_chada"),
    ThaiCharacter("ฏ", "to_patak"),
    ThaiCharacter("ฐ", "tho_than"),
    ThaiCharacter("ฑ", "tho_nangmontho"),
    ThaiCharacter("ฒ", "tho_phuthao"),
    ThaiCharacter("ณ", "no_nen"),
    ThaiCharacter("ด", "do_dek"),
    ThaiCharacter("ต", "to_tao"),
    ThaiCharacter("ถ", "tho_thung"),
    ThaiCharacter("ท", "tho_thahan"),
    ThaiCharacter("ธ", "tho_thong"),
    ThaiCharacter("น", "no_nu"),
    ThaiCharacter("บ", "bo_baimai"),
    ThaiCharacter("ป", "po_pla"),
    ThaiCharacter("ผ", "pho_phueng"),
    ThaiCharacter("ฝ", "fo_fa"),
    ThaiCharacter("พ", "pho_phan"),
    ThaiCharacter("ฟ", "fo_fan"),
    ThaiCharacter("ภ", "pho_samphao"),
    ThaiCharacter("ม", "mo_ma"),
    ThaiCharacter("ย", "yo_yak"),
    ThaiCharacter("ร", "ro_ruea"),
    ThaiCharacter("ล", "lo_ling"),
    ThaiCharacter("ว", "wo_waen"),
    ThaiCharacter("ศ", "so_sala"),
    ThaiCharacter("ษ", "so_ruesi"),
    ThaiCharacter("ส", "so_suea"),
    ThaiCharacter("ห", "ho_hip"),
    ThaiCharacter("ฬ", "lo_chula"),
    ThaiCharacter("อ", "o_ang"),
    ThaiCharacter("ฮ", "ho_nokhuk"),
]


def render_character(
    character: str,
    font: ImageFont.FreeTypeFont,
) -> Image.Image:
    source = Image.new(
        mode="L",
        size=(SOURCE_CANVAS_SIZE, SOURCE_CANVAS_SIZE),
        color=0,
    )

    draw = ImageDraw.Draw(source)

    bbox = draw.textbbox(
        (0, 0),
        character,
        font=font,
    )

    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    draw_x = (
        (SOURCE_CANVAS_SIZE - text_width) // 2
        - bbox[0]
    )

    draw_y = (
        (SOURCE_CANVAS_SIZE - text_height) // 2
        - bbox[1]
    )

    draw.text(
        (draw_x, draw_y),
        character,
        font=font,
        fill=255,
    )

    visible_box = source.getbbox()

    if visible_box is None:
        raise RuntimeError(
            f"ไม่สามารถวาดตัวอักษร {character!r}"
        )

    return source.crop(visible_box)


def fit_into_glyph(source: Image.Image) -> Image.Image:
    scale = min(
        MAX_WIDTH / source.width,
        MAX_HEIGHT / source.height,
    )

    new_width = max(
        1,
        round(source.width * scale),
    )

    new_height = max(
        1,
        round(source.height * scale),
    )

    resized = source.resize(
        (new_width, new_height),
        resample=Image.Resampling.LANCZOS,
    )

    glyph = Image.new(
        mode="L",
        size=(GLYPH_SIZE, GLYPH_SIZE),
        color=0,
    )

    target_x = (
        GLYPH_SIZE - new_width
    ) // 2

    target_y = (
        GLYPH_SIZE - new_height
    ) // 2

    glyph.paste(
        resized,
        (target_x, target_y),
    )

    return glyph.point(
        lambda value: (
            255 if value >= THRESHOLD else 0
        )
    )


def create_palette_glyph(
    mask: Image.Image,
    palette: list[int],
) -> Image.Image:
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


def visible_bounds(
    glyph: Image.Image,
) -> tuple[int, int, int, int]:
    positions = [
        (x, y)
        for y in range(GLYPH_SIZE)
        for x in range(GLYPH_SIZE)
        if glyph.getpixel((x, y)) != BACKGROUND
    ]

    if not positions:
        raise RuntimeError(
            "Glyph ไม่มีพิกเซลที่มองเห็น"
        )

    return (
        min(x for x, _ in positions),
        max(x for x, _ in positions),
        min(y for _, y in positions),
        max(y for _, y in positions),
    )


def create_contact_sheet(
    records: list[
        tuple[int, ThaiCharacter, Image.Image]
    ],
) -> None:
    columns = 6
    cell_width = 160
    cell_height = 180

    rows = (
        len(records) + columns - 1
    ) // columns

    sheet = Image.new(
        mode="RGB",
        size=(
            columns * cell_width,
            rows * cell_height,
        ),
        color="white",
    )

    draw = ImageDraw.Draw(sheet)

    for index, (
        glyph_id,
        item,
        glyph,
    ) in enumerate(records):
        column = index % columns
        row = index // columns

        cell_x = column * cell_width
        cell_y = row * cell_height

        enlarged = glyph.convert("RGB").resize(
            (
                GLYPH_SIZE * PREVIEW_SCALE,
                GLYPH_SIZE * PREVIEW_SCALE,
            ),
            resample=Image.Resampling.NEAREST,
        )

        image_x = (
            cell_x
            + (cell_width - enlarged.width) // 2
        )

        sheet.paste(
            enlarged,
            (image_x, cell_y + 5),
        )

        draw.text(
            (cell_x + 8, cell_y + 137),
            (
                f"{item.character}  "
                f"0x{glyph_id:03X}"
            ),
            fill="black",
        )

        draw.text(
            (cell_x + 8, cell_y + 154),
            item.name,
            fill="black",
        )

    CONTACT_SHEET_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    sheet.save(CONTACT_SHEET_PATH)


def main() -> None:
    if not FONT_PATH.exists():
        raise SystemExit(
            f"ไม่พบฟอนต์: {FONT_PATH}"
        )

    if not FONT_SHEET_PATH.exists():
        raise SystemExit(
            f"ไม่พบ Font Sheet: {FONT_SHEET_PATH}"
        )

    font_sheet = Image.open(FONT_SHEET_PATH)

    if font_sheet.mode != "P":
        raise SystemExit(
            "latin_normal.png ต้องเป็นโหมด P"
        )

    palette = font_sheet.getpalette()

    if palette is None:
        raise SystemExit(
            "ไม่พบ Palette ใน latin_normal.png"
        )

    font = ImageFont.truetype(
        str(FONT_PATH),
        FONT_SIZE,
    )

    GLYPH_OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    records: list[
        tuple[int, ThaiCharacter, Image.Image]
    ] = []

    manifest_lines = [
        "# Thai consonant batch preview",
        "# ยังไม่ได้แก้ charmap.txt หรือ src/fonts.c",
        "",
    ]

    for index, item in enumerate(CHARACTERS):
        glyph_id = FIRST_GLYPH_ID + index

        source = render_character(
            item.character,
            font,
        )

        mask = fit_into_glyph(source)

        glyph = create_palette_glyph(
            mask,
            palette,
        )

        output_path = (
            GLYPH_OUTPUT_DIR
            / f"{glyph_id:04X}_{item.name}.png"
        )

        glyph.save(output_path)

        min_x, max_x, min_y, max_y = (
            visible_bounds(glyph)
        )

        suggested_width = max_x + 1

        low_byte = glyph_id & 0xFF

        manifest_lines.append(
            (
                f"{item.character}\t"
                f"0x{glyph_id:03X}\t"
                f"F9 {low_byte:02X}\t"
                f"width={suggested_width}\t"
                f"bounds=X{min_x}-{max_x},"
                f"Y{min_y}-{max_y}\t"
                f"{output_path}"
            )
        )

        records.append(
            (
                glyph_id,
                item,
                glyph,
            )
        )

        print(
            f"{item.character} "
            f"→ 0x{glyph_id:03X} "
            f"→ F9 {low_byte:02X} "
            f"→ width {suggested_width}"
        )

    MANIFEST_PATH.write_text(
        "\n".join(manifest_lines) + "\n",
        encoding="utf-8",
    )

    create_contact_sheet(records)

    print("\n=== Batch Preview Completed ===")
    print(f"Characters    : {len(records)}")
    print(f"Glyph folder  : {GLYPH_OUTPUT_DIR}")
    print(f"Manifest      : {MANIFEST_PATH}")
    print(f"Contact sheet : {CONTACT_SHEET_PATH}")
    print("\nยังไม่มีการแก้ไฟล์เกมจริง")


if __name__ == "__main__":
    main()