#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

PRODUCTION_CHECKPOINT = "770548dfe"
BATCH1_AREAS = {"MAIN_MENU", "OPTION_MENU", "START_SAVE"}

SCOPE = [
    {
        "order": 1,
        "area": "MAIN_MENU",
        "display_th": "หน้าหลักและเริ่มเกม",
        "priority": "P1",
        "files": ["src/main_menu.c", "src/title_screen.c", "src/naming_screen.c"],
        "qa_route": "เปิดเกมใหม่ ตรวจ Main Menu, Continue/New Game/Option, เลือกเพศและตั้งชื่อ",
    },
    {
        "order": 2,
        "area": "OPTION_MENU",
        "display_th": "เมนูตัวเลือก",
        "priority": "P1",
        "files": ["src/option_menu.c"],
        "qa_route": "เปิด OPTION และตรวจทุกค่า รวมข้อความชิดขวา",
    },
    {
        "order": 3,
        "area": "START_SAVE",
        "display_th": "Start Menu และระบบบันทึก",
        "priority": "P1",
        "files": ["src/start_menu.c", "src/save.c", "data/text/save.inc"],
        "qa_route": "เปิด Start Menu ตรวจทุกคำสั่ง แล้วทดสอบ Save/Overwrite/Success/Error",
    },
    {
        "order": 4,
        "area": "PARTY_MENU",
        "display_th": "Party Menu",
        "priority": "P1",
        "files": ["src/party_menu.c", "src/data/party_menu.h"],
        "qa_route": "เปิด Party ตรวจ Summary/Switch/Item/Field Move/Prompt",
    },
    {
        "order": 5,
        "area": "SUMMARY",
        "display_th": "Pokémon Summary",
        "priority": "P1",
        "files": ["src/pokemon_summary_screen.c"],
        "qa_route": "ตรวจทุกแท็บ ชื่อโปเกมอน ชื่อท่า PP ค่าสถานะและข้อความชิดขวา",
    },
    {
        "order": 6,
        "area": "MOVE_UI",
        "display_th": "หน้าจอเรียนและลืมท่า",
        "priority": "P1",
        "files": ["src/move_relearner.c"],
        "qa_route": "ตรวจ Move Relearner/Learn/Forget และรายละเอียดท่า",
    },
    {
        "order": 7,
        "area": "BAG",
        "display_th": "Bag และการใช้ไอเทม",
        "priority": "P1",
        "files": ["src/item_menu.c", "src/item_use.c"],
        "qa_route": "ตรวจทุก Pocket, Context Menu, จำนวน, ราคา และ Prompt",
    },
    {
        "order": 8,
        "area": "BATTLE_UI",
        "display_th": "Battle UI",
        "priority": "P1",
        "files": [
            "src/battle_interface.c",
            "src/battle_controller_player.c",
            "src/battle_controller_safari.c",
        ],
        "qa_route": "ตรวจ Fight/Bag/Pokémon/Run, Move Selection, PP/Type และ Safari Battle",
    },
    {
        "order": 9,
        "area": "SHOP",
        "display_th": "ร้านค้า",
        "priority": "P2",
        "files": ["src/shop.c", "data/text/mart_clerk.inc"],
        "qa_route": "ตรวจ Buy/Sell/Quit, ราคา, จำนวน, เงินไม่พอและ Bag เต็ม",
    },
    {
        "order": 10,
        "area": "PC_STORAGE",
        "display_th": "PC และ Pokémon Storage",
        "priority": "P2",
        "files": [
            "src/player_pc.c",
            "src/pokemon_storage_system.c",
            "data/text/pc.inc",
            "data/text/pc_transfer.inc",
        ],
        "qa_route": "ตรวจ PC, Withdraw/Deposit/Move/Release/Box และข้อความยืนยัน",
    },
    {
        "order": 11,
        "area": "POKEDEX",
        "display_th": "Pokédex",
        "priority": "P2",
        "files": [
            "src/pokedex.c",
            "src/pokedex_area_screen.c",
            "src/pokedex_cry_screen.c",
            "src/pokedex_area_region_map.c",
        ],
        "qa_route": "ตรวจ Seen/Owned/Search/Area/Size/รายการและปุ่มช่วยเหลือ",
    },
    {
        "order": 12,
        "area": "POKENAV",
        "display_th": "PokéNav",
        "priority": "P2",
        "files": [
            "src/pokenav.c",
            "src/pokenav_main_menu.c",
            "src/pokenav_menu_handler.c",
            "src/pokenav_conditions.c",
            "src/pokenav_conditions_search_results.c",
            "src/pokenav_match_call_list.c",
            "src/pokenav_match_call_gfx.c",
            "src/pokenav_region_map.c",
            "src/pokenav_ribbons_list.c",
            "src/pokenav_ribbons_summary.c",
        ],
        "qa_route": "ตรวจ Main Menu, Map, Condition, Match Call, Ribbons และปุ่มช่วยเหลือ",
    },
]

C_DEF_START = re.compile(
    r"(?m)^(?:static\s+)?const\s+u8\s+(?P<symbol>[A-Za-z0-9_]+)\[\]\s*=\s*_\("
)
STRING_TOKEN = re.compile(r'"(?:\\.|[^"\\])*"')
G_TEXT = re.compile(r"\b(gText_[A-Za-z0-9_]+)\b")
CONTROL_CODE = re.compile(r"\{[^{}]+\}|\\p|\\l")
FUNCTION_SIGNATURE = re.compile(
    r"(?m)^(?:static\s+)?(?:[A-Za-z_][A-Za-z0-9_\s\*]+?)\s+"
    r"(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*\([^;{}]*\)\s*$"
)
SIMPLE_DEFINE = re.compile(
    r"(?m)^#define\s+(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s+(?P<value>(?:0x[0-9A-Fa-f]+|\d+))\s*$"
)
THAI_CHAR = re.compile(r"[\u0E00-\u0E7F]")
LATIN_LETTER = re.compile(r"[A-Za-z]")


@dataclass(frozen=True)
class Definition:
    symbol: str
    text: str
    raw_literal: str
    source_file: str
    source_line: int
    kind: str


def decode_literal_body(body: str, *, strip_asm_terminator: bool = False) -> str:
    output: list[str] = []

    for token in STRING_TOKEN.findall(body):
        value = token[1:-1]
        index = 0

        while index < len(value):
            char = value[index]

            if char != "\\":
                output.append(char)
                index += 1
                continue

            if index + 1 >= len(value):
                output.append("\\")
                index += 1
                continue

            escaped = value[index + 1]

            if escaped == "n":
                output.append("\n")
            elif escaped == "t":
                output.append("\t")
            elif escaped == "r":
                output.append("\r")
            elif escaped == '"':
                output.append('"')
            elif escaped == "'":
                output.append("'")
            elif escaped == "\\":
                output.append("\\")
            elif escaped == "x" and index + 3 < len(value):
                try:
                    output.append(chr(int(value[index + 2:index + 4], 16)))
                    index += 2
                except ValueError:
                    output.append("\\x")
            else:
                output.append("\\" + escaped)

            index += 2

    decoded = "".join(output)
    if strip_asm_terminator and decoded.endswith("$"):
        decoded = decoded[:-1]
    return decoded


def parse_c_definitions(path: Path, relative: str) -> list[Definition]:
    text = path.read_text(encoding="utf-8", errors="replace")
    definitions: list[Definition] = []

    for match in C_DEF_START.finditer(text):
        position = match.end()
        index = position
        depth = 1
        state = "code"
        end = None

        while index < len(text):
            char = text[index]

            if state == "code":
                if char == '"':
                    state = "string"
                elif char == "(":
                    depth += 1
                elif char == ")":
                    depth -= 1
                    if depth == 0:
                        end = index
                        break
            else:
                if char == "\\":
                    index += 1
                elif char == '"':
                    state = "code"

            index += 1

        if end is None:
            continue

        body = text[position:end]
        definitions.append(
            Definition(
                symbol=match.group("symbol"),
                text=decode_literal_body(body),
                raw_literal=body.strip(),
                source_file=relative,
                source_line=text.count("\n", 0, match.start()) + 1,
                kind="c_u8",
            )
        )

    return definitions


def parse_asm_definitions(path: Path, relative: str) -> list[Definition]:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    definitions: list[Definition] = []
    index = 0

    while index < len(lines):
        label_match = re.match(r"^(gText_[A-Za-z0-9_]+)::\s*$", lines[index])

        if label_match is None:
            index += 1
            continue

        symbol = label_match.group(1)
        start_line = index + 1
        raw_parts: list[str] = []
        index += 1

        while index < len(lines):
            if re.match(r"^[A-Za-z_][A-Za-z0-9_]*::\s*$", lines[index]):
                break

            string_match = re.match(r"^\s*\.string\s+(.+?)\s*$", lines[index])
            if string_match is not None:
                raw_parts.append(string_match.group(1))

            index += 1

        if raw_parts:
            raw = " ".join(raw_parts)
            definitions.append(
                Definition(
                    symbol=symbol,
                    text=decode_literal_body(raw, strip_asm_terminator=True),
                    raw_literal=raw,
                    source_file=relative,
                    source_line=start_line,
                    kind="asm_string",
                )
            )

    return definitions


def global_definition_index(root: Path) -> tuple[dict[str, Definition], list[dict[str, str]]]:
    index: dict[str, Definition] = {}
    duplicates: list[dict[str, str]] = []
    candidates: list[Path] = []

    for base in (root / "src", root / "data"):
        if not base.is_dir():
            continue
        candidates.extend(base.rglob("*.c"))
        candidates.extend(base.rglob("*.h"))
        candidates.extend(base.rglob("*.inc"))

    for path in sorted(set(candidates)):
        relative = path.relative_to(root).as_posix()
        definitions = parse_c_definitions(path, relative)
        if path.suffix == ".inc":
            definitions.extend(parse_asm_definitions(path, relative))

        for definition in definitions:
            if not definition.symbol.startswith("gText_"):
                continue
            if definition.symbol in index:
                previous = index[definition.symbol]
                duplicates.append(
                    {
                        "symbol": definition.symbol,
                        "first_file": previous.source_file,
                        "first_line": str(previous.source_line),
                        "duplicate_file": definition.source_file,
                        "duplicate_line": str(definition.source_line),
                    }
                )
                continue
            index[definition.symbol] = definition

    return index, duplicates


def function_for_lines(text: str) -> dict[int, str]:
    lines = text.splitlines()
    result: dict[int, str] = {}
    current = "GLOBAL"
    pending = ""
    brace_depth = 0

    for number, line in enumerate(lines, start=1):
        if brace_depth == 0:
            signature = FUNCTION_SIGNATURE.match(line)
            if signature is not None:
                pending = signature.group("name")
            if pending and "{" in line:
                current = pending
                pending = ""

        result[number] = current
        brace_depth += line.count("{") - line.count("}")

        if brace_depth <= 0:
            brace_depth = 0
            current = "GLOBAL"

        if line.strip().endswith(";") and brace_depth == 0:
            pending = ""

    return result


def classify_context(line: str) -> str:
    if "AddTextPrinter" in line or "PrintText" in line:
        return "direct_text_printer"
    if "GetStringRightAlignXOffset" in line:
        return "right_aligned"
    if "GetStringCenterAlignXOffset" in line:
        return "center_aligned"
    if "StringExpandPlaceholders" in line:
        return "placeholder_expansion"
    if "ShowSaveMessage" in line or "ShowFieldMessage" in line:
        return "message_window"
    if "msgbox" in line or re.search(r"\bmessage\b", line):
        return "script_message"
    if "MenuAction" in line or re.search(r"\{\s*(?:gText_|s[A-Za-z0-9_]+)", line):
        return "menu_action_or_table"
    return "symbol_reference"


def scope_class(definition: Definition | None, text: str) -> str:
    if definition is None:
        return "unresolved"

    file_lower = definition.source_file.lower()
    visible = CONTROL_CODE.sub("", text).strip()

    if file_lower.endswith("data/text/birch_speech.inc"):
        return "story_deferred"

    if not visible or not (THAI_CHAR.search(visible) or LATIN_LETTER.search(visible)):
        return "technical_not_translatable"

    if "\\p" in text or "{PAUSE" in text or len(visible) > 160:
        return "system_message"

    if "\n" in text or visible.endswith(("?", ".", "!", "…")):
        return "core_ui_prompt"

    return "core_ui_label"


def current_language(text: str) -> str:
    visible = CONTROL_CODE.sub("", text)
    has_thai = THAI_CHAR.search(visible) is not None
    has_latin = LATIN_LETTER.search(visible) is not None

    if has_thai and has_latin:
        return "mixed"
    if has_thai:
        return "thai"
    if has_latin:
        return "english"
    return "nonlinguistic"


def translation_status(text: str, classification: str) -> str:
    language = current_language(text)

    if classification == "technical_not_translatable":
        return "not_applicable"
    if classification == "story_deferred":
        return "deferred_story"
    if language in {"thai", "mixed"}:
        return "existing_thai_review"
    return "pending"


def parse_window_templates(root: Path, scoped_files: dict[str, list[str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    declaration = re.compile(
        r"static\s+const\s+struct\s+WindowTemplate\s+"
        r"(?P<symbol>[A-Za-z0-9_]+)(?P<array>\[\])?\s*=\s*\{"
    )

    for area, files in scoped_files.items():
        for relative in files:
            path = root / relative
            if not path.is_file() or path.suffix != ".c":
                continue

            text = path.read_text(encoding="utf-8", errors="replace")
            defines = {
                match.group("name"): int(match.group("value"), 0)
                for match in SIMPLE_DEFINE.finditer(text)
            }

            for match in declaration.finditer(text):
                symbol = match.group("symbol")
                is_array = bool(match.group("array"))
                outer_start = text.find("{", match.start())
                depth = 0
                index = outer_start
                state = "code"
                outer_end = None

                while index < len(text):
                    char = text[index]
                    if state == "code":
                        if char == '"':
                            state = "string"
                        elif char == "{":
                            depth += 1
                        elif char == "}":
                            depth -= 1
                            if depth == 0:
                                outer_end = index + 1
                                break
                    else:
                        if char == "\\":
                            index += 1
                        elif char == '"':
                            state = "code"
                    index += 1

                if outer_end is None:
                    continue

                body = text[outer_start + 1:outer_end - 1]
                entries: list[tuple[str, str, int]] = []

                if not is_array:
                    entries.append(("single", body, text.count("\n", 0, match.start()) + 1))
                else:
                    local_depth = 0
                    entry_start = None
                    entry_index = 0
                    state = "code"
                    offset = 0
                    while offset < len(body):
                        char = body[offset]
                        if state == "code":
                            if char == '"':
                                state = "string"
                            elif char == "{":
                                if local_depth == 0:
                                    entry_start = offset
                                local_depth += 1
                            elif char == "}":
                                local_depth -= 1
                                if local_depth == 0 and entry_start is not None:
                                    entry_text = body[entry_start + 1:offset]
                                    prefix = body[max(0, entry_start - 80):entry_start]
                                    label_match = re.search(r"\[([^\]]+)\]\s*=\s*$", prefix)
                                    label = label_match.group(1) if label_match else str(entry_index)
                                    line = text.count("\n", 0, outer_start + 1 + entry_start) + 1
                                    entries.append((label, entry_text, line))
                                    entry_index += 1
                                    entry_start = None
                        else:
                            if char == "\\":
                                offset += 1
                            elif char == '"':
                                state = "code"
                        offset += 1

                for entry_label, entry_text, line in entries:
                    fields: dict[str, str] = {}
                    for field in (
                        "bg", "tilemapLeft", "tilemapTop", "width",
                        "height", "paletteNum", "baseBlock"
                    ):
                        field_match = re.search(
                            rf"\.{field}\s*=\s*([^,\n}}]+)", entry_text
                        )
                        fields[field] = field_match.group(1).strip() if field_match else ""

                    if not fields["width"] and not fields["height"]:
                        continue

                    def resolve(expr: str) -> str:
                        if not expr:
                            return ""
                        if expr in defines:
                            return str(defines[expr])
                        try:
                            return str(int(expr, 0))
                        except ValueError:
                            return ""

                    width_tiles = resolve(fields["width"])
                    height_tiles = resolve(fields["height"])
                    outer_px = str(int(width_tiles) * 8) if width_tiles else ""

                    rows.append(
                        {
                            "ui_area": area,
                            "source_file": relative,
                            "source_line": str(line),
                            "template_symbol": symbol,
                            "entry": entry_label,
                            "bg_expr": fields["bg"],
                            "tilemap_left_expr": fields["tilemapLeft"],
                            "tilemap_top_expr": fields["tilemapTop"],
                            "width_expr": fields["width"],
                            "height_expr": fields["height"],
                            "width_tiles_resolved": width_tiles,
                            "height_tiles_resolved": height_tiles,
                            "outer_width_px": outer_px,
                            "palette_expr": fields["paletteNum"],
                            "base_block_expr": fields["baseBlock"],
                            "constraint_status": "outer_window_only_pending_text_padding_mapping",
                        }
                    )

    return rows


def csv_safe_cell(value: object) -> object:
    # Preserve meaningful line-ending spaces without physical CSV whitespace.
    if not isinstance(value, str):
        return value

    safe_lines: list[str] = []

    for line in value.split("\n"):
        body = line.rstrip(" \t")
        suffix = line[len(body):]
        safe_lines.append(
            body
            + suffix.replace(" ", r"\x20").replace("\t", r"\t")
        )

    return "\n".join(safe_lines)


def write_csv(path: Path, fields: list[str], rows: Iterable[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fields,
            lineterminator="\n",
            extrasaction="ignore",
        )
        writer.writeheader()
        writer.writerows(
            {
                field: csv_safe_cell(row.get(field, ""))
                for field in fields
            }
            for row in rows
        )

def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--output-root", type=Path, default=None)
    args = parser.parse_args()

    root = args.root.resolve()
    output_root = (args.output_root or root).resolve()

    if not (root / "src/strings.c").is_file():
        raise RuntimeError(f"Missing source root: {root}")

    scoped_files = {entry["area"]: entry["files"] for entry in SCOPE}
    missing_scope = [
        relative
        for entry in SCOPE
        for relative in entry["files"]
        if not (root / relative).is_file()
    ]
    if missing_scope:
        raise RuntimeError(f"Missing scoped UI files: {missing_scope}")

    global_defs, duplicate_globals = global_definition_index(root)
    entry_defs: dict[str, Definition] = {}
    entry_areas: dict[str, set[str]] = defaultdict(set)
    entry_usage_count: Counter[str] = Counter()
    usage_rows: list[dict[str, str]] = []

    for entry in SCOPE:
        area = entry["area"]
        for relative in entry["files"]:
            path = root / relative
            text = path.read_text(encoding="utf-8", errors="replace")
            lines = text.splitlines()
            functions = function_for_lines(text)
            local_defs = {
                definition.symbol: definition
                for definition in parse_c_definitions(path, relative)
                if not definition.symbol.startswith("gText_")
            }

            for symbol, definition in local_defs.items():
                key = f"local:{relative}:{symbol}"
                entry_defs[key] = definition
                entry_areas[key].add(area)

            local_patterns = {
                symbol: re.compile(rf"\b{re.escape(symbol)}\b")
                for symbol in local_defs
            }

            for line_number, line in enumerate(lines, start=1):
                if re.match(r"^\s*gText_[A-Za-z0-9_]+::", line):
                    continue

                for symbol in G_TEXT.findall(line):
                    key = f"global:{symbol}"
                    if key not in entry_defs and symbol in global_defs:
                        entry_defs[key] = global_defs[symbol]
                    entry_areas[key].add(area)
                    entry_usage_count[key] += 1
                    font_match = re.search(r"\b(FONT_[A-Z0-9_]+)\b", line)
                    alignment = (
                        "right" if "GetStringRightAlignXOffset" in line
                        else "center" if "GetStringCenterAlignXOffset" in line
                        else "left_or_dynamic"
                    )
                    usage_rows.append(
                        {
                            "ui_key": key,
                            "symbol": symbol,
                            "ui_area": area,
                            "usage_file": relative,
                            "usage_line": str(line_number),
                            "function_or_scope": functions.get(line_number, "GLOBAL"),
                            "context_kind": classify_context(line),
                            "font_direct": font_match.group(1) if font_match else "",
                            "alignment_direct": alignment,
                            "window_and_position_status": "direct_line_only_pending_call_flow_mapping",
                            "source_context": line.strip(),
                            "usage_status": "active_reference",
                        }
                    )

                if C_DEF_START.match(line):
                    continue

                for symbol, pattern in local_patterns.items():
                    if pattern.search(line) is None:
                        continue
                    key = f"local:{relative}:{symbol}"
                    entry_usage_count[key] += 1
                    font_match = re.search(r"\b(FONT_[A-Z0-9_]+)\b", line)
                    alignment = (
                        "right" if "GetStringRightAlignXOffset" in line
                        else "center" if "GetStringCenterAlignXOffset" in line
                        else "left_or_dynamic"
                    )
                    usage_rows.append(
                        {
                            "ui_key": key,
                            "symbol": symbol,
                            "ui_area": area,
                            "usage_file": relative,
                            "usage_line": str(line_number),
                            "function_or_scope": functions.get(line_number, "GLOBAL"),
                            "context_kind": classify_context(line),
                            "font_direct": font_match.group(1) if font_match else "",
                            "alignment_direct": alignment,
                            "window_and_position_status": "direct_line_only_pending_call_flow_mapping",
                            "source_context": line.strip(),
                            "usage_status": "active_reference",
                        }
                    )

    all_keys = sorted(entry_areas)
    string_rows: list[dict[str, str]] = []
    unresolved_rows: list[dict[str, str]] = []

    for ui_id, key in enumerate(all_keys, start=1):
        definition = entry_defs.get(key)
        symbol = key.split(":")[-1]
        text = definition.text if definition else ""
        classification = scope_class(definition, text)
        areas = sorted(entry_areas[key])
        controls = sorted(set(CONTROL_CODE.findall(text)))
        language = current_language(text)
        status = translation_status(text, classification)

        if definition is None:
            unresolved_rows.append(
                {
                    "ui_key": key,
                    "symbol": symbol,
                    "ui_areas": ";".join(areas),
                    "usage_count": str(entry_usage_count[key]),
                    "reason": "definition_not_found_in_archived_source",
                }
            )

        string_rows.append(
            {
                "ui_id": f"UI{ui_id:04d}",
                "ui_key": key,
                "symbol": symbol,
                "current_text": text,
                "target_text_th": text if language in {"thai", "mixed"} else "",
                "translation_status": status,
                "scope_class": classification,
                "current_language": language,
                "ui_areas": ";".join(areas),
                "usage_count": str(entry_usage_count[key]),
                "definition_kind": definition.kind if definition else "unresolved",
                "source_file": definition.source_file if definition else "",
                "source_line": str(definition.source_line) if definition else "",
                "line_count": str(text.count("\n") + 1 if text else 0),
                "control_codes": ";".join(controls),
                "has_placeholders": "yes" if controls else "no",
                "width_constraint_status": "pending_usage_to_window_mapping",
                "visual_qa_status": "pending",
                "translator_note": "",
            }
        )

    usage_rows.sort(
        key=lambda row: (
            row["ui_area"], row["usage_file"], int(row["usage_line"]), row["ui_key"]
        )
    )
    windows = parse_window_templates(root, scoped_files)
    windows.sort(key=lambda row: (row["ui_area"], row["source_file"], int(row["source_line"])))

    inventory_dir = output_root / "tools/thai/translation/inventory"
    report_dir = output_root / "tools/thai/translation/reports/core_ui_inventory"
    tool_path = output_root / "tools/thai/extract_core_ui_inventory.py"

    string_fields = [
        "ui_id", "ui_key", "symbol", "current_text", "target_text_th",
        "translation_status", "scope_class", "current_language",
        "ui_areas", "usage_count", "definition_kind", "source_file",
        "source_line", "line_count", "control_codes", "has_placeholders",
        "width_constraint_status", "visual_qa_status", "translator_note",
    ]
    usage_fields = [
        "ui_key", "symbol", "ui_area", "usage_file", "usage_line",
        "function_or_scope", "context_kind", "font_direct",
        "alignment_direct", "window_and_position_status", "source_context",
        "usage_status",
    ]
    scope_fields = [
        "phase_order", "ui_area", "display_name_th", "priority",
        "source_files", "qa_route", "inventory_status",
    ]
    window_fields = [
        "ui_area", "source_file", "source_line", "template_symbol", "entry",
        "bg_expr", "tilemap_left_expr", "tilemap_top_expr", "width_expr",
        "height_expr", "width_tiles_resolved", "height_tiles_resolved",
        "outer_width_px", "palette_expr", "base_block_expr",
        "constraint_status",
    ]

    write_csv(inventory_dir / "ui_text_strings.csv", string_fields, string_rows)
    write_csv(inventory_dir / "ui_text_usage.csv", usage_fields, usage_rows)
    write_csv(
        inventory_dir / "ui_screen_scope.csv",
        scope_fields,
        [
            {
                "phase_order": str(entry["order"]),
                "ui_area": entry["area"],
                "display_name_th": entry["display_th"],
                "priority": entry["priority"],
                "source_files": ";".join(entry["files"]),
                "qa_route": entry["qa_route"],
                "inventory_status": "inventory_ready",
            }
            for entry in SCOPE
        ],
    )
    write_csv(report_dir / "ui_window_templates.csv", window_fields, windows)
    write_csv(
        report_dir / "unresolved_ui_text_references.csv",
        ["ui_key", "symbol", "ui_areas", "usage_count", "reason"],
        unresolved_rows,
    )
    write_csv(
        report_dir / "duplicate_global_ui_text_definitions.csv",
        ["symbol", "first_file", "first_line", "duplicate_file", "duplicate_line"],
        duplicate_globals,
    )

    existing_thai = [row for row in string_rows if row["translation_status"] == "existing_thai_review"]
    write_csv(report_dir / "existing_thai_ui_review.csv", string_fields, existing_thai)

    batch1_rows = []
    for row in string_rows:
        areas = set(filter(None, row["ui_areas"].split(";")))
        if not (areas & BATCH1_AREAS):
            continue
        if row["scope_class"] in {"story_deferred", "technical_not_translatable", "unresolved"}:
            continue
        batch = dict(row)
        batch["batch_status"] = "ready_for_constraint_mapping"
        batch1_rows.append(batch)

    batch1_fields = string_fields + ["batch_status"]
    write_csv(report_dir / "batch1_main_option_start_strings.csv", batch1_fields, batch1_rows)

    batch1_keys = {row["ui_key"] for row in batch1_rows}
    batch1_usage = [row for row in usage_rows if row["ui_key"] in batch1_keys]
    write_csv(report_dir / "batch1_main_option_start_usage.csv", usage_fields, batch1_usage)
    batch1_windows = [row for row in windows if row["ui_area"] in BATCH1_AREAS]
    write_csv(report_dir / "batch1_main_option_start_windows.csv", window_fields, batch1_windows)

    by_area = Counter()
    for row in string_rows:
        for area in filter(None, row["ui_areas"].split(";")):
            by_area[area] += 1
    by_class = Counter(row["scope_class"] for row in string_rows)
    by_status = Counter(row["translation_status"] for row in string_rows)
    by_language = Counter(row["current_language"] for row in string_rows)

    readme = [
        "# Phase 5 — Core UI Inventory",
        "",
        f"Generated from production checkpoint `{PRODUCTION_CHECKPOINT}`.",
        "",
        "## Coverage",
        "",
        f"- UI areas: {len(SCOPE)}",
        f"- Unique UI text entries: {len(string_rows)}",
        f"- Usage references: {len(usage_rows)}",
        f"- Window-template entries: {len(windows)}",
        f"- Unresolved text definitions: {len(unresolved_rows)}",
        f"- Duplicate global definitions: {len(duplicate_globals)}",
        f"- Batch 1 entries (Main/Option/Start-Save): {len(batch1_rows)}",
        "",
        "## Translation status",
        "",
    ]
    readme.extend(f"- `{key}`: {value}" for key, value in sorted(by_status.items()))
    readme.extend(["", "## Scope classes", ""])
    readme.extend(f"- `{key}`: {value}" for key, value in sorted(by_class.items()))
    readme.extend(["", "## Current language", ""])
    readme.extend(f"- `{key}`: {value}" for key, value in sorted(by_language.items()))
    readme.extend(["", "## Entries by UI area", ""])
    readme.extend(f"- `{key}`: {value}" for key, value in sorted(by_area.items()))
    readme.extend(
        [
            "",
            "## Important limitations",
            "",
            "- Battle system narration is intentionally excluded from this Core UI inventory; it belongs to Phase 6 system and variable messages.",
            "- Window widths are outer window sizes only. They are not safe translation limits until text padding, cursor space, icons, alignment, and dynamic values are mapped per printer call.",
            "- Batch 1 is inventory-ready, not translation-ready. The next step is to map exact width/render constraints for Main Menu, Option Menu, and Start/Save before changing source text.",
            "",
            "## Existing Thai entry",
            "",
            "`gText_MainMenuNewGame` currently contains `เริ่มเกมส์` and is marked `existing_thai_review`; it should be reviewed against the project spelling policy before reuse.",
        ]
    )
    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "README.md").write_text("\n".join(readme) + "\n", encoding="utf-8")

    tool_path.parent.mkdir(parents=True, exist_ok=True)
    tool_path.write_bytes(Path(__file__).read_bytes())

    tracked_outputs = [
        tool_path,
        inventory_dir / "ui_text_strings.csv",
        inventory_dir / "ui_text_usage.csv",
        inventory_dir / "ui_screen_scope.csv",
        report_dir / "ui_window_templates.csv",
        report_dir / "unresolved_ui_text_references.csv",
        report_dir / "duplicate_global_ui_text_definitions.csv",
        report_dir / "existing_thai_ui_review.csv",
        report_dir / "batch1_main_option_start_strings.csv",
        report_dir / "batch1_main_option_start_usage.csv",
        report_dir / "batch1_main_option_start_windows.csv",
        report_dir / "README.md",
    ]

    sums = "".join(
        f"{file_sha256(path)}  {path.relative_to(output_root).as_posix()}\n"
        for path in tracked_outputs
    )
    (report_dir / "SHA256SUMS").write_text(sums, encoding="utf-8", newline="\n")

    print("=== CORE UI INVENTORY RESULT ===")
    print(f"UI areas               : {len(SCOPE)}")
    print(f"Unique UI entries      : {len(string_rows)}")
    print(f"Usage references       : {len(usage_rows)}")
    print(f"Window entries         : {len(windows)}")
    print(f"Pending translations   : {by_status.get('pending', 0)}")
    print(f"Existing Thai review   : {by_status.get('existing_thai_review', 0)}")
    print(f"Story deferred         : {by_status.get('deferred_story', 0)}")
    print(f"Not applicable         : {by_status.get('not_applicable', 0)}")
    print(f"Unresolved definitions : {len(unresolved_rows)}")
    print(f"Batch 1 entries        : {len(batch1_rows)}")
    print(f"Output root            : {output_root}")
    print("PASS: Core UI inventory generated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
