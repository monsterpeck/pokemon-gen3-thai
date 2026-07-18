# Obsolete Thai precomposed experiments

The Phase 3/4 longest-match encoder, review-sheet workflow, candidate generator,
and precomposed cluster constants are retained only as recovery evidence.

They are not part of the production build or normal translation workflow.
Production Thai strings use literal single-codepoint Unicode mappings and are
shaped by the combining renderer in `src/text.c`.

Archived tests are retained under `tools/thai/archive/precomposed/tests/`.
