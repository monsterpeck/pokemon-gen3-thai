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
