#!/usr/bin/env python3
"""Create and render the native-resolution Thai Phase 4 review sheet."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw

from thai_font import CELL_SIZE, MASTER_PATH, ROOT, load_registry, open_indexed, tile_box


REVIEW_PATH = ROOT / "tools/thai/font/thai_review_sheet.png"
PREVIEW_PATH = ROOT / "tools/thai/generated/thai_review_sheet_enlarged.png"
COORDINATE_REPORT_PATH = ROOT / "tools/thai/generated/thai_pixel_coordinates.md"
RECOVERY_DIR = ROOT / "tools/thai/font/recovery"
TARGET_IDS = (0x145, 0x146, 0x147)
REFERENCE_IDS = (0x118, 0x136, 0x138, 0x13D)  # ก ม ร ส
SHEET_IDS = TARGET_IDS + REFERENCE_IDS
SHEET_COLUMNS = len(SHEET_IDS)
SHEET_SIZE = (SHEET_COLUMNS * CELL_SIZE, 2 * CELL_SIZE)
SCALE = 12
LABEL_HEIGHT = 34


def copy_cell(source: Image.Image, glyph_id: int, destination: Image.Image, column: int) -> None:
    destination.paste(source.crop(tile_box(glyph_id)), (column * CELL_SIZE, 0))


def draw_native_guides(sheet: Image.Image, column: int) -> None:
    """Draw a palette-only guide cell below each editable/reference source cell."""
    x0 = column * CELL_SIZE
    pixels = sheet.load()
    # Safe bounds x=1..14 and y=1..14.
    for x in range(1, 15):
        pixels[x0 + x, 17] = 1
        pixels[x0 + x, 30] = 1
    for y in range(17, 31):
        pixels[x0 + 1, y] = 1
        pixels[x0 + 14, y] = 1
    # Tone-mark zone y=1..3, upper-vowel zone y=4..6, baseline y=13.
    for x in range(2, 14):
        pixels[x0 + x, 19] = 3
        pixels[x0 + x, 22] = 2
        pixels[x0 + x, 29] = 1


def expected_review_sheet(master: Image.Image) -> Image.Image:
    sheet = Image.new("P", SHEET_SIZE, 0)
    sheet.putpalette(master.getpalette())
    for column, glyph_id in enumerate(SHEET_IDS):
        copy_cell(master, glyph_id, sheet, column)
        draw_native_guides(sheet, column)
    return sheet


def target_box(column: int) -> tuple[int, int, int, int]:
    return column * CELL_SIZE, 0, (column + 1) * CELL_SIZE, CELL_SIZE


def save_recovery(master: Image.Image, recovery_dir: Path = RECOVERY_DIR) -> None:
    recovery_dir.mkdir(parents=True, exist_ok=True)
    master_backup = recovery_dir / "thai_master_before_phase4.png"
    if not master_backup.exists():
        master.save(master_backup, optimize=False)
    registry = {glyph.glyph_id: glyph for glyph in load_registry()}
    for glyph_id in TARGET_IDS:
        path = recovery_dir / f"{glyph_id:04x}_{registry[glyph_id].token.lower()}_draft.png"
        if not path.exists():
            master.crop(tile_box(glyph_id)).save(path, optimize=False)


def non_target_pixels_match(actual: Image.Image, expected: Image.Image) -> bool:
    allowed = set()
    for column in range(len(TARGET_IDS)):
        x0 = column * CELL_SIZE
        allowed.update((x, y) for y in range(CELL_SIZE) for x in range(x0, x0 + CELL_SIZE))
    return all(
        actual.getpixel((x, y)) == expected.getpixel((x, y))
        for y in range(actual.height) for x in range(actual.width)
        if (x, y) not in allowed
    )


def enlarged_preview(review: Image.Image) -> Image.Image:
    width = review.width * SCALE
    height = LABEL_HEIGHT + CELL_SIZE * SCALE
    preview = Image.new("RGB", (width, height), "#20242a")
    draw = ImageDraw.Draw(preview)
    registry = {glyph.glyph_id: glyph for glyph in load_registry()}
    for column, glyph_id in enumerate(SHEET_IDS):
        x0 = column * CELL_SIZE * SCALE
        tile = review.crop(target_box(column)).convert("RGB").resize(
            (CELL_SIZE * SCALE, CELL_SIZE * SCALE), Image.Resampling.NEAREST
        )
        preview.paste(tile, (x0, LABEL_HEIGHT))
        glyph = registry[glyph_id]
        label = f"0x{glyph_id:03X} {glyph.token.replace('THAI_', '')}"
        draw.text((x0 + 3, 3), label[:25], fill="white")
        draw.text((x0 + 3, 17), "TARGET" if glyph_id in TARGET_IDS else "REFERENCE", fill="#ffd166")
        for grid in range(CELL_SIZE + 1):
            position = x0 + grid * SCALE
            draw.line((position, LABEL_HEIGHT, position, height - 1), fill="#4b5563")
        for grid in range(CELL_SIZE + 1):
            position = LABEL_HEIGHT + grid * SCALE
            draw.line((x0, position, x0 + CELL_SIZE * SCALE - 1, position), fill="#4b5563")
        # Visual-only zone overlays. The indexed editable cells are not altered.
        draw.rectangle((x0 + SCALE, LABEL_HEIGHT + SCALE, x0 + 15 * SCALE, LABEL_HEIGHT + 4 * SCALE), outline="#ef476f", width=2)
        draw.rectangle((x0 + SCALE, LABEL_HEIGHT + 4 * SCALE, x0 + 15 * SCALE, LABEL_HEIGHT + 7 * SCALE), outline="#06d6a0", width=2)
        draw.line((x0 + SCALE, LABEL_HEIGHT + 13 * SCALE, x0 + 15 * SCALE, LABEL_HEIGHT + 13 * SCALE), fill="#ffd166", width=3)
        draw.rectangle((x0 + SCALE, LABEL_HEIGHT + SCALE, x0 + 15 * SCALE, LABEL_HEIGHT + 15 * SCALE), outline="#118ab2", width=2)
    return preview


def glyph_metrics(tile: Image.Image, background: int = 0) -> dict[str, object]:
    points = [(x, y) for y in range(CELL_SIZE) for x in range(CELL_SIZE) if tile.getpixel((x, y)) != background]
    if not points:
        return {"bbox": None, "rightmost": None, "topmost": None, "bottommost": None, "recommended_width": None}
    left = min(x for x, _ in points)
    right = max(x for x, _ in points)
    top = min(y for _, y in points)
    bottom = max(y for _, y in points)
    return {
        "bbox": (left, top, right, bottom),
        "rightmost": right,
        "topmost": top,
        "bottommost": bottom,
        "recommended_width": min(CELL_SIZE, right + 1),
    }


def coordinate_report(review: Image.Image) -> str:
    registry = {glyph.glyph_id: glyph for glyph in load_registry()}
    metrics = {
        glyph_id: glyph_metrics(review.crop(target_box(column)))
        for column, glyph_id in enumerate(SHEET_IDS)
    }
    comparison = {0x145: None, 0x146: 0x138, 0x147: 0x13D}
    lines = [
        "# Thai target glyph coordinate report", "",
        "Coordinates are zero-based within each native 16×16 cell.", "",
        "| ID | Token | Display | Bounding box | Rightmost | Topmost | Bottommost | Registry width | Recommended width | Comparison |",
        "|---:|---|---|---|---:|---:|---:|---:|---:|---|",
    ]
    for glyph_id in TARGET_IDS:
        glyph = registry[glyph_id]
        item = metrics[glyph_id]
        base_id = comparison[glyph_id]
        if base_id is None:
            compare_text = "standalone preposed vowel"
        else:
            base = metrics[base_id]
            base_name = registry[base_id].display
            compare_text = (
                f"vs {base_name}: top {item['topmost'] - base['topmost']:+d}, "
                f"bottom {item['bottommost'] - base['bottommost']:+d}, "
                f"right {item['rightmost'] - base['rightmost']:+d}"
            )
        lines.append(
            f"| 0x{glyph_id:03X} | `{glyph.token}` | {glyph.display} | `{item['bbox']}` | "
            f"{item['rightmost']} | {item['topmost']} | {item['bottommost']} | {glyph.width} | "
            f"{item['recommended_width']} | {compare_text} |"
        )
    lines.extend([
        "", "Guide zones used by the enlarged preview:", "",
        "- tone-mark zone: rows 1–3", "- upper-vowel zone: rows 4–6",
        "- baseline: row 13", "- safe bounds: columns/rows 1–14", "",
    ])
    return "\n".join(lines)


def export_review_sheet(
    master_path: Path = MASTER_PATH,
    review_path: Path = REVIEW_PATH,
    preview_path: Path = PREVIEW_PATH,
    report_path: Path = COORDINATE_REPORT_PATH,
    force: bool = False,
) -> None:
    master = open_indexed(master_path)
    expected = expected_review_sheet(master)
    save_recovery(master)
    if review_path.exists() and not force:
        review = open_indexed(review_path)
        if review.size != SHEET_SIZE or review.getpalette() != master.getpalette():
            raise ValueError("existing review sheet has invalid dimensions or palette; use --force only after backing it up")
        if not non_target_pixels_match(review, expected):
            raise ValueError("existing review sheet changed reference or guide cells")
    else:
        review_path.parent.mkdir(parents=True, exist_ok=True)
        expected.save(review_path, optimize=False)
        review = expected
    preview_path.parent.mkdir(parents=True, exist_ok=True)
    enlarged_preview(review).save(preview_path)
    report_path.write_text(coordinate_report(review), encoding="utf-8")
    print(f"editable: {review_path}")
    print(f"preview : {preview_path}")
    print(f"metrics : {report_path}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="replace the editable sheet from the current master")
    args = parser.parse_args()
    try:
        export_review_sheet(force=args.force)
        return 0
    except (OSError, ValueError) as error:
        print(f"error: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
