# Thai localization toolchain

Production Thai text remains ordinary Unicode in source and is shaped by HarfBuzz during the build. The compiler stream contains explicit positioned-glyph commands consumed by a small renderer decoder; the GBA performs no Thai grammatical shaping. The former runtime combining layer remains only as recovery compatibility code and is not used by build-time-shaped source strings.

## Canonical production sources

- `font/thai_master.png`: indexed 16-column sheet of native 16x16 cells.
- `font/glyph_registry.csv`: glyph allocation, Unicode character, width, status,
  and provenance.
- `font/thai_glyph_metadata.csv`: one class, logical advance, mark offsets, and
  second-level offset for every active Thai glyph.
- `font/thai_base_metrics.csv`: explicit upper, lower, and tone anchors for every
  base consonant.
- `font/consonant_hashes.csv`: preservation hashes for the 42 recovered consonants.
- `generate_thai_metadata.py`: generates the C metadata consumed by the renderer.
- `build_thai_font.py`: deterministically generates the font, widths, and direct
  single-codepoint charmap entries.
- `validate_thai_font.py` and `validate_combining_renderer.py`: validate assets,
  mappings, metadata, source text, and consonant preservation.
- `thai_shaper.py`: host-side reference calculations driven by the same CSV data.

All new artwork must remain indexed, use the existing palette, stay at native
16x16 resolution, and have hard pixel edges. Never resize, stretch, vertically
compress, or algorithmically reshape the preserved consonants.

## Translation and build workflow

Write natural source text directly:

```c
const u8 gText_MainMenuNewGame[] = _("เริ่มเกมส์");
```

Then run:

```sh
make thai-font
make check-thai-font
make test-thai-toolchain
make test-thai-renderer
make test-thai-menu
make -j$(nproc)
```

`make thai-font` regenerates runtime metadata before rebuilding font outputs.
`make check-thai-font` fails if generated metadata or font outputs are stale.

## Build-time shaping and renderer behavior

`shape_thai_text.py` runs before the existing C and assembly text preprocessor. It shapes Thai runs with the pinned Noto font, maps exact HarfBuzz glyph IDs through `font/thai_shaped_glyph_map.json`, and emits `FC 19` positioned-glyph commands. `RenderThaiPositionedGlyph` draws the mapped bitmap at its encoded signed offset and advances only by the encoded advance. Spaces, newlines, controls, colors, shadows, printer speed, and non-Thai paths retain their existing behavior.

Run `make thai-noto-font`, `make test-thai-shaped-text`, and the normal ROM build. A missing shaped glyph mapping fails the build. The Professor Birch opening screen contains the six controlled acceptance strings; visual completion still requires an mGBA screenshot.

## Obsolete recovery workflows

The encoder, cluster scanner, review sheet, and candidate generator are not
production dependencies. Their scripts and tests remain for recovery evidence;
see `archive/experimental/README.md` and `archive/precomposed/tests/`. Do not use
precomposed word/cluster tokens for normal Thai translation.

New vowel and mark artwork remains draft until reviewed in an emulator screenshot.
## Noto Sans Thai font-engineering proofs

The candidate-only engineering pipeline uses Noto Sans Thai Regular from the official Noto Fonts repository. The exact source URL and SHA-256 are pinned in `font/thai_font_spec.json`; the cached TTF is intentionally ignored by Git. `licenses/OFL-NotoSansThai.txt` preserves the SIL Open Font License 1.1 text.

Run `make thai-noto-font`, `make check-thai-noto-font`, and `make thai-noto-proof`. These commands create derivative 16x16 indexed proof tiles, OpenType metric/anchor evidence, a HarfBuzz shaping trace, and comparison images under `tools/thai/generated/`. They do not install or replace any game font glyph. The derivatives remain candidates pending pixel review and in-game screenshot acceptance.
