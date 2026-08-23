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
| Pokémon | Ability Descriptions | TRANSLATE_REQUIRED | 77 | 77 | 0 | DONE |
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
- Starter / lead-mon / Pokémon nickname species display integration: CLOSED; canonical Species Names remain 386/386 DONE, pending 0. Starter label, `bufferleadmonspeciesname`, and Naming Screen header runtime PASS; this is runtime integration, NOT a translation backlog.
- Trainer Spoken Dialogue: 1633/1633 CLOSED; do not reopen for Trainer Class work.
- Trainer Class Names: 66/66 CLOSED; Battle Intro runtime PASS; PokéNav Match Call and Union Room Trainer Card runtime QA OPTIONAL/WAIVED.
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


## Ability Descriptions — REGISTERED

- User-selected new scope.
- Required real Abilities: 77.
- Existing/closed: 17.
- Pending translation: 60.
- `ABILITY_NONE`: NOT_APPLICABLE.
- Canonical tracker: `batches/phaseF-ability-descriptions-78-canonical-reconcile.csv`.
- `ABILITY` heading: preserve English.
- Ability Names: preserve English.
- Nature Names: preserve English.
- Type Names: out of this scope; do not translate piecemeal.


### Ability Descriptions Batch 01 — CLOSED

- Rows: 15/15.
- Wording: APPROVED 15/15.
- Width/layout: PASS 15/15, 144 px / 1 line, no window resize.
- Injection dry-run: PASS.
- Apply: PASS 15/15.
- Production build: PASS.
- EWRAM: 252772 B / 96.42%.
- IWRAM: 31468 B / 96.03%.
- ROM: 15981646 B / 47.63%.
- Scope total after Batch 01: DONE 17/77, PENDING 60.


### Ability Descriptions Batch 02 — CLOSED

- Rows: 15/15.
- Batch 01 terminology correction: 1/1.
- Terminology gate: PASS.
- Width/layout: PASS 16/16 within existing 144 px / 1-line budget.
- Window resize: NO.
- Apply: PASS 16/16 source changes.
- Production build: PASS.
- EWRAM: 252772 B / 96.42%.
- IWRAM: 31468 B / 96.03%.
- ROM: 15983334 B / 47.63%.
- Scope total: 32/77 DONE, 45 PENDING.
- Remaining 45 approved as one final batch.


### Ability Descriptions — CLOSED 77/77

- Required: 77.
- DONE: 77.
- PENDING: 0.
- Final 45 width/layout: PASS 45/45 within existing 144 px / 1-line window.
- Window resize: NO.
- Production build: PASS.
- EWRAM: 252772 B / 96.42%.
- IWRAM: 31468 B / 96.03%.
- ROM: 15988046 B / 47.65%.
- Runtime Summary QA: PASS (SYNCHRONIZE / SOUNDPROOF sampled).

### Title Screen Translation Credit — CLOSED

- Scope: user-selected Title Screen translation credit.
- Status: DONE / CLOSED.
- Required: 1.
- DONE: 1.
- PENDING: 0.
- Final wording:
  - `Thai by Emu`
  - `เข้าเส้น`
- Runtime implementation:
  - dedicated `graphics/title_screen/thai_credit_banner.png`;
  - 160x32 px total;
  - five 32x32 OBJ sprites;
  - original title-screen blink behavior preserved;
  - original copyright banner preserved;
  - original `graphics/title_screen/press_start.png` unchanged.
- Production build: PASS.
- Final runtime visual QA: PASS.
- Final palette: remapped to the actual runtime Press Start/Copyright OBJ palette.
- Do not reopen absent a new reproducible runtime failure, source/baseline change, or direct contradictory evidence.
