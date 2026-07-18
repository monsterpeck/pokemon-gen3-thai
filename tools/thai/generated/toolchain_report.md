# Thai toolchain Phase 0–3 report

Date: 2026-07-18
Branch: `thai-toolchain-recovery`
Recovery checkpoint: `7d9c81522`

## Result

The project now has a source-level, build-time Thai localization toolchain. The
original pokeemerald renderer remains clean and unchanged. Multi-codepoint Thai
sequences are encoded by longest match into precomposed glyph tokens; no runtime
combining-mark implementation is used.

Validation, automated tests, `git diff --check`, and the full ROM build pass.
`pokeemerald.gba` was generated successfully.

## Files created

- `tools/thai/README.md`
- `tools/thai/bootstrap_thai_master.py`
- `tools/thai/build_thai_font.py`
- `tools/thai/encode_thai_text.py`
- `tools/thai/scan_thai_clusters.py`
- `tools/thai/thai_font.py`
- `tools/thai/validate_thai_font.py`
- `tools/thai/tests/test_toolchain.py`
- `tools/thai/font/thai_master.png`
- `tools/thai/font/glyph_registry.csv`
- `tools/thai/font/consonant_hashes.csv`
- `tools/thai/generated/thai_contact_sheet.png` (generated, ignored)
- `tools/thai/generated/font_report.txt` (generated, ignored)
- `tools/thai/generated/thai_clusters.csv` (generated, ignored)
- `tools/thai/generated/toolchain_report.md` (this report; generated path is ignored)

## Files modified

- `.gitignore`: ignores future Thai Python cache files.
- `Makefile`: adds `thai-font`, `check-thai-font`, and `test-thai-toolchain`.
- `charmap.txt`: replaces ad hoc prototype aliases with registry-generated tokens.
- `graphics/fonts/latin_normal.png`: deterministically rebuilt from registered
  master cells; all 42 consonant tile pixels are preserved.
- `src/fonts.c`: normalizes the generated width-table row; registered widths retain
  their recovered values.

`src/text.c` and `include/text.h` were not modified. Both matched the clean
pre-combining `develop` baseline before and after the work.

## Experimental and recovery material

No experimental script was deleted or moved. The older `create_*`, `preview_*`,
`prepare_*`, `install_*`, and combining-prototype scripts remain as forensic
recovery material. `tools/thai/README.md` marks them non-production and warns that
the `install_*` scripts directly edit project files.

The 33 committed `*.bak` and `*.before_*` files also remain intact. Cleanup should
occur in a separate reviewed commit after the production master has been manually
validated in-game.

## Registry

- Active entries: 46
- Final entries: 43 (42 consonants plus `sara aa`)
- Draft entries: 3
- Highest allocated ID: `0x147`
- Free contiguous range: `0x148..0x1FF`
- Remaining slots: 184

Rare consonants `ฃ` and `ฅ` remain intentionally unallocated. Canonical lowercase
assets are used for `ค` and `ง`; the distinct uppercase filename variants remain
only as legacy recovery evidence.

## Supported prototype clusters

- `เ` → `{THAI_SARA_E}` / `0x145`
- `ริ่` → `{THAI_RO_RUEA_SARA_I_MAI_EK}` / `0x146`
- `ส์` → `{THAI_SO_SUEA_THANTHAKHAT}` / `0x147`

The normal source string `เริ่มเกมส์` encodes to:

`{THAI_SARA_E}{THAI_RO_RUEA_SARA_I_MAI_EK}ม{THAI_SARA_E}กม{THAI_SO_SUEA_THANTHAKHAT}`

Single-codepoint registered consonants remain Unicode characters where possible.
Existing brace constants and C escapes are preserved.

## Verification

- `make thai-font`: pass; second run is idempotent.
- `make check-thai-font`: pass.
- Validator: pass; 46 registered glyphs, 184 free slots.
- `make test-thai-toolchain`: 11 tests passed.
- Corpus scanner: 2 observed clusters, 0 missing in the current prototype source.
- `make -j$(nproc)`: pass.
- ROM output: `pokeemerald.gba` exists.
- `git diff --check`: pass.
- Renderer forbidden-marker scan: pass.
- 42-consonant pixel preservation manifest: pass.

## Known limitations

- The three menu prototype glyphs are status `draft`; their shapes are not claimed
  to be production quality.
- Only clusters currently present in the small prototype corpus are registered.
- Source encoding is an explicit source-level command; broad localization should
  run the scanner and encoder as part of the translation import workflow.
- The normal font has a hard 512-ID limit. Precomposed clusters consume slots.
- Legacy standalone experimental cells `0x143` and `0x144` remain in the live font
  for recovery but are not cluster-registry entries.
- Backup files, tracked historical bytecode, and obsolete scripts require a later
  cleanup commit; they were deliberately preserved in this milestone.

## Exact next step

Open `tools/thai/font/thai_master.png` in an indexed-pixel editor with a visible
16×16 grid. Manually redraw cells `0x145`, `0x146`, and `0x147` at native resolution
using only the existing four palette indexes—do not scale consonant artwork. Test
the three cells in-game on the New Game menu, adjust their registry widths if
needed, then change their registry status from `draft` to `final` and rerun:

```sh
make thai-font
make check-thai-font
make test-thai-toolchain
make -j$(nproc)
```

# Phase 4: production glyph review workflow

Date: 2026-07-18

## Status gates

- **Toolchain complete:** Yes. Review export/import, coordinate reporting, normal-source menu encoding, Make targets, tests, validation, and ROM build pass.
- **Glyph artwork draft:** IDs `0x145`, `0x146`, and `0x147` remain `draft` in `glyph_registry.csv`.
- **Glyph artwork reviewed:** No. The enlarged preview has been generated, but no in-game screenshot has been supplied or reviewed.
- **Glyph artwork final:** No. These IDs must not be promoted to `final` until manual pixel editing and in-game screenshot review are complete.

## Phase 4 files

- `tools/thai/font/thai_review_sheet.png`: editable indexed 112×32 sheet containing seven native 16×16 source cells and palette-only guide cells.
- `tools/thai/export_review_sheet.py`: safe export, enlarged preview, recovery files, and coordinate report.
- `tools/thai/import_review_sheet.py`: dimensions, indexed palette, indexes 0–3, reference/guide immutability, target-only edits, nonblank targets, and width validation.
- `tools/thai/generated/thai_review_sheet_enlarged.png`: labeled 12× nearest-neighbor review preview with zone overlays.
- `tools/thai/generated/thai_pixel_coordinates.md`: target metrics and base comparisons.
- `tools/thai/font/recovery/`: original Phase 4 master and three draft target cells.
- `tools/thai/testdata/thai_menu_source.c`: canonical normal-source `_("เริ่มเกมส์")` fixture.
- `tools/thai/test_thai_menu.py`: automatic longest-match encoding and expected-token/residual-cluster checks.
- `tools/thai/tests/test_phase4_review.py`: six Phase 4 workflow tests.
- `make_thai.mk`: Phase 4 Make targets included by the main Makefile.

## Target metrics

- `0x145` เ: bounding box `(5, 4, 7, 14)`, rightmost 7, top 4, bottom 14, recommended width 8; registry width remains 7 with the permitted one-pixel preposed-vowel overhang.
- `0x146` ริ่: bounding box `(4, 0, 12, 15)`, rightmost 12, top 0, bottom 15, recommended width 13; compared with ร it extends one pixel upward.
- `0x147` ส์: bounding box `(4, 0, 12, 15)`, rightmost 12, top 0, bottom 15, recommended width 13; compared with ส it extends one pixel upward.

## Verification

- `git diff --check`: pass.
- `make thai-review-sheet`: pass.
- `make check-thai-review-sheet`: pass; target cells match the master.
- `make test-thai-toolchain`: 17 tests passed.
- `make test-thai-menu`: pass; expected token sequence generated and no unsupported Thai cluster remains.
- `make -j$(nproc)`: pass; `pokeemerald.gba` generated.
- Consonant preservation: the 42-glyph preservation tests pass.
- Renderer: `src/text.c` and `include/text.h` remain unchanged.
- Recovery: `thai_master_before_phase4.png` and `thai_master.png` have identical SHA-256 `49671f038e26388415289d1c77bc8f8f713a9ddacb2d8050a87d6f02fd29653b`.

## Manual review stop point

Open `tools/thai/font/thai_review_sheet.png` in an indexed pixel editor. Edit only row-zero cells 0–2 (IDs `0x145..0x147`) at native 16×16 resolution using palette indexes 0–3. Do not edit the ก/ม/ร/ส references or guide row. Then run `make check-thai-review-sheet`; do not import or change registry status until the edited sheet is deliberately approved. In-game screenshot review is still required before any artwork can be called final.
