# Phase 5 — Core UI Inventory

Generated from production checkpoint `770548dfe`.

## Coverage

- UI areas: 12
- Unique UI text entries: 574
- Usage references: 762
- Window-template entries: 100
- Unresolved text definitions: 0
- Duplicate global definitions: 0
- Batch 1 entries (Main/Option/Start-Save): 130

## Translation status

- `deferred_story`: 8
- `existing_thai_review`: 1
- `not_applicable`: 53
- `pending`: 512

## Scope classes

- `core_ui_label`: 233
- `core_ui_prompt`: 201
- `story_deferred`: 8
- `system_message`: 79
- `technical_not_translatable`: 53

## Current language

- `english`: 520
- `nonlinguistic`: 53
- `thai`: 1

## Entries by UI area

- `BAG`: 42
- `BATTLE_UI`: 16
- `MAIN_MENU`: 92
- `MOVE_UI`: 10
- `OPTION_MENU`: 22
- `PARTY_MENU`: 134
- `PC_STORAGE`: 79
- `POKEDEX`: 63
- `POKENAV`: 34
- `SHOP`: 23
- `START_SAVE`: 33
- `SUMMARY`: 59

## Important limitations

- Battle system narration is intentionally excluded from this Core UI inventory; it belongs to Phase 6 system and variable messages.
- Window widths are outer window sizes only. They are not safe translation limits until text padding, cursor space, icons, alignment, and dynamic values are mapped per printer call.
- Batch 1 is inventory-ready, not translation-ready. The next step is to map exact width/render constraints for Main Menu, Option Menu, and Start/Save before changing source text.

## Existing Thai entry

`gText_MainMenuNewGame` currently contains `เริ่มเกมส์` and is marked `existing_thai_review`; it should be reviewed against the project spelling policy before reuse.

## Batch 1 constraint mapping

- Batch 1 entries mapped: 130/130.
- Constraint profiles used: 26.
- Unresolved constraints: 0.
- First translation pilot: 55 labels.
- Prompt pilot after labels: 22 entries.
- Deferred for Thai input architecture: 49 entries.
- Moved to Phase 6 system messages: 4 entries.
- Exact geometry was verified from source before generating the mapping.

## Pilot labels 55

- Translated labels: 55/55.
- Source shaping: passed for all 55.
- Width and option-group geometry: passed.
- Option value copy buffer: expanded from 16 to 128 bytes because Thai precompose sequences are multi-byte.
- Existing `เริ่มเกมส์` corrected to `เริ่มเกม`.
- Full ROM build: passed.
- Candidate ROM SHA-256: `20c1f4a943a9357f720c7dca6bf77e2f1a86450ac04e8bd266253142fe0b3aa4`.
- Runtime visual QA: pending.

## Pilot prompts 22

- Translated prompts: 22/22.
- Source definitions verified against inventory before replacement.
- Thai shaping, control codes, dynamic placeholders, and line widths: passed.
- `gText_PkmnsNickname` uses the concise title `ตั้งชื่อเล่น?` to avoid collision with maximum-length Pokémon names.
- Shared YES/NO strings remain outside this Batch 1 scope and are not silently modified.
- Full ROM build: passed.
- Candidate ROM SHA-256: `a8c990fd4926dede8ec3fe3e6ff495504b08724e8cdeff172742a02dcf22dc34`.
- Runtime visual QA: pending.

## Birch gender prompt scope correction

- `gText_Birch_BoyOrGirl` was present in the master inventory but was incorrectly classified as `story_deferred` by the generic Birch-speech rule.
- Correct classification: `core_ui_prompt`.
- Batch 1 entries: 131.
- Pilot prompts: 23.
- Translation: `เธอเป็นเด็กชาย? / หรือเป็นเด็กหญิง?`.
- Width check: 74 px and 80 px within the 216 px message box.
- Full ROM build: passed.
- Candidate ROM SHA-256: `9410f8e1de54f3df196093f51574bc4b8861ca2d4ea680d4d57ba4b44dc07139`.
- Runtime visual QA: pending.

## Birch gender prompt visual QA

- Symbol: `gText_Birch_BoyOrGirl`.
- Full ROM build: passed.
- Runtime rendering: passed.
- Translation review: passed.
- Width/layout: passed.
- Thai glyph rendering: passed.
- Final status: `proof_passed`.

## Reviewed pilot visual QA checkpoint

- Scope audit reviewed: 7 deferred-story entries remain story content; 4 transfer messages remain Phase 6 system content; 53 technical/control strings remain not applicable.
- No additional Core UI scope omission was found.
- Screenshot-backed label proofs recorded: 30.
- Screenshot-backed prompt proofs recorded in this checkpoint: 4.
- Previously recorded Birch gender prompt proof retained: 1.
- Total `proof_passed` inventory entries: 35.
- Remaining translated entries awaiting runtime proof: 43.
- ROM rebuild: not required because this checkpoint changes QA metadata only.

## Remaining Core UI gallery QA checkpoint

- ROM 01 prompt gallery pages 01–08: passed.
- ROM 02 V4 Start Menu and direct Safari/Pyramid cycle: passed without Save-screen refresh.
- ROM 03 naming-title gallery: passed.
- Labels `proof_passed`: 52/55.
- Prompts `proof_passed`: 18/23.
- Total Core UI pilot proof: 70/78.
- Remaining visual QA: 8 entries, all accessible from ROM 01 V2.
- ROM rebuild: not required; this checkpoint changes QA metadata only.

## Final prompt gallery visual QA

- Prompt gallery pages 09–13: passed.
- Pilot prompts: 23/23 `proof_passed`.
- Pilot labels: 52/55 `proof_passed`.
- Total Core UI pilot proof: 75/78.
- Remaining visual QA: 3 Main Menu hidden labels.
- ROM rebuild: not required; this checkpoint changes QA metadata only.

## Core UI pilot Batch 1 final checkpoint

- Pilot labels: 55/55 `proof_passed`.
- Pilot prompts: 23/23 `proof_passed`.
- Total translated pilot entries: 78/78 `proof_passed`.
- Automated source, shaping, control-code, width, and ROM build checks: passed.
- Runtime visual QA: passed for every pilot entry.
- Remaining translated entries awaiting proof: 0.
- ROM rebuild: not required; this checkpoint changes QA metadata only.
- This closes Phase 5 Batch 1 only; the remaining Core UI inventory is still pending future batches.

## Phase 5 Batch 2A — Party Menu

- Direct Party labels/actions translated: 26/26.
- Source-definition guards: passed.
- Thai precompose shaping: 26/26 passed.
- Width constraints: 26/26 passed.
- Normal ROM build: passed.
- Runtime visual QA gallery: 6/6 pages passed.
- Visual profiles reviewed: 28/28.
- Batch 2A entries: 26/26 `proof_passed`.
- Deferred Party/Summary stat terms: 9 unchanged.
- This closes Party Menu Batch 2A only; Phase 5 and the full Party Menu inventory remain in progress.

Inventory status after this checkpoint:

- `pending`: 410
- `proof_passed`: 104
- `not_applicable`: 53
- `deferred_story`: 7

## Phase 5 Batch 2B — Party Menu Prompts

- Party prompts: 49/49 `proof_passed`.
- Dynamic/control-token prompts: 9/9 passed.
- Runtime gallery: 14/14 pages passed.
- Full-message renderer origin corrected from x=0 to x=1.
- Full-message effective width: 223 px.
- Normal ROM build after correction: passed.
- Final ROM SHA-256: `9781d48c2f86d132f4c61155c946674a15b1222c1bc4973c7b9b7ac3c36fc9b1`.
- Deferred Party/Summary stat terms: 9 unchanged.
- This closes Party Menu Batch 2B only; Phase 5 remains in progress.

Inventory status after this checkpoint:

- `pending`: 361
- `proof_passed`: 153
- `not_applicable`: 53
- `deferred_story`: 7

## Phase 5 Batch 2C — Party Menu System Messages

- Party system messages translated: 44/44.
- Fixed messages: 13/13.
- Dynamic placeholder messages: 31/31.
- Runtime pages: 50/50.
- Multipage flows: 4/4.
- Runtime visual gallery: 17/17 pages passed.
- Visual profiles: 51/51 passed.
- Shared `gText_WontHaveEffect` Bag/Battle Pyramid route: passed at x=0 with `{CLEAR 1}`.
- Batch 2C entries: 44/44 `proof_passed`.
- Party Menu Batch 2A–2C total: 119 entries closed (26 labels/actions + 49 prompts + 44 system messages).
- Deferred Party/Summary stat terms: 9 unchanged.
- This closes Party Menu Batch 2C, not all remaining Phase 5 inventory.

Inventory status after this checkpoint:

- `pending`: 317
- `proof_passed`: 197
- `not_applicable`: 53
- `deferred_story`: 7
