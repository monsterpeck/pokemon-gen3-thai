from __future__ import annotations

import sys
import unittest
from pathlib import Path

THAI_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(THAI_DIR))

from generate_glyph_candidates import PATTERNS, TARGET_IDS, VERSIONS, candidate_set
from install_glyph_candidate import install_cells
from thai_font import MASTER_PATH, open_indexed, tile_box


class CandidateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.master = open_indexed(MASTER_PATH)

    def test_six_complete_explicit_candidate_sets(self):
        self.assertEqual(VERSIONS, ("V01", "V02", "V03", "V04", "V05", "V06"))
        for version in VERSIONS:
            self.assertEqual(set(PATTERNS[version]), set(TARGET_IDS))
            self.assertTrue(all(PATTERNS[version][glyph_id] for glyph_id in TARGET_IDS))

    def test_candidates_are_native_indexed_palette_images(self):
        for version in VERSIONS:
            for tile in candidate_set(version, self.master).values():
                self.assertEqual(tile.size, (16, 16))
                self.assertEqual(tile.mode, "P")
                self.assertEqual(tile.getpalette(), self.master.getpalette())
                self.assertLessEqual(set(tile.getdata()), {0, 1, 2, 3})

    def test_base_consonant_pixels_are_unchanged(self):
        for version in VERSIONS:
            candidates = candidate_set(version, self.master)
            for target_id, base_id in ((0x146, 0x138), (0x147, 0x13D)):
                base = self.master.crop(tile_box(base_id))
                candidate = candidates[target_id]
                for y in range(16):
                    for x in range(16):
                        if base.getpixel((x, y)):
                            self.assertEqual(candidate.getpixel((x, y)), base.getpixel((x, y)))

    def test_installer_changes_only_target_cells(self):
        updated = install_cells(self.master, candidate_set("V03", self.master))
        for glyph_id in range(512):
            same = list(self.master.crop(tile_box(glyph_id)).getdata()) == list(updated.crop(tile_box(glyph_id)).getdata())
            self.assertEqual(same, glyph_id not in TARGET_IDS)


if __name__ == "__main__":
    unittest.main()
