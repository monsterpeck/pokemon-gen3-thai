#!/usr/bin/env python3
"""Deterministically inject the reviewed main-story Thai master.

The default mode is a read-only dry-run.  Pass ``--apply`` only after a
successful dry-run to replace the resolved assembly string definitions.
"""
from __future__ import annotations

import argparse
import csv
import os
import re
import sys
import tempfile
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

import extract_dialogue as extraction
import validate_main_story_translation as validation


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MASTER = (
    ROOT
    / "tools/thai/translation/story_order/translation/dialogue_main_story_thai.csv"
)
ASM_STRING_RE = extraction.ASM_STRING_RE
VALID_ESCAPE_RE = re.compile(r"\\(?:[npl]|[vcx](?:[0-9A-Fa-f]{0,2})?)")
BRACE_RE = re.compile(r"\{[^{}]*\}")
NUMERIC_BRACE_RE = re.compile(r"\{[0-9]+\}")


class InjectionError(RuntimeError):
    """A hard guard failure that prevents all source writes."""


@dataclass(frozen=True)
class Target:
    row_id: str
    path: Path
    start: int
    end: int
    indent: str
    english: str
    thai: str


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_master(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        raise InjectionError(f"master not found: {path}")
    if not path.read_bytes().startswith(b"\xef\xbb\xbf"):
        raise InjectionError(f"{relative(path)}: missing UTF-8 BOM")
    with path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    required = {"id", "source_file", "source_line", "source_label", "english_raw", "thai"}
    missing = required - set(rows[0] if rows else ())
    if missing:
        raise InjectionError("master missing columns: " + ", ".join(sorted(missing)))
    if not rows:
        raise InjectionError("master contains no rows")
    ids = [row["id"] for row in rows]
    duplicates = sorted(key for key, count in Counter(ids).items() if count > 1)
    if duplicates:
        raise InjectionError("duplicate master id: " + duplicates[0])
    return rows


def parse_assembly_targets(text: str) -> list[dict[str, object]]:
    """Add replacement spans to the extractor's assembly parsing semantics."""
    clean = extraction.strip_comments(text)
    labels = list(extraction.ASM_LABEL_RE.finditer(clean))
    targets: list[dict[str, object]] = []
    for index, label in enumerate(labels):
        block_end = labels[index + 1].start() if index + 1 < len(labels) else len(clean)
        fragments = list(ASM_STRING_RE.finditer(clean, label.end(), block_end))
        if not fragments:
            continue
        first, last = fragments[0], fragments[-1]
        line_start = text.rfind("\n", 0, first.start()) + 1
        line_end = text.find("\n", last.end())
        if line_end < 0:
            line_end = len(text)
        else:
            line_end += 1
        indent_match = re.match(r"[ \t]*", text[line_start:first.start()])
        targets.append(
            {
                "label": label.group(1),
                "line": clean.count("\n", 0, label.start()) + 1,
                "raw": "".join(
                    extraction.decode_literal(fragment.group(1)) for fragment in fragments
                ),
                "start": line_start,
                "end": line_end,
                "indent": indent_match.group(0) if indent_match else "",
            }
        )
    return targets


def guard_syntax(row_id: str, field: str, text: str) -> None:
    escape_starts = {match.start() for match in VALID_ESCAPE_RE.finditer(text)}
    for match in re.finditer(r"\\", text):
        if match.start() not in escape_starts:
            raise InjectionError(f"{row_id}: malformed control sequence in {field}")

    brace_spans = {(match.start(), match.end()) for match in BRACE_RE.finditer(text)}
    if text.count("{") != len(brace_spans) or text.count("}") != len(brace_spans):
        raise InjectionError(f"{row_id}: malformed brace sequence in {field}")
    recognized = {
        (match.start(), match.end())
        for pattern in (validation.CONTROL_RE, validation.PLACEHOLDER_RE, NUMERIC_BRACE_RE)
        for match in pattern.finditer(text)
        if match.group(0).startswith("{")
    }
    if brace_spans != recognized:
        raise InjectionError(f"{row_id}: malformed control or placeholder in {field}")
    if text.count("$") != 1 or not text.endswith("$"):
        raise InjectionError(f"{row_id}: malformed string terminator in {field}")


def guard_translation(row: dict[str, str]) -> None:
    row_id, english, thai = row["id"], row["english_raw"], row["thai"]
    if not thai:
        raise InjectionError(f"{row_id}: empty Thai translation")
    guard_syntax(row_id, "english_raw", english)
    guard_syntax(row_id, "thai", thai)
    if validation.PLACEHOLDER_RE.findall(thai) != validation.PLACEHOLDER_RE.findall(english):
        raise InjectionError(f"{row_id}: placeholder mismatch")
    if validation.required_controls(thai) != validation.required_controls(english):
        raise InjectionError(f"{row_id}: required control sequence mismatch")
    for code in (r"\n", r"\l"):
        if validation.controls(thai).count(code) != validation.controls(english).count(code):
            raise InjectionError(f"{row_id}: {code} count mismatch")


def source_path(value: str) -> Path:
    path = (ROOT / value).resolve()
    if ROOT not in path.parents or not path.is_file() or path.suffix != ".inc":
        raise InjectionError(f"invalid assembly source_file: {value}")
    return path


def resolve(rows: list[dict[str, str]]) -> tuple[list[Target], dict[Path, str]]:
    texts: dict[Path, str] = {}
    parsed: dict[Path, list[dict[str, object]]] = {}
    targets: list[Target] = []
    identities: set[tuple[Path, int, int]] = set()
    for row in rows:
        guard_translation(row)
        path = source_path(row["source_file"])
        if path not in texts:
            texts[path] = path.read_text(encoding="utf-8")
            parsed[path] = parse_assembly_targets(texts[path])
        try:
            line = int(row["source_line"])
        except ValueError as error:
            raise InjectionError(f'{row["id"]}: invalid source_line') from error
        candidates = [
            entry
            for entry in parsed[path]
            if entry["label"] == row["source_label"] and entry["line"] == line
        ]
        if not candidates:
            raise InjectionError(f'{row["id"]}: source target missing')
        if len(candidates) != 1:
            raise InjectionError(f'{row["id"]}: source target ambiguous')
        entry = candidates[0]
        if entry["raw"] != row["english_raw"]:
            raise InjectionError(f'{row["id"]}: English baseline mismatch')
        identity = (path, int(entry["start"]), int(entry["end"]))
        if identity in identities:
            raise InjectionError(f'{row["id"]}: duplicate target')
        identities.add(identity)
        targets.append(
            Target(
                row_id=row["id"], path=path, start=int(entry["start"]),
                end=int(entry["end"]), indent=str(entry["indent"]),
                english=row["english_raw"], thai=row["thai"],
            )
        )
    return targets, texts


def encode_assembly_body(text: str) -> str:
    return text.replace('"', r'\"')


def rendered_sources(targets: list[Target], texts: dict[Path, str]) -> dict[Path, str]:
    by_path: dict[Path, list[Target]] = {}
    for target in targets:
        by_path.setdefault(target.path, []).append(target)
    rendered: dict[Path, str] = {}
    for path, path_targets in by_path.items():
        output = texts[path]
        for target in sorted(path_targets, key=lambda item: item.start, reverse=True):
            replacement = f'{target.indent}.string "{encode_assembly_body(target.thai)}"\n'
            output = output[:target.start] + replacement + output[target.end:]
        rendered[path] = output
    return rendered


def apply_sources(rendered: dict[Path, str]) -> None:
    temporary: list[tuple[Path, Path]] = []
    try:
        for path in sorted(rendered, key=relative):
            descriptor, name = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
            temp = Path(name)
            with os.fdopen(descriptor, "w", encoding="utf-8", newline="") as handle:
                handle.write(rendered[path])
            temporary.append((temp, path))
        for temp, path in temporary:
            os.replace(temp, path)
    finally:
        for temp, _ in temporary:
            if temp.exists():
                temp.unlink()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="modify resolved game sources")
    parser.add_argument("--master", type=Path, default=DEFAULT_MASTER, help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    try:
        master = args.master.resolve()
        if ROOT not in master.parents:
            raise InjectionError("master path must be inside the repository")
        rows = read_master(master)
        targets, texts = resolve(rows)
        rendered = rendered_sources(targets, texts)
        if args.apply:
            apply_sources(rendered)
        print("=== PHASE D INJECTION DRY-RUN ===" if not args.apply else "=== PHASE D INJECTION APPLY ===")
        print("STATUS: PASS")
        print(f"MASTER_ROWS: {len(rows)}")
        print(f"RESOLVED: {len(targets)}")
        print(f"UNIQUE_TARGETS: {len({(t.path, t.start, t.end) for t in targets})}")
        print(f"BASELINE_MATCH: {len(targets)}")
        print(f"CONTROL_PLACEHOLDER_GUARD: PASS ({len(rows)}/{len(rows)})")
        print(f"SOURCE_FILES_TARGETED: {len(rendered)}")
        print(f"SOURCE_FILES_MODIFIED: {len(rendered) if args.apply else 0}")
        print(f"READY_FOR_APPLY: {'YES' if not args.apply else 'APPLIED'}")
        return 0
    except (InjectionError, OSError, UnicodeError, csv.Error) as error:
        print(f"injection failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
