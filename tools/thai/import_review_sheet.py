#!/usr/bin/env python3
"""Validate and optionally import edited Phase 4 target cells into the master."""

from __future__ import annotations

import argparse
from pathlib import Path

from export_review_sheet import (
    REVIEW_PATH,
    SHEET_IDS,
    SHEET_SIZE,
    TARGET_IDS,
    expected_review_sheet,
    glyph_metrics,
    save_recovery,
    target_box,
)
from thai_font import CELL_SIZE, MASTER_PATH, ROOT, load_registry, open_indexed, tile_box


def review_errors(review_path: Path = REVIEW_PATH, master_path: Path = MASTER_PATH) -> list[str]:
    errors = []
    try:
        master = open_indexed(master_path)
        review = open_indexed(review_path)
    except ValueError as error:
        return [str(error)]
    if review.size != SHEET_SIZE:
        return [f"review sheet must be {SHEET_SIZE[0]}x{SHEET_SIZE[1]}, got {review.size[0]}x{review.size[1]}"]
    if review.getpalette() != master.getpalette():
        errors.append("review sheet palette differs from thai_master.png")
    allowed = {0, 1, 2, 3}
    unexpected = set(review.getdata()) - allowed
    if unexpected:
        errors.append(f"review sheet uses unexpected palette indexes {sorted(unexpected)}")
    expected = expected_review_sheet(master)
    target_pixels = set()
    for column in range(len(TARGET_IDS)):
        x0 = column * CELL_SIZE
        target_pixels.update((x, y) for y in range(CELL_SIZE) for x in range(x0, x0 + CELL_SIZE))
    for y in range(review.height):
        for x in range(review.width):
            if (x, y) not in target_pixels and review.getpixel((x, y)) != expected.getpixel((x, y)):
                area = "reference" if y < CELL_SIZE else "guide"
                errors.append(f"{area} cell changed at ({x}, {y}); only target cells may be edited")
                break
        if errors and "cell changed" in errors[-1]:
            break
    registry = {glyph.glyph_id: glyph for glyph in load_registry()}
    for column, glyph_id in enumerate(TARGET_IDS):
        tile = review.crop(target_box(column))
        metrics = glyph_metrics(tile)
        glyph = registry[glyph_id]
        if metrics["bbox"] is None:
            errors.append(f"{glyph.token}: target glyph is blank")
            continue
        # Preposed vowels may overhang their advance by one pixel; clusters may not.
        allowance = 1 if glyph.kind == "vowel" else 0
        if metrics["rightmost"] + 1 > glyph.width + allowance:
            errors.append(
                f"{glyph.token}: rightmost pixel {metrics['rightmost']} exceeds width {glyph.width}"
            )
    return errors


def import_review_sheet(review_path: Path = REVIEW_PATH, master_path: Path = MASTER_PATH, check: bool = False) -> list[int]:
    errors = review_errors(review_path, master_path)
    if errors:
        raise ValueError("\n".join(errors))
    master = open_indexed(master_path)
    review = open_indexed(review_path)
    changed = []
    for column, glyph_id in enumerate(TARGET_IDS):
        edited = review.crop(target_box(column))
        if list(edited.getdata()) != list(master.crop(tile_box(glyph_id)).getdata()):
            changed.append(glyph_id)
    if check:
        return changed
    if changed:
        save_recovery(master)
        for column, glyph_id in enumerate(TARGET_IDS):
            if glyph_id in changed:
                master.paste(review.crop(target_box(column)), tile_box(glyph_id)[:2])
        master.save(master_path, optimize=False)
    return changed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="validate without modifying the master")
    args = parser.parse_args()
    try:
        changed = import_review_sheet(check=args.check)
        action = "would import" if args.check else "imported"
        if changed:
            print(f"{action}: " + ", ".join(f"0x{glyph_id:03X}" for glyph_id in changed))
        else:
            print("review sheet valid; target cells match the master")
        return 0
    except (OSError, ValueError) as error:
        print(f"error: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
