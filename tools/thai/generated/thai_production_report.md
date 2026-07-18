# Thai production contextual shaping report

## Architecture

Natural Unicode Thai is shaped by HarfBuzz during the build, analyzed by Unicode
cluster, fitted through the ordered production candidates, and encoded as compact
positioned-glyph commands. The unchanged runtime only draws the selected bitmap
with its precomputed offset and advance; it contains no Thai grammar.

## Fit and contextual selection

The solver renders proof-identical normal cells first, measures combined visible
bounds against rows 0–15, tests silhouette separation only where base and upper
mark pixels overlap horizontally, then tries base clearance, compact upper marks,
compact tones, and combined high-stack forms in increasing transformation order.
It fails rather than cropping an unsolved cluster. Tall bases use the permitted
one-row nearest-neighbor reduction before their contextual downshift.

Palette convention is fixed: index 0 transparent, index 1 dark main stroke, and
index 2 light shadow. The sheet remains indexed mode P.

## Generated variants

{'compact_tone': 1, 'compact_tone_high': 2, 'compact_upper_mark_high': 1, 'normal': 31, 'upper_clearance_2': 3}

Applied transformations: [('uni0E0D', 'upper_clearance_2'), ('uni0E19', 'upper_clearance_2'), ('uni0E35', 'compact_upper_mark_high'), ('uni0E48.small', 'compact_tone'), ('uni0E48.small', 'compact_tone_high'), ('uni0E49.small', 'compact_tone_high')]

The trace records every selected index, original index, bound, offset adjustment,
advance, and palette count. Normal cells remain proof-identical. Differences in
the difference proof occur only for selected contextual variants.

## Verification

- ROM SHA256: `25b9f7e12e0872d905ad3d94e0b5eea571af2f00b3be2c45d36952f7d895b675`
- linked font asset SHA256: `57b50be33fa42a1a8854dee0de31baf9af28561d9c7978cb4ee65b57ef0b5719`
- temporary X/square probes: absent
- menu source: natural Unicode `เริ่มเกมส์`
- known limitation: 16-pixel fitting requires controlled contextual bitmap forms;
  emulator visual review remains mandatory.

This milestone is not release-ready until the rebuilt ROM is reviewed in an
emulator screenshot.
