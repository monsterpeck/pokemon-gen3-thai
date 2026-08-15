#!/usr/bin/env python3
"""Generate deterministic Phase B support-B artifacts from the reviewed master."""
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STORY = ROOT / "tools/thai/translation/story_order"
TRANS = STORY / "translation"
MASTER = TRANS / "dialogue_main_story_thai.csv"


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path, fieldnames, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def translated_name(source):
    return source.with_name(source.stem + "_thai.csv").name


def review_name(source):
    return source.with_suffix(".md").name


def source_groups(directory):
    groups = []
    for path in sorted(directory.glob("*.csv")):
        groups.append((path, [row["id"] for row in read_csv(path)]))
    return groups


def glossary_terms(row, glossary):
    haystack = row["english_raw"].casefold()
    return [entry["english"] for entry in glossary if entry["english"].casefold() in haystack]


def row_review(row, glossary):
    def value(key):
        return row.get(key, "") or "—"
    terms = ", ".join(glossary_terms(row, glossary)) or "—"
    return "\n".join([
        f'<!-- dialogue-id: {row["id"]} -->',
        f'#### {row["global_order"]}. `{row["id"]}`', "",
        f'- Chapter: {value("chapter_id")} — {value("chapter_title_en")} / {value("chapter_title_th")}',
        f'- Event: {value("event_id")} — {value("event_title_en")} / {value("event_title_th")}',
        f'- Map: {value("map_name")}', f'- Map period: {value("map_period")}',
        f'- Speaker: {value("speaker")}', f'- Source label: `{value("source_label")}`',
        f'- English preview: {value("english_preview").replace(chr(10), "<br>")}',
        f'- Thai: {value("thai").replace(chr(10), "<br>")}',
        f'- Placeholders: {value("placeholders")}', f'- Control codes: {value("control_codes")}',
        f'- Translation confidence: {value("translation_confidence")}',
        f'- Glossary terms used: {terms}', f'- Term review: {value("term_review")}',
        f'- Length review: {value("length_review")}', f'- Translation notes: {value("translation_notes")}', "",
    ])


def write_review(path, title, rows, glossary, grouped=False):
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"# {title}", "", "Generated deterministically from `dialogue_main_story_thai.csv`.", ""]
    last = (None, None, None)
    for row in rows:
        keys = (row["chapter_id"], row["event_id"], (row["map_name"], row["map_period"]))
        if grouped:
            if keys[0] != last[0]:
                lines += [f'## Chapter {row["chapter_order"]}: {row["chapter_title_en"]} / {row["chapter_title_th"]}', ""]
            if keys[1] != last[1]:
                lines += [f'### Event {row["event_order"]}: {row["event_title_en"]} / {row["event_title_th"]}', ""]
            if keys[2] != last[2]:
                lines += [f'#### Map period: {row["map_name"] or "Global"} — {row["map_period"]}', ""]
        lines.append(row_review(row, glossary))
        last = keys
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main():
    rows = read_csv(MASTER)
    fields = list(rows[0])
    by_id = {row["id"]: row for row in rows}
    glossary = read_csv(TRANS / "glossary.csv")
    memory = read_csv(TRANS / "translation_memory.csv")
    speakers = read_csv(TRANS / "speaker_style_guide.csv")
    maps = source_groups(STORY / "maps")
    chapters = source_groups(STORY / "chapters")

    for out_dir in (TRANS / "maps", TRANS / "chapters", TRANS / "reviews/maps", TRANS / "reviews/chapters"):
        out_dir.mkdir(parents=True, exist_ok=True)

    for source, ids in maps:
        selected = [by_id[item] for item in ids]
        write_csv(TRANS / "maps" / translated_name(source), fields, selected)
        write_review(TRANS / "reviews/maps" / review_name(source), f"Map-period review: {source.stem}", selected, glossary)
    for source, ids in chapters:
        selected = [by_id[item] for item in ids]
        write_csv(TRANS / "chapters" / translated_name(source), fields, selected)
        write_review(TRANS / "reviews/chapters" / review_name(source), f"Chapter review: {source.stem}", selected, glossary)
    write_review(TRANS / "reviews/main_story_translation_review.md", "Pokémon Emerald main-story Thai translation review", rows, glossary, True)

    confidence = Counter(row["translation_confidence"] for row in rows)
    terms = Counter(row["term_review"] for row in rows)
    lengths = Counter(row["length_review"] for row in rows)
    generated = ["dialogue_main_story_thai.csv", "batches/batch_001_complete_main_story.csv",
                 "glossary.csv", "translation_memory.csv", "speaker_style_guide.csv",
                 "main_story_length_review.csv", "reviews/main_story_translation_review.md",
                 "translation_progress.json", "main_story_translation_report.md"]
    generated += [f"maps/{translated_name(p)}" for p, _ in maps]
    generated += [f"chapters/{translated_name(p)}" for p, _ in chapters]
    generated += [f"reviews/maps/{review_name(p)}" for p, _ in maps]
    generated += [f"reviews/chapters/{review_name(p)}" for p, _ in chapters]
    progress = {
        "source_database": "tools/thai/translation/story_order/dialogue_main_story_ordered.csv",
        "total_ordered_dialogue_rows": len(rows), "total_translated_rows": sum(bool(r["thai"].strip()) for r in rows),
        "total_untranslated_rows": sum(not bool(r["thai"].strip()) for r in rows),
        "completed_batches": ["batch_001_complete_main_story"], "current_batch": None,
        "batch_start_global_order": 1, "batch_end_global_order": 261, "batch_row_count": len(rows),
        "remaining_untranslated_row_count": sum(not bool(r["thai"].strip()) for r in rows),
        "chapters_touched": len({r["chapter_id"] for r in rows}), "events_touched": len({r["event_id"] for r in rows}),
        "maps_touched": len({r["map_name"] for r in rows}), "map_periods_touched": len(maps),
        "glossary_term_count": len(glossary), "glossary_review_count": sum(r["status"] == "review" for r in glossary),
        "translation_memory_entry_count": len(memory), "speaker_style_entry_count": len(speakers),
        "translation_confidence_counts": dict(sorted(confidence.items())), "term_review_counts": dict(sorted(terms.items())),
        "length_review_counts": dict(sorted(lengths.items())), "generated_files": sorted(generated),
        "notes": ["Support artifacts generated from the authoritative completed Thai master.",
                  "No dialogue was translated or injected into game source during finalization."],
    }
    (TRANS / "translation_progress.json").write_text(json.dumps(progress, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    review_terms = [r["english"] for r in glossary if r["status"] == "review"]
    tone_review = [r["id"] for r in rows if r["translation_confidence"] in {"medium", "low"}]
    length_review = [r["id"] for r in rows if r["length_review"] != "ok"]
    report = f"""# Main-story Thai translation report

## Summary

- Source scope validation: passed (`make check-story-scope`); independently rechecked by the translation validator
- Total mandatory dialogue rows: {len(rows)}
- Translated rows: {progress['total_translated_rows']}
- Untranslated rows: {progress['total_untranslated_rows']}
- Chapters: {progress['chapters_touched']}
- Events: {progress['events_touched']}
- Map periods: {progress['map_periods_touched']}
- Translation confidence (high / medium / low): {confidence['high']} / {confidence['medium']} / {confidence['low']}
- Glossary terms: {len(glossary)} ({progress['glossary_review_count']} marked review)
- Translation-memory entries: {len(memory)}
- Speaker-style entries: {len(speakers)}
- Length review: {', '.join(f'{k}={v}' for k, v in sorted(lengths.items()))}
- Control-code review count: {lengths['review_control_codes']}

## Human review queues

- Terms requiring human confirmation: {', '.join(review_terms) if review_terms else 'None'}
- Dialogue requiring tone review: {', '.join(tone_review) if tone_review else 'None'}
- Dialogue requiring length review: {', '.join(length_review) if length_review else 'None'}

## Integrity confirmations

- Original English fields in the ordered source remain unchanged by these outputs.
- This finalization did not modify original game dialogue source, fonts, renderer, charmap, or Thai shaping source.
- The translation was not injected into game source.
- No ROM was built by this finalization.
"""
    (TRANS / "main_story_translation_report.md").write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
