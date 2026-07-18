#!/usr/bin/env python3
"""Validate and visualize build-time contextual upper-clearance variants."""
from __future__ import annotations
import csv,json,subprocess,tempfile
from pathlib import Path
from PIL import Image,ImageChops,ImageDraw,ImageFont
from noto_thai import GENERATED,PROOF_LINES,ROOT
from shape_thai_text import FONT_PNG,encode_run,load_mapping,shift_indexed_tile_down

TRACE=GENERATED/"contextual_clearance_trace.csv"
CLUSTERS=GENERATED/"contextual_clearance_clusters.png"
BEFORE_AFTER=GENERATED/"contextual_clearance_before_after.png"
PALETTE_PROOF=GENERATED/"contextual_clearance_palette_proof.png"
LATFONT=ROOT/"build/assets/graphics/fonts/thai_shaped.png.latfont"
ROM=ROOT/"pokeemerald.gba"
TEXTS=("เรม","เริ่ม","เกมส์","เริ่มเกมส์","ผู้เล่น","ญี่ปุ่น")
FIELDS=("input_text","cluster","unicode_sequence","glyph_id","glyph_name","base_variant","cluster_has_upper_marks","original_compact_index","selected_compact_index","x_offset","y_offset","x_advance","main_pixel_count_index_1","shadow_pixel_count_index_2")

def cell(sheet,index):
 x,y=index%16*16,index//16*16
 return sheet.crop((x,y,x+16,y+16))

def mask(tile,index):return tile.point(lambda p:255 if p==index else 0).convert("L")

def render_text(text,mapping,sheet,use_variants):
 _data,records,_total=encode_run(text,mapping);width=sum(r["x_advance"] for r in records)+24
 out=Image.new("P",(width,28),0);out.putpalette(sheet.getpalette());pen=4
 for r in records:
  index=r["selected_compact_index"] if use_variants else r["original_compact_index"]
  tile=cell(sheet,index);x=max(0,pen+r["x_offset"]);y=max(0,16+r["y_offset"])
  out.paste(tile,(x,y),tile.point(lambda p:255 if p else 0).convert("L"));pen+=r["x_advance"]
 return out,records

def verify_binary(sheet):
 if not LATFONT.exists() or not ROM.exists():return
 with tempfile.TemporaryDirectory() as directory:
  decoded=Path(directory)/"decoded.png"
  subprocess.run([str(ROOT/"tools/gbagfx/gbagfx"),str(LATFONT),str(decoded)],check=True)
  image=Image.open(decoded);image.load()
  if image.tobytes()!=sheet.tobytes():raise AssertionError(".latfont round trip changed palette indexes")
 symbols=subprocess.check_output(["arm-none-eabi-nm","-n",str(ROOT/"pokeemerald.elf")],text=True)
 address=next(int(line.split()[0],16) for line in symbols.splitlines() if line.endswith(" gFontThaiShapedGlyphs"))
 asset=LATFONT.read_bytes();offset=address-0x08000000
 if ROM.read_bytes()[offset:offset+len(asset)]!=asset:raise AssertionError("linked ROM differs from contextual .latfont")

def verify(generate=False):
 mapping=load_mapping();variants=mapping["upper_clearance_hb_to_gba"]
 sheet=Image.open(FONT_PNG);sheet.load()
 if sheet.mode!="P" or set(sheet.getdata())-{0,1,2}:raise AssertionError("invalid production palette indexes")
 engine=(ROOT/"tools/gbagfx/font.c").read_text()
 if "// fg (dark grey)" not in engine or "// shadow (light grey)" not in engine:raise AssertionError("GBA index semantics changed")
 for entry in mapping["glyphs"]:
  tile=cell(sheet,int(entry["gba_glyph_id"]))
  if entry["glyph_name"]!="space" and 1 not in tile.getdata():raise AssertionError("production glyph lacks index-1 main pixels")
 for gid,index in variants.items():
  normal=int(mapping["hb_to_gba"][gid]);variant=int(index);a=cell(sheet,normal);b=cell(sheet,variant)
  if b.tobytes()!=shift_indexed_tile_down(a).tobytes():raise AssertionError(f"variant HB {gid} is not an exact one-pixel shift")
  if 1 not in b.getdata():raise AssertionError(f"variant HB {gid} lacks index-1 main pixels")
  if set(a.getdata())-{0,1,2} or set(b.getdata())-{0,1,2}:raise AssertionError("normal/variant palette mismatch")
 rows=[]
 for text in TEXTS:
  _encoded,records,_total=encode_run(text,mapping)
  normal_mapping=dict(mapping);normal_mapping["upper_clearance_hb_to_gba"]={};_plain,normal_records,_plain_total=encode_run(text,normal_mapping)
  if [(r["glyph_id"],r["x_offset"],r["y_offset"],r["x_advance"]) for r in records]!=[(r["glyph_id"],r["x_offset"],r["y_offset"],r["x_advance"]) for r in normal_records]:raise AssertionError("context selection changed shaping geometry")
  starts=sorted({r["cluster"] for r in records});ends={s:(starts[i+1] if i+1<len(starts) else len(text)) for i,s in enumerate(starts)}
  for r in records:
   tile=cell(sheet,r["selected_compact_index"]);cluster=text[r["cluster"]:ends[r["cluster"]]]
   rows.append(dict(input_text=text,cluster=cluster,unicode_sequence=" ".join(f"U+{ord(ch):04X}" for ch in cluster),glyph_id=r["glyph_id"],glyph_name=r["glyph_name"],base_variant=r["base_variant"],cluster_has_upper_marks=r["cluster_has_upper_marks"],original_compact_index=r["original_compact_index"],selected_compact_index=r["selected_compact_index"],x_offset=r["x_offset"],y_offset=r["y_offset"],x_advance=r["x_advance"],main_pixel_count_index_1=sum(p==1 for p in tile.getdata()),shadow_pixel_count_index_2=sum(p==2 for p in tile.getdata())))
 def base(text,gid):return next(r for r in rows if r["input_text"]==text and r["glyph_id"]==gid)
 if base("เรม",81)["selected_compact_index"]!=16:raise AssertionError("plain ร did not keep normal compact 16")
 if base("เริ่ม",81)["selected_compact_index"]==16:raise AssertionError("marked ร did not select clearance variant")
 if base("เกมส์",110)["selected_compact_index"]==25:raise AssertionError("marked ส did not select clearance variant")
 verify_binary(sheet)
 if generate:
  with TRACE.open("w",newline="",encoding="utf-8") as handle:w=csv.DictWriter(handle,fieldnames=FIELDS);w.writeheader();w.writerows(rows)
  draw_proofs(mapping,sheet)
 return rows

def draw_proofs(mapping,sheet):
 scale=5;line_h=150;width=980;ui=ImageFont.load_default()
 before=Image.new("RGB",(width,line_h*len(TEXTS)),"white");d=ImageDraw.Draw(before)
 clusters=Image.new("RGB",(width,line_h*len(TEXTS)),"white");dc=ImageDraw.Draw(clusters)
 for i,text in enumerate(TEXTS):
  old,records=render_text(text,mapping,sheet,False);new,_=render_text(text,mapping,sheet,True);y=i*line_h
  d.text((8,y+8),text,font=ui,fill="black");d.text((120,y+8),"original",font=ui,fill="black");d.text((500,y+8),"contextual",font=ui,fill="black")
  d.line((110,y+96,width-10,y+96),fill="red");before.paste(old.convert("RGB").resize((old.width*scale,old.height*scale),Image.Resampling.NEAREST),(120,y+20));before.paste(new.convert("RGB").resize((new.width*scale,new.height*scale),Image.Resampling.NEAREST),(500,y+20))
  dc.text((8,y+8),text,font=ui,fill="black");clusters.paste(new.convert("RGB").resize((new.width*scale,new.height*scale),Image.Resampling.NEAREST),(200,y+10));pen=220
  for r in records:dc.text((pen,y+125),f"{r['cluster']}:{r['selected_compact_index']}",font=ui,fill="black");pen+=max(35,r["x_advance"]*scale)
 before.save(BEFORE_AFTER);clusters.save(CLUSTERS)
 variants=sorted(mapping["upper_clearance_hb_to_gba"].items(),key=lambda item:int(item[1]));row_h=110
 proof=Image.new("RGB",(780,row_h*len(variants)),"white");dp=ImageDraw.Draw(proof)
 for row,(gid,index) in enumerate(variants):
  normal=cell(sheet,int(mapping["hb_to_gba"][gid]));variant=cell(sheet,int(index));y=row*row_h
  dp.text((8,y+8),f"HB {gid}: normal {mapping['hb_to_gba'][gid]} / variant {index}",font=ui,fill="black")
  images=[mask(variant,0),mask(variant,1),mask(variant,2),variant.convert("RGB")]
  labels=["index 0","index 1 dark main","index 2 light shadow","combined"]
  for col,(image,label) in enumerate(zip(images,labels)):
   x=250+col*125;proof.paste(image.convert("RGB").resize((80,80),Image.Resampling.NEAREST),(x,y));dp.text((x,y+84),label,font=ui,fill="black")
 proof.save(PALETTE_PROOF)

if __name__=="__main__":
 rows=verify(generate=True);print(f"verified {len(rows)} contextual trace rows");print(BEFORE_AFTER);print(PALETTE_PROOF);print(TRACE)
