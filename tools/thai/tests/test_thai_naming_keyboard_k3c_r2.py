import ast
import hashlib
import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SOURCE_PATH = ROOT / "src/naming_screen.c"
SNAPSHOT_PATH = Path.home() / ".local/share/pekeemerald/thai-naming-keyboard/k3c_r2_preflight_snapshot.json"
R2_ALLOWLIST = {
    "src/naming_screen.c",
    "tools/thai/tests/test_thai_naming_keyboard_k3c.py",
    "tools/thai/tests/test_thai_naming_keyboard_k3c_r2.py",
    "tools/thai/generated/thai_naming_keyboard_k3c_r2_result.md",
    "tools/thai/generated/thai_naming_keyboard_k3c_r2_result.json",
}


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


generator = load("runtime_generator_r2", ROOT / "tools/thai/generate_thai_naming_runtime_map.py")
COMPACT_TO_CANONICAL = generator.COMPACT_TO_CANONICAL


def source_text():
    return SOURCE_PATH.read_text(encoding="utf-8")


def initializer(source, name):
    match = re.search(rf"static const u8 (?:\*const )?{name}.*?=\s*\n(\{{.*?\n\}});", source, re.DOTALL)
    assert match, name
    return match.group(1)


def parse_cells():
    source = source_text()
    labels = dict((int(index), text) for index, text in
                  re.findall(r'sThaiPrototypeLabel_(\d+)\[\] = _\("([^"]+)"\);', source))
    text_init = initializer(source, "sThaiPrototypeKeyboardText")
    text_tokens = re.findall(r"sThaiPrototypeLabel_(\d+)|NULL", text_init)
    display = [labels[int(token)] if token else None for token in text_tokens]
    assert len(display) == 3 * 4 * 8

    chars_init = initializer(source, "sThaiPrototypeKeyboardChars")
    tokens = re.findall(r"0x[0-9A-Fa-f]+|EOS", chars_init)
    payload = [None if token == "EOS" else COMPACT_TO_CANONICAL[int(token, 16)] for token in tokens]
    assert len(payload) == 3 * 4 * 8
    return display, payload


def test_pre_r2_snapshot_protection():
    snapshot = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))
    assert snapshot["preflight_pass"] is True
    assert snapshot["head"] == "823533c16e5a2e5a198b48a87c96d5c662b09a5b"
    for relative, record in snapshot["files"].items():
        if relative in R2_ALLOWLIST:
            continue
        actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
        assert actual == record["sha256"], relative


def test_complete_65_cell_label_payload_contract():
    display, payload = parse_cells()
    reachable = [(index // 32, index % 32 // 8, index % 8, label, payload[index])
                 for index, label in enumerate(display) if label is not None]
    assert len(reachable) == 65
    assert sum(value is not None for value in payload) == 65
    for page, row, col, label, value in reachable:
        # Carrier labels intentionally visualize standalone combining payloads.
        if value not in "ัิีึืุู่้๊๋็์ํำ":
            assert label == value, (page, row, col, label, value)
    for index, label in enumerate(display):
        assert (label is None) == (payload[index] is None)
    assert all(display[col] == payload[col] for col in range(8))
    assert all(display[32 + col] == payload[32 + col] for col in range(8))
    assert display[64] == payload[64] == "ๆ"


def test_unified_center_coordinate_contract_and_shaped_width_centering():
    source = source_text()
    assert "#define THAI_KEY_CELL_CENTER_OFFSET 14" in source
    assert "sPageColumnXPos[KEYBOARD_LETTERS_UPPER][column] + THAI_KEY_CELL_CENTER_OFFSET" in source
    assert "GetThaiPrototypeKeyCellCenterX(x) + sWindowTemplates[WIN_KB_PAGE_1].tilemapLeft * 8" in source
    assert re.search(r"GetThaiPrototypeKeyCellCenterX\(j\)\s*\n\s*- GetStringWidth\(FONT_NORMAL, label, 0\) / 2", source)
    column_offsets = [0, 12, 24, 56, 68, 80, 92, 123]
    window_origin = 3 * 8
    for offset in column_offsets:
        label_screen_center = window_origin + offset + 14
        cursor_screen_center = offset + 38
        assert label_screen_center == cursor_screen_center


def test_empty_cells_are_unselectable_and_navigation_is_deterministic():
    source = source_text()
    assert "&& sThaiPrototypeKeyboardText[page][row][column] != NULL" in source
    assert "&& sThaiPrototypeKeyboardChars[page][row][column] != EOS" in source
    assert "!IsThaiPrototypeKeyCell(CurrentPageToKeyboardId(), cursorX, cursorY)" in source
    assert "!IsThaiPrototypeKeyCell(CurrentPageToKeyboardId(), x, y)" in source
    display, payload = parse_cells()
    assert all(value is None for value in display[65:])
    assert all(value is None for value in payload[65:])


def test_printers_render_immediately_without_dma_backlog():
    source = source_text()
    prototype = re.search(
        r"static void PrintKeyboardKeys\(u8 window, u8 page\)\n\{(.*?)\n\}",
        source,
        re.DOTALL,
    ).group(1)
    assert "TEXT_SKIP_DRAW, label" in prototype
    assert prototype.count("CopyWindowToVram(window, COPYWIN_GFX);") == 1
    assert ", 0, label" not in prototype
    text_source = (ROOT / "src/text.c").read_text(encoding="utf-8")
    assert "if (speed != TEXT_SKIP_DRAW)\n            CopyWindowToVram" in text_source
    assert "sTextPrinters[printerTemplate->windowId].active = FALSE;" in text_source


if __name__ == "__main__":
    tests = [value for name, value in globals().items() if name.startswith("test_")]
    for test in tests:
        test()
    print(f"{len(tests)} K3C-R2 tests passed; 65 reachable key cells checked")
