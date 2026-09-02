---
project: PekeEmerald
document: PROJECT_CONTROL_CENTER
control_center_version: 1
status: ACTIVE
last_updated_local: "2026-08-22 23:04 +07:00"
repo: "~/dev/projects/pokeemerald-phaseF-remaining-thai-translation"
branch: "work/phaseF-remaining-thai-translation"
authoritative_head: "6ac3327a5"
authoritative_head_message: "thai: fix Pokemon Storage display runtime"
production_macro: "THAI_NAMING_PRODUCTION"
---

# PekeEmerald — Project Control Center

> **READ THIS FILE FIRST IN EVERY NEW CHAT.**
>
> This file is the single source of truth for current project scope, closed gates, policy locks,
> current blockers, and the next exact step.
>
> **Do not reconstruct current status from old batch CSVs, raw inventory counts, historical HOLD
> metadata, or chat memory if they conflict with this file.**
>
> The project intentionally does **not** translate every English string in the ROM.
> Translation scope is selective and must match the user's intended player-facing experience.

## 0. Authority order

When two sources disagree, use this order:

1. **`PROJECT_CONTROL_CENTER.md`** — current scope/status authority.
2. **Closed source/build/runtime evidence named in this file** — authoritative technical proof.
3. **Dedicated tracker explicitly named by a CLOSED scope in this file.**
4. `project_scope_summary.csv` / `PROJECT_SCOPE_DASHBOARD.md` — supporting summary only.
5. `project_scope_manifest.csv` — discovery/scope support only unless a row-level decision is explicitly promoted here.
6. `remaining_translation_inventory.csv`, `dialogue_master.csv`, historical batch CSVs, old reconcile/audit packs — **not current-status authority by themselves**.

### Offline-work rule

A file does **not** need to be committed to Git to be valid evidence, because early Phase F work was done offline.

However, offline evidence becomes authoritative only when it is registered in this Control Center with:
- the scope it proves,
- the exact count,
- the relevant artifact/tracker path,
- and the closed gate/result.

Do not infer `NOT DONE` merely because Git has no commit for an old offline artifact.

---

# 1. Project intent — LOCKED

The goal is **not** “translate all text in Pokémon Emerald.”

The goal is:
- translate the player-facing content the user intentionally selected,
- preserve names/data/mechanics that the user intentionally keeps in English or unchanged,
- avoid duplicate work,
- understand **what the player actually sees in-game** before deciding whether a new text group belongs in scope,
- keep the game stable and readable.

For every genuinely new scope:
1. Read the whole candidate group.
2. Explain where/how the player sees it in-game.
3. Separate UI / mechanic / tutorial / service / system / NPC flavor / data / credits / etc.
4. Let the user approve the scope.
5. Only then translate.

Do not use raw categories alone to decide scope.

---

# 2. Anti-loop rules — LOCKED

1. A passed gate is CLOSED. Do not re-check it unless:
   - a new reproducible failure appears,
   - source/baseline changes,
   - or direct contradictory evidence appears.
2. Before asking for another check, state what decision the result can change.
3. Missing information is either **BLOCKER** or **OPTIONAL**.
4. One audit round per decision maximum.
5. Build PASS + no new reproducible problem => do not rebuild/re-audit old code.
6. Terminal instructions: one command or one short block at a time.
7. Never push proof/search work back to the user unnecessarily.
8. Do not revoke a previous decision unless a real blocker or direct contradiction appears.
9. If user says `STOP LOOP`, stop auditing immediately and move forward from closed evidence.
10. Never use `set -e`, `exit`, or shell structures that may terminate the user's WSL session.

---

# 3. Git / worktree safety — LOCKED

Repo:
`~/dev/projects/pokeemerald-phaseF-remaining-thai-translation`

Branch:
`work/phaseF-remaining-thai-translation`

Current authoritative HEAD:
`db49febad` — `translation: refresh Phase F scope dashboard`

Recent checkpoints:
- `ecee9f81a` — `translation: add Frontier shared strings`
- `214d4bc6b` — `translation: add Frontier lounge 4-8 text`
- `ea6ab6b92` — `translation: add Frontier lounge text`
- `2b86a757a` — `translation: add Frontier common misc text`
- `3d2cc94f` — `translation: add Frontier outside and reception text`
- `93b976e92` — `translation: add Frontier Exchange text`
- `5b342b958` — `translation: add Battle Tent map text`
- `9f8a4635c` — `translation: add Battle Tent shared text`
- `58328c027` — `thai: fix Pokemon summary runtime display`
- `51a60fa04` — `translation: close expanded trainer scope`

Safety:
- Never `git add .`
- Never `git add -A`
- Stage only explicit intended files.
- Do not broad reset/clean/stash the Phase F worktree.
- CRLF -> LF Git warnings are normal line-ending normalization, not failures.

---

# 4. Production build baseline — CLOSED

Latest proven production build after Group 7 Batch 24:

- EWRAM: **251236 B / 95.84%**
- IWRAM: **31468 B / 96.03%**
- ROM: **15945110 B / 47.52%**

Production build must keep:
`-DTHAI_NAMING_PRODUCTION`

This baseline is CLOSED.
Do not rebuild merely to increase confidence.

---

# 5. Authoritative closed translation scope

These scopes are CLOSED unless a new reproducible runtime/source contradiction appears.

| Scope | Policy | Closed result |
|---|---|---:|
| Move Names | PRESERVE_EXISTING | POLICY_LOCKED |
| Move Descriptions | TRANSLATE_REQUIRED | 344 / 344 |
| Item Names | PRESERVE_EXISTING | POLICY_LOCKED |
| Item Descriptions | TRANSLATE_REQUIRED | 309 / 309 |
| Contest Move Names | PRESERVE_EXISTING | POLICY_LOCKED |
| Contest Move/Effect Descriptions | TRANSLATE_REQUIRED | 48 / 48 |
| Pokémon Species Names | Dedicated tracker | 386 / 386 |
| Main Story | TRANSLATE_REQUIRED | 191 / 191 |
| Trainer Spoken Dialogue | TRANSLATE_REQUIRED | 1633 / 1633 |
| Core UI | Dedicated tracker | 504 / 504 actionable |
| Battle/System normal player-facing messages | Dedicated tracker | 434 / 434 actionable |
| Optional NPC Dialogue | TRANSLATE_REQUIRED | 1820 / 1820 |
| Match Call Dialogue / UI | TRANSLATE_REQUIRED | 671 / 671 |
| PC / Decoration UI | TRANSLATE_REQUIRED | 32 / 32 |
| Pokédex Core Content | TRANSLATE_REQUIRED | 774 / 774 |
| Pokédex Rating | TRANSLATE_REQUIRED | 23 / 23 |
| Shared UI/System `src/strings.c` | TRANSLATE_REQUIRED | 28 / 28 |
| Birch Lab Menu/UI | TRANSLATE_REQUIRED | 1 / 1 |
| Devon Corp 2F PokéNav | TRANSLATE_REQUIRED | 3 / 3 |
| Mauville Man Pokédex reader | TRANSLATE_REQUIRED | 3 / 3 |
| Rival House 2F Pokédex | TRANSLATE_REQUIRED | 2 / 2 |
| Route 104 Rival Pokédex | TRANSLATE_REQUIRED | 2 / 2 |
| Route 105 Dad PokéNav | TRANSLATE_REQUIRED | 2 / 2 |
| Bulk-safe Menu Dialogue | TRANSLATE_REQUIRED | 7 / 7 |
| Special/UI Menu Text | TRANSLATE_REQUIRED | 4 / 4 |
| Final Structured C UI | TRANSLATE_REQUIRED | 3 / 3 |

## Group 7 — Battle Frontier / Battle Tent — CLOSED

Explicit facility scope:
**1700**

Final classification:
- `NEEDS_TRANSLATION`: **1610**
- `PRESERVE_DATA`: **80**
- `NOT_APPLICABLE`: **10**

Final result:
- translated/applied/build-closed: **1610 / 1610**
- remaining actionable: **0**
- Batches **01–24 CLOSED**

Final translation commit:
`ecee9f81a`

Dashboard checkpoint:
`db49febad`

**Do not reopen Group 7 facility scope.**

Historical Group 7 CSVs may still contain `HOLD` metadata.
That metadata is historical and is not current scope status.

---

# 6. Trainer expanded scope — CLOSED

Trainer expanded-scope reconciliation is CLOSED.

Known reconciliation:
- original HOLD trainer rows: **356**
- `PRESERVE_DATA`: **198**
- initial candidates: **158**
- duplicate/covered: **5**
- translated actionable: **153**

Trainer Spoken Dialogue authoritative total is now:
**1633 / 1633 DONE**

The 198 `PRESERVE_DATA` rows are not translation backlog.

Do not reopen Trainer scope because old CSVs still say HOLD.

---

# 7. Translation policy locks

## Names / labels

- `PC` stays **PC**.
- `ABILITY` heading: **do not translate**.
- Pokémon Ability names such as `SYNCHRONIZE`: **do not translate**.
- Ability descriptions: **translate Thai**.
- Nature names such as `QUIET`: **do not translate**.
- Type names: do not translate piecemeal. Current Frontier decision keeps Type names English.
- Stats such as `ATTACK`, `DEFENSE`, `SPEED`: keep English where the locked policy applies.
- Move Names: preserve existing.
- Item Names: preserve existing.
- Contest Move Names: preserve existing.

## Context-sensitive wording

- `abilities` in normal prose may mean skill/potential and should be translated by context.
- `Ability Symbol` in Battle Frontier is **not** a Pokémon Ability mechanic.
  It was approved as Thai `สัญลักษณ์ความสามารถ`.

## Locked place terminology

- Battle Tent = `แบทเทิลเทนต์`
- Fallarbor = `ฮาจิสึเกะ`
- Verdanturf = `ชิดาเกะ`
- Slateport = `ไคไน`

## Pokémon naming examples

Japanese-derived Thai policy remains active where applicable:
- Abra = `เคซี`
- SKITTY = `เอเนโค`
- SMOOCHUM = `มูจูรู`

---

# 8. Font / precompose / text-layout safety — LOCKED

The Thai production font is full at **768 / 768 glyphs**.

Known production font decision:
- atlas slot/index 764 was repurposed from `ฬิ` to `ตุ๊`
- no glyph-index shifts
- runtime/bbox checks passed for the approved replacement

Known risky/unsupported sequences previously encountered include:
- `ฬิ`
- `กึ`
- `ติ๊`
- U+0E4B (`๋`) caused failures in earlier batches

Previously approved safe rewrites include:
- `ตั๋ว` -> `บัตรโดยสาร`
- `อ๋อ` -> `อ้อ`
- `เดี๋ยวนี้` -> `ตอนนี้`

`หึหึหึ!` was runtime font-shaper validated and is safe.

## Permanent UI layout rule

For player-visible Thai:
1. Fit wording into the real game UI/message-box width and height.
2. Prefer shorter, context-correct Thai wording first.
3. Do **not** automatically enlarge windows, buffers, or memory merely to force wording to fit.
4. Structural expansion is allowed only when narrow, justified, and technically safe.
5. If a proposed expansion has plausible crash/corruption risk, **STOP and ask the user before changing it**.

A successful Build alone is not proof that every screen layout is safe.

---

# 9. Known runtime / structural fixes — CLOSED

## Pokémon Summary runtime buffer

Root cause:
`BufferMonTrainerMemo()` used a 32-byte met-location buffer.
Thai precomposed map names can expand into much larger positioned-glyph byte sequences.

Production fix:
- production met-location buffer = **512 bytes**
- fix committed in `58328c027`

This fix was runtime-proven stable.

Do not:
- increase `POKEMON_NAME_LENGTH`,
- enlarge BoxPokemon nickname storage,
- reapply the old renderer clipping experiment.

The renderer clipping experiment worsened visuals and was reverted.

## Thai player/Pokémon display

Battle HUD, Party/List, species display and Summary Thai display fixes that already passed runtime QA are CLOSED.
Do not reopen without a new reproducible failure.

---

# 10. Raw inventory / historical tracker warning

The following are **discovery/history**, not current completion authority:

- `dialogue_master.csv`
- `remaining_translation_inventory.csv`
- raw category counts in old dashboards
- historical batch CSV `scope_status=HOLD`
- old broad HOLD packs
- old reconcile/audit packs unless this Control Center explicitly promotes them

Reason:
these files can contain rows that were later translated, preserved, excluded, or covered by a dedicated tracker.

Example:
the historical remaining inventory still lists Battle Frontier rows as untranslated even though Group 7 is CLOSED.

Therefore:
**Never select new work directly from `translation_status=untranslated` or `scope_status=HOLD` without reconciling against this Control Center first.**

---

# 11. Current HOLD landscape

Battle review is now CLOSED and must not be counted as remaining HOLD work.

Historical prior-review pools still not canonically closed:

- system: **4437**
- item: **1003**
- sign: **10**

Historical non-Battle review-pool total: **5450**

Important:

These are **review-pool counts only**, not translation backlog and not project
completion numbers.

`battle: 505` is CLOSED:
- 286 COVERED_ALREADY
- 153 translated / applied / build-passed
- 26 PRESERVE_EXISTING
- 32 NOT_APPLICABLE
- 8 intentional HOLD
- 0 unresolved

Do not use `remaining_translation_inventory.csv` to infer current backlog.
# 12. Battle HOLD 505 canonical reconciliation — CLOSED

Battle HOLD review pool:
**505 / 505 terminally reconciled**

Final canonical disposition:

- `COVERED_ALREADY`: **286**
- `NEEDS_TRANSLATION`: **153**
- `PRESERVE_EXISTING`: **26**
- `NOT_APPLICABLE`: **32**
- `HOLD_FOR_CONTEXT`: **8**
- unresolved outside approved HOLD: **0**

Canonical tracker:

`tools/thai/translation/phaseF/batches/phaseF-battle-hold-505-canonical-reconcile.csv`

Actionable translation pack:

`tools/thai/translation/phaseF/batches/phaseF-battle-hold-actionable-153.csv`

Important historical correction:

The earlier proposal to translate 497 rows is superseded.
It contained already-covered / preserve / N/A targets because older IDs and historical trackers
did not provide a complete current view.

The final 505 reconciliation proved:
- 286 rows already covered by closed work,
- 26 rows intentionally preserved,
- 32 rows not applicable,
- 8 Group-I rows intentionally held for context,
- only 153 rows are genuinely actionable.

**Do not reopen the Battle 505 scope audit.**
Only the 153 `NEEDS_TRANSLATION` rows are eligible for translation.

# 13. Exact next step

Historical Sign HOLD 10 is CLOSED.

Do not reopen:
- Battle 505 / actionable 153
- Trainer expanded scope
- Group 7 Battle Frontier / Battle Tent
- Pokémon Storage runtime issue
- Historical Sign HOLD 10 / End Credits 9

Next work must be selected from the remaining non-closed HOLD landscape
using this Control Center as authority, not the stale remaining inventory.

# 14. New-chat bootstrap instruction

When a new chat starts, the assistant should:

1. Read `PROJECT_CONTROL_CENTER.md` first.
2. State the current HEAD, closed scope, current blocker, and next exact step from this file.
3. Do **not** ask the user to restate old scope decisions.
4. Do **not** inspect historical HOLD files to reconstruct current status unless the Control Center explicitly says the current task requires it.
5. Treat any older tracker conflict as historical unless it provides direct contradictory evidence against the current Control Center.
6. Update this file whenever a scope/batch decision closes.

---

# 15. Status vocabulary

Use only these meanings:

- **DONE / CLOSED** — passed and frozen; no re-audit without new failure/source change/direct contradiction.
- **POLICY_LOCKED** — intentionally preserved/untranslated by user decision.
- **PRESERVE_DATA / PRESERVE_EXISTING** — data/text deliberately unchanged.
- **COVERED_ALREADY** — another closed authoritative scope owns the target.
- **NOT_APPLICABLE** — not part of intended player-facing translation scope.
- **NEEDS_TRANSLATION** — genuinely actionable and not covered elsewhere.
- **HOLD_FOR_CONTEXT** — not yet safe to decide because player-visible purpose/context is unresolved.
- **BLOCKER** — missing evidence can change the decision and work must stop.
- **OPTIONAL** — useful extra confidence only; must not stop work.

---

# 16. Maintenance rule

Every time a batch or scope closes, update this file immediately with:
- exact scope count,
- final disposition,
- closed gates,
- commit/checkpoint,
- build/runtime evidence if relevant,
- and the next exact step.

If a future chat finds a contradiction:
- do not silently overwrite history,
- record the contradiction,
- state which decision it changes,
- resolve it once,
- update this file,
- then close the issue.

This file exists specifically to prevent repeated scoping, duplicate translation, and context loss across chats.

## Battle actionable 153 — technical closure

Canonical actionable pack:
`tools/thai/translation/phaseF/batches/phaseF-battle-hold-actionable-153-thai.csv`

Status:
- translation: 153/153
- font/precompose: PASS 153/153
- controls/placeholders: PASS
- page/line structure: PASS
- real layout gate: PASS 153/153
- injector dry-run: PASS 153/153
- injector apply: PASS 153/153
- source files modified: 11
- structural/window/buffer change: NONE
- production build: PASS

Build metrics:
- EWRAM: 251236 B / 95.84%
- IWRAM: 31468 B / 96.03%
- ROM: 15974118 B / 47.61%

Battle HOLD 505 reconciliation remains CLOSED.
The earlier 497 proposal remains superseded.
No further Battle 505 audit or rebuild is required absent a new reproducible failure,
source/baseline change, or direct contradictory evidence.

Targeted runtime QA may follow for constrained/special UI only
(Easy Chat / Union Room / Mystery Gift / other dedicated fixed UI).
Do not rebuild solely for that QA.

Battle 153 closure commit: `f5f9c040d` — `translation: complete remaining Battle HOLD scope`

## Canonical troubleshooting guide

Solved runtime/build/tooling issues are recorded in:

`docs/PEKEEMERALD_RUNTIME_TROUBLESHOOTING.md`

Future chats must consult this guide before opening a new audit.
A matching CLOSED issue must reuse its proven solution unless new
reproducible contradictory evidence exists.

## Pokémon Storage runtime closure

Commit:
`6ac3327a5` — `thai: fix Pokemon Storage display runtime`

Runtime proof:
- Thai nickname display: PASS
- Thai species display: PASS
- Storage bottom messages: PASS
- action-menu geometry: PASS
- visual corruption: resolved
- EWRAM: 252260 B / 96.23%
- IWRAM: 31468 B / 96.03%
- ROM: 15974646 B / 47.61%

Canonical issue record:
`docs/PEKEEMERALD_RUNTIME_TROUBLESHOOTING.md`

Status: CLOSED.
Do not reopen absent a new reproducible failure, source/baseline change,
or direct contradictory evidence.

## Historical Sign HOLD 10 — CLOSED

Final disposition:
- `PRESERVE_EXISTING`: **9** — End Credits / Staff Credits, terminally excluded
- `TRANSLATED`: **1** — `gEasyChatWord_Design`: `DESIGN` → `ออกแบบ`
- unresolved: **0**

Gates for the actionable row:
- context/scope approval: PASS
- font/precompose: PASS
- layout: 39 px / 96 px
- injector dry-run: PASS 1/1
- injector apply: PASS 1/1
- production build: PASS

Build:
- EWRAM: 252260 B / 96.23%
- IWRAM: 31468 B / 96.03%
- ROM: 15974686 B / 47.61%

Canonical tracker:
`tools/thai/translation/phaseF/batches/phaseF-sign-hold-10-canonical-reconcile.csv`

Translation pack:
`tools/thai/translation/phaseF/batches/phaseF-sign-hold-actionable-1-thai.csv`

The 9 End Credits rows must not return to translation scope absent a
source/policy change or direct contradictory evidence.

## Healthbox Pokémon Name Width — CLOSED (2026-08-23)

- Runtime display budget: 56 px total, `FONT_SMALL`.
- Gender symbol width: 5 px.
- Canonical Thai species audit: 386/386.
  - PASS: 377
  - RISK_WITH_GENDER: 6
  - OVERFLOW: 3
- Production fix: healthbox-only adaptive Thai advance fitting.
  - gendered Thai names reserve 5 px for `♂/♀` and fit name within 51 px.
  - genderless names may use full 56 px.
  - canonical species names remain unchanged.
  - nickname/save storage remains unchanged.
  - Pokédex / Party / Summary / PC Storage remain unchanged.
  - Healthbox dimensions and structures remain unchanged.
- Build PASS:
  - EWRAM 252260 B / 96.23%
  - IWRAM 31468 B / 96.03%
  - ROM 15975078 B / 47.61%
- Runtime QA PASS: long Thai name renders fully with gender symbol visible and no healthbox corruption.
- Reopen only for a new reproducible clipping/layout regression, source/baseline change, or direct contradictory evidence.


## Battle Capture / Pokédex Pokémon Name Resolution — CLOSED (2026-08-23)

- Symptom: Battle Healthbox showed canonical Thai species name, but capture/Pokédex messages still displayed the legacy English name.
- Root cause: `B_TXT_OPPONENT_MON1_NAME` used vanilla nickname resolution.
- Fix: reuse `ResolveBattleNicknameForText()` for the direct opponent MON1 placeholder.
- Default species names now resolve through `GetSpeciesNameForDisplay()`.
- Thai custom nicknames remain shaped/preserved.
- Healthbox, save structures, Party, PC Storage and canonical species names are unchanged.
- Build PASS: EWRAM 252260 B / 96.23%, IWRAM 31468 B / 96.03%, ROM 15975102 B / 47.61%.
- Runtime QA PASS: capture messages and Pokédex flow show canonical Thai species name correctly.
- Reopen only for a new reproducible direct-name-resolution regression, source/baseline change, or direct contradictory evidence.

## Trainer Class Names — CLOSED (2026-08-23)

- Scope: 66/66 DONE; 0 PENDING.
- Tracker: `tools/thai/translation/phaseF/batches/phaseF-trainer-class-66-scope.csv`
- Source: `src/data/text/trainer_class_names.h`
- Root blocker: original `gTrainerClassNames[][13]` fixed 13-byte rows cannot hold shaped Thai safely.
- Proven fix: production pointer table; English non-production fallback preserved.
- Union Room: bypass 15-byte temporary copy and use direct class-string pointer.
- PokéNav Match Call: 69px class budget; 52 direct fit, 14 adaptive fit, 0 hard-width risks.
- Adaptive fit changes display advance only; canonical Thai wording unchanged.
- Build PASS: EWRAM 252516 B / 96.33%, IWRAM 31468 B / 96.03%, ROM 15979302 B / 47.62%.
- Battle Intro runtime PASS.
- PokéNav Match Call runtime QA: OPTIONAL / WAIVED.
- Union Room Trainer Card runtime QA: OPTIONAL / WAIVED.
- Trainer individual names remain OPTIONAL / separate.
- Trainer Spoken Dialogue remains CLOSED 1633/1633.
- Reopen only for new reproducible failure, source/baseline change, or direct contradictory evidence.

## Group 8 — Special NPC Systems — CLOSED (2026-08-23)

Final reconciliation:
- total reviewed: **21**
- `TRANSLATE_REQUIRED`: **12**
- `PRESERVE_EXISTING`: **9**
- `HOLD_FOR_CONTEXT`: **0**
- unresolved: **0**

Translation/apply:
- translated: **12/12**
- injection dry-run: PASS 12/12
- injection apply: PASS 12/12
- source modified: `src/strings.c`

Production build:
- MODE: `THAI_NAMING_PRODUCTION`
- STATUS: PASS
- EWRAM: **252516 B / 96.33%**
- IWRAM: **31468 B / 96.03%**
- ROM: **15979790 B / 47.62%**
- BUILD GATE: CLOSED

Runtime QA:
- Contest Lady: OPTIONAL / WAIVED
- Quiz Lady: OPTIONAL / WAIVED
- Favor Lady: OPTIONAL / WAIVED
- Reason: user has not naturally reached these paths yet.
- If a reproducible issue appears later, reopen only the affected path.

Canonical tracker:
`tools/thai/translation/phaseF/batches/phaseF-group8-special-npc-21-canonical-reconcile.csv`

Actionable Thai pack:
`tools/thai/translation/phaseF/batches/phaseF-group8-special-npc-actionable-12-thai.csv`

The 9 `PRESERVE_EXISTING` rows are terminally excluded from translation scope.
Do not reopen Group 8 absent a new reproducible failure, source/baseline change,
or direct contradictory evidence.

Next exact step:
Select the next genuinely non-closed translation scope from canonical authority.
Do not infer backlog from stale broad inventories.


## Starter / Lead-Mon / Nickname Species Display — CLOSED (2026-08-23)

Classification:
- `Pokémon Species Names` → `Runtime Display Integration`
- This is NOT a new translation scope.
- Canonical species tracker remains CLOSED at 386/386.
- Required translation count remains unchanged.
- Pending remains 0.

New reproducible runtime failure:
- starter selection label displayed legacy English species names,
- `bufferleadmonspeciesname` inserted legacy English species names into field dialogue,
- Pokémon nickname Naming Screen header displayed legacy English species names,
- first implementation caused a black screen when entering the Naming Screen.

Confirmed root causes:
- `src/starter_choose.c::CreateStarterPokemonLabel()` read `gSpeciesNames[species]` directly.
- `src/scrcmd.c::ScrCmd_bufferleadmonspeciesname()` read `gSpeciesNames[species]` directly.
- `src/naming_screen.c::DrawMonTextEntryBox()` read `gSpeciesNames[...]` directly.
- the new 256-byte starter display scratch initially consumed default static/IWRAM space; moving it to `EWRAM_DATA` restored the proven IWRAM baseline and removed the Naming Screen black-screen regression.

Production fix:
- resolve affected species display paths through `GetSpeciesNameForDisplay()`.
- Starter label keeps its 104 px display budget.
- Naming header keeps its existing 17-tile window; usable text area is 128 px from x=8 and species-name fitting reserves the actual title width.
- fitting modifies only FC19 positioned-glyph `advance` values in a mutable display copy.
- minimum fitted advance is 3 px.
- canonical species wording is unchanged.
- save/nickname storage is unchanged.
- global font metrics are unchanged.
- window dimensions are unchanged.

Shared-effect note:
- `ScrCmd_bufferleadmonspeciesname()` is intentionally shared by multiple map scripts.
- All callers now receive the canonical Thai species display name.
- This is expected runtime-display behavior and MUST NOT be reclassified as untranslated generic dialogue/system rows.

Final production build PASS:
- EWRAM: 252772 B / 96.42%
- IWRAM: 31468 B / 96.03%
- ROM: 15980070 B / 47.62%

Runtime QA PASS:
- Starter selection canonical Thai species labels: PASS
- Littleroot Lab received-starter species name: PASS
- nickname prompt species name: PASS
- Pokémon Naming Screen header canonical Thai species name: PASS
- Naming Screen black screen: RESOLVED

Do not reopen this runtime path unless there is a new reproducible failure,
source/baseline change, or direct contradictory evidence.
Do not create a new translation backlog from direct `gSpeciesNames[]`,
RAW candidates, BASELINE_EXACT rows, or historical HOLD data for these paths.


## Ability Descriptions — ACTIVE SCOPE

Canonical tracker:
`tools/thai/translation/phaseF/batches/phaseF-ability-descriptions-78-canonical-reconcile.csv`

State:
- 77 real Ability descriptions required.
- 77 covered/closed.
- 0 PENDING translation.
- 1 NOT_APPLICABLE (`ABILITY_NONE`).
- Status: IN_PROGRESS.

Scope lock:
- Translate descriptions only.
- Keep `ABILITY` heading English.
- Keep Ability Names English.
- Keep Nature Names English.
- Type Names remain outside this scope and must not be translated piecemeal.

Existing coverage must not be translated twice:
- `ABILITY_BATTLE_ARMOR`: canonical Thai description already present.
- `ABILITY_BLAZE`: Thai Summary runtime override already player-visible.


Ability Descriptions Batch 01: CLOSED
- 15 descriptions translated/applied.
- Width gate PASS 15/15 within existing 144 px single-line budget.
- No window resize.
- Production build PASS: EWRAM 252772 B, IWRAM 31468 B, ROM 15981646 B.
- Current Ability Description scope: 17/77 DONE, 60 PENDING.


Ability Descriptions Batch 02: CLOSED
- 15 descriptions translated/applied.
- Batch 01 SPEED BOOST terminology correction applied.
- Width gate PASS; no window resize.
- Production build PASS: EWRAM 252772 B, IWRAM 31468 B, ROM 15983334 B.
- Current scope: 32/77 DONE, 45 PENDING.
- User approved all remaining 45 as one final batch.


Ability Descriptions: CLOSED 77/77
- 75 descriptions translated in canonical source.
- Existing BATTLE ARMOR Thai + BLAZE Summary runtime override complete total coverage.
- Width/layout PASS within existing Summary window; no resize.
- Final production build PASS: EWRAM 252772 B, IWRAM 31468 B, ROM 15988046 B.
- Runtime Summary QA PASS.

## CLOSED — Title Screen Translation Credit

- User-selected credit insertion is complete.
- Final visual: `Thai by Emu` / `เข้าเส้น`.
- Dedicated 160x32 sprite asset is wired into the Title Screen path.
- Five 32x32 sprites retain the original blink callback.
- Copyright path remains unchanged.
- Runtime QA PASS.
- PENDING: 0.
- Next user-selected scope: second in-game translation-credit location; exact location has not yet been chosen.


## Release-prep closures — 2026-08-24

### Translation Credit #2 — CLOSED

- Main Menu / Continue footer.
- Final text: `Font by Plae Pai Len Pai | Mod by RetroSpective`
- Runtime QA: PASS.
- Production build PASS:
  - EWRAM 252772 B / 96.42%
  - IWRAM 31468 B / 96.03%
  - ROM 15988806 B / 47.65%
- Title Screen Credit remains separately CLOSED.

### New Game PC Gifts — CLOSED

New games receive the following items in Bedroom PC Item Storage:
- Potion x50
- Super Potion x60
- Rare Candy x100

Source:
`src/player_pc.c::sNewGamePCItems`

Runtime QA: PASS 3/3.

Final production build:
- EWRAM 252772 B / 96.42%
- IWRAM 31468 B / 96.03%
- ROM 15988814 B / 47.65%

Existing saves are unchanged.
Save structures and PC capacity are unchanged.
Build Gate: CLOSED.

### Current next step

Release patch preparation.
Do not infer new translation backlog from historical inventories.


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
## Global Pokémon Display Name Consumers — CLOSED

Status: **BUILD + RUNTIME QA + BPS + PACKAGE PASS**

Source commit: `95fbe5676` — `thai: unify Pokemon display names globally`

Permanent policy: custom Thai nickname → shaped display; auto/default → canonical Thai species; custom non-Thai → preserve; live Party → `CopyMonNameForDisplay()`; Box → `CopyBoxMonNameForDisplay()`; stored/snapshot → `CopyStoredMonNameForDisplay()`; species-only → `GetSpeciesNameForDisplay()`; raw storage and transport remain raw; no species whitelist; shaped-name buffers require proven capacity.

Closed systems: Party Menu; field actions; Move Relearner; Pokéblock; species-only UI; Trade; Hall of Fame; Daycare; Egg Hatch; PokéNav; Contest; TV; Lottery; Storage display; script buffers; battle placeholders and link/species buffers.

Production build PASS: EWRAM 252,772 B / 96.42%; IWRAM 31,644 B / 96.57%; ROM 15,992,502 B / 47.66%; BUILD_RC=0.

Release authority: ROM SHA-1 `2a9e0d6f3967f60a2030de4cfff533109f79028d`; BPS SHA-1 `0ae84fe6745983b04b09cf807777cfcf2aac97f7`; BPS SHA-256 `79eda0fda490e7b482e1df1294a816eb4f98128b1a2544394071afc9115c7145`; ZIP 1,122,110 bytes; ZIP SHA-256 `38019b0f150d900916041c1ea68a6a5cc83ca339f4e6b3c2c49da23fecbd6b54`; BPS byte-identical PASS.

Reopen only for a new reproducible display failure, source/baseline change, or direct contradictory evidence. Current workflow: refresh remaining canonical docs → docs commit → push → fresh chat.
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

## 2026-09-03 — Safari / Healthbox / Pokédex runtime closure
- Source authority: `b21e5c8d4 — thai: harden Safari battle and Pokedex list`.
- Safari freezes were traced to two deterministic overruns: `gStringVar4[1000]` versus Thai field text up to 3,202 B, and Safari ball-count `text[16]` versus a 42 B Thai label. Fixed to 4,096 B and 64 B respectively.
- Reporter-save runtime QA PASS: Safari entry and wild encounter no longer freeze.
- Canonical Thai healthbox names now remove only the proven 1 px inter-glyph spacing; custom Thai nickname fitting remains unchanged. 386-species safe-fit audit unresolved = 0.
- Pokédex list uses a 56 px species-name slot. Thai overflow had left stale pixels in x=232..239 because row clearing ended at x=231. Names now fit to 56 px and row clear reaches x=240 exactly.
- Pokédex runtime QA PASS at representative reported regions including No125 and unseen `----------` rows.
- Production build PASS: EWRAM 257,780 B / 256 KB (98.34%); IWRAM 31,468 B / 32 KB (96.03%); ROM 15,996,182 B.
- Current release authority: `PekeEmerald-Thai-2026-09-03-FINAL`.
- ROM SHA-1 `e450d29ca263bff2608fefff0070154d54542daa`; BPS SHA-1 `ff66a12660ec803d58f68204130f47bf13780deb`; BPS SHA-256 `725a202b80b37d85496a9d087e358eb07cdb36bb4af968ec7a7c36d90f1ef5dc`.
- ZIP SHA-256 `7917d8b8dd2cf18ca3f18ff42aeb4a66e7e14daddcf8f551e0d751aedc2a43a0`; ZIP size 1,123,979 B; BPS apply byte-identical PASS.
- These runtime gates are CLOSED and must not be re-audited absent a new reproducible failure, source/baseline change, or direct contradiction.
