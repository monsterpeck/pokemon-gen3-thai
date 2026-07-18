"""Shared definitions for the evidence-only Noto Thai font pipeline."""
from __future__ import annotations
import hashlib, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; THAI=ROOT/"tools/thai"; CACHE=THAI/"cache"
sys.path.insert(0,str(CACHE/"python"))
FONT=CACHE/"NotoSansThai-Regular.ttf"; LICENSE=THAI/"licenses/OFL-NotoSansThai.txt"
SPEC_PATH=THAI/"font/thai_font_spec.json"; GENERATED=THAI/"generated"; RASTER_DIR=GENERATED/"noto_rasterized"
EXPECTED_SHA256="404ddfb5ed0aaa6b6ec8a85700d682978992062d67da93903967b56cbd9a4acc"
CONSONANTS="กขคฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรลวศษสหฬอฮ"
VOWELS_MARKS="ะัาำิีึืุูเแโใไ็่้๊๋์ํ"; PUNCTUATION="ๆฯ฿"; CHARACTERS=CONSONANTS+VOWELS_MARKS+PUNCTUATION
PROOF_LINES=("เริ่มเกมส์","โปเกมอน","ผู้เล่น","น้ำ เก็บไว้","ญี่ปุ่น","ความสามารถ")
UPPER=set("ัิีึื็ํ"); LOWER=set("ุู"); TONE=set("่้๊๋์"); LEADING=set("เแโใไ"); SPACING=set("ะาำ")
def glyph_class(c):
    if c in CONSONANTS:return "base"
    if c in UPPER:return "upper"
    if c in LOWER:return "lower"
    if c in TONE:return "tone"
    if c in LEADING:return "leading"
    if c in SPACING:return "spacing"
    return "punctuation"
def spec():return json.loads(SPEC_PATH.read_text(encoding="utf-8"))
def sha256(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def require_source():
    if not FONT.exists():raise FileNotFoundError(f"missing source font: {FONT}")
    if sha256(FONT)!=EXPECTED_SHA256:raise ValueError("Noto source SHA256 mismatch")
