#!/usr/bin/env python3
"""Build-time HarfBuzz shaping for ordinary Unicode Thai project strings."""
from __future__ import annotations
import argparse, json, math, re, sys
from pathlib import Path
from PIL import Image
from fontTools.ttLib import TTFont
from noto_thai import *
from render_thai_proof import GlyphRasterizer, rasterize_shaped_cell, shape_text

CMD_BEGIN=0xFC
CMD_THAI_POSITIONED=0x19
COMMAND_SIZE=8
MAP_PATH=THAI/"font/thai_shaped_glyph_map.json"
FONT_PNG=ROOT/"graphics/fonts/thai_shaped.png"
THAI_RE=re.compile(r"[\u0E00-\u0E7F]+")
STRING_RE=re.compile(r'"(?:\\.|[^"\\])*"')
TRACE_PATH=GENERATED/"thai_shaping_trace_fixed.csv"

UPPER_CLEARANCE_MARKS={chr(x)for x in[0xE31,0xE34,0xE35,0xE36,0xE37,0xE47,0xE4D,0xE48,0xE49,0xE4A,0xE4B,0xE4C]}

def cluster_upper_flags(text,items):
    starts=sorted({info.cluster for info,_pos in items})
    ends={start:(starts[i+1] if i+1<len(starts) else len(text)) for i,start in enumerate(starts)}
    return {start:any(ch in UPPER_CLEARANCE_MARKS for ch in text[start:ends[start]]) for start in starts}

def thai_base_glyph_ids():
    tt=TTFont(FONT);order=tt.getGlyphOrder();cmap=tt.getBestCmap()
    return {order.index(cmap[ord(ch)]) for ch in CONSONANTS}

def shift_indexed_tile_down(tile):
    shifted=Image.new("P",(16,16),0);shifted.putpalette(tile.getpalette())
    shifted.paste(tile.crop((0,0,16,15)),(0,1))
    return shifted

def round_half_away(value):
    return math.floor(value+0.5) if value>=0 else math.ceil(value-0.5)

def load_context():
    require_source()
    tt=TTFont(FONT); upem=tt["head"].unitsPerEm
    data=FONT.read_bytes()
    return data,upem,tt.getGlyphOrder()

def shape_run(text,mapping=None):
    data,upem,order=load_context(); scale=spec()["logical_scale"]; n=spec()["oversample"]
    hb_font,items=shape_text(text,data,upem)
    upper_by_cluster=cluster_upper_flags(text,items);base_gids=thai_base_glyph_ids()
    raster=GlyphRasterizer(FONT,upem,scale,n)
    result=[]; cumulative=0.0; rounded_pen=0
    last_cluster=None
    for info,pos in items:
        gid=info.codepoint
        name=order[gid]
        if hb_font.glyph_to_string(gid)!=name or raster.glyph_name(gid)!=name:
            raise ValueError(f"glyph ID mapping mismatch for {gid}")
        bm=raster.rasterize(gid)
        if bm["bitmap_width"]>16 or bm["bitmap_height"]>16:
            raise ValueError(f"shaped glyph {gid} ({name}) exceeds 16x16")
        if mapping is not None and str(gid) not in mapping["hb_to_gba"]:
            raise ValueError(f"missing shaped glyph mapping for HarfBuzz glyph {gid} ({name})")
        cumulative += pos.x_advance*scale
        next_pen=round_half_away(cumulative)
        advance=next_pen-rounded_pen; rounded_pen=next_pen
        if not 0<=advance<=255: raise ValueError(f"advance out of range for glyph {gid}: {advance}")
        draw_x=round_half_away(pos.x_offset*scale+bm["bitmap_left"])
        draw_y=round_half_away(-pos.y_offset*scale-bm["bitmap_top"])
        if not -128<=draw_x<=127 or not -128<=draw_y<=127:
            raise ValueError(f"offset out of range for glyph {gid}: {draw_x},{draw_y}")
        cluster_start=info.cluster!=last_cluster; last_cluster=info.cluster
        result.append(dict(glyph_id=gid,glyph_name=name,cluster=info.cluster,
            cluster_start=cluster_start,x_offset=draw_x,y_offset=draw_y,x_advance=advance,
            font_x_advance=pos.x_advance,font_y_advance=pos.y_advance,
            font_x_offset=pos.x_offset,font_y_offset=pos.y_offset,bitmap=bm,
            is_base=gid in base_gids,cluster_has_upper_marks=upper_by_cluster[info.cluster],
            base_variant="upper_clearance" if gid in base_gids and upper_by_cluster[info.cluster] else "normal"))
    return result,round_half_away(cumulative)

def encode_run(text,mapping):
    records,total=shape_run(text,mapping); out=[]
    for r in records:
        original=int(mapping["hb_to_gba"][str(r["glyph_id"])])
        variants=mapping.get("upper_clearance_hb_to_gba",{})
        gba=int(variants[str(r["glyph_id"])]) if r["is_base"] and r["cluster_has_upper_marks"] and str(r["glyph_id"]) in variants else original
        r["original_compact_index"]=original;r["selected_compact_index"]=gba
        flags=1 if r["cluster_start"] else 0
        out += [CMD_BEGIN,CMD_THAI_POSITIONED,gba&255,gba>>8,
                r["x_offset"]&255,r["y_offset"]&255,r["x_advance"],flags]
    return bytes(out),records,total

def brace_bytes(data):
    return "".join("{%d}"%b for b in data)

def transform_literal(literal,mapping):
    body=literal[1:-1]
    return '"'+THAI_RE.sub(lambda m: brace_bytes(encode_run(m.group(0),mapping)[0]),body)+'"'

def transform_source(source,mapping):
    def replace(match):
        if not THAI_RE.search(match.group(0)):return match.group(0)
        prefix=source[:match.start()]
        line_prefix=prefix[prefix.rfind("\n")+1:]
        in_project_string=bool(re.search(r"_\s*\([^)]*$",prefix[-4096:],re.S))
        in_asm_string=bool(re.search(r"\.(?:string|ascii)\s*$",line_prefix))
        return transform_literal(match.group(0),mapping) if in_project_string or in_asm_string else match.group(0)
    return STRING_RE.sub(replace,source)

def build_font():
    data,upem,order=load_context(); scale=spec()["logical_scale"]; n=spec()["oversample"]
    gids=set();variant_gids=set();base_gids=thai_base_glyph_ids()
    for text in PROOF_LINES:
        hb_font,items=shape_text(text,data,upem);gids.update(i.codepoint for i,_ in items)
        upper=cluster_upper_flags(text,items)
        variant_gids.update(info.codepoint for info,_pos in items if info.codepoint in base_gids and upper[info.cluster])
    gids=sorted(gids);variant_gids=sorted(variant_gids)
    raster=GlyphRasterizer(FONT,upem,scale,n)
    cols=16;total=len(gids)+len(variant_gids);rows=(total+cols-1)//cols
    sheet=Image.new("P",(cols*16,rows*16),0)
    pal=[]
    for rgb in spec()["palette_rgb"]:pal.extend(rgb)
    sheet.putpalette(pal+[0]*(768-len(pal)))
    entries=[];hb_to_gba={};upper_to_gba={}
    for gba,gid in enumerate(gids):
        rendered=rasterize_shaped_cell(raster,gid,sheet.getpalette());bm=rendered["bitmap"];w=rendered["width"];h=rendered["height"];tile=rendered["tile"]
        sheet.paste(tile,((gba%cols)*16,(gba//cols)*16));hb_to_gba[str(gid)]=gba
        entries.append(dict(gba_glyph_id=gba,hb_glyph_id=gid,glyph_name=order[gid],variant="normal",bitmap_width=w,bitmap_height=h))
    for offset,gid in enumerate(variant_gids):
        gba=len(gids)+offset;rendered=rasterize_shaped_cell(raster,gid,sheet.getpalette());tile=shift_indexed_tile_down(rendered["tile"])
        if 1 not in set(tile.getdata()):raise ValueError(f"clearance variant HB {gid} has no index-1 main pixels")
        sheet.paste(tile,((gba%cols)*16,(gba//cols)*16));upper_to_gba[str(gid)]=gba
        entries.append(dict(gba_glyph_id=gba,hb_glyph_id=gid,glyph_name=order[gid],variant="upper_clearance",source_gba_glyph_id=hb_to_gba[str(gid)],bitmap_width=rendered["width"],bitmap_height=rendered["height"]))
    if sheet.mode!="P" or set(sheet.getdata())-{0,1,2}:raise ValueError("invalid shaped font palette indexes")
    FONT_PNG.parent.mkdir(parents=True,exist_ok=True);sheet.save(FONT_PNG,optimize=False)
    mapping=dict(format_version=2,font_sha256=EXPECTED_SHA256,units_per_em=upem,scale=scale,command_begin=CMD_BEGIN,command_id=CMD_THAI_POSITIONED,command_size=COMMAND_SIZE,hb_to_gba=hb_to_gba,upper_clearance_hb_to_gba=upper_to_gba,glyphs=entries)
    mapping_text=json.dumps(mapping,indent=2)+"\n"
    if not MAP_PATH.exists() or MAP_PATH.read_text(encoding="utf-8")!=mapping_text:
        MAP_PATH.write_text(mapping_text,encoding="utf-8")
    return mapping

def load_mapping():
    if not MAP_PATH.exists():raise FileNotFoundError(f"missing shaped glyph map: {MAP_PATH}")
    return json.loads(MAP_PATH.read_text(encoding="utf-8"))

def check_trace(mapping):
    import csv
    with TRACE_PATH.open(encoding="utf-8") as h: proof=list(csv.DictReader(h))
    for line,text in enumerate(PROOF_LINES,1):
        records,_=shape_run(text,mapping); expected=[r for r in proof if int(r["line"])==line]
        if [r["glyph_id"] for r in records]!=[int(r["glyph_id"]) for r in expected]:
            raise ValueError(f"glyph IDs differ from proof on line {line}")
        for got,want in zip(records,expected):
            for key in ("font_x_advance","font_y_advance","font_x_offset","font_y_offset"):
                if got[key]!=int(want[key]):raise ValueError(f"{key} differs from proof on line {line}")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--build-font",action="store_true")
    ap.add_argument("--filter-source",nargs="?",const="-")
    ap.add_argument("--check",action="store_true")
    ap.add_argument("--encode")
    args=ap.parse_args()
    mapping=build_font() if args.build_font else load_mapping()
    if args.check:check_trace(mapping)
    if args.encode:
        encoded,records,total=encode_run(args.encode,mapping)
        print(encoded.hex(" "));print(json.dumps({"advance":total,"glyphs":[{k:v for k,v in r.items() if k!="bitmap"} for r in records]},ensure_ascii=False,indent=2))
    if args.filter_source is not None:
        source=sys.stdin.read() if args.filter_source=="-" else Path(args.filter_source).read_text(encoding="utf-8")
        sys.stdout.write(transform_source(source,mapping))

if __name__=="__main__":main()
