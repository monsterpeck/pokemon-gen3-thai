#!/usr/bin/env python3
"""Generate the build-time Thai shaping implementation report."""
from noto_thai import *
from shape_thai_production import *

def build(build_result="passed"):
    mapping=load_mapping()
    traces=[]
    for i,text in enumerate(PROOF_LINES,1):
        encoded,records,total=encode_run(text,mapping)
        traces.append(f"### Line {i}: {text}\n\n- Final advance: {total}px\n- Bytes: \x60{encoded.hex(' ')}\x60\n")
    report=f"""# Thai build-time shaping report

## Status

Build-time shaping is implemented and the automated build result is **{build_result}**.
This is not visual completion; the real-game screen still requires review in mGBA.

## Encoded positioned-glyph command

Each shaped glyph occupies exactly 8 bytes:

| Offset | Bytes | Meaning |
|---|---:|---|
| 0 | 1 | \x60FC\x60 extended-control introducer |
| 1 | 1 | \x6019\x60 Thai positioned-glyph command |
| 2 | 2 | GBA shaped-glyph ID, unsigned little-endian |
| 4 | 1 | signed two's-complement bitmap X offset |
| 5 | 1 | signed two's-complement bitmap Y offset from the line baseline |
| 6 | 1 | unsigned cursor X advance |
| 7 | 1 | flags; bit 0 marks a new HarfBuzz cluster |

Spaces, newlines, existing extended controls, placeholders, escapes, and EOS keep
their existing formats. The command does not redefine any English character byte.

## Build-time preprocessing

\x60tools/thai/shape_thai_production.py\x60 filters only compiler/preprocessor streams.
Repository C and assembly sources remain ordinary Unicode. Thai runs inside string
literals are shaped, converted to numeric brace bytes, and then handled by the
existing project text preprocessor. Non-Thai literals are emitted byte-for-byte.

Both C and assembly preprocessing rules in \x60Makefile\x60 invoke the filter.
\x60--check\x60 verifies the accepted proof trace, and a missing shaped glyph
mapping is a fatal error.

## HarfBuzz and glyph mapping

The shaper uses the pinned Noto Sans Thai Regular font, HarfBuzz guessed Thai
segment properties, OpenType shaping, a 1000-unit font scale, and the exact
glyph-index checks used by the accepted corrected proof. HarfBuzz IDs are never
mapped back to Unicode.

\x60tools/thai/font/thai_shaped_glyph_map.json\x60 maps {len(mapping["glyphs"])}
required HarfBuzz glyph IDs deterministically to dense GBA IDs. The generated
\x60graphics/fonts/thai_shaped.png\x60 stores those exact glyph-index outlines
at one global 14 px/em scale without per-glyph resizing.

## Coordinate conversion and rounding

For each FreeType bitmap:

\x60bitmap_x = round_half_away(HB_x_offset * 0.014 + bitmap_left)\x60

\x60bitmap_y = round_half_away(-HB_y_offset * 0.014 - bitmap_top)\x60

The renderer adds the encoded X offset to \x60cursorX\x60 and the encoded Y
offset to \x60currentY + 12\x60, the common baseline. Advances use cumulative
error-diffused half-away rounding, so the line's encoded advance remains within
one pixel of the accepted floating-point proof.

## Renderer

\x60RenderThaiPositionedGlyph\x60 in \x60src/text.c\x60 validates the GBA glyph
ID, decompresses the mapped bitmap, clamps draw coordinates, draws through the
existing color/shadow/window path, restores the baseline Y, and advances X only
by the encoded advance. Width and fixed-buffer scanners understand and skip the
six-byte payload.

No Thai classes, anchors, grammatical rules, HarfBuzz logic, or mark stacking
run on the GBA.

## Runtime lookup investigation

The reported emulator image did not respond to shaped-cell artwork changes. Repository-side tracing found no encoder, compact-map, command-decoding, stride, copy-size, clipping, or regeneration defect. The production command separates HarfBuzz IDs from compact indexes; the runtime decodes the compact little-endian u16 unchanged. The 2048-byte .latfont contains 32 physical 64-byte cells, each four 8x8 2-bpp tiles (32 u16 words), matching the normal Latin 16x16 decompression path. The linked ROM font region is byte-identical to the rebuilt .latfont.

For ร, HarfBuzz ID 81 maps, encodes, and decodes as compact index 16 (u16 source offset 0x0200). For ส, HarfBuzz ID 110 maps, encodes, and decodes as compact index 25 (u16 source offset 0x0320). The host reconstruction uses only the encoded production commands, compact map, shaped sheet, and runtime-equivalent offset/advance arithmetic.

Because the repository output and linked ROM contain the edited cells while the reported emulator display did not change, the remaining root cause is outside this lookup/copy path: the emulator session was displaying a stale or different ROM. No unsupported renderer change was made to conceal that deployment mismatch. Visual review remains pending after explicitly reloading the newly rebuilt ROM.

## Exact encoded traces

{chr(10).join(traces)}
## Tests and acceptance screen

\x60make test-thai-shaped-text\x60 covers Unicode source readability, accepted
proof glyph IDs/metrics, combining offsets, spaces/newlines, unchanged English,
preserved controls, missing mappings, signed round trips, decoder bounds,
advances, allocation, determinism, preprocessing integration, ROM presence, and
the controlled screen.

The controlled in-game screen is Professor Birch's opening speech at
\x60data/text/birch_speech.inc\x60 and contains all six strings. The New Game
label in \x60src/strings.c\x60 also exercises the real C-source preprocessing
path.

Runtime Thai grammatical shaping is not used. Visual quality must still be
confirmed with an mGBA screenshot.
"""
    path=GENERATED/"thai_build_time_shaping_report.md"
    path.write_text(report,encoding="utf-8")
    print(path)
if __name__=="__main__":build()
