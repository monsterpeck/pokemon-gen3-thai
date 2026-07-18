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
from encode_thai_text import ClusterEncoder
from thai_font import Glyph, ROOT, ThaiToolError, load_registry, registry_errors, renderer_errors
from validate_thai_font import validate


class EncoderTests(unittest.TestCase):
    def test_longest_match_and_expected_menu_text(self):
        result = ClusterEncoder().encode_content("เริ่มเกมส์")
        self.assertEqual(
            result,
            "{THAI_SARA_E}{THAI_RO_RUEA_SARA_I_MAI_EK}ม"
            "{THAI_SARA_E}กม{THAI_SO_SUEA_THANTHAKHAT}",
        )

    def test_existing_constants_and_escapes_are_preserved(self):
        source = r'const u8 x[] = _("{COLOR RED}ก\\n{PLAYER}");'
        self.assertEqual(ClusterEncoder().encode_source(source), source)

    def test_only_wrapped_c_strings_are_processed(self):
        source = 'const char *a = "เริ่ม"; const u8 b[] = _("เริ่ม");'
        result = ClusterEncoder().encode_source(source)
        self.assertIn('"เริ่ม"', result)
        self.assertIn('{THAI_SARA_E}{THAI_RO_RUEA_SARA_I_MAI_EK}ม', result)

    def test_unsupported_cluster_has_codepoint(self):
        with self.assertRaisesRegex(ThaiToolError, "U\\+0E35"):
            ClusterEncoder().encode_content("กี")

    def test_longest_match_beats_single_character(self):
        glyphs = [
            Glyph(1, "A", "ก", "base", 1, "final", "test"),
            Glyph(2, "AB", "กิ", "cluster", 1, "final", "test"),
        ]
        self.assertEqual(ClusterEncoder(glyphs).encode_content("กิ"), "{AB}")


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

    def test_renderer_baseline_is_clean(self):
        self.assertEqual(renderer_errors(), [])


if __name__ == "__main__":
    unittest.main()
