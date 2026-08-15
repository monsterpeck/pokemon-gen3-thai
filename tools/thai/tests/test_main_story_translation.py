import csv
import json
import subprocess
import unittest
from collections import Counter

from tools.thai import validate_main_story_translation as validate


def rows(path):
    return validate.read_csv(path)


class MainStoryTranslationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = rows(validate.SOURCE)
        cls.master = rows(validate.MASTER)
        cls.batch = rows(validate.BATCH)
        cls.ids = [row["id"] for row in cls.source]

    def test_complete_preservation_ids_and_order(self):
        self.assertEqual(len(self.master), 261)
        self.assertEqual([r["id"] for r in self.master], self.ids)
        self.assertEqual([r["id"] for r in self.batch], self.ids)
        self.assertEqual([int(r["global_order"]) for r in self.master], list(range(1, 262)))

    def test_english_and_source_metadata_preserved(self):
        for source, translated in zip(self.source, self.master):
            self.assertEqual({k: source[k] for k in validate.SOURCE_FIELDS},
                             {k: translated[k] for k in validate.SOURCE_FIELDS})

    def test_placeholders_and_controls_preserved(self):
        for row in self.master:
            self.assertEqual(validate.PLACEHOLDER_RE.findall(row["english_raw"]), validate.PLACEHOLDER_RE.findall(row["thai"]))
            self.assertEqual(validate.required_controls(row["english_raw"]), validate.required_controls(row["thai"]))
            for code in (r"\n", r"\l"):
                self.assertEqual(validate.controls(row["english_raw"]).count(code), validate.controls(row["thai"]).count(code))

    def test_translation_review_values(self):
        self.assertTrue(all(r["thai"].strip() and r["translation_status"] == "draft_review" for r in self.master))
        self.assertTrue(all(r["translation_confidence"] in {"high", "medium", "low"} for r in self.master))
        self.assertTrue(all(r["term_review"] in {"ok", "review"} for r in self.master))
        self.assertTrue(all(r["length_review"] in {"ok", "review_long_line", "review_long_page", "review_control_codes"} for r in self.master))

    def test_glossary_keys_and_spelling_unique(self):
        glossary = rows(validate.TRANS / "glossary.csv")
        keys = [r["english"].strip().casefold() for r in glossary]
        self.assertEqual(len(keys), len(set(keys)))
        self.assertEqual(len({(k, r["thai"]) for k, r in zip(keys, glossary)}), len(glossary))

    def test_translation_memory_conflicts_documented(self):
        grouped = {}
        for row in rows(validate.TRANS / "translation_memory.csv"):
            key = row["english_normalized"]
            if key in grouped and grouped[key] != row["thai"]:
                self.assertTrue(row["context_variants"].strip() or row["status"] == "review")
            grouped[key] = row["thai"]

    def test_recurring_speaker_styles(self):
        guided = {r["speaker"] for r in rows(validate.TRANS / "speaker_style_guide.csv")}
        recurring = {k for k, v in Counter(r["speaker"] for r in self.master if r["speaker"]).items() if v > 1}
        self.assertLessEqual(recurring, guided)

    def test_length_review_complete(self):
        length = rows(validate.TRANS / "main_story_length_review.csv")
        self.assertEqual([r["id"] for r in length], self.ids)
        self.assertEqual(len(length), 261)

    def test_map_and_chapter_splits_complete(self):
        self.assertEqual(validate.split_rows(validate.TRANS / "maps"), self.master)
        self.assertEqual(validate.split_rows(validate.TRANS / "chapters"), self.master)

    def test_review_coverage(self):
        self.assertEqual(validate.review_ids(validate.TRANS / "reviews/main_story_translation_review.md"), self.ids)
        map_ids = [item for p in sorted((validate.TRANS / "reviews/maps").glob("*.md")) for item in validate.review_ids(p)]
        chapter_ids = [item for p in sorted((validate.TRANS / "reviews/chapters").glob("*.md")) for item in validate.review_ids(p)]
        self.assertEqual(map_ids, self.ids)
        self.assertEqual(chapter_ids, self.ids)

    def test_progress_counts(self):
        progress = json.loads((validate.TRANS / "translation_progress.json").read_text(encoding="utf-8"))
        self.assertEqual(progress["total_ordered_dialogue_rows"], 261)
        self.assertEqual(progress["total_translated_rows"], 261)
        self.assertEqual(progress["total_untranslated_rows"], 0)
        self.assertEqual(progress["batch_row_count"], 261)
        self.assertEqual(progress["translation_confidence_counts"], dict(sorted(Counter(r["translation_confidence"] for r in self.master).items())))

    def test_all_csv_outputs_have_bom(self):
        for path in validate.TRANS.rglob("*.csv"):
            self.assertTrue(path.read_bytes().startswith(b"\xef\xbb\xbf"), str(path))

    def test_scope_aware_protected_source_integrity(self):
        self.assertEqual(validate.git_changed_protected(), [])
        self.assertEqual(list(validate.ROOT.glob("*.gba")), [])

    def test_full_validator(self):
        self.assertEqual(validate.validation_errors(run_scope=False), [])

    def test_deterministic_generation(self):
        before = validate.deterministic_support_hashes()
        subprocess.run(["python3", "-B", "tools/thai/generate_main_story_translation_support.py"], cwd=validate.ROOT, check=True)
        self.assertEqual(validate.deterministic_support_hashes(), before)


if __name__ == "__main__":
    unittest.main()
