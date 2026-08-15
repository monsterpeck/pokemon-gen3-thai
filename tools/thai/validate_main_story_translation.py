#!/usr/bin/env python3
"""Validate the completed 261-row Phase B translation and support artifacts."""
import csv
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STORY = ROOT / "tools/thai/translation/story_order"
TRANS = STORY / "translation"
SOURCE = STORY / "dialogue_main_story_ordered.csv"
MASTER = TRANS / "dialogue_main_story_thai.csv"
BATCH = TRANS / "batches/batch_001_complete_main_story.csv"
SOURCE_FIELDS = ("id global_order chapter_order chapter_id event_order event_id map_order map_name map_period "
                 "location_name dialogue_order speaker script_label source_file source_line source_label english_raw "
                 "english_preview control_codes placeholders chronology_confidence scope_confidence").split()
PLACEHOLDER_RE = re.compile(r"\{(?!COLOR\b|PAUSE\b|PLAY_SE\b|WAIT_SE\b|CLEAR\b|PAUSE_UNTIL_PRESS\b)[A-Z][A-Z0-9_]*\}")
CONTROL_RE = re.compile(r"\\[pnlvcx](?:\[[^]]*\])?|\{(?:COLOR|PAUSE|PLAY_SE|WAIT_SE|CLEAR|PAUSE_UNTIL_PRESS)(?: [^}]*)?\}")
ID_MARKER_RE = re.compile(r"<!-- dialogue-id: ([a-z0-9_]+) -->")


def read_csv(path):
    if not path.read_bytes().startswith(b"\xef\xbb\xbf"):
        raise ValueError(f"{path.relative_to(ROOT)}: missing UTF-8 BOM")
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def controls(text):
    return CONTROL_RE.findall(text)


def required_controls(text):
    return [item for item in controls(text) if item not in {r"\n", r"\l"}]


def split_rows(directory):
    result = []
    for path in sorted(directory.glob("*.csv")):
        result.extend(read_csv(path))
    return result


def review_ids(path):
    return ID_MARKER_RE.findall(path.read_text(encoding="utf-8"))


def git_changed_protected():
    protected = ["data/maps", "data/scripts", "data/text", "src", "include", "graphics", "charmap.txt"]
    run = subprocess.run(["git", "diff", "--name-only", "--", *protected], cwd=ROOT,
                         text=True, capture_output=True, check=True)
    return [line for line in run.stdout.splitlines() if line]


def validation_errors(run_scope=True):
    errors = []
    def check(condition, message):
        if not condition:
            errors.append(message)
    try:
        if run_scope:
            scope = subprocess.run([sys.executable, "-B", "tools/thai/validate_story_scope.py"], cwd=ROOT,
                                   text=True, capture_output=True)
            check(scope.returncode == 0, "story-scope validation failed: " + (scope.stderr.strip() or scope.stdout.strip()))
        source, master, batch = read_csv(SOURCE), read_csv(MASTER), read_csv(BATCH)
        check(len(source) == 261, f"ordered source row count is {len(source)}, expected 261")
        check(len(master) == 261, f"Thai master row count is {len(master)}, expected 261")
        check(len(batch) == 261, f"Batch 001 row count is {len(batch)}, expected 261")
        source_ids, master_ids, batch_ids = ([r["id"] for r in group] for group in (source, master, batch))
        expected_orders = list(range(1, 262))
        check([int(r["global_order"]) for r in master] == expected_orders, "Thai master global_order is not contiguous 1..261")
        check(master_ids == source_ids, "Thai master IDs/order differ from ordered source")
        check(batch_ids == source_ids, "Batch 001 IDs/order differ from ordered source")
        check(len(set(master_ids)) == len(master_ids), "duplicate Thai master IDs")
        source_by_id = {r["id"]: r for r in source}
        for row in master:
            original = source_by_id.get(row["id"])
            if not original:
                continue
            changed = [field for field in SOURCE_FIELDS if row.get(field) != original.get(field)]
            check(not changed, f'{row["id"]}: source fields changed: {", ".join(changed)}')
            check(bool(row["thai"].strip()), f'{row["id"]}: empty Thai translation')
            check(row["translation_status"] == "draft_review", f'{row["id"]}: invalid translation_status')
            check(row["translation_confidence"] in {"high", "medium", "low"}, f'{row["id"]}: invalid confidence')
            check(row["term_review"] in {"ok", "review"}, f'{row["id"]}: invalid term_review')
            check(row["length_review"] in {"ok", "review_long_line", "review_long_page", "review_control_codes"},
                  f'{row["id"]}: invalid length_review')
            check(PLACEHOLDER_RE.findall(row["thai"]) == PLACEHOLDER_RE.findall(row["english_raw"]),
                  f'{row["id"]}: placeholder sequence differs')
            check(required_controls(row["thai"]) == required_controls(row["english_raw"]),
                  f'{row["id"]}: required control-code sequence differs')
            for code in (r"\n", r"\l"):
                check(controls(row["thai"]).count(code) == controls(row["english_raw"]).count(code),
                      f'{row["id"]}: {code} count differs')

        glossary = read_csv(TRANS / "glossary.csv")
        keys = [r["english"].strip().casefold() for r in glossary]
        check(len(keys) == len(set(keys)), "duplicate normalized glossary English keys")
        spellings = {}
        for row in glossary:
            key = row["english"].strip().casefold()
            check(not key or key not in spellings or spellings[key] == row["thai"], f'{row["english"]}: inconsistent glossary Thai')
            spellings[key] = row["thai"]
        memory = read_csv(TRANS / "translation_memory.csv")
        by_normalized = {}
        for row in memory:
            key = row["english_normalized"]
            if key in by_normalized and by_normalized[key] != row["thai"] and not (row["context_variants"].strip() or row["status"] == "review"):
                errors.append(f"translation-memory conflict without documented variant: {key[:60]}")
            by_normalized[key] = row["thai"]
        styles = read_csv(TRANS / "speaker_style_guide.csv")
        style_speakers = {r["speaker"] for r in styles}
        recurring = {speaker for speaker, count in Counter(r["speaker"] for r in master if r["speaker"]).items() if count > 1}
        check(recurring <= style_speakers, "recurring speakers missing style guidance: " + ", ".join(sorted(recurring - style_speakers)))

        map_rows, chapter_rows = split_rows(TRANS / "maps"), split_rows(TRANS / "chapters")
        check(map_rows == master, "translated map-period files do not concatenate exactly to Thai master")
        check(chapter_rows == master, "translated chapter files do not concatenate exactly to Thai master")
        expected_maps = {p.stem + "_thai.csv" for p in (STORY / "maps").glob("*.csv")}
        expected_chapters = {p.stem + "_thai.csv" for p in (STORY / "chapters").glob("*.csv")}
        check({p.name for p in (TRANS / "maps").glob("*.csv")} == expected_maps, "translated map filename set differs from source")
        check({p.name for p in (TRANS / "chapters").glob("*.csv")} == expected_chapters, "translated chapter filename set differs from source")

        check(review_ids(TRANS / "reviews/main_story_translation_review.md") == master_ids, "master review coverage/order differs")
        map_review_ids = [item for p in sorted((TRANS / "reviews/maps").glob("*.md")) for item in review_ids(p)]
        chapter_review_ids = [item for p in sorted((TRANS / "reviews/chapters").glob("*.md")) for item in review_ids(p)]
        check(map_review_ids == master_ids and Counter(map_review_ids) == Counter(master_ids), "map review coverage is not exactly once")
        check(chapter_review_ids == master_ids and Counter(chapter_review_ids) == Counter(master_ids), "chapter review coverage is not exactly once")
        check(len(list((TRANS / "reviews/maps").glob("*.md"))) == len(expected_maps), "map review file count mismatch")
        check(len(list((TRANS / "reviews/chapters").glob("*.md"))) == len(expected_chapters), "chapter review file count mismatch")
        length_rows = read_csv(TRANS / "main_story_length_review.csv")
        check([r["id"] for r in length_rows] == master_ids, "length-review IDs/order differ from master")

        progress = json.loads((TRANS / "translation_progress.json").read_text(encoding="utf-8"))
        actual_confidence = dict(sorted(Counter(r["translation_confidence"] for r in master).items()))
        actual_terms = dict(sorted(Counter(r["term_review"] for r in master).items()))
        actual_lengths = dict(sorted(Counter(r["length_review"] for r in master).items()))
        checks = {"total_ordered_dialogue_rows": len(source), "total_translated_rows": sum(bool(r["thai"].strip()) for r in master),
                  "total_untranslated_rows": sum(not bool(r["thai"].strip()) for r in master), "batch_row_count": len(batch),
                  "remaining_untranslated_row_count": sum(not bool(r["thai"].strip()) for r in master),
                  "glossary_term_count": len(glossary), "translation_memory_entry_count": len(memory),
                  "speaker_style_entry_count": len(styles), "translation_confidence_counts": actual_confidence,
                  "term_review_counts": actual_terms, "length_review_counts": actual_lengths}
        for key, value in checks.items():
            check(progress.get(key) == value, f"progress {key} does not match actual value")
        check(progress.get("batch_start_global_order") == 1 and progress.get("batch_end_global_order") == 261,
              "progress batch boundaries differ")

        for path in sorted(TRANS.rglob("*.csv")):
            read_csv(path)
            text = path.read_text(encoding="utf-8-sig")
            check("\ufffd" not in text, f"{path.relative_to(ROOT)} contains U+FFFD")
            check("```" not in text, f"{path.relative_to(ROOT)} contains Markdown fence")
        for path in sorted(TRANS.rglob("*")):
            if path.is_file():
                check("\ufffd" not in path.read_text(encoding="utf-8-sig"), f"{path.relative_to(ROOT)} contains U+FFFD")
        changed = git_changed_protected()
        check(not changed, "protected game/font/renderer source differs in this worktree: " + ", ".join(changed))
        roms = [p for p in ROOT.glob("*.gba") if p.is_file()]
        check(not roms, "ROM output exists at repository root: " + ", ".join(p.name for p in roms))
    except (FileNotFoundError, KeyError, ValueError, csv.Error, json.JSONDecodeError, subprocess.CalledProcessError) as error:
        errors.append(str(error))
    return errors


def deterministic_support_hashes():
    paths = list((TRANS / "maps").glob("*.csv")) + list((TRANS / "chapters").glob("*.csv"))
    paths += list((TRANS / "reviews").rglob("*.md"))
    paths += [TRANS / "translation_progress.json", TRANS / "main_story_translation_report.md"]
    return {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}


def main():
    errors = validation_errors()
    if errors:
        print("main-story translation validation failed: " + errors[0], file=sys.stderr)
        return 1
    print("main-story translation validation passed (261 rows, 41 map periods, 12 chapters)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
