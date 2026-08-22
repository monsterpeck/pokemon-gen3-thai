---
project: PekeEmerald
document: PROJECT_CONTROL_CENTER
control_center_version: 1
status: ACTIVE
last_updated_local: "2026-08-22 23:04 +07:00"
repo: "~/dev/projects/pokeemerald-phaseF-remaining-thai-translation"
branch: "work/phaseF-remaining-thai-translation"
authoritative_head: "de074bf93"
authoritative_head_message: "translation: add Phase F project control center"
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

After excluding:
- closed Group 7 facility rows,
- closed Trainer translation scope,
- Trainer `PRESERVE_DATA`,
- policy-locked names,

a prior review observed an Unclassified HOLD pool of:

- system: **4437**
- item: **1003**
- battle: **505**
- sign: **10**
- total: **5955**

These counts are **review-pool counts**, not “required translation remaining.”

Do not convert `5955` into project completion percentage or translation backlog.

---

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

Current actionable Battle translation scope:
**153 rows**

Next task:

1. Read the complete `phaseF-battle-hold-actionable-153.csv`.
2. Explain the player-visible context of the remaining 153 only.
3. Preserve all locked terminology/policies.
4. Translate the 153 in one batch if layout/runtime constraints permit.
5. Run:
   - control/placeholder gate,
   - font/precompose gate,
   - width/height/message-block layout gate.
6. If a structural expansion has plausible crash/corruption risk, STOP and ask the user before changing it.
7. Dry-run.
8. Apply.
9. Build once.
10. Commit.
11. Update this Control Center immediately.

Battle 505 scope reconciliation is CLOSED and must not be repeated.

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
