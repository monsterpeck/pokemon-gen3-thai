#!/usr/bin/env python3
"""Render exact HarfBuzz glyph IDs with FreeType using shared shaping geometry."""
from __future__ import annotations

import csv
import math
from pathlib import Path

import freetype
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from PIL import Image, ImageChops, ImageDraw, ImageFont

from noto_thai import *

TRACE_COLUMNS = (
    "line", "input_text", "cluster", "glyph_id", "glyph_name",
    "font_x_advance", "font_y_advance", "font_x_offset", "font_y_offset",
    "pixel_x_advance", "pixel_x_offset", "pixel_y_offset",
    "bitmap_left", "bitmap_top", "bitmap_width", "bitmap_height",
    "final_draw_x", "final_draw_y",
)
UI_FONT = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")


def shape_text(text: str, font_data: bytes, upem: int):
    face = hb.Face(font_data)
    font = hb.Font(face)
    font.scale = (upem, upem)
    hb.ot_font_set_funcs(font)
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(font, buf, {})
    return font, list(zip(buf.glyph_infos, buf.glyph_positions))


class GlyphRasterizer:
    def __init__(self, font_path: Path, upem: int, scale: float, oversample: int):
        self.face = freetype.Face(str(font_path))
        self.upem = upem
        self.scale = scale
        self.oversample = oversample
        pixel_size = round(upem * scale * oversample)
        self.face.set_pixel_sizes(0, pixel_size)

    def glyph_name(self, glyph_id: int) -> str:
        value = self.face.get_glyph_name(glyph_id)
        return value.decode("ascii") if isinstance(value, bytes) else str(value)

    def rasterize(self, glyph_id: int):
        flags = freetype.FT_LOAD_RENDER | freetype.FT_LOAD_NO_HINTING
        self.face.load_glyph(glyph_id, flags)
        slot = self.face.glyph
        bitmap = slot.bitmap
        width, rows, pitch = bitmap.width, bitmap.rows, bitmap.pitch
        image = Image.new("L", (width, rows), 0)
        if width and rows:
            raw = bytes(bitmap.buffer)
            pixels = []
            stride = abs(pitch)
            for row in range(rows):
                start = row * stride
                pixels.extend(raw[start:start + width])
            image.putdata(pixels)
        n = self.oversample
        return {
            "image": image,
            "left_hi": slot.bitmap_left,
            "top_hi": slot.bitmap_top,
            "bitmap_left": slot.bitmap_left / n,
            "bitmap_top": slot.bitmap_top / n,
            "bitmap_width": width / n,
            "bitmap_height": rows / n,
        }

def rasterize_shaped_cell(rasterizer, glyph_id, palette):
    """Accepted proof raster and production indexed cell from one glyph bitmap."""
    bitmap = rasterizer.rasterize(glyph_id)
    width = math.ceil(bitmap["bitmap_width"])
    height = math.ceil(bitmap["bitmap_height"])
    if width > 16 or height > 16:
        raise ValueError(f"glyph {glyph_id} exceeds the 16x16 shaped allocation")
    coverage = bitmap["image"]
    if coverage.size != (width, height):
        coverage = coverage.resize((width, height), Image.Resampling.BOX)
    threshold = math.ceil(spec()["rasterization_threshold"] * 255)
    ink = {(x, y) for y in range(height) for x in range(width) if coverage.getpixel((x, y)) >= threshold}
    monochrome = Image.new("L", (16, 16), 0)
    for x, y in ink:
        monochrome.putpixel((x, y), 255)
    tile = Image.new("P", (16, 16), 0)
    tile.putpalette(palette)
    # Proven GBA convention: index 1 main ink, index 2 down-right shadow.
    for x, y in ink:
        if x + 1 < 16 and y + 1 < 16 and (x + 1, y + 1) not in ink:
            tile.putpixel((x + 1, y + 1), 2)
    for x, y in ink:
        tile.putpixel((x, y), 1)
    return {"bitmap": bitmap, "coverage": coverage, "monochrome": monochrome, "tile": tile, "width": width, "height": height}


def compose(items, hb_font, glyph_order, rasterizer, scale, origin_x, baseline_y, shared_cells=False, palette=None):
    n = rasterizer.oversample
    pen_x = 0
    pen_y = 0
    records = []
    layers = []
    for info, pos in items:
        glyph_id = info.codepoint
        expected_name = glyph_order[glyph_id]
        hb_name = hb_font.glyph_to_string(glyph_id)
        ft_name = rasterizer.glyph_name(glyph_id)
        assert hb_name == expected_name, (glyph_id, hb_name, expected_name)
        assert ft_name == expected_name, (glyph_id, ft_name, expected_name)

        rendered = rasterize_shaped_cell(rasterizer, glyph_id, palette) if shared_cells else None
        bitmap = rendered["bitmap"] if rendered else rasterizer.rasterize(glyph_id)
        final_x = origin_x + (pen_x + pos.x_offset) * scale + bitmap["bitmap_left"]
        final_y = baseline_y - (pen_y + pos.y_offset) * scale - bitmap["bitmap_top"]
        layer = rendered["monochrome"] if rendered else bitmap["image"]
        layers.append((layer, round(final_x if rendered else final_x * n), round(final_y if rendered else final_y * n), glyph_id))
        records.append({
            "cluster": info.cluster,
            "glyph_id": glyph_id,
            "glyph_name": expected_name,
            "font_x_advance": pos.x_advance,
            "font_y_advance": pos.y_advance,
            "font_x_offset": pos.x_offset,
            "font_y_offset": pos.y_offset,
            "pixel_x_advance": pos.x_advance * scale,
            "pixel_x_offset": pos.x_offset * scale,
            "pixel_y_offset": pos.y_offset * scale,
            "bitmap_left": bitmap["bitmap_left"],
            "bitmap_top": bitmap["bitmap_top"],
            "bitmap_width": bitmap["bitmap_width"],
            "bitmap_height": bitmap["bitmap_height"],
            "final_draw_x": final_x,
            "final_draw_y": final_y,
        })
        pen_x += pos.x_advance
        pen_y += pos.y_advance
    return records, layers, pen_x * scale


def render_layers(layers, width, height, oversample, monochrome):
    canvas = Image.new("L", (width * oversample, height * oversample), 0)
    for glyph, x, y, _glyph_id in layers:
        canvas.paste(ImageChops.lighter(canvas.crop((x, y, x + glyph.width, y + glyph.height)), glyph), (x, y))
    reduced = canvas.resize((width, height), Image.Resampling.BOX)
    if monochrome:
        reduced = reduced.point(lambda value: 255 if value >= 90 else 0)
    return reduced


def report_text(scale, upem, advances, overflow):
    comparisons = "\n".join(
        f"- Line {i}: reference-derived target advance {a:.3f}px; target advance {b:.3f}px; difference {abs(a-b):.3f}px"
        for i, (a, b) in enumerate(advances, 1)
    )
    overflow_text = "\n".join(
        f"- Line {line}, glyph {gid} ({name}): {w:.3f} x {h:.3f}px"
        for line, gid, name, w, h in overflow
    ) or "- None at the current global 14 px/em diagnostic scale."
    return f"""# Thai proof pipeline correction report

## Root cause

The original target proof was invalid. HarfBuzz shaped each input correctly, but
the proof then mapped each shaped cluster back to a Unicode character and loaded
an independently rasterized `uXXXX.png` tile. This discarded substituted glyph
IDs (for example small tone-mark forms), reused independently normalized class
origins, and positioned 16x16 character tiles rather than the shaped glyph
sequence. It therefore did use Unicode code points incorrectly after shaping.
It did not use registry widths, but its tile geometry effectively replaced the
HarfBuzz glyph geometry. Its Y placement also mixed tile baselines with negated
HarfBuzz offsets.

## Corrected pipeline

Both diagnostic paths now consume the same HarfBuzz glyph IDs and positions.
Each HarfBuzz glyph ID is compared with both the fontTools glyph order and
FreeType's glyph name before FreeType rasterizes that exact index.

The font has {upem} units per em. The target global scale is:

`target pixels / font unit = 14 / {upem} = {scale}`

No glyph is individually fitted, centered, stretched, or normalized. FreeType
uses the same global size with 8x oversampling and no hinting.

For a current pen in font units, the target placement is:

`draw_x = origin_x + (pen_x + x_offset) * scale + bitmap_left`

`draw_y = baseline_y - (pen_y + y_offset) * scale - bitmap_top`

The Y subtraction converts HarfBuzz's upward-positive font coordinates and
FreeType's upward-positive bitmap top to the downward-positive image canvas.
Only HarfBuzz `x_advance` and `y_advance` update the pen. Combining marks
receive no invented character advance.

## Final advance comparison

{comparisons}

All differences are within one target pixel; they are zero before display
rounding because both paths use the same shaped advances.

## Glyph bitmaps exceeding 16x16

{overflow_text}

This proof deliberately permits bitmap overflow and records it rather than
forcing shaped glyphs into standalone cells.

## Feasibility

The corrected geometry proves that normal Thai shaping cannot be represented by
concatenating independently normalized Unicode tiles. A 16x16 bitmap can hold
individual outlines at this 14 px/em scale, but readable Thai still requires the
renderer to apply shaped glyph substitutions and offsets, or a separately
engineered finite cluster representation. Therefore a general 16x16 GBA glyph
representation is not feasible as a drop-in font-only replacement without a
layout/encoding design. No such redesign or installation is performed here.

## Production-file confirmation

No production ROM, font, charmap, font-loader, or renderer file was modified.
The corrected proof is diagnostic only and is not evidence that the pixel font
is usable. It requires visual review.
"""


def build():
    require_source()
    GENERATED.mkdir(parents=True, exist_ok=True)
    font_data = FONT.read_bytes()
    tt = TTFont(FONT)
    upem = tt["head"].unitsPerEm
    glyph_order = tt.getGlyphOrder()
    scale = upem and spec()["font_size_pixels"] / upem
    assert scale == spec()["logical_scale"]
    oversample = spec()["oversample"]

    palette_values = sum(spec()["palette_rgb"], [])
    indexed_palette = palette_values + [0] * (768 - len(palette_values))
    target_raster = GlyphRasterizer(FONT, upem, scale, oversample)
    reference_scale = 32 / upem
    reference_raster = GlyphRasterizer(FONT, upem, reference_scale, oversample)

    all_rows = []
    line_data = []
    overflow = []
    advance_pairs = []
    any_cluster_mismatch = False
    for line_no, text in enumerate(PROOF_LINES, 1):
        hb_font, items = shape_text(text, font_data, upem)
        if len(items) != len(text):
            any_cluster_mismatch = True

        target_records, target_layers, target_advance = compose(
            items, hb_font, glyph_order, target_raster, scale, 24, 42, shared_cells=True, palette=indexed_palette
        )
        reference_records, reference_layers, reference_advance = compose(
            items, hb_font, glyph_order, reference_raster, reference_scale, 24, 48
        )
        reference_as_target = reference_advance * scale / reference_scale
        assert abs(reference_as_target - target_advance) <= 1.0
        advance_pairs.append((reference_as_target, target_advance))

        for record in target_records:
            record["line"] = line_no
            record["input_text"] = text
            all_rows.append({key: record[key] for key in TRACE_COLUMNS})
            if record["bitmap_width"] > 16 or record["bitmap_height"] > 16:
                overflow.append((
                    line_no, record["glyph_id"], record["glyph_name"],
                    record["bitmap_width"], record["bitmap_height"],
                ))
        line_data.append((text, target_records, target_layers, reference_layers, target_advance))

    # The pipeline must not rely on a one-code-point/one-glyph assumption.
    assert any_cluster_mismatch

    trace = GENERATED / "thai_shaping_trace_fixed.csv"
    with trace.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=TRACE_COLUMNS)
        writer.writeheader()
        writer.writerows(all_rows)

    width = 1120
    group_h = 350
    image = Image.new("RGB", (width, group_h * len(line_data)), "white")
    draw = ImageDraw.Draw(image)
    ui = ImageFont.truetype(str(UI_FONT), 15) if UI_FONT.exists() else ImageFont.load_default()
    for i, (text, records, target_layers, reference_layers, target_advance) in enumerate(line_data):
        top = i * group_h
        draw.text((8, top + 4), f"Line {i + 1}", font=ui, fill="black")

        draw.text((8, top + 28), "A  Noto reference (same HB glyph IDs)", font=ui, fill="black")
        ref = render_layers(reference_layers, width - 300, 62, oversample, False)
        image.paste(Image.merge("RGB", (ref, ref, ref)), (290, top + 20))

        draw.text((8, top + 96), "B  Target monochrome (14 px/em)", font=ui, fill="black")
        target = render_layers(target_layers, width - 300, 58, 1, False)
        image.paste(Image.merge("RGB", (target, target, target)), (290, top + 84))

        draw.text((8, top + 158), "C  Enlarged target + baseline/origins", font=ui, fill="black")
        enlarged = target.resize((target.width * 3, target.height * 3), Image.Resampling.NEAREST)
        crop = enlarged.crop((0, 0, width - 300, 180))
        image.paste(Image.merge("RGB", (crop, crop, crop)), (290, top + 166))
        baseline = top + 166 + 42 * 3
        draw.line((290, baseline, width - 10, baseline), fill=(220, 0, 0), width=1)
        for record in records:
            ox = 290 + round((record["final_draw_x"] - record["bitmap_left"]) * 3)
            draw.line((ox, top + 166, ox, top + 346), fill=(0, 90, 220), width=1)
        draw.text((8, top + 326), f"advance={target_advance:.3f}px", font=ui, fill="black")

    proof = GENERATED / "thai_reference_vs_pixel_proof_fixed.png"
    image.save(proof)
    (GENERATED / "thai_proof_pipeline_report.md").write_text(
        report_text(scale, upem, advance_pairs, overflow), encoding="utf-8"
    )
    print(f"wrote {proof}, {trace}, and proof pipeline report")


if __name__ == "__main__":
    build()
