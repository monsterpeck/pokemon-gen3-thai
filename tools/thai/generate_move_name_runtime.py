#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import difflib
import hashlib
import re
import shutil
import sys
import tempfile
from collections import Counter
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

TRANSLATION_CSV = (
    ROOT
    / "tools/thai/translation"
    / "move_names_thai.csv"
)

MOVE_CONSTANTS_HEADER = (
    ROOT
    / "include/constants/moves.h"
)

OUTPUT_SOURCE = (
    ROOT
    / "src/move_names.c"
)

GENERATED_REPORT = (
    ROOT
    / "tools/thai/generated/move_names"
    / "move_name_runtime_generation_report.md"
)

PREVIEW_SOURCE = Path(
    "/tmp/move_names.generated.c"
)

BACKUP_DIR = Path(
    "/tmp/pokemon-gen3-thai-backups"
)

EXPECTED_MOVE_COUNT = 355

REQUIRED_FIELDS = {
    "move_id",
    "move_constant",
    "english_name",
    "thai_name",
    "status",
    "translation_source",
    "qa_notes",
}


class GenerationError(RuntimeError):
    pass


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return sha256_bytes(
        text.encode("utf-8")
    )


def read_text(path: Path) -> str:
    try:
        return path.read_text(
            encoding="utf-8"
        )
    except FileNotFoundError as error:
        raise GenerationError(
            f"ไม่พบไฟล์: {path.relative_to(ROOT)}"
        ) from error


def parse_move_id(
    raw_value: str,
    row_number: int,
) -> int:
    value = raw_value.strip()

    try:
        move_id = int(value, 0)
    except ValueError as error:
        raise GenerationError(
            "Move ID ไม่ถูกต้องที่ CSV row "
            f"{row_number}: {value!r}"
        ) from error

    if move_id < 0:
        raise GenerationError(
            "Move ID ต้องไม่ติดลบที่ CSV row "
            f"{row_number}: {move_id}"
        )

    return move_id


def load_translation_rows() -> list[dict[str, str | int]]:
    if not TRANSLATION_CSV.is_file():
        raise GenerationError(
            "ไม่พบ Translation CSV: "
            f"{TRANSLATION_CSV.relative_to(ROOT)}"
        )

    with TRANSLATION_CSV.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as handle:
        reader = csv.DictReader(handle)
        fieldnames = set(
            reader.fieldnames or []
        )

        missing_fields = sorted(
            REQUIRED_FIELDS - fieldnames
        )

        if missing_fields:
            raise GenerationError(
                "Translation CSV ขาดคอลัมน์: "
                + ", ".join(missing_fields)
            )

        raw_rows = list(reader)

    if len(raw_rows) != EXPECTED_MOVE_COUNT:
        raise GenerationError(
            "จำนวน Move rows ไม่ถูกต้อง: "
            f"คาด {EXPECTED_MOVE_COUNT}, "
            f"พบ {len(raw_rows)}"
        )

    rows: list[dict[str, str | int]] = []

    for csv_index, raw_row in enumerate(
        raw_rows,
        start=2,
    ):
        move_constant = raw_row[
            "move_constant"
        ].strip()

        english_name = raw_row[
            "english_name"
        ].strip()

        thai_name = raw_row[
            "thai_name"
        ].strip()

        status = raw_row[
            "status"
        ].strip() or "pending"

        if not re.fullmatch(
            r"MOVE_[A-Z0-9_]+",
            move_constant,
        ):
            raise GenerationError(
                "Move constant ไม่ถูกต้องที่ CSV row "
                f"{csv_index}: {move_constant!r}"
            )

        if not english_name:
            raise GenerationError(
                "English name ว่างที่ CSV row "
                f"{csv_index}: {move_constant}"
            )

        if any(
            character in thai_name
            for character in (
                "\x00",
                "\r",
                "\n",
            )
        ):
            raise GenerationError(
                "Thai name มีอักขระควบคุมที่ "
                f"{move_constant}"
            )

        if thai_name and status == "pending":
            raise GenerationError(
                f"{move_constant} มีชื่อไทยแล้ว "
                "แต่ Status ยังเป็น pending"
            )

        if (
            not thai_name
            and status == "proof_passed"
        ):
            raise GenerationError(
                f"{move_constant} เป็น proof_passed "
                "แต่ไม่มีชื่อไทย"
            )

        rows.append(
            {
                "move_id": parse_move_id(
                    raw_row["move_id"],
                    csv_index,
                ),
                "move_constant": move_constant,
                "english_name": english_name,
                "thai_name": thai_name,
                "status": status,
                "translation_source": raw_row[
                    "translation_source"
                ].strip(),
                "qa_notes": raw_row[
                    "qa_notes"
                ].strip(),
            }
        )

    ids = [
        int(row["move_id"])
        for row in rows
    ]

    constants = [
        str(row["move_constant"])
        for row in rows
    ]

    duplicate_ids = sorted(
        move_id
        for move_id, count
        in Counter(ids).items()
        if count > 1
    )

    duplicate_constants = sorted(
        constant
        for constant, count
        in Counter(constants).items()
        if count > 1
    )

    if duplicate_ids:
        raise GenerationError(
            "พบ Move ID ซ้ำ: "
            + ", ".join(
                map(str, duplicate_ids)
            )
        )

    if duplicate_constants:
        raise GenerationError(
            "พบ Move constant ซ้ำ: "
            + ", ".join(
                duplicate_constants
            )
        )

    expected_ids = list(
        range(EXPECTED_MOVE_COUNT)
    )

    if sorted(ids) != expected_ids:
        missing_ids = sorted(
            set(expected_ids) - set(ids)
        )

        extra_ids = sorted(
            set(ids) - set(expected_ids)
        )

        raise GenerationError(
            "ลำดับ Move ID ไม่ครบ 0-354; "
            f"missing={missing_ids}, "
            f"extra={extra_ids}"
        )

    rows.sort(
        key=lambda row: int(
            row["move_id"]
        )
    )

    return rows


def load_known_constants() -> set[str]:
    header = read_text(
        MOVE_CONSTANTS_HEADER
    )

    constants = set(
        re.findall(
            r"\bMOVE_[A-Z0-9_]+\b",
            header,
        )
    )

    if not constants:
        raise GenerationError(
            "ไม่พบ Move constants ใน "
            f"{MOVE_CONSTANTS_HEADER.relative_to(ROOT)}"
        )

    return constants


def symbol_suffix(
    move_constant: str,
) -> str:
    name = move_constant.removeprefix(
        "MOVE_"
    )

    parts = [
        part
        for part in name.split("_")
        if part
    ]

    suffix = "".join(
        part[:1].upper()
        + part[1:].lower()
        for part in parts
    )

    if not suffix:
        raise GenerationError(
            "สร้าง Symbol suffix ไม่ได้จาก "
            f"{move_constant}"
        )

    return suffix


def c_string_escape(text: str) -> str:
    return (
        text
        .replace("\\", "\\\\")
        .replace('"', '\\"')
    )


def translated_rows(
    rows: list[dict[str, str | int]],
) -> list[dict[str, str | int]]:
    return [
        row
        for row in rows
        if str(row["thai_name"]).strip()
    ]


def validate_translated_constants(
    translated: list[
        dict[str, str | int]
    ],
    known_constants: set[str],
) -> None:
    missing = sorted(
        str(row["move_constant"])
        for row in translated
        if str(row["move_constant"])
        not in known_constants
    )

    if missing:
        raise GenerationError(
            "ไม่พบ Constant ต่อไปนี้ใน "
            "include/constants/moves.h: "
            + ", ".join(missing)
        )


def validate_symbol_collisions(
    translated: list[
        dict[str, str | int]
    ],
) -> None:
    symbols = [
        "sMoveNameThai_"
        + symbol_suffix(
            str(row["move_constant"])
        )
        for row in translated
    ]

    duplicates = sorted(
        symbol
        for symbol, count
        in Counter(symbols).items()
        if count > 1
    )

    if duplicates:
        raise GenerationError(
            "พบ Generated symbol ซ้ำ: "
            + ", ".join(duplicates)
        )


def generate_source(
    translated: list[
        dict[str, str | int]
    ],
) -> str:
    lines = [
        '#include "global.h"',
        '#include "data.h"',
        '#include "constants/moves.h"',
        "",
        "/*",
        " * Generated by "
        "tools/thai/generate_move_name_runtime.py",
        " * Source: "
        "tools/thai/translation/move_names_thai.csv",
        " * Do not edit this file manually.",
        " */",
    ]

    if translated:
        lines.append("")

    for row in translated:
        move_constant = str(
            row["move_constant"]
        )

        thai_name = c_string_escape(
            str(row["thai_name"])
        )

        symbol = (
            "sMoveNameThai_"
            + symbol_suffix(move_constant)
        )

        lines.append(
            f"static const u8 {symbol}[] = "
            f'_("{thai_name}");'
        )

    lines.extend(
        [
            "",
            "const u8 *GetMoveName(u16 move)",
            "{",
            "    switch (move)",
            "    {",
        ]
    )

    for row in translated:
        move_constant = str(
            row["move_constant"]
        )

        symbol = (
            "sMoveNameThai_"
            + symbol_suffix(move_constant)
        )

        lines.extend(
            [
                f"    case {move_constant}:",
                f"        return {symbol};",
            ]
        )

    lines.extend(
        [
            "    default:",
            "        if (move >= MOVES_COUNT)",
            "            move = MOVE_NONE;",
            "",
            "        return gMoveNames[move];",
            "    }",
            "}",
            "",
        ]
    )

    return "\n".join(lines)


def unified_diff(
    current: str,
    generated: str,
) -> str:
    return "".join(
        difflib.unified_diff(
            current.splitlines(
                keepends=True
            ),
            generated.splitlines(
                keepends=True
            ),
            fromfile="a/src/move_names.c",
            tofile="b/src/move_names.c",
        )
    )


def write_report(
    rows: list[
        dict[str, str | int]
    ],
    generated: str,
) -> None:
    translated = translated_rows(rows)

    status_counts = Counter(
        str(row["status"])
        for row in rows
    )

    lines = [
        "# Move Name Runtime Generation Report",
        "",
        (
            "- Source CSV: "
            "`tools/thai/translation/"
            "move_names_thai.csv`"
        ),
        (
            "- Output source: "
            "`src/move_names.c`"
        ),
        (
            f"- Total move rows: "
            f"**{len(rows)}**"
        ),
        (
            f"- Thai runtime overrides: "
            f"**{len(translated)}**"
        ),
        (
            f"- Pending translations: "
            f"**{status_counts.get('pending', 0)}**"
        ),
        (
            "- Generated source SHA-256: "
            f"`{sha256_text(generated)}`"
        ),
        "",
        "## Runtime Overrides",
        "",
        "| ID | Constant | English | Thai | Status |",
        "|---:|---|---|---|---|",
    ]

    for row in translated:
        lines.append(
            "| "
            f"{row['move_id']} | "
            f"`{row['move_constant']}` | "
            f"{row['english_name']} | "
            f"{row['thai_name']} | "
            f"{row['status']} |"
        )

    lines.extend(
        [
            "",
            "## Status Counts",
            "",
        ]
    )

    for status, count in sorted(
        status_counts.items()
    ):
        lines.append(
            f"- `{status}`: {count}"
        )

    GENERATED_REPORT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    GENERATED_REPORT.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )


def backup_current_source() -> Path:
    if not OUTPUT_SOURCE.is_file():
        raise GenerationError(
            "ไม่พบ Source ที่จะ Backup: "
            f"{OUTPUT_SOURCE.relative_to(ROOT)}"
        )

    BACKUP_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    backup_path = (
        BACKUP_DIR
        / f"move_names.c.{timestamp}.bak"
    )

    shutil.copy2(
        OUTPUT_SOURCE,
        backup_path,
    )

    return backup_path


def atomic_write(
    path: Path,
    text: str,
) -> None:
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        newline="\n",
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
        delete=False,
    ) as handle:
        temporary_path = Path(
            handle.name
        )

        handle.write(text)
        handle.flush()

    temporary_path.replace(path)


def show_summary(
    rows: list[
        dict[str, str | int]
    ],
    generated: str,
) -> None:
    translated = translated_rows(rows)

    status_counts = Counter(
        str(row["status"])
        for row in rows
    )

    print(
        f"CSV rows              : {len(rows)}"
    )

    print(
        "Thai runtime overrides: "
        f"{len(translated)}"
    )

    print(
        "Proof passed          : "
        f"{status_counts.get('proof_passed', 0)}"
    )

    print(
        "Pending               : "
        f"{status_counts.get('pending', 0)}"
    )

    print(
        "Generated SHA-256     : "
        f"{sha256_text(generated)}"
    )

    print()
    print("Runtime overrides:")

    for row in translated:
        print(
            f"  {int(row['move_id']):>3} | "
            f"{str(row['move_constant']):<24} | "
            f"{str(row['english_name']):<16} | "
            f"{row['thai_name']}"
        )


def run(action: str) -> int:
    rows = load_translation_rows()
    known_constants = load_known_constants()
    translated = translated_rows(rows)

    validate_translated_constants(
        translated,
        known_constants,
    )

    validate_symbol_collisions(
        translated
    )

    generated = generate_source(
        translated
    )

    current = (
        OUTPUT_SOURCE.read_text(
            encoding="utf-8"
        )
        if OUTPUT_SOURCE.is_file()
        else ""
    )

    print("========================================")
    print("MOVE NAME RUNTIME GENERATOR")
    print("========================================")
    print(f"Action                : {action}")
    print(
        "CSV                   : "
        f"{TRANSLATION_CSV.relative_to(ROOT)}"
    )
    print(
        "Output                : "
        f"{OUTPUT_SOURCE.relative_to(ROOT)}"
    )
    print()

    show_summary(
        rows,
        generated,
    )

    print()

    if action == "preview":
        PREVIEW_SOURCE.write_text(
            generated,
            encoding="utf-8",
        )

        print(
            f"Preview               : "
            f"{PREVIEW_SOURCE}"
        )

        print()
        print("SOURCE DIFF")
        print("-----------")

        diff = unified_diff(
            current,
            generated,
        )

        if diff:
            print(
                diff,
                end=(
                    ""
                    if diff.endswith("\n")
                    else "\n"
                ),
            )
        else:
            print(
                "(current source already matches)"
            )

        print()
        print(
            "RESULT: GENERATOR PREVIEW PASSED"
        )

        return 0

    if action == "check":
        if current != generated:
            print(
                "RESULT: GENERATED SOURCE OUT OF DATE"
            )
            print(
                "Run with action 'write' "
                "after reviewing preview."
            )
            return 1

        print(
            "RESULT: GENERATED SOURCE IS CURRENT"
        )
        return 0

    backup_path = backup_current_source()

    atomic_write(
        OUTPUT_SOURCE,
        generated,
    )

    write_report(
        rows,
        generated,
    )

    written = OUTPUT_SOURCE.read_text(
        encoding="utf-8"
    )

    if written != generated:
        raise GenerationError(
            "ตรวจสอบ Source หลังเขียนไม่ผ่าน"
        )

    print(
        f"Backup                : "
        f"{backup_path}"
    )

    print(
        "Report                : "
        f"{GENERATED_REPORT.relative_to(ROOT)}"
    )

    print()
    print(
        "RESULT: MOVE NAME RUNTIME SOURCE WRITTEN"
    )

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Generate Thai move-name runtime "
            "overrides from the translation CSV."
        )
    )

    parser.add_argument(
        "action",
        choices=(
            "preview",
            "write",
            "check",
        ),
    )

    args = parser.parse_args()

    return run(args.action)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except GenerationError as error:
        print(
            f"ERROR: {error}",
            file=sys.stderr,
        )
        print(
            "RESULT: MOVE NAME RUNTIME "
            "GENERATION FAILED",
            file=sys.stderr,
        )
        raise SystemExit(1)
    except KeyboardInterrupt:
        print(
            "\nCancelled. "
            "ไม่มีการเขียน Source เพิ่มเติม",
            file=sys.stderr,
        )
        raise SystemExit(130)
