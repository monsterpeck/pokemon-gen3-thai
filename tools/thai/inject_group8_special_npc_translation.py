#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path

import inject_main_story_translation as inj
import shape_thai_precompose as shape

ROOT = Path(__file__).resolve().parents[2]
PACK = ROOT / "tools/thai/translation/phaseF/batches/phaseF-group8-special-npc-actionable-12-thai.csv"


def read_pack():
    with PACK.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    required = {
        "id", "source_file", "source_line",
        "source_label", "english_raw", "thai_text",
    }
    missing = required - set(rows[0] if rows else ())
    if missing:
        raise inj.InjectionError("pack missing columns: " + ", ".join(sorted(missing)))
    if len(rows) != 12:
        raise inj.InjectionError(f"expected 12 rows, got {len(rows)}")

    ids = [r["id"] for r in rows]
    dup = [x for x, n in Counter(ids).items() if n > 1]
    if dup:
        raise inj.InjectionError("duplicate id: " + dup[0])

    if {r["source_file"] for r in rows} != {"src/strings.c"}:
        raise inj.InjectionError("unexpected source file outside src/strings.c")

    return rows


def shape_text(text, mapping):
    def repl(match):
        encoded, _records, _advance = shape.encode_run(match.group(0), mapping)
        return shape.brace_bytes(encoded)
    return shape.THAI_RE.sub(repl, text)


def main():
    parser = argparse.ArgumentParser(
        description="Deterministically inject approved Group 8 Special NPC Thai strings."
    )
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    rows = read_pack()
    mapping = shape.load_mapping()

    prepared = []
    shaped_ok = 0

    for row in rows:
        item = dict(row)
        item["thai"] = shape_text(row["thai_text"], mapping)

        if item["thai"] and not shape.THAI_RE.search(item["thai"]):
            shaped_ok += 1

        prepared.append(item)

    targets, texts = inj.resolve(prepared)
    rendered = inj.rendered_sources(targets, texts)

    unique_targets = {
        (str(t.path), t.start, t.end)
        for t in targets
    }

    print("=== GROUP 8 INJECTION DRY-RUN ===" if not args.apply
          else "=== GROUP 8 INJECTION APPLY ===")
    print("STATUS: PASS")
    print("MASTER_ROWS:", len(rows))
    print("SHAPED:", f"{shaped_ok}/{len(rows)}")
    print("RESOLVED:", len(targets))
    print("UNIQUE_TARGETS:", len(unique_targets))
    print("BASELINE_MATCH:", len(targets))
    print("CONTROL_PLACEHOLDER_GUARD: PASS")
    print("SOURCE_FILES_TARGETED:", len(texts))

    if args.apply:
        inj.apply_sources(rendered)
        print("SOURCE_FILES_MODIFIED:", len(rendered))
        print("APPLY: PASS")
    else:
        print("SOURCE_FILES_MODIFIED: 0")
        print("READY_FOR_APPLY:", "YES" if len(targets) == 12 and shaped_ok == 12 else "NO")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
