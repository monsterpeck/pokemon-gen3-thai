from __future__ import annotations

import hashlib
import sys
import unittest
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
THAI = ROOT / "tools/thai"
sys.path[:0] = [str(THAI), str(THAI / "cache/python")]

from noto_thai import PROOF_LINES
from production_shaping import bbox, clusters, role
from shape_thai_production import FONT_PNG, ISOLATION_LINES, MAP_PATH, build_font, encode_run, load_mapping, shape_run, transform_source
from thai_production_artifacts import LATFONT, ROM, validate


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class ThaiProductionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mapping = load_mapping()
        cls.sheet = Image.open(FONT_PNG)
        cls.sheet.load()

    def variants(self, gid):
        return {entry["variant"]: entry for entry in self.mapping["glyphs"] if entry["hb_glyph_id"] == gid}

    def test_plain_ro_and_so_remain_normal(self):
        for text, gid in (("\u0e40\u0e23\u0e21", 81), ("\u0e2a\u0e19", 110)):
            _data, records, _total = encode_run(text, self.mapping)
            record = next(item for item in records if item["glyph_id"] == gid)
            self.assertEqual(record["selected_variant"], "normal")
            self.assertEqual(record["original_compact_index"], record["selected_compact_index"])

    def test_contextual_selection_is_cluster_driven(self):
        _data, records, _total = encode_run("\u0e40\u0e23\u0e34\u0e48\u0e21", self.mapping)
        self.assertTrue(any(r["selected_variant"] != "normal" for r in records if r["cluster_analysis"]["above_count"] == 2))
        _data, records, _total = encode_run("\u0e40\u0e01\u0e21\u0e2a\u0e4c", self.mapping)
        self.assertTrue(all(r["selected_variant"] == "normal" for r in records) or any(r["normal_combined_top"] < 0 for r in records))

    def test_two_level_clusters_fit_and_compact_when_required(self):
        for text in ("\u0e40\u0e23\u0e34\u0e48\u0e21", "\u0e23\u0e35\u0e48", "\u0e19\u0e49\u0e33", "\u0e0d\u0e35\u0e48\u0e1b\u0e38\u0e48\u0e19"):
            _data, records, _total = encode_run(text, self.mapping)
            self.assertTrue(all(0 <= r["final_combined_top"] <= r["final_combined_bottom"] <= 15 for r in records))
            if any(r["normal_combined_top"] < 0 for r in records):
                self.assertTrue(any("compact" in r["selected_variant"] for r in records))

    def test_unique_deterministic_in_range_indexes(self):
        indexes = [entry["compact_index"] for entry in self.mapping["glyphs"]]
        self.assertEqual(indexes, list(range(len(indexes))))
        for text in (*PROOF_LINES, *ISOLATION_LINES):
            data, records, _total = encode_run(text, self.mapping)
            self.assertTrue(data)
            self.assertTrue(all(0 <= r["selected_compact_index"] < len(indexes) for r in records))

    def test_map_has_required_provenance(self):
        required = {"compact_index", "hb_glyph_id", "glyph_name", "variant", "source_cluster_class",
                    "source_bitmap_hash", "production_bitmap_hash", "palette_index_1_count",
                    "palette_index_2_count", "bitmap_bbox", "baseline", "contextual_shift_x",
                    "contextual_shift_y"}
        for entry in self.mapping["glyphs"]:
            self.assertLessEqual(required, set(entry))

    def test_palette_and_probes(self):
        validate(self.mapping, self.sheet)

    def test_harfbuzz_order_and_advances_unchanged(self):
        for text in PROOF_LINES:
            raw, raw_total = shape_run(text, self.mapping)
            _data, selected, selected_total = encode_run(text, self.mapping)
            self.assertEqual([r["glyph_id"] for r in raw], [r["glyph_id"] for r in selected])
            self.assertEqual([r["x_advance"] for r in raw], [r["x_advance"] for r in selected])
            self.assertEqual(raw_total, selected_total)

    def test_english_byte_identity_and_natural_source(self):
        english = 'const u8 s[] = _("English");'
        self.assertEqual(transform_source(english, self.mapping), english)
        self.assertIn("\u0e40\u0e23\u0e34\u0e48\u0e21\u0e40\u0e01\u0e21\u0e2a\u0e4c", (ROOT / "src/strings.c").read_text(encoding="utf-8"))

    def test_repeated_generation_is_deterministic(self):
        before = digest(FONT_PNG), digest(MAP_PATH)
        build_font()
        self.assertEqual(before, (digest(FONT_PNG), digest(MAP_PATH)))

    def test_runtime_has_no_new_thai_grammar(self):
        source = (ROOT / "src/text.c").read_text(encoding="utf-8")
        start = source.index("static u16 RenderThaiPositionedGlyph", source.index("static u16 RenderThaiPositionedGlyph") + 1)
        body = source[start:source.index("static u16 RenderText(", start)]
        for term in ("cluster", "upper", "tone", "HarfBuzz"):
            self.assertNotIn(term, body)

    def test_physical_asset_and_rom_when_present(self):
        if LATFONT.exists():
            self.assertEqual(LATFONT.stat().st_size, self.sheet.width // 16 * self.sheet.height // 16 * 64)
        if LATFONT.exists() and ROM.exists():
            self.assertTrue(ROM.stat().st_mtime < LATFONT.stat().st_mtime or LATFONT.read_bytes() in ROM.read_bytes())


if __name__ == "__main__":
    unittest.main()
