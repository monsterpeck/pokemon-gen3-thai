# Thai proof pipeline correction report

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

The font has 1000 units per em. The target global scale is:

`target pixels / font unit = 14 / 1000 = 0.014`

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

- Line 1: reference-derived target advance 48.552px; target advance 48.552px; difference 0.000px
- Line 2: reference-derived target advance 50.372px; target advance 50.372px; difference 0.000px
- Line 3: reference-derived target advance 29.638px; target advance 29.638px; difference 0.000px
- Line 4: reference-derived target advance 49.896px; target advance 49.896px; difference 0.000px
- Line 5: reference-derived target advance 29.778px; target advance 29.778px; difference 0.000px
- Line 6: reference-derived target advance 72.996px; target advance 72.996px; difference 0.000px

All differences are within one target pixel; they are zero before display
rounding because both paths use the same shaped advances.

## Glyph bitmaps exceeding 16x16

- None at the current global 14 px/em diagnostic scale.

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
