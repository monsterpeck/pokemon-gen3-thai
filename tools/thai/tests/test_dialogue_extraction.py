import csv
import io
import unittest
from pathlib import Path

from tools.thai import extract_dialogue as extraction


class DialogueExtractionTests(unittest.TestCase):
    def test_assembly_adjacent_controls_and_placeholders(self):
        source = 'Example::\n .string "Hello.\\p"\n .string "World, {PLAYER}!$"\n'
        entry = extraction.parse_assembly(source)[0]
        self.assertEqual(entry["raw"], "Hello.\\pWorld, {PLAYER}!$")
        self.assertIn("[PAGE]", extraction.make_preview(entry["raw"]))
        self.assertIn("{PLAYER}", extraction.PLACEHOLDER_RE.findall(entry["raw"]))

    def test_c_adjacent_fragments_and_escaped_quotes(self):
        source = 'const u8 gText_Test[] = _("Say \\\"hello\\\"\\n" "again.");'
        entry = extraction.parse_c(source)[0]
        self.assertEqual(entry["label"], "gText_Test")
        self.assertEqual(entry["raw"], 'Say "hello"\\nagain.')

    def test_comments_ignored(self):
        self.assertEqual(extraction.parse_c('// const u8 x[] = _("debug");'), [])
        self.assertEqual(extraction.parse_assembly('/* X::\n.string "debug$"\n*/'), [])

    def test_archived_and_generated_ignored(self):
        self.assertTrue(extraction.is_ignored(Path("src/a.c.before_probe")))
        self.assertTrue(extraction.is_ignored(Path("tools/thai/generated/a.inc")))
        self.assertTrue(extraction.is_ignored(Path("tools/thai/archive/a.inc")))

    def test_stable_unique_ids_and_empty_thai(self):
        source = extraction.ROOT / "data/text/birch_speech.inc"
        first, _ = extraction.build_rows([source])
        second, _ = extraction.build_rows([source])
        self.assertEqual([r["id"] for r in first], [r["id"] for r in second])
        self.assertEqual(len(first), len({r["id"] for r in first}))
        self.assertTrue(all(not r["thai"] for r in first))
        self.assertTrue(all(r["translation_status"] == "untranslated" for r in first))

    def test_csv_bom_quoting(self):
        row = {column: "" for column in extraction.COLUMNS}
        row.update(id="test", english_raw='line 1\n"line, 2"', translation_status="untranslated")
        content = extraction.csv_bytes([row])
        self.assertTrue(content.startswith(b"\xef\xbb\xbf"))
        parsed = list(csv.DictReader(io.StringIO(content.decode("utf-8-sig"))))
        self.assertEqual(parsed[0]["english_raw"], row["english_raw"])

    def test_story_subset_and_repeat_bytes(self):
        source = extraction.ROOT / "data/text/birch_speech.inc"
        rows, types = extraction.build_rows([source])
        first = extraction.render_outputs(rows, types, [source], [])
        second = extraction.render_outputs(rows, types, [source], [])
        self.assertEqual(first, second)
        master = list(csv.DictReader(io.StringIO(first["dialogue_master.csv"].decode("utf-8-sig"))))
        story = list(csv.DictReader(io.StringIO(first["dialogue_main_story.csv"].decode("utf-8-sig"))))
        self.assertLessEqual({r["id"] for r in story}, {r["id"] for r in master})


if __name__ == "__main__":
    unittest.main()
