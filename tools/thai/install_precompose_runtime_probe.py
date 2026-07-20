#!/usr/bin/env python3
"""
Install, inspect, or restore the 11x12 precomposed "เริ่มเกมส์" runtime probe.

This probe changes only:
  1. graphics/fonts/thai_shaped.png
  2. src/strings.c

It deliberately does NOT change:
  - charmap.txt
  - graphics/fonts/latin_normal.png
  - tools/thai/font/thai_shaped_glyph_map.json
  - the production shaper or renderer

Usage from the repository root:
  python3 tools/thai/install_precompose_runtime_probe.py install
  python3 tools/thai/install_precompose_runtime_probe.py status
  python3 tools/thai/install_precompose_runtime_probe.py restore
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image


WORD = "เริ่มเกมส์"
CMD_BEGIN = 0xFC
CMD_THAI_POSITIONED = 0x19
X_OFFSET = 0
Y_OFFSET = -12
CLUSTER_START_FLAG = 1

SCRIPT_PATH = Path(__file__).resolve()
ROOT = SCRIPT_PATH.parents[2]

PROBE_DIR = ROOT / "tools/thai/generated/precompose_probe"
PROBE_ATLAS = PROBE_DIR / "precompose_start_game_atlas.png"
PROBE_MAP = PROBE_DIR / "precompose_start_game_map.json"

TARGET_ATLAS = ROOT / "graphics/fonts/thai_shaped.png"
STRINGS_SOURCE = ROOT / "src/strings.c"

STATE_DIR = ROOT / "tools/thai/generated/precompose_runtime_probe"
BACKUP_DIR = STATE_DIR / "backup"
MANIFEST_PATH = STATE_DIR / "manifest.json"
COMMAND_REPORT = STATE_DIR / "positioned_command_report.txt"

BACKUP_ATLAS = BACKUP_DIR / "thai_shaped.png"
BACKUP_STRINGS = BACKUP_DIR / "strings.c"

MENU_PATTERN = re.compile(
    r'const u8 gText_MainMenuNewGame\[\]\s*=\s*_\(".*?"\);',
    re.DOTALL,
)


def fail(message: str) -> "NoReturn":
    raise SystemExit(f"ERROR: {message}")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def git_value(*args: str) -> str:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=ROOT,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
    except Exception:
        return "unknown"
    return result.stdout.strip() or "unknown"


def require_repository() -> None:
    if not (ROOT / ".git").exists():
        fail(f"ไม่พบ Git repository ที่ {ROOT}")

    for path in (PROBE_ATLAS, PROBE_MAP, TARGET_ATLAS, STRINGS_SOURCE):
        if not path.is_file():
            fail(f"ไม่พบไฟล์ที่จำเป็น: {path.relative_to(ROOT)}")


def load_probe_map() -> dict[str, Any]:
    try:
        data = json.loads(PROBE_MAP.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"อ่าน Probe map ไม่สำเร็จ: {exc}")

    if data.get("format") != "pokemon-gen3-thai-precompose-probe-v1":
        fail(f"Probe map format ไม่ถูกต้อง: {data.get('format')!r}")
    if data.get("word") != WORD:
        fail(f"Probe map word ต้องเป็น {WORD!r}")
    if data.get("destination_cell") != [16, 16]:
        fail("Probe atlas ปลายทางต้องเป็นเซลล์ 16x16")

    clusters = data.get("clusters")
    indices = data.get("encoded_atlas_indices")
    glyphs = data.get("glyphs")

    if not isinstance(clusters, list) or not clusters:
        fail("Probe map ไม่มี clusters")
    if not isinstance(indices, list) or len(indices) != len(clusters):
        fail("encoded_atlas_indices ไม่ตรงกับ clusters")
    if not isinstance(glyphs, list) or not glyphs:
        fail("Probe map ไม่มี glyph entries")

    return data


def validate_probe_atlas() -> None:
    with Image.open(PROBE_ATLAS) as opened:
        image = opened.copy()

    if image.mode != "P":
        fail(f"Probe atlas ต้องเป็น indexed PNG mode P แต่พบ {image.mode}")
    if image.size != (256, 16):
        fail(f"Probe atlas ต้องมีขนาด 256x16 แต่พบ {image.size}")

    pixels = image.get_flattened_data() if hasattr(image, "get_flattened_data") else image.getdata()
    used = set(pixels)
    if used - {0, 1, 2}:
        fail(f"Probe atlas มี Palette index นอก 0/1/2: {sorted(used)}")


def build_commands(data: dict[str, Any]) -> tuple[list[int], str, list[dict[str, Any]]]:
    glyph_by_name = {
        entry["name"]: entry
        for entry in data["glyphs"]
        if isinstance(entry, dict) and isinstance(entry.get("name"), str)
    }

    output: list[int] = []
    rows: list[dict[str, Any]] = []

    for cluster, atlas_index in zip(
        data["clusters"],
        data["encoded_atlas_indices"],
    ):
        entry = glyph_by_name.get(cluster)
        if entry is None:
            fail(f"ไม่พบ Glyph entry สำหรับ Cluster {cluster!r}")

        advance = entry.get("source_advance")
        if not isinstance(atlas_index, int) or not 0 <= atlas_index <= 0xFFFF:
            fail(f"Atlas index ของ {cluster!r} ไม่ถูกต้อง: {atlas_index!r}")
        if not isinstance(advance, int) or not 0 <= advance <= 255:
            fail(f"Advance ของ {cluster!r} ไม่ถูกต้อง: {advance!r}")

        command = [
            CMD_BEGIN,
            CMD_THAI_POSITIONED,
            atlas_index & 0xFF,
            (atlas_index >> 8) & 0xFF,
            X_OFFSET & 0xFF,
            Y_OFFSET & 0xFF,
            advance,
            CLUSTER_START_FLAG,
        ]
        output.extend(command)
        rows.append(
            {
                "cluster": cluster,
                "atlas_index": atlas_index,
                "advance": advance,
                "bytes": command,
            }
        )

    brace_text = "".join(f"{{{value}}}" for value in output)
    return output, brace_text, rows


def replacement_line(brace_text: str) -> str:
    return (
        'const u8 gText_MainMenuNewGame[] = '
        f'_("{brace_text}");'
    )


def read_menu_declaration() -> str:
    source = STRINGS_SOURCE.read_text(encoding="utf-8")
    matches = MENU_PATTERN.findall(source)
    if len(matches) != 1:
        fail(
            "ต้องพบ gText_MainMenuNewGame เพียง 1 จุด "
            f"แต่พบ {len(matches)} จุด"
        )
    return matches[0]


def rewrite_menu(new_declaration: str) -> None:
    source = STRINGS_SOURCE.read_text(encoding="utf-8")
    updated, count = MENU_PATTERN.subn(new_declaration, source, count=1)
    if count != 1:
        fail("แก้ gText_MainMenuNewGame ไม่สำเร็จ")

    temporary = STRINGS_SOURCE.with_suffix(".c.precompose_probe_tmp")
    temporary.write_text(updated, encoding="utf-8")
    temporary.replace(STRINGS_SOURCE)


def load_manifest() -> dict[str, Any] | None:
    if not MANIFEST_PATH.exists():
        return None
    try:
        return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"Manifest เสียหรืออ่านไม่ได้: {exc}")


def write_manifest(data: dict[str, Any]) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def create_initial_backup() -> dict[str, Any]:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    if BACKUP_ATLAS.exists() or BACKUP_STRINGS.exists():
        fail(
            "พบ Backup บางส่วนแต่ไม่มี Manifest ที่สมบูรณ์ "
            f"กรุณาหยุดและตรวจ {BACKUP_DIR.relative_to(ROOT)}"
        )

    shutil.copy2(TARGET_ATLAS, BACKUP_ATLAS)
    shutil.copy2(STRINGS_SOURCE, BACKUP_STRINGS)

    manifest = {
        "format": "pokemon-gen3-thai-precompose-runtime-probe-v1",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "branch": git_value("branch", "--show-current"),
        "head": git_value("rev-parse", "HEAD"),
        "installed": False,
        "backup": {
            "atlas_path": str(BACKUP_ATLAS.relative_to(ROOT)),
            "atlas_sha256": sha256(BACKUP_ATLAS),
            "strings_path": str(BACKUP_STRINGS.relative_to(ROOT)),
            "strings_sha256": sha256(BACKUP_STRINGS),
        },
        "probe": {
            "atlas_path": str(PROBE_ATLAS.relative_to(ROOT)),
            "atlas_sha256": sha256(PROBE_ATLAS),
            "map_path": str(PROBE_MAP.relative_to(ROOT)),
            "map_sha256": sha256(PROBE_MAP),
        },
    }
    write_manifest(manifest)
    return manifest


def ensure_backup() -> dict[str, Any]:
    manifest = load_manifest()
    if manifest is None:
        return create_initial_backup()

    if manifest.get("format") != "pokemon-gen3-thai-precompose-runtime-probe-v1":
        fail("Manifest format ไม่ถูกต้อง")

    for path in (BACKUP_ATLAS, BACKUP_STRINGS):
        if not path.is_file():
            fail(f"Backup หาย: {path.relative_to(ROOT)}")

    backup = manifest.get("backup", {})
    if sha256(BACKUP_ATLAS) != backup.get("atlas_sha256"):
        fail("SHA-256 ของ Backup thai_shaped.png ไม่ตรงกับ Manifest")
    if sha256(BACKUP_STRINGS) != backup.get("strings_sha256"):
        fail("SHA-256 ของ Backup strings.c ไม่ตรงกับ Manifest")

    return manifest


def write_command_report(
    data: dict[str, Any],
    rows: list[dict[str, Any]],
    declaration: str,
) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    lines = [
        "THAI PRECOMPOSE RUNTIME PROBE",
        "==============================",
        f"Word          : {WORD}",
        f"Clusters      : {' | '.join(data['clusters'])}",
        f"Atlas indices : {', '.join(map(str, data['encoded_atlas_indices']))}",
        f"Total advance : {data.get('total_advance')}",
        f"X offset      : {X_OFFSET}",
        f"Y offset      : {Y_OFFSET}",
        "",
        "COMMANDS",
        "--------",
    ]

    for row in rows:
        lines.append(
            f"{row['cluster']}: atlas={row['atlas_index']} "
            f"advance={row['advance']} "
            + " ".join(f"{value:02X}" for value in row["bytes"])
        )

    lines.extend(
        [
            "",
            "SOURCE DECLARATION",
            "------------------",
            declaration,
        ]
    )
    COMMAND_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def status() -> int:
    require_repository()
    data = load_probe_map()
    validate_probe_atlas()
    _raw, brace_text, _rows = build_commands(data)
    expected_declaration = replacement_line(brace_text)

    manifest = load_manifest()
    atlas_installed = sha256(TARGET_ATLAS) == sha256(PROBE_ATLAS)
    menu_installed = read_menu_declaration() == expected_declaration

    print("========================================")
    print("PRECOMPOSE RUNTIME PROBE STATUS")
    print("========================================")
    print(f"Repository      : {ROOT}")
    print(f"Branch          : {git_value('branch', '--show-current')}")
    print(f"HEAD            : {git_value('rev-parse', '--short', 'HEAD')}")
    print(f"Manifest        : {'FOUND' if manifest else 'NOT FOUND'}")
    print(f"Atlas installed : {'YES' if atlas_installed else 'NO'}")
    print(f"Menu installed  : {'YES' if menu_installed else 'NO'}")
    print(f"Current menu    : {read_menu_declaration()}")
    print()
    if atlas_installed and menu_installed:
        print("STATUS: INSTALLED")
        return 0
    if not atlas_installed and not menu_installed:
        print("STATUS: NOT INSTALLED / RESTORED")
        return 0

    print("STATUS: PARTIAL STATE — ห้าม Build จนกว่าจะตรวจหรือ Restore")
    return 2


def install() -> int:
    require_repository()
    data = load_probe_map()
    validate_probe_atlas()
    _raw, brace_text, rows = build_commands(data)
    declaration = replacement_line(brace_text)

    manifest = ensure_backup()

    atlas_installed = sha256(TARGET_ATLAS) == sha256(PROBE_ATLAS)
    menu_installed = read_menu_declaration() == declaration
    if atlas_installed and menu_installed:
        print("Runtime probe ติดตั้งอยู่แล้ว ไม่มีการแก้ไฟล์เพิ่ม")
        return status()

    if manifest.get("installed"):
        fail(
            "Manifest ระบุว่าติดตั้งอยู่ แต่ไฟล์ปัจจุบันไม่ตรงครบ "
            "กรุณารัน status และ restore ก่อน"
        )

    # A restored state must still match the original backup before reinstalling.
    if sha256(TARGET_ATLAS) != manifest["backup"]["atlas_sha256"]:
        fail(
            "thai_shaped.png ปัจจุบันไม่ตรงกับ Backup เดิม "
            "จึงไม่ติดตั้งทับงานที่อาจแก้เพิ่มภายหลัง"
        )
    if sha256(STRINGS_SOURCE) != manifest["backup"]["strings_sha256"]:
        fail(
            "src/strings.c ปัจจุบันไม่ตรงกับ Backup เดิม "
            "จึงไม่ติดตั้งทับงานที่อาจแก้เพิ่มภายหลัง"
        )

    shutil.copy2(PROBE_ATLAS, TARGET_ATLAS)
    rewrite_menu(declaration)
    write_command_report(data, rows, declaration)

    manifest["installed"] = True
    manifest["installed_at_utc"] = datetime.now(timezone.utc).isoformat()
    manifest["installed_files"] = {
        "atlas_sha256": sha256(TARGET_ATLAS),
        "strings_sha256": sha256(STRINGS_SOURCE),
        "menu_declaration": declaration,
    }
    write_manifest(manifest)

    print("========================================")
    print("PRECOMPOSE RUNTIME PROBE INSTALLED")
    print("========================================")
    print(f"Atlas          : {TARGET_ATLAS.relative_to(ROOT)}")
    print(f"Menu source    : {STRINGS_SOURCE.relative_to(ROOT)}")
    print(f"Backup         : {BACKUP_DIR.relative_to(ROOT)}")
    print(f"Command report : {COMMAND_REPORT.relative_to(ROOT)}")
    print(f"Clusters       : {' | '.join(data['clusters'])}")
    print(f"Atlas indices  : {', '.join(map(str, data['encoded_atlas_indices']))}")
    print(f"Total advance  : {data.get('total_advance')}")
    print()
    print("NEXT:")
    print("  rm -f build/assets/graphics/fonts/thai_shaped.png.latfont")
    print('  make -j"$(nproc)"')
    return 0


def restore() -> int:
    require_repository()
    manifest = ensure_backup()

    shutil.copy2(BACKUP_ATLAS, TARGET_ATLAS)
    shutil.copy2(BACKUP_STRINGS, STRINGS_SOURCE)

    if sha256(TARGET_ATLAS) != manifest["backup"]["atlas_sha256"]:
        fail("Restore thai_shaped.png แล้ว SHA-256 ไม่ตรง")
    if sha256(STRINGS_SOURCE) != manifest["backup"]["strings_sha256"]:
        fail("Restore strings.c แล้ว SHA-256 ไม่ตรง")

    manifest["installed"] = False
    manifest["restored_at_utc"] = datetime.now(timezone.utc).isoformat()
    write_manifest(manifest)

    print("========================================")
    print("PRECOMPOSE RUNTIME PROBE RESTORED")
    print("========================================")
    print("คืนไฟล์เดิมสำเร็จ:")
    print(f"  {TARGET_ATLAS.relative_to(ROOT)}")
    print(f"  {STRINGS_SOURCE.relative_to(ROOT)}")
    print()
    print("เมื่อต้องการ Build สถานะเดิม:")
    print("  rm -f build/assets/graphics/fonts/thai_shaped.png.latfont")
    print('  make -j"$(nproc)"')
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "action",
        choices=("install", "status", "restore"),
    )
    args = parser.parse_args()

    if args.action == "install":
        return install()
    if args.action == "status":
        return status()
    return restore()


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("\nCancelled. ไม่มีการดำเนินการต่อ", file=sys.stderr)
        raise SystemExit(130)
