"""Deterministic contextual variants and 16-pixel Thai cluster fit solver."""
from __future__ import annotations

import hashlib
from collections import defaultdict

from PIL import Image

UPPER_VOWELS = set("ัิีึื็ํ")
TONES = set("่้๊๋์")
LOWER_VOWELS = set("ฺุู")
UPPER_MARKS = UPPER_VOWELS | TONES
VARIANT_ORDER = {
    "normal": 0,
    "upper_clearance_1": 1,
    "upper_clearance_2": 2,
    "compact_upper_mark": 3,
    "compact_upper_mark_high": 4,
    "compact_tone": 5,
    "compact_tone_high": 6,
}


def bbox(tile):
    points = [(x, y) for y in range(16) for x in range(16) if tile.getpixel((x, y))]
    if not points:
        return None
    xs, ys = zip(*points)
    return [min(xs), min(ys), max(xs), max(ys)]


def bitmap_hash(tile):
    return hashlib.sha256(bytes(tile.getdata())).hexdigest()


def shift(tile, dy):
    out = Image.new("P", (16, 16), 0)
    out.putpalette(tile.getpalette())
    if dy:
        out.paste(tile.crop((0, 0, 16, 16 - dy)), (0, dy))
    else:
        out.paste(tile)
    return out


def compact(tile, levels):
    box = bbox(tile)
    if not box or not levels:
        return tile.copy()
    left, top, right, bottom = box
    crop = tile.crop((left, top, right + 1, bottom + 1))
    height = max(1, crop.height - levels)
    reduced = crop.resize((crop.width, height), Image.Resampling.NEAREST)
    out = Image.new("P", (16, 16), 0)
    out.putpalette(tile.getpalette())
    out.paste(reduced, (left, top))
    return out


def variant_tile(tile, variant):
    if variant == "normal":
        return tile.copy()
    if variant == "upper_clearance_1":
        return shift(compact(tile, 1) if bbox(tile) and bbox(tile)[3] - bbox(tile)[1] + 1 >= 12 else tile, 1)
    if variant == "upper_clearance_2":
        return shift(compact(tile, 1), 1) if bbox(tile) and bbox(tile)[3] - bbox(tile)[1] + 1 >= 12 else shift(tile, 2)
    if variant in ("compact_upper_mark", "compact_tone"):
        return compact(tile, 1)
    if variant in ("compact_upper_mark_high", "compact_tone_high"):
        return compact(tile, 2)
    raise ValueError(f"unknown variant {variant}")


def analyze(text, items):
    starts = sorted({info.cluster for info, _ in items})
    result = {}
    for number, start in enumerate(starts):
        end = starts[number + 1] if number + 1 < len(starts) else len(text)
        chars = text[start:end]
        result[start] = {
            "text": chars,
            "unicode_sequence": " ".join(f"U+{ord(ch):04X}" for ch in chars),
            "upper_marks": [ch for ch in chars if ch in UPPER_VOWELS],
            "tones": [ch for ch in chars if ch in TONES],
            "lower_marks": [ch for ch in chars if ch in LOWER_VOWELS],
            "above_count": sum(ch in UPPER_MARKS for ch in chars),
        }
    return result


def clusters(records):
    grouped = defaultdict(list)
    for record in records:
        grouped[record["cluster"]].append(record)
    return [grouped[key] for key in sorted(grouped)]


def role(record):
    if record["is_base"]:
        return "base"
    analysis = record["cluster_analysis"]
    name = record["glyph_name"]
    if analysis["tones"] and any(code in name for code in ("0E48", "0E49", "0E4A", "0E4B", "0E4C")):
        return "tone"
    if analysis["upper_marks"] and record["font_x_advance"] == 0 and record["y_offset"] < 0:
        return "upper"
    if analysis["lower_marks"] and record["font_x_advance"] == 0 and record["y_offset"] >= 0:
        return "lower"
    return "spacing"


def assignments(cluster):
    def make(base="normal", upper="normal", tone="normal", level=0):
        output = []
        for record in cluster:
            kind = role(record)
            variant = base if kind == "base" else upper if kind == "upper" else tone if kind == "tone" else "normal"
            dy = level if kind in ("upper", "tone") and variant != "normal" else 0
            if kind == "lower":
                dy = -1
            output.append((variant, 0, dy))
        return output
    return [
        make(),
        make(base="upper_clearance_1"),
        make(upper="compact_upper_mark", level=1),
        make(tone="compact_tone", level=1),
        make(base="upper_clearance_1", upper="compact_upper_mark", tone="compact_tone", level=1),
        make(base="upper_clearance_2", upper="compact_upper_mark_high", tone="compact_tone_high", level=2),
    ]


def bounds(cluster, selected):
    boxes = []
    for record, (variant, dx, dy) in zip(cluster, selected):
        box = bbox(variant_tile(record["normal_tile"], variant))
        if box:
            boxes.append([record["x_offset"] + dx + box[0], 12 + record["y_offset"] + dy + box[1],
                          record["x_offset"] + dx + box[2], 12 + record["y_offset"] + dy + box[3]])
    return {"top": min((box[1] for box in boxes), default=0),
            "bottom": max((box[3] for box in boxes), default=0), "boxes": boxes}


def fits(cluster, selected):
    extent = bounds(cluster, selected)
    if extent["top"] < 0 or extent["bottom"] > 15:
        return None
    base_boxes, mark_boxes = [], []
    for record, choice in zip(cluster, selected):
        box = bbox(variant_tile(record["normal_tile"], choice[0]))
        if not box:
            continue
        placed = [record["x_offset"] + choice[1] + box[0], 12 + record["y_offset"] + choice[2] + box[1],
                  record["x_offset"] + choice[1] + box[2], 12 + record["y_offset"] + choice[2] + box[3]]
        if role(record) == "base":
            base_boxes.append(placed)
        elif role(record) in ("upper", "tone"):
            mark_boxes.append(placed)
    if any(mark[2] >= base[0] and mark[0] <= base[2] and mark[3] >= base[1] for base in base_boxes for mark in mark_boxes):
        return None
    return extent


def solve(cluster):
    normal = bounds(cluster, assignments(cluster)[0])
    for selected in assignments(cluster):
        final = fits(cluster, selected)
        if final:
            return selected, normal, final
    raise ValueError(f"no permitted cluster fit for {cluster[0]['cluster_analysis']['text']!r}")


def select(records):
    for number, cluster in enumerate(clusters(records)):
        selected, normal, final = solve(cluster)
        for record, (variant, dx, dy) in zip(cluster, selected):
            record.update(selected_variant=variant, contextual_shift_x=dx, contextual_shift_y=dy,
                          cluster_number=number, normal_combined_top=normal["top"],
                          normal_combined_bottom=normal["bottom"], final_combined_top=final["top"],
                          final_combined_bottom=final["bottom"], fit_result="fit")
    return records
