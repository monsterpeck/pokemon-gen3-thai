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


## Release-prep additions — CLOSED

### Translation Credit #2

- Location: Main Menu / Continue footer
- Status: DONE / CLOSED
- Runtime QA: PASS
- Text: `Font by Plae Pai Len Pai | Mod by RetroSpective`

### New Game PC Gifts

- Potion: 50
- Super Potion: 60
- Rare Candy: 100
- Status: DONE / CLOSED
- Runtime QA: PASS
- Production build: PASS
- Final ROM: 15988814 B / 47.65%


## 2026-08-24 — Public Release Package READY

Release source:
- Authoritative HEAD: `f9309dc19`
- Production ROM SHA-1: `e92a748200eb5d59baff7a8bc3dd7dc295b16d4a`
- Required clean base SHA-1: `f3ae088181bf583e55daf962a92bb46f4f1d07b7`

Patch:
- Format: BPS
- File: `PekeEmerald-Thai.bps`
- BPS SHA-1: `db56b658bbda108793a740a59d209efe80fd995e`
- BPS SHA-256: `648eae9b857025c494a76281c713fcd17abfe4a6c3521117f1f215984db71b2c`
- Apply-back verification: BYTE IDENTICAL PASS

Release package:
- File: `PekeEmerald-Thai-2026-08-24.zip`
- Size: 1094279 bytes
- ZIP SHA-256: `925d17def4964c8564eda125400537bd6f2ebe3bc8798de5e630beb0a7fe8bfb`
- Contains patch + Thai README + SHA256SUMS.
- No original or pre-patched commercial ROM is included.

Release status: READY FOR PUBLIC DISTRIBUTION.

Do not rebuild, regenerate, or re-verify this release artifact unless the
production ROM/source changes or a reproducible release failure is reported.


## 2026-08-24 — AUTHORITATIVE PUBLIC RELEASE V2 READY

This release supersedes the earlier 2026-08-24 release candidate.

Reason for supersession:
- Main Menu translation credit originally rendered only in `HAS_SAVED_GAME`.
- Runtime testing of a freshly patched ROM with no save exposed the missing footer.
- `HAS_NO_SAVED_GAME` now renders the same dedicated credit footer.
- Runtime QA PASS with save and without save.

Release source:
- Production source commit: `d0440c5bc`
- Fix: `thai: show main menu credit without save data`
- Required clean base SHA-1:
  `f3ae088181bf583e55daf962a92bb46f4f1d07b7`
- Production ROM SHA-1:
  `bca43db50b1b4ee2d00d50169393e8c9b1673f10`

Final production build:
- EWRAM: 252772 B / 96.42%
- IWRAM: 31468 B / 96.03%
- ROM: 15988878 B / 47.65%
- Build Gate: CLOSED

Patch:
- Format: BPS
- BPS SHA-1:
  `605cbcbfaa6251d3b9fbd667f0df253e7ddedcaf`
- BPS SHA-256:
  `90d6521136a9d561d5cf1f66c83e514dbe142199b3d68bb776824e3caaa210b1`
- Apply-back verification: BYTE IDENTICAL PASS

Release package:
- `PekeEmerald-Thai-2026-08-24.zip`
- Size: 1092374 bytes
- ZIP SHA-256:
  `5ddb3a89e69a988ec8fa28f7ba303447fde6fbbcfbda1dc8fc18061b4374377f`

The previous release hashes/package are SUPERSEDED and must not be used as
the current public-release authority.

Release V2 status: READY FOR PUBLIC DISTRIBUTION.

Do not rebuild, regenerate, or re-verify this release unless production source
changes or a new reproducible release failure is reported.

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
- ROM: 15990926 B / 32 MB / 47.65%

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
- SHA-1: `a04c65349e86698e53e9cbb78077a57c70876f79`
- Build memory:
  - EWRAM: 252772 B / 256 KB / 96.42%
  - IWRAM: 31468 B / 32 KB / 96.03%
  - ROM: 15990926 B / 32 MB / 47.65%

Required clean base ROM:
- SHA-1: `f3ae088181bf583e55daf962a92bb46f4f1d07b7`

Final BPS:
- File: `PekeEmerald-Thai-2026-08-24-FINAL.bps`
- SHA-1: `9438a3393d018ba0b3a34087c864ad5703b56541`
- SHA-256: `2cd2a68efcc1f973b20a0b6482d979e3e1bfd822ff42ab6ef595db918322120b`
- Create: PASS
- Apply: PASS
- Byte-identical verification against authoritative production ROM: PASS

Final public ZIP:
- File: `PekeEmerald-Thai-2026-08-24-FINAL.zip`
- Size: 1,099,741 bytes
- SHA-256: `1a60fb1116c16b9c115eb0c5cbca0270f5094d33b9da3f2d2a4b50f60e31f08b`
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

<!-- GLOBAL_POKEMON_DISPLAY_NAME_CLOSURE:START -->
## Global Pokémon Display Name Consumers

| Item | Status |
|---|---|
| Source remediation | CLOSED |
| Party / item messages | PASS |
| Field / Relearner / Pokéblock | PASS |
| Species-only consumers | PASS |
| Trade / Hall of Fame | PASS |
| Daycare / Egg Hatch | PASS |
| PokéNav lists / Search / Ribbon | PASS |
| PokéNav Condition Graph | PASS |
| Use Pokéblock formatter | PASS |
| Contest / Contest Util | PASS |
| TV species display | 90/90 PASS |
| TV full Pokémon-name display | 16/16 PASS |
| TV Name Rater structural handling | PASS |
| Lottery / Storage / Script buffers | PASS |
| Battle placeholders / Link / buffers | PASS |
| Custom Thai nickname | PASS |
| Auto/default canonical Thai species | PASS |
| Custom non-Thai nickname | PRESERVED |
| Stored/save nickname data | PRESERVED |
| Capacity blockers | 0 |
| Remaining actionable blockers | **0** |

Release source: `95fbe5676`

Build: EWRAM 252,772 B (96.42%); IWRAM 31,644 B (96.57%); ROM 15,992,502 B (47.66%); BUILD_RC=0.

Release authority: ROM SHA-1 `2a9e0d6f3967f60a2030de4cfff533109f79028d`; BPS SHA-256 `79eda0fda490e7b482e1df1294a816eb4f98128b1a2544394071afc9115c7145`; ZIP SHA-256 `38019b0f150d900916041c1ea68a6a5cc83ca339f4e6b3c2c49da23fecbd6b54`.

Gate: do not reopen without a new reproducible failure, source/baseline change, or direct contradictory evidence.
<!-- GLOBAL_POKEMON_DISPLAY_NAME_CLOSURE:END -->

## 2026-08-24 — IWRAM HOTFIX RELEASE CLOSURE

- Source hotfix: `bcaa3b6b0` — `fix: move contest Thai name scratch buffers to EWRAM`
- Root cause: two Contest Thai display scratch buffers were placed in IWRAM; moving them to EWRAM removed the IWRAM regression.
- Production build: PASS
  - EWRAM: 252936 B / 256 KB / 96.49%
  - IWRAM: 31468 B / 32 KB / 96.03%
  - ROM: 15992502 B / 32 MB / 47.66%
- Runtime QA: PASS; the prior black-screen freeze no longer reproduces after the IWRAM regression removal.
- Delta fast-forward audio stutter is tracked separately as emulator behavior and is not a ROM regression unless it reproduces at normal 1x speed after a cold emulator launch.
- ROM SHA-1: `ae70979957f8cf0ff401e4eadbea768a634fa0f3`
- Final BPS SHA-1: `fb3092e548548784ca01ea9a755c2ca26eaea9e7`
- Final BPS SHA-256: `8c85e04435c8fe9f62d91f1069737d178050ad9e972cf1c7e906e3a03a57f8c2`
- BPS apply byte-identical verification: PASS
- Final ZIP size: 1121494 bytes
- Final ZIP SHA-256: `885032c29494bb685722e2fec2ca3fa180f08c746d32a02bd9eae6fb7b855cb6`
- This hotfix release supersedes all earlier 2026-08-24 ROM/BPS/ZIP hashes and packages.
- Anti-loop: do not rebuild, re-audit, regenerate BPS/package, or reopen closed global Pokémon display-name gates unless there is a new reproducible failure, source/baseline change, or direct contradictory evidence.

## 2026-08-30 — Berry Tree + Rustboro Post-Battle Remediation CLOSED

This section SUPERSEDES all earlier public-release authority/hash lines in this file.

Source commit:
- `2d08f7733` — `translation: close berry tree and Rustboro post-battle gaps`
- Pushed to `origin/work/phaseF-remaining-thai-translation`: PASS

Reopened only from new reproducible runtime evidence:
- Berry Tree interaction: 18 translated labels + 1 non-language `!` preserve = 19/19 classified.
- Rustboro Gym post-battle: Josh / Tommy / Marc = 3/3 translated.
- The three Rustboro rows previously marked `COVERED_ALREADY` are a proven false closure and are superseded by this remediation.
- Targeted post-Fortree main-story audit: 95/95 checked rows already Thai encoded; do not reopen the full post-Gym-6 main-story scope without new contradictory runtime evidence.

Gates:
- Placeholder/control preservation: PASS
- Thai encoder/precompose: PASS
- Target-only source diff: PASS
- Production build: PASS
- Runtime QA from Delta screenshots: PASS
- BPS create/apply: PASS
- Byte-identical patched ROM verification: PASS
- Release package refresh: PASS

Production build metrics:
- EWRAM: 252,936 B / 256 KB (96.49%)
- IWRAM: 31,468 B / 32 KB (96.03%)
- ROM: 15,994,918 B / 32 MB (47.67%)

Release authority:
- Clean base ROM SHA-1: `f3ae088181bf583e55daf962a92bb46f4f1d07b7`
- Production ROM SHA-1: `a0af8d4efdd2d7489ffc3a3ad262d69839786965`
- BPS: `PekeEmerald-Thai-2026-08-30-FINAL.bps`
- BPS SHA-1: `60e56a07227de295e54bdcea8b8fb5c5358c4fd6`
- BPS SHA-256: `65284453702139e25b51966828ce0b6535de8bb6a50be9939e35f6d9bfae36b2`
- ZIP: `PekeEmerald-Thai-2026-08-30-FINAL.zip`
- ZIP size: 1,121,247 bytes
- ZIP SHA-256: `8876f2aa645709743f488fd8aacdbeddfadc8a636d6d3506b799cc3a820de208`

Local public release directory now contains only the 2026-08-30 FINAL BPS and ZIP.
The 2026-08-24 package is superseded and removed from the release directory.

Anti-loop:
- Do not rebuild, rerun this remediation audit, regenerate BPS/ZIP, or retest these closed paths merely for confidence.
- Reopen only for a new reproducible runtime defect, source/baseline change, or direct contradictory evidence.
## 2026-08-30 — Battle text hardening + Thai field reflow CLOSED

Source commit: `864848777` — `thai: harden battle text and reflow field dialogue`

Closed remediation:
- Localized the unregistered-SELECT system prompt; `SELECT` remains the literal button name.
- Expanded `gDisplayedStringBattle` from 300 to 2048 bytes. Real trainer lose/defeat maximum measured 1,593 B; conservative normal-battle expansion maximum 1,676 B, both below 2,048 B.
- Added centralized Thai battle-display names for 8 Gym Leaders, 4 Elite Four members, and Champion Wallace; ordinary Trainer names remain under the existing English-name policy.
- Reflowed 99 static field-dialogue labels across 34 files using Thai word boundaries and production glyph advances. Runtime placeholders were not force-reflowed. Field box = 216 px; safety limit = 208 px; final maximum line = 180 px.

Runtime QA PASS:
- SELECT prompt displays Thai correctly.
- Boss battle display shows localized leader names correctly.
- Representative Rustboro/Slateport line-break cases no longer split Thai words unnaturally.
- Winona full post-battle flow PASS: defeat text -> Feather Badge -> TM40 -> dialogue completion -> field control restored; no freeze.

Authoritative production build (already passed; do not rebuild for confidence):
- EWRAM: 254,684 B / 256 KB (97.15%)
- IWRAM: 31,468 B / 32 KB (96.03%)
- ROM: 15,995,870 B / 32 MB

Superseding release authority:
- ROM SHA-1: `a8f4de05976118d2bbca93e54df046764c84fdb5`
- BPS SHA-1: `e51457c240ef378c4a141f87ebcd1fed5e10f0d3`
- BPS SHA-256: `ac90981c4b85ba98ad6447cdaa84d0c43cb5f043c7d5ef43b8b77ef3dc99f0fa`
- BPS apply byte-identical: PASS
- FINAL ZIP: `PekeEmerald-Thai-2026-08-30-FINAL.zip`
- ZIP size: 1,124,116 bytes
- ZIP SHA-256: `5af736d619ba19586a942b31ca8394d40319935f9ad6a999361d73bc04280af1`

This supersedes the earlier 2026-08-30 package hashes. Reopen only for a new reproducible failure, source/baseline change, or direct contradictory evidence.

OPTIONAL cosmetic item not applied in this release: Thai glyph cluster `งั้` advance 7 -> 6 px. Do not block release on it.

## 2026-08-31 — PokéNav + whole-field line-break remediation CLOSED

This section SUPERSEDES the 2026-08-30 release authority above.

Source commit:
- `1ac517a34` — `thai: harden PokeNav condition and field line breaks`
- Pushed to `origin/work/phaseF-remaining-thai-translation`: PASS

Closed runtime defects:
- Match Call tile corruption: production `PokenavList::itemTextBuffer` expanded 128 -> 512 bytes for positioned Thai list rows.
- Condition redraw/search corruption: production `locationText` expanded 24 -> 64 bytes; current mon name/location are rebuilt from authoritative `currIndex` at render time instead of trusting the rotating preload text cache.
- Whole-field line-break regression: dirty production worktree audit checked 2,410 Thai field strings; 125 raw candidates reduced to 103 real break moves across 92 labels / 39 files. Permanent gate: raw 22 / allowed 22 / actionable 0 = PASS.
- Source hygiene: synthetic HEAD reproduced only 3 HEAD-level line-break defects; the source commit stages those 3 plus PokéNav fixes and the permanent linter. The other 100 worktree-only reflows sit on pre-existing dirty translation changes and were intentionally not staged, preventing old scope from leaking into this commit.

Runtime QA from user screenshots: Match Call PASS; Condition CANCEL -> back-scroll PASS; Condition Search/COOL detail PASS; reported field-dialogue split PASS.
Production build PASS: EWRAM 254,684 B / 256 KB (97.15%); IWRAM 31,468 B / 32 KB (96.03%); ROM 15,995,886 B / 32 MB.
Permanent gate: `python3 tools/thai/audit_field_linebreaks.py` -> checked 2410 / raw 22 / allowed 22 / actionable 0 / PASS.

Superseding release authority:
- Clean base ROM SHA-1: `f3ae088181bf583e55daf962a92bb46f4f1d07b7`
- Production ROM SHA-1: `50b57e301070df9928626e8939451b98fd78b072`
- BPS SHA-1: `4e1f927f6b75a96a39b7877d754e811d1330255c`
- BPS SHA-256: `6ef2d904eaf879d9e2000a54f21f5ee9846ce24c94d08462d5fc914366bfb115`
- BPS apply byte-identical: PASS
- FINAL ZIP size: 1,123,456 bytes
- FINAL ZIP SHA-256: `b9a0e77fccfafb341da532814ee96d93ac90b9a7d5d5ff50797ce57f986e94ee`

Anti-loop: do not rebuild, refresh, re-audit these PokéNav paths, or rerun whole-field reflow without a new reproducible failure, source/baseline change, or direct contradiction.

## 2026-08-31 — Release package naming correction CLOSED

This packaging-only correction supersedes the `2026-08-30-FINAL` filename from the prior closure. ROM and BPS payloads were NOT regenerated.

Correct release name:
- `PekeEmerald-Thai-2026-08-31-FINAL`
- BPS SHA-1 unchanged: `4e1f927f6b75a96a39b7877d754e811d1330255c`
- BPS SHA-256 unchanged: `6ef2d904eaf879d9e2000a54f21f5ee9846ce24c94d08462d5fc914366bfb115`
- ZIP SHA-256: `621f7755bcf5dd0bb4e4018ab9382929c7a2176bdc133fb13419ee6652ef1ecf`
- ZIP size: 1,123,457 bytes

Package audit: ZIP contains the correctly named BPS, updated README, SHA1SUMS.txt, and SHA256SUMS.txt; internal checksums PASS. Old `2026-08-30-FINAL` BPS/ZIP files were removed to prevent release ambiguity.

No ROM build, BPS creation, BPS apply, or release refresh was performed for this naming correction.

## 2026-09-03 — Runtime remediation status
- Safari battle freeze: CLOSED / PASS.
  - `gStringVar4` expanded 1000 -> 4096 B after measured field text exceeded vanilla capacity.
  - Safari ball-count scratch expanded 16 -> 64 B after 42 B Thai label overflow was confirmed.
- Battle healthbox canonical Thai name overlap: CLOSED / PASS.
  - Canonical species fitting removes at most 1 px inter-glyph spacing; custom Thai nickname path unchanged.
  - 386-species safe-fit audit: unresolved 0.
- Pokédex list right-edge stale pixels: CLOSED / PASS.
  - 56 px list-name fit added; row clear widened `0x60 -> 0x68`, ending exactly at x=240.
  - Runtime QA PASS around No043–No051 and No123–No130 including No125 and blank `----------` rows.
- Source: `b21e5c8d4`.
- Release: `PekeEmerald-Thai-2026-09-03-FINAL`.
- ROM SHA-1 `e450d29ca263bff2608fefff0070154d54542daa`; BPS SHA-1 `ff66a12660ec803d58f68204130f47bf13780deb`; byte-identical PASS.
- No further audit/build/refresh is required unless new reproducible evidence appears.
