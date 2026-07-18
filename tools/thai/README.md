# Thai localization toolchain

This toolchain performs Thai shaping at build time and keeps pokeemerald's original
text renderer. A longest-match encoder replaces registered multi-codepoint clusters
with charmap tokens whose glyphs are already composed on a 16×16 pixel grid.

Runtime combining was rejected because it adds fragile cursor and base-glyph state
to several mature text-printer paths. Do not add Thai state to `src/text.c` or
`include/text.h`.

## Canonical sources

- `font/thai_master.png`: indexed 16-column sheet of 16×16 cells; cell number is
  the glyph ID. Edit indexed pixels only. Never rescale or change the palette.
- `font/glyph_registry.csv`: glyph ID, token, Unicode display sequence, type,
  width, status, and provenance.
- `font/consonant_hashes.csv`: preservation hashes for the 42 recovered consonants.
- `build_thai_font.py`: injects master cells and generates widths/charmap constants.
- `validate_thai_font.py`: validates assets, integration, and renderer cleanliness.
- `encode_thai_text.py`: encodes Thai inside C strings wrapped by `_()`.
- `scan_thai_clusters.py`: ranks registered and missing source-text clusters.

Older creation, preview, installation, and combining-prototype scripts remain in
`tools/thai/` as recovery evidence. Production tools do not import them. Do not run
the direct-edit `install_*` scripts without reviewing them and taking a checkpoint.

## Add or edit a glyph

1. Run `python3 -B tools/thai/scan_thai_clusters.py` and prioritize frequent gaps.
2. Allocate a free `0x000..0x1FF` ID in `glyph_registry.csv` with a unique token and
   exact Unicode sequence.
3. Draw the precomposed glyph by hand in that master-sheet cell. Preserve indexed
   mode, palette, dimensions, and hard edges; do not vertically rescale consonants.
4. Run `make thai-font`, `make check-thai-font`, and `make test-thai-toolchain`.

`bootstrap_thai_master.py` is a recovery-only utility. It re-extracts registered
cells from the live font and would overwrite manual master edits.

## Encode and build

```sh
python3 -B tools/thai/encode_thai_text.py --text 'เริ่มเกมส์'
python3 -B tools/thai/encode_thai_text.py --dry-run src/strings.c
python3 -B tools/thai/encode_thai_text.py src/input.c --output /tmp/input.c
make thai-font
make check-thai-font
make test-thai-toolchain
make -j$(nproc)
```

`--check` fails if wrapped C strings retain encodable clusters. Existing brace
constants, C escapes, and non-Thai strings are preserved. Unsupported Thai marks
or clusters fail with a source offset and code point; there is no runtime fallback.

## Limits and expansion

The normal font has 512 IDs. Every precomposed cluster consumes one, so corpus
frequency must drive allocation. The current draft entries support the menu
prototype; production work must redraw and validate them in-game before marking
them final.

If the table fills, add a bounded second font page selected by build-time token
metadata. Do not respond by adding general runtime combining or ROM hex patches.
