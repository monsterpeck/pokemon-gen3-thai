import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EOS, SPACE = 0xFF, 0x00


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


generator = load("runtime_generator", ROOT / "tools/thai/generate_thai_naming_runtime_map.py")
production = load("production_shaper", ROOT / "tools/thai/shape_thai_precompose.py")
mapping = production.load_mapping()
entries = generator.load_entries()
to_compact = {value: key for key, value in generator.COMPACT_TO_CANONICAL.items()}


def compact(text):
    return bytes(SPACE if char == " " else to_compact[char] for char in text)


def runtime_shape(source):
    output, position = bytearray(), 0
    while position < len(source):
        if source[position] == SPACE:
            output.append(SPACE)
            position += 1
            continue
        match = next((e for e in entries
                      if tuple(source[position:position + len(e["key"])]) == e["key"]), None)
        if match is None:
            raise ValueError("unsupported compact sequence")
        output += bytes((0xFC, 0x19, match["glyph"] & 255, match["glyph"] >> 8,
                         match["x"] & 255, 0xF4, match["advance"], 1))
        position += len(match["key"])
    return bytes(output + bytes((EOS,)))


def production_shape(text):
    output = bytearray()
    for index, run in enumerate(text.split(" ")):
        if index:
            output.append(SPACE)
        if run:
            output += production.encode_run(run, mapping)[0]
    return bytes(output + bytes((EOS,)))


def width(data):
    total = position = 0
    while data[position] != EOS:
        if data[position:position + 2] == b"\xFC\x19":
            total += data[position + 6]
            position += 8
        elif data[position] == SPACE:
            position += 1
        else:
            raise AssertionError("non-FC19 runtime byte")
    return total


def test_gate_and_provenance():
    gate = Path.home() / ".local/share/pekeemerald/thai-naming-keyboard/k3c_gate0_precompose_reproducibility_v2.json"
    assert json.loads(gate.read_text(encoding="utf-8"))["pass"] is True
    assert generator.hashlib.sha256(generator.MAP_PATH.read_bytes()).hexdigest() == generator.EXPECTED_SHA256
    assert generator.OUTPUT_PATH.read_text(encoding="utf-8") == generator.render(entries)


def test_all_reachable_clusters_match_production_records_and_widths():
    keys = [entry["key"] for entry in entries]
    assert len(keys) == len(set(keys)) == 758
    for entry in entries:
        actual = runtime_shape(bytes(entry["key"]))
        assert actual == production_shape(entry["name"])
        assert width(actual) == entry["advance"]
        assert entry["glyph"] < 761


def test_required_corpus_and_deletion_prefixes():
    corpus = ["ก", "กา", "เก", "กิ", "กุ", "กิ่", "กำ", "กั่",
              "เริ่ม", "ญี่ปุ่น", "รู้", "สู้", "ผู้"]
    for text in corpus:
        assert runtime_shape(compact(text)) == production_shape(text)
    for text in ("เริ่ม", "ญี่ปุ่น", "รู้", "สู้", "ผู้"):
        for end in range(len(text) + 1):
            try:
                expected = production_shape(text[:end])
            except production.PrecomposeError:
                continue
            assert runtime_shape(compact(text[:end])) == expected


def test_invalid_ordering_has_no_direct_font_fallback():
    for text in ("ั", "ิ", "ุ", "่", "้", "์", "ํ", "ฯ", "กิิ", "กุิ", "่ก"):
        try:
            runtime_shape(compact(text))
        except (ValueError, KeyError):
            continue
        raise AssertionError(f"invalid sequence accepted: {text}")


def test_capacity_guards_backspace_and_relaunch_model():
    source = bytearray([0xA6] + [EOS] * 8 + [0x6A])
    shaped = bytearray([0xA6] + [0xCC] * 57 + [0x6A])
    for index in range(7):
        source[index + 1] = to_compact["ก"]
        result = runtime_shape(bytes(source[1:index + 2]))
        shaped[1:1 + len(result)] = result
    before = bytes(source), bytes(shaped), width(result)
    assert source[8] == EOS and (bytes(source), bytes(shaped), width(result)) == before
    assert source[0] == shaped[0] == 0xA6 and source[-1] == shaped[-1] == 0x6A
    for index in range(7, 0, -1):
        source[index] = EOS
        runtime_shape(bytes(source[1:index]))
    assert source[1:9] == bytes((EOS,)) * 8
    source[1:9] = bytes((EOS,)) * 8
    assert source[1] == EOS


def test_static_labels_compile_independently_to_fc19():
    source = (ROOT / "src/naming_screen.c").read_text(encoding="utf-8")
    assert "THAI_LABEL_GLYPH" not in source
    labels = re.findall(r'sThaiPrototypeLabel_\d+\[\] = _\("([^"]+)"\);', source)
    assert len(labels) == 65
    for label in labels:
        encoded, records, _ = production.encode_run(label, mapping)
        assert encoded.startswith(b"\xFC\x19") and records
        assert all(record["glyph_id"] < 761 for record in records)
    assert "sThaiPrototypeKeyboardText[page][i][j]" in source
    assert "GetThaiPrototypeKeyCellCenterX(j)" in source
    assert "GetStringWidth(FONT_NORMAL, label, 0) / 2" in source
    assert "TEXT_SKIP_DRAW, label" in source


def test_preview_caret_scratch_gate_and_help_trace():
    naming = (ROOT / "src/naming_screen.c").read_text(encoding="utf-8")
    text = (ROOT / "src/text.c").read_text(encoding="utf-8")
    assert "sNamingScreen->shapedText, x, 1" in naming
    assert "GetStringWidth(FONT_NORMAL, sNamingScreen->shapedText, 0)" in naming
    assert "ThaiShapeCompactPrototype" in naming
    assert "IsThaiCompactPrototypeMode" not in text and "ThaiCompactPrototypeIdToGlyph" not in text
    prototype = naming.split("void DoThaiNamingScreenPrototype", 1)[1].split("#endif", 1)[0]
    assert "sThaiPrototypeScratch.text" in prototype
    assert not any(value in prototype for value in ("gSaveBlock", "SetMonData", "GetBoxNamePtr"))
    assert "IsStringJapanese" not in naming
    assert "FONT_SMALL" in naming and "gText_MoveOkBack" in naming
    help_line = next(line for line in (ROOT / "src/strings.c").read_text(encoding="utf-8").splitlines()
                     if "gText_MoveOkBack[]" in line)
    assert help_line.count("{252}{25}") == 11


def test_legacy_save_and_pressed_ok_flow_are_compile_time_unchanged():
    naming = (ROOT / "src/naming_screen.c").read_text(encoding="utf-8")
    assert "static void SaveInputText(void);" in naming
    assert "static bool8 SaveInputText(void)" not in naming
    assert re.search(r"#ifdef THAI_NAMING_KEYBOARD_K3C\nstatic bool8 SaveThaiPrototypeInputText\(void\);\n#endif", naming)

    legacy_save = re.search(
        r"static void SaveInputText\(void\)\n\{.*?\n\}\n\n#ifdef THAI_NAMING_KEYBOARD_K3C",
        naming,
        re.DOTALL,
    )
    assert legacy_save
    legacy_save_body = legacy_save.group(0).split("#ifdef", 1)[0]
    assert "Thai" not in legacy_save_body
    assert "return TRUE" not in legacy_save_body

    pressed_ok = re.search(
        r"static bool8 MainState_PressedOKButton\(void\)\n\{(.*?)\n\}\n\nstatic bool8 MainState_FadeOut",
        naming,
        re.DOTALL,
    )
    assert pressed_ok
    body = pressed_ok.group(1)
    gate = re.search(r"#ifdef THAI_NAMING_KEYBOARD_K3C.*?#endif\n", body, re.DOTALL)
    assert gate and "SaveThaiPrototypeInputText()" in gate.group(0)
    legacy_body = body[:gate.start()] + body[gate.end():]
    assert legacy_body.lstrip().startswith("SaveInputText();\n    SetInputState(INPUT_STATE_DISABLED);")


if __name__ == "__main__":
    tests = [value for name, value in globals().items() if name.startswith("test_")]
    for test in tests:
        test()
    print(f"{len(tests)} K3C tests passed; {len(entries)} reachable clusters checked")
