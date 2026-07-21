#!/usr/bin/env python3
"""Check Thai text coverage against the full 761-glyph precompose map."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MAP_CANDIDATES = (
    ROOT / "tools/thai/font/thai_precompose_glyph_map.json",
    ROOT / "tools/thai/generated/precompose_full/thai_precompose_full_map.json",
)
DEFAULT_PATHS = (
    ROOT / "src",
    ROOT / "data",
    ROOT / "include",
    ROOT / "asm",
    ROOT / "sound",
    ROOT / "tools/thai/translation",
)
REPORT_DIR = ROOT / "tools/thai/generated/precompose_coverage"

THAI_RE = re.compile(r"[\u0E00-\u0E7F]+")
STRING_RE = re.compile(r'"(?:\\.|[^"\\])*"', re.DOTALL)
CODE_EXTS = {".c", ".h", ".s", ".inc"}
TEXT_EXTS = {".csv", ".json", ".txt", ".md"}
EXTS = CODE_EXTS | TEXT_EXTS
EXCLUDED_DIRS = {".git", ".vscode", "__pycache__", "build", "cache", "generated"}
EXPECTED_FORMAT = "pokemon-gen3-thai-precompose-full-v1"
EXPECTED_GLYPHS = 761


class CoverageError(RuntimeError):
    pass


def show_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT.resolve()))
    except ValueError:
        return str(path.resolve())


def resolve_map(explicit: Path | None) -> Path:
    if explicit:
        path = explicit.expanduser().resolve()
        if not path.is_file():
            raise CoverageError(f"ไม่พบ Map: {path}")
        return path
    for path in MAP_CANDIDATES:
        if path.is_file():
            return path.resolve()
    raise CoverageError("ไม่พบ Full Precompose map")


def load_map(path: Path):
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("format") != EXPECTED_FORMAT:
        raise CoverageError(f"Map format ไม่ถูกต้อง: {data.get('format')!r}")
    glyphs = data.get("glyphs")
    if not isinstance(glyphs, list) or len(glyphs) != EXPECTED_GLYPHS:
        raise CoverageError(f"Map ต้องมี {EXPECTED_GLYPHS} Glyph")
    lookup = {}
    indices = []
    for pos, entry in enumerate(glyphs):
        if not isinstance(entry, dict):
            raise CoverageError(f"glyphs[{pos}] ไม่ใช่ Object")
        name = entry.get("name")
        idx = entry.get("target_index")
        advance = entry.get("advance")
        if not isinstance(name, str) or not name:
            raise CoverageError(f"glyphs[{pos}] ไม่มี name")
        if name in lookup:
            raise CoverageError(f"ชื่อ Glyph ซ้ำ: {name!r}")
        if not isinstance(idx, int):
            raise CoverageError(f"{name!r} ไม่มี target_index")
        if not isinstance(advance, int) or advance <= 0:
            raise CoverageError(f"{name!r} ไม่มี advance ที่ถูกต้อง")
        lookup[name] = entry
        indices.append(idx)
    if sorted(indices) != list(range(EXPECTED_GLYPHS)):
        raise CoverageError("target_index ต้องต่อเนื่อง 0..760")
    csv_only = data.get("csv_only", [])
    if not isinstance(csv_only, list):
        csv_only = []
    return data, lookup, max(map(len, lookup)), [x for x in csv_only if isinstance(x, str)]


def iter_files(paths: list[Path]):
    seen = set()
    for raw in paths:
        path = raw.expanduser().resolve()
        if not path.exists():
            continue
        candidates = [path] if path.is_file() else path.rglob("*")
        for file in candidates:
            if not file.is_file():
                continue
            if file.suffix.lower() not in EXTS:
                continue
            if any(part in EXCLUDED_DIRS for part in file.parts):
                continue
            resolved = file.resolve()
            if resolved not in seen:
                seen.add(resolved)
                yield resolved


def iter_runs(text: str, suffix: str):
    if suffix in CODE_EXTS:
        for literal in STRING_RE.finditer(text):
            body = literal.group(0)[1:-1]
            base = literal.start() + 1
            for run in THAI_RE.finditer(body):
                start = base + run.start()
                end = base + run.end()
                yield start, end, "string_literal"
    else:
        for run in THAI_RE.finditer(text):
            yield run.start(), run.end(), "plain_text"


def tokenize(run: str, lookup, max_len: int):
    tokens = []
    pos = 0
    while pos < len(run):
        match = None
        for end in range(min(len(run), pos + max_len), pos, -1):
            candidate = run[pos:end]
            if candidate in lookup:
                match = candidate
                break
        if match is None:
            return tokens, pos
        tokens.append(match)
        pos += len(match)
    return tokens, None


def line_col(text: str, offset: int):
    line = text.count("\n", 0, offset) + 1
    prev = text.rfind("\n", 0, offset)
    col = offset + 1 if prev < 0 else offset - prev
    return line, col


def context_line(text: str, offset: int):
    start = text.rfind("\n", 0, offset) + 1
    end = text.find("\n", offset)
    if end < 0:
        end = len(text)
    value = re.sub(r"\s+", " ", text[start:end].strip())
    return value[:160]


def csv_hints(run: str, fail_pos: int, csv_only: list[str]):
    hints = []
    for item in csv_only:
        start = run.find(item)
        if start >= 0 and start <= fail_pos < start + len(item):
            hints.append(item)
    return sorted(set(hints))


def scan_file(path: Path, lookup, max_len: int, csv_only: list[str]):
    text = path.read_text(encoding="utf-8")
    findings = []
    counter = Counter()
    total_runs = 0
    covered_runs = 0
    for start, end, mode in iter_runs(text, path.suffix.lower()):
        run = text[start:end]
        total_runs += 1
        tokens, fail_pos = tokenize(run, lookup, max_len)
        counter.update(tokens)
        if fail_pos is None:
            covered_runs += 1
            continue
        absolute = start + fail_pos
        line, col = line_col(text, absolute)
        char = run[fail_pos]
        findings.append({
            "file": show_path(path),
            "line": line,
            "column": col,
            "thai_run": run,
            "matched_prefix": "".join(tokens),
            "unsupported_remainder": run[fail_pos:],
            "unsupported_character": char,
            "unsupported_codepoint": f"U+{ord(char):04X}",
            "csv_only_hints": csv_hints(run, fail_pos, csv_only),
            "source_mode": mode,
            "context": context_line(text, absolute),
        })
    return findings, counter, total_runs, covered_runs


def write_reports(report_dir: Path, summary: dict, findings: list[dict], tokens: Counter):
    report_dir.mkdir(parents=True, exist_ok=True)
    json_path = report_dir / "precompose_coverage_report.json"
    csv_path = report_dir / "precompose_coverage_findings.csv"
    md_path = report_dir / "precompose_coverage_report.md"

    payload = {**summary, "top_tokens": tokens.most_common(100), "findings": findings}
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    fields = [
        "file", "line", "column", "thai_run", "matched_prefix",
        "unsupported_remainder", "unsupported_character",
        "unsupported_codepoint", "csv_only_hints", "source_mode", "context",
    ]
    with csv_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for finding in findings:
            row = dict(finding)
            row["csv_only_hints"] = " | ".join(finding["csv_only_hints"])
            writer.writerow(row)

    lines = [
        "# Thai Precompose Coverage Report", "",
        f"- Files scanned: **{summary['files_scanned']}**",
        f"- Thai runs: **{summary['thai_runs']}**",
        f"- Covered runs: **{summary['covered_runs']}**",
        f"- Unsupported runs: **{summary['unsupported_runs']}**",
        f"- Unique tokens used: **{summary['unique_tokens']}**", "",
    ]
    if findings:
        lines += [
            "## Unsupported sequences", "",
            "| File | Line | Thai run | Unsupported | Code point | CSV-only hint |",
            "|---|---:|---|---|---|---|",
        ]
        for item in findings:
            hints = ", ".join(item["csv_only_hints"]) or "—"
            lines.append(
                f"| `{item['file']}` | {item['line']}:{item['column']} | "
                f"`{item['thai_run']}` | `{item['unsupported_remainder']}` | "
                f"`{item['unsupported_codepoint']}` | `{hints}` |"
            )
    else:
        lines += ["## Result", "", "**PASS — All scanned Thai runs are covered.**"]
    lines += ["", "## Most-used tokens", "", "| Token | Count |", "|---|---:|"]
    for token, count in tokens.most_common(50):
        lines.append(f"| `{token}` | {count} |")
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return json_path, csv_path, md_path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--map", type=Path)
    parser.add_argument("--path", action="append", type=Path, dest="paths")
    parser.add_argument("--report-dir", type=Path, default=REPORT_DIR)
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--show", type=int, default=30)
    args = parser.parse_args()

    try:
        map_path = resolve_map(args.map)
        _data, lookup, max_len, csv_only = load_map(map_path)
        scan_paths = args.paths or [p for p in DEFAULT_PATHS if p.exists()]
        files = list(iter_files(scan_paths))
        if not files:
            raise CoverageError("ไม่พบไฟล์สำหรับตรวจ")

        all_findings = []
        all_tokens = Counter()
        total_runs = 0
        covered_runs = 0
        skipped = []

        for path in files:
            try:
                findings, tokens, runs, covered = scan_file(path, lookup, max_len, csv_only)
            except UnicodeDecodeError:
                skipped.append(show_path(path))
                continue
            all_findings.extend(findings)
            all_tokens.update(tokens)
            total_runs += runs
            covered_runs += covered

        summary = {
            "format": "pokemon-gen3-thai-precompose-coverage-v1",
            "map": show_path(map_path),
            "scan_paths": [show_path(p) for p in scan_paths],
            "files_scanned": len(files) - len(skipped),
            "skipped_files": skipped,
            "thai_runs": total_runs,
            "covered_runs": covered_runs,
            "unsupported_runs": len(all_findings),
            "unique_tokens": len(all_tokens),
            "total_tokens": sum(all_tokens.values()),
        }
        reports = write_reports(args.report_dir.expanduser().resolve(), summary, all_findings, all_tokens)

        print("========================================")
        print("THAI PRECOMPOSE COVERAGE")
        print("========================================")
        print(f"Map              : {show_path(map_path)}")
        print(f"Glyph count      : {len(lookup)}")
        print(f"Max cluster size : {max_len}")
        print(f"Files scanned    : {summary['files_scanned']}")
        print(f"Thai runs        : {total_runs}")
        print(f"Covered runs     : {covered_runs}")
        print(f"Unsupported runs : {len(all_findings)}")
        print(f"Unique tokens    : {len(all_tokens)}")
        print(f"Skipped files    : {len(skipped)}")
        print()

        if all_findings:
            print("FIRST FINDINGS")
            print("--------------")
            for item in all_findings[:max(0, args.show)]:
                hint = (
                    " | CSV-only: " + ", ".join(item["csv_only_hints"])
                    if item["csv_only_hints"] else ""
                )
                print(
                    f"{item['file']}:{item['line']}:{item['column']}: "
                    f"{item['thai_run']!r} -> "
                    f"unsupported {item['unsupported_remainder']!r} "
                    f"({item['unsupported_codepoint']}){hint}"
                )
            remaining = len(all_findings) - max(0, args.show)
            if remaining > 0:
                print(f"... อีก {remaining} รายการใน Report")
            print()

        print("REPORTS")
        print("-------")
        for report in reports:
            print(show_path(report))
        print()

        if all_findings:
            print("RESULT: COVERAGE FAILED")
            return 1 if args.strict else 0

        print("RESULT: COVERAGE PASSED")
        return 0

    except (CoverageError, json.JSONDecodeError) as exc:
        print(f"Coverage checker error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
