#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import re
import shutil
from collections import OrderedDict
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

MASTER_CSV = (
    ROOT
    / "tools/thai/translation"
    / "move_names_thai.csv"
)

OUTPUT_DIR = (
    ROOT
    / "tools/thai/translation/batches"
)

BACKUP_DIR = Path(
    "/tmp/pokemon-gen3-thai-backups"
)

EXPECTED_MASTER_ROWS = 355


class BatchError(RuntimeError):
    pass


def species_to_symbol(species: str) -> str:
    parts = [
        part
        for part in species.lower().split("_")
        if part
    ]

    return "".join(
        part[:1].upper() + part[1:]
        for part in parts
    )


def safe_batch_id(value: str) -> str:
    normalized = re.sub(
        r"[^a-z0-9_-]+",
        "-",
        value.lower(),
    ).strip("-_")

    if not normalized:
        raise BatchError(
            "Batch ID ไม่ถูกต้อง"
        )

    return normalized


def load_master() -> dict[str, dict[str, str]]:
    if not MASTER_CSV.is_file():
        raise BatchError(
            "ไม่พบ Master CSV: "
            f"{MASTER_CSV.relative_to(ROOT)}"
        )

    with MASTER_CSV.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as handle:
        rows = list(
            csv.DictReader(handle)
        )

    if len(rows) != EXPECTED_MASTER_ROWS:
        raise BatchError(
            "จำนวน Master rows ไม่ถูกต้อง: "
            f"คาด {EXPECTED_MASTER_ROWS}, "
            f"พบ {len(rows)}"
        )

    required_fields = {
        "move_id",
        "move_constant",
        "english_name",
        "thai_name",
        "status",
    }

    actual_fields = (
        set(rows[0].keys())
        if rows
        else set()
    )

    missing_fields = sorted(
        required_fields - actual_fields
    )

    if missing_fields:
        raise BatchError(
            "Master CSV ขาดคอลัมน์: "
            + ", ".join(missing_fields)
        )

    result: dict[str, dict[str, str]] = {}

    for row in rows:
        constant = row[
            "move_constant"
        ].strip()

        if not constant:
            raise BatchError(
                "พบ Move constant ว่างใน Master CSV"
            )

        if constant in result:
            raise BatchError(
                f"พบ Move constant ซ้ำ: {constant}"
            )

        result[constant] = {
            key: (
                value.strip()
                if isinstance(value, str)
                else value
            )
            for key, value in row.items()
        }

    return result


def candidate_learnset_files() -> list[Path]:
    pokemon_dir = (
        ROOT / "src/data/pokemon"
    )

    preferred = (
        pokemon_dir
        / "level_up_learnsets.h"
    )

    paths: list[Path] = []

    if preferred.is_file():
        paths.append(preferred)

    for path in sorted(
        pokemon_dir.rglob(
            "*level*learnset*.h"
        )
    ):
        if path not in paths:
            paths.append(path)

    if not paths:
        raise BatchError(
            "ไม่พบไฟล์ Level-up learnset "
            "ใน src/data/pokemon"
        )

    return paths


def locate_learnset(
    species: str,
    paths: list[Path],
) -> tuple[Path, list[tuple[int, str]]]:
    symbol = (
        "s"
        + species_to_symbol(species)
        + "LevelUpLearnset"
    )

    declaration_pattern = re.compile(
        r"static\s+const\s+u16\s+"
        + re.escape(symbol)
        + r"\s*\[\]\s*=\s*\{"
        + r"(?P<body>.*?)"
        + r"\};",
        re.DOTALL,
    )

    move_pattern = re.compile(
        r"LEVEL_UP_MOVE\s*\(\s*"
        r"(?P<level>\d+)\s*,\s*"
        r"(?P<move>MOVE_[A-Z0-9_]+)"
        r"\s*\)"
    )

    for path in paths:
        text = path.read_text(
            encoding="utf-8"
        )

        match = declaration_pattern.search(
            text
        )

        if match is None:
            continue

        moves = [
            (
                int(move_match.group("level")),
                move_match.group("move"),
            )
            for move_match
            in move_pattern.finditer(
                match.group("body")
            )
        ]

        if not moves:
            raise BatchError(
                f"พบ {symbol} แต่ไม่มี LEVEL_UP_MOVE"
            )

        return path, moves

    raise BatchError(
        f"ไม่พบ Learnset symbol: {symbol}"
    )


def backup_existing(path: Path) -> Path | None:
    if not path.is_file():
        return None

    BACKUP_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    backup = (
        BACKUP_DIR
        / f"{path.stem}_{timestamp}{path.suffix}"
    )

    shutil.copy2(path, backup)

    return backup


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Create a move-name translation batch "
            "from Pokémon level-up learnsets."
        )
    )

    parser.add_argument(
        "--batch-id",
        required=True,
    )

    parser.add_argument(
        "--species",
        nargs="+",
        required=True,
    )

    args = parser.parse_args()

    batch_id = safe_batch_id(
        args.batch_id
    )

    species_list = [
        species.strip().upper()
        for species in args.species
        if species.strip()
    ]

    if not species_list:
        raise BatchError(
            "ไม่ได้ระบุ Species"
        )

    master = load_master()
    learnset_paths = candidate_learnset_files()

    records: OrderedDict[
        str,
        dict[str, object],
    ] = OrderedDict()

    source_files: set[Path] = set()

    print("========================================")
    print("MOVE NAME TRANSLATION BATCH")
    print("========================================")
    print(f"Batch ID : {batch_id}")
    print(
        "Species  : "
        + ", ".join(species_list)
    )
    print()

    for species_order, species in enumerate(
        species_list
    ):
        path, learnset = locate_learnset(
            species,
            learnset_paths,
        )

        source_files.add(path)

        print(
            f"{species:<10}: "
            f"{len(learnset)} entries "
            f"from {path.relative_to(ROOT)}"
        )

        for learn_order, (
            level,
            move_constant,
        ) in enumerate(learnset):
            master_row = master.get(
                move_constant
            )

            if master_row is None:
                raise BatchError(
                    "ไม่พบ Move ใน Master CSV: "
                    f"{move_constant}"
                )

            source_label = (
                f"{species}@Lv{level}"
            )

            if move_constant not in records:
                records[move_constant] = {
                    "species_order": species_order,
                    "learn_order": learn_order,
                    "move_id": master_row[
                        "move_id"
                    ],
                    "move_constant": move_constant,
                    "english_name": master_row[
                        "english_name"
                    ],
                    "current_thai_name": master_row[
                        "thai_name"
                    ],
                    "current_status": master_row[
                        "status"
                    ],
                    "sources": [
                        source_label
                    ],
                }
            else:
                sources = records[
                    move_constant
                ]["sources"]

                if isinstance(sources, list):
                    sources.append(
                        source_label
                    )

    output_rows = list(
        records.values()
    )

    output_rows.sort(
        key=lambda row: (
            int(row["species_order"]),
            int(row["learn_order"]),
            int(str(row["move_id"]), 0),
        )
    )

    csv_path = (
        OUTPUT_DIR
        / f"move_names_batch_{batch_id}.csv"
    )

    report_path = (
        OUTPUT_DIR
        / f"move_names_batch_{batch_id}.md"
    )

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    csv_backup = backup_existing(
        csv_path
    )

    report_backup = backup_existing(
        report_path
    )

    fieldnames = [
        "batch_id",
        "order",
        "move_id",
        "move_constant",
        "english_name",
        "current_thai_name",
        "current_status",
        "learnset_sources",
        "proposed_thai_name",
        "proposed_status",
        "reviewer_notes",
    ]

    with csv_path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
            lineterminator="\n",
        )

        writer.writeheader()

        for order, row in enumerate(
            output_rows,
            start=1,
        ):
            current_thai = str(
                row["current_thai_name"]
            )

            current_status = str(
                row["current_status"]
            )

            writer.writerow(
                {
                    "batch_id": batch_id,
                    "order": order,
                    "move_id": row["move_id"],
                    "move_constant": row[
                        "move_constant"
                    ],
                    "english_name": row[
                        "english_name"
                    ],
                    "current_thai_name": (
                        current_thai
                    ),
                    "current_status": (
                        current_status
                    ),
                    "learnset_sources": "; ".join(
                        row["sources"]
                    ),
                    "proposed_thai_name": (
                        current_thai
                    ),
                    "proposed_status": (
                        current_status
                        if current_thai
                        else ""
                    ),
                    "reviewer_notes": "",
                }
            )

    translated_count = sum(
        1
        for row in output_rows
        if str(
            row["current_thai_name"]
        )
    )

    pending_count = (
        len(output_rows)
        - translated_count
    )

    report_lines = [
        "# Move Name Translation Batch",
        "",
        f"- Batch ID: `{batch_id}`",
        (
            "- Species: "
            + ", ".join(
                f"`{species}`"
                for species in species_list
            )
        ),
        (
            f"- Unique moves: "
            f"**{len(output_rows)}**"
        ),
        (
            f"- Already translated: "
            f"**{translated_count}**"
        ),
        (
            f"- Pending translation: "
            f"**{pending_count}**"
        ),
        "",
        "## Source Files",
        "",
    ]

    for path in sorted(source_files):
        report_lines.append(
            f"- `{path.relative_to(ROOT)}`"
        )

    report_lines.extend(
        [
            "",
            "## Move Inventory",
            "",
            (
                "| # | ID | Constant | English | "
                "Current Thai | Sources |"
            ),
            "|---:|---:|---|---|---|---|",
        ]
    )

    for order, row in enumerate(
        output_rows,
        start=1,
    ):
        sources = "<br>".join(
            row["sources"]
        )

        report_lines.append(
            f"| {order} "
            f"| {row['move_id']} "
            f"| `{row['move_constant']}` "
            f"| {row['english_name']} "
            f"| {row['current_thai_name']} "
            f"| {sources} |"
        )

    report_path.write_text(
        "\n".join(report_lines) + "\n",
        encoding="utf-8",
    )

    print()
    print(
        f"Unique moves       : {len(output_rows)}"
    )
    print(
        f"Already translated : {translated_count}"
    )
    print(
        f"Pending            : {pending_count}"
    )

    if csv_backup:
        print(
            f"CSV backup         : {csv_backup}"
        )

    if report_backup:
        print(
            f"Report backup      : {report_backup}"
        )

    print()
    print(
        "CSV                : "
        f"{csv_path.relative_to(ROOT)}"
    )
    print(
        "Report             : "
        f"{report_path.relative_to(ROOT)}"
    )
    print()
    print(
        "RESULT: MOVE NAME BATCH CREATED"
    )

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BatchError as error:
        print(
            f"ERROR: {error}"
        )
        print(
            "RESULT: MOVE NAME BATCH FAILED"
        )
        raise SystemExit(1)
