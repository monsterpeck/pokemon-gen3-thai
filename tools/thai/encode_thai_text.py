#!/usr/bin/env python3
"""Encode Thai clusters in pokeemerald _("...") C string literals."""

from __future__ import annotations

import argparse
import difflib
import re
from pathlib import Path

from thai_font import ThaiToolError, load_registry, registry_errors


C_STRING_RE = re.compile(r'(_\(\s*")((?:\\.|[^"\\])*)("\s*\))')


def is_thai(character: str) -> bool:
    return "\u0e00" <= character <= "\u0e7f"


class ClusterEncoder:
    def __init__(self, glyphs=None):
        self.glyphs = glyphs if glyphs is not None else load_registry()
        errors = registry_errors(self.glyphs)
        if errors:
            raise ThaiToolError("\n".join(errors))
        self.matches = sorted(
            (g for g in self.glyphs if g.status != "unused"),
            key=lambda glyph: (-len(glyph.display), glyph.glyph_id),
        )

    def encode_content(self, content: str, source: str = "<string>") -> str:
        output = []
        index = 0
        while index < len(content):
            char = content[index]
            if char == "{":
                end = content.find("}", index + 1)
                if end < 0:
                    raise ThaiToolError(f"{source}:{index}: unterminated brace constant")
                output.append(content[index:end + 1])
                index = end + 1
                continue
            if char == "\\":
                if index + 1 >= len(content):
                    raise ThaiToolError(f"{source}:{index}: trailing escape")
                output.append(content[index:index + 2])
                index += 2
                continue
            if not is_thai(char):
                output.append(char)
                index += 1
                continue
            match = next((g for g in self.matches if content.startswith(g.display, index)), None)
            if match is None:
                codepoint = f"U+{ord(char):04X}"
                context = content[max(0, index - 4):index + 5]
                raise ThaiToolError(
                    f"{source}:{index}: unsupported Thai sequence at {codepoint} in {context!r}"
                )
            if len(match.display) == 1 and (match.kind == "base" or match.display == "า"):
                output.append(match.display)
            else:
                output.append("{" + match.token + "}")
            index += len(match.display)
        return "".join(output)

    def encode_source(self, text: str, source: str = "<source>") -> str:
        def replace(match: re.Match[str]) -> str:
            encoded = self.encode_content(match.group(2), source)
            return match.group(1) + encoded + match.group(3)
        return C_STRING_RE.sub(replace, text)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", type=Path)
    parser.add_argument("--text", help="encode one string instead of a file")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if (args.path is None) == (args.text is None):
        parser.error("provide exactly one of path or --text")
    try:
        encoder = ClusterEncoder()
        if args.text is not None:
            print(encoder.encode_content(args.text, "--text"))
            return 0
        original = args.path.read_text(encoding="utf-8")
        encoded = encoder.encode_source(original, str(args.path))
        if args.check:
            if encoded != original:
                print(f"{args.path}: contains unencoded Thai clusters")
                return 1
            print(f"{args.path}: Thai text is encoded")
            return 0
        if args.dry_run:
            print("".join(difflib.unified_diff(
                original.splitlines(True), encoded.splitlines(True),
                fromfile=str(args.path), tofile=str(args.path) + " (encoded)",
            )), end="")
            return 0
        destination = args.output or args.path
        destination.write_text(encoded, encoding="utf-8")
        print(f"wrote {destination}")
        return 0
    except (OSError, ThaiToolError) as error:
        print(f"error: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
