# Phase 5 Batch 2B — Party Menu Prompts

Source checkpoint: `2c40f2f0b` on `work/core-ui-inventory`.

## Applied translations

- Party prompts: 49/49.
- Fixed prompts: 40/40.
- Dynamic/control-token prompts: 9/9.
- Multiline prompts: 15.
- Move names `SURF` and `CUT` remain English.
- Dynamic item and move names remain English at runtime.
- Refined after final source-context review: `gText_ReturnToHealingSpot` and `gText_TeachWhichPokemon`.

## Automated QA

- Exact source definitions matched: 49/49.
- Placeholder/control tokens preserved: 9/9.
- Thai precompose shaping: 49/49 passed.
- Runtime width profiles: 49/49 passed.
- Widest expanded line: `gText_ReturnToHealingSpot` at 154/224 px.
- Tightest margin: `gText_NotAble2` with 5 px remaining.
- Normal ROM build: passed.
- Source SHA-256: `c970ef19fdd10e618325b8f170604236caa4eb86e566e77ef9c6598819893059`.
- ROM SHA-256: `bbc18a401f28a6d86fbf3fda0ebf4318989ff305adf1c5aaeeaec282b4858cd9`.
- Reviewed archive SHA-256: `ecc691a04dcf1777859ed0731b315b532c57027e60b4c9ab135c7c0f2bcf039d`.

## Status

All 49 entries are `translated_pending_qa`. Runtime visual evidence is required before any entry is changed to `proof_passed`.

## Shaper verification

```text
Map format       : pokemon-gen3-thai-precompose-full-v1
Glyph count      : 761
Atlas size       : [256, 768]
Start-game       : เ | ริ่ | ม | เ | ก | ม | ส์
Total advance    : 40
RESULT: PRECOMPOSE SHAPER CHECK PASSED
```
