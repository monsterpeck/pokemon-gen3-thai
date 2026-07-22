#!/usr/bin/env python3
from __future__ import annotations

import csv
import re
import shutil
import subprocess
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

INVENTORY_CSV = (
    ROOT
    / "tools/thai/generated/move_names"
    / "move_names_inventory.csv"
)

FALLBACK_SOURCE = (
    ROOT
    / "src/data/text/move_names.h"
)

OUTPUT_CSV = (
    ROOT
    / "tools/thai/translation"
    / "move_names_thai.csv"
)

REPORT_PATH = (
    ROOT
    / "tools/thai/translation"
    / "move_names_translation_report.md"
)

EXPECTED_MOVE_COUNT = 355

SEED_TRANSLATIONS = {
    "MOVE_SCRATCH": {
        "thai_name": "ข่วน",
        "status": "proof_passed",
        "translation_source": "torchic_runtime_proof",
        "qa_notes": (
            "ผ่าน Battle Menu, Battle Message, "
            "Battle Moves และ Contest Moves"
        ),
    },
    "MOVE_GROWL": {
        "thai_name": "คำราม",
        "status": "proof_passed",
        "translation_source": "torchic_runtime_proof",
        "qa_notes": (
            "ผ่าน Battle Menu, Battle Moves "
            "และ Contest Moves"
        ),
    },
    "MOVE_FOCUS_ENERGY": {
        "thai_name": "รวมพลัง",
        "status": "proof_passed",
        "translation_source": "torchic_runtime_proof",
        "qa_notes": (
            "ผ่าน Battle Menu, Battle Moves "
            "และ Contest Moves"
        ),
    },
}

OUTPUT_FIELDS = [
    "move_id",
    "move_constant",
    "english_name",
    "thai_name",
    "status",
    "translation_source",
    "qa_notes",
]


def get_git_value(args: list[str]) -> str:
    try:
        return subprocess.check_output(
            ["git", *args],
            cwd=ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except subprocess.SubprocessError:
        return "UNKNOWN"


def detect_field(
    fieldnames: list[str],
    candidates: tuple[str, ...],
) -> str | None:
    normalized = {
        field.strip().lower(): field
        for field in fieldnames
        if field
    }

    for candidate in candidates:
        if candidate in normalized:
            return normalized[candidate]

    return None


def load_inventory_csv() -> list[dict[str, str]]:
    with INVENTORY_CSV.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        fieldnames = list(reader.fieldnames or [])

    constant_field = detect_field(
        fieldnames,
        (
            "move_constant",
            "constant",
            "move_symbol",
            "symbol",
        ),
    )

    english_field = detect_field(
        fieldnames,
        (
            "english_name",
            "move_name",
            "name",
            "english",
        ),
    )

    id_field = detect_field(
        fieldnames,
        (
            "move_id",
            "move_index",
            "index",
            "id",
        ),
    )

    if constant_field is None or english_field is None:
        raise ValueError(
            "ไม่พบคอลัมน์ Move constant หรือ English name "
            f"ใน Inventory: {fieldnames}"
        )

    result = []

    for fallback_id, row in enumerate(rows):
        move_constant = row.get(
            constant_field,
            "",
        ).strip()

        english_name = row.get(
            english_field,
            "",
        ).strip()

        raw_id = (
            row.get(id_field, "").strip()
            if id_field
            else ""
        )

        move_id = raw_id or str(fallback_id)

        if not move_constant:
            continue

        result.append(
            {
                "move_id": move_id,
                "move_constant": move_constant,
                "english_name": english_name,
            }
        )

    return result


def load_fallback_source() -> list[dict[str, str]]:
    source = FALLBACK_SOURCE.read_text(
        encoding="utf-8",
    )

    pattern = re.compile(
        r"\[\s*(MOVE_[A-Z0-9_]+)\s*\]\s*="
        r'\s*_\("((?:\\.|[^"\\])*)"\)'
    )

    matches = pattern.findall(source)

    return [
        {
            "move_id": str(move_id),
            "move_constant": move_constant,
            "english_name": english_name,
        }
        for move_id, (
            move_constant,
            english_name,
        ) in enumerate(matches)
    ]


def load_existing_translations() -> dict[str, dict[str, str]]:
    if not OUTPUT_CSV.is_file():
        return {}

    with OUTPUT_CSV.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as handle:
        reader = csv.DictReader(handle)

        return {
            row.get("move_constant", "").strip(): row
            for row in reader
            if row.get("move_constant", "").strip()
        }


def backup_existing_output() -> Path | None:
    if not OUTPUT_CSV.is_file():
        return None

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    backup_path = (
        Path("/tmp/pokemon-gen3-thai-backups")
        / f"move_names_thai_{timestamp}.csv"
    )

    shutil.copy2(
        OUTPUT_CSV,
        backup_path,
    )

    return backup_path


def normalize_move_id(value: str, fallback: int) -> str:
    value = value.strip()

    try:
        return str(int(value, 0))
    except ValueError:
        return str(fallback)


def main() -> int:
    print("========================================")
    print("MOVE NAME TRANSLATION TABLE BUILDER")
    print("========================================")
    print(f"Repository : {ROOT}")
    print(
        "Branch     : "
        + get_git_value(
            ["branch", "--show-current"]
        )
    )
    print(
        "HEAD       : "
        + get_git_value(
            ["log", "-1", "--oneline"]
        )
    )
    print()

    inventory_source = "inventory_csv"

    try:
        if not INVENTORY_CSV.is_file():
            raise FileNotFoundError(
                INVENTORY_CSV
            )

        inventory_rows = load_inventory_csv()
    except (
        FileNotFoundError,
        ValueError,
        csv.Error,
    ) as error:
        print(
            "Inventory CSV ใช้งานไม่ได้ "
            f"จึงอ่านจาก move_names.h: {error}"
        )

        inventory_source = "move_names_header"
        inventory_rows = load_fallback_source()

    if len(inventory_rows) != EXPECTED_MOVE_COUNT:
        print(
            "ERROR: จำนวนชื่อท่าไม่ตรงตามที่คาด"
        )
        print(
            f"Expected : {EXPECTED_MOVE_COUNT}"
        )
        print(
            f"Found    : {len(inventory_rows)}"
        )
        print(
            "RESULT: TRANSLATION TABLE BUILD FAILED"
        )
        return 1

    constants = [
        row["move_constant"]
        for row in inventory_rows
    ]

    duplicate_constants = sorted(
        constant
        for constant, count
        in Counter(constants).items()
        if count > 1
    )

    if duplicate_constants:
        print(
            "ERROR: พบ Move constants ซ้ำ:"
        )

        for constant in duplicate_constants:
            print(f"  {constant}")

        print(
            "RESULT: TRANSLATION TABLE BUILD FAILED"
        )
        return 1

    missing_seeds = sorted(
        set(SEED_TRANSLATIONS)
        - set(constants)
    )

    if missing_seeds:
        print(
            "ERROR: ไม่พบ Move constants "
            "สำหรับ Runtime Proof:"
        )

        for constant in missing_seeds:
            print(f"  {constant}")

        print(
            "RESULT: TRANSLATION TABLE BUILD FAILED"
        )
        return 1

    previous_rows = load_existing_translations()
    backup_path = backup_existing_output()

    output_rows = []

    for fallback_id, source_row in enumerate(
        inventory_rows
    ):
        move_constant = source_row[
            "move_constant"
        ]

        previous = previous_rows.get(
            move_constant,
            {},
        )

        row = {
            "move_id": normalize_move_id(
                source_row.get("move_id", ""),
                fallback_id,
            ),
            "move_constant": move_constant,
            "english_name": source_row[
                "english_name"
            ],
            "thai_name": previous.get(
                "thai_name",
                "",
            ).strip(),
            "status": previous.get(
                "status",
                "pending",
            ).strip() or "pending",
            "translation_source": previous.get(
                "translation_source",
                "",
            ).strip(),
            "qa_notes": previous.get(
                "qa_notes",
                "",
            ).strip(),
        }

        if move_constant in SEED_TRANSLATIONS:
            row.update(
                SEED_TRANSLATIONS[
                    move_constant
                ]
            )

        output_rows.append(row)

    OUTPUT_CSV.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with OUTPUT_CSV.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=OUTPUT_FIELDS,
            lineterminator="\n",
        )

        writer.writeheader()
        writer.writerows(output_rows)

    status_counts = Counter(
        row["status"]
        for row in output_rows
    )

    translated_rows = [
        row
        for row in output_rows
        if row["thai_name"]
    ]

    report_lines = [
        "# Move Name Translation Report",
        "",
        f"- Repository: `{ROOT}`",
        (
            "- Branch: `"
            + get_git_value(
                ["branch", "--show-current"]
            )
            + "`"
        ),
        (
            "- HEAD: `"
            + get_git_value(
                ["log", "-1", "--oneline"]
            )
            + "`"
        ),
        f"- Inventory source: `{inventory_source}`",
        f"- Total moves: **{len(output_rows)}**",
        f"- Thai names entered: **{len(translated_rows)}**",
        (
            "- Pending: **"
            f"{status_counts.get('pending', 0)}"
            "**"
        ),
        (
            "- Runtime proof passed: **"
            f"{status_counts.get('proof_passed', 0)}"
            "**"
        ),
        "",
        "## Runtime Proof Names",
        "",
        "| ID | Constant | English | Thai | Status |",
        "|---:|---|---|---|---|",
    ]

    for row in translated_rows:
        report_lines.append(
            "| "
            + row["move_id"]
            + " | `"
            + row["move_constant"]
            + "` | "
            + row["english_name"]
            + " | "
            + row["thai_name"]
            + " | "
            + row["status"]
            + " |"
        )

    report_lines.extend(
        [
            "",
            "## Status Counts",
            "",
        ]
    )

    for status, count in sorted(
        status_counts.items()
    ):
        report_lines.append(
            f"- `{status}`: {count}"
        )

    REPORT_PATH.write_text(
        "\n".join(report_lines) + "\n",
        encoding="utf-8",
    )

    print(f"Inventory source : {inventory_source}")
    print(f"Total moves      : {len(output_rows)}")
    print(f"Thai names       : {len(translated_rows)}")
    print(
        "Proof passed     : "
        f"{status_counts.get('proof_passed', 0)}"
    )
    print(
        "Pending          : "
        f"{status_counts.get('pending', 0)}"
    )

    if backup_path:
        print(f"Backup           : {backup_path}")

    print()
    print("Runtime proof entries:")

    for row in translated_rows:
        print(
            f"  {row['move_constant']:<22}"
            f" {row['english_name']:<16}"
            f" -> {row['thai_name']}"
        )

    print()
    print(
        "CSV    : "
        f"{OUTPUT_CSV.relative_to(ROOT)}"
    )
    print(
        "Report : "
        f"{REPORT_PATH.relative_to(ROOT)}"
    )
    print()
    print(
        "RESULT: MOVE NAME TRANSLATION "
        "TABLE CREATED"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
