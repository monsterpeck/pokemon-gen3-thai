from __future__ import annotations
import copy,csv,hashlib,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];THAI=ROOT/"tools/thai"
sys.path[:0]=[str(THAI),str(THAI/"cache/python")]
from noto_thai import PROOF_LINES,GENERATED
from shape_thai_text import *
from runtime_glyph_trace import BYTES_PER_GLYPH, LATFONT, TEXT as START_GAME_TEXT, decode as decode_runtime, verify_and_generate
from compare_proof_production import verify as verify_proof_production
from contextual_clearance import verify as verify_contextual_clearance

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def decode(data):
 out=[];i=0
 while i<len(data):
  if data[i]!=CMD_BEGIN or i+COMMAND_SIZE>len(data) or data[i+1]!=CMD_THAI_POSITIONED:raise ValueError("invalid positioned glyph stream")
  gid=data[i+2]|data[i+3]<<8;sx=data[i+4]-256 if data[i+4]>=128 else data[i+4];sy=data[i+5]-256 if data[i+5]>=128 else data[i+5]
  out.append((gid,sx,sy,data[i+6],data[i+7]));i+=COMMAND_SIZE
 return out

class BuildTimeShapingTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.mapping=load_mapping()
  with (GENERATED/"thai_shaping_trace_fixed.csv").open(encoding="utf-8") as h:cls.proof=list(csv.DictReader(h))
 def test_unicode_source_remains_readable(self):
  self.assertIn(f'_("{PROOF_LINES[0]}")',(ROOT/"src/strings.c").read_text(encoding="utf-8"))
  speech=(ROOT/"data/text/birch_speech.inc").read_text(encoding="utf-8")
  for text in PROOF_LINES:self.assertIn(text,speech)
 def test_glyph_ids_advances_and_offsets_match_proof(self):
  for line,text in enumerate(PROOF_LINES,1):
   records,total=shape_run(text,self.mapping);expected=[r for r in self.proof if int(r["line"])==line]
   self.assertEqual([r["glyph_id"] for r in records],[int(r["glyph_id"]) for r in expected])
   for got,want in zip(records,expected):
    self.assertEqual(got["font_x_advance"],int(want["font_x_advance"]));self.assertEqual(got["font_x_offset"],int(want["font_x_offset"]));self.assertEqual(got["font_y_offset"],int(want["font_y_offset"]))
   self.assertLessEqual(abs(total-round(sum(float(r["pixel_x_advance"]) for r in expected))),1)
 def test_combining_marks_keep_shaped_offsets(self):
  records,_=shape_run(PROOF_LINES[0],self.mapping);marks=[r for r in records if r["font_x_advance"]==0]
  self.assertTrue(marks);self.assertTrue(any(r["font_x_offset"] or r["font_y_offset"] for r in marks))
 def test_spaces_newlines_and_controls_are_preserved(self):
  source=f'_("{PROOF_LINES[3]}\\n{{COLOR RED}}OK")';output=transform_source(source,self.mapping)
  self.assertIn(" ",output);self.assertIn("\\n",output);self.assertIn("{COLOR RED}",output);self.assertIn("OK",output)
 def test_english_is_byte_identical(self):
  source='const u8 s[] = _("English {COLOR RED}\\n");';self.assertEqual(transform_source(source,self.mapping),source)
 def test_missing_glyph_fails(self):
  broken=copy.deepcopy(self.mapping);records,_=shape_run(PROOF_LINES[0],broken);del broken["hb_to_gba"][str(records[0]["glyph_id"])]
  with self.assertRaisesRegex(ValueError,"missing shaped glyph"):encode_run(PROOF_LINES[0],broken)
 def test_signed_offsets_round_trip(self):
  encoded,records,_=encode_run(PROOF_LINES[0],self.mapping);decoded=decode(encoded)
  self.assertEqual([(r["x_offset"],r["y_offset"]) for r in records],[(x,y) for _,x,y,_,_ in decoded])
 def test_command_decoder_is_bounds_safe(self):
  source=(ROOT/"src/text.c").read_text(encoding="utf-8");self.assertIn("glyphId >= gFontThaiShapedGlyphCount",source);self.assertIn("currentChar += 6",source)
  with self.assertRaises(ValueError):decode(bytes([CMD_BEGIN,CMD_THAI_POSITIONED,0]))
 def test_all_glyph_ids_fit_allocated_font(self):
  indexes=set(map(int,self.mapping["hb_to_gba"].values()))|set(map(int,self.mapping["upper_clearance_hb_to_gba"].values()));self.assertEqual(indexes,set(range(len(self.mapping["glyphs"]))))
  for text in PROOF_LINES:encode_run(text,self.mapping)
 def test_builder_is_deterministic(self):
  build_font();before=(digest(MAP_PATH),digest(FONT_PNG));build_font();self.assertEqual(before,(digest(MAP_PATH),digest(FONT_PNG)))
 def test_production_cells_match_accepted_proof_raster(self):
  verify_proof_production(draw_output=False)
 def test_contextual_clearance_selection_palette_and_assets(self):
  verify_contextual_clearance(generate=False)
 def test_start_game_runtime_lookup_and_reconstruction(self):
  encoded,shaped,_=encode_run(START_GAME_TEXT,self.mapping);decoded=decode_runtime(encoded)
  self.assertEqual(len(decoded),len(shaped))
  self.assertEqual(LATFONT.stat().st_size % BYTES_PER_GLYPH,0)
  verify_and_generate()
 def test_preprocessor_is_integrated(self):self.assertIn("$(THAI_SHAPER) --filter-source",(ROOT/"Makefile").read_text(encoding="utf-8"))
 def test_runtime_has_no_thai_grammar_in_command(self):
  source=(ROOT/"src/text.c").read_text(encoding="utf-8");start=source.index("static u16 RenderThaiPositionedGlyph",source.index("static u16 RenderThaiPositionedGlyph")+1);body=source[start:source.index("static u16 RenderText(",start)]
  self.assertNotIn("GetThaiGlyphInfo",body);self.assertNotIn("ThaiBaseMetrics",body)
 def test_command_format_is_fixed_and_explicit(self):
  self.assertEqual(COMMAND_SIZE,8);encoded,_,_=encode_run(PROOF_LINES[0],self.mapping);self.assertEqual(len(encoded)%COMMAND_SIZE,0);decode(encoded)
 def test_acceptance_screen_contains_all_six_strings(self):
  speech=(ROOT/"data/text/birch_speech.inc").read_text(encoding="utf-8");self.assertTrue(all(text in speech for text in PROOF_LINES))
 def test_compiled_rom_contains_positioned_stream(self):
  encoded,_,_=encode_run(PROOF_LINES[0],self.mapping);self.assertIn(encoded+(bytes([255])),(ROOT/"pokeemerald.gba").read_bytes())
 def test_rom_exists_after_full_build(self):self.assertTrue((ROOT/"pokeemerald.gba").is_file())

if __name__=="__main__":unittest.main()
