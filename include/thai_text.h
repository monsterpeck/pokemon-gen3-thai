#ifndef GUARD_THAI_TEXT_H
#define GUARD_THAI_TEXT_H

#include "global.h"

#define THAI_GLYPH_LIMIT 0x200
#define THAI_GLYPH_SARA_AA 0x11C
#define THAI_GLYPH_NIKHAHIT 0x156
#define THAI_FALLBACK_MARK_ADVANCE 4

enum ThaiGlyphClass
{
    THAI_CLASS_NONE,
    THAI_CLASS_BASE,
    THAI_CLASS_LEADING_VOWEL,
    THAI_CLASS_SPACING_VOWEL,
    THAI_CLASS_UPPER_VOWEL,
    THAI_CLASS_LOWER_VOWEL,
    THAI_CLASS_TONE,
    THAI_CLASS_THAN_THAKHAT,
    THAI_CLASS_NIKHAHIT,
    THAI_CLASS_SARA_AM,
    THAI_CLASS_PUNCTUATION,
};

enum ThaiBaseShapeGroup
{
    THAI_SHAPE_NORMAL,
    THAI_SHAPE_TALL,
    THAI_SHAPE_WIDE,
    THAI_SHAPE_DESCENDER,
    THAI_SHAPE_SPECIAL,
};

struct ThaiGlyphInfo
{
    u8 class;
    u8 advance;
    s8 markOffsetX;
    s8 markOffsetY;
    s8 secondLevelOffsetY;
    u16 componentGlyphId;
};

struct ThaiBaseMetrics
{
    u16 glyphId;
    u8 advance;
    s8 upperAnchorX;
    s8 upperAnchorY;
    s8 lowerAnchorX;
    s8 lowerAnchorY;
    s8 toneAnchorX;
    s8 toneAnchorY;
    u8 shapeGroup;
};

extern const struct ThaiGlyphInfo gThaiGlyphInfo[THAI_GLYPH_LIMIT];
extern const struct ThaiBaseMetrics gThaiBaseMetrics[];
extern const u16 gThaiBaseMetricsCount;

const struct ThaiGlyphInfo *GetThaiGlyphInfo(u16 glyphId);
const struct ThaiBaseMetrics *GetThaiBaseMetrics(u16 glyphId);
bool32 IsThaiGlyphId(u16 glyphId);
bool32 IsThaiCombiningClass(u8 glyphClass);

#ifdef THAI_NAMING_KEYBOARD_K3C
#define THAI_COMPACT_PROTOTYPE_COUNT 65
#define THAI_NAMING_SHAPED_CAPACITY 57

bool32 IsThaiCompactPrototypeId(u8 compactId);
bool32 ThaiShapeCompactPrototype(const u8 *source, u8 length, u8 sourceCapacity,
                                 u8 *destination, u16 destinationCapacity);
#endif

#endif
