#!/usr/bin/env python3
"""Rasterize one coherent Noto Sans Thai-derived 16x16 indexed candidate set."""
from __future__ import annotations
from PIL import Image,ImageDraw,ImageFont
from noto_thai import *

def palette():
    values=[]
    for rgb in spec()["palette_rgb"]: values.extend(rgb)
    return values+[0]*(768-len(values))

def rasterize(char):
    s=spec(); n=s["oversample"]; cls=glyph_class(char); size=s["font_size_pixels"]*n
    # Draw with a full-cell guard band. Cropping only after rasterization lets
    # validation distinguish genuinely clipped source ink from generated shadow.
    pad=16*n; mask=Image.new("L",(48*n,48*n)); draw=ImageDraw.Draw(mask)
    font=ImageFont.truetype(str(FONT),size,layout_engine=ImageFont.Layout.BASIC)
    x=pad+s["class_origin_x"][cls]*n
    y=pad+(15 if char == "ำ" else s["class_baseline_y"][cls])*n
    draw.text((x,y),char,font=font,fill=255,anchor="ls")
    source_bbox=mask.getbbox()
    cell=(pad,pad,pad+16*n,pad+16*n)
    coverage=mask.crop(cell).resize((16,16),Image.Resampling.BOX)
    ink=[[coverage.getpixel((x,y))/255>=s["rasterization_threshold"] for x in range(16)] for y in range(16)]
    out=Image.new("P",(16,16),0); out.putpalette(palette())
    # Existing Thai tiles use foreground index 2 and a one-pixel down-right index-1 shadow.
    for y in range(15):
        for x in range(15):
            if ink[y][x] and not ink[y+1][x+1]: out.putpixel((x+1,y+1),1)
    for y in range(16):
        for x in range(16):
            if ink[y][x]: out.putpixel((x,y),2)
    clipped=source_bbox is None or source_bbox[0]<cell[0] or source_bbox[1]<cell[1] or source_bbox[2]>cell[2] or source_bbox[3]>cell[3]
    return out,coverage,clipped

def build():
    require_source(); RASTER_DIR.mkdir(parents=True,exist_ok=True)
    tiles=[]
    for char in CHARACTERS:
        tile,_,clipped=rasterize(char)
        if clipped: raise ValueError(f"source ink for U+{ord(char):04X} exceeds the 16x16 cell")
        path=RASTER_DIR/f"u{ord(char):04x}.png"; tile.save(path,optimize=False); tiles.append((char,tile))
    # Source-sized indexed contact sheet, 10 cells per row.
    cols=10; rows=(len(tiles)+cols-1)//cols
    sheet=Image.new("P",(cols*16,rows*16),0); sheet.putpalette(palette())
    for i,(_,tile) in enumerate(tiles): sheet.paste(tile,((i%cols)*16,(i//cols)*16))
    sheet.save(GENERATED/"noto_thai_contact_sheet.png",optimize=False)
    # Labeled nearest-neighbor proof; labels are rendered separately from production tiles.
    scale=8; cell_w=16*scale; cell_h=16*scale+30
    proof=Image.new("RGB",(cols*cell_w,rows*cell_h),"white"); d=ImageDraw.Draw(proof)
    label_font=ImageFont.truetype(str(FONT),16)
    for i,(char,tile) in enumerate(tiles):
        ox=(i%cols)*cell_w; oy=(i//cols)*cell_h
        proof.paste(tile.convert("RGB").resize((cell_w,16*scale),Image.Resampling.NEAREST),(ox,oy))
        for k in range(17):
            d.line((ox+k*scale,oy,ox+k*scale,oy+16*scale),fill=(90,90,90))
            d.line((ox,oy+k*scale,ox+cell_w,oy+k*scale),fill=(90,90,90))
        s=spec(); d.line((ox,oy+s["target_baseline"]*scale,ox+cell_w,oy+s["target_baseline"]*scale),fill="red",width=2)
        d.text((ox+2,oy+16*scale+2),f"U+{ord(char):04X} {char}",font=label_font,fill="black")
    proof.save(GENERATED/"noto_thai_proof.png")
    return tiles

if __name__=="__main__":
    tiles=build(); print(f"rasterized {len(tiles)} glyphs from {FONT}")
