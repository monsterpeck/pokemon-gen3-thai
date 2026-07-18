#!/usr/bin/env python3
"""Extract OpenType metric and GPOS anchor evidence from Noto Sans Thai."""
from __future__ import annotations
import csv,json
from noto_thai import *
from fontTools.ttLib import TTFont

def anchor(a): return None if a is None else {"x":a.XCoordinate,"y":a.YCoordinate}
def extract_anchors(font):
    evidence={}
    if "GPOS" not in font:return evidence
    for lookup_index,lookup in enumerate(font["GPOS"].table.LookupList.Lookup):
        for sub in lookup.SubTable:
            if lookup.LookupType==4: # mark-to-base
                marks=sub.MarkCoverage.glyphs; bases=sub.BaseCoverage.glyphs
                for name,record in zip(marks,sub.MarkArray.MarkRecord):
                    evidence.setdefault(name,[]).append({"kind":"mark","lookup":lookup_index,"class":record.Class,"anchor":anchor(record.MarkAnchor)})
                for name,record in zip(bases,sub.BaseArray.BaseRecord):
                    for cls,a in enumerate(record.BaseAnchor):
                        if a:evidence.setdefault(name,[]).append({"kind":"base","lookup":lookup_index,"class":cls,"anchor":anchor(a)})
            elif lookup.LookupType==6: # mark-to-mark
                for name,record in zip(sub.Mark1Coverage.glyphs,sub.Mark1Array.MarkRecord):
                    evidence.setdefault(name,[]).append({"kind":"mark1","lookup":lookup_index,"class":record.Class,"anchor":anchor(record.MarkAnchor)})
                for name,record in zip(sub.Mark2Coverage.glyphs,sub.Mark2Array.Mark2Record):
                    for cls,a in enumerate(record.Mark2Anchor):
                        if a:evidence.setdefault(name,[]).append({"kind":"mark2","lookup":lookup_index,"class":cls,"anchor":anchor(a)})
    return evidence

def build():
    require_source(); GENERATED.mkdir(parents=True,exist_ok=True); font=TTFont(FONT)
    cmap=font.getBestCmap(); glyf=font["glyf"]; hmtx=font["hmtx"]; anchors=extract_anchors(font); s=spec(); scale=s["logical_scale"]
    raw={"font":FONT.name,"sha256":sha256(FONT),"units_per_em":font["head"].unitsPerEm,"glyphs":{}}
    rows=[]
    for char in CHARACTERS:
        name=cmap[ord(char)]; glyph=glyf[name]; advance,_=hmtx[name]; items=anchors.get(name,[])
        chosen=next((item["anchor"] for item in items if item.get("anchor")),None)
        bbox={k:getattr(glyph,k,None) for k in ("xMin","yMin","xMax","yMax")}
        raw["glyphs"][f"U+{ord(char):04X}"]={"character":char,"glyph_name":name,"advance":advance,"bbox":bbox,"anchors":items}
        cls=glyph_class(char); origin_x=s["class_origin_x"][cls]; baseline=s["class_baseline_y"][cls]
        rows.append({"unicode":f"U+{ord(char):04X}","character":char,"glyph_name":name,"class":cls,
          "source_advance":advance,"target_advance":round(advance*scale,3),
          "source_anchor_x":"" if not chosen else chosen["x"],"source_anchor_y":"" if not chosen else chosen["y"],
          "target_anchor_x":"" if not chosen else round(origin_x+chosen["x"]*scale,3),
          "target_anchor_y":"" if not chosen else round(baseline-chosen["y"]*scale,3),
          "bbox_left":bbox["xMin"],"bbox_top":bbox["yMax"],"bbox_right":bbox["xMax"],"bbox_bottom":bbox["yMin"],
          "evidence":"GPOS" if items else "none","status":"evidenced" if items else "missing-anchor-evidence"})
    (GENERATED/"noto_thai_opentype_metrics.json").write_text(json.dumps(raw,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    path=THAI/"font/thai_metrics_proposed.csv"
    with path.open("w",newline="",encoding="utf-8") as handle:
        writer=csv.DictWriter(handle,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    print(f"wrote {path} and OpenType evidence for {len(rows)} glyphs")

if __name__=="__main__":build()
