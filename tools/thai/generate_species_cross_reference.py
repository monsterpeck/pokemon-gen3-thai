#!/usr/bin/env python3
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

REF = ROOT / "tools/thai/translation/reference/species_names_th.csv"
CONSTANTS = ROOT / "include/constants/species.h"
ENGLISH = ROOT / "src/data/text/species_names.h"

OUT = ROOT / "tools/thai/translation/reference/species_names_cross_reference.csv"
REPORT = ROOT / "tools/thai/translation/reference/species_names_cross_reference_report.md"

const_re = re.compile(r"^#define\s+(SPECIES_[A-Z0-9_]+)\s+(\d+)\s*$")
name_re = re.compile(
    r'^\s*\[(SPECIES_[A-Z0-9_]+)\]\s*=\s*_\("([^"]*)"\),?\s*$'
)

constants = {}
for line in CONSTANTS.read_text(encoding="utf-8").splitlines():
    m = const_re.match(line)
    if m:
        constants[int(m.group(2))] = m.group(1)

english_by_constant = {}
for line in ENGLISH.read_text(encoding="utf-8").splitlines():
    m = name_re.match(line)
    if m:
        english_by_constant[m.group(1)] = m.group(2)

with REF.open(encoding="utf-8-sig", newline="") as f:
    ref_rows = list(csv.DictReader(f))

seen = set()
duplicates = []
active = []
reserved = []

for row in ref_rows:
    idx = int(row["index"])
    if idx in seen:
        duplicates.append(idx)
    seen.add(idx)

    if row["status"] == "SYSTEM_RESERVED":
        reserved.append(idx)
        continue
    active.append(row)

errors = []
out_rows = []

for row in active:
    idx = int(row["index"])
    constant = constants.get(idx)

    if constant is None:
        errors.append(f"index {idx}: missing SPECIES constant")
        continue

    english = english_by_constant.get(constant)
    if english is None:
        errors.append(f"index {idx} {constant}: missing English mapping")
        continue

    status = row["status"]
    out_rows.append({
        "species_index": idx,
        "species_constant": constant,
        "english_name": english,
        "japanese_name": row["source_jp"],
        "thai_name": row["translation_th"],
        "reference_status": status,
        "review_required": "YES" if status == "NEEDS_REVIEW_GLOSSARY_CHANGE" else "NO",
    })

if duplicates:
    errors.append("duplicate Species IDs: " + ",".join(map(str, sorted(duplicates))))

index80 = next((r for r in out_rows if r["species_index"] == 80), None)
if index80 is None:
    errors.append("index 80 missing from active cross-reference")
elif index80["review_required"] != "YES":
    errors.append(
        "index 80 is not marked Review "
        f"(reference_status={index80['reference_status']})"
    )

if len(out_rows) != len(active):
    errors.append(
        f"active/output mismatch: active={len(active)} output={len(out_rows)}"
    )

if errors:
    print("FAIL")
    for error in errors:
        print("-", error)
    raise SystemExit(1)

OUT.parent.mkdir(parents=True, exist_ok=True)

with OUT.open("w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "species_index",
            "species_constant",
            "english_name",
            "japanese_name",
            "thai_name",
            "reference_status",
            "review_required",
        ],
        lineterminator="\n",
    )
    writer.writeheader()
    writer.writerows(out_rows)

review_rows = [r for r in out_rows if r["review_required"] == "YES"]

REPORT.write_text(
    "\n".join([
        "# Species Names Cross-reference Report",
        "",
        "## Phase A",
        "",
        f"- Reference rows: {len(ref_rows)}",
        f"- Active species rows: {len(active)}",
        f"- Reserved rows excluded: {len(reserved)}",
        f"- Cross-reference rows generated: {len(out_rows)}",
        f"- Duplicate Species IDs: {len(duplicates)}",
        f"- Missing English mappings: 0",
        f"- Review rows: {len(review_rows)}",
        "",
        "## Validation",
        "",
        "- PASS: every active reference row has exactly one Internal Species ID / constant mapping.",
        "- PASS: every active reference row has an English runtime-name mapping.",
        "- PASS: SYSTEM_RESERVED rows are excluded.",
        "- PASS: Thai names are copied directly from species_names_th.csv translation_th.",
        "- PASS: Species ID 80 is marked for Review.",
        "",
        "## Review Required",
        "",
        *[
            f"- {r['species_index']} {r['species_constant']}: "
            f"{r['english_name']} → {r['japanese_name']} → {r['thai_name']} "
            f"({r['reference_status']})"
            for r in review_rows
        ],
        "",
        "Generated deterministically from:",
        "",
        "- include/constants/species.h",
        "- src/data/text/species_names.h",
        "- tools/thai/translation/reference/species_names_th.csv",
        "",
        "No game source files were modified by this generator.",
        "",
    ]),
    encoding="utf-8",
)

print("PASS")
print("reference rows:", len(ref_rows))
print("active:", len(active))
print("reserved excluded:", len(reserved))
print("generated:", len(out_rows))
print("review rows:", len(review_rows))
print("index80:", index80["reference_status"])
