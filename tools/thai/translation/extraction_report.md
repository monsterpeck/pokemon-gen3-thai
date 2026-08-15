# Dialogue extraction report

Extractor version: `1.0.0`

## Coverage

Scanned `data/maps`, `data/scripts`, `data/text`, `src`, and `include` recursively. Supports assembly `.string` labels and C `_()` declarations, adjacent fragments, escaped quotes, controls, and placeholders.

- Total entries: 17250
- Main-story entries: 191
- Unknown entries: 0
- Duplicate groups: 1000
- Entries with placeholders: 2430
- Entries with control codes: 9696

## Files skipped

- Archived, backup, generated, debug-fixture, and temporary-probe paths are excluded by rule.

## Limitations

Classification is intentionally conservative and based on source paths and labels. Static extraction cannot prove every runtime call path, speaker, or narrative dependency. Only the dedicated opening speech receives a deterministic story order; uncertain order remains blank. Current non-English source text is preserved verbatim.

## Recommended translation workflow

Translate the main-story CSV first while preserving every control code and placeholder, then translate NPC and system inventories. Keep IDs and source metadata unchanged.

No game source, existing dialogue, renderer, font asset, charmap, or Thai shaping file was modified.

