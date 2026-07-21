#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MAP_PATH = ROOT / "tools/thai/font/thai_precompose_glyph_map.json"

CMD_BEGIN = 0xFC
CMD_ID = 0x19
COMMAND_SIZE = 8
Y_OFFSET = -12
FLAGS = 1

THAI_RE = re.compile(r"[\u0E00-\u0E7F]+")
STRING_RE = re.compile(r'"(?:\\.|[^"\\])*"')
EXPECTED_FORMAT = "pokemon-gen3-thai-precompose-full-v1"
EXPECTED_COUNT = 761


class PrecomposeError(ValueError):
    pass


def brace_bytes(data):
    return "".join("{%d}" % value for value in data)


def load_mapping():
    if not MAP_PATH.is_file():
        raise PrecomposeError(f"missing map: {MAP_PATH}")

    data = json.loads(MAP_PATH.read_text(encoding="utf-8"))
    glyphs = data.get("glyphs")

    if data.get("format") != EXPECTED_FORMAT:
        raise PrecomposeError(f"unexpected format: {data.get('format')!r}")
    if not isinstance(glyphs, list) or len(glyphs) != EXPECTED_COUNT:
        raise PrecomposeError(
            f"expected {EXPECTED_COUNT} glyphs, found "
            f"{len(glyphs) if isinstance(glyphs, list) else 'invalid'}"
        )
    if data.get("atlas_size") != [256, 768]:
        raise PrecomposeError(f"unexpected atlas size: {data.get('atlas_size')!r}")

    names = []
    indices = []

    for position, entry in enumerate(glyphs):
        name = entry.get("name")
        glyph_id = entry.get("target_index")
        advance = entry.get("advance")
        left = entry.get("left")

        if not isinstance(name, str) or not name:
            raise PrecomposeError(f"invalid name at glyph {position}")
        if not isinstance(glyph_id, int) or not 0 <= glyph_id <= 0xFFFF:
            raise PrecomposeError(f"invalid target_index for {name!r}")
        if not isinstance(advance, int) or not 0 <= advance <= 255:
            raise PrecomposeError(f"invalid advance for {name!r}")
        if not isinstance(left, int) or not -128 <= left <= 127:
            raise PrecomposeError(f"invalid left bearing for {name!r}")

        names.append(name)
        indices.append(glyph_id)

    if len(set(names)) != len(names):
        raise PrecomposeError("duplicate glyph names")
    if sorted(indices) != list(range(len(glyphs))):
        raise PrecomposeError("target indices are not continuous 0..N-1")

    return data


def lookup_for(mapping):
    lookup = {entry["name"]: entry for entry in mapping["glyphs"]}
    return lookup, max(map(len, lookup))


def tokenize(text, lookup, max_length):
    tokens = []
    position = 0

    while position < len(text):
        matched = None
        upper = min(len(text), position + max_length)

        for end in range(upper, position, -1):
            candidate = text[position:end]
            if candidate in lookup:
                matched = candidate
                break

        if matched is None:
            char = text[position]
            raise PrecomposeError(
                f"unsupported Thai sequence at character {position}: "
                f"{char!r} U+{ord(char):04X}; remaining={text[position:]!r}"
            )

        tokens.append(matched)
        position += len(matched)

    return tokens


def encode_run(text, mapping):
    lookup, max_length = lookup_for(mapping)
    tokens = tokenize(text, lookup, max_length)

    output = []
    records = []
    total = 0

    for token in tokens:
        entry = lookup[token]
        glyph_id = int(entry["target_index"])
        advance = int(entry["advance"])
        x_offset = int(entry["left"])

        command = [
            CMD_BEGIN,
            CMD_ID,
            glyph_id & 0xFF,
            (glyph_id >> 8) & 0xFF,
            x_offset & 0xFF,
            Y_OFFSET & 0xFF,
            advance,
            FLAGS,
        ]

        output.extend(command)
        total += advance
        records.append({
            "cluster": token,
            "glyph_id": glyph_id,
            "advance": advance,
            "x_offset": x_offset,
            "y_offset": Y_OFFSET,
            "flags": FLAGS,
            "bytes": command,
        })

    return bytes(output), records, total


def transform_literal(literal, mapping):
    body = literal[1:-1]

    def replace(match):
        encoded, _records, _total = encode_run(match.group(0), mapping)
        return brace_bytes(encoded)

    return '"' + THAI_RE.sub(replace, body) + '"'


def transform_source(source, mapping):
    def replace(match):
        literal = match.group(0)

        if not THAI_RE.search(literal):
            return literal

        prefix = source[:match.start()]
        line_prefix = prefix[prefix.rfind("\n") + 1:]

        project = bool(re.search(r"_\s*\([^)]*$", prefix[-4096:], re.S))
        assembly = bool(re.search(r"\.(?:string|ascii)\s*$", line_prefix))

        return transform_literal(literal, mapping) if project or assembly else literal

    return STRING_RE.sub(replace, source)


def check(mapping):
    encoded, records, total = encode_run("เริ่มเกมส์", mapping)
    tokens = [record["cluster"] for record in records]
    expected = ["เ", "ริ่", "ม", "เ", "ก", "ม", "ส์"]

    if tokens != expected:
        raise PrecomposeError(f"token mismatch: {tokens!r}")
    if total != 40:
        raise PrecomposeError(f"advance mismatch: {total}")
    if len(encoded) != len(expected) * COMMAND_SIZE:
        raise PrecomposeError("command length mismatch")

    print("Map format       :", mapping["format"])
    print("Glyph count      :", len(mapping["glyphs"]))
    print("Atlas size       :", mapping["atlas_size"])
    print("Start-game       :", " | ".join(tokens))
    print("Total advance    :", total)
    print("RESULT: PRECOMPOSE SHAPER CHECK PASSED")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--filter-source", nargs="?", const="-")
    parser.add_argument("--encode")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    mapping = load_mapping()

    if args.check:
        check(mapping)

    if args.encode is not None:
        encoded, records, total = encode_run(args.encode, mapping)
        print(encoded.hex(" "))
        print(json.dumps(
            {"advance": total, "glyphs": records},
            ensure_ascii=False,
            indent=2,
        ))

    if args.filter_source is not None:
        source = (
            sys.stdin.read()
            if args.filter_source == "-"
            else Path(args.filter_source).read_text(encoding="utf-8")
        )
        sys.stdout.write(transform_source(source, mapping))


if __name__ == "__main__":
    try:
        main()
    except PrecomposeError as exc:
        print(f"Thai precompose error: {exc}", file=sys.stderr)
        raise SystemExit(2)
