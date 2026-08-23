# PekeEmerald — CURRENT HANDOVER CHECKPOINT

Date: 2026-08-23

## Repository
- Repo: `~/dev/projects/pokeemerald-phaseF-remaining-thai-translation`
- Branch: `work/phaseF-remaining-thai-translation`
- Current committed HEAD before Trainer Class closure commit: `f2d62110f`
- Canonical authority: `tools/thai/translation/phaseF/PROJECT_CONTROL_CENTER.md`
- Troubleshooting authority: `docs/PEKEEMERALD_RUNTIME_TROUBLESHOOTING.md`

## Recent CLOSED runtime fixes
- Battle Healthbox Thai name width: CLOSED
  - commit `de5c005f6`
  - full Thai name + gender runtime PASS
- Capture / Pokédex direct species-name resolution: CLOSED
  - commit `8424a2dc4`
  - capture/Pokédex Thai species runtime PASS
- Trainer Class scope registration:
  - commit `f2d62110f`

## Trainer Class Names — CLOSED
- Required: 66
- DONE: 66
- PENDING: 0
- Individual Trainer names: OPTIONAL / separate scope
- Trainer Spoken Dialogue remains CLOSED 1633/1633

### Translation / preflight
- Thai Trainer Class labels: 66/66
- Font/precompose: PASS 66/66
- Thai Unicode remaining after shaping: 0
- PokéNav direct fit: 52
- PokéNav adaptive fit: 14
- Hard width risk: 0
- Encoded >255 bytes: 0
- Maximum encoded size: 121 bytes

### Proven architecture
- Original `gTrainerClassNames[][13]` fixed rows were too small for shaped Thai.
- Production representation changed to pointer table.
- English non-production fallback preserved.
- Union Room 15-byte temporary Trainer Class copy bypassed using direct placeholder pointer.
- PokéNav Match Call keeps real 69px class budget with display-only adaptive Thai advance.
- Minimum adaptive Thai advance: 3px.
- Canonical Thai wording unchanged.
- Save data unchanged.
- Wireless/Union Room structure sizes unchanged.

### Build
- STATUS: PASS
- EWRAM: 252516 B / 96.33%
- IWRAM: 31468 B / 96.03%
- ROM: 15979302 B / 47.62%

### Runtime QA
- Battle Intro: PASS
- Thai Trainer Class: PASS
- Individual Trainer name English: PASS / intended
- PokéNav Match Call runtime: OPTIONAL / WAIVED
- Union Room Trainer Card runtime: OPTIONAL / WAIVED

Do not block progress on the two OPTIONAL runtime checks.
If a reproducible issue appears later, reopen only that specific path.

## Major scopes that must NOT be reopened
- Group 7 Battle Frontier / Battle Tent: 1610/1610 actionable CLOSED
- Trainer Spoken Dialogue: 1633/1633 DONE
- Battle HOLD 505 reconciliation/actionable work: CLOSED
- Pokémon Storage Thai display runtime: CLOSED
- Historical Sign HOLD 10: CLOSED
- Species Names: 386/386 DONE
- Starter / lead-mon / nickname species display integration: CLOSED
- Battle Healthbox Thai width handling: CLOSED
- Capture / Pokédex species-name resolution: CLOSED
- Trainer Class Names: 66/66 CLOSED

## Permanent anti-loop workflow
1. CLOSED gates stay CLOSED absent new reproducible failure, source/baseline change, or direct contradictory evidence.
2. Before an audit, state what decision the result can change.
3. Missing information is BLOCKER or OPTIONAL only.
4. Maximum one audit round per decision.
5. Build once after source change; after PASS do not rebuild without a new problem.
6. Runtime-test only the affected player-visible path.
7. Reuse proven Thai-aware helpers and display scratch buffers.
8. Avoid save/compact-storage/network-structure changes unless genuinely unavoidable.
9. Use actual UI width/layout budgets.
10. Prefer display-only adaptive fit over changing canonical wording or window geometry.

## Terminal pattern
- One short WSL command/block at a time.
- Never use `set -e`, `exit`, or `exec`.
- Do not suppress output.
- Do not use quiet/hidden redirection.
- Never `git add .` or `git add -A`.
- Stage explicit files only.
- Output should be compact and evidence-first.

Preferred result style:

=== <SCOPE> FULL PREFLIGHT ===
ROWS: N
SOURCE_LINE SYNCED: N
FONT/PRECOMPOSE: PASS N/N
SOURCE TARGETS: N/N
BASELINE MATCH: N/N
CONTROL/PLACEHOLDERS: N/N
DUPLICATE CONSISTENCY: PASS
FULL BATCH PREFLIGHT: PASS

=== PHASE D INJECTION DRY-RUN ===
STATUS: PASS
MASTER_ROWS: N
RESOLVED: N
UNIQUE_TARGETS: N
BASELINE_MATCH: N
CONTROL_PLACEHOLDER_GUARD: PASS (N/N)
SOURCE_FILES_TARGETED: N
SOURCE_FILES_MODIFIED: 0
READY_FOR_APPLY: YES

Only use checks relevant to the actual scope.

## Next exact step
1. Commit the staged Trainer Class closure.
2. Record returned commit hash as authoritative HEAD.
3. Start a fresh chat using this checkpoint.
4. Continue from current Control Center; do not infer backlog from stale broad inventories.

## Mandatory startup rule for every new chat
Before opening any audit or translation batch, follow
`Mandatory Dashboard Reading Protocol` in
`docs/PEKEEMERALD_RUNTIME_TROUBLESHOOTING.md`.

A raw candidate, BASELINE_EXACT row, historical HOLD, or broad inventory hit
MUST NOT be treated as remaining work unless the current Control Center /
Dashboard shows that scope as PENDING or unresolved HOLD.


## Starter / Lead-Mon / Nickname Species Display Closure

Status: CLOSED / runtime PASS.

Classification:
- Pokémon Species Names → Runtime Display Integration.
- NOT a new translation scope.
- Species Names remain 386/386 DONE, pending 0.

Affected paths closed:
- Starter selection label → canonical Thai species display.
- `ScrCmd_bufferleadmonspeciesname()` → canonical Thai species display for all callers.
- Pokémon Naming Screen header → canonical Thai species display with species-only adaptive fitting.

Layout / safety:
- Starter label budget: 104 px.
- Naming header: 17 tiles; printing begins at x=8, therefore 128 px usable.
- Naming fitting reserves the actual title width and compresses only mutable FC19 species-name advances.
- minimum adaptive advance: 3 px.
- canonical species strings, save/nickname storage, global font metrics, and window dimensions remain unchanged.
- `sStarterSpeciesNameDisplay[256]` must remain `EWRAM_DATA`; default static placement caused the reproduced Naming Screen black-screen regression.

Final build:
- EWRAM 252772 B / 96.42%
- IWRAM 31468 B / 96.03%
- ROM 15980070 B / 47.62%

Runtime proof:
- Starter labels: PASS
- Lab received-starter species name: PASS
- nickname prompt: PASS
- Naming Screen header: PASS
- black screen: RESOLVED

Do not reopen or regenerate translation scope from these paths unless a new
reproducible runtime failure, source/baseline change, or direct contradiction appears.


## Current Active Scope — Ability Descriptions

- User-selected scope.
- Required: 77 real Ability descriptions.
- Done/covered: 77.
- Pending: 0.
- NOT_APPLICABLE: 1 (`ABILITY_NONE`).
- Canonical tracker:
  `tools/thai/translation/phaseF/batches/phaseF-ability-descriptions-78-canonical-reconcile.csv`
- Translate descriptions only.
- Ability heading/names, Nature names, and Type names are not part of this scope.
- Batch 01: CLOSED 15/15 after width gate, apply and production build.
- Latest build: EWRAM 252772 B / 96.42%, IWRAM 31468 B / 96.03%, ROM 15981646 B / 47.63%.
- Next step: Batch 02 context/translation review from the remaining 60 PENDING descriptions.


## Ability Descriptions — Final Batch Direction

- Batch 02 CLOSED.
- Latest production build: EWRAM 252772 B / 96.42%, IWRAM 31468 B / 96.03%, ROM 15983334 B / 47.63%.
- Remaining 45 PENDING descriptions are approved to proceed as one final batch.
- Reuse established project terminology before proposing wording.


## Ability Descriptions — CLOSED

- 77/77 DONE.
- 0 PENDING.
- Final build: EWRAM 252772 B / 96.42%, IWRAM 31468 B / 96.03%, ROM 15988046 B / 47.65%.
- Runtime Summary QA PASS.
- No window resize required.
- Do not reopen absent new reproducible failure/source-baseline change/direct contradiction.

## 2026-08-23 — Title Screen Credit CLOSED / next credit location

### Closed in this checkpoint

- Ability Descriptions: CLOSED 77/77, PENDING 0.
- Title Screen Translation Credit: CLOSED 1/1, PENDING 0.
- Final Title Screen wording:
  - `Thai by Emu`
  - `เข้าเส้น`
- Final runtime visual QA: PASS.
- Dedicated banner: 160x32, five 32x32 sprites.
- Blink preserved.
- Copyright preserved.
- Original `press_start.png` preserved.
- Indexed runtime palette issue resolved.

### Production Thai-font lock

Use only:

- `tools/thai/font/thai_precompose_glyph_map.json`
- `graphics/fonts/thai_shaped.png`
- `tools/thai/shape_thai_precompose.py`
- 768 glyphs (`0..767`)

Do not use the Noto/reference pipeline or
`thai_shaped_glyph_map.json` for production rendering.

### Next exact workflow

The next user-selected work is to add translation credit at one more in-game
location.

Do not broad-audit the game for credit locations. Wait for the user to identify
or show the desired screen/location, then trace only that affected runtime path.

### Repository synchronization

Ability-description and Title-Screen-credit work must be reviewed in the current
working tree and committed/pushed before treating the remote branch as
synchronized. Do not assume the previous pushed HEAD contains these changes.

## AUTHORITATIVE PRODUCTION BUILD — MANDATORY

For every ROM-affecting production source/asset change, use exactly:

```bash
cd ~/dev/projects/pokeemerald-phaseF-remaining-thai-translation && \
make -j"$(nproc)" CPPFLAGS="-iquote include -Wno-trigraphs -DMODERN=0 -I tools/agbcc/include -I tools/agbcc -nostdinc -undef -std=gnu89 -DTHAI_NAMING_PRODUCTION"
```

### Why this exact command is mandatory

1. `cd ~/dev/projects/pokeemerald-phaseF-remaining-thai-translation`
   - Builds the authoritative Phase F production worktree.
   - Prevents accidentally building another repo, worktree, or obsolete baseline.

2. `make -j"$(nproc)"`
   - Uses the established project build path with the available CPU cores.

3. The complete `CPPFLAGS` value must be preserved:
   - `-iquote include`
   - `-Wno-trigraphs`
   - `-DMODERN=0`
   - `-I tools/agbcc/include`
   - `-I tools/agbcc`
   - `-nostdinc`
   - `-undef`
   - `-std=gnu89`
   - `-DTHAI_NAMING_PRODUCTION`
   - Supplying `CPPFLAGS=` on the command line replaces the value used for that invocation,
     so do not shorten it to only the Thai production macro.

4. `-DTHAI_NAMING_PRODUCTION` is mandatory:
   - It is part of the current production Thai Naming/runtime baseline.
   - It affects runtime structures and behavior used by the Thai player-name implementation.
   - Building without the production configuration previously caused Thai player-name,
     Trainer Card, and runtime/save-layout mismatch symptoms.

5. Use `CPPFLAGS`, not `CFLAGS`:
   - This is a preprocessor configuration for the agbcc build path.

### Build discipline

- ROM-affecting source/asset change -> run the authoritative Production Build once.
- If the Production Build passes and there is no new reproducible failure -> Build Gate CLOSED.
- Do not routinely run `make clean`.
- Docs/tracker-only changes require no ROM rebuild.
- Do not use bare `make` as the authoritative closure build.
- Record EWRAM / IWRAM / ROM from the successful production build.
