# Species Names Cross-reference Report

## Phase A

- Reference rows: 412
- Active species rows: 386
- Reserved rows excluded: 26
- Cross-reference rows generated: 386
- Duplicate Species IDs: 0
- Missing English mappings: 0
- Review rows: 1

## Validation

- PASS: every active reference row has exactly one Internal Species ID / constant mapping.
- PASS: every active reference row has an English runtime-name mapping.
- PASS: SYSTEM_RESERVED rows are excluded.
- PASS: Thai names are copied directly from species_names_th.csv translation_th.
- PASS: Species ID 80 is marked for Review.

## Review Required

- 80 SPECIES_SLOWBRO: SLOWBRO → ヤドラン → ยาโดรัน (NEEDS_REVIEW_GLOSSARY_CHANGE)

Generated deterministically from:

- include/constants/species.h
- src/data/text/species_names.h
- tools/thai/translation/reference/species_names_th.csv

No game source files were modified by this generator.
