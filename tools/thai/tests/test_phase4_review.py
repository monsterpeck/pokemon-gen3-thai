from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image

THAI_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(THAI_DIR))

from export_review_sheet import SHEET_SIZE, expected_review_sheet, target_box
from import_review_sheet import import_review_sheet, review_errors
from test_thai_menu import EXPECTED, verify_menu_source
from thai_font import MASTER_PATH, open_indexed


class ReviewSheetTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.directory = Path(self.temporary.name)
        self.master_path = self.directory / "master.png"
        self.review_path = self.directory / "review.png"
        master = open_indexed(MASTER_PATH)
        master.save(self.master_path, optimize=False)
        expected_review_sheet(master).save(self.review_path, optimize=False)

    def tearDown(self):
        self.temporary.cleanup()

    def test_review_sheet_round_trip(self):
        self.assertEqual(import_review_sheet(self.review_path, self.master_path, check=True), [])
        self.assertEqual(review_errors(self.review_path, self.master_path), [])

    def test_palette_is_preserved(self):
        master = open_indexed(self.master_path)
        review = open_indexed(self.review_path)
        self.assertEqual(review.mode, "P")
        self.assertEqual(review.getpalette(), master.getpalette())
        self.assertEqual(review.size, SHEET_SIZE)

    def test_reference_cell_is_immutable(self):
        review = open_indexed(self.review_path)
        review.putpixel((3 * 16 + 2, 2), (review.getpixel((3 * 16 + 2, 2)) + 1) % 4)
        review.save(self.review_path, optimize=False)
        self.assertTrue(any("reference cell changed" in error for error in review_errors(self.review_path, self.master_path)))

    def test_edited_target_is_detected(self):
        review = open_indexed(self.review_path)
        x, y = 2, 8
        review.putpixel((x, y), (review.getpixel((x, y)) + 1) % 4)
        review.save(self.review_path, optimize=False)
        self.assertEqual(import_review_sheet(self.review_path, self.master_path, check=True), [0x145])

    def test_antialiased_rgb_image_is_rejected(self):
        Image.open(self.review_path).convert("RGB").save(self.review_path)
        self.assertTrue(any("expected indexed mode P" in error for error in review_errors(self.review_path, self.master_path)))


class ThaiMenuTests(unittest.TestCase):
    def test_expected_normal_source_encoding(self):
        source = self.directory / "menu.c" if hasattr(self, "directory") else None
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "menu.c"
            output = Path(directory) / "encoded.c"
            source.write_text('const u8 x[] = _("เริ่มเกมส์");\n', encoding="utf-8")
            encoded = verify_menu_source(source, output)
            self.assertIn(EXPECTED, encoded)
            self.assertEqual(output.read_text(encoding="utf-8"), encoded)


if __name__ == "__main__":
    unittest.main()
