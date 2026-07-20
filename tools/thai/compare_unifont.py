from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

from PIL import Image, ImageDraw


UNIFONT_DIR = Path.home() / "dev/tools/gba-free-fonts/fonts/Unifont"
FNT_PATH = UNIFONT_DIR / "unifont.fnt"

OUTPUT_DIR = Path("tools/thai/generated/unifont_compare")
CONTACT_SHEET_PATH = OUTPUT_DIR / "contact_sheet.png"

GLYPH_SIZE = 16
PREVIEW_SCALE = 10


@dataclass(frozen=True)
class CharacterSpec:
    character: str
    name: str


@dataclass(frozen=True)
class GlyphMetric:
    codepoint: int
    x: int
    y: int
    width: int
    height: int
    xoffset: int
    yoffset: int
    xadvance: int
    page: int


CHARACTERS = [
    CharacterSpec("ก", "ko_kai"),
    CharacterSpec("ข", "kho_khai"),
    CharacterSpec("ค", "kho_khwai"),
    CharacterSpec("ง", "ngo_ngu"),
    CharacterSpec("จ", "cho_chan"),
    CharacterSpec("า", "sara_aa"),
    CharacterSpec("ิ", "sara_i"),
    CharacterSpec("่", "mai_ek"),
]


CHAR_PATTERN = re.compile(
    r"^char id=(?P<id>\d+)\s+"
    r"x=(?P<x>\d+)\s+"
    r"y=(?P<y>\d+)\s+"
    r"width=(?P<width>\d+)\s+"
    r"height=(?P<height>\d+)\s+"
    r"xoffset=(?P<xoffset>-?\d+)\s+"
    r"yoffset=(?P<yoffset>-?\d+)\s+"
    r"xadvance=(?P<xadvance>-?\d+)\s+"
    r"page=(?P<page>\d+)\s+"
)


def parse_page_files() -> dict[int, Path]:
    page_pattern = re.compile(
        r'^page id=(\d+) file="([^"]+)"$'
    )

    pages: dict[int, Path] = {}

    for line in FNT_PATH.read_text(
        encoding="utf-8"
    ).splitlines():
        match = page_pattern.match(line.strip())

        if match is None:
            continue

        page_id = int(match.group(1))
        filename = match.group(2)

        pages[page_id] = UNIFONT_DIR / filename

    return pages


def parse_metrics() -> dict[int, GlyphMetric]:
    wanted = {
        ord(item.character)
        for item in CHARACTERS
    }

    metrics: dict[int, GlyphMetric] = {}

    for line in FNT_PATH.read_text(
        encoding="utf-8"
    ).splitlines():
        match = CHAR_PATTERN.match(line.strip())

        if match is None:
            continue

        codepoint = int(match.group("id"))

        if codepoint not in wanted:
            continue

        metrics[codepoint] = GlyphMetric(
            codepoint=codepoint,
            x=int(match.group("x")),
            y=int(match.group("y")),
            width=int(match.group("width")),
            height=int(match.group("height")),
            xoffset=int(match.group("xoffset")),
            yoffset=int(match.group("yoffset")),
            xadvance=int(match.group("xadvance")),
            page=int(match.group("page")),
        )

    return metrics


def extract_mask(
    atlas: Image.Image,
    metric: GlyphMetric,
) -> Image.Image:
    crop = atlas.crop(
        (
            metric.x,
            metric.y,
            metric.x + metric.width,
            metric.y + metric.height,
        )
    )

    if crop.mode == "RGBA":
        return crop.getchannel("A")

    if crop.mode == "LA":
        return crop.getchannel("A")

    return crop.convert("L")


def create_normalized_canvas(
    mask: Image.Image,
) -> Image.Image:
    bbox = mask.getbbox()

    if bbox is None:
        return Image.new(
            "L",
            (GLYPH_SIZE, GLYPH_SIZE),
            0,
        )

    cropped = mask.crop(bbox)

    if (
        cropped.width > GLYPH_SIZE - 2
        or cropped.height > GLYPH_SIZE - 2
    ):
        cropped.thumbnail(
            (GLYPH_SIZE - 2, GLYPH_SIZE - 2),
            resample=Image.Resampling.NEAREST,
        )

    canvas = Image.new(
        "L",
        (GLYPH_SIZE, GLYPH_SIZE),
        0,
    )

    target_x = (
        GLYPH_SIZE - cropped.width
    ) // 2

    target_y = (
        GLYPH_SIZE - cropped.height
    ) // 2

    canvas.paste(
        cropped,
        (target_x, target_y),
    )

    return canvas


def create_metric_canvas(
    mask: Image.Image,
    metric: GlyphMetric,
) -> Image.Image:
    canvas = Image.new(
        "L",
        (GLYPH_SIZE, GLYPH_SIZE),
        0,
    )

    # ตัวปกติเริ่มใกล้ด้านซ้าย
    # Combining mark ใช้จุดอ้างอิงกลางช่อง
    if metric.xadvance == 0:
        pen_x = 8
    else:
        pen_x = 2

    target_x = pen_x + metric.xoffset
    target_y = metric.yoffset

    canvas.paste(
        mask,
        (target_x, target_y),
        mask,
    )

    return canvas


def enlarge(image: Image.Image) -> Image.Image:
    return image.resize(
        (
            GLYPH_SIZE * PREVIEW_SCALE,
            GLYPH_SIZE * PREVIEW_SCALE,
        ),
        resample=Image.Resampling.NEAREST,
    )


def main() -> None:
    if not FNT_PATH.exists():
        raise SystemExit(
            f"ไม่พบไฟล์: {FNT_PATH}"
        )

    pages = parse_page_files()
    metrics = parse_metrics()

    missing = [
        item.character
        for item in CHARACTERS
        if ord(item.character) not in metrics
    ]

    if missing:
        raise SystemExit(
            "ไม่พบ Metric ของ: "
            + " ".join(missing)
        )

    atlases: dict[int, Image.Image] = {}

    for page_id, path in pages.items():
        if not path.exists():
            raise SystemExit(
                f"ไม่พบ Atlas page {page_id}: {path}"
            )

        atlases[page_id] = Image.open(path)

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    cell_width = 360
    cell_height = 225

    sheet = Image.new(
        "RGB",
        (
            cell_width * 2,
            cell_height * 4,
        ),
        "white",
    )

    draw = ImageDraw.Draw(sheet)

    for index, item in enumerate(CHARACTERS):
        metric = metrics[ord(item.character)]
        atlas = atlases[metric.page]

        mask = extract_mask(
            atlas,
            metric,
        )

        normalized = create_normalized_canvas(mask)
        metric_canvas = create_metric_canvas(
            mask,
            metric,
        )

        normalized_path = (
            OUTPUT_DIR
            / f"{item.name}_normalized.png"
        )

        metric_path = (
            OUTPUT_DIR
            / f"{item.name}_metric.png"
        )

        enlarge(normalized).save(normalized_path)
        enlarge(metric_canvas).save(metric_path)

        column = index % 2
        row = index // 2

        cell_x = column * cell_width
        cell_y = row * cell_height

        sheet.paste(
            enlarge(normalized).convert("RGB"),
            (cell_x + 10, cell_y + 10),
        )

        sheet.paste(
            enlarge(metric_canvas).convert("RGB"),
            (cell_x + 185, cell_y + 10),
        )

        draw.text(
            (cell_x + 10, cell_y + 175),
            (
                f"{item.name}  U+{metric.codepoint:04X}\n"
                f"size={metric.width}x{metric.height}  "
                f"offset=({metric.xoffset},{metric.yoffset})  "
                f"advance={metric.xadvance}"
            ),
            fill="black",
        )

        print(
            f"{item.character} "
            f"U+{metric.codepoint:04X} "
            f"page={metric.page} "
            f"size={metric.width}x{metric.height} "
            f"offset=({metric.xoffset},{metric.yoffset}) "
            f"advance={metric.xadvance}"
        )

    sheet.save(CONTACT_SHEET_PATH)

    print("\n=== Unifont Comparison Created ===")
    print(f"Output folder : {OUTPUT_DIR}")
    print(f"Contact sheet : {CONTACT_SHEET_PATH}")
    print("\nซ้าย = จัดให้อยู่กลางเพื่อดูรูปทรง")
    print("ขวา = วางตาม xoffset/yoffset ของ Unifont")
    print("ยังไม่มีการแก้ไฟล์เกมจริง")


if __name__ == "__main__":
    main()