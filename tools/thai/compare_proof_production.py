#!/usr/bin/env python3
"""Assert and visualize proof-raster versus production shaped cells."""
from __future__ import annotations
import json
from PIL import Image, ImageChops, ImageDraw, ImageFont
from fontTools.ttLib import TTFont
from noto_thai import FONT, GENERATED, PROOF_LINES, ROOT, spec
from render_thai_proof import GlyphRasterizer, rasterize_shaped_cell, shape_text

SHEET=ROOT/"graphics/fonts/thai_shaped.png"
MAP=ROOT/"tools/thai/font/thai_shaped_glyph_map.json"
OUTPUT=GENERATED/"proof_vs_production_glyphs.png"

def verify(draw_output=True):
 data=FONT.read_bytes();font=TTFont(FONT);upem=font["head"].unitsPerEm;order=font.getGlyphOrder()
 mapping=json.loads(MAP.read_text(encoding="utf-8"))
 rasterizer=GlyphRasterizer(FONT,upem,spec()["logical_scale"],spec()["oversample"])
 sheet=Image.open(SHEET);sheet.load()
 if sheet.mode!="P" or set(sheet.getdata())-{0,1,2}:raise AssertionError("production sheet mode or indexes changed")
 gids=set()
 for text in PROOF_LINES:
  _font,items=shape_text(text,data,upem);gids.update(info.codepoint for info,_pos in items)
 gids=sorted(gids,key=lambda gid:int(mapping["hb_to_gba"][str(gid)]))
 rows=[]
 for gid in gids:
  compact=int(mapping["hb_to_gba"][str(gid)])
  rendered=rasterize_shaped_cell(rasterizer,gid,sheet.getpalette())
  x,y=compact%16*16,compact//16*16;production=sheet.crop((x,y,x+16,y+16))
  if rendered["tile"].tobytes()!=production.tobytes():raise AssertionError(f"proof/production mismatch: HB {gid}, compact {compact}")
  rows.append((gid,order[gid],compact,rendered["tile"],production))
 if draw_output:
  scale=5;cell=16*scale;row_h=cell+34
  image=Image.new("RGB",(cell*3+300,row_h*len(rows)),"white");draw=ImageDraw.Draw(image);ui=ImageFont.load_default()
  for row,(gid,name,compact,proof,production) in enumerate(rows):
   y=row*row_h;proof_rgb=proof.convert("RGB");production_rgb=production.convert("RGB");difference=ImageChops.difference(proof_rgb,production_rgb)
   image.paste(proof_rgb.resize((cell,cell),Image.Resampling.NEAREST),(280,y))
   image.paste(production_rgb.resize((cell,cell),Image.Resampling.NEAREST),(280+cell,y))
   image.paste(difference.resize((cell,cell),Image.Resampling.NEAREST),(280+cell*2,y))
   draw.text((8,y+8),f"HB {gid} {name}",font=ui,fill="black");draw.text((8,y+24),f"compact {compact}",font=ui,fill="black")
   draw.text((280,y+cell+4),"proof",font=ui,fill="black");draw.text((280+cell,y+cell+4),"production",font=ui,fill="black");draw.text((280+cell*2,y+cell+4),"difference",font=ui,fill="black")
  image.save(OUTPUT)
 return rows

if __name__=="__main__":
 rows=verify();print(f"verified {len(rows)} pixel-identical proof/production glyphs");print(OUTPUT)
