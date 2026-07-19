#!/usr/bin/env python3
"""Generate a deterministic translation inventory from pokeemerald sources."""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

VERSION = "1.0.0"
ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = ROOT / "tools/thai/translation"
COLUMNS = [
    "id", "category", "subcategory", "story_order", "map_name",
    "location_name", "speaker", "source_file", "source_line", "source_label",
    "english_raw", "english_preview", "thai", "translation_status",
    "control_codes", "placeholders", "duplicate_group", "notes",
]
CATEGORIES = [
    "main_story", "optional_npc", "trainer", "match_call", "sign",
    "interaction", "tutorial", "system", "menu", "battle", "item", "unknown",
]
NPC_CATEGORIES = {"optional_npc", "trainer", "match_call", "sign", "interaction"}
SYSTEM_CATEGORIES = {"tutorial", "system", "menu", "battle", "item"}
CONTROL_RE = re.compile(r"\\[nplvcx](?:[0-9A-Fa-f]{0,2})?|\{[^{}]+\}")
PLACEHOLDER_RE = re.compile(
    r"\{(?:PLAYER|RIVAL|STR_VAR_[123]|POKEBLOCK|"
    r"[A-Z0-9_]*(?:NAME|BUFF|TRAINER|SPECIES|MOVE|ABILITY)[A-Z0-9_]*)\}"
)
ASM_LABEL_RE = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_]*):{1,2}(?!:)", re.MULTILINE)
ASM_STRING_RE = re.compile(r'^\s*\.string\s+"((?:\\.|[^"\\])*)"', re.MULTILINE)


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def is_ignored(path: Path) -> bool:
    name = path.name.lower()
    parts = {part.lower() for part in path.parts}
    return (
        name.endswith(".bak")
        or ".before_" in name
        or "archive" in parts
        or "generated" in parts
        or "__pycache__" in parts
        or any(word in name for word in ("temporary_probe", "temp_probe", "debug_fixture"))
    )


def discover_sources(source: str | None = None) -> tuple[list[Path], list[str]]:
    if source:
        path = (ROOT / source).resolve()
        if ROOT not in path.parents or not path.is_file() or is_ignored(path):
            raise ValueError(f"invalid or ignored source: {source}")
        return [path], []

    specs = (
        (ROOT / "data/maps", {".inc"}),
        (ROOT / "data/scripts", {".inc"}),
        (ROOT / "data/text", {".inc"}),
        (ROOT / "src", {".c", ".h", ".inc"}),
        (ROOT / "include", {".h", ".inc"}),
    )
    candidates: list[Path] = []
    for base, suffixes in specs:
        if base.exists():
            candidates.extend(
                path for path in base.rglob("*")
                if path.is_file() and path.suffix.lower() in suffixes
            )
    files = sorted({p for p in candidates if not is_ignored(p)}, key=relative)
    skipped = sorted(relative(p) for p in candidates if is_ignored(p))
    return files, skipped


def strip_comments(text: str) -> str:
    """Blank comments while retaining offsets and line numbers."""
    def blank(match: re.Match[str]) -> str:
        return "".join("\n" if char == "\n" else " " for char in match.group(0))
    return re.sub(r"//[^\n]*|/\*.*?\*/", blank, text, flags=re.DOTALL)


def decode_literal(body: str) -> str:
    """Decode quote escapes but retain game/C control escapes verbatim."""
    return body.replace(r'\"', '"')


def parse_assembly(text: str) -> list[dict[str, object]]:
    clean = strip_comments(text)
    labels = list(ASM_LABEL_RE.finditer(clean))
    entries = []
    for index, label in enumerate(labels):
        end = labels[index + 1].start() if index + 1 < len(labels) else len(clean)
        fragments = list(ASM_STRING_RE.finditer(clean, label.end(), end))
        if fragments:
            entries.append({
                "label": label.group(1),
                "line": clean.count("\n", 0, label.start()) + 1,
                "raw": "".join(decode_literal(fragment.group(1)) for fragment in fragments),
                "source_type": "assembly",
            })
    return entries


def parse_c(text: str) -> list[dict[str, object]]:
    clean = strip_comments(text)
    entries = []
    macro = re.compile(r"(?<![A-Za-z0-9_])_\s*\(")
    position = 0
    while True:
        match = macro.search(clean, position)
        if not match:
            break
        index, depth, quoted = match.end(), 1, False
        while index < len(clean) and depth:
            char = clean[index]
            if quoted:
                if char == "\\":
                    index += 2
                    continue
                if char == '"':
                    quoted = False
            elif char == '"':
                quoted = True
            elif char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
            index += 1
        position = max(index, match.end())
        if depth:
            continue
        expression = clean[match.end():index - 1]
        fragments = re.findall(r'"((?:\\.|[^"\\])*)"', expression)
        if not fragments:
            continue
        line = clean.count("\n", 0, match.start()) + 1
        preceding = clean[max(0, match.start() - 600):match.start()]
        symbols = re.findall(
            r"([A-Za-z_][A-Za-z0-9_]*)\s*(?:\[[^;=]*\])?\s*=\s*$", preceding
        )
        entries.append({
            "label": symbols[-1] if symbols else f"inline_{line}",
            "line": line,
            "raw": "".join(decode_literal(fragment) for fragment in fragments),
            "source_type": "c",
        })
    return entries


def classify(path: str, label: str) -> tuple[str, str, str]:
    evidence = (path + " " + label).lower()
    progression_evidence = (
        "movingin", "setclock", "meet_rival", "meetrival", "rivalbattle",
        "rescuebirch", "savebirch", "team_aqua", "teamaqua", "team_magma",
        "teammagma", "mtchimney", "weatherinstitute", "seafloorcavern",
        "caveoforigin", "sky_pillar", "skypillar", "awakenrayquaza",
        "awakenkyogre", "awakengroudon", "gymleader", "elitefour",
        "elite_four", "championbattle", "halloffame", "hall_of_fame",
        "theend", "endingsequence",
    )
    if path.startswith("data/maps/") and any(token in evidence for token in progression_evidence):
        return "main_story", "required_event", "Map path or label explicitly identifies progression."
    if "match_call" in evidence or "matchcall" in evidence:
        return "match_call", "", ""
    if "trainer" in evidence or any(x in evidence for x in ("beforebattle", "defeated", "afterbattle")):
        return "trainer", "trainer_dialogue", ""
    if "sign" in evidence or "bookshelf" in evidence:
        return "sign", "", ""
    if "tutorial" in evidence or "teachy" in evidence:
        return "tutorial", "", ""
    if "battle" in evidence:
        return "battle", "", ""
    if any(x in evidence for x in ("menu", "option", "keyboard", "pokenav", "pokedex", "summary")):
        return "menu", "", ""
    if any(x in evidence for x in ("item", "berry", "obtain", "bag")) and not path.startswith("data/maps/"):
        return "item", "", ""

    explicit_story = (
        path == "data/text/birch_speech.inc"
        or any(x in evidence for x in (
            "eventscript_birch", "eventscript_rival", "eventscript_team_aqua",
            "eventscript_team_magma", "eventscript_gymleader", "eventscript_elitefour",
            "eventscript_champion", "eventscript_halloffame", "eventscript_legendary",
            "eventscript_ending", "eventscript_credits",
        ))
    )
    if explicit_story:
        return "main_story", "required_event", "Source path or label explicitly identifies progression."
    if path.startswith("data/maps/"):
        if any(x in evidence for x in ("interact", "books", "pc", "tv", "door", "statue")):
            return "interaction", "", ""
        return "optional_npc", "", "Main-story status is not proven by static source evidence."
    if path.startswith(("data/", "src/", "include/")):
        return "system", "source_text", ""
    return "unknown", "", "Insufficient classification evidence."


def infer_speaker(label: str) -> str:
    speakers = {
        "Birch": "Professor Birch", "Archie": "Archie", "Maxie": "Maxie",
        "Steven": "Steven", "Wallace": "Wallace", "Wally": "Wally",
        "Roxanne": "Roxanne", "Brawly": "Brawly", "Wattson": "Wattson",
        "Flannery": "Flannery", "Norman": "Norman", "Winona": "Winona",
        "Tate": "Tate", "Liza": "Liza", "Juan": "Juan",
        "Brendan": "Brendan", "May": "May",
    }
    return next((value for key, value in speakers.items() if key.lower() in label.lower()), "")


def make_preview(raw: str) -> str:
    for source, marker in (
        (r"\n", "\n"), (r"\l", "\n"), (r"\p", "\n[PAGE]\n"),
        (r"\v", "[VARIABLE]"), (r"\c", "[COLOR]"), (r"\x", "[HEX]"),
    ):
        raw = raw.replace(source, marker)
    return raw.replace("$", "")


def build_rows(files: list[Path]) -> tuple[list[dict[str, str]], Counter]:
    rows: list[dict[str, str]] = []
    source_types: Counter = Counter()
    for path in files:
        text = path.read_text(encoding="utf-8", errors="replace")
        entries = parse_assembly(text) if path.suffix == ".inc" else parse_c(text)
        for ordinal, entry in enumerate(entries, 1):
            raw = str(entry["raw"])
            if not raw or not re.search(r"[A-Za-zÀ-ÿก-๙0-9{]", raw):
                continue
            source_file, label = relative(path), str(entry["label"])
            category, subcategory, note = classify(source_file, label)
            parts = Path(source_file).parts
            map_name = parts[2] if len(parts) > 2 and parts[:2] == ("data", "maps") else ""
            identity = f"{source_file}\0{entry['line']}\0{label}\0{ordinal}\0{raw}".encode("utf-8")
            rows.append({
                "id": "dlg_" + hashlib.sha256(identity).hexdigest()[:16],
                "category": category, "subcategory": subcategory, "story_order": "",
                "map_name": map_name, "location_name": map_name.replace("_", " "),
                "speaker": infer_speaker(label), "source_file": source_file,
                "source_line": str(entry["line"]), "source_label": label,
                "english_raw": raw, "english_preview": make_preview(raw), "thai": "",
                "translation_status": "untranslated",
                "control_codes": " | ".join(CONTROL_RE.findall(raw)),
                "placeholders": " | ".join(PLACEHOLDER_RE.findall(raw)),
                "duplicate_group": "", "notes": note,
            })
            source_types[str(entry["source_type"])] += 1
    rows.sort(key=lambda row: (row["source_file"], int(row["source_line"]), row["source_label"], row["id"]))

    opening = [r for r in rows if r["category"] == "main_story" and r["source_file"] == "data/text/birch_speech.inc"]
    for index, row in enumerate(opening, 1):
        row["story_order"] = f"001.{index:03d}"

    texts: defaultdict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        texts[row["english_raw"]].append(row)
    duplicate_sets = sorted((raw, members) for raw, members in texts.items() if len(members) > 1)
    for index, (_, members) in enumerate(duplicate_sets, 1):
        for row in members:
            row["duplicate_group"] = f"dup_{index:05d}"
    return rows, source_types


def csv_bytes(rows: list[dict], columns: list[str] = COLUMNS) -> bytes:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=columns, lineterminator="\n")
    writer.writeheader()
    writer.writerows({column: row.get(column, "") for column in columns} for row in rows)
    return b"\xef\xbb\xbf" + buffer.getvalue().encode("utf-8")


def extraction_timestamp() -> str:
    try:
        return subprocess.check_output(
            ["git", "log", "-1", "--format=%cI"], cwd=ROOT, text=True
        ).strip()
    except (OSError, subprocess.SubprocessError):
        return "1970-01-01T00:00:00+00:00"


def render_outputs(rows, source_types, files, skipped) -> dict[str, bytes]:
    counts = Counter(row["category"] for row in rows)
    grouped: defaultdict[str, list[dict]] = defaultdict(list)
    for row in rows:
        if row["duplicate_group"]:
            grouped[row["duplicate_group"]].append(row)
    duplicate_rows = [
        {"duplicate_group": group, "english_raw": members[0]["english_raw"],
         "occurrence_count": len(members),
         "source_labels": " | ".join(row["source_label"] for row in members),
         "source_files": " | ".join(row["source_file"] for row in members)}
        for group, members in sorted(grouped.items())
    ]
    inventory = {
        "extraction_timestamp": extraction_timestamp(), "extractor_version": VERSION,
        "total_entries": len(rows), "count_by_category": dict(sorted(counts.items())),
        "count_by_source_type": dict(sorted(source_types.items())),
        "count_containing_placeholders": sum(bool(r["placeholders"]) for r in rows),
        "count_containing_control_codes": sum(bool(r["control_codes"]) for r in rows),
        "duplicate_groups": len(grouped), "untranslated_count": len(rows),
        "main_story_count": counts["main_story"],
        "unknown_classification_count": counts["unknown"],
        "source_files_scanned": [relative(path) for path in files],
        "source_files_skipped": skipped,
    }
    index = ["# Dialogue by source", ""]
    current_file = current_label = None
    for row in rows:
        if row["source_file"] != current_file:
            current_file, current_label = row["source_file"], None
            index.extend((f"## `{current_file}`", ""))
        if row["source_label"] != current_label:
            current_label = row["source_label"]
            index.extend((f"### `{current_label}`", ""))
        shown = row["english_preview"].replace("\n", " ⏎ ")
        index.extend((f"- `{row['id']}` · {row['category']} · {row['speaker'] or '—'} · {shown}", ""))

    report = [
        "# Dialogue extraction report", "", f"Extractor version: `{VERSION}`", "",
        "## Coverage", "",
        "Scanned `data/maps`, `data/scripts`, `data/text`, `src`, and `include` recursively. Supports assembly `.string` labels and C `_()` declarations, adjacent fragments, escaped quotes, controls, and placeholders.", "",
        f"- Total entries: {len(rows)}", f"- Main-story entries: {counts['main_story']}",
        f"- Unknown entries: {counts['unknown']}", f"- Duplicate groups: {len(grouped)}",
        f"- Entries with placeholders: {inventory['count_containing_placeholders']}",
        f"- Entries with control codes: {inventory['count_containing_control_codes']}", "",
        "## Files skipped", "",
        *(f"- `{name}`" for name in skipped),
        "- Archived, backup, generated, debug-fixture, and temporary-probe paths are excluded by rule.", "",
        "## Limitations", "",
        "Classification is intentionally conservative and based on source paths and labels. Static extraction cannot prove every runtime call path, speaker, or narrative dependency. Only the dedicated opening speech receives a deterministic story order; uncertain order remains blank. Current non-English source text is preserved verbatim.", "",
        "## Recommended translation workflow", "",
        "Translate the main-story CSV first while preserving every control code and placeholder, then translate NPC and system inventories. Keep IDs and source metadata unchanged.", "",
        "No game source, existing dialogue, renderer, font asset, charmap, or Thai shaping file was modified.", "",
    ]
    story = sorted(
        (r for r in rows if r["category"] == "main_story"),
        key=lambda r: (not r["story_order"], r["story_order"], r["source_file"], int(r["source_line"])),
    )
    return {
        "dialogue_master.csv": csv_bytes(rows),
        "dialogue_main_story.csv": csv_bytes(story),
        "dialogue_npc.csv": csv_bytes([r for r in rows if r["category"] in NPC_CATEGORIES]),
        "dialogue_system.csv": csv_bytes([r for r in rows if r["category"] in SYSTEM_CATEGORIES]),
        "dialogue_duplicates.csv": csv_bytes(
            duplicate_rows, ["duplicate_group", "english_raw", "occurrence_count", "source_labels", "source_files"]
        ),
        "dialogue_inventory.json": (json.dumps(inventory, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8"),
        "dialogue_by_source.md": ("\n".join(index) + "\n").encode("utf-8"),
        "extraction_report.md": ("\n".join(report) + "\n").encode("utf-8"),
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--category", choices=CATEGORIES)
    parser.add_argument("--source")
    args = parser.parse_args(argv)
    try:
        files, skipped = discover_sources(args.source)
    except ValueError as error:
        parser.error(str(error))
    rows, source_types = build_rows(files)
    if args.category:
        rows = [row for row in rows if row["category"] == args.category]
    outputs = render_outputs(rows, source_types, files, skipped)
    if args.check:
        stale = [name for name, content in outputs.items() if not (OUTPUT_DIR / name).is_file() or (OUTPUT_DIR / name).read_bytes() != content]
        if stale:
            print("missing or stale dialogue outputs: " + ", ".join(stale), file=sys.stderr)
            return 1
        print(f"dialogue extraction check passed ({len(rows)} entries)")
        return 0
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for name, content in outputs.items():
        (OUTPUT_DIR / name).write_bytes(content)
    print(f"extracted {len(rows)} entries from {len(files)} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
