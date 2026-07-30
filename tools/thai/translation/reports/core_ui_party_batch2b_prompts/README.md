# Phase 5 Batch 2B — Party Menu Prompts

Translation input checkpoint: `9126a0a24` on `work/core-ui-inventory`.

## Final status

- Party prompts: 49/49 `proof_passed`.
- Fixed prompts: 40/40.
- Dynamic/control-token prompts: 9/9.
- Runtime gallery screenshots: 14/14 pages passed.
- Runtime profiles: 8/8 passed.
- Thai shaping and width checks: 49/49 passed.
- Normal ROM build after renderer correction: passed.
- Final ROM SHA-256: `9781d48c2f86d132f4c61155c946674a15b1222c1bc4973c7b9b7ac3c36fc9b1`.

## Renderer correction

The 20 full-message prompts clipped the first Thai glyph at x=0. `PrintMessage` now starts at x=1 while preserving y=1, text speed, NULL callback, zero spacing, the original white/dark-gray/light-gray colors, and the alternate-down-arrow reset. The effective full-message text width is 223 px.

## Final width evidence

- Widest expanded line: `gText_ReturnToHealingSpot` at 154/223 px.
- Tightest margin: `gText_NotAble2` with 5 px remaining.
- V3 pages 01-07 passed and are unaffected by the full-message renderer correction.
- V5 pages 08-14 passed with the exact x=1 candidate used by the final source.

## Shaper verification

```text
Map format       : pokemon-gen3-thai-precompose-full-v1
Glyph count      : 761
Atlas size       : [256, 768]
Start-game       : เ | ริ่ | ม | เ | ก | ม | ส์
Total advance    : 40
RESULT: PRECOMPOSE SHAPER CHECK PASSED
```
