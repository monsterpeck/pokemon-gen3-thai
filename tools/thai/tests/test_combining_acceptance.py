from __future__ import annotations

import sys
import unittest
from pathlib import Path

THAI_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(THAI_DIR))

from thai_shaper import logical_width, shape


class CombiningAcceptanceTests(unittest.TestCase):
    def test_upper_vowel_zero_advance(self):
        self.assertEqual(shape("กิ")[-1].advance, 0)

    def test_lower_vowel_zero_advance(self):
        self.assertEqual(shape("กุ")[-1].advance, 0)

    def test_tone_zero_advance(self):
        self.assertEqual(shape("ก่")[-1].advance, 0)

    def test_thanthakhat_uses_tone_anchor(self):
        thanthakhat = shape("ส์")[-1]
        tone = shape("ส่")[-1]
        self.assertEqual((thanthakhat.x, thanthakhat.y), (tone.x, tone.y))

    def test_non_thai_spacing_resets_base(self):
        mark = shape("กAิ")[-1]
        self.assertEqual((mark.x, mark.y), (logical_width("ก"), 0))

    def test_no_stale_base_after_control_boundary(self):
        mark = shape("ก\n่")[-1]
        self.assertEqual((mark.x, mark.y), (logical_width("ก"), 0))

    def test_english_utf8_bytes_are_unaffected(self):
        source = "English text 123!"
        self.assertEqual("".join(event.char for event in shape(source)).encode("utf-8"), source.encode("utf-8"))


if __name__ == "__main__":
    unittest.main()
