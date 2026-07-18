from __future__ import annotations

import csv
import sys
import unittest
from pathlib import Path

THAI_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(THAI_DIR))

from thai_shaper import METADATA, logical_width, shape


class CombiningRendererTests(unittest.TestCase):
    def test_required_acceptance_strings_are_mapped(self):
        with METADATA.open(newline="", encoding="utf-8") as handle:
            mapped = {row["char"] for row in csv.DictReader(handle)}
        for text in ("เริ่มเกมส์", "โปเกมอน", "ผู้เล่น", "น้ำ เก็บไว้", "ญี่ปุ่น", "ความสามารถ"):
            self.assertFalse({char for char in text if "\u0e00" <= char <= "\u0e7f"} - mapped)

    def test_base_advances(self):
        self.assertEqual(shape("ก")[0].advance, 14)

    def test_upper_lower_and_tone_have_zero_advance(self):
        for text in ("กิ", "กุ", "ก่", "ส์"):
            self.assertEqual(shape(text)[-1].advance, 0)

    def test_tone_stacks_above_upper_vowel(self):
        self.assertEqual(shape("กิ่")[-1].y, shape("ก่")[-1].y - 2)

    def test_sara_am_is_nikhahit_plus_spacing_aa(self):
        events = shape("นำ")
        self.assertEqual([event.component for event in events[-2:]], ["nikhahit", "sara_aa"])
        self.assertEqual([event.advance for event in events[-2:]], [0, 10])

    def test_leading_vowel_advances_before_base(self):
        self.assertEqual([event.x for event in shape("เก")], [0, 7])

    def test_space_and_newline_reset_base_state(self):
        for separator in (" ", "\n"):
            self.assertEqual(shape("ก" + separator + "ิ")[-1].x, logical_width("ก"))

    def test_non_thai_is_preserved(self):
        self.assertEqual([event.char for event in shape("ABC")], list("ABC"))

    def test_word_width_ignores_marks(self):
        self.assertEqual(logical_width("กิ่"), logical_width("ก"))

    def test_missing_base_mark_fallback_is_visible(self):
        event = shape("ิ")[0]
        self.assertEqual((event.x, event.y, event.advance), (0, 0, 4))

    def test_all_metadata_ids_are_extended(self):
        with METADATA.open(newline="", encoding="utf-8") as handle:
            ids = [int(row["glyph_id"], 0) for row in csv.DictReader(handle)]
        self.assertTrue(all(0x100 <= glyph_id <= 0x1FF for glyph_id in ids))


if __name__ == "__main__":
    unittest.main()
