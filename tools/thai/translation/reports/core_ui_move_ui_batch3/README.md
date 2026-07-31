# Phase 5 Batch 3 — Move UI / Move Relearner

Base checkpoint: `work/core-ui-inventory` at `4e495f6e8`.

## Applied scope

- Symbols: 9/9
- Active usages: 10/10
- Runtime pages: 15/15
- Multipage symbols: 4/4
- Placeholder symbols: 7/7
- Window: `RELEARNERWIN_MSG`, 22×4 tiles, 176×32 px
- Font: `FONT_NORMAL`
- Text origin: x=0, y=1
- Visible lines per page: 2

## Automated result

- Translation review: 9/9 approved
- Source injection: 9/9 passed
- Runtime tokens: 9/9 passed
- Thai shaping: 9/9 passed
- Dynamic expansions: 7/7 passed
- Runtime page layouts: 15/15 passed
- Page-break encoding: 6/6 single-backslash
- Preflight `strings.o`: passed
- Normal ROM build: passed
- ROM SHA-256: `6426edc9cc30e116fa13b946874a59262c1096b3299078cd963d3d466f1d9fe4`
- Widest expanded line: `gText_TeachWhichMoveToPkmn` (134/176 px)
- Tightest remaining margin: `gText_TeachWhichMoveToPkmn` (42 px)

## Inventory after apply

- pending: 308
- translated_pending_qa: 9
- proof_passed: 197
- not_applicable: 53
- deferred_story: 7

Runtime visual QA remains pending for all 9 symbols. Do not promote this batch to `proof_passed` until the visual QA ROM has been reviewed.
