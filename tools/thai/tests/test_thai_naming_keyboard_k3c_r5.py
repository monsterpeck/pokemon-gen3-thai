#!/usr/bin/env python3
"""Source, preprocessing, ROM, and snapshot checks for K3C-R5."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MAIN = (ROOT / "src/main_menu.c").read_text(encoding="utf-8")
NAMING = (ROOT / "src/naming_screen.c").read_text(encoding="utf-8")
WINDOW = (ROOT / "src/window.c").read_text(encoding="utf-8")
SNAPSHOT = json.loads((Path.home() / ".local/share/pekeemerald/thai-naming-keyboard/k3c_r5_preflight_snapshot.json").read_text())
CPP_FLAGS = ["-iquote", "include", "-Wno-trigraphs", "-DMODERN=0", "-I", "tools/agbcc/include", "-I", "tools/agbcc", "-nostdinc", "-undef", "-std=gnu89"]
MAKE_FLAGS = " ".join(CPP_FLAGS)
R5_SYMBOL = "CB2_ThaiPrototypeLaunchHandoff"
PROBE_HASHES = {
    1: "62e3bf68e9eeab1c09b444066161e61423c08ce6a63b4d62a33acbeb90ad0362",
    2: "8f72a235a2948095316e3497aaa9201a8e77a1c3a8e95c0e663037a2062549ad",
    3: "11685a088e1c423f7cc8be44a039e474dd98a2a7f46e40f88c4668c01c5892ff",
    4: "4917526dc74953669bccf2e43b454863ffdf53adc13ae1e0e78d0c8dcf9198ef",
    5: "9eb57c416a80ce6d6a4fba26c4b49289391bb077060286c7b6be9dd31041d4f0",
}

def run(args: list[str], cwd: Path = ROOT, input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(args, cwd=cwd, input=input_text, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode:
        raise AssertionError(f"failed ({result.returncode}): {' '.join(args)}\n{result.stdout}\n{result.stderr}")
    return result

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def body(source: str, signature: str) -> str:
    match = re.search(re.escape(signature) + r"[^;{]*\{", source)
    assert match, signature
    start = source.index("{", match.start())
    depth = 0
    for pos in range(start, len(source)):
        depth += source[pos] == "{"
        depth -= source[pos] == "}"
        if depth == 0:
            return source[start + 1:pos]
    raise AssertionError(signature)

def cpp(*defines: str, source: str = "src/main_menu.c") -> str:
    return run(["cc", "-E", "-P", *CPP_FLAGS, *(f"-D{x}" for x in defines), source]).stdout

def make_rom(*defines: str) -> str:
    run(["make", "clean"])
    flags = MAKE_FLAGS + (" " if defines else "") + " ".join(f"-D{x}" for x in defines)
    run(["make", "-j4", f"CPPFLAGS={flags}"])
    return sha(ROOT / "pokeemerald.gba")

def test_repeated_launch_root_cause() -> None:
    init_menu = body(MAIN, "static u32 InitMainMenu(bool8 returningFromOptionsMenu)")
    assert "InitWindows(sWindowTemplates_MainMenu);" in init_menu
    init_windows = body(WINDOW, "bool16 InitWindows(const struct WindowTemplate *templates)")
    assert "gWindows[i].tileData = NULL;" in init_windows
    assert "AllocZeroed" in init_windows
    free_windows = body(WINDOW, "void FreeAllWindowBuffers(void)")
    assert "Free(gWindows[i].tileData);" in free_windows
    init_bgs = body(NAMING, "static void NamingScreen_InitBGs(void)")
    assert "InitStandardTextBoxWindows();" in init_bgs
    assert "for (i = 0; i < WIN_COUNT; i++)" in init_bgs and "AddWindow(&sWindowTemplates[i])" in init_bgs
    assert re.search(r"WIN_COUNT\s*,", NAMING)
    old = run(["git", "show", f"{SNAPSHOT['head']}:src/main_menu.c"]).stdout
    # The pre-R5 worktree delta is the direct launch recorded by the snapshot.
    assert "DoThaiNamingScreenPrototype(CB2_InitMainMenu);" in MAIN
    assert "FreeAllWindowBuffers" not in body(old, "static bool8 HandleMainMenuInput(u8 taskId)")

def test_deferred_current_frame_and_handoff_order() -> None:
    normal = cpp("THAI_NAMING_KEYBOARD_K3C")
    handle = body(normal, "static bool8 HandleMainMenuInput(u8 taskId)")
    assert f"SetMainCallback2({R5_SYMBOL});" in handle
    chord_source = body(MAIN, "static bool8 HandleMainMenuInput(u8 taskId)").split("JOY_NEW(SELECT_BUTTON)", 1)[1].split("else\n#endif", 1)[0]
    assert chord_source.count("PlaySE(SE_SELECT);") == 1
    for forbidden in ("DoThaiNamingScreenPrototype", "FreeAllWindowBuffers", "ResetTasks", "ResetSpriteData", "SetVBlankCallback"):
        assert forbidden not in handle
    assert R5_SYMBOL in normal
    handoff = body(MAIN, f"static void {R5_SYMBOL}(void)")
    required = ["SetVBlankCallback(NULL);", "SetHBlankCallback(NULL);", "SetGpuReg(REG_OFFSET_DISPCNT, 0);", "DeactivateAllTextPrinters();", "FreeAllWindowBuffers();", "DoThaiNamingScreenPrototype(CB2_InitMainMenu);", "return;"]
    positions = [handoff.index(item) for item in required]
    assert positions == sorted(positions)
    for forbidden in ("RunTasks", "AnimateSprites", "BuildOamBuffer", "UpdatePaletteFade", "CB2_InitMainMenu();"):
        assert forbidden not in handoff

def test_probe_and_compile_off_isolation() -> None:
    probe = cpp("THAI_NAMING_KEYBOARD_K3C", "THAI_NAMING_RETURN_PROBE")
    assert R5_SYMBOL not in probe
    probe_handle = body(probe, "static bool8 HandleMainMenuInput(u8 taskId)")
    assert probe_handle.index("PlaySE(") < probe_handle.index("DoThaiNamingScreenPrototype(CB2_InitMainMenu);")
    off = cpp()
    pristine = run(["git", "show", f"{SNAPSHOT['head']}:src/main_menu.c"]).stdout
    pristine_off = run(["cc", "-E", "-P", *CPP_FLAGS, "-x", "c", "-"], input_text=pristine).stdout
    assert re.sub(r"\s+", " ", off) == re.sub(r"\s+", " ", pristine_off)
    assert R5_SYMBOL not in off and "DoThaiNamingScreenPrototype" not in off

def test_snapshot_and_rom_contracts() -> None:
    assert SNAPSHOT["preflight_pass"] is True
    for relative, record in SNAPSHOT["files"].items():
        if relative == "src/main_menu.c":
            continue
        assert sha(ROOT / relative) == record["sha256"], relative
    allowed = set(SNAPSHOT["changed_files"]) | {"tools/thai/tests/test_thai_naming_keyboard_k3c_r5.py"}
    for line in run(["git", "status", "--porcelain"]).stdout.splitlines():
        if line[3:].startswith("tools/thai/generated/thai_naming_keyboard_k3c_r5_result.") or line[3:] == "pokeemerald-thai-naming-k3c-r5.gba":
            continue
        assert line[3:] in allowed, line
    pristine_hash = make_rom()
    assert make_rom() == pristine_hash
    for stage, expected in PROBE_HASHES.items():
        assert make_rom("THAI_NAMING_KEYBOARD_K3C", "THAI_NAMING_RETURN_PROBE", f"THAI_NAMING_RETURN_PROBE_STAGE={stage}") == expected

TESTS = [test_repeated_launch_root_cause, test_deferred_current_frame_and_handoff_order, test_probe_and_compile_off_isolation, test_snapshot_and_rom_contracts]

if __name__ == "__main__":
    for test in TESTS:
        test()
        print(f"PASS: {test.__name__}")
    print(f"PASS: {len(TESTS)} K3C-R5 regression groups")
