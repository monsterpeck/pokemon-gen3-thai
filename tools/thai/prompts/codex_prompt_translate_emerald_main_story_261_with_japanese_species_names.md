# Codex Prompt — Translate Pokémon Emerald Main Story (261 Rows)

Workspace:

```text
/home/luffy/dev/projects/pokeemerald
```

```text
Translate all 261 verified mandatory Pokémon Emerald main-story dialogue rows
into Thai.

The mandatory-story scope has already been corrected and validated:

- 261 mandatory dialogue rows retained
- 173 optional/postgame rows removed
- 45 mandatory story events preserved
- IDs are unique
- global_order is contiguous from 1 through 261
- all chronology and scope validation passes
- map-period and chapter splits match the ordered master
- known false positives are absent
- all Thai fields remain empty
- all translation_status values remain untranslated
- repeated generation is byte-identical

This task translates the complete mandatory story database as one batch because
261 rows falls within the requested 200–300 row batch size.

Do not perform another broad scope reclassification unless validation detects a
specific concrete error.

Do not inject translations into game source.
Do not build the ROM.
Do not modify fonts, renderer, charmap, or shaping code.
Do not commit automatically.

WORKSPACE

/home/luffy/dev/projects/pokeemerald

SOURCE OF TRUTH

Use these unchanged source files:

tools/thai/translation/story_order/dialogue_main_story_ordered.csv
tools/thai/translation/story_order/story_events.csv
tools/thai/translation/story_order/dialogue_event_links.csv
tools/thai/translation/story_order/scope_audit.csv
tools/thai/translation/story_order/coverage_report.md
tools/thai/translation/story_order/scope_corrections_report.md
tools/thai/translation/story_order/maps/
tools/thai/translation/story_order/chapters/

FILES THAT MUST NOT BE MODIFIED

Do not modify:

- data/maps/**
- data/scripts/**
- data/text/**
- src/**
- include/**
- graphics/**
- charmap.txt
- font assets
- renderer code
- Thai shaping code
- ROM assets
- script_graph.json
- story_events.csv
- dialogue_event_links.csv
- scope_audit.csv
- dialogue_main_story_ordered.csv
- existing map-period source CSV files
- existing chapter source CSV files

PREREQUISITE VALIDATION

Before translating, run:

make check-story-scope
make test-story-scope

Verify:

1. dialogue_main_story_ordered.csv contains exactly 261 rows.
2. global_order is contiguous from 1 through 261.
3. Every row has a nonempty stable ID.
4. Every row has a nonempty event_id.
5. There are no duplicate IDs.
6. Every Thai field is empty.
7. Every translation_status is untranslated.
8. Every ordered row is marked mandatory in scope_audit.csv.
9. Every ordered row has a mandatory dialogue-event link.
10. No mandatory coverage sequence is missing.
11. Map-period files together equal the ordered master.
12. Chapter files together equal the ordered master.
13. Known optional and postgame false positives are absent.
14. Story-scope generation remains deterministic.

If validation fails:

- stop immediately
- do not create a partial translation
- do not create incomplete glossary files
- print the exact blocker

OUTPUT STRUCTURE

Create:

tools/thai/translation/story_order/translation/
tools/thai/translation/story_order/translation/batches/
tools/thai/translation/story_order/translation/maps/
tools/thai/translation/story_order/translation/chapters/
tools/thai/translation/story_order/translation/reviews/
tools/thai/translation/story_order/translation/reviews/maps/
tools/thai/translation/story_order/translation/reviews/chapters/

TRANSLATION BATCH

Translate all 261 rows in ascending global_order.

Create:

tools/thai/translation/story_order/translation/batches/
batch_001_complete_main_story.csv

Batch 001 must:

- begin at global_order 1
- end at global_order 261
- contain exactly 261 rows
- contain every ordered master ID exactly once
- preserve chronological order
- not skip any row
- not add any optional or postgame row

MASTER THAI FILE

Create:

tools/thai/translation/story_order/translation/
dialogue_main_story_thai.csv

This must contain exactly the same 261 source rows and source metadata as
dialogue_main_story_ordered.csv, with Thai translation and review fields added.

Use exactly these columns:

id
global_order
chapter_order
chapter_id
chapter_title_en
chapter_title_th
event_order
event_id
event_title_en
event_title_th
map_order
map_name
map_period
location_name
dialogue_order
speaker
script_label
source_file
source_line
source_label
english_raw
english_preview
thai
translation_status
control_codes
placeholders
chronology_confidence
scope_confidence
translation_confidence
term_review
length_review
translation_notes

SOURCE FIELD PRESERVATION

Copy the following fields from dialogue_main_story_ordered.csv without changing
them:

- id
- global_order
- chapter_order
- chapter_id
- event_order
- event_id
- map_order
- map_name
- map_period
- location_name
- dialogue_order
- speaker
- script_label
- source_file
- source_line
- source_label
- english_raw
- english_preview
- control_codes
- placeholders
- chronology_confidence
- scope_confidence

Do not normalize, correct, rewrite, or reformat english_raw.

Do not alter stable IDs, source labels, source paths, source lines, events, map
periods, or chronology.

CSV requirements:

- UTF-8 with BOM
- proper CSV quoting
- preserved multiline fields
- deterministic ordering
- no replacement characters
- no Markdown code fences inside fields

THAI TRANSLATION STYLE

Translate every row into polished, natural Thai suitable for a Pokémon Game Boy
Advance localization.

Prioritize:

- original meaning
- story context
- speaker personality
- natural Thai sentence structure
- concise presentation
- readability on a small GBA dialogue box
- consistent terminology
- consistent character and place names

Avoid:

- mechanical word-for-word translation
- English sentence structure copied unnaturally into Thai
- excessive formal language
- excessive polite particles
- unnecessary spaces between Thai words
- modern internet slang
- unsupported gender assumptions
- deleting meaning merely to shorten a line

Use spaces where useful between Thai and:

- numbers
- English abbreviations
- placeholders
- symbols
- technical names

Do not add spaces between ordinary Thai words.

SPEAKER TONE

Professor Birch should sound:

- friendly
- knowledgeable
- approachable
- enthusiastic about Pokémon

The rival should sound:

- confident
- energetic
- competitive
- natural for their age
- not unnecessarily rude

Team Aqua and Team Magma must retain:

- their different ideologies
- organizational identity
- dramatic tone
- villainous intent where present

Gym Leaders, Elite Four members, the Champion, scientists, sailors, executives,
children, elders, villains, and officials must retain distinct speech styles.

Do not make every speaker use the same pronouns or polite particles.

Do not invent speaker gender when source evidence is unavailable.

CONTROL CODES

Preserve every required control code.

Examples include:

\n
\p
\l
\v
\c
\x
{COLOR ...}
{PAUSE ...}
{PLAY_SE ...}
{WAIT_SE}
{CLEAR}
{PAUSE_UNTIL_PRESS}

Rules:

- do not translate control-code names
- do not delete control codes
- do not alter required control-code order
- do not remove or add a \p page break silently
- preserve the number and order of pages

A line break \n or \l may be repositioned only when needed for natural Thai
layout.

When repositioning a line break:

- preserve the same page structure
- preserve all visible meaning
- add LINEBREAK_ADJUSTED to translation_notes

If the control-code sequence requires human review, set:

length_review = review_control_codes
translation_confidence = low

and document the exact concern.

PLACEHOLDERS

Preserve every placeholder exactly and in the same sequence.

Examples include:

{PLAYER}
{RIVAL}
{STR_VAR_1}
{STR_VAR_2}
{STR_VAR_3}
{POKEMON}
{POKEBLOCK}
{KUN}
{RUBY}
{SAPPHIRE}

Do not:

- translate placeholder names
- change spelling or capitalization
- add placeholders
- remove placeholders
- reorder placeholders
- insert characters inside placeholders

Validate placeholder names, occurrence counts, and sequence against english_raw.

TRANSLATION STATUS

For every translated row set:

translation_status = draft_review

Set translation_confidence to exactly one of:

high
medium
low

Use:

- high: meaning, context, speaker, and terminology are clear
- medium: translation is clear but tone or terminology needs review
- low: source context, speaker, or terminology is ambiguous

Set term_review to exactly one of:

ok
review

Use review when any proper noun or game term needs human confirmation.

Do not leave Thai empty in a row marked draft_review.

GLOSSARY

Create:

tools/thai/translation/story_order/translation/glossary.csv

Use exactly these columns:

term_type
english
thai
status
first_dialogue_id
first_source
occurrence_count
notes

Allowed term_type values:

character
pokemon
place
item
move
ability
organization
title
technical
recurring_phrase
other

The glossary must contain every proper noun and important recurring game term
encountered in the complete 261-row mandatory story.

Capture at minimum:

- character names
- Pokémon names
- city names
- town names
- route names
- caves
- buildings
- regions
- item names
- Key Item names
- move names
- ability names
- organizations
- Team Aqua
- Team Magma
- Gym titles
- Gym Leader titles
- Professor titles
- Elite Four titles
- Champion title
- Pokémon terminology
- Trainer terminology
- recurring forms of address
- recurring story phrases

GLOSSARY RULES

The glossary is the authoritative terminology source for all later source
injection and editing.

Use one row per normalized English term.

Do not create duplicate entries caused by:

- capitalization differences
- surrounding whitespace
- punctuation differences
- pluralization of the same proper noun
- abbreviation variants referring to the same entity

Use one Thai spelling consistently throughout all 261 rows.

Do not silently use multiple Thai spellings for the same:

- person
- Pokémon
- city
- town
- route
- location
- item
- organization
- title

For every glossary entry:

- status = draft when the Thai spelling is confidently selected
- status = review when human confirmation is required

For Pokémon names:

- use established Thai Pokémon names only when confidently known
- do not invent a spelling silently
- when uncertain, choose one consistent draft spelling
- mark status = review
- explain alternatives in notes

For character and location names:

- record the first dialogue ID
- record the first source
- calculate occurrence_count deterministically
- list uncertain transliteration alternatives in notes

Do not overwrite an existing glossary decision silently during generation.

TRANSLATION MEMORY

Create:

tools/thai/translation/story_order/translation/translation_memory.csv

Use exactly these columns:

english_normalized
english_raw
thai
usage_count
source_ids
context_variants
status
notes

Rules:

1. Preserve english_raw separately.
2. Normalize English only for matching.
3. Identical English dialogue should normally use the same Thai translation.
4. Context-specific translations are allowed.
5. Document every context-specific variant.
6. source_ids must list all IDs using the memory entry.
7. Do not silently create conflicting translations.
8. status must be draft or review.
9. Output order must be deterministic.

SPEAKER STYLE GUIDE

Create:

tools/thai/translation/story_order/translation/speaker_style_guide.csv

Use exactly these columns:

speaker
role
tone
formality
self_pronoun
listener_pronoun
preferred_particles
avoid
example_english
example_thai
notes

Add recurring speakers found in the mandatory story.

Do not invent unsupported:

- gender
- age
- relationship
- title
- role
- personality

Use source labels, script ownership, story context, and dialogue evidence.

When speaker identity is unclear:

- use conservative style guidance
- leave unsupported fields blank
- document uncertainty in notes

LENGTH REVIEW

For every translated row calculate:

- visible English character count excluding control codes
- visible Thai character count excluding control codes
- longest visible English line
- longest visible Thai line
- page count
- placeholder count
- control-code sequence

Set length_review to exactly one of:

ok
review_long_line
review_long_page
review_control_codes

Use review_long_line when a Thai line is likely too wide for a GBA dialogue box.

Use review_long_page when a translated page is significantly longer than the
English source and may overflow or feel crowded.

Do not remove meaning merely to obtain an ok result.

Create:

tools/thai/translation/story_order/translation/
main_story_length_review.csv

Use exactly these columns:

id
global_order
chapter_id
event_id
map_name
map_period
speaker
source_label
english_visible_length
thai_visible_length
longest_english_line
longest_thai_line
page_count
placeholder_count
control_code_sequence
result
notes

MAP-PERIOD TRANSLATION FILES

Create translated map-period CSV files under:

tools/thai/translation/story_order/translation/maps/

Use the same chronological filenames as the verified source map-period files,
adding `_thai` before `.csv`.

Examples:

001_Global_opening_thai.csv
002_LittlerootTown_BrendansHouse_1F_arrival_thai.csv
003_LittlerootTown_BrendansHouse_1F_rival_intro_thai.csv

Requirements:

- every translated master row appears in exactly one map-period file
- no row is lost
- no row is duplicated
- map files together exactly equal dialogue_main_story_thai.csv
- preserve chronological map-period ordering

CHAPTER TRANSLATION FILES

Create translated chapter CSV files under:

tools/thai/translation/story_order/translation/chapters/

Use filenames based on the source chapter files, adding `_thai` before `.csv`.

Examples:

01_opening_thai.csv
02_littleroot_thai.csv
03_pokedex_thai.csv

Requirements:

- every translated master row appears in exactly one chapter file
- no row is lost
- no row is duplicated
- chapter files together exactly equal dialogue_main_story_thai.csv

REVIEW DOCUMENTS

Create the master review file:

tools/thai/translation/story_order/translation/reviews/
main_story_translation_review.md

Group in this order:

chapter
-> event
-> map period
-> global order

For every row show:

- stable ID
- global order
- chapter
- event
- map
- map period
- speaker
- source label
- English preview
- Thai translation
- placeholders
- control codes
- translation confidence
- glossary terms used
- term review
- length review
- translation notes

Create one map-period review file under:

tools/thai/translation/story_order/translation/reviews/maps/

Create one chapter review file under:

tools/thai/translation/story_order/translation/reviews/chapters/

Every translated row must appear in:

- the master review
- exactly one map-period review
- exactly one chapter review

Do not omit low-confidence or review-required entries.

PROGRESS FILE

Create:

tools/thai/translation/story_order/translation/
translation_progress.json

Include:

- source_database
- total_ordered_dialogue_rows
- total_translated_rows
- total_untranslated_rows
- completed_batches
- current_batch
- batch_start_global_order
- batch_end_global_order
- batch_row_count
- remaining_untranslated_row_count
- chapters_touched
- events_touched
- maps_touched
- map_periods_touched
- glossary_term_count
- glossary_review_count
- translation_memory_entry_count
- speaker_style_entry_count
- translation_confidence_counts
- term_review_counts
- length_review_counts
- generated_files
- notes

Required Batch 001 progress values:

- total_ordered_dialogue_rows = 261
- total_translated_rows = 261
- total_untranslated_rows = 0
- completed_batches includes batch_001_complete_main_story
- batch_start_global_order = 1
- batch_end_global_order = 261
- batch_row_count = 261
- remaining_untranslated_row_count = 0

TRANSLATION REPORT

Create:

tools/thai/translation/story_order/translation/
main_story_translation_report.md

Include:

- source scope validation result
- total mandatory dialogue rows
- translated rows
- untranslated rows
- chapter count
- event count
- map-period count
- high/medium/low translation-confidence counts
- glossary term count
- glossary terms marked review
- translation-memory entry count
- speaker-style entry count
- length-review counts
- control-code review count
- terms requiring human confirmation
- dialogue requiring tone review
- dialogue requiring length review
- confirmation that original English source remains unchanged
- confirmation that game source files were not modified
- confirmation that translation was not injected
- confirmation that the ROM was not built

VALIDATION SCRIPT

Create:

tools/thai/validate_main_story_translation.py

Validate:

1. Story-scope validation still passes.
2. Ordered master contains exactly 261 rows.
3. Thai master contains exactly 261 rows.
4. Batch 001 contains exactly 261 rows.
5. Global order is contiguous from 1 through 261.
6. Batch and Thai master IDs exactly equal the ordered source IDs.
7. No unexpected IDs exist.
8. No duplicate IDs exist.
9. No source row is missing.
10. english_raw remains unchanged.
11. Source paths, source lines, source labels, event IDs, and map periods remain
    unchanged.
12. Every Thai field is nonempty.
13. Every translation_status is draft_review.
14. translation_confidence values are permitted.
15. term_review values are permitted.
16. length_review values are permitted.
17. Placeholder names, order, and counts are unchanged.
18. Required control-code sequence is preserved.
19. Glossary English keys are unique.
20. Glossary Thai spellings are used consistently.
21. Translation-memory conflicts are reported.
22. Every recurring speaker has consistent style guidance where evidence exists.
23. Map-period translated files exactly equal the Thai master.
24. Chapter translated files exactly equal the Thai master.
25. Every row appears in the master review.
26. Every row appears in exactly one map-period review.
27. Every row appears in exactly one chapter review.
28. Length-review CSV contains every translated ID exactly once.
29. Progress counts match actual files.
30. All CSV files use UTF-8 with BOM.
31. No replacement character U+FFFD exists.
32. No accidental Markdown code fences occur inside CSV fields.
33. No original game dialogue source was modified.
34. No font, renderer, charmap, or shaping source was modified.
35. No ROM output was created by this task.
36. Generation order and generated metadata are deterministic.

TESTS

Create:

tools/thai/tests/test_main_story_translation.py

Test:

- complete 261-row preservation
- full ID equality
- chronological ordering
- English raw preservation
- placeholder preservation
- control-code preservation
- glossary key uniqueness
- glossary spelling consistency
- translation-memory conflict detection
- speaker-style validation
- translation status validation
- confidence validation
- term-review validation
- length-review generation
- map split completeness
- chapter split completeness
- master review coverage
- map review coverage
- chapter review coverage
- progress count accuracy
- UTF-8 BOM output
- no source modification
- no font or renderer modification
- deterministic ordering and metadata

MAKE TARGETS

Add these targets without changing normal ROM build behavior:

make check-main-story-translation
make test-main-story-translation

Do not add a target that automatically overwrites human-reviewed Thai
translations.

RUN

Run:

git diff --check
make check-story-scope
make test-story-scope
make check-main-story-translation
make test-main-story-translation
python3 -B -m unittest tools.thai.tests.test_main_story_translation -v

Run validation twice and confirm identical results.

Do not run make for the ROM.
Do not inject Thai into source dialogue.
Do not commit automatically.

AT COMPLETION PRINT

pwd
git branch --show-current
git status --short
git diff --stat
git diff --check

make check-story-scope
make test-story-scope
make check-main-story-translation
make test-main-story-translation

python3 - <<'PY'
import csv
import json
from collections import Counter
from pathlib import Path

root = Path(
    "tools/thai/translation/story_order/translation"
)

master_path = root / "dialogue_main_story_thai.csv"
batch_path = root / "batches/batch_001_complete_main_story.csv"
glossary_path = root / "glossary.csv"
memory_path = root / "translation_memory.csv"
speaker_path = root / "speaker_style_guide.csv"
length_path = root / "main_story_length_review.csv"
progress_path = root / "translation_progress.json"

def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))

master = read_csv(master_path)
batch = read_csv(batch_path)
glossary = read_csv(glossary_path)
memory = read_csv(memory_path)
speakers = read_csv(speaker_path)
length_rows = read_csv(length_path)
progress = json.loads(progress_path.read_text(encoding="utf-8"))

orders = [int(row["global_order"]) for row in master]

print("master rows:", len(master))
print("batch rows:", len(batch))
print("start global order:", min(orders))
print("end global order:", max(orders))
print(
    "translated rows:",
    sum(bool(row["thai"].strip()) for row in master),
)
print(
    "translation statuses:",
    dict(sorted(Counter(row["translation_status"] for row in master).items())),
)
print(
    "translation confidence:",
    dict(sorted(Counter(row["translation_confidence"] for row in master).items())),
)
print(
    "term review:",
    dict(sorted(Counter(row["term_review"] for row in master).items())),
)
print(
    "length review:",
    dict(sorted(Counter(row["length_review"] for row in master).items())),
)
print("glossary terms:", len(glossary))
print(
    "glossary review terms:",
    sum(row["status"] == "review" for row in glossary),
)
print("translation-memory entries:", len(memory))
print("speaker-style entries:", len(speakers))
print("length-review rows:", len(length_rows))
print("progress:", progress)
PY

find tools/thai/translation/story_order/translation -maxdepth 3 -type f \
  -printf '%p %s bytes\n' | sort
```

---

POKÉMON NAME POLICY — AUTHORITATIVE OVERRIDE

This section overrides any earlier generic Pokémon naming guidance in this
prompt.

Use Japanese-based Thai Pokémon species names from the project reference CSV.

Required reference file:

tools/thai/translation/reference/species_names_th.csv

Required mapping path:

English species name in pokeemerald
-> internal species ID
-> Japanese species name
-> Thai name from species_names_th.csv

Rules:

1. Match Pokémon species by internal species ID only.
2. Do not match species using approximate spelling.
3. Do not transliterate the English species name.
4. Do not replace the CSV spelling with English-based Thai names.
5. Do not replace the CSV spelling with names from another Thai localization
   silently.
6. Ignore rows whose status is SYSTEM_RESERVED.
7. Preserve translation_th exactly for dialogue and glossary usage.
8. Import referenced active species into glossary.csv with:
   term_type = pokemon
9. Map source statuses as follows:
   LOCKED_GLOSSARY -> locked
   TRANSLATED_DRAFT -> draft
   NEEDS_REVIEW_GLOSSARY_CHANGE -> review
10. When a CSV spelling appears questionable:
    - keep the CSV spelling in the translated dialogue
    - set term_review = review
    - record the proposed alternative in translation_notes and glossary notes
11. Do not modify species_names_th.csv during this translation task.
12. Validate that every referenced Pokémon species has exactly one internal-ID
    mapping and exactly one Thai name.
13. Build and preserve a deterministic English-to-Japanese-to-Thai species
    cross-reference for later source injection.
14. The glossary spelling from species_names_th.csv is authoritative throughout
    all 261 translated dialogue rows.

Examples:

BULBASAUR -> フシギダネ -> ฟุชิกิดาเนะ
CHARMANDER -> ヒトカゲ -> ฮิโตคาเงะ
TREECKO -> キモリ -> คิโมริ

Do not use:

BULBASAUR -> บัลบาซอร์
CHARMANDER -> ชาร์แมนเดอร์
TREECKO -> ทรีคโค

