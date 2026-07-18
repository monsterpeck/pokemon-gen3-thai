#!/usr/bin/env python3
"""Encode and verify the normal-source Thai New Game menu fixture."""

from __future__ import annotations

from pathlib import Path

from encode_thai_text import C_STRING_RE, ClusterEncoder, is_thai
from thai_font import ROOT, ThaiToolError


SOURCE = ROOT / "tools/thai/testdata/thai_menu_source.c"
OUTPUT = ROOT / "tools/thai/generated/thai_menu_encoded.c"
EXPECTED = (
    "{THAI_SARA_E}{THAI_RO_RUEA_SARA_I_MAI_EK}ม"
    "{THAI_SARA_E}กม{THAI_SO_SUEA_THANTHAKHAT}"
)


def verify_menu_source(source_path: Path = SOURCE, output_path: Path = OUTPUT) -> str:
    source = source_path.read_text(encoding="utf-8")
    matches = list(C_STRING_RE.finditer(source))
    if len(matches) != 1 or matches[0].group(2) != "เริ่มเกมส์":
        raise ThaiToolError(f"{source_path}: expected exactly one _(\"เริ่มเกมส์\") fixture")
    encoded = ClusterEncoder().encode_source(source, str(source_path))
    encoded_match = C_STRING_RE.search(encoded)
    if encoded_match is None or encoded_match.group(2) != EXPECTED:
        raise ThaiToolError("menu encoding did not produce the expected token sequence")
    residual = "".join(
        character for character in encoded_match.group(2)
        if is_thai(character) and character not in "กม"
    )
    if residual:
        codepoints = " ".join(f"U+{ord(character):04X}" for character in residual)
        raise ThaiToolError(f"unsupported Thai cluster content remains: {codepoints}")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(encoded, encoding="utf-8")
    return encoded


def main() -> int:
    try:
        verify_menu_source()
        print(f"Thai menu source encoded and verified: {OUTPUT}")
        print(EXPECTED)
        return 0
    except (OSError, ThaiToolError) as error:
        print(f"error: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
