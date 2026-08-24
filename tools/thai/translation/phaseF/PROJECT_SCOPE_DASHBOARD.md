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
- ROM: 15990214 B / 32 MB / 47.65%

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
- SHA-1: `4257a4f903cd272e62fbebde1b8c882f3837ef95`
- Build memory:
  - EWRAM: 252772 B / 256 KB / 96.42%
  - IWRAM: 31468 B / 32 KB / 96.03%
  - ROM: 15990214 B / 32 MB / 47.65%

Required clean base ROM:
- SHA-1: `f3ae088181bf583e55daf962a92bb46f4f1d07b7`

Final BPS:
- File: `PekeEmerald-Thai-2026-08-24-FINAL.bps`
- SHA-1: `395439f6247bb7db1f28b11f16ade469061d451e`
- SHA-256: `425058cd6209a7468dad80cf827dffe72c5b9dfcc2588b2fb08067523adfbc99`
- Create: PASS
- Apply: PASS
- Byte-identical verification against authoritative production ROM: PASS

Final public ZIP:
- File: `PekeEmerald-Thai-2026-08-24-FINAL.zip`
- Size: 1,098,411 bytes
- SHA-256: `65c1c427674c5842a3bfcafae0b2af4e7b8868d89d9d85682c949e38c656065e`
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
