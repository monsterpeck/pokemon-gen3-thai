#include "global.h"
#include "thai_text.h"
#ifdef THAI_NAMING_KEYBOARD_K3C
#include "constants/characters.h"
#endif

#include "data/thai_text_metadata.inc"

#ifdef THAI_NAMING_KEYBOARD_K3C
struct ThaiNamingRuntimeMapEntry
{
    u8 key[7];
    u8 length;
    u16 glyphId;
    s8 x;
    s8 y;
    u8 advance;
    u8 flags;
};

#include "data/thai_naming_runtime_map.inc"

bool32 IsThaiCompactPrototypeId(u8 compactId)
{
    return (compactId >= 0x37 && compactId <= 0x50)
        || (compactId >= 0x5E && compactId <= 0x67)
        || (compactId >= 0x69 && compactId <= 0x6E)
        || (compactId >= 0x70 && compactId <= 0x76)
        || compactId == 0x78
        || (compactId >= 0x7D && compactId <= 0x83)
        || (compactId >= 0x87 && compactId <= 0x8E);
}

static bool32 RuntimeKeyMatches(const struct ThaiNamingRuntimeMapEntry *entry,
                                const u8 *source, u8 remaining)
{
    u8 i;

    if (entry->length > remaining)
        return FALSE;
    for (i = 0; i < entry->length; i++)
    {
        if (entry->key[i] != source[i])
            return FALSE;
    }
    return TRUE;
}

bool32 ThaiShapeCompactPrototype(const u8 *source, u8 length, u8 sourceCapacity,
                                 u8 *destination, u16 destinationCapacity)
{
    u8 temporary[THAI_NAMING_SHAPED_CAPACITY];
    u8 sourcePos = 0;
    u16 destinationPos = 0;
    u16 mapPos;

    if (source == NULL || destination == NULL || sourceCapacity > 7
     || length > sourceCapacity || source[length] != EOS)
        return FALSE;

    while (sourcePos < length)
    {
        const struct ThaiNamingRuntimeMapEntry *match = NULL;
        const struct ThaiNamingRuntimeMapEntry *entry;

        if (source[sourcePos] == CHAR_SPACE)
        {
            if (destinationPos + 1 >= sizeof(temporary))
                return FALSE;
            temporary[destinationPos++] = CHAR_SPACE;
            sourcePos++;
            continue;
        }
        if (!IsThaiCompactPrototypeId(source[sourcePos]))
            return FALSE;

        for (mapPos = 0; mapPos < THAI_NAMING_RUNTIME_MAP_COUNT; mapPos++)
        {
            entry = &sThaiNamingRuntimeMap[mapPos];
            if (RuntimeKeyMatches(entry, source + sourcePos, length - sourcePos))
            {
                match = entry;
                break;
            }
        }
        if (match == NULL || destinationPos + 8 >= sizeof(temporary))
            return FALSE;

        temporary[destinationPos++] = EXT_CTRL_CODE_BEGIN;
        temporary[destinationPos++] = EXT_CTRL_CODE_THAI_POSITIONED_GLYPH;
        temporary[destinationPos++] = match->glyphId;
        temporary[destinationPos++] = match->glyphId >> 8;
        temporary[destinationPos++] = match->x;
        temporary[destinationPos++] = match->y;
        temporary[destinationPos++] = match->advance;
        temporary[destinationPos++] = match->flags;
        sourcePos += match->length;
    }
    temporary[destinationPos++] = EOS;
    if (destinationPos > destinationCapacity)
        return FALSE;
    memcpy(destination, temporary, destinationPos);
    return TRUE;
}
#endif

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
