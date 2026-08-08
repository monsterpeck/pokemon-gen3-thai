#!/usr/bin/env python3
"""Static/control-flow regression tests for the K3C-R3 return handoff."""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[3]
NAMING = (ROOT / "src/naming_screen.c").read_text()
MAIN = (ROOT / "src/main.c").read_text()
MAIN_MENU = (ROOT / "src/main_menu.c").read_text()


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
                return source[brace + 1 : pos]
    raise AssertionError(f"unterminated function: {signature}")


def ordered(body: str, *needles: str) -> None:
    positions = [body.index(needle) for needle in needles]
    assert positions == sorted(positions), (needles, positions)


def test_engine_handoff_schedule() -> None:
    loop = function_body(MAIN, "void AgbMain(void)")
    ordered(loop, "UpdateLinkAndCallCallbacks();", "WaitForVBlank();")
    call_callbacks = function_body(MAIN, "static void CallCallbacks(void)")
    assert "gMain.callback2();" in call_callbacks
    wait = function_body(MAIN, "static void WaitForVBlank(void)")
    assert "while (!(gMain.intrCheck & INTR_FLAG_VBLANK))" in wait


def test_vblank_owns_naming_state() -> None:
    vblank = function_body(NAMING, "static void VBlankCB_NamingScreen(void)")
    assert len(re.findall(r"sNamingScreen->", vblank)) >= 4
    reset = function_body(NAMING, "static void ResetVHBlank(void)")
    ordered(reset, "SetVBlankCallback(NULL);", "SetHBlankCallback(NULL);")


def test_prototype_exit_relinquishes_vblank_before_free() -> None:
    exit_body = function_body(NAMING, "static bool8 MainState_Exit(void)")
    gated = re.search(
        r"#ifdef THAI_NAMING_KEYBOARD_K3C(?P<body>.*?)#endif",
        exit_body,
        re.S,
    )
    assert gated
    assert "if (sNamingScreen->compactThaiMode)" in gated.group("body")
    assert "SetVBlankCallback(NULL);" in gated.group("body")
    ordered(
        exit_body,
        "SetVBlankCallback(NULL);",
        "SetMainCallback2(sNamingScreen->returnCallback);",
        "DestroyTask(FindTaskIdByFunc(Task_NamingScreen));",
        "FreeAllWindowBuffers();",
        "FREE_AND_SET_NULL(sNamingScreen);",
    )


def test_exact_confirm_state_sequence_and_blank_contract() -> None:
    task = function_body(NAMING, "static void Task_NamingScreen(u8 taskId)")
    ordered(task, "case STATE_PRESSED_OK:", "case STATE_FADE_OUT:", "case STATE_EXIT:")
    pressed = function_body(NAMING, "static bool8 MainState_PressedOKButton(void)")
    ordered(pressed, "SaveThaiPrototypeInputText()", "sNamingScreen->state = STATE_FADE_OUT;")
    fade = function_body(NAMING, "static bool8 MainState_FadeOut(void)")
    ordered(fade, "BeginNormalPaletteFade", "sNamingScreen->state++;")
    save = function_body(NAMING, "static bool8 SaveThaiPrototypeInputText(void)")
    assert "if (ch == EOS)\n            break;" in save
    ordered(save, "ShapeThaiPrototypeText()", "SaveInputText();", "return TRUE;")
    legacy = function_body(NAMING, "static void SaveInputText(void)")
    assert "static void SaveInputText(void)" in NAMING
    assert "StringCopyN" in legacy


def test_callback_and_main_menu_initializer_contract() -> None:
    launch = function_body(MAIN_MENU, "static bool8 HandleMainMenuInput(u8 taskId)")
    assert "DoThaiNamingScreenPrototype(CB2_InitMainMenu);" in launch
    prototype = function_body(NAMING, "void DoThaiNamingScreenPrototype(MainCallback returnCallback)")
    assert "DoNamingScreen(NAMING_SCREEN_THAI_PROTOTYPE" in prototype
    do_naming = function_body(NAMING, "void DoNamingScreen(u8 templateNum")
    ordered(do_naming, "sNamingScreen->returnCallback = returnCallback;", "SetMainCallback2(CB2_LoadNamingScreen);")
    init = function_body(MAIN_MENU, "static u32 InitMainMenu(bool8 returningFromOptionsMenu)")
    ordered(
        init,
        "SetVBlankCallback(NULL);",
        "ResetTasks();",
        "InitWindows(sWindowTemplates_MainMenu);",
        "SetVBlankCallback(VBlankCB_MainMenu);",
        "SetMainCallback2(CB2_MainMenu);",
        "CreateTask(Task_MainMenuCheckSaveFile, 0);",
    )


def test_relaunch_clear_and_no_persistence() -> None:
    prototype = function_body(NAMING, "void DoThaiNamingScreenPrototype(MainCallback returnCallback)")
    ordered(
        prototype,
        "sThaiPrototypeScratch.guardLeft = THAI_PROTOTYPE_GUARD_LEFT;",
        "sThaiPrototypeScratch.text[i] = EOS;",
        "DoNamingScreen(NAMING_SCREEN_THAI_PROTOTYPE",
    )
    assert "gSaveBlock" not in prototype
    assert "SetMonData" not in prototype


TESTS = [
    test_engine_handoff_schedule,
    test_vblank_owns_naming_state,
    test_prototype_exit_relinquishes_vblank_before_free,
    test_exact_confirm_state_sequence_and_blank_contract,
    test_callback_and_main_menu_initializer_contract,
    test_relaunch_clear_and_no_persistence,
]


def main() -> None:
    for test in TESTS:
        test()
        print(f"PASS: {test.__name__}")
    print(f"PASS: {len(TESTS)} K3C-R3 regression groups")


if __name__ == "__main__":
    main()
