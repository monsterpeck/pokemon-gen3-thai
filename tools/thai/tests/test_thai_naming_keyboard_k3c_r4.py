#!/usr/bin/env python3
"""Source, preprocessing, object/ROM, and snapshot checks for K3C-R4."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
NAMING_PATH = ROOT / "src/naming_screen.c"
NAMING = NAMING_PATH.read_text(encoding="utf-8")
SNAPSHOT_PATH = Path.home() / ".local/share/pekeemerald/thai-naming-keyboard/k3c_r4_preflight_snapshot.json"
SNAPSHOT = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))
CPP_FLAGS = [
    "-iquote", "include", "-Wno-trigraphs", "-DMODERN=0",
    "-I", "tools/agbcc/include", "-I", "tools/agbcc", "-nostdinc",
    "-undef", "-std=gnu89",
]
MAKE_CPPFLAGS = " ".join(CPP_FLAGS)
PROBE_HASHES = {
    1: "62e3bf68e9eeab1c09b444066161e61423c08ce6a63b4d62a33acbeb90ad0362",
    2: "8f72a235a2948095316e3497aaa9201a8e77a1c3a8e95c0e663037a2062549ad",
    3: "11685a088e1c423f7cc8be44a039e474dd98a2a7f46e40f88c4668c01c5892ff",
    4: "4917526dc74953669bccf2e43b454863ffdf53adc13ae1e0e78d0c8dcf9198ef",
    5: "9eb57c416a80ce6d6a4fba26c4b49289391bb077060286c7b6be9dd31041d4f0",
}
R4_SYMBOLS = (
    "CB2_ThaiPrototypeExitHandoff", "sThaiPrototypeSavedReturnCallback",
    "sThaiPrototypeExitHandoffPending",
)


def run(command: list[str], *, input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        command, cwd=ROOT, input=input_text, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if result.returncode:
        raise AssertionError(
            f"command failed ({result.returncode}): {' '.join(command)}\n"
            f"{result.stdout}\n{result.stderr}"
        )
    return result


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def function_body(source: str, signature: str) -> str:
    match = re.search(re.escape(signature) + r"[^;{]*\{", source)
    if match is None:
        raise AssertionError(f"function definition not found: {signature}")
    brace = source.index("{", match.start())
    depth = 0
    for pos in range(brace, len(source)):
        if source[pos] == "{":
            depth += 1
        elif source[pos] == "}":
            depth -= 1
            if depth == 0:
                return source[brace + 1:pos]
    raise AssertionError(f"unterminated function: {signature}")


def ordered(body: str, *needles: str) -> None:
    positions = [body.index(needle) for needle in needles]
    assert positions == sorted(positions), (needles, positions)


def preprocess(*defines: str, source: str | None = None) -> str:
    command = ["cc", "-E", "-P", *CPP_FLAGS]
    command.extend(f"-D{define}" for define in defines)
    if source is None:
        command.append("src/naming_screen.c")
        return run(command).stdout
    command.extend(["-x", "c", "-"])
    return run(command, input_text=source).stdout


def make_rom(*defines: str) -> str:
    run(["make", "clean"])
    flags = MAKE_CPPFLAGS + " " + " ".join(f"-D{x}" for x in defines)
    run(["make", "-j4", f"CPPFLAGS={flags}"])
    return sha256(ROOT / "pokeemerald.gba")


def test_probe_result_root_cause_contract() -> None:
    callback = function_body(NAMING, "static void CB2_NamingScreen(void)")
    ordered(callback, "RunTasks();", "AnimateSprites();", "BuildOamBuffer();", "UpdatePaletteFade();")
    task = function_body(NAMING, "static void Task_NamingScreen(u8 taskId)")
    assert "case STATE_EXIT:" in task and "MainState_Exit();" in task
    assert callback.index("RunTasks();") < callback.index("AnimateSprites();")
    underscore = function_body(NAMING, "static void SpriteCB_Underscore(struct Sprite *sprite)")
    arrow = function_body(NAMING, "static void SpriteCB_InputArrow(struct Sprite *sprite)")
    position = function_body(NAMING, "static u8 GetTextEntryPosition(void)")
    caret = function_body(NAMING, "static u16 GetTextEntryCaretX(void)")
    assert "GetTextEntryPosition()" in underscore and "sNamingScreen->" in position
    assert "GetTextEntryCaretX()" in arrow and "sNamingScreen->" in caret


def test_deferred_exit_and_handoff_order() -> None:
    normal = preprocess("THAI_NAMING_KEYBOARD_K3C")
    exit_body = function_body(normal, "static bool8 MainState_Exit(void)")
    compact = exit_body.split("if (sNamingScreen->compactThaiMode)", 1)[1].split("return 0;", 1)[0]
    ordered(
        compact,
        "sThaiPrototypeSavedReturnCallback = sNamingScreen->returnCallback;",
        "sThaiPrototypeExitHandoffPending = 1;",
        "SetMainCallback2(CB2_ThaiPrototypeExitHandoff);",
        "DestroyTask(namingTaskId);",
    )
    assert "FreeAllWindowBuffers" not in compact
    assert "Free(sNamingScreen)" not in compact
    assert "SetMainCallback2(sNamingScreen->returnCallback)" not in compact

    handoff = function_body(normal, "static void CB2_ThaiPrototypeExitHandoff(void)")
    ordered(
        handoff,
        "sThaiPrototypeExitHandoffPending",
        "sThaiPrototypeSavedReturnCallback != ((void *)0)",
        "SetVBlankCallback(((void *)0));",
        "SetHBlankCallback(((void *)0));",
        "returnCallback = sThaiPrototypeSavedReturnCallback;",
        "sThaiPrototypeExitHandoffPending = 0;",
        "sThaiPrototypeSavedReturnCallback = ((void *)0);",
        "FreeAllWindowBuffers();",
        "Free(sNamingScreen); sNamingScreen = ((void *)0);",
        "SetMainCallback2(handoffIsValid ? returnCallback : CB2_InitMainMenu);",
        "return;",
    )
    for forbidden in ("RunTasks", "AnimateSprites", "BuildOamBuffer", "UpdatePaletteFade", "AddTextPrinter", "SaveInputText"):
        assert forbidden not in handoff
    after_free = handoff.split("sNamingScreen = ((void *)0);", 1)[1]
    assert "sNamingScreen->" not in after_free
    assert "returnCallback();" not in handoff


def test_relaunch_reset_and_legacy_isolation() -> None:
    normal = preprocess("THAI_NAMING_KEYBOARD_K3C")
    launch = function_body(normal, "void DoThaiNamingScreenPrototype(MainCallback returnCallback)")
    ordered(
        launch,
        "sThaiPrototypeScratch.guardLeft",
        "sThaiPrototypeScratch.guardRight",
        "sThaiPrototypeScratch.text[i] = 0xFF;",
        "sThaiPrototypeExitHandoffPending = 0;",
        "sThaiPrototypeSavedReturnCallback = ((void *)0);",
        "DoNamingScreen(",
    )
    compile_off = preprocess()
    pristine = run(["git", "show", f"{SNAPSHOT['head']}:src/naming_screen.c"]).stdout
    # Existing K3C indentation survives -P around disabled branches; tokens must
    # remain exactly legacy, while ROM identity is proven by the clean builds.
    assert re.sub(r"\s+", " ", compile_off) == re.sub(r"\s+", " ", preprocess(source=pristine))
    for symbol in R4_SYMBOLS:
        assert symbol not in compile_off
    assert "static void SaveInputText(void)" in NAMING
    exit_body = function_body(normal, "static bool8 MainState_Exit(void)")
    legacy_tail = exit_body.rsplit("SetMainCallback2(sNamingScreen->returnCallback);", 1)[1]
    ordered(legacy_tail, "DestroyTask", "FreeAllWindowBuffers();", "Free(sNamingScreen)")


def test_r2_r3_preservation_and_no_unrelated_apis() -> None:
    payload = re.search(r"static const u8 sThaiPrototypeKeyboardChars.*?^};", NAMING, re.S | re.M)
    rendering = function_body(NAMING, "static void PrintKeyboardKeys(u8 window, u8 page)")
    assert payload and payload.group(0).count("EOS") == 31
    assert "{{0x37,0x38,0x39,0x3A,0x3B,0x3C,0x3D,0x3E}" in payload.group(0)
    thai_branch = rendering.split("if (sNamingScreen->compactThaiMode)", 1)[1].split("#endif", 1)[0]
    assert thai_branch.count("CopyWindowToVram(window, COPYWIN_GFX);") == 1
    assert "TEXT_SKIP_DRAW" in thai_branch
    assert len(re.findall(r'sThaiPrototypeLabel_\d+\[\] = _\("', NAMING)) == 65
    assert "ShapeThaiPrototypeText" in NAMING and "sThaiPrototypeScratch.text" in NAMING
    exit_source = function_body(NAMING, "static bool8 MainState_Exit(void)")
    assert "SetVBlankCallback(NULL);" in exit_source
    prototype_scope = function_body(NAMING, "void DoThaiNamingScreenPrototype(MainCallback returnCallback)")
    prototype_scope += function_body(NAMING, "static void CB2_ThaiPrototypeExitHandoff(void)")
    for forbidden in ("SaveBlock", "SetMonData", "SetBoxMonData", "SendLink", "TrySavingData", "GetBoxNamePtr"):
        assert forbidden not in prototype_scope


def test_probe_preprocessing_and_exact_roms() -> None:
    for stage in range(1, 6):
        probe = preprocess(
            "THAI_NAMING_KEYBOARD_K3C", "THAI_NAMING_RETURN_PROBE",
            f"THAI_NAMING_RETURN_PROBE_STAGE={stage}",
        )
        for symbol in R4_SYMBOLS:
            assert symbol not in probe
        assert make_rom(
            "THAI_NAMING_KEYBOARD_K3C", "THAI_NAMING_RETURN_PROBE",
            f"THAI_NAMING_RETURN_PROBE_STAGE={stage}",
        ) == PROBE_HASHES[stage]


def test_normal_object_and_snapshot_protection() -> None:
    with tempfile.TemporaryDirectory(prefix="k3c-r4-object.") as directory:
        output = Path(directory) / "naming_screen.o"
        run(["make", "clean"])
        flags = MAKE_CPPFLAGS + " -DTHAI_NAMING_KEYBOARD_K3C"
        run(["make", "-j4", f"CPPFLAGS={flags}", "build/emerald/src/naming_screen.o"])
        symbols = run(["arm-none-eabi-nm", str(ROOT / "build/emerald/src/naming_screen.o")]).stdout
        assert "CB2_ThaiPrototypeExitHandoff" in symbols

    assert SNAPSHOT["preflight_pass"] is True
    for relative, record in SNAPSHOT["files"].items():
        if relative == "src/naming_screen.c":
            continue
        assert sha256(ROOT / relative) == record["sha256"], relative
    status = run(["git", "status", "--porcelain"]).stdout.splitlines()
    allowed = set(SNAPSHOT["changed_files"]) | {
        "src/naming_screen.c", "tools/thai/tests/test_thai_naming_keyboard_k3c_r4.py",
    }
    for line in status:
        assert line[3:] in allowed, line


def test_diff_check() -> None:
    run(["git", "diff", "--check"])


TESTS = [
    test_probe_result_root_cause_contract,
    test_deferred_exit_and_handoff_order,
    test_relaunch_reset_and_legacy_isolation,
    test_r2_r3_preservation_and_no_unrelated_apis,
    test_probe_preprocessing_and_exact_roms,
    test_normal_object_and_snapshot_protection,
    test_diff_check,
]


def main() -> None:
    for test in TESTS:
        test()
        print(f"PASS: {test.__name__}")
    print(f"PASS: {len(TESTS)} K3C-R4 regression groups")


if __name__ == "__main__":
    main()
