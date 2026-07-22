#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

MOVE_NAMES = ROOT / "src/data/text/move_names.h"
MOVE_CONSTANTS = ROOT / "include/constants/moves.h"
THAI_MAP = ROOT / "tools/thai/font/thai_precompose_glyph_map.json"

OUTPUT_DIR = ROOT / "tools/thai/generated/move_names"
CSV_OUTPUT = OUTPUT_DIR / "move_names_inventory.csv"
JSON_OUTPUT = OUTPUT_DIR / "move_names_inventory.json"
REPORT_OUTPUT = OUTPUT_DIR / "move_names_inventory_report.md"

MOVE_NAME_LENGTH = 12
FIXED_SLOT_BYTES = MOVE_NAME_LENGTH + 1
THAI_COMMAND_BYTES = 8

THAI_RE = re.compile(r"[\u0E00-\u0E7F]+")

SEED_TRANSLATIONS = {
    "MOVE_TACKLE": {
        "thai_name": "พุ่งชน",
        "translation_style": "meaning_based",
        "review_status": "draft",
        "notes": "ตัวอย่างคำแปลจากชื่ออังกฤษ",
    },
    "MOVE_EMBER": {
        "thai_name": "สะเก็ดไฟ",
        "translation_style": "meaning_based",
        "review_status": "draft",
        "notes": "ตัวอย่างคำแปลจากชื่ออังกฤษ",
    },
    "MOVE_THUNDERBOLT": {
        "thai_name": "แสนโวลต์",
        "translation_style": "familiar_name",
        "review_status": "draft",
        "notes": "ชื่อที่แฟนโปเกมอนไทยคุ้นเคย ต้องตรวจแหล่งอ้างอิงภายหลัง",
    },
}


def fail(message: str) -> None:
    raise SystemExit(f"ERROR: {message}")


def load_move_ids() -> dict[str, int]:
    source = MOVE_CONSTANTS.read_text(encoding="utf-8")

    move_ids = {
        constant: int(number)
        for constant, number in re.findall(
            r"^\s*#define\s+(MOVE_[A-Z0-9_]+)\s+(\d+)\b",
            source,
            flags=re.MULTILINE,
        )
    }

    if not move_ids:
        fail("อ่าน Move ID จาก include/constants/moves.h ไม่สำเร็จ")

    return move_ids


def load_thai_map() -> tuple[dict[str, dict], int]:
    data = json.loads(
        THAI_MAP.read_text(encoding="utf-8")
    )

    glyphs = data.get("glyphs")

    if not isinstance(glyphs, list):
        fail("Thai map ไม่มีรายการ glyphs")

    lookup = {}

    for entry in glyphs:
        if not isinstance(entry, dict):
            continue

        name = entry.get("name")

        if isinstance(name, str) and name:
            lookup[name] = entry

    if not lookup:
        fail("Thai map ไม่มี Glyph ที่ใช้งานได้")

    return lookup, max(len(name) for name in lookup)


def tokenize_thai(
    text: str,
    lookup: dict[str, dict],
    max_length: int,
) -> list[str]:
    tokens = []
    position = 0

    while position < len(text):
        matched = None
        upper = min(len(text), position + max_length)

        for end in range(upper, position, -1):
            candidate = text[position:end]

            if candidate in lookup:
                matched = candidate
                break

        if matched is None:
            character = text[position]

            fail(
                f"Thai map ไม่รองรับ {text!r} "
                f"ตรง {character!r} "
                f"U+{ord(character):04X}"
            )

        tokens.append(matched)
        position += len(matched)

    return tokens


def calculate_thai_metrics(
    text: str,
    lookup: dict[str, dict],
    max_length: int,
) -> tuple[int, int]:
    if not text:
        return 0, 0

    cluster_count = 0
    encoded_bytes = 0
    cursor = 0

    for match in THAI_RE.finditer(text):
        # ตัวอักษรที่ไม่ใช่ไทย เช่น Space
        encoded_bytes += match.start() - cursor

        tokens = tokenize_thai(
            match.group(0),
            lookup,
            max_length,
        )

        cluster_count += len(tokens)
        encoded_bytes += len(tokens) * THAI_COMMAND_BYTES
        cursor = match.end()

    encoded_bytes += len(text) - cursor

    # เพิ่ม EOS อีก 1 ไบต์
    return cluster_count, encoded_bytes + 1


def main() -> int:
    for path in (
        MOVE_NAMES,
        MOVE_CONSTANTS,
        THAI_MAP,
    ):
        if not path.is_file():
            fail(f"ไม่พบไฟล์ {path.relative_to(ROOT)}")

    move_ids = load_move_ids()
    thai_lookup, max_cluster_length = load_thai_map()

    source = MOVE_NAMES.read_text(encoding="utf-8")

    pattern = re.compile(
        r'\[\s*(MOVE_[A-Z0-9_]+)\s*\]\s*='
        r'\s*_\("((?:\\.|[^"\\])*)"\)'
    )

    rows = []

    for match in pattern.finditer(source):
        move_constant, english_name = match.groups()

        move_id = move_ids.get(move_constant)

        if move_id is None:
            fail(f"ไม่พบ Move ID ของ {move_constant}")

        source_line = (
            source.count("\n", 0, match.start()) + 1
        )

        seed = SEED_TRANSLATIONS.get(
            move_constant,
            {},
        )

        thai_name = seed.get("thai_name", "")

        cluster_count, encoded_bytes = (
            calculate_thai_metrics(
                thai_name,
                thai_lookup,
                max_cluster_length,
            )
        )

        if thai_name:
            fits_slot = (
                "YES"
                if encoded_bytes <= FIXED_SLOT_BYTES
                else "NO"
            )
        else:
            fits_slot = ""

        rows.append(
            {
                "move_id": move_id,
                "move_constant": move_constant,
                "english_name": english_name,
                "english_length": len(english_name),
                "english_storage_bytes": (
                    len(english_name) + 1
                ),
                "source_file": str(
                    MOVE_NAMES.relative_to(ROOT)
                ),
                "source_line": source_line,
                "japanese_name": "",
                "thai_name": thai_name,
                "thai_cluster_count": (
                    cluster_count if thai_name else ""
                ),
                "thai_encoded_bytes": (
                    encoded_bytes if thai_name else ""
                ),
                "fixed_slot_bytes": FIXED_SLOT_BYTES,
                "fits_current_fixed_slot": fits_slot,
                "translation_style": seed.get(
                    "translation_style",
                    "",
                ),
                "review_status": seed.get(
                    "review_status",
                    "untranslated",
                ),
                "notes": seed.get("notes", ""),
            }
        )

    rows.sort(key=lambda item: item["move_id"])

    if len(rows) != 355:
        fail(
            f"คาดว่า 355 Move entries "
            f"แต่พบ {len(rows)}"
        )

    if len({row["move_id"] for row in rows}) != len(rows):
        fail("พบ Move ID ซ้ำ")

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    fieldnames = list(rows[0].keys())

    with CSV_OUTPUT.open(
        "w",
        encoding="utf-8-sig",
        newline="",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
        )
        writer.writeheader()
        writer.writerows(rows)

    JSON_OUTPUT.write_text(
        json.dumps(
            {
                "format": (
                    "pokemon-gen3-thai-"
                    "move-inventory-v1"
                ),
                "move_count": len(rows),
                "move_name_length": MOVE_NAME_LENGTH,
                "fixed_slot_bytes": (
                    FIXED_SLOT_BYTES
                ),
                "thai_command_bytes_per_cluster": (
                    THAI_COMMAND_BYTES
                ),
                "rows": rows,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    seeded_rows = [
        row for row in rows
        if row["thai_name"]
    ]

    fitting_rows = [
        row for row in seeded_rows
        if row["fits_current_fixed_slot"] == "YES"
    ]

    report = [
        "# Move Name Inventory Report",
        "",
        f"- Move entries: **{len(rows)}**",
        (
            "- Current fixed slot: "
            f"**{FIXED_SLOT_BYTES} bytes including EOS**"
        ),
        (
            "- Thai positioned command: "
            f"**{THAI_COMMAND_BYTES} bytes per cluster**"
        ),
        (
            "- Seeded Thai examples: "
            f"**{len(seeded_rows)}**"
        ),
        (
            "- Seeded examples fitting current slot: "
            f"**{len(fitting_rows)}/{len(seeded_rows)}**"
        ),
        "",
        "## Seeded examples",
        "",
        (
            "| Constant | English | Thai draft | "
            "Clusters | Encoded bytes | Fits slot |"
        ),
        "|---|---|---|---:|---:|---|",
    ]

    for row in seeded_rows:
        report.append(
            f"| `{row['move_constant']}` "
            f"| `{row['english_name']}` "
            f"| `{row['thai_name']}` "
            f"| {row['thai_cluster_count']} "
            f"| {row['thai_encoded_bytes']} "
            f"| {row['fits_current_fixed_slot']} |"
        )

    report.extend(
        [
            "",
            "## Conclusion",
            "",
            (
                "The current fixed-width "
                "`gMoveNames[][13]` layout cannot hold "
                "ordinary Thai precompose names."
            ),
            (
                "The move-name storage architecture must "
                "be changed before production Thai names "
                "are inserted."
            ),
        ]
    )

    REPORT_OUTPUT.write_text(
        "\n".join(report) + "\n",
        encoding="utf-8",
    )

    print("========================================")
    print("MOVE NAME INVENTORY")
    print("========================================")
    print(f"Move entries      : {len(rows)}")
    print(
        f"Fixed slot        : "
        f"{FIXED_SLOT_BYTES} bytes"
    )
    print(
        f"Seeded Thai names : "
        f"{len(seeded_rows)}"
    )
    print(
        f"Fit current slot  : "
        f"{len(fitting_rows)}/{len(seeded_rows)}"
    )
    print()

    for row in seeded_rows:
        print(
            f"{row['move_constant']:<22} "
            f"{row['english_name']:<12} -> "
            f"{row['thai_name']:<12} "
            f"clusters={row['thai_cluster_count']} "
            f"bytes={row['thai_encoded_bytes']} "
            f"fit={row['fits_current_fixed_slot']}"
        )

    print()
    print(
        f"CSV    : "
        f"{CSV_OUTPUT.relative_to(ROOT)}"
    )
    print(
        f"JSON   : "
        f"{JSON_OUTPUT.relative_to(ROOT)}"
    )
    print(
        f"Report : "
        f"{REPORT_OUTPUT.relative_to(ROOT)}"
    )
    print("RESULT: MOVE NAME INVENTORY PASSED")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
