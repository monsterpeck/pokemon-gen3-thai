#!/usr/bin/env python3

from __future__ import annotations

import csv
import re
import sys
from io import StringIO
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

MOVE_FILE = (
    ROOT
    / "tools/thai/translation/inventory/move_descriptions.csv"
)

ITEM_FILE = (
    ROOT
    / "tools/thai/translation/inventory/"
    "item_description_strings.csv"
)

OUTPUT_FILE = (
    ROOT
    / "tools/thai/translation/glossary.csv"
)


GLOSSARY_TSV = """term_en	term_th	category	status	match_mode	excluded_phrases	notes
POKéMON	โปเกมอน	general	locked	ignore_case		Generic species term, not an individual Pokémon name.
foe	คู่ต่อสู้	battle_actor	locked	ignore_case		Includes possessive forms such as foe's.
user	ผู้ใช้ท่า	battle_actor	locked	ignore_case		The Pokémon using the move.
target	เป้าหมาย	battle_actor	locked	ignore_case		Approved project terminology.
damage	ความเสียหาย	battle_effect	locked	ignore_case		Approved project terminology.
critical hit	การโจมตีคริติคอล	battle_effect	locked	ignore_case		Source variants include critical-hit and critical-hit ratio; 14 semantic occurrences were audited.
status problem	สถานะผิดปกติ	status	locked	ignore_case		Source commonly uses the plural status problems; 5 semantic occurrences were audited.
flinch	ชะงัก	status	locked	ignore_case		Covers flinch, flinches, and flinching; 13 semantic occurrences were audited.
confusion	สับสน	status	locked	ignore_case		Approved project terminology.
paralysis	อัมพาต	status	locked	ignore_case		Approved project terminology.
burn	ไหม้	status	locked	ignore_case		Covers burn and inflected forms; translate according to noun, verb, or status context. 16 semantic occurrences audited.
freeze	แช่แข็ง	status	locked	ignore_case		Covers freeze, freezing, and frozen; translate according to context. 7 semantic occurrences audited.
poison	พิษ	status	locked	ignore_case		Covers poison and inflected forms; translate according to noun, verb, or status context. 17 semantic occurrences audited.
sleep	หลับ	status	locked	ignore_case		Covers sleep, sleeping, and asleep; translate according to context. 15 semantic occurrences audited.
recoil	ความเสียหายสะท้อนกลับ	battle_effect	locked	ignore_case		Approved project terminology for future text; not present in the current description corpus.
held item	ไอเทมที่ถืออยู่	item	locked	ignore_case		Approved project terminology.
raises	เพิ่ม	stat_change	locked	ignore_case	sharply raises	Covers the normal stat-increase concept. Translate longer phrases such as sharply raises first. 78 raise-form occurrences were audited.
lowers	ลด	stat_change	locked	ignore_case	sharply lowers	Covers the normal stat-decrease concept. Translate longer phrases such as sharply lowers first. 43 lower-form occurrences were audited.
sharply raises	เพิ่มอย่างมาก	stat_change	locked	ignore_case		Higher priority than raises.
sharply lowers	ลดอย่างมาก	stat_change	locked	ignore_case		Higher priority than lowers.
restores	ฟื้นฟู	recovery	locked	ignore_case		Covers restore and inflected forms; 38 semantic occurrences were audited.
recovers	ฟื้นฟู	recovery	locked	ignore_case		Covers recover and inflected forms; 5 semantic occurrences were audited.
prevents	ป้องกัน	battle_effect	locked	ignore_case		Approved project terminology.
turn	เทิร์น	battle_time	locked	ignore_case		Approved project terminology.
weather	สภาพอากาศ	weather	locked	ignore_case		Approved project terminology.
rain	ฝน	weather	locked	ignore_case		Approved weather terminology; not present as a standalone word in the current corpus.
sunlight	แดดจ้า	weather	locked	ignore_case		Approved project terminology.
sandstorm	พายุทราย	weather	locked	ignore_case		Approved project terminology.
hail	ลูกเห็บ	weather	locked	ignore_case		Approved weather terminology; not present as a standalone word in the current corpus.
HP	HP	abbreviation	locked	exact_case		Keep the standard abbreviation.
PP	PP	abbreviation	locked	exact_case		Keep the standard abbreviation.
EXP	EXP	abbreviation	locked	exact_case		Keep the standard abbreviation.
TM	TM	abbreviation	locked	exact_case		Keep the standard abbreviation.
HM	HM	abbreviation	locked	exact_case		Keep the standard abbreviation.
ATTACK	พลังโจมตี	stat	locked	exact_case		Uppercase stat label only; lowercase attack is a normal noun.
DEFENSE	พลังป้องกัน	stat	locked	exact_case		Uppercase stat label only.
SPEED	ความเร็ว	stat	locked	exact_case		Uppercase stat label only; lowercase speed may be ordinary prose.
SP. ATK	พลังโจมตีพิเศษ	stat	locked	exact_case		Uppercase abbreviated stat label only.
SP. DEF	พลังป้องกันพิเศษ	stat	locked	exact_case		Uppercase abbreviated stat label only.
"""


EXPECTED_COUNTS = {
    "ATTACK": (24, 24),
    "DEFENSE": (24, 24),
    "SPEED": (17, 17),
    "raises": (62, 58),
    "sharply raises": (4, 4),
    "lowers": (17, 14),
    "sharply lowers": (3, 3),
}


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        raise FileNotFoundError(f"Missing inventory file: {path}")

    with path.open(
        encoding="utf-8-sig",
        newline="",
    ) as csv_file:
        return list(csv.DictReader(csv_file))


def read_glossary_definition() -> list[dict[str, str]]:
    return list(
        csv.DictReader(
            StringIO(GLOSSARY_TSV),
            delimiter="\t",
        )
    )


def compile_term_pattern(
    term: str,
    match_mode: str,
) -> re.Pattern[str]:
    flags = 0

    if match_mode == "ignore_case":
        flags = re.IGNORECASE
    elif match_mode != "exact_case":
        raise ValueError(
            f"Unsupported match mode for {term}: {match_mode}"
        )

    return re.compile(
        rf"(?<!\w){re.escape(term)}(?!\w)",
        flags,
    )


def find_spans(
    text: str,
    term: str,
    match_mode: str,
) -> list[tuple[int, int]]:
    pattern = compile_term_pattern(term, match_mode)

    return [
        match.span()
        for match in pattern.finditer(text)
    ]


def count_term_in_text(
    text: str,
    term: str,
    match_mode: str,
    excluded_phrases: list[str],
) -> tuple[int, int]:
    term_spans = find_spans(
        text,
        term,
        match_mode,
    )

    excluded_spans: list[tuple[int, int]] = []

    for phrase in excluded_phrases:
        excluded_spans.extend(
            find_spans(
                text,
                phrase,
                match_mode,
            )
        )

    allowed_spans = [
        term_span
        for term_span in term_spans
        if not any(
            excluded_start <= term_span[0]
            and term_span[1] <= excluded_end
            for excluded_start, excluded_end
            in excluded_spans
        )
    ]

    return len(term_spans), len(allowed_spans)


def main() -> int:
    if OUTPUT_FILE.exists():
        print(
            "ERROR: Glossary already exists. "
            "Refusing to overwrite review work:",
            file=sys.stderr,
        )
        print(f"  {OUTPUT_FILE}", file=sys.stderr)
        return 1

    move_rows = read_csv(MOVE_FILE)
    item_rows = read_csv(ITEM_FILE)
    glossary_rows = read_glossary_definition()

    pending_items = [
        row
        for row in item_rows
        if row["status"] == "pending"
    ]

    errors: list[str] = []

    if len(move_rows) != 354:
        errors.append(
            f"Expected 354 move rows, found {len(move_rows)}"
        )

    if len(item_rows) != 310:
        errors.append(
            f"Expected 310 item rows, found {len(item_rows)}"
        )

    if len(pending_items) != 309:
        errors.append(
            "Expected 309 pending item descriptions, "
            f"found {len(pending_items)}"
        )

    if len(glossary_rows) != 39:
        errors.append(
            "Expected 39 glossary definitions, "
            f"found {len(glossary_rows)}"
        )

    normalized_terms = [
        row["term_en"].casefold()
        for row in glossary_rows
    ]

    duplicate_terms = sorted(
        term
        for term in set(normalized_terms)
        if normalized_terms.count(term) > 1
    )

    if duplicate_terms:
        errors.append(
            f"Duplicate glossary terms: {duplicate_terms}"
        )

    entries: list[dict[str, str]] = []

    for row in move_rows:
        entries.append(
            {
                "reference": row["move_id"],
                "source_text": row["source_text"],
            }
        )

    for row in pending_items:
        entries.append(
            {
                "reference": row["description_symbol"],
                "source_text": row["source_text"],
            }
        )

    if len(entries) != 663:
        errors.append(
            f"Expected 663 corpus entries, found {len(entries)}"
        )

    output_rows: list[dict[str, object]] = []

    for glossary_row in glossary_rows:
        term = glossary_row["term_en"]
        match_mode = glossary_row["match_mode"]

        excluded_phrases = [
            phrase.strip()
            for phrase
            in glossary_row["excluded_phrases"].split("|")
            if phrase.strip()
        ]

        raw_count = 0
        occurrence_count = 0
        example_refs: list[str] = []

        for entry in entries:
            raw_matches, allowed_matches = count_term_in_text(
                entry["source_text"],
                term,
                match_mode,
                excluded_phrases,
            )

            raw_count += raw_matches
            occurrence_count += allowed_matches

            if (
                allowed_matches > 0
                and entry["reference"] not in example_refs
                and len(example_refs) < 3
            ):
                example_refs.append(entry["reference"])

        output_rows.append(
            {
                "term_en": term,
                "term_th": glossary_row["term_th"],
                "category": glossary_row["category"],
                "status": glossary_row["status"],
                "match_mode": match_mode,
                "excluded_phrases": " | ".join(
                    excluded_phrases
                ),
                "raw_occurrence_count": raw_count,
                "occurrence_count": occurrence_count,
                "example_refs": " | ".join(example_refs),
                "notes": glossary_row["notes"],
            }
        )

    output_by_term = {
        str(row["term_en"]): row
        for row in output_rows
    }

    for term, expected in EXPECTED_COUNTS.items():
        row = output_by_term.get(term)

        if row is None:
            errors.append(
                f"Expected semantic audit term missing: {term}"
            )
            continue

        actual = (
            int(row["raw_occurrence_count"]),
            int(row["occurrence_count"]),
        )

        if actual != expected:
            errors.append(
                f"{term}: expected counts {expected}, "
                f"found {actual}"
            )

    locked_expected = {
        str(row["term_en"])
        for row in output_rows
    }

    locked_actual = {
        str(row["term_en"])
        for row in output_rows
        if row["status"] == "locked"
    }

    if locked_actual != locked_expected:
        errors.append(
            "Not all glossary terms are locked: "
            f"{sorted(locked_expected - locked_actual)}"
        )

    translated_abbreviations = [
        str(row["term_en"])
        for row in output_rows
        if (
            row["category"] == "abbreviation"
            and row["term_en"] != row["term_th"]
        )
    ]

    if translated_abbreviations:
        errors.append(
            "Standard abbreviations were translated: "
            f"{translated_abbreviations}"
        )

    print("=== GLOSSARY SOURCE AUDIT ===")
    print(f"Move descriptions : {len(move_rows)}")
    print(f"Item descriptions : {len(pending_items)}")
    print(f"Corpus entries    : {len(entries)}")
    print(f"Glossary entries  : {len(output_rows)}")
    print(f"Duplicate terms   : {len(duplicate_terms)}")
    print(f"Validation errors : {len(errors)}")

    print()
    print("=== SEMANTIC COUNT CHECK ===")

    for term in EXPECTED_COUNTS:
        row = output_by_term[term]

        print(
            f"{term:20} "
            f"raw={int(row['raw_occurrence_count']):3} "
            f"effective={int(row['occurrence_count']):3} "
            f"mode={row['match_mode']}"
        )

    if errors:
        print()
        print("ERRORS:")

        for error in errors:
            print(f"- {error}")

        return 1

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    temporary_file = OUTPUT_FILE.with_suffix(".csv.tmp")

    try:
        with temporary_file.open(
            "w",
            encoding="utf-8-sig",
            newline="",
        ) as csv_file:
            writer = csv.DictWriter(
                csv_file,
                fieldnames=[
                    "term_en",
                    "term_th",
                    "category",
                    "status",
                    "match_mode",
                    "excluded_phrases",
                    "raw_occurrence_count",
                    "occurrence_count",
                    "example_refs",
                    "notes",
                ],
                lineterminator="\n",
            )

            writer.writeheader()
            writer.writerows(output_rows)

        temporary_file.replace(OUTPUT_FILE)

    finally:
        if temporary_file.exists():
            temporary_file.unlink()

    zero_terms = [
        str(row["term_en"])
        for row in output_rows
        if int(row["occurrence_count"]) == 0
    ]

    print()
    print("=== ZERO-OCCURRENCE TERMS ===")

    if zero_terms:
        for term in zero_terms:
            print(f"- {term}")
    else:
        print("None")

    print()
    print(f"Created: {OUTPUT_FILE.relative_to(ROOT)}")
    print(
        "PASS: Semantically corrected glossary "
        "created successfully."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
