from __future__ import annotations

import csv
import hashlib
import sys
import unittest
from pathlib import Path

THAI_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(THAI_DIR))

from thai_font import MASTER_PATH, ROOT, load_registry, open_indexed, palette_signature, tile_box
from thai_shaper import BASE_METRICS, METADATA, shape


class CombiningMetadataTests(unittest.TestCase):
    def metadata(self):
        with METADATA.open(newline="", encoding="utf-8") as handle:
            return list(csv.DictReader(handle))

    def test_every_base_has_explicit_metrics(self):
        with BASE_METRICS.open(newline="", encoding="utf-8") as handle:
            metric_ids = {int(row["glyph_id"], 0) for row in csv.DictReader(handle)}
        base_ids = {int(row["glyph_id"], 0) for row in self.metadata() if row["class"] == "BASE"}
        self.assertEqual(metric_ids, base_ids)

    def test_nikhahit_has_zero_advance(self):
        row = next(row for row in self.metadata() if row["class"] == "NIKHAHIT")
        self.assertEqual(int(row["advance"]), 0)

    def test_control_boundary_resets_state(self):
        mark = shape("ก\x1bิ")[-1]
        self.assertEqual((mark.y, mark.advance), (0, 4))

    def test_brace_constants_and_escapes_remain_in_charmap(self):
        charmap = (ROOT / "charmap.txt").read_text(encoding="utf-8")
        self.assertIn("COLOR = FC 01", charmap)
        self.assertIn("'\\n' = FE", charmap)

    def test_consonant_hash_manifest_matches_master(self):
        master = open_indexed(MASTER_PATH)
        with (ROOT / "tools/thai/font/consonant_hashes.csv").open(newline="", encoding="ascii") as handle:
            expected = {int(row["glyph_id"], 0): row["sha256"] for row in csv.DictReader(handle)}
        self.assertEqual(len(expected), 42)
        for glyph_id, digest in expected.items():
            actual = hashlib.sha256(bytes(master.crop(tile_box(glyph_id)).getdata())).hexdigest()
            self.assertEqual(actual, digest)

    def test_master_and_generated_font_keep_indexed_palette(self):
        master = open_indexed(MASTER_PATH)
        generated = open_indexed(ROOT / "graphics/fonts/latin_normal.png")
        self.assertEqual(palette_signature(master), palette_signature(generated))

    def test_every_active_registry_glyph_has_one_class(self):
        metadata_ids = [int(row["glyph_id"], 0) for row in self.metadata()]
        active_ids = [glyph.glyph_id for glyph in load_registry() if glyph.status != "unused"]
        self.assertEqual(sorted(metadata_ids), sorted(active_ids))
        self.assertEqual(len(metadata_ids), len(set(metadata_ids)))


if __name__ == "__main__":
    unittest.main()
