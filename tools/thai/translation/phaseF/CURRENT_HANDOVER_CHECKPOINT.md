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
