# PekeEmerald — Runtime / Tooling Troubleshooting Guide

This file is the canonical record of reproducible issues that have already
been root-caused and solved in the PekeEmerald Thai production project.

## Mandatory usage

Before opening a new audit for a runtime/build/tooling problem:

1. Search this guide for the symptom.
2. Reuse a proven fix when the failure matches.
3. Do not reopen a CLOSED issue unless:
   - a new reproducible failure appears,
   - source/baseline changed,
   - or direct contradictory evidence exists.
4. Never introduce structural expansion when a display-only fix is sufficient.

---

# Reusable Thai runtime rules

## R1 — Compact Thai name data is not display text

Thai Pokémon/player names may be stored in compact form.

Never send compact Thai bytes directly to a normal text printer.

Correct pattern:

compact stored name
→ `ThaiShapeCompactName()`
→ sufficiently large display scratch buffer
→ text printer

Do not increase:
- `POKEMON_NAME_LENGTH`
- `struct BoxPokemon`
- save structure

unless a separate structural design explicitly requires it.

---

## R2 — Shaped Thai byte length is not visual width

Never use:

`StringLength(shapedThaiText)`

to calculate UI/window width.

Thai shaped streams use multiple bytes per visible glyph.

Use rendered width:

`GetStringWidth(font, text, spacing)`

then convert pixels to tiles if required.

This rule is especially important for dynamically sized menus.

---

## R3 — Keep shaped Thai out of small vanilla buffers

Examples encountered:

- Pokémon Storage `displayMonName[POKEMON_NAME_LENGTH + 1]`
- Pokémon Storage `displayMonNameText[36]`
- Pokémon Storage `messageText[40]`

These buffers are valid for vanilla/compact data but may be too small for
precomposed/shaped Thai display streams.

Preferred fix:

use a separate display-only scratch buffer, normally in EWRAM.

---

## R4 — Correct EWRAM declaration pattern

Proven project pattern:

`EWRAM_DATA static u8 buffer[...] = {0};`

Do not use:

`static EWRAM_DATA ...`

The latter caused a 512-byte Thai Storage scratch allocation to land in IWRAM.

Observed proof:

Before correction:
- IWRAM: 31,996 B

After correction:
- IWRAM: 31,468 B
- EWRAM increased by exactly 512 B

---

# ISSUE 001 — Pokémon Summary corruption / crash

## Symptom

Pokémon Summary could corrupt visually or crash when displaying Thai
met-location/map-name text.

## Root cause

`BufferMonTrainerMemo()` allocated only 32 bytes for the met-location string.

Thai precomposed location names can require much more display storage.

## Proven fix

Under `THAI_NAMING_PRODUCTION`:

`metLocationString = Alloc(512);`

while retaining the original vanilla allocation outside production mode.

## Proven commit

`58328c027` — `thai: fix Pokemon summary runtime display`

## Do not do

- Do not increase `POKEMON_NAME_LENGTH`.
- Do not change `struct BoxPokemon`.
- Do not reapply the old renderer clipping workaround.
- Do not treat a successful build alone as runtime proof.

## Status

CLOSED / runtime proven.

---

# ISSUE 002 — Pokémon Storage Thai names missing + corrupted UI

## Symptoms

Observed in Pokémon Storage:

- Thai nickname not displayed correctly.
- Default species appeared as `/ABRA`.
- Bottom messages still used `ABRA`.
- Thai nickname could be truncated.
- Pressing A on a Pokémon created a huge white/corrupted action menu.

## Root causes

Several independent display paths were still vanilla.

### A. Nickname display path

Storage used:

`MON_DATA_NICKNAME`
→ `StringGet_Nickname()`
→ printer

without shaping compact Thai names.

### B. Species display path

Storage copied directly from:

`gSpeciesNames[...]`

instead of the Thai-aware helper.

### C. Small vanilla buffers

Storage contained:

- `displayMonName[POKEMON_NAME_LENGTH + 1]`
- `displayMonNameText[36]`
- `messageText[40]`

These must not receive large shaped Thai streams.

### D. Bottom-message placeholder path

Dynamic messages still received the vanilla/compact name rather than the
Thai display name.

### E. Action-menu geometry

The dynamically sized Pokémon action menu used visual text length derived
from `StringLength()`.

For shaped Thai this counted encoded bytes, not visible glyph width.

The resulting width became far too large and corrupted window geometry.

## Proven fix

### Thai nickname

Use:

`IsBoxMonNicknameThai()`
+ `ThaiShapeCompactName()`

into a separate 256-byte EWRAM display scratch buffer.

### Species

Use:

`GetSpeciesNameForDisplay(species)`

instead of direct `gSpeciesNames[...]`.

### Messages

Use separate 256-byte EWRAM scratch buffers for shaped Storage messages
and persistent release-name text.

### Info panel

The panel is only 9 tiles wide.

For Thai nickname display:

- use `FONT_NARROW`
- recover the left margin with x = 0

without changing the window dimensions.

### Action menu

Calculate menu width using:

`GetStringWidth(FONT_NORMAL, menu->text, 0)`

then:

`ceil(pixelWidth / 8)`

and cap text width so the final menu window remains inside the valid
horizontal area.

## Structural changes intentionally avoided

Unchanged:

- save format
- `struct BoxPokemon`
- `POKEMON_NAME_LENGTH`
- renderer
- Pokémon Storage window dimensions

## Runtime proof

Verified:

- custom Thai nickname displays correctly
- `/เคซี` replaces `/ABRA`
- bottom messages use Thai display names
- action menu returns to normal geometry
- repeated Storage navigation no longer corrupts the screen

Final build metrics:

- EWRAM: 252260 B / 96.23%
- IWRAM: 31468 B / 96.03%
- ROM: 15974646 B / 47.61%

## Status

CLOSED / runtime proven.
Proven commit: `6ac3327a5` — `thai: fix Pokemon Storage display runtime`.

---

# ISSUE 003 — Injector `source target missing` after source-line drift

## Symptom

Injector dry-run failed with:

`source target missing`

even though the label still existed in source.

Example:

`LilycoveCity_ContestHall_Text_NeverWonBattleButContest`

was currently at line 391 while historical metadata still pointed to line 466.

## Root cause

`source_line` in the translation CSV was stale.

The current-source extraction already contained the correct
`source_line_current`.

## Proven fix

Synchronize:

`source_line = source_line_current`

for the affected translation pack.

Do not reopen translation scope or redo content QA.

## Proof

Battle 153:

- 68 source lines synchronized
- injector dry-run PASS 153/153
- apply PASS 153/153
- build PASS

## Status

CLOSED.

---

# ISSUE 004 — Apparent missing Emerald save

## Symptom

After a test build the game appeared to enter the new-game path and the
existing save looked lost.

## Important rule

Do not immediately create or save a new game over the file.

First verify the save structure read-only.

## Observed save

`pokeemerald.sav`

- file size: 131088 B
- Flash save area: 131072 B
- extra tail: 16 B
- valid Emerald sector signatures: 28 / 32
- save indices: 17, 18
- section IDs: 0–13

This proved that the save data was still present.

The original save subsequently loaded successfully.

## Safe response

1. Do not overwrite the save.
2. Create a byte-for-byte backup.
3. Verify Emerald sector signatures.
4. Only investigate emulator/ROM association after proving the save itself
   is structurally present.

## Status

DATA LOSS DISPROVED.
Exact reason for the temporary load failure was not established.

---

# ISSUE 005 — Thai scratch buffer accidentally consumed IWRAM

## Symptom

After adding two 256-byte Pokémon Storage display buffers:

- EWRAM unexpectedly remained unchanged.
- IWRAM increased from 31,468 B to 31,996 B.

## Root cause

Declaration used the wrong project attribute ordering:

`static EWRAM_DATA ...`

## Proven fix

Use:

`EWRAM_DATA static ...`

## Proof

After correction:

- EWRAM increased by 512 B
- IWRAM returned to 31,468 B

## Status

CLOSED.

---

# Future issue-entry template

## ISSUE XXX — Short title

### Symptom
What the player/tool actually does.

### Reproduction
Smallest reliable reproduction.

### Root cause
Only record this once proven.

### Proven fix
Exact safe mechanism.

### Do not do
Dangerous or disproven approaches.

### Evidence
Build/runtime/tooling proof and commit.

### Reopen conditions
Only new reproducible failure, baseline/source change,
or direct contradictory evidence.

### Status
CLOSED / OPEN BLOCKER.


## Battle Healthbox Thai name clipping with gender — CLOSED (2026-08-23)

**Symptom**
Long Thai Pokémon names could be clipped in the 7-tile Battle Healthbox. An intermediate fix preserved the full name by hiding `♂/♀`, but this was visually undesirable.

**Root cause**
The Healthbox copies only 7 text tiles = 56 px. Thai shaped names use per-glyph advance values, while the gender symbol consumes another 5 px.

**Proven fix**
Keep canonical/save names untouched and adjust only the mutable Healthbox Thai display stream:
- gendered names: fit Thai name within 51 px, preserving the 5 px gender symbol.
- genderless names: fit within 56 px.
- use existing Thai shaped glyph advance values; do not resize the Healthbox, save structs, nickname storage, or canonical species strings.

**Evidence**
386 canonical species audited: 377 PASS, 6 gender-risk, 3 overflow.
Final build PASS: EWRAM 252260 B, IWRAM 31468 B, ROM 15975078 B.
Runtime QA PASS: full Thai name + gender visible, no clipping or geometry corruption.

**Do not reopen**
Unless a new reproducible clipping/layout failure appears, source/baseline changes, or direct contradictory evidence is found.


## Capture / Pokédex battle message still showed English species name — CLOSED (2026-08-23)

**Symptom**
Capture and Pokédex-related battle messages displayed the English default species name even though the Battle Healthbox correctly showed the Thai canonical name.

**Root cause**
`B_TXT_OPPONENT_MON1_NAME` bypassed the existing Thai-aware battle nickname resolver and used the vanilla nickname path.

**Proven fix**
Route `B_TXT_OPPONENT_MON1_NAME` through `ResolveBattleNicknameForText()`.
This preserves Thai custom nicknames and resolves default species names through `GetSpeciesNameForDisplay()`.

**Evidence**
Runtime QA PASS across capture/caught/nickname-prompt/Pokédex flow.
Final build PASS: EWRAM 252260 B, IWRAM 31468 B, ROM 15975102 B.

**Do not reopen**
Unless a new reproducible direct-name-resolution failure appears, source/baseline changes, or direct contradictory evidence is found.

## Trainer Class fixed-row overflow — CLOSED (2026-08-23)

### Symptom / requirement
Trainer Class labels needed Thai, but the original table was `gTrainerClassNames[][13]`.

### Root cause
Thai precomposed strings are longer than the original fixed 13-byte English rows.
Direct replacement would be unsafe.

A second risk existed in Union Room because `trainerCardStrBuffer[12][15]`
was used as a temporary Trainer Class destination.

PokéNav Match Call also has a real 69px Trainer Class display budget.

### Proven fix
1. Convert production Trainer Class storage to a pointer table.
2. Preserve English non-production fallback.
3. Union Room: point the dynamic placeholder directly to the Trainer Class string.
4. PokéNav: use a 256-byte display scratch and reduce Thai advance only when needed.
5. Minimum adaptive advance: 3px.
6. Do not alter save data, wireless structs, or canonical Thai wording.

### Evidence
- Rows: 66/66
- Font/precompose: PASS 66/66
- PokéNav direct fit: 52
- Adaptive fit: 14
- Hard width risk: 0
- Max encoded size: 121 bytes
- Build: PASS
- Battle Intro runtime: PASS
- PokéNav / Union Room runtime: OPTIONAL / WAIVED

### Avoid
- Do not force Thai into `[13]`.
- Do not enlarge save or wireless structures for display text.
- Do not globally shorten canonical class names for one screen.
- Do not reopen all 66 rows for one future screen-specific problem.

### Reopen only when
A new reproducible regression appears, source/baseline changes,
or direct contradictory evidence is found.

