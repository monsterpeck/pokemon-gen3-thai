from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

THAI_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(THAI_DIR))

from build_thai_font import build_outputs, image_bytes, render_charmap
from thai_font import ROOT, load_registry, registry_errors, renderer_errors
from validate_thai_font import validate


class RegistryTests(unittest.TestCase):
    def test_duplicate_id_and_token_are_rejected(self):
        glyph = load_registry()[0]
        errors = registry_errors([glyph, replace(glyph, display="ข")])
        self.assertTrue(any("duplicate glyph ID" in error for error in errors))
        self.assertTrue(any("duplicate token" in error for error in errors))

    def test_invalid_width_is_rejected(self):
        glyph = replace(load_registry()[0], width=17)
        self.assertTrue(any("width must be 1..16" in error for error in registry_errors([glyph])))


class IntegrationTests(unittest.TestCase):
    def test_validator_passes(self):
        self.assertEqual(validate(), [])

    def test_builder_is_idempotent(self):
        first = build_outputs()
        second = build_outputs()
        self.assertEqual(image_bytes(first[0]), image_bytes(second[0]))
        self.assertEqual(first[1:], second[1:])

    def test_generated_charmap_has_no_hash_comments(self):
        glyphs = load_registry()
        output = render_charmap((ROOT / "charmap.txt").read_text(encoding="utf-8"), glyphs)
        self.assertFalse(any(line.lstrip().startswith("#") for line in output.splitlines()))
        for glyph in glyphs:
            self.assertEqual(output.count(f"{glyph.token} = "), 1)



if __name__ == "__main__":
    unittest.main()
