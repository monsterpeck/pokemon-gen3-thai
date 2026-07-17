from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw


PROJECT_ROOT = Path(__file__).resolve().parents[2]

SOURCE_DIR = (
    PROJECT_ROOT
    / "tools/thai/generated/pixel_consonants/glyphs"
)

SOURCE_MANIFEST = (
    PROJECT_ROOT
    / "tools/thai/generated/pixel_consonants/manifest.txt"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "tools/thai/generated/pixel_consonants_game"
)

GLYPH_DIR = OUTPUT_DIR / "glyphs"
CONTACT_SHEET_PATH = OUTPUT_DIR / "contact_sheet.png"
MANIFEST_PATH = OUTPUT_DIR / "manifest.txt"

FONT_SHEET_PATH = (
    PROJECT_ROOT
    / "graphics/fonts/latin_normal.png"
)

GLYPH_SIZE = 16
PREVIEW_SCALE = 6
CONTACT_COLUMNS = 7

BACKGROUND = 0
MAIN_STROKE = 1
SHADOW = 2


@dataclass(frozen=True)
class GlyphEntry:
    character: str
    name: str
    glyph_id: int
    mapping: str
    source_filename: str


def parse_manifest() -> list[GlyphEntry]:
    if not SOURCE_MANIFEST.exists():
        raise SystemExit(
            f"ไม่พบ Manifest: {SOURCE_MANIFEST}"
        )

    entries: list[GlyphEntry] = []

    for line_number, raw_line in enumerate(
        SOURCE_MANIFEST.read_text(
            encoding="utf-8"
        ).splitlines(),
        start=1,
    ):
        line = raw_line.strip()

        if not line or line.startswith("#"):
            continue

        parts = line.split("\t")

        if len(parts) != 7:
            raise SystemExit(
                f"Manifest ผิดรูปแบบบรรทัด {line_number}: "
                f"{raw_line}"
            )

        entries.append(
            GlyphEntry(
                character=parts[0],
                name=parts[1],
                glyph_id=int(parts[2], 16),
                mapping=parts[3],
                source_filename=parts[6],
            )
        )

    if not entries:
        raise SystemExit(
            "Manifest ไม่มี Glyph"
        )

    return entries


def load_palette() -> list[int]:
    if not FONT_SHEET_PATH.exists():
        raise SystemExit(
            f"ไม่พบ Font Sheet: {FONT_SHEET_PATH}"
        )

    with Image.open(FONT_SHEET_PATH) as image:
        if image.mode != "P":
            raise SystemExit(
                "latin_normal.png ต้องเป็นโหมด P "
                f"แต่พบ {image.mode}"
            )

        palette = image.getpalette()

    if palette is None:
        raise SystemExit(
            "ไม่พบ Palette"
        )

    return palette


def convert_glyph(
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
            if source.getpixel((x, y)) < 128:
                main_pixels.add((x, y))

    if not main_pixels:
        raise SystemExit(
            f"{source_path.name} ไม่มีพิกเซล"
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
    min_x, max_x, _, _ = visible_bounds(glyph)

    visible_width = max_x - min_x + 1

    # Width ต้องใช้ตำแหน่งพิกเซลขวาสุดจริง
    # เพราะ Renderer ใช้ Width เพื่อเลือกครึ่งซ้าย/ขวาของ Glyph
    width = max_x + 2

    # หลีกเลี่ยงระยะที่กว้างเกินไป
    if visible_width <= 8:
        width = max(width, 9)

    return min(
        GLYPH_SIZE,
        width,
    )


def create_contact_sheet(
    records: list[
        tuple[GlyphEntry, Image.Image, int]
    ],
) -> None:
    cell_width = 125
    cell_height = 145

    rows = (
        len(records)
        + CONTACT_COLUMNS - 1
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

    for index, (
        entry,
        glyph,
        width,
    ) in enumerate(records):
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
                x + 104,
                y + 104,
            ),
            outline="gray",
        )

        draw.text(
            (x + 8, y + 111),
            (
                f"U+{ord(entry.character):04X} "
                f"0x{entry.glyph_id:03X}"
            ),
            fill="black",
        )

        draw.text(
            (x + 8, y + 127),
            f"width={width}",
            fill="black",
        )

    sheet.save(
        CONTACT_SHEET_PATH
    )


def main() -> None:
    entries = parse_manifest()
    palette = load_palette()

    GLYPH_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    records: list[
        tuple[GlyphEntry, Image.Image, int]
    ] = []

    manifest_lines = [
        (
            "# character\tname\tglyph_id"
            "\tmapping\twidth\tfilename"
        )
    ]

    for entry in entries:
        source_path = (
            SOURCE_DIR
            / entry.source_filename
        )

        glyph = convert_glyph(
            source_path,
            palette,
        )

        width = calculate_width(
            glyph
        )

        output_filename = (
            f"{entry.glyph_id:04x}_"
            f"{entry.name}.png"
        )

        output_path = (
            GLYPH_DIR
            / output_filename
        )

        glyph.save(
            output_path
        )

        records.append(
            (entry, glyph, width)
        )

        manifest_lines.append(
            "\t".join(
                [
                    entry.character,
                    entry.name,
                    f"0x{entry.glyph_id:03X}",
                    entry.mapping,
                    str(width),
                    output_filename,
                ]
            )
        )

        bounds = visible_bounds(glyph)

        print(
            f"{entry.character} "
            f"glyph=0x{entry.glyph_id:03X} "
            f"bounds=X{bounds[0]}..{bounds[1]},"
            f"Y{bounds[2]}..{bounds[3]} "
            f"width={width}"
        )

    MANIFEST_PATH.write_text(
        "\n".join(manifest_lines) + "\n",
        encoding="utf-8",
    )

    create_contact_sheet(
        records
    )

    print("")
    print("=== Game Consonants Prepared ===")
    print(f"Characters    : {len(records)}")
    print(f"Glyphs        : {GLYPH_DIR}")
    print(f"Manifest      : {MANIFEST_PATH}")
    print(f"Contact sheet : {CONTACT_SHEET_PATH}")
    print("")
    print("ยังไม่มีการแก้ไฟล์เกม")


if __name__ == "__main__":
    main()
