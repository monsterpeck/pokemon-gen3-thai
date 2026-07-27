# Move Description Bulk Translation QA

## Scope

- Inventory rows: 354
- Existing proof-passed rows preserved: 10
- Newly translated rows: 344
- Final status after risk-based visual QA: 354 `proof_passed`

## Automated QA results

- Move IDs, row order, source text, source locations, and mapping locations preserved.
- Only `target_text_th` and `description_status` changed for the 344 pending rows.
- Every description has exactly two non-empty lines.
- UTF-8 without BOM and LF line endings preserved.
- Production Thai precompose glyph map supports every Thai sequence.
- `FONT_NARROW` width passed for every line at the 128 px Move Relearner limit.
- Maximum line width: 126 px (MOVE_TAIL_GLOW).
- Lines at or above 120 px: 11.
- Descriptions containing Latin text, abbreviations, digits, or `/`: 72.
- Required source abbreviations `HP`, `PP`, `EXP`, `TM`, and `HM` are preserved when present.
- Distinct numeric values from each source description are preserved.
- Locked uppercase stat terminology is present in Thai targets.
- All 344 source definitions were applied to `src/data/text/move_descriptions.h`.
- Text outside move-description definitions is unchanged.
- Two pre-existing line-end spaces in the English definitions for `MOVE_HARDEN` and `MOVE_SPIKES` differed from the normalized inventory; only those line-end whitespace differences were accepted by the source guard.

## Final risk-based visual QA

- Full ROM build passed.
- Full ROM SHA-256: `941960ec7f2336c7f99b61cfa8dbb024de49a3a6c3baf98e0eb480b083bf2898`.
- Eight QA ROMs were generated and their checksums verified.
- All 30 highest-risk entries passed manual visual QA.
- Two previously proof-passed control entries also passed.
- `OVERHEAT` and `PSYCHO BOOST` intentionally share a description because their English source text is identical.
- `OUTRAGE`, `PETAL DANCE`, and `THRASH` intentionally share a description because their English source text is identical.
- The 344 new rows qualify as `proof_passed` under the agreed criterion: complete automated QA, successful full ROM build, representative renderer proof, and visual approval of every risk-selected entry.

## Files

- `tools/thai/translation/inventory/move_descriptions.csv`
- `src/data/text/move_descriptions.h`
- `tools/thai/translation/reports/move_descriptions_bulk_344/move_description_bulk_qa.csv`
- `tools/thai/translation/reports/move_descriptions_bulk_344/visual_qa_recommended_30.csv`
- `tools/thai/translation/reports/move_descriptions_bulk_344/source_guard_anomalies.csv`
- `tools/thai/translation/reports/move_descriptions_bulk_344/visual_qa_manifest_32.csv`
- `tools/thai/translation/reports/move_descriptions_bulk_344/visual_qa_results_32.csv`
