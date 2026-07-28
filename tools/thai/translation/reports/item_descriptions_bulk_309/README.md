# Thai Item Description Bulk Translation — 309

## Result

- String definitions: 310
- Translatable descriptions: 309
- Dummy description: 1 (`sDummyDesc`, `?????`, 68 usages)
- Item usage rows: 377
- String status after translation: 309 `translated_pending_qa`, 1 `not_applicable`
- Usage status after translation: 309 `translated_pending_qa`, 68 `not_applicable`
- Empty Thai targets: 0
- Source symbols missing or duplicated: 0
- Maximum line count: 3
- Conservative width hard limit: 120 px using `gFontNormalLatinGlyphWidths` plus production Thai precompose advances
- Width overflow: 0
- Widest line: 117 px (`sDragonScaleDesc`)
- Unsupported Thai glyph sequences: 0
- Control-code mismatch: 0
- Required HP / PP / EXP / TM / HM abbreviation loss: 0

## Files

- `src/data/text/item_descriptions.h`
- `tools/thai/translation/inventory/item_description_strings.csv`
- `tools/thai/translation/inventory/item_description_usage.csv`
- `tools/thai/translation/reports/item_descriptions_bulk_309/item_description_bulk_qa.csv`
- `tools/thai/translation/reports/item_descriptions_bulk_309/visual_qa_recommended_30.csv`
- `tools/thai/translation/reports/item_descriptions_bulk_309/species_name_reference_review.csv`
- `tools/thai/translation/reports/item_descriptions_bulk_309/proper_name_terminology_review.csv`
- `tools/thai/translation/reports/item_descriptions_bulk_309/source_guard_anomalies.csv`

## Important QA scope

This package is a translation candidate, not a final `proof_passed` result. All 309 real descriptions are marked `translated_pending_qa`.

Species-name candidates were verified against `tools/thai/translation/reference/species_names_th.csv` by SPECIES ID. Seven spellings were corrected to the project reference, and all 18 review rows are now `reference_verified`. The Bag/TM Case UI source was not included in the input archive, so runtime window dimensions still require full-ROM and visual QA. English locations, people, and organizations not covered by the supplied glossary remain listed in `proper_name_terminology_review.csv`.

Before final proof:

1. Species spellings verified 18/18 against `tools/thai/translation/reference/species_names_th.csv`.
2. Apply the package on `work/item-descriptions-bulk-309`.
3. Run `git diff --check` and full ROM build.
4. Test the 30 highest-risk entries from `visual_qa_recommended_30.csv` in the Bag and TM/HM Case screens.
5. Confirm actual runtime width, line spacing, control-code rendering, and mixed Thai/Latin text.

## Translation revision notes

- `sPotionDesc`: ภาพทดสอบ Bag รอบแรกผ่านด้านการแสดงผล แต่ปรับสำนวนเป็น `ฟื้นฟู HP ให้โปเกมอน / ได้ 20 หน่วย`; ต้องทดสอบภาพจาก ROM ที่ Build ใหม่ก่อนเปลี่ยนเป็น `proof_passed`.

## Visual QA progress

- `sPotionDesc` / `POTION`: `proof_passed` after a rebuilt-ROM Bag screenshot confirmed the revised two-line Thai description.
- Remaining risk-selected descriptions: 30 `pending`.
- Current description status: 1 `proof_passed`, 308 `translated_pending_qa`, 1 `not_applicable`.

## Locked terminology policy

- Pokémon names: use the Japanese-reference Thai names from `species_names_th.csv`.
- Person and location names: render in Thai from the English source names.
- Item and move names: keep English.
- General and system terminology: translate to Thai.
- Terminology review: 36 entries updated in Thai and 18 entries verified to remain in English.
- All revised lines passed the current automated width and glyph checks; runtime visual QA remains pending except entries already marked `proof_passed`.
