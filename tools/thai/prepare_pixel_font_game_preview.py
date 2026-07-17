from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw


PROJECT_ROOT = Path(__file__).resolve().parents[2]

SOURCE_DIR = (
    PROJECT_ROOT
    / "tools/thai/generated/pixel_font_preview/glyphs"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "tools/thai/generated/pixel_font_game_preview"
)

GLYPH_OUTPUT_DIR = OUTPUT_DIR / "glyphs"
CONTACT_SHEET_PATH = OUTPUT_DIR / "contact_sheet.png"
MANIFEST_PATH = OUTPUT_DIR / "manifest.txt"

FONT_SHEET_PATH = (
    PROJECT_ROOT
    / "graphics/fonts/latin_normal.png"
)

GLYPH_SIZE = 16
PREVIEW_SCALE = 8

BACKGROUND = 0
MAIN_STROKE = 1
SHADOW = 2


@dataclass(frozen=True)
class GlyphSpec:
    character: str
    name: str
    glyph_id: int
    source_filename: str


GLYPHS = [
    GlyphSpec(
        character="ก",
        name="ko_kai",
        glyph_id=0x118,
        source_filename="00_u0e01.png",
    ),
    GlyphSpec(
        character="ข",
        name="kho_khai",
        glyph_id=0x119,
        source_filename="01_u0e02.png",
    ),
    GlyphSpec(
        character="ค",
        name="kho_khwai",
        glyph_id=0x11A,
        source_filename="03_u0e04.png",
    ),
    GlyphSpec(
        character="ง",
        name="ngo_ngu",
        glyph_id=0x11B,
        source_filename="06_u0e07.png",
    ),
    GlyphSpec(
        character="จ",
        name="cho_chan",
        glyph_id=0x11D,
        source_filename="07_u0e08.png",
    ),
    GlyphSpec(
        character="ฉ",
        name="cho_ching",
        glyph_id=0x11E,
        source_filename="08_u0e09.png",
    ),
]


def load_font_palette() -> list[int]:
    if not FONT_SHEET_PATH.exists():
        raise SystemExit(
            f"ไม่พบ Font Sheet: {FONT_SHEET_PATH}"
        )

    with Image.open(FONT_SHEET_PATH) as font_sheet:
        if font_sheet.mode != "P":
            raise SystemExit(
                "Font Sheet ต้องเป็นโหมด P "
                f"แต่พบ {font_sheet.mode}"
            )

        palette = font_sheet.getpalette()

    if palette is None:
        raise SystemExit(
            "Font Sheet ไม่มีข้อมูล Palette"
        )

    return palette


def convert_to_game_glyph(
    source_path: Path,
    palette: list[int],
) -> Image.Image:
    if not source_path.exists():
        raise SystemExit(
            f"ไม่พบ Glyph ต้นฉบับ: {source_path}"
        )

    with Image.open(source_path) as image:
        source = image.convert("L")

    if source.size != (GLYPH_SIZE, GLYPH_SIZE):
        raise SystemExit(
            f"{source_path.name} ต้องมีขนาด 16x16 "
            f"แต่พบ {source.width}x{source.height}"
        )

    main_pixels: set[tuple[int, int]] = set()

    for y in range(GLYPH_SIZE):
        for x in range(GLYPH_SIZE):
            # Glyph ต้นฉบับเป็นเส้นสีดำบนพื้นขาว
            if source.getpixel((x, y)) < 128:
                main_pixels.add((x, y))

    if not main_pixels:
        raise SystemExit(
            f"{source_path.name} ไม่มีพิกเซลตัวอักษร"
        )

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


def calculate_width(
    glyph: Image.Image,
) -> int:
    _, max_x, _, _ = visible_bounds(glyph)

    # Width ต้องครอบคลุมพิกเซลขวาสุด
    # และเผื่อระยะห่างหนึ่งพิกเซล
    return min(
        GLYPH_SIZE,
        max_x + 2,
    )


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
        tuple[GlyphSpec, Image.Image, int]
    ],
) -> None:
    columns = 6
    cell_width = 155
    cell_height = 185

    sheet = Image.new(
        "RGB",
        (
            columns * cell_width,
            cell_height,
        ),
        "white",
    )

    draw = ImageDraw.Draw(sheet)

    for index, (
        spec,
        glyph,
        width,
    ) in enumerate(records):
        x = index * cell_width
        y = 0

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
                x + 8 + 128,
                y + 8 + 128,
            ),
            outline="gray",
        )

        draw.text(
            (x + 8, y + 142),
            f"U+{ord(spec.character):04X}",
            fill="black",
        )

        draw.text(
            (x + 8, y + 158),
            (
                f"glyph=0x{spec.glyph_id:03X} "
                f"width={width}"
            ),
            fill="black",
        )

    sheet.save(CONTACT_SHEET_PATH)


def main() -> None:
    palette = load_font_palette()

    GLYPH_OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    records: list[
        tuple[GlyphSpec, Image.Image, int]
    ] = []

    manifest_lines = [
        "# character\tglyph_id\twidth\tfilename"
    ]

    for spec in GLYPHS:
        source_path = (
            SOURCE_DIR
            / spec.source_filename
        )

        glyph = convert_to_game_glyph(
            source_path,
            palette,
        )

        width = calculate_width(glyph)

        output_path = (
            GLYPH_OUTPUT_DIR
            / (
                f"{spec.glyph_id:03x}_"
                f"{spec.name}.png"
            )
        )

        glyph.save(output_path)

        records.append(
            (spec, glyph, width)
        )

        manifest_lines.append(
            "\t".join(
                [
                    spec.character,
                    f"0x{spec.glyph_id:03X}",
                    str(width),
                    output_path.name,
                ]
            )
        )

        min_x, max_x, min_y, max_y = (
            visible_bounds(glyph)
        )

        print(
            f"{spec.character} "
            f"glyph=0x{spec.glyph_id:03X} "
            f"bounds=X{min_x}..{max_x},"
            f"Y{min_y}..{max_y} "
            f"width={width}"
        )

    MANIFEST_PATH.write_text(
        "\n".join(manifest_lines) + "\n",
        encoding="utf-8",
    )

    create_contact_sheet(records)

    print(
        "\n=== Game Glyph Preview Created ==="
    )

    print(
        f"Glyphs        : {GLYPH_OUTPUT_DIR}"
    )

    print(
        f"Manifest      : {MANIFEST_PATH}"
    )

    print(
        f"Contact sheet : {CONTACT_SHEET_PATH}"
    )

    print(
        "ยังไม่มีการแก้ Font Sheet หรือ Width Table"
    )


if __name__ == "__main__":
    main()
