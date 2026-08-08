#!/usr/bin/env python3
"""Source, preprocessing, object, and snapshot checks for K3C-R3D probes."""

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
SNAPSHOT_PATH = Path.home() / ".local/share/pekeemerald/thai-naming-keyboard/k3c_r3d_preflight_snapshot.json"
SNAPSHOT = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))
CPP_FLAGS = [
    "-iquote", "include", "-Wno-trigraphs", "-DMODERN=0",
    "-I", "tools/agbcc/include", "-I", "tools/agbcc", "-nostdinc",
    "-undef", "-std=gnu89",
]
PROBE_NAMES = (
    "CB2_ThaiReturnProbeHold", "EnterThaiReturnProbeHold",
    "sThaiReturnProbeColor", "sThaiReturnProbeFrameCounter",
    "CB2_ThaiReturnProbeWrapper", "THAI_RETURN_PROBE_FADE_TIMEOUT",
)


def run(command: list[str], *, input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        command, cwd=ROOT, input=input_text, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if result.returncode:
        raise AssertionError(
            f"command failed ({result.returncode}): {' '.join(command)}\n{result.stderr}"
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


def preprocess(*defines: str) -> str:
    command = ["cc", "-E", "-P", *CPP_FLAGS]
    command.extend(f"-D{define}" for define in defines)
    command.append("src/naming_screen.c")
    return run(command).stdout


def compile_probe_object(stage: int, output: Path) -> str:
    defines = [
        "THAI_NAMING_KEYBOARD_K3C", "THAI_NAMING_RETURN_PROBE",
        f"THAI_NAMING_RETURN_PROBE_STAGE={stage}",
    ]
    cpp = run(["cc", "-E", *CPP_FLAGS, *(f"-D{x}" for x in defines), "src/naming_screen.c"]).stdout
    shaped = run(
        ["python3", "-B", "tools/thai/shape_thai_precompose.py", "--filter-source"],
        input_text=cpp,
    ).stdout
    preprocessed = run(
        ["tools/preproc/preproc", "-i", "-g", "build/assets", "src/naming_screen.c", "charmap.txt"],
        input_text=shaped,
    ).stdout
    assembly = run(
        ["tools/agbcc/bin/agbcc", "-mthumb-interwork", "-Wimplicit", "-Wparentheses",
         "-Werror", "-O2", "-fhex-asm", "-g", "-o", "-", "-"],
        input_text=preprocessed,
    ).stdout + ".text\n\t.align\t2, 0\n"
    run(["arm-none-eabi-as", "-mcpu=arm7tdmi", "--defsym", "MODERN=0", "-o", str(output), "-"], input_text=assembly)
    return run(["arm-none-eabi-nm", str(output)]).stdout


def test_double_gate_and_preprocessing_isolation() -> None:
    assert NAMING.count("defined(THAI_NAMING_KEYBOARD_K3C) && defined(THAI_NAMING_RETURN_PROBE)") >= 4
    normal_r3 = preprocess("THAI_NAMING_KEYBOARD_K3C")
    compile_off = preprocess()
    for name in PROBE_NAMES:
        assert name not in normal_r3
        assert name not in compile_off
    assert "DoThaiNamingScreenPrototype" in normal_r3
    assert "DoThaiNamingScreenPrototype" not in compile_off
    assert "SaveThaiPrototypeInputText" not in compile_off


def test_hold_display_contract() -> None:
    hold = function_body(NAMING, "static void CB2_ThaiReturnProbeHold(void)")
    ordered(
        hold, "SetVBlankCallback(NULL);", "SetHBlankCallback(NULL);",
        "SetGpuReg(REG_OFFSET_DISPCNT, DISPCNT_MODE_0);",
        "gPlttBufferUnfaded[0] = sThaiReturnProbeColor;",
        "gPlttBufferFaded[0] = sThaiReturnProbeColor;",
        "*((u16 *)PLTT) = sThaiReturnProbeColor;",
        "SetMainCallback2(CB2_ThaiReturnProbeHold);",
    )
    assert "while" not in hold and "for" not in hold
    assert "AddTextPrinter" not in hold and "PlaySE" not in hold


def test_probe_1_fade_gate() -> None:
    body = function_body(preprocess(
        "THAI_NAMING_KEYBOARD_K3C", "THAI_NAMING_RETURN_PROBE",
        "THAI_NAMING_RETURN_PROBE_STAGE=1",
    ), "static bool8 MainState_Exit(void)")
    ordered(body, "gPaletteFade.active", "++sThaiReturnProbeFrameCounter >= 180", "EnterThaiReturnProbeHold(((0) | ((31) << 5) | ((0) << 10)))")
    assert "EnterThaiReturnProbeHold(((31) | ((0) << 5) | ((0) << 10)))" in body
    launch = function_body(NAMING, "void DoThaiNamingScreenPrototype(MainCallback returnCallback)")
    ordered(launch, "sThaiReturnProbeFrameCounter = 0;", "DoNamingScreen(")


def test_probe_2_cleanup_order_and_no_post_free_read() -> None:
    body = function_body(preprocess(
        "THAI_NAMING_KEYBOARD_K3C", "THAI_NAMING_RETURN_PROBE",
        "THAI_NAMING_RETURN_PROBE_STAGE=2",
    ), "static bool8 MainState_Exit(void)")
    ordered(
        body, "SetVBlankCallback(((void *)0));", "SetMainCallback2(sNamingScreen->returnCallback);",
        "DestroyTask(FindTaskIdByFunc(Task_NamingScreen));", "FreeAllWindowBuffers();",
        "Free(sNamingScreen); sNamingScreen = ((void *)0);", "EnterThaiReturnProbeHold(((0) | ((0) << 5) | ((31) << 10)))",
    )
    after_free = body.split("sNamingScreen = ((void *)0);", 1)[1]
    assert "sNamingScreen->" not in after_free


def test_wrappers_and_stage_objects() -> None:
    expected = {
        3: ("RGB_YELLOW", False, True),
        4: ("RGB_CYAN", True, True),
        5: (None, True, False),
    }
    with tempfile.TemporaryDirectory(prefix="k3c-r3d-objects.") as directory:
        for stage in range(1, 6):
            obj = Path(directory) / f"stage{stage}.o"
            symbols = compile_probe_object(stage, obj)
            assert "CB2_ThaiReturnProbeHold" in symbols
            if stage >= 3:
                assert "CB2_ThaiReturnProbeWrapper" in symbols
            source = preprocess(
                "THAI_NAMING_KEYBOARD_K3C", "THAI_NAMING_RETURN_PROBE",
                f"THAI_NAMING_RETURN_PROBE_STAGE={stage}",
            )
            if stage in expected:
                body = function_body(source, "static void CB2_ThaiReturnProbeWrapper(void)")
                color, calls_menu, holds = expected[stage]
                assert body.count("CB2_InitMainMenu();") == int(calls_menu)
                assert ("EnterThaiReturnProbeHold" in body) is holds
                if color == "RGB_YELLOW":
                    assert "CB2_InitMainMenu" not in body
                if stage == 4:
                    ordered(body, "CB2_InitMainMenu();", "EnterThaiReturnProbeHold")


def test_r2_blocks_and_snapshot_protection() -> None:
    # These are the R2 authoritative payload and single-upload rendering markers.
    payload = re.search(r"static const u8 sThaiPrototypeKeyboardChars.*?^};", NAMING, re.S | re.M)
    rendering = function_body(NAMING, "static void PrintKeyboardKeys(u8 window, u8 page)")
    assert payload and payload.group(0).count("EOS") == 31
    assert "{{0x37,0x38,0x39,0x3A,0x3B,0x3C,0x3D,0x3E}" in payload.group(0)
    thai_branch = rendering.split("if (sNamingScreen->compactThaiMode)", 1)[1].split("#endif", 1)[0]
    assert thai_branch.count("CopyWindowToVram(window, COPYWIN_GFX);") == 1
    assert "TEXT_SKIP_DRAW" in thai_branch

    assert SNAPSHOT["preflight_pass"] is True
    for relative, record in SNAPSHOT["files"].items():
        if relative == "src/naming_screen.c":
            continue
        assert sha256(ROOT / relative) == record["sha256"], relative


def test_diff_check() -> None:
    run(["git", "diff", "--check"])


TESTS = [
    test_double_gate_and_preprocessing_isolation,
    test_hold_display_contract,
    test_probe_1_fade_gate,
    test_probe_2_cleanup_order_and_no_post_free_read,
    test_wrappers_and_stage_objects,
    test_r2_blocks_and_snapshot_protection,
    test_diff_check,
]


def main() -> None:
    for test in TESTS:
        test()
        print(f"PASS: {test.__name__}")
    print(f"PASS: {len(TESTS)} K3C-R3D diagnostic groups")


if __name__ == "__main__":
    main()
