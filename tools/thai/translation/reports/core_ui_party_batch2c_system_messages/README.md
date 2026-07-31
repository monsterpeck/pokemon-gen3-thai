# Phase 5 Batch 2C — Party Menu System Messages

Source checkpoint: `8a57bc290` on `work/core-ui-inventory`.

## Applied translations

- System messages: 44/44.
- Fixed messages: 13/13.
- Dynamic placeholder messages: 31/31.
- Runtime pages: 50/50.
- Multipage flows: 4/4.
- Final semantic refinements: `gText_CantUseUntilNewBadge`, `gText_PkmnAlreadyKnows`, `gText_PkmnBurnHealed`, `gText_PkmnFriendlyBaseVar2CantFall`, and `gText_PkmnHPRestoredByVar2`.
- Move and item placeholders remain English at runtime.

## Automated QA

- Exact source definitions matched: 44/44.
- Runtime tokens preserved/approved: 44/44.
- Dynamic expansions: 31/31 passed.
- Page-layout tests: 50/50 passed.
- Thai precompose shaping: 44/44 passed.
- Strict width checks: 44/44 passed.
- Widest expanded line: `gText_PkmnFriendlyBaseVar2CantFall` at 152/223 px.
- Tightest margin: `gText_PkmnFriendlyBaseVar2CantFall` with 71 px remaining.
- `gText_WontHaveEffect` uses `{CLEAR 1}` and the stricter 216 px Bag/Pyramid profile.
- Normal ROM build: passed.
- Source SHA-256: `cb0f176c7d68808962ba7713b48e0a8f8930888645e0a1c26f51667f8ad299df`.
- ROM SHA-256: `5e6a746ec6f48fee32a9cec80b7d2002a3bc8263b36fd901fbc4b1e9c5c9a21e`.
- Reviewed archive SHA-256: `bb1e72f9d303a30778e3c6b5be09164b0abdfc89e5da84835fd93980cfd3c925`.

## Status

All 44 entries are `translated_pending_qa`. Runtime visual evidence is required before any entry is changed to `proof_passed`. The shared `gText_WontHaveEffect` route also needs Bag and Battle Pyramid Bag evidence.

## Shaper verification

```text
Map format       : pokemon-gen3-thai-precompose-full-v1
Glyph count      : 761
Atlas size       : [256, 768]
Start-game       : เ | ริ่ | ม | เ | ก | ม | ส์
Total advance    : 40
RESULT: PRECOMPOSE SHAPER CHECK PASSED
```

## Runtime visual QA

- User-confirmed screenshots reviewed: 17/17 gallery pages.
- Party Menu runtime pages: 50/50 passed at 224 px with x=1 (223 px effective text area).
- Shared Bag/Battle Pyramid profile: X01 passed at 216 px with x=0 and the approved `{CLEAR 1}` inset.
- Visual profiles: 51/51 passed.
- Unique system-message symbols: 44/44 `proof_passed`.
- Dynamic placeholder messages: 31/31 displayed correctly.
- Multipage flows: 4/4 displayed across all 10 runtime pages.
- No clipping, overflow, broken glyphs, or overlapping Thai vowels/tone marks were found.
- Decorative border/tile artifacts outside some QA text windows are temporary gallery-harness artifacts; they did not overlap or invalidate the tested text.
- This closes Party Menu Batch 2C only.
