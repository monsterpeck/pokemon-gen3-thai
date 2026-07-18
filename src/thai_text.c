#include "global.h"
#include "thai_text.h"

#include "data/thai_text_metadata.inc"

const struct ThaiGlyphInfo *GetThaiGlyphInfo(u16 glyphId)
{
    if (glyphId >= THAI_GLYPH_LIMIT)
        return NULL;
    return &gThaiGlyphInfo[glyphId];
}

const struct ThaiBaseMetrics *GetThaiBaseMetrics(u16 glyphId)
{
    u16 i;

    for (i = 0; i < gThaiBaseMetricsCount; i++)
    {
        if (gThaiBaseMetrics[i].glyphId == glyphId)
            return &gThaiBaseMetrics[i];
    }
    return NULL;
}

bool32 IsThaiGlyphId(u16 glyphId)
{
    const struct ThaiGlyphInfo *info = GetThaiGlyphInfo(glyphId);
    return info != NULL && info->class != THAI_CLASS_NONE;
}

bool32 IsThaiCombiningClass(u8 glyphClass)
{
    return glyphClass == THAI_CLASS_UPPER_VOWEL
        || glyphClass == THAI_CLASS_LOWER_VOWEL
        || glyphClass == THAI_CLASS_TONE
        || glyphClass == THAI_CLASS_THAN_THAKHAT
        || glyphClass == THAI_CLASS_NIKHAHIT;
}
