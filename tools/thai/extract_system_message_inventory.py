from __future__ import annotations

import argparse
import csv
import dataclasses
import importlib.util
import os
import re
import sys
from collections import defaultdict
from pathlib import Path


UI_FIELDS = [
    "ui_id",
    "ui_key",
    "symbol",
    "current_text",
    "target_text_th",
    "translation_status",
    "scope_class",
    "current_language",
    "ui_areas",
    "usage_count",
    "definition_kind",
    "source_file",
    "source_line",
    "line_count",
    "control_codes",
    "has_placeholders",
    "width_constraint_status",
    "visual_qa_status",
    "translator_note",
]

USAGE_FIELDS = [
    "ui_key",
    "symbol",
    "ui_area",
    "usage_file",
    "usage_line",
    "function_or_scope",
    "context_kind",
    "font_direct",
    "alignment_direct",
    "window_and_position_status",
    "source_context",
    "usage_status",
]

HANDLERS = [
    "STRINGID_INTROMSG",
    "STRINGID_INTROSENDOUT",
    "STRINGID_RETURNMON",
    "STRINGID_SWITCHINMON",
    "STRINGID_USEDMOVE",
    "STRINGID_BATTLEEND",
]

HELPERS = [
    "sText_SpaceIs",
    "sText_ApostropheS",
    "sText_ExclamationMark",
    "sText_ExclamationMark2",
    "sText_ExclamationMark3",
    "sText_ExclamationMark4",
    "sText_ExclamationMark5",
]

EXPECTED = {
    "canonical_table": 369,
    "canonical_outside_core": 365,
    "canonical_core_overlap": 4,
    "dynamic_direct": 49,
    "dynamic_outside_canonical": 46,
    "dynamic_canonical_overlap": 3,
    "helpers": 7,
    "inline": 18,
    "total": 436,
}

POINTER_ENTRY = re.compile(
    r"^\s*\[\s*(STRINGID_[A-Za-z0-9_]+)\s*-\s*"
    r"BATTLESTRINGS_TABLE_START\s*\]\s*=\s*"
    r"([A-Za-z_][A-Za-z0-9_]*)\s*,"
)
STRING_PTR = re.compile(
    r"\bstringPtr\s*=\s*([A-Za-z_][A-Za-z0-9_]*)\s*;"
)
INLINE_STRING = re.compile(
    r'_\(\s*(?P<body>(?:"(?:\\.|[^"\\])*"\s*)+)\)', re.S
)
PLACEHOLDER = re.compile(
    r"\{(?:B_|STR_VAR_|PLAYER|RIVAL|PKMN|POKEMON|MOVE|ITEM|TRAINER|"
    r"ABILITY|TYPE|STAT|DYNAMIC|STRING)"
)


def stop(message: str) -> None:
    raise SystemExit(f"STOP: {message}")


def require_equal(label: str, actual: int, expected: int) -> None:
    if actual != expected:
        stop(f"{label}: expected {expected}, found {actual}")


def unique_in_order(values):
    seen = set()
    result = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result


def load_core_extractor(root: Path):
    path = root / "tools/thai/extract_core_ui_inventory.py"
    spec = importlib.util.spec_from_file_location("core_ui_extractor", path)
    if spec is None or spec.loader is None:
        stop(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def definition_values(definition) -> dict[str, object]:
    if dataclasses.is_dataclass(definition):
        values = dataclasses.asdict(definition)
    else:
        values = vars(definition)

    required = {
        "symbol",
        "text",
        "raw_literal",
        "source_file",
        "source_line",
        "kind",
    }
    missing = sorted(required - values.keys())
    if missing:
        stop(
            "Definition fields changed; missing "
            + ", ".join(missing)
            + f"; available={sorted(values)}"
        )

    normalized = dict(values)
    normalized["definition_kind"] = str(values["kind"])
    normalized["line_count"] = str(values["text"]).count("\n") + 1
    return normalized


def find_braced_block(lines: list[str], start_index: int) -> tuple[int, int]:
    depth = 0
    saw_open = False
    for index in range(start_index, len(lines)):
        line = lines[index]
        if "{" in line:
            saw_open = True
        if saw_open:
            depth += line.count("{")
            depth -= line.count("}")
            if depth == 0:
                return start_index, index
    stop(f"unterminated braced block at line {start_index + 1}")


def find_named_block(lines: list[str], name: str) -> tuple[int, int]:
    matches = [index for index, line in enumerate(lines) if name in line]
    declaration_matches = [
        index
        for index in matches
        if "=" in lines[index]
        and lines[index].find(name) < lines[index].find("=")
        and not lines[index].lstrip().startswith("//")
    ]
    if len(declaration_matches) != 1:
        stop(
            f"expected one declaration for {name}, "
            f"found {len(declaration_matches)}"
        )
    return find_braced_block(lines, declaration_matches[0])


def handler_blocks(lines: list[str]) -> dict[str, tuple[int, int]]:
    result = {}
    for handler in HANDLERS:
        pattern = re.compile(
            rf"^(?P<indent>\s*)case\s+{re.escape(handler)}\s*:"
        )
        matches = [
            (index, pattern.match(line))
            for index, line in enumerate(lines)
            if pattern.match(line)
        ]
        if len(matches) != 1:
            stop(f"expected one case for {handler}, found {len(matches)}")
        start, match = matches[0]
        indent = len(match.group("indent"))
        end = len(lines)
        for index in range(start + 1, len(lines)):
            stripped = lines[index].lstrip()
            current_indent = len(lines[index]) - len(stripped)
            if current_indent == indent and (
                re.match(r"case\s+STRINGID_[A-Za-z0-9_]+\s*:", stripped)
                or re.match(r"default\s*:", stripped)
            ):
                end = index
                break
        result[handler] = (start, end)
    return result


def key_for(symbol: str, source_file: str) -> str:
    if symbol.startswith("gText_"):
        return f"global:{symbol}"
    return f"local:{source_file}:{symbol}"


def usage_row(
    *,
    ui_key: str,
    symbol: str,
    line_number: int,
    function_or_scope: str,
    context_kind: str,
    source_context: str,
) -> dict[str, str]:
    return {
        "ui_key": ui_key,
        "symbol": symbol,
        "ui_area": "BATTLE_SYSTEM",
        "usage_file": "src/battle_message.c",
        "usage_line": str(line_number),
        "function_or_scope": function_or_scope,
        "context_kind": context_kind,
        "font_direct": "",
        "alignment_direct": "left_or_dynamic",
        "window_and_position_status": "pending_call_flow_mapping",
        "source_context": source_context.strip(),
        "usage_status": "active_reference",
    }


def read_previous(path: Path) -> dict[str, dict[str, str]]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return {row["ui_key"]: row for row in csv.DictReader(handle)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()

    root = args.root.resolve()
    battle_path = root / "src/battle_message.c"
    core_csv = root / "tools/thai/translation/inventory/ui_text_strings.csv"
    output_dir = root / "tools/thai/translation/inventory"
    strings_path = output_dir / "system_message_strings.csv"
    usage_path = output_dir / "system_message_usage.csv"

    core = load_core_extractor(root)
    battle_text = battle_path.read_text(encoding="utf-8")
    lines = battle_text.splitlines()

    with core_csv.open("r", encoding="utf-8-sig", newline="") as handle:
        core_rows = list(csv.DictReader(handle))
    core_symbols = {row["symbol"] for row in core_rows if row["symbol"]}

    battle_definitions = {
        item.symbol: item
        for item in core.parse_c_definitions(
            battle_path, "src/battle_message.c"
        )
    }
    global_definitions, _ = core.global_definition_index(root)

    table_start, table_end = find_named_block(lines, "gBattleStringsTable")
    table_entries = []
    for index in range(table_start, table_end + 1):
        match = POINTER_ENTRY.match(lines[index])
        if match:
            table_entries.append(
                {
                    "string_id": match.group(1),
                    "symbol": match.group(2),
                    "line": index + 1,
                    "context": lines[index],
                }
            )

    canonical_symbols_all = unique_in_order(
        entry["symbol"] for entry in table_entries
    )
    require_equal(
        "canonical table entries",
        len(table_entries),
        EXPECTED["canonical_table"],
    )
    require_equal(
        "canonical unique symbols",
        len(canonical_symbols_all),
        EXPECTED["canonical_table"],
    )

    canonical_core_overlap = set(canonical_symbols_all) & core_symbols
    require_equal(
        "canonical/Core UI overlap",
        len(canonical_core_overlap),
        EXPECTED["canonical_core_overlap"],
    )
    canonical_symbols = [
        symbol
        for symbol in canonical_symbols_all
        if symbol not in core_symbols
    ]
    require_equal(
        "canonical outside Core UI",
        len(canonical_symbols),
        EXPECTED["canonical_outside_core"],
    )

    blocks = handler_blocks(lines)
    dynamic_occurrences = []
    for handler in HANDLERS:
        start, end = blocks[handler]
        for index in range(start, end):
            for match in STRING_PTR.finditer(lines[index]):
                dynamic_occurrences.append(
                    {
                        "handler": handler,
                        "symbol": match.group(1),
                        "line": index + 1,
                        "context": lines[index],
                    }
                )

    dynamic_symbols_all = unique_in_order(
        entry["symbol"] for entry in dynamic_occurrences
    )
    require_equal(
        "dynamic direct unique symbols",
        len(dynamic_symbols_all),
        EXPECTED["dynamic_direct"],
    )
    dynamic_canonical_overlap = (
        set(dynamic_symbols_all) & set(canonical_symbols_all)
    )
    require_equal(
        "dynamic/canonical overlap",
        len(dynamic_canonical_overlap),
        EXPECTED["dynamic_canonical_overlap"],
    )
    dynamic_symbols = [
        symbol
        for symbol in dynamic_symbols_all
        if symbol not in set(canonical_symbols_all)
    ]
    require_equal(
        "dynamic outside canonical",
        len(dynamic_symbols),
        EXPECTED["dynamic_outside_canonical"],
    )
    if set(dynamic_symbols) & core_symbols:
        stop(
            "dynamic outside canonical overlaps Core UI: "
            + ", ".join(sorted(set(dynamic_symbols) & core_symbols))
        )

    helper_symbols = list(HELPERS)
    require_equal("helper symbols", len(helper_symbols), EXPECTED["helpers"])
    helper_overlap = (
        set(helper_symbols)
        & (set(canonical_symbols_all) | set(dynamic_symbols_all) | core_symbols)
    )
    if helper_overlap:
        stop("helper overlap: " + ", ".join(sorted(helper_overlap)))

    inline_start, inline_end = find_named_block(lines, "sATypeMove_Table")
    inline_block = "\n".join(lines[inline_start:inline_end + 1])
    inline_entries = []
    for ordinal, match in enumerate(INLINE_STRING.finditer(inline_block)):
        before = inline_block[:match.start()]
        source_line = inline_start + before.count("\n") + 1
        body = match.group("body")
        inline_entries.append(
            {
                "ordinal": ordinal,
                "symbol": f"sATypeMove_Table[{ordinal}]",
                "text": core.decode_literal_body(body),
                "source_line": source_line,
                "line_count": body.count("\n") + 1,
                "context": lines[source_line - 1],
            }
        )
    require_equal("inline entries", len(inline_entries), EXPECTED["inline"])

    groups = [
        ("canonical_table", canonical_symbols),
        ("dynamic_direct", dynamic_symbols),
        ("usedmove_helper", helper_symbols),
    ]
    ordered_symbols = [symbol for _, symbols in groups for symbol in symbols]
    require_equal("named candidate uniqueness", len(set(ordered_symbols)), 418)
    require_equal(
        "total candidates",
        len(ordered_symbols) + len(inline_entries),
        EXPECTED["total"],
    )

    group_for_symbol = {
        symbol: group for group, symbols in groups for symbol in symbols
    }
    definitions = {}
    for symbol in ordered_symbols:
        definition = battle_definitions.get(symbol) or global_definitions.get(symbol)
        if definition is None:
            stop(f"definition not found for {symbol}")
        definitions[symbol] = definition_values(definition)

    rows = []
    key_by_symbol = {}
    for symbol in ordered_symbols:
        definition = definitions[symbol]
        ui_key = key_for(symbol, str(definition["source_file"]))
        key_by_symbol[symbol] = ui_key
        text = str(definition["text"])
        controls = unique_in_order(core.CONTROL_CODE.findall(text))
        rows.append(
            {
                "ui_key": ui_key,
                "symbol": symbol,
                "current_text": text,
                "target_text_th": "",
                "translation_status": "pending",
                "scope_class": "system_message",
                "current_language": core.current_language(text),
                "ui_areas": "BATTLE_SYSTEM",
                "definition_kind": str(definition["definition_kind"]),
                "source_file": str(definition["source_file"]),
                "source_line": str(definition["source_line"]),
                "line_count": str(definition["line_count"]),
                "control_codes": "; ".join(controls),
                "has_placeholders": "yes" if PLACEHOLDER.search(text) else "no",
                "width_constraint_status": "pending_usage_to_window_mapping",
                "visual_qa_status": "pending",
                "translator_note": f"phase6_group={group_for_symbol[symbol]}",
            }
        )

    for entry in inline_entries:
        text = entry["text"]
        controls = unique_in_order(core.CONTROL_CODE.findall(text))
        rows.append(
            {
                "ui_key": (
                    "inline:src/battle_message.c:sATypeMove_Table:"
                    + str(entry["ordinal"])
                ),
                "symbol": entry["symbol"],
                "current_text": text,
                "target_text_th": "",
                "translation_status": "pending",
                "scope_class": "system_message",
                "current_language": core.current_language(text),
                "ui_areas": "BATTLE_SYSTEM",
                "definition_kind": "inline_c_string",
                "source_file": "src/battle_message.c",
                "source_line": str(entry["source_line"]),
                "line_count": str(entry["line_count"]),
                "control_codes": "; ".join(controls),
                "has_placeholders": "yes" if PLACEHOLDER.search(text) else "no",
                "width_constraint_status": "pending_usage_to_window_mapping",
                "visual_qa_status": "pending",
                "translator_note": "phase6_group=usedmove_inline",
            }
        )

    usage_rows = []
    candidate_keys = {row["ui_key"] for row in rows}

    for entry in table_entries:
        symbol = entry["symbol"]
        if symbol not in key_by_symbol:
            continue
        usage_rows.append(
            usage_row(
                ui_key=key_by_symbol[symbol],
                symbol=symbol,
                line_number=entry["line"],
                function_or_scope="gBattleStringsTable",
                context_kind="pointer_table_entry",
                source_context=entry["context"],
            )
        )

    for entry in dynamic_occurrences:
        symbol = entry["symbol"]
        if symbol not in key_by_symbol:
            continue
        usage_rows.append(
            usage_row(
                ui_key=key_by_symbol[symbol],
                symbol=symbol,
                line_number=entry["line"],
                function_or_scope=entry["handler"],
                context_kind="dynamic_handler_reference",
                source_context=entry["context"],
            )
        )

    for symbol in helper_symbols:
        definition_line = int(definitions[symbol]["source_line"])
        matches = []
        pattern = re.compile(rf"\b{re.escape(symbol)}\b")
        for index, line in enumerate(lines, 1):
            if (
                index != definition_line
                and not line.lstrip().startswith("//")
                and pattern.search(line)
            ):
                matches.append((index, line))
        if not matches:
            stop(f"no active helper reference for {symbol}")
        for line_number, line in matches:
            usage_rows.append(
                usage_row(
                    ui_key=key_by_symbol[symbol],
                    symbol=symbol,
                    line_number=line_number,
                    function_or_scope="ChooseTypeOfMoveUsedString",
                    context_kind="usedmove_helper_reference",
                    source_context=line,
                )
            )

    for entry in inline_entries:
        ui_key = (
            "inline:src/battle_message.c:sATypeMove_Table:"
            + str(entry["ordinal"])
        )
        usage_rows.append(
            usage_row(
                ui_key=ui_key,
                symbol=entry["symbol"],
                line_number=entry["source_line"],
                function_or_scope="sATypeMove_Table",
                context_kind="inline_table_entry",
                source_context=entry["context"],
            )
        )

    usage_by_key = defaultdict(int)
    for usage in usage_rows:
        if usage["ui_key"] not in candidate_keys:
            stop(f"usage has unknown key {usage['ui_key']}")
        usage_by_key[usage["ui_key"]] += 1

    previous = read_previous(strings_path)
    preserve_fields = [
        "target_text_th",
        "translation_status",
        "width_constraint_status",
        "visual_qa_status",
        "translator_note",
    ]
    preserved = 0
    for index, row in enumerate(rows, 1):
        row["ui_id"] = f"SM{index:04d}"
        row["usage_count"] = str(usage_by_key[row["ui_key"]])
        if row["usage_count"] == "0":
            stop(f"candidate has no usage: {row['ui_key']}")
        old = previous.get(row["ui_key"])
        if (
            old
            and old.get("current_text")
            != core.csv_safe_cell(row["current_text"])
        ):
            stop(f"source text changed for existing row {row['ui_key']}")
        if old:
            for field in preserve_fields:
                row[field] = old.get(field, row[field])
            preserved += 1

    if previous and set(previous) != candidate_keys:
        removed = sorted(set(previous) - candidate_keys)
        added = sorted(candidate_keys - set(previous))
        stop(
            "candidate identity drift on regeneration; "
            f"removed={removed[:5]} added={added[:5]}"
        )

    require_equal("final string rows", len(rows), EXPECTED["total"])

    strings_tmp = strings_path.with_suffix(".csv.tmp")
    usage_tmp = usage_path.with_suffix(".csv.tmp")
    core.write_csv(strings_tmp, UI_FIELDS, rows)
    core.write_csv(usage_tmp, USAGE_FIELDS, usage_rows)
    os.replace(strings_tmp, strings_path)
    os.replace(usage_tmp, usage_path)

    print("===== PHASE 6 INVENTORY CREATED =====")
    print(f"canonical table entries: {len(table_entries)}")
    print(f"canonical/Core UI overlap: {len(canonical_core_overlap)}")
    print(f"canonical outside Core UI: {len(canonical_symbols)}")
    print(f"dynamic direct unique: {len(dynamic_symbols_all)}")
    print(f"dynamic/canonical overlap: {len(dynamic_canonical_overlap)}")
    print(f"dynamic outside canonical: {len(dynamic_symbols)}")
    print(f"USEDMOVE helpers: {len(helper_symbols)}")
    print(f"USEDMOVE inline entries: {len(inline_entries)}")
    print(f"system message rows: {len(rows)}")
    print(f"usage rows: {len(usage_rows)}")
    print(f"preserved translated rows: {preserved}")
    print(f"strings sha256: {core.file_sha256(strings_path)}")
    print(f"usage sha256: {core.file_sha256(usage_path)}")


if __name__ == "__main__":
    main()
