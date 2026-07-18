# Thai font engineering report

## Scope and status

This milestone is a font-engineering proof only. It does not modify the text renderer, production font sheet, font loader, charmap, or source strings. No candidate glyph has been installed, and nothing here is production-ready or visually accepted in-game.

## Authoritative design source

- Family/style: Noto Sans Thai Regular
- Source: https://raw.githubusercontent.com/notofonts/noto-fonts/main/hinted/ttf/NotoSansThai/NotoSansThai-Regular.ttf
- SHA-256: `404ddfb5ed0aaa6b6ec8a85700d682978992062d67da93903967b56cbd9a4acc`
- License: SIL Open Font License 1.1
- License source: https://raw.githubusercontent.com/google/fonts/main/ofl/notosansthai/OFL.txt
- License copy: `tools/thai/licenses/OFL-NotoSansThai.txt`

The source TTF is cached at `tools/thai/cache/NotoSansThai-Regular.ttf` and is ignored by Git. Generated indexed tiles are derivative design proofs under the OFL; they are not installed into the game font.

## Raster engineering

The required inventory contains 67 Thai characters: 42 consonants, 22 vowels/marks, and 3 punctuation/symbol characters. Every tile is generated at native 16x16 resolution in indexed mode using only palette indexes 0, 1, and 2. The common raster scale is 14 px from the 1000-unit Noto em (`0.014` target pixels per source unit), rendered at 8x oversampling and reduced by coverage threshold without per-glyph resize, stretch, or compression. Foreground uses index 2; a deterministic one-pixel down-right shadow uses index 1.

The original 20 px experiment was rejected because source ink for wide Thai consonants and tall ascender/descender forms exceeded a 16x16 cell. The coherent 14 px scale and class baselines fit all source ink. Validation draws into a guard-banded canvas before cropping, so clipping checks measure source ink and cannot be fooled by a generated edge shadow.

## Metrics and shaping evidence

`tools/thai/generated/noto_thai_opentype_metrics.json` records source advances, glyph bounds, and GPOS mark-to-base/mark-to-mark anchors. Proposed scaled values and explicit `missing-anchor-evidence` states are in `tools/thai/font/thai_metrics_proposed.csv`; missing evidence is not guessed.

HarfBuzz shapes six proof strings using the pinned TTF. The exact glyph IDs, clusters, source advances/offsets, and scaled target values are recorded in `tools/thai/generated/thai_shaping_trace.csv`. Reference and pixel candidates are compared in `tools/thai/generated/thai_reference_vs_pixel_proof.png`.

## Generated review artifacts

- `tools/thai/generated/noto_rasterized/uXXXX.png`
- `tools/thai/generated/noto_thai_contact_sheet.png`
- `tools/thai/generated/noto_thai_proof.png`
- `tools/thai/generated/noto_thai_opentype_metrics.json`
- `tools/thai/generated/thai_shaping_trace.csv`
- `tools/thai/generated/thai_reference_vs_pixel_proof.png`

## Verification and acceptance boundary

Automated checks cover the pinned source hash and license, complete inventory, 16x16 indexed format and palette indexes, nonblank and unclipped source ink, deterministic raster/proof generation, metric evidence, and forbidden-file immutability. Passing these checks establishes reproducibility only. Pixel quality remains a candidate draft and requires human review plus emulator screenshot confirmation before any install or production claim.
