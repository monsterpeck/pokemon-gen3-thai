#!/usr/bin/env python3
"""Scan source strings and rank registered and unsupported Thai sequences."""

from __future__ import annotations

import argparse
import csv
import re
import unicodedata
from collections import Counter
from pathlib import Path

from encode_thai_text import C_STRING_RE, is_thai
from thai_font import ROOT, load_registry


SOURCE_SUFFIXES = {".c", ".h", ".inc", ".s"}


def rough_clusters(text: str) -> list[str]:
    clusters = []
    index = 0
    while index < len(text):
        if not is_thai(text[index]):
            index += 1
            continue
        start = index
        if text[index] in "เแโใไ" and index + 1 < len(text) and is_thai(text[index + 1]):
            index += 1
        index += 1
        while index < len(text) and is_thai(text[index]) and (
            unicodedata.combining(text[index]) or text[index] in "ะาำๅ"
        ):
            index += 1
        clusters.append(text[start:index])
    return clusters


def scan(paths: list[Path]):
    registered = {glyph.display: glyph.token for glyph in load_registry() if glyph.status != "unused"}
    counts = Counter()
    locations: dict[str, set[str]] = {}
    for path in paths:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for match in C_STRING_RE.finditer(text):
            for cluster in rough_clusters(match.group(2)):
                counts[cluster] += 1
                locations.setdefault(cluster, set()).add(str(path.relative_to(ROOT)))
    rows = []
    for cluster, count in counts.most_common():
        rows.append({
            "cluster": cluster,
            "codepoints": " ".join(f"U+{ord(c):04X}" for c in cluster),
            "count": count,
            "status": "registered" if cluster in registered else "missing",
            "token": registered.get(cluster, ""),
            "files": ";".join(sorted(locations[cluster])),
        })
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="*", type=Path)
    parser.add_argument("--output", type=Path, default=ROOT / "tools/thai/generated/thai_clusters.csv")
    args = parser.parse_args()
    roots = args.paths or [ROOT / "src", ROOT / "include", ROOT / "data"]
    paths = []
    for root in roots:
        if root.is_file():
            paths.append(root)
        elif root.exists():
            paths.extend(path for path in root.rglob("*") if path.suffix in SOURCE_SUFFIXES)
    rows = scan(paths)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=("cluster", "codepoints", "count", "status", "token", "files"))
        writer.writeheader()
        writer.writerows(rows)
    missing = sum(row["status"] == "missing" for row in rows)
    print(f"wrote {args.output}: {len(rows)} clusters, {missing} missing")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
