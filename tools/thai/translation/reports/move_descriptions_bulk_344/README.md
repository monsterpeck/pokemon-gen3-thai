# Move Description Bulk Translation QA

## Scope

- Inventory rows: 354
- Existing proof-passed rows preserved: 10
- Newly translated rows: 344
- Final status: 344 `translated_pending_qa`, 10 `proof_passed`

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

## Visual QA recommendation

- Test the 30 highest-risk entries from `visual_qa_recommended_30.csv`.
- Prioritize lines nearest 128 px, mixed Thai/Latin strings, numbers, and sharp stat changes.
- Keep all 344 new rows as `translated_pending_qa` until the agreed risk-based visual QA and ROM build pass.

## Files

- `tools/thai/translation/inventory/move_descriptions.csv`
- `src/data/text/move_descriptions.h`
- `tools/thai/translation/reports/move_descriptions_bulk_344/move_description_bulk_qa.csv`
- `tools/thai/translation/reports/move_descriptions_bulk_344/visual_qa_recommended_30.csv`
- `tools/thai/translation/reports/move_descriptions_bulk_344/source_guard_anomalies.csv`
