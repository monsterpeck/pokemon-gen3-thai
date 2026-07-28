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
