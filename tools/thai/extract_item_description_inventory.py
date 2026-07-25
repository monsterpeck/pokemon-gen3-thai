#!/usr/bin/env python3

from __future__ import annotations

import ast
import csv
import re
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

DESCRIPTION_FILE = ROOT / "src/data/text/item_descriptions.h"
ITEM_TABLE_FILE = ROOT / "src/data/items.h"

OUTPUT_DIR = ROOT / "tools/thai/translation/inventory"
STRINGS_OUTPUT = OUTPUT_DIR / "item_description_strings.csv"
USAGE_OUTPUT = OUTPUT_DIR / "item_description_usage.csv"


def decode_c_strings(expression: str) -> str:
    """Decode and concatenate adjacent C-style string literals."""
    tokens = re.findall(r'"(?:\\.|[^"\\])*"', expression)

    if not tokens:
        return ""

    decoded: list[str] = []

    for token in tokens:
        try:
            decoded.append(ast.literal_eval(token))
        except (SyntaxError, ValueError) as exc:
            raise ValueError(f"Unable to decode string literal: {token}") from exc

    joined = "".join(decoded)

    # Normalize accidental spaces and tabs before line breaks.
    # Keep the original line structure for translation and QA.
    return "\n".join(
        line.rstrip(" \t")
        for line in joined.split("\n")
    )


def source_line(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def extract_description_definitions(text: str) -> dict[str, dict[str, object]]:
    pattern = re.compile(
        r"static\s+const\s+u8\s+"
        r"(?P<symbol>s[A-Za-z0-9_]+Desc)\[\]\s*=\s*"
        r"_\(\s*(?P<strings>(?:\"(?:\\.|[^\"\\])*\"\s*)+)\s*\);",
        re.MULTILINE | re.DOTALL,
    )

    definitions: dict[str, dict[str, object]] = {}

    for match in pattern.finditer(text):
        symbol = match.group("symbol")

        if symbol in definitions:
            raise ValueError(f"Duplicate description definition: {symbol}")

        definitions[symbol] = {
            "source_text": decode_c_strings(match.group("strings")),
            "source_line": source_line(text, match.start()),
        }

    return definitions


def extract_item_entries(text: str) -> list[dict[str, object]]:
    block_pattern = re.compile(
        r"^[ \t]*\[(?P<item_id>ITEM_[A-Z0-9_]+)\]\s*=\s*\{"
        r"(?P<body>.*?)"
        r"^[ \t]*\},",
        re.MULTILINE | re.DOTALL,
    )

    name_pattern = re.compile(
        r"\.name\s*=\s*_\(\s*"
        r"(?P<strings>(?:\"(?:\\.|[^\"\\])*\"\s*)+)"
        r"\)",
        re.DOTALL,
    )

    description_pattern = re.compile(
        r"\.description\s*=\s*(?P<symbol>s[A-Za-z0-9_]+Desc)\s*,"
    )

    entries: list[dict[str, object]] = []

    for block_match in block_pattern.finditer(text):
        item_id = block_match.group("item_id")
        body = block_match.group("body")

        name_match = name_pattern.search(body)
        description_match = description_pattern.search(body)

        item_name = ""
        if name_match:
            item_name = decode_c_strings(name_match.group("strings"))

        description_symbol = ""
        if description_match:
            description_symbol = description_match.group("symbol")

        entries.append(
            {
                "item_id": item_id,
                "item_name_en": item_name,
                "description_symbol": description_symbol,
                "source_line": source_line(text, block_match.start()),
            }
        )

    return entries


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8-sig", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    if not DESCRIPTION_FILE.is_file():
        print(f"ERROR: Missing file: {DESCRIPTION_FILE}", file=sys.stderr)
        return 1

    if not ITEM_TABLE_FILE.is_file():
        print(f"ERROR: Missing file: {ITEM_TABLE_FILE}", file=sys.stderr)
        return 1

    description_text = DESCRIPTION_FILE.read_text(encoding="utf-8")
    item_table_text = ITEM_TABLE_FILE.read_text(encoding="utf-8")

    definitions = extract_description_definitions(description_text)
    items = extract_item_entries(item_table_text)

    if not definitions:
        print(
            "ERROR: No item description definitions were parsed.",
            file=sys.stderr,
        )
        return 1

    if not items:
        print(
            "ERROR: No item entries were parsed from src/data/items.h.",
            file=sys.stderr,
        )
        return 1

    duplicate_item_ids = [
        item_id
        for item_id, count in Counter(
            str(item["item_id"]) for item in items
        ).items()
        if count > 1
    ]

    missing_names = [
        str(item["item_id"])
        for item in items
        if not str(item["item_name_en"])
    ]

    missing_mappings = [
        str(item["item_id"])
        for item in items
        if not str(item["description_symbol"])
    ]

    unresolved_symbols = sorted(
        {
            str(item["description_symbol"])
            for item in items
            if str(item["description_symbol"])
            and str(item["description_symbol"]) not in definitions
        }
    )

    if duplicate_item_ids:
        print("ERROR: Duplicate item IDs:", file=sys.stderr)
        for item_id in duplicate_item_ids:
            print(f"  {item_id}", file=sys.stderr)
        return 1

    if missing_names:
        print("ERROR: Item names could not be parsed:", file=sys.stderr)
        for item_id in missing_names:
            print(f"  {item_id}", file=sys.stderr)
        return 1

    if missing_mappings:
        print("ERROR: Description mappings could not be parsed:", file=sys.stderr)
        for item_id in missing_mappings:
            print(f"  {item_id}", file=sys.stderr)
        return 1

    if unresolved_symbols:
        print("ERROR: Description symbols have no definition:", file=sys.stderr)
        for symbol in unresolved_symbols:
            print(f"  {symbol}", file=sys.stderr)
        return 1

    usage_counts = Counter(
        str(item["description_symbol"]) for item in items
    )

    strings_rows: list[dict[str, object]] = []

    for symbol, definition in definitions.items():
        status = "not_applicable" if symbol == "sDummyDesc" else "pending"

        strings_rows.append(
            {
                "description_symbol": symbol,
                "source_text": definition["source_text"],
                "target_text_th": "",
                "status": status,
                "usage_count": usage_counts.get(symbol, 0),
                "source_file": DESCRIPTION_FILE.relative_to(ROOT).as_posix(),
                "source_line": definition["source_line"],
            }
        )

    usage_rows: list[dict[str, object]] = []

    for item in items:
        symbol = str(item["description_symbol"])
        item_id = str(item["item_id"])

        usage_rows.append(
            {
                "item_id": item_id,
                "item_name_en": item["item_name_en"],
                "name_status": (
                    "not_applicable"
                    if item_id == "ITEM_NONE"
                    else "keep_english"
                ),
                "description_symbol": symbol,
                "description_status": (
                    "not_applicable"
                    if symbol == "sDummyDesc"
                    else "pending"
                ),
                "source_file": ITEM_TABLE_FILE.relative_to(ROOT).as_posix(),
                "source_line": item["source_line"],
            }
        )

    write_csv(
        STRINGS_OUTPUT,
        [
            "description_symbol",
            "source_text",
            "target_text_th",
            "status",
            "usage_count",
            "source_file",
            "source_line",
        ],
        strings_rows,
    )

    write_csv(
        USAGE_OUTPUT,
        [
            "item_id",
            "item_name_en",
            "name_status",
            "description_symbol",
            "description_status",
            "source_file",
            "source_line",
        ],
        usage_rows,
    )

    referenced_symbols = set(usage_counts)
    unused_symbols = sorted(set(definitions) - referenced_symbols)
    shared_symbols = sorted(
        symbol for symbol, count in usage_counts.items() if count > 1
    )

    print("=== ITEM DESCRIPTION INVENTORY ===")
    print(f"Description definitions : {len(definitions)}")
    print(f"Item entries            : {len(items)}")
    print(f"Referenced symbols      : {len(referenced_symbols)}")
    print(f"Shared symbols          : {len(shared_symbols)}")
    print(f"Unused definitions      : {len(unused_symbols)}")
    print(f"Unresolved symbols      : {len(unresolved_symbols)}")
    print()
    print(f"Created: {STRINGS_OUTPUT.relative_to(ROOT)}")
    print(f"Created: {USAGE_OUTPUT.relative_to(ROOT)}")

    if unused_symbols:
        print()
        print("Unused description definitions:")
        for symbol in unused_symbols:
            print(f"  {symbol}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
