# PekeEmerald Thai Font Handover

## CURRENT PRODUCTION = 765

Authoritative production Thai font baseline for all future PekeEmerald translation and shaping work.

- Active map: `tools/thai/font/thai_precompose_glyph_map.json`
- Active atlas: `graphics/fonts/thai_shaped.png`
- Glyphs: **765** (`0..764`)
- Tail: `761=ษั`, `762=จุ้`, `763=ง็`, `764=ฬิ`
- Remaining atlas slots: **3** (`765..767`)
- MAP SHA-256: `6f1f8b33ba5acb4d092cd40e2b6da254a54ebde1a48589e2dbcf3bbb8b79d39c`
- ATLAS SHA-256: `57b1c08e5c9a3aecaad3d9af622b2153e8dd0677fb10f74f9527ff4cb010fbc2`

### Production policy

- Use this active 765-glyph set for all future translation/shaping.
- Do not fall back to the historical 761 snapshot or sandbox copies.
- Check new translated text against the active 765 map first.
- Add glyphs only for an actual unsupported-cluster blocker.
- New glyphs are append-only; never reorder indices `0..764`.
- Future translation follows the locked Context Rules and Japanese-based canonical Pokémon names.

