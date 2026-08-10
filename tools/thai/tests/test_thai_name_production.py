#!/usr/bin/env python3

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "src/thai_name.c"
HEADER = ROOT / "include/thai_name.h"
RUNTIME_MAP = ROOT / "src/data/thai_naming_runtime_map.inc"

EOS = 0xFF
CHAR_SPACE = 0x00
EXT_CTRL_CODE_BEGIN = 0xFC
EXT_CTRL_CODE_THAI_POSITIONED_GLYPH = 0x19

PLAYER_NAME_LENGTH = 7
BOX_NAME_LENGTH = 8
POKEMON_NAME_LENGTH = 10
SHAPED_CAPACITY = POKEMON_NAME_LENGTH * 8 + 1


def parse_runtime_map():
    entries = []

    for lineno, line in enumerate(
        RUNTIME_MAP.read_text(encoding="utf-8").splitlines(), 1
    ):
        m = re.match(
            r"\s*\{\{([^}]*)\},\s*(\d+),\s*(\d+),\s*(-?\d+),\s*(-?\d+),\s*(\d+),\s*(\d+)\}",
            line,
        )
        if not m:
            continue

        raw_key = [
            int(x, 16)
            for x in re.findall(r"0x[0-9A-Fa-f]+", m.group(1))
        ]

        length = int(m.group(2))
        entries.append(
            {
                "line": lineno,
                "key": tuple(raw_key[:length]),
                "length": length,
                "glyph": int(m.group(3)),
                "x": int(m.group(4)),
                "y": int(m.group(5)),
                "advance": int(m.group(6)),
                "flags": int(m.group(7)),
            }
        )

    return entries


ENTRIES = parse_runtime_map()


def is_compact_id(value):
    return (
        0x37 <= value <= 0x50
        or 0x5E <= value <= 0x67
        or 0x69 <= value <= 0x6E
        or 0x70 <= value <= 0x76
        or value == 0x78
        or 0x7D <= value <= 0x83
        or 0x87 <= value <= 0x8E
    )


def shape(source, length, max_chars, destination_capacity):
    if source is None:
        return None

    if max_chars > POKEMON_NAME_LENGTH or length > max_chars:
        return None

    if length > len(source):
        return None

    out = []
    pos = 0

    while pos < length:
        ch = source[pos]

        if ch == CHAR_SPACE:
            if len(out) + 1 >= SHAPED_CAPACITY:
                return None
            out.append(CHAR_SPACE)
            pos += 1
            continue

        if not is_compact_id(ch):
            return None

        match = None
        remaining = length - pos

        for entry in ENTRIES:
            if entry["length"] > remaining:
                continue

            if tuple(source[pos:pos + entry["length"]]) == entry["key"]:
                match = entry
                break

        if match is None:
            return None

        if len(out) + 8 >= SHAPED_CAPACITY:
            return None

        glyph = match["glyph"]

        out.extend(
            [
                EXT_CTRL_CODE_BEGIN,
                EXT_CTRL_CODE_THAI_POSITIONED_GLYPH,
                glyph & 0xFF,
                (glyph >> 8) & 0xFF,
                match["x"] & 0xFF,
                match["y"] & 0xFF,
                match["advance"],
                match["flags"],
            ]
        )

        pos += match["length"]

    out.append(EOS)

    if len(out) > destination_capacity:
        return None

    return bytes(out)


def first_single_key():
    for entry in ENTRIES:
        if entry["length"] == 1:
            return entry["key"][0]
    raise AssertionError("No single-byte runtime-map key")


def test_source_contract():
    source = SOURCE.read_text(encoding="utf-8")
    header = HEADER.read_text(encoding="utf-8")

    assert "#ifdef THAI_NAMING_PRODUCTION" in source
    assert "#ifdef THAI_NAMING_PRODUCTION" in header

    assert "THAI_NAME_MAX_SOURCE_LENGTH POKEMON_NAME_LENGTH" in header
    assert "THAI_NAME_SHAPED_CAPACITY ((THAI_NAME_MAX_SOURCE_LENGTH * 8) + 1)" in header

    assert "source[length] != EOS" not in source
    assert "maxChars > THAI_NAME_MAX_SOURCE_LENGTH" in source
    assert "length > maxChars" in source


def test_runtime_map_contract():
    assert len(ENTRIES) == 758
    assert max(e["length"] for e in ENTRIES) <= 7

    violations = []

    for short_i, short in enumerate(ENTRIES):
        for long_i, long in enumerate(ENTRIES):
            if long["length"] <= short["length"]:
                continue

            if long["key"][:short["length"]] == short["key"]:
                if short_i < long_i:
                    violations.append((short["line"], long["line"]))

    assert violations == []


def test_player_7():
    key = first_single_key()
    src = [key] * PLAYER_NAME_LENGTH

    out = shape(
        src,
        PLAYER_NAME_LENGTH,
        PLAYER_NAME_LENGTH,
        SHAPED_CAPACITY,
    )

    assert out is not None
    assert out[-1] == EOS
    assert len(out) == PLAYER_NAME_LENGTH * 8 + 1


def test_box_8():
    key = first_single_key()
    src = [key] * BOX_NAME_LENGTH

    out = shape(
        src,
        BOX_NAME_LENGTH,
        BOX_NAME_LENGTH,
        SHAPED_CAPACITY,
    )

    assert out is not None
    assert out[-1] == EOS
    assert len(out) == BOX_NAME_LENGTH * 8 + 1


def test_pokemon_10_without_eos():
    key = first_single_key()

    # Exactly 10 raw bytes. No EOS byte exists in this source field.
    src = [key] * POKEMON_NAME_LENGTH

    assert len(src) == 10
    assert EOS not in src

    out = shape(
        src,
        POKEMON_NAME_LENGTH,
        POKEMON_NAME_LENGTH,
        SHAPED_CAPACITY,
    )

    assert out is not None
    assert len(out) == 81
    assert out[-1] == EOS


def test_spaces():
    src = [CHAR_SPACE] * POKEMON_NAME_LENGTH

    out = shape(
        src,
        POKEMON_NAME_LENGTH,
        POKEMON_NAME_LENGTH,
        SHAPED_CAPACITY,
    )

    assert out == bytes([CHAR_SPACE] * 10 + [EOS])


def test_invalid_compact_id():
    assert shape(
        [0xBB],
        1,
        PLAYER_NAME_LENGTH,
        SHAPED_CAPACITY,
    ) is None


def test_length_over_max():
    key = first_single_key()

    assert shape(
        [key] * 8,
        8,
        PLAYER_NAME_LENGTH,
        SHAPED_CAPACITY,
    ) is None


def test_max_chars_over_production_limit():
    key = first_single_key()

    assert shape(
        [key],
        1,
        POKEMON_NAME_LENGTH + 1,
        SHAPED_CAPACITY,
    ) is None


def test_destination_too_small():
    key = first_single_key()
    src = [key] * POKEMON_NAME_LENGTH

    assert shape(
        src,
        POKEMON_NAME_LENGTH,
        POKEMON_NAME_LENGTH,
        80,
    ) is None

    assert shape(
        src,
        POKEMON_NAME_LENGTH,
        POKEMON_NAME_LENGTH,
        81,
    ) is not None


TESTS = [
    test_source_contract,
    test_runtime_map_contract,
    test_player_7,
    test_box_8,
    test_pokemon_10_without_eos,
    test_spaces,
    test_invalid_compact_id,
    test_length_over_max,
    test_max_chars_over_production_limit,
    test_destination_too_small,
]


if __name__ == "__main__":
    for test in TESTS:
        test()
        print(f"PASS: {test.__name__}")

    print(f"PASS: {len(TESTS)} production Thai-name contract groups")
