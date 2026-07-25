#!/usr/bin/env python3

from __future__ import annotations

import ast
import csv
import re
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

MOVE_NAMES_FILE = ROOT / "src/data/text/move_names.h"
MOVE_DESCRIPTIONS_FILE = ROOT / "src/data/text/move_descriptions.h"

OUTPUT_FILE = (
    ROOT
    / "tools/thai/translation/inventory/move_descriptions.csv"
)


def decode_c_strings(expression: str) -> str:
    tokens = re.findall(r'"(?:\\.|[^"\\])*"', expression)

    if not tokens:
        raise ValueError("No C string literals were found.")

    decoded: list[str] = []

    for token in tokens:
        try:
            decoded.append(ast.literal_eval(token))
        except (SyntaxError, ValueError) as exc:
            raise ValueError(
                f"Unable to decode C string literal: {token}"
            ) from exc

    joined = "".join(decoded)

    # Remove accidental spaces or tabs immediately before line breaks.
    # Preserve the original line structure for translation and visual QA.
    return "\n".join(
        line.rstrip(" \t")
        for line in joined.split("\n")
    )


def source_line(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def extract_move_names(
    text: str,
) -> list[dict[str, object]]:
    pattern = re.compile(
        r"^[ \t]*"
        r"\[(?P<move_id>MOVE_[A-Z0-9_]+)\]"
        r"\s*=\s*"
        r"_\(\s*"
        r"(?P<strings>(?:\"(?:\\.|[^\"\\])*\"\s*)+)"
        r"\)\s*,",
        re.MULTILINE | re.DOTALL,
    )

    rows: list[dict[str, object]] = []

    for match in pattern.finditer(text):
        rows.append(
            {
                "move_id": match.group("move_id"),
                "move_name_en": decode_c_strings(
                    match.group("strings")
                ),
                "source_line": source_line(
                    text,
                    match.start(),
                ),
            }
        )

    return rows


def extract_description_definitions(
    text: str,
) -> list[dict[str, object]]:
    pattern = re.compile(
        r"static\s+const\s+u8\s+"
        r"(?P<symbol>s[A-Za-z0-9_]+Description)"
        r"\[\]\s*=\s*"
        r"_\(\s*"
        r"(?P<strings>(?:\"(?:\\.|[^\"\\])*\"\s*)+)"
        r"\s*\);",
        re.MULTILINE | re.DOTALL,
    )

    rows: list[dict[str, object]] = []

    for match in pattern.finditer(text):
        rows.append(
            {
                "description_symbol": match.group("symbol"),
                "source_text": decode_c_strings(
                    match.group("strings")
                ),
                "source_line": source_line(
                    text,
                    match.start(),
                ),
            }
        )

    return rows


def extract_description_mappings(
    text: str,
) -> list[dict[str, object]]:
    pattern = re.compile(
        r"^[ \t]*"
        r"\[\s*"
        r"(?P<move_id>MOVE_[A-Z0-9_]+)"
        r"\s*-\s*1\s*\]"
        r"\s*=\s*"
        r"(?P<symbol>s[A-Za-z0-9_]+Description)"
        r"\s*,",
        re.MULTILINE,
    )

    rows: list[dict[str, object]] = []

    for match in pattern.finditer(text):
        rows.append(
            {
                "move_id": match.group("move_id"),
                "description_symbol": match.group("symbol"),
                "source_line": source_line(
                    text,
                    match.start(),
                ),
            }
        )

    return rows


def duplicate_values(values: list[str]) -> list[str]:
    return sorted(
        value
        for value, count in Counter(values).items()
        if count > 1
    )


def write_csv_atomic(
    path: Path,
    fieldnames: list[str],
    rows: list[dict[str, object]],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    temporary_path = path.with_suffix(path.suffix + ".tmp")

    try:
        with temporary_path.open(
            "w",
            encoding="utf-8-sig",
            newline="",
        ) as csv_file:
            writer = csv.DictWriter(
                csv_file,
                fieldnames=fieldnames,
            )
            writer.writeheader()
            writer.writerows(rows)

        temporary_path.replace(path)

    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def main() -> int:
    for required_file in [
        MOVE_NAMES_FILE,
        MOVE_DESCRIPTIONS_FILE,
    ]:
        if not required_file.is_file():
            print(
                f"ERROR: Missing source file: {required_file}",
                file=sys.stderr,
            )
            return 1

    if OUTPUT_FILE.exists():
        print(
            "ERROR: Output file already exists. "
            "Refusing to overwrite possible translation work:",
            file=sys.stderr,
        )
        print(f"  {OUTPUT_FILE}", file=sys.stderr)
        return 1

    names_text = MOVE_NAMES_FILE.read_text(
        encoding="utf-8"
    )
    descriptions_text = MOVE_DESCRIPTIONS_FILE.read_text(
        encoding="utf-8"
    )

    names = extract_move_names(names_text)
    definitions = extract_description_definitions(
        descriptions_text
    )
    mappings = extract_description_mappings(
        descriptions_text
    )

    name_ids = [
        str(row["move_id"])
        for row in names
    ]
    definition_symbols = [
        str(row["description_symbol"])
        for row in definitions
    ]
    mapped_move_ids = [
        str(row["move_id"])
        for row in mappings
    ]
    mapped_symbols = [
        str(row["description_symbol"])
        for row in mappings
    ]

    duplicate_name_ids = duplicate_values(name_ids)
    duplicate_definitions = duplicate_values(
        definition_symbols
    )
    duplicate_mapped_moves = duplicate_values(
        mapped_move_ids
    )
    duplicate_mapped_symbols = duplicate_values(
        mapped_symbols
    )

    names_by_id = {
        str(row["move_id"]): row
        for row in names
    }
    definitions_by_symbol = {
        str(row["description_symbol"]): row
        for row in definitions
    }

    expected_mapped_moves = set(names_by_id) - {
        "MOVE_NONE"
    }
    actual_mapped_moves = set(mapped_move_ids)

    missing_move_mappings = sorted(
        expected_mapped_moves - actual_mapped_moves
    )
    unexpected_move_mappings = sorted(
        actual_mapped_moves - expected_mapped_moves
    )

    unknown_description_symbols = sorted(
        set(mapped_symbols) - set(definitions_by_symbol)
    )
    unused_description_symbols = sorted(
        set(definitions_by_symbol) - set(mapped_symbols)
    )

    errors: list[str] = []

    if len(names) != 355:
        errors.append(
            f"Expected 355 move names, found {len(names)}"
        )

    if len(definitions) != 355:
        errors.append(
            "Expected 355 description definitions, "
            f"found {len(definitions)}"
        )

    if len(mappings) != 354:
        errors.append(
            "Expected 354 description mappings, "
            f"found {len(mappings)}"
        )

    if duplicate_name_ids:
        errors.append(
            f"Duplicate move names: {duplicate_name_ids}"
        )

    if duplicate_definitions:
        errors.append(
            "Duplicate description definitions: "
            f"{duplicate_definitions}"
        )

    if duplicate_mapped_moves:
        errors.append(
            "Duplicate mapped move IDs: "
            f"{duplicate_mapped_moves}"
        )

    if duplicate_mapped_symbols:
        errors.append(
            "Description symbols mapped more than once: "
            f"{duplicate_mapped_symbols}"
        )

    if missing_move_mappings:
        errors.append(
            "Moves without description mappings: "
            f"{missing_move_mappings}"
        )

    if unexpected_move_mappings:
        errors.append(
            "Unexpected mapped move IDs: "
            f"{unexpected_move_mappings}"
        )

    if unknown_description_symbols:
        errors.append(
            "Mapped symbols without definitions: "
            f"{unknown_description_symbols}"
        )

    if unused_description_symbols != [
        "sNullDescription"
    ]:
        errors.append(
            "Unexpected unused description definitions: "
            f"{unused_description_symbols}"
        )

    if "MOVE_NONE" not in names_by_id:
        errors.append("MOVE_NONE was not found.")
    elif names_by_id["MOVE_NONE"]["move_name_en"] != "-":
        errors.append(
            "MOVE_NONE must keep the original name '-'."
        )

    if "MOVE_NONE" in actual_mapped_moves:
        errors.append(
            "MOVE_NONE must not have a description mapping."
        )

    if "sNullDescription" not in definitions_by_symbol:
        errors.append(
            "sNullDescription definition was not found."
        )

    empty_move_names = sorted(
        move_id
        for move_id, row in names_by_id.items()
        if not str(row["move_name_en"])
    )

    if empty_move_names:
        errors.append(
            f"Empty move names: {empty_move_names}"
        )

    empty_descriptions = sorted(
        symbol
        for symbol, row in definitions_by_symbol.items()
        if (
            symbol != "sNullDescription"
            and not str(row["source_text"])
        )
    )

    if empty_descriptions:
        errors.append(
            "Empty move descriptions: "
            f"{empty_descriptions}"
        )

    print("=== MOVE DESCRIPTION SOURCE AUDIT ===")
    print(f"Move names              : {len(names)}")
    print(f"Description definitions : {len(definitions)}")
    print(f"Description mappings    : {len(mappings)}")
    print(
        f"Duplicate move names    : "
        f"{len(duplicate_name_ids)}"
    )
    print(
        f"Duplicate mapped moves  : "
        f"{len(duplicate_mapped_moves)}"
    )
    print(
        f"Duplicate mapped symbols: "
        f"{len(duplicate_mapped_symbols)}"
    )
    print(
        f"Unknown symbols         : "
        f"{len(unknown_description_symbols)}"
    )
    print(
        f"Unused definitions      : "
        f"{unused_description_symbols}"
    )
    print(f"Validation errors       : {len(errors)}")

    if errors:
        print()
        print("ERRORS:")

        for error in errors:
            print(f"- {error}")

        return 1

    output_rows: list[dict[str, object]] = []

    for mapping in mappings:
        move_id = str(mapping["move_id"])
        symbol = str(mapping["description_symbol"])

        name = names_by_id[move_id]
        definition = definitions_by_symbol[symbol]

        output_rows.append(
            {
                "move_id": move_id,
                "move_name_en": name["move_name_en"],
                "name_status": "keep_english",
                "description_symbol": symbol,
                "source_text": definition["source_text"],
                "target_text_th": "",
                "description_status": "pending",
                "move_name_source_file": (
                    MOVE_NAMES_FILE
                    .relative_to(ROOT)
                    .as_posix()
                ),
                "move_name_source_line": (
                    name["source_line"]
                ),
                "description_source_file": (
                    MOVE_DESCRIPTIONS_FILE
                    .relative_to(ROOT)
                    .as_posix()
                ),
                "description_source_line": (
                    definition["source_line"]
                ),
                "mapping_source_line": (
                    mapping["source_line"]
                ),
            }
        )

    write_csv_atomic(
        OUTPUT_FILE,
        [
            "move_id",
            "move_name_en",
            "name_status",
            "description_symbol",
            "source_text",
            "target_text_th",
            "description_status",
            "move_name_source_file",
            "move_name_source_line",
            "description_source_file",
            "description_source_line",
            "mapping_source_line",
        ],
        output_rows,
    )

    print()
    print(f"Inventory rows          : {len(output_rows)}")
    print(
        "Name policy             : "
        "keep_english"
    )
    print(
        "Description status      : "
        "pending"
    )
    print(
        "Created                 : "
        f"{OUTPUT_FILE.relative_to(ROOT)}"
    )
    print()
    print(
        "PASS: Move description inventory "
        "created successfully."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
