from __future__ import annotations
import csv,hashlib,subprocess,sys,unittest
from pathlib import Path
from PIL import Image
THAI=Path(__file__).resolve().parents[1]; ROOT=THAI.parents[1]
sys.path.insert(0,str(THAI));sys.path.insert(0,str(THAI/"cache/python"))
from noto_thai import *
from rasterize_noto_thai import build as raster_build,rasterize
from extract_noto_thai_metrics import build as metrics_build
from render_thai_proof import build as proof_build
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
class NotoFontEngineeringTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):raster_build();metrics_build();proof_build()
 def test_source_hash_and_license(self):self.assertEqual(sha256(FONT),EXPECTED_SHA256);self.assertIn("SIL OPEN FONT LICENSE",LICENSE.read_text(encoding="utf-8").upper())
 def test_every_required_character_generated(self):self.assertEqual({p.stem for p in RASTER_DIR.glob("u*.png")},{f"u{ord(c):04x}" for c in CHARACTERS})
 def test_tiles_are_indexed_16x16_with_allowed_indexes(self):
  allowed=set(spec()["allowed_indexed_palette_entries"])
  for path in RASTER_DIR.glob("u*.png"):
   with Image.open(path) as im:self.assertEqual((im.mode,im.size),("P",(16,16)));self.assertLessEqual(set(im.getdata()),allowed)
 def test_no_required_glyph_is_blank_or_clipped(self):
  for char in CHARACTERS:
   tile,coverage,clipped=rasterize(char)
   self.assertTrue(any(tile.getdata()),f"U+{ord(char):04X}")
   self.assertFalse(clipped,f"U+{ord(char):04X}")
 def test_rasterization_is_deterministic(self):
  before={p.name:digest(p) for p in RASTER_DIR.glob("*.png")};raster_build();self.assertEqual(before,{p.name:digest(p) for p in RASTER_DIR.glob("*.png")})
 def test_metrics_and_anchor_evidence_exist(self):
  self.assertIn('"anchors"',(GENERATED/"noto_thai_opentype_metrics.json").read_text(encoding="utf-8"))
  with (THAI/"font/thai_metrics_proposed.csv").open(encoding="utf-8") as h:self.assertEqual(len(list(csv.DictReader(h))),len(CHARACTERS))
 def test_proof_is_deterministic(self):
  paths=[GENERATED/"thai_reference_vs_pixel_proof_fixed.png",GENERATED/"thai_shaping_trace_fixed.csv",GENERATED/"thai_proof_pipeline_report.md"];before=[digest(p) for p in paths];proof_build();self.assertEqual(before,[digest(p) for p in paths])
 def test_fixed_proof_uses_shaped_glyph_ids(self):
  source=(THAI/"render_thai_proof.py").read_text(encoding="utf-8")
  self.assertNotIn("RASTER_DIR",source)
  self.assertNotIn("cluster_char",source)
  with (GENERATED/"thai_shaping_trace_fixed.csv").open(encoding="utf-8") as h:
   rows=list(csv.DictReader(h))
  required={"glyph_id","glyph_name","font_x_advance","font_y_advance","font_x_offset","font_y_offset","final_draw_x","final_draw_y"}
  self.assertLessEqual(required,set(rows[0]))
  self.assertTrue(any(int(r["font_x_advance"])==0 and (int(r["font_x_offset"]) or int(r["font_y_offset"])) for r in rows))
 def test_production_files_are_unmodified(self):
  names=subprocess.check_output(["git","diff","--name-only"],cwd=ROOT,text=True).splitlines();forbidden={"graphics/fonts/latin_normal.png","charmap.txt"};self.assertFalse(forbidden&set(names))
if __name__=="__main__":unittest.main()
