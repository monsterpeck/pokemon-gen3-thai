from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


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
    / "tools/thai/generated/font_family_audit"
)

CONTACT_SHEET_PATH = OUTPUT_DIR / "contact_sheet.png"
REPORT_PATH = OUTPUT_DIR / "report.txt"

GLYPH_SIZE = 16
PREVIEW_SCALE = 10

FAMILIES = {
    "top_tall": {
        "label": "ส่วนบนสูง",
        "characters": "ปฝฟ",
    },
    "mid_full": {
        "label": "มวลกลาง",
        "characters": "ผพภม",
    },
    "descender": {
        "label": "ส่วนล่างยาว",
        "characters": "ญฎฏฐ",
    },
    "reference": {
        "label": "ตัวอ้างอิง",
        "characters": "กคดตนบ",
    },
}


@dataclass(frozen=True)
class GlyphRecord:
    character: str
    name: str
    glyph_id: int
    filename: str
    image: Image.Image
    min_x: int
    max_x: int
    min_y: int
    max_y: int

    @property
    def visible_width(self) -> int:
        return self.max_x - self.min_x + 1

    @property
    def visible_height(self) -> int:
        return self.max_y - self.min_y + 1

    @property
    def pixel_count(self) -> int:
        return sum(
            1
            for y in range(GLYPH_SIZE)
            for x in range(GLYPH_SIZE)
            if self.image.getpixel((x, y)) < 128
        )


def parse_manifest() -> dict[str, tuple[str, int, str]]:
    if not SOURCE_MANIFEST.exists():
        raise SystemExit(
            f"ไม่พบ Manifest: {SOURCE_MANIFEST}"
        )

    records: dict[str, tuple[str, int, str]] = {}

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

        character = parts[0]
        name = parts[1]
        glyph_id = int(parts[2], 16)
        filename = parts[6]

        records[character] = (
            name,
            glyph_id,
            filename,
        )

    return records


def visible_bounds(
    image: Image.Image,
) -> tuple[int, int, int, int]:
    positions = [
        (x, y)
        for y in range(GLYPH_SIZE)
        for x in range(GLYPH_SIZE)
        if image.getpixel((x, y)) < 128
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


def load_glyph(
    character: str,
    manifest: dict[str, tuple[str, int, str]],
) -> GlyphRecord:
    if character not in manifest:
        raise SystemExit(
            f"ไม่พบ {character} ใน Manifest"
        )

    name, glyph_id, filename = manifest[character]

    path = SOURCE_DIR / filename

    if not path.exists():
        raise SystemExit(
            f"ไม่พบ Glyph: {path}"
        )

    with Image.open(path) as opened:
        image = opened.convert("L")

    if image.size != (GLYPH_SIZE, GLYPH_SIZE):
        raise SystemExit(
            f"{filename} ไม่ใช่ขนาด 16x16"
        )

    min_x, max_x, min_y, max_y = visible_bounds(image)

    return GlyphRecord(
        character=character,
        name=name,
        glyph_id=glyph_id,
        filename=filename,
        image=image,
        min_x=min_x,
        max_x=max_x,
        min_y=min_y,
        max_y=max_y,
    )


def enlarge(image: Image.Image) -> Image.Image:
    return image.resize(
        (
            GLYPH_SIZE * PREVIEW_SCALE,
            GLYPH_SIZE * PREVIEW_SCALE,
        ),
        resample=Image.Resampling.NEAREST,
    )


def draw_guides(
    preview: Image.Image,
    record: GlyphRecord,
) -> Image.Image:
    result = preview.convert("RGB")
    draw = ImageDraw.Draw(result)

    scale = PREVIEW_SCALE

    # เส้นบนสุดของ Glyph
    draw.line(
        (
            0,
            record.min_y * scale,
            result.width - 1,
            record.min_y * scale,
        ),
        fill=(180, 180, 180),
        width=1,
    )

    # Baseline โดยประมาณที่ y=14
    draw.line(
        (
            0,
            14 * scale,
            result.width - 1,
            14 * scale,
        ),
        fill=(120, 120, 120),
        width=1,
    )

    # กรอบ Bounding Box
    draw.rectangle(
        (
            record.min_x * scale,
            record.min_y * scale,
            (record.max_x + 1) * scale - 1,
            (record.max_y + 1) * scale - 1,
        ),
        outline=(80, 80, 80),
        width=1,
    )

    return result


def create_contact_sheet(
    family_records: dict[str, list[GlyphRecord]],
) -> None:
    max_characters = max(
        len(records)
        for records in family_records.values()
    )

    cell_width = 190
    cell_height = 230
    label_width = 170

    sheet_width = (
        label_width
        + max_characters * cell_width
    )

    sheet_height = (
        len(family_records)
        * cell_height
    )

    sheet = Image.new(
        "RGB",
        (sheet_width, sheet_height),
        "white",
    )

    draw = ImageDraw.Draw(sheet)

    for family_index, (
        family_key,
        records,
    ) in enumerate(family_records.items()):
        y = family_index * cell_height

        family_label = FAMILIES[
            family_key
        ]["label"]

        draw.text(
            (10, y + 20),
            family_key,
            fill="black",
        )

        draw.text(
            (10, y + 42),
            family_label,
            fill="black",
        )

        for index, record in enumerate(records):
            x = label_width + index * cell_width

            preview = draw_guides(
                enlarge(record.image),
                record,
            )

            sheet.paste(
                preview,
                (x + 8, y + 8),
            )

            draw.rectangle(
                (
                    x + 8,
                    y + 8,
                    x + 8 + 160,
                    y + 8 + 160,
                ),
                outline="gray",
            )

            draw.text(
                (x + 8, y + 174),
                (
                    f"{record.character} "
                    f"U+{ord(record.character):04X}"
                ),
                fill="black",
            )

            draw.text(
                (x + 8, y + 192),
                (
                    f"W={record.visible_width} "
                    f"H={record.visible_height} "
                    f"PX={record.pixel_count}"
                ),
                fill="black",
            )

            draw.text(
                (x + 8, y + 208),
                (
                    f"X={record.min_x}..{record.max_x} "
                    f"Y={record.min_y}..{record.max_y}"
                ),
                fill="black",
            )

    sheet.save(CONTACT_SHEET_PATH)


def create_report(
    family_records: dict[str, list[GlyphRecord]],
) -> None:
    lines: list[str] = []

    for family_key, records in family_records.items():
        lines.append(
            f"[{family_key}] "
            f"{FAMILIES[family_key]['label']}"
        )

        for record in records:
            lines.append(
                (
                    f"{record.character} "
                    f"glyph=0x{record.glyph_id:03X} "
                    f"width={record.visible_width} "
                    f"height={record.visible_height} "
                    f"pixels={record.pixel_count} "
                    f"bounds="
                    f"X{record.min_x}..{record.max_x},"
                    f"Y{record.min_y}..{record.max_y}"
                )
            )

        average_width = (
            sum(record.visible_width for record in records)
            / len(records)
        )

        average_height = (
            sum(record.visible_height for record in records)
            / len(records)
        )

        average_pixels = (
            sum(record.pixel_count for record in records)
            / len(records)
        )

        lines.append(
            (
                f"average_width={average_width:.2f} "
                f"average_height={average_height:.2f} "
                f"average_pixels={average_pixels:.2f}"
            )
        )

        lines.append("")

    REPORT_PATH.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def main() -> None:
    manifest = parse_manifest()

    family_records: dict[
        str,
        list[GlyphRecord],
    ] = {}

    for family_key, config in FAMILIES.items():
        family_records[family_key] = [
            load_glyph(character, manifest)
            for character in config["characters"]
        ]

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    create_contact_sheet(family_records)
    create_report(family_records)

    print("=== Thai Font Family Audit ===")
    print(f"Contact sheet : {CONTACT_SHEET_PATH}")
    print(f"Report        : {REPORT_PATH}")
    print("")
    print("ยังไม่มีการแก้ Glyph หรือไฟล์เกม")


if __name__ == "__main__":
    main()
