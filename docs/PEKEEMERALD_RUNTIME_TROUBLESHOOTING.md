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



## Group 8 Special NPC Systems — Runtime QA Deferral

- Scope: Contest Lady / Quiz Lady / Favor Lady player-visible text.
- Translation/apply/build: PASS 12/12.
- Production build: EWRAM 252516 B / 96.33%, IWRAM 31468 B / 96.03%, ROM 15979790 B / 47.62%.
- Runtime QA is OPTIONAL / WAIVED because these paths have not been naturally reached yet.
- Do not force navigation or block closure solely to obtain runtime proof.
- If a reproducible issue appears during normal play, reopen only the affected path.
- Do not rerun preflight, injection, or build unless source/baseline changes or the failure requires it.

## Mandatory Dashboard Reading Protocol

This protocol is MANDATORY at the start of every new chat/session before
creating a new audit, HOLD group, reconcile pack, or translation batch.

### Canonical authority order
1. `tools/thai/translation/phaseF/PROJECT_CONTROL_CENTER.md`
2. `tools/thai/translation/phaseF/PROJECT_SCOPE_DASHBOARD.md`
3. `tools/thai/translation/phaseF/project_scope_summary.csv`
4. Dedicated canonical tracker explicitly named by the Control Center/Dashboard
5. Historical inventories / broad discovery pools / old HOLD packs

Lower-priority files MUST NOT override a CLOSED/DONE decision from a higher
authority unless there is a new reproducible failure, source/baseline change,
or direct contradictory evidence.

### How to read the Dashboard

`DONE` / `CLOSED`
- Scope decision is finished.
- If `pending = 0`, do NOT audit that scope again.
- New raw hits that resemble this scope are presumed historical/duplicate/
  covered until direct contradictory evidence proves otherwise.
- Do NOT create a new translation batch from those hits.

`PENDING`
- This is real remaining actionable work inside the approved scope.
- Only these rows/counts are eligible to become the next translation batch.

`HOLD`
- This means a decision is still unresolved.
- HOLD does NOT mean "translate this".
- Reconcile context once, then decide TRANSLATE_REQUIRED,
  PRESERVE_EXISTING, NOT_APPLICABLE, or COVERED_ALREADY.

`PRESERVE_EXISTING`
- Intentional non-translation. Not backlog.

`NOT_APPLICABLE`
- Not a translation target. Not backlog.

`COVERED_ALREADY`
- Already handled by another closed scope/tracker. Not backlog.

### Critical interpretation rules

1. `BASELINE EXACT` does NOT mean "untranslated".
   It only means the current source still matches the baseline used by that audit.

2. `RAW CANDIDATES` does NOT mean "remaining work".
   It is only a discovery/reconcile pool.

3. A historical HOLD count does NOT override Dashboard `DONE / pending=0`.

4. If Dashboard says a scope is DONE and its canonical tracker is closed,
   STOP. Do not inspect the same source again merely because a broad scan found it.

5. Before opening any new audit, answer:
   "Which Dashboard row says this work is still PENDING/HOLD?"
   If no such canonical row exists, do not open the audit.

6. If a raw candidate appears to belong to a CLOSED scope:
   classify it as probable `COVERED_ALREADY` and verify only if there is
   direct contradictory evidence that can change that decision.

7. Do not infer backlog from:
   - `remaining_translation_inventory.csv`
   - `dialogue_master.csv`
   - old reconcile packs
   - old HOLD packs
   - broad source scans
   unless the Dashboard/Control Center explicitly points to them as current authority.

### Mandatory new-chat startup sequence

Before any source scan or audit:

1. Confirm repo / branch / current HEAD.
2. Read `PROJECT_CONTROL_CENTER.md`.
3. Read `PROJECT_SCOPE_DASHBOARD.md`.
4. Read `project_scope_summary.csv`.
5. Identify ONLY rows with current `PENDING > 0` or unresolved `HOLD`.
6. Ignore CLOSED/DONE scopes.
7. Only then inspect a dedicated tracker or source if needed.

### Decision gate

A new audit is allowed only when:
- Dashboard/Control Center shows real PENDING/HOLD work, OR
- a new reproducible runtime failure exists, OR
- source/baseline changed, OR
- direct contradictory evidence exists.

Otherwise:
`AUDIT NOT ALLOWED — CANONICAL SCOPE ALREADY CLOSED`

### Closure discipline

When a scope is completed:
1. Update canonical tracker.
2. Update `project_scope_summary.csv`.
3. Update `PROJECT_SCOPE_DASHBOARD.md`.
4. Update `PROJECT_CONTROL_CENTER.md`.
5. Record reusable technical fixes in this troubleshooting guide.
6. From that point forward the scope is CLOSED and must not be rediscovered
   by future broad scans.

The Dashboard is a decision authority, not a discovery list.


## Starter / Lead-Mon / Naming Screen still shows English species name — CLOSED (2026-08-23)

### Symptom

Canonical Thai Pokémon Species Names were already complete 386/386, but some
player-visible paths still showed legacy English names.

Reproduced examples:
- Starter selection showed `TORCHIC` instead of `อาจาโม`.
- Littleroot Lab dialogue using `bufferleadmonspeciesname` showed the legacy English name.
- the Pokémon nickname Naming Screen header showed `TORCHIC`.
- after the first implementation, entering the Naming Screen produced a black screen.

This is a runtime-display integration failure, NOT missing translation data.

### Root cause

Three affected paths bypassed the canonical Thai-aware resolver:

- `src/starter_choose.c::CreateStarterPokemonLabel()`
  used `gSpeciesNames[species]`.
- `src/scrcmd.c::ScrCmd_bufferleadmonspeciesname()`
  used `gSpeciesNames[species]`.
- `src/naming_screen.c::DrawMonTextEntryBox()`
  used `gSpeciesNames[sNamingScreen->monSpecies]`.

The first implementation also introduced:

`static u8 sStarterSpeciesNameDisplay[256];`

in default static storage. IWRAM increased from the proven 31468 B baseline to
31740 B. Entering the Naming Screen then black-screened.

Moving the scratch buffer to:

`EWRAM_DATA static u8 sStarterSpeciesNameDisplay[256] = {0};`

returned IWRAM to 31468 B and the reproduced black screen disappeared.

### Proven fix

Use:

`GetSpeciesNameForDisplay(species)`

for the affected display-only species paths.

Do NOT change:
- canonical Japanese-based Thai species names,
- Pokémon nickname/save structures,
- `POKEMON_NAME_LENGTH`,
- global Thai font metrics,
- window dimensions.

### Width handling

Starter label:
- window width = 13 tiles = 104 px.
- center/display the canonical Thai species name within that existing 104 px budget.
- if required, adapt only FC19 positioned-glyph `advance` values in the mutable display copy.
- minimum adaptive advance = 3 px.

Pokémon Naming Screen header:
- `WIN_TEXT_ENTRY_BOX` width = 17 tiles = 136 px.
- text begins at x=8, leaving 128 px usable.
- measure the existing title first.
- species budget = `128 - titleWidth`.
- fit only the species-name display copy.
- never compress or rewrite the title itself.

The shared helper:

`FitThaiPositionedGlyphAdvances()`

is display-only and inert unless explicitly called.

### Important FC19 note

`GetStringWidth()` already understands
`EXT_CTRL_CODE_THAI_POSITIONED_GLYPH` and reads the positioned-glyph advance.
Do not blame FC19 width parsing for this resolved black-screen case unless new
direct evidence appears.

### Shared script-command behavior

`ScrCmd_bufferleadmonspeciesname()` is used by multiple map scripts.

Changing it to `GetSpeciesNameForDisplay()` intentionally makes all callers
receive the canonical Thai species display name. This is the correct shared
runtime behavior.

Do NOT treat those map usages as new untranslated dialogue/system backlog.

### Final evidence

Production build PASS:
- EWRAM: 252772 B / 96.42%
- IWRAM: 31468 B / 96.03%
- ROM: 15980070 B / 47.62%

Runtime QA:
- Starter selection canonical Thai species names: PASS
- Littleroot Lab received-starter name: PASS
- nickname prompt species name: PASS
- Pokémon Naming Screen header: PASS
- Naming Screen black screen: RESOLVED

### Reopen rule

CLOSED.

Reopen only for:
- a new reproducible failure,
- source/baseline change,
- direct contradictory evidence.

Do not reopen Species Names 386/386 or create translation scope from
`gSpeciesNames[]`, RAW candidates, BASELINE_EXACT rows, historical HOLD pools,
or generic source scans for this already-closed runtime path.

## Title Screen credit banners and indexed OBJ palettes

### Proven Title Screen credit implementation

The approved Title Screen translation credit uses a dedicated graphic asset:

- `graphics/title_screen/thai_credit_banner.png`
- 160x32 px
- five 32x32 OBJ sprites
- wording:
  - `Thai by Emu`
  - `เข้าเส้น`

The original `press_start.png` remains intact because it is also used by the
copyright banner. The new credit uses its own sprite sheet while retaining the
existing Press Start blink callback.

### Critical indexed-palette rule

A PNG can look correct in an image viewer but render incorrectly in-game when
its palette indices do not match the OBJ palette actually loaded at runtime.

For this Title Screen path the sprite template uses the existing
Press Start/Copyright palette. Therefore the credit bitmap's pixel indices must
be remapped to the indices of that runtime palette rather than relying on RGB
values embedded in the standalone PNG.

Symptoms of a bad index mapping included:

- white text becoming faint/gray in-game;
- black appearing as an opaque rectangle;
- an asset looking correct in Windows but wrong in the ROM.

The proven fix is to keep index 0 transparent and remap foreground/shadow pixel
indices against the palette used by `gTitleScreenPressStartPal`.

### Production Thai-font authority

For current PekeEmerald production work use only:

- `tools/thai/font/thai_precompose_glyph_map.json`
- `graphics/fonts/thai_shaped.png`
- `tools/thai/shape_thai_precompose.py`
- production glyph count: 768 (`0..767`)

`thai_shaped_glyph_map.json`, Noto-based proof tooling, and historical shaping
artifacts are legacy/reference paths and must not be selected for production
rendering merely because their filenames appear related.


## Main Menu footer credit / New Game PC gifts — CLOSED 2026-08-24

### Main Menu footer credit

Observed implementation requirement:
- Raw `|` inside the `_()` credit string failed agbcc with U+007C.
- Proven solution: use `{EMOJI_PIPE}` from `charmap.txt`.
- Final player-visible text:
  `Font by Plae Pai Len Pai | Mod by RetroSpective`
- Runtime QA PASS.

Do not replace `{EMOJI_PIPE}` with a raw `|` unless the text compiler behavior
changes and is re-proven.

### New Game PC gifts

Initial PC contents are controlled by:
`src/player_pc.c::sNewGamePCItems`

Closed production configuration:
- `ITEM_POTION, 50`
- `ITEM_SUPER_POTION, 60`
- `ITEM_RARE_CANDY, 100`
- terminal `ITEM_NONE, 0`

`NewGameInitPCItems()` clears the New Game PC item slots and loads this table.
This does not retroactively modify existing save files.

Runtime QA PASS 3/3.
Final production build PASS:
- EWRAM 252772 B / 96.42%
- IWRAM 31468 B / 96.03%
- ROM 15988814 B / 47.65%


## Main Menu credit missing on fresh/no-save ROM — CLOSED 2026-08-24

Symptom:
- BPS applied successfully and ROM matched production bytes.
- Translation credit appeared with an existing save but was absent on the
  `NEW GAME / OPTION` menu when no save file existed.

Root cause:
- Footer rendering was implemented only in `HAS_SAVED_GAME`.
- `HAS_NO_SAVED_GAME` did not draw the dedicated credit window.

Production fix:
- Reuse the existing dedicated credit window and text in
  `HAS_NO_SAVED_GAME`.
- No font, window geometry, save structure, or existing translation scope
  changes were required.

Runtime QA:
- Saved-game Main Menu credit: PASS.
- No-save Main Menu credit: PASS.

Production build:
- EWRAM 252772 B / 96.42%
- IWRAM 31468 B / 96.03%
- ROM 15988878 B / 47.65%

Release consequence:
- First release candidate is SUPERSEDED.
- Authoritative release source is `d0440c5bc`.

<!-- ODAMAKI_POLICY_CLOSURE_START -->
## Professor Odamaki Naming Policy Closure — 2026-08-24

Status: **CLOSED / RUNTIME PASS**

Player-visible naming policy:
- Professor Birch -> `ศ.โอดามากิ`
- Bare self-introduction `เบิร์ช` -> `โอดามากิ`
- Full-title form `ศาสตราจารย์เบิร์ช` -> `ศาสตราจารย์โอดามากิ`
- Internal identifiers such as `ProfBirch_*`, `BIRCH_*`, flags, map IDs, functions and filenames remain unchanged.

Applied scope:
- 14 production source files
- 50 changed lines
- 52 player-visible name replacements

Runtime QA PASS:
- New Game professor introduction
- Early-game mother dialogue
- Starter rescue screen
- Route 101 professor dialogue
- Professor's Lab dialogue
- No observed layout regression from the longer Odamaki name

Authoritative production build after closure:
- EWRAM: 252772 B / 256 KB / 96.42%
- IWRAM: 31468 B / 32 KB / 96.03%
- ROM: 15990286 B / 32 MB / 47.65%

Reopen only if:
- a reproducible player-visible `เบิร์ช` / `เบริซ์` / English `BIRCH` leak is found,
- a layout/runtime regression appears,
- or the source/baseline changes.

Previous release package/checksums created before this naming-policy change are superseded.
Next release step: commit this closure, then regenerate and byte-verify the final BPS package from the authoritative production ROM.
<!-- ODAMAKI_POLICY_CLOSURE_END -->

<!-- FINAL_RELEASE_20260824_START -->
## Final Public Release Package — 2026-08-24

Status: **CLOSED / RELEASE VERIFIED**

Authoritative production ROM:
- SHA-1: `9c0ee64dc5d543c9d90fc470371bc0fe273c2823`
- Build memory:
  - EWRAM: 252772 B / 256 KB / 96.42%
  - IWRAM: 31468 B / 32 KB / 96.03%
  - ROM: 15990286 B / 32 MB / 47.65%

Required clean base ROM:
- SHA-1: `f3ae088181bf583e55daf962a92bb46f4f1d07b7`

Final BPS:
- File: `PekeEmerald-Thai-2026-08-24-FINAL.bps`
- SHA-1: `d4dee6ccd4d37f56a0c86a0c853fbb1dcf968118`
- SHA-256: `2d6f832e3acacc4bf68e5eb3b7bea0d63bc0f243c79e7f5391a026044a9f8cd5`
- Create: PASS
- Apply: PASS
- Byte-identical verification against authoritative production ROM: PASS

Final public ZIP:
- File: `PekeEmerald-Thai-2026-08-24-FINAL.zip`
- Size: 1,099,592 bytes
- SHA-256: `5e02d74576468bcb615635ac1b784e018410339dbabe38c136562506f9ad8a05`
- Local package path: `/home/luffy/dev/releases/PekeEmerald-Thai-2026-08-24-FINAL.zip`

Package contents include:
- BPS patch
- Detailed Thai installation / usage README
- SHA-1 checksum file
- SHA-256 checksum file

Distribution policy:
- Distribute the BPS patch only.
- Do not redistribute the clean Pokémon Emerald ROM.
- Do not redistribute a pre-patched `.gba` ROM.

This release supersedes all earlier 2026-08-24 release packages and hashes.

Reopen the release gate only for a new reproducible runtime defect,
a source/baseline change, or direct contradictory evidence.
<!-- FINAL_RELEASE_20260824_END -->

## Runtime Closure — Evolution / Rare Candy Pokémon Display Names

Status: **CLOSED / BUILD + RUNTIME QA PASS**

Scope closed:
- Normal Evolution and Trade Evolution Pokémon-name display
- Evolution start / success / cancel messages
- Rare Candy level-up Pokémon-name display
- Move learn / forget / stop-learning Pokémon-name display
- Custom Thai nickname display
- Auto/default nickname policy via canonical Thai species display
- Applies generically to all Pokémon species; no species whitelist

Root cause:
- Several vanilla consumers used independent nickname/display paths.
- Thai shaped names cannot be treated as ordinary fixed-size nickname strings everywhere.
- Move-learning paths must respect the battle text-buffer contract rather than copying expanded shaped text into compact buffers.

Permanent implementation rule:
- Use the centralized Pokémon Display Name API for player-visible Pokémon names.
- Custom Thai nickname -> preserve and shape the player's nickname.
- Auto/default nickname -> GetSpeciesNameForDisplay(species).
- Custom non-Thai nickname -> preserve original nickname.
- Do not modify stored nickname/species data merely to change display text.
- Do not create per-species fixes or duplicate display-name resolvers for individual screens.

Runtime QA:
- Rare Candy level-up custom Thai nickname: PASS
- Move learn / forget custom Thai nickname: PASS
- Evolution custom Thai nickname: PASS
- Evolution Thai start/success text: PASS
- Post-evolution Thai species display: PASS
- No blank / corrupted Thai Pokémon names observed in tested flows.

Latest production build:
- EWRAM: 252772 B / 256 KB / 96.42%
- IWRAM: 31468 B / 32 KB / 96.03%
- ROM: 15990926 B / 32 MB / 47.66%

Reopen only for:
- a new reproducible display failure,
- source/baseline change, or
- direct contradictory runtime evidence.

