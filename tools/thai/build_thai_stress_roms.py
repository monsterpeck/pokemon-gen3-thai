#!/usr/bin/env python3
"""
Build several ROM variants that use the NEW GAME menu label as a safe
Thai font stress-test target.

The script:
- requires branch thai-precompose-full
- requires the full-precompose proof commit/tag in history
- preflights every Thai test string with shape_thai_precompose.py
- changes only src/strings.c temporarily
- builds one ROM per test case
- restores src/strings.c exactly, even after an error or Ctrl+C
- writes ROMs, logs, and a manifest under:
    tools/thai/generated/precompose_stress_roms/

It does not commit, stage, reset, clean, or delete user work.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
BRANCH = "thai-precompose-full"
REQUIRED_REF = "full-precompose-761-runtime-proof"

STRINGS_SOURCE = ROOT / "src/strings.c"
SHAPER = ROOT / "tools/thai/shape_thai_precompose.py"
ROM = ROOT / "pokeemerald.gba"

OUTPUT_DIR = ROOT / "tools/thai/generated/precompose_stress_roms"
LOG_DIR = OUTPUT_DIR / "logs"
MANIFEST = OUTPUT_DIR / "stress_rom_manifest.json"
REPORT = OUTPUT_DIR / "stress_rom_report.txt"

MENU_PATTERN = re.compile(
    r'const u8 gText_MainMenuNewGame\[\]\s*=\s*_\(".*?"\);',
    re.DOTALL,
)

TEST_CASES: list[dict[str, str]] = [
    {
        "id": "01_start_game",
        "label": "Baseline",
        "text": "เริ่มเกมส์",
        "focus": "คำต้นแบบ ริ่ และ ส์",
    },
    {
        "id": "02_upper_marks",
        "label": "Upper marks",
        "text": "กิ กี กี่",
        "focus": "สระบนและวรรณยุกต์",
    },
    {
        "id": "03_lower_marks",
        "label": "Lower marks",
        "text": "กุ กู กุ่",
        "focus": "สระล่างและวรรณยุกต์ร่วมกัน",
    },
    {
        "id": "04_mixed_stacks",
        "label": "Mixed stacks",
        "text": "รู้ สู้ ผู้",
        "focus": "กลุ่มสระล่างและวรรณยุกต์",
    },
    {
        "id": "05_japanese_word",
        "label": "Japanese word",
        "text": "ญี่ปุ่น",
        "focus": "ญี่ ปุ่ และการต่อ Cluster",
    },
    {
        "id": "06_sara_am",
        "label": "Sara am",
        "text": "น้ำ คำ ย้ำ",
        "focus": "สระอำและวรรณยุกต์",
    },
    {
        "id": "07_pokemon",
        "label": "Pokémon",
        "text": "โปเกมอน",
        "focus": "สระนำหน้าและคำศัพท์หลัก",
    },
    {
        "id": "08_trainer",
        "label": "Trainer",
        "text": "เทรนเนอร์",
        "focus": "คำยาว ร์ และระยะรวม",
    },
]


class StressBuildError(RuntimeError):
    pass


def fail(message: str) -> "NoReturn":
    raise StressBuildError(message)


def run(
    command: list[str],
    *,
    capture: bool = False,
    check: bool = True,
    log_path: Path | None = None,
) -> subprocess.CompletedProcess[str]:
    if log_path is not None:
        with log_path.open("w", encoding="utf-8") as handle:
            result = subprocess.run(
                command,
                cwd=ROOT,
                text=True,
                stdout=handle,
                stderr=subprocess.STDOUT,
            )
        if check and result.returncode != 0:
            fail(
                f"คำสั่งล้มเหลว (exit {result.returncode}): "
                + " ".join(command)
                + f"\nLog: {log_path.relative_to(ROOT)}"
            )
        return result

    return subprocess.run(
        command,
        cwd=ROOT,
        check=check,
        text=True,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.PIPE if capture else None,
    )


def git_output(*args: str) -> str:
    result = run(["git", *args], capture=True)
    return result.stdout.strip()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_repository() -> None:
    if not (ROOT / ".git").exists():
        fail(f"ไม่พบ Git worktree ที่ {ROOT}")

    branch = git_output("branch", "--show-current")
    if branch != BRANCH:
        fail(f"ต้องรันบน Branch {BRANCH!r} แต่ปัจจุบันคือ {branch!r}")

    ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", REQUIRED_REF, "HEAD"],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if ancestor.returncode != 0:
        fail(f"ไม่พบ {REQUIRED_REF!r} ในประวัติ Branch")

    for path in (STRINGS_SOURCE, SHAPER):
        if not path.is_file():
            fail(f"ไม่พบไฟล์ที่จำเป็น: {path.relative_to(ROOT)}")


def read_menu_declaration(source: str) -> str:
    matches = MENU_PATTERN.findall(source)
    if len(matches) != 1:
        fail(
            "ต้องพบ gText_MainMenuNewGame เพียง 1 จุด "
            f"แต่พบ {len(matches)} จุด"
        )
    return matches[0]


def replace_menu(source: str, text: str) -> str:
    declaration = (
        'const u8 gText_MainMenuNewGame[] = '
        f'_("{text}");'
    )
    updated, count = MENU_PATTERN.subn(declaration, source, count=1)
    if count != 1:
        fail("เปลี่ยน gText_MainMenuNewGame ไม่สำเร็จ")
    return updated


def write_atomic(path: Path, content: bytes) -> None:
    temporary = path.with_name(path.name + ".stress_tmp")
    temporary.write_bytes(content)
    temporary.replace(path)


def preflight_cases() -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    thai_re = re.compile(r"[\u0E00-\u0E7F]+")

    for case in TEST_CASES:
        thai_runs = thai_re.findall(case["text"])

        if not thai_runs:
            fail(
                f"Test case {case['id']} ไม่มีข้อความไทย: "
                f"{case['text']!r}"
            )

        encoded_runs: list[str] = []

        for thai_run in thai_runs:
            result = run(
                [
                    sys.executable,
                    str(SHAPER.relative_to(ROOT)),
                    "--encode",
                    thai_run,
                ],
                capture=True,
                check=False,
            )

            if result.returncode != 0:
                fail(
                    f"Shaper ไม่รองรับ Test case {case['id']}: "
                    f"{case['text']!r}\n"
                    f"Thai run: {thai_run!r}\n"
                    f"{result.stderr.strip()}"
                )

            output_lines = result.stdout.splitlines()

            if not output_lines:
                fail(
                    f"Shaper ไม่คืนผลลัพธ์สำหรับ "
                    f"{thai_run!r}"
                )

            encoded_runs.append(output_lines[0].strip())

        results.append(
            {
                **case,
                "thai_runs": thai_runs,
                "encoded_hex_runs": encoded_runs,
            }
        )

    return results


def build_case(
    case: dict[str, Any],
    original_source: str,
) -> dict[str, Any]:
    source_text = replace_menu(original_source, case["text"])
    write_atomic(STRINGS_SOURCE, source_text.encode("utf-8"))

    strings_object = ROOT / "build/emerald/src/strings.o"
    if strings_object.exists():
        strings_object.unlink()

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_path = LOG_DIR / f"{case['id']}.log"

    jobs = max(1, os.cpu_count() or 1)
    run(
        ["make", f"-j{jobs}"],
        log_path=log_path,
    )

    if not ROM.is_file():
        fail(f"Build ผ่านแต่ไม่พบ ROM สำหรับ {case['id']}")

    output_rom = OUTPUT_DIR / f"{case['id']}.gba"
    shutil.copy2(ROM, output_rom)

    return {
        **case,
        "rom": str(output_rom.relative_to(ROOT)),
        "rom_size": output_rom.stat().st_size,
        "rom_sha256": sha256(output_rom),
        "log": str(log_path.relative_to(ROOT)),
    }


def write_reports(
    *,
    original_menu: str,
    results: list[dict[str, Any]],
) -> None:
    payload = {
        "format": "pokemon-gen3-thai-precompose-stress-roms-v1",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "branch": git_output("branch", "--show-current"),
        "head": git_output("rev-parse", "HEAD"),
        "required_ref": REQUIRED_REF,
        "original_menu": original_menu,
        "cases": results,
    }
    MANIFEST.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    lines = [
        "THAI PRECOMPOSE STRESS ROMS",
        "============================",
        f"Branch       : {payload['branch']}",
        f"HEAD         : {payload['head']}",
        f"Original menu: {original_menu}",
        "",
    ]

    for item in results:
        lines.extend(
            [
                f"{item['id']}",
                f"  Text   : {item['text']}",
                f"  Focus  : {item['focus']}",
                f"  ROM    : {item['rom']}",
                f"  SHA256 : {item['rom_sha256']}",
                f"  Log    : {item['log']}",
                "",
            ]
        )

    lines.extend(
        [
            "RESULT: STRESS ROM BUILD PASSED",
            "",
            "ตรวจภาพใน Emulator ทีละ ROM แล้วบันทึก:",
            "- รูปร่างตัวอักษร",
            "- สระ/วรรณยุกต์ชนกันหรือไม่",
            "- ระยะตัวอักษร",
            "- การล้นหรือถูกตัดในเมนู",
        ]
    )

    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    verify_repository()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    original_bytes = STRINGS_SOURCE.read_bytes()
    original_source = original_bytes.decode("utf-8")
    original_menu = read_menu_declaration(original_source)

    print("========================================")
    print("THAI STRESS ROM PRECHECK")
    print("========================================")
    print(f"Repository : {ROOT}")
    print(f"Branch     : {git_output('branch', '--show-current')}")
    print(f"HEAD       : {git_output('rev-parse', '--short', 'HEAD')}")
    print(f"Cases      : {len(TEST_CASES)}")
    print()

    preflight = preflight_cases()
    for case in preflight:
        print(f"PASS: {case['id']} -> {case['text']}")
    print()

    results: list[dict[str, Any]] = []

    try:
        for number, case in enumerate(preflight, 1):
            print(
                f"[{number}/{len(preflight)}] "
                f"Building {case['id']}: {case['text']}"
            )
            result = build_case(case, original_source)
            results.append(result)
            print(f"  ROM    : {result['rom']}")
            print(f"  SHA256 : {result['rom_sha256']}")
    finally:
        write_atomic(STRINGS_SOURCE, original_bytes)
        print()
        print("Restored : src/strings.c")

    if len(results) != len(TEST_CASES):
        fail(
            f"สร้าง ROM ได้ {len(results)}/{len(TEST_CASES)} ชุด"
        )

    write_reports(
        original_menu=original_menu,
        results=results,
    )

    print()
    print("========================================")
    print("THAI STRESS ROM RESULT")
    print("========================================")
    print(f"ROM count : {len(results)}")
    print(f"Output    : {OUTPUT_DIR.relative_to(ROOT)}")
    print(f"Manifest  : {MANIFEST.relative_to(ROOT)}")
    print(f"Report    : {REPORT.relative_to(ROOT)}")
    print("Source    : RESTORED")
    print("RESULT: STRESS ROM BUILD PASSED")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except StressBuildError as exc:
        print(f"Stress ROM error: {exc}", file=sys.stderr)
        raise SystemExit(2)
    except KeyboardInterrupt:
        print("\nCancelled. src/strings.c will be restored.", file=sys.stderr)
        raise SystemExit(130)
