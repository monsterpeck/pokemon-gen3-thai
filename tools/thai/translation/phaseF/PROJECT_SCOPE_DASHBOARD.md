# PekeEmerald Translation Scope Dashboard

> `dialogue_master.csv` (17,250 rows) is a discovery inventory, not the project completion target.
> Future translation waves may select only `TRANSLATE_REQUIRED + PENDING`.

## Authoritative project scope

| Group | Subgroup | Policy | Required | Done | Pending | Status |
|---|---|---|---:|---:|---:|---|
| Moves | Move Names | PRESERVE_EXISTING | - | - | 0 | POLICY_LOCKED |
| Moves | Move Descriptions | TRANSLATE_REQUIRED | 344 | 344 | 0 | DONE |
| Items | Item Names | PRESERVE_EXISTING | - | - | 0 | POLICY_LOCKED |
| Items | Item Descriptions | TRANSLATE_REQUIRED | 309 | 309 | 0 | DONE |
| Contest | Contest Move Names | PRESERVE_EXISTING | - | - | 0 | POLICY_LOCKED |
| Contest | Contest Move/Effect Descriptions | TRANSLATE_REQUIRED | 48 | 48 | 0 | DONE |
| Pokémon | Species Names | COVERED_BY_DEDICATED_TRACKER | 386 | 386 | 0 | DONE |
| Story | Main Story | TRANSLATE_REQUIRED | 191 | 191 | 0 | DONE |
| Trainer | Spoken Trainer Dialogue | TRANSLATE_REQUIRED | 1633 | 1633 | 0 | DONE |
| Trainer | Trainer Class Names | TRANSLATE_REQUIRED | 66 | 66 | 0 | DONE |
| Core UI | Player-facing Core UI | COVERED_BY_DEDICATED_TRACKER | 504 actionable | 504 | 0 | DONE |
| Battle/System | Normal Player-facing Messages | COVERED_BY_DEDICATED_TRACKER | 434 actionable | 434 | 0 | DONE |
| Optional NPC | Optional NPC Dialogue | TRANSLATE_REQUIRED | 1820 | 1820 | 0 | DONE |
| Match Call | Match Call Dialogue / UI | TRANSLATE_REQUIRED | 671 | 671 | 0 | DONE |
| PC / Decoration UI | Decoration Management | TRANSLATE_REQUIRED | 32 | 32 | 0 | DONE |
| Pokédex Core Content | Category + Description | TRANSLATE_REQUIRED | 774 | 774 | 0 | DONE |
| Pokédex Rating | Professor Birch Pokédex evaluation | TRANSLATE_REQUIRED | 23 | 23 | 0 | DONE |
| Shared UI/System Strings | src/strings.c | TRANSLATE_REQUIRED | 28 | 28 | 0 | DONE |
| Birch Lab Menu/UI | National Pokédex upgrade message | TRANSLATE_REQUIRED | 1 | 1 | 0 | DONE |
| Devon Corp 2F Menu/Dialogue | Pokenav dialogue | TRANSLATE_REQUIRED | 3 | 3 | 0 | DONE |
| Mauville Man | Pokédex reader dialogue | TRANSLATE_REQUIRED | 3 | 3 | 0 | DONE |
| Rival House 2F Menu/Dialogue | Rival Pokédex dialogue | TRANSLATE_REQUIRED | 2 | 2 | 0 | DONE |
| Route 104 Rival Dialogue | Rival Pokédex dialogue | TRANSLATE_REQUIRED | 2 | 2 | 0 | DONE |
| Route 105 Dad PokéNav | Dad PokéNav call and registration | TRANSLATE_REQUIRED | 2 | 2 | 0 | DONE |
| Bulk-safe Menu Dialogue | Pokédex / PokéNav player-facing text | TRANSLATE_REQUIRED | 7 | 7 | 0 | DONE |
| Special/UI Menu Text | Match Call / Cycling / PokéNav / Trick House | TRANSLATE_REQUIRED | 4 | 4 | 0 | DONE |
| Final Structured C UI Text | Credits / Trade | TRANSLATE_REQUIRED | 3 | 3 | 0 | DONE |

## Raw inventory cross-reference

| Raw category | Total | Done/Covered | Required Pending | HOLD |
|---|---:|---:|---:|---:|
| system | 6105 | 822 | 0 | 5283 |
| trainer | 3283 | 1634 | 0 | 203 |
| battle | 2652 | 419 | 0 | 2233 |
| optional_npc | 1991 | 1991 | 0 | 0 |
| item | 1068 | 47 | 0 | 1021 |
| menu | 959 | 959 | 0 | 0 |
| match_call | 676 | 676 | 0 | 0 |
| interaction | 197 | 197 | 0 | 0 |
| main_story | 191 | 191 | 0 | 0 |
| sign | 126 | 116 | 0 | 10 |
| tutorial | 2 | 2 | 0 | 0 |

<!-- GROUP7_STATUS_BEGIN -->
## Group 7 — Battle Frontier / Battle Tent

**Status: DONE**

- Explicit facility scope: **1,700**
- Translated / applied / build-closed: **1,610 / 1,610**
- PRESERVE_DATA: **80**
- NOT_APPLICABLE: **10**
- Remaining actionable: **0**
- Batches **01–24 CLOSED**
- Final commit: `ecee9f81a`
- Final build: EWRAM 95.84% / IWRAM 96.03% / ROM 47.52%

> Historical Batch CSVs may still contain their original HOLD metadata.
> They are not authoritative for current Group 7 completion.
<!-- GROUP7_STATUS_END -->

## Runtime Closure Checkpoints — 2026-08-23

- Pokémon Species Names: canonical Thai 386/386 remains CLOSED.
- Battle Healthbox Thai name width: CLOSED at `de5c005f6`; full Thai name + gender runtime PASS.
- Capture / Pokédex direct species-name resolution: CLOSED at `8424a2dc4`; canonical Thai species name runtime PASS.
- Trainer Spoken Dialogue: 1633/1633 CLOSED; do not reopen for Trainer Class work.
- Trainer Class Names: NEW approved scope, 66 entries, 0 DONE / 66 PENDING.
- Trainer individual names: separate OPTIONAL scope; not included in the 66 Trainer Class entries.

<!-- GROUP8_SPECIAL_NPC_STATUS -->
## Group 8 — Special NPC Systems — CLOSED

| Classification | Count |
|---|---:|
| Reconciled rows | 21 |
| TRANSLATE_REQUIRED | 12 |
| Translated / applied / build-passed | 12 |
| PRESERVE_EXISTING | 9 |
| HOLD_FOR_CONTEXT | 0 |
| Unresolved | 0 |
| Pending | 0 |

Production build: **PASS**
- EWRAM: 252516 B / 96.33%
- IWRAM: 31468 B / 96.03%
- ROM: 15979790 B / 47.62%

Runtime QA: **OPTIONAL / WAIVED**
Reopen only the affected player-visible path if a reproducible issue is found later.

Canonical tracker:
`tools/thai/translation/phaseF/batches/phaseF-group8-special-npc-21-canonical-reconcile.csv`

Thai pack:
`tools/thai/translation/phaseF/batches/phaseF-group8-special-npc-actionable-12-thai.csv`
