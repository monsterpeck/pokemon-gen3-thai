#!/usr/bin/env python3
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

ROOT = Path(__file__).resolve().parents[2]
BRANCH = "thai-precompose-full"
CHECKPOINT = "edc1d458b"

FULL_DIR = ROOT / "tools/thai/generated/precompose_full"
FULL_ATLAS = FULL_DIR / "thai_precompose_full.png"
FULL_MAP = FULL_DIR / "thai_precompose_full_map.json"

SHAPER = ROOT / "tools/thai/shape_thai_precompose.py"
ACTIVE_MAP = ROOT / "tools/thai/font/thai_precompose_glyph_map.json"
MAKEFILE = ROOT / "Makefile"
ATLAS = ROOT / "graphics/fonts/thai_shaped.png"
STRINGS = ROOT / "src/strings.c"

STATE = ROOT / "tools/thai/generated/precompose_full_runtime"
BACKUP = STATE / "backup"
MANIFEST = STATE / "manifest.json"

BACKUP_MAKEFILE = BACKUP / "Makefile"
BACKUP_ATLAS = BACKUP / "thai_shaped.png"
BACKUP_STRINGS = BACKUP / "strings.c"
BACKUP_ACTIVE_MAP = BACKUP / "thai_precompose_glyph_map.json"

OLD_SHAPER = (
    "THAI_SHAPER := PYTHONPATH=tools/thai/cache/python:tools/thai "
    "python3 -B tools/thai/shape_thai_production.py"
)
NEW_SHAPER = (
    "THAI_SHAPER := PYTHONPATH=tools/thai/cache/python:tools/thai "
    "python3 -B tools/thai/shape_thai_precompose.py"
)
OLD_MAP = "tools/thai/font/thai_shaped_glyph_map.json"
NEW_MAP = "tools/thai/font/thai_precompose_glyph_map.json"

MENU_RE = re.compile(
    r'const u8 gText_MainMenuNewGame\[\]\s*=\s*_\(".*?"\);',
    re.S,
)
UNICODE_MENU = 'const u8 gText_MainMenuNewGame[] = _("เริ่มเกมส์");'


def fail(message):
    raise SystemExit(f"ERROR: {message}")


def digest(path):
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def git(*args, check=True):
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and result.returncode:
        fail(result.stderr.strip() or "git command failed")
    return result


def verify_repo():
    branch = git("branch", "--show-current").stdout.strip()
    if branch != BRANCH:
        fail(f"ต้องรันบน Branch {BRANCH!r}; ปัจจุบันคือ {branch!r}")

    result = git(
        "merge-base",
        "--is-ancestor",
        CHECKPOINT,
        "HEAD",
        check=False,
    )
    if result.returncode:
        fail(f"ไม่พบ Checkpoint {CHECKPOINT} ใน Branch ปัจจุบัน")


def require_files():
    for path in (FULL_ATLAS, FULL_MAP, SHAPER, MAKEFILE, ATLAS, STRINGS):
        if not path.is_file():
            fail(f"ไม่พบไฟล์: {path.relative_to(ROOT)}")

    data = json.loads(FULL_MAP.read_text(encoding="utf-8"))
    if data.get("format") != "pokemon-gen3-thai-precompose-full-v1":
        fail("Full map format ไม่ถูกต้อง")
    if data.get("glyph_count") != 761:
        fail("Full map ต้องมี 761 Glyph")
    if data.get("atlas_size") != [256, 768]:
        fail("Full map ต้องอ้าง Atlas 256x768")


def menu_text():
    matches = MENU_RE.findall(STRINGS.read_text(encoding="utf-8"))
    if len(matches) != 1:
        fail(f"ต้องพบ gText_MainMenuNewGame 1 จุด แต่พบ {len(matches)}")
    return matches[0]


def set_menu(declaration):
    source = STRINGS.read_text(encoding="utf-8")
    updated, count = MENU_RE.subn(declaration, source, count=1)
    if count != 1:
        fail("แก้ gText_MainMenuNewGame ไม่สำเร็จ")
    temp = STRINGS.with_suffix(".c.precompose_full_tmp")
    temp.write_text(updated, encoding="utf-8")
    temp.replace(STRINGS)


def load_manifest():
    if not MANIFEST.exists():
        return None
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def write_manifest(data):
    STATE.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def create_backup():
    BACKUP.mkdir(parents=True, exist_ok=True)
    for path in (BACKUP_MAKEFILE, BACKUP_ATLAS, BACKUP_STRINGS, BACKUP_ACTIVE_MAP):
        if path.exists():
            fail(f"พบ Backup เดิมที่ไม่คาดไว้: {path.relative_to(ROOT)}")

    shutil.copy2(MAKEFILE, BACKUP_MAKEFILE)
    shutil.copy2(ATLAS, BACKUP_ATLAS)
    shutil.copy2(STRINGS, BACKUP_STRINGS)

    preexisting_map = ACTIVE_MAP.exists()
    if preexisting_map:
        shutil.copy2(ACTIVE_MAP, BACKUP_ACTIVE_MAP)

    data = {
        "format": "pokemon-gen3-thai-precompose-full-runtime-v1",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "installed": False,
        "active_map_preexisted": preexisting_map,
        "backup": {
            "makefile": digest(BACKUP_MAKEFILE),
            "atlas": digest(BACKUP_ATLAS),
            "strings": digest(BACKUP_STRINGS),
        },
    }
    if preexisting_map:
        data["backup"]["active_map"] = digest(BACKUP_ACTIVE_MAP)

    write_manifest(data)
    return data


def backup_data():
    data = load_manifest()
    if data is None:
        return create_backup()
    if data.get("format") != "pokemon-gen3-thai-precompose-full-runtime-v1":
        fail("Manifest format ไม่ถูกต้อง")

    checks = (
        (BACKUP_MAKEFILE, data["backup"]["makefile"]),
        (BACKUP_ATLAS, data["backup"]["atlas"]),
        (BACKUP_STRINGS, data["backup"]["strings"]),
    )
    for path, expected in checks:
        if not path.is_file() or digest(path) != expected:
            fail(f"Backup ไม่สมบูรณ์: {path.relative_to(ROOT)}")
    return data


def state():
    make_text = MAKEFILE.read_text(encoding="utf-8")
    return {
        "atlas": digest(ATLAS) == digest(FULL_ATLAS),
        "map": ACTIVE_MAP.is_file() and digest(ACTIVE_MAP) == digest(FULL_MAP),
        "make_shaper": NEW_SHAPER in make_text,
        "make_map": make_text.count(NEW_MAP) == 3,
        "menu": menu_text() == UNICODE_MENU,
    }


def status():
    verify_repo()
    require_files()
    values = state()

    print("========================================")
    print("FULL PRECOMPOSE RUNTIME STATUS")
    print("========================================")
    print("Repository       :", ROOT)
    print("Branch           :", git("branch", "--show-current").stdout.strip())
    print("HEAD             :", git("rev-parse", "--short", "HEAD").stdout.strip())
    print("Manifest         :", "FOUND" if MANIFEST.exists() else "NOT FOUND")
    print("Atlas installed  :", "YES" if values["atlas"] else "NO")
    print("Map installed    :", "YES" if values["map"] else "NO")
    print("Makefile shaper  :", "YES" if values["make_shaper"] else "NO")
    print("Makefile map     :", "YES" if values["make_map"] else "NO")
    print("Unicode menu     :", "YES" if values["menu"] else "NO")
    print("Current menu     :", menu_text())
    print()

    if all(values.values()):
        print("STATUS: INSTALLED")
        return 0
    if not any(values.values()):
        print("STATUS: NOT INSTALLED / RESTORED")
        return 0

    print("STATUS: PARTIAL STATE — ห้าม Build จนกว่าจะ Restore")
    return 2


def install():
    verify_repo()
    require_files()
    manifest = backup_data()

    values = state()
    if all(values.values()):
        print("Full precompose runtime ติดตั้งอยู่แล้ว")
        return status()
    if manifest.get("installed"):
        fail("Manifest ระบุว่าติดตั้งแล้ว แต่ไฟล์ไม่ตรงครบ ให้ Restore ก่อน")

    expected = (
        (MAKEFILE, manifest["backup"]["makefile"]),
        (ATLAS, manifest["backup"]["atlas"]),
        (STRINGS, manifest["backup"]["strings"]),
    )
    for path, expected_hash in expected:
        if digest(path) != expected_hash:
            fail(f"ไม่ติดตั้งทับไฟล์ที่เปลี่ยนจาก Backup: {path.relative_to(ROOT)}")

    if ACTIVE_MAP.exists() and not manifest["active_map_preexisted"]:
        fail(f"พบ Active map ที่ไม่ได้สร้างโดย Installer: {ACTIVE_MAP.relative_to(ROOT)}")

    make_text = MAKEFILE.read_text(encoding="utf-8")
    if make_text.count(OLD_SHAPER) != 1:
        fail("Makefile ต้องมี Production shaper definition 1 จุด")
    if make_text.count(OLD_MAP) != 3:
        fail("Makefile ต้องมี Old map dependency 3 จุด")

    shutil.copy2(FULL_ATLAS, ATLAS)
    shutil.copy2(FULL_MAP, ACTIVE_MAP)

    make_text = make_text.replace(OLD_SHAPER, NEW_SHAPER, 1)
    make_text = make_text.replace(OLD_MAP, NEW_MAP)
    MAKEFILE.write_text(make_text, encoding="utf-8")
    set_menu(UNICODE_MENU)

    check = subprocess.run(
        [sys.executable, str(SHAPER.relative_to(ROOT)), "--check"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if check.returncode:
        print(check.stdout, end="")
        print(check.stderr, end="", file=sys.stderr)
        fail("Precompose shaper check ไม่ผ่าน")

    manifest["installed"] = True
    manifest["installed_at_utc"] = datetime.now(timezone.utc).isoformat()
    write_manifest(manifest)

    print(check.stdout, end="")
    print()
    print("========================================")
    print("FULL PRECOMPOSE RUNTIME INSTALLED")
    print("========================================")
    print("Atlas  :", ATLAS.relative_to(ROOT))
    print("Map    :", ACTIVE_MAP.relative_to(ROOT))
    print("Shaper :", SHAPER.relative_to(ROOT))
    print("Menu   :", UNICODE_MENU)
    print("Backup :", BACKUP.relative_to(ROOT))
    print()
    print("NEXT:")
    print("  rm -f build/assets/graphics/fonts/thai_shaped.png.latfont")
    print('  make -j"$(nproc)"')
    return 0


def restore():
    verify_repo()
    require_files()
    manifest = backup_data()

    shutil.copy2(BACKUP_MAKEFILE, MAKEFILE)
    shutil.copy2(BACKUP_ATLAS, ATLAS)
    shutil.copy2(BACKUP_STRINGS, STRINGS)

    if manifest["active_map_preexisted"]:
        shutil.copy2(BACKUP_ACTIVE_MAP, ACTIVE_MAP)
    elif ACTIVE_MAP.exists():
        ACTIVE_MAP.unlink()

    manifest["installed"] = False
    manifest["restored_at_utc"] = datetime.now(timezone.utc).isoformat()
    write_manifest(manifest)

    print("========================================")
    print("FULL PRECOMPOSE RUNTIME RESTORED")
    print("========================================")
    print("คืน Makefile, Atlas และ src/strings.c สำเร็จ")
    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("install", "status", "restore"))
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
        print("\nCancelled.", file=sys.stderr)
        raise SystemExit(130)
