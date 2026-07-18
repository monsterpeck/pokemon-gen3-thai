# Thai localization toolchain

Production Thai text uses literal, single-codepoint Unicode mappings and the
combining-mark layer in `src/text.c`. Translators write ordinary Thai inside
`_()` strings. The longest-match/precomposed workflow is obsolete and retained
only as recovery evidence.

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

## Renderer behavior

The renderer tracks the most recent Thai base and its explicit metrics. Upper
and lower vowels, tone marks, thanthakhat, and nikhahit draw relative to that
base with zero logical advance. Sara-am composes nikhahit plus spacing sara-aa.
State resets at spaces, newlines, positioning/control boundaries, font changes,
non-Thai spacing glyphs, printer resets, and end-of-string. An invalid standalone
combining mark remains visible and advances by `THAI_FALLBACK_MARK_ADVANCE`.

English and Japanese continue through the original renderer paths. Thai handling
activates only for registered Thai glyph IDs in `FONT_NORMAL` English-mode text.

## Obsolete recovery workflows

The encoder, cluster scanner, review sheet, and candidate generator are not
production dependencies. Their scripts and tests remain for recovery evidence;
see `archive/experimental/README.md` and `archive/precomposed/tests/`. Do not use
precomposed word/cluster tokens for normal Thai translation.

New vowel and mark artwork remains draft until reviewed in an emulator screenshot.