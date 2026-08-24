#include "global.h"
#include "data.h"
#include "thai_name.h"
#include "string_util.h"
#include "international_string_util.h"
#include "data/text/thai_species_names.inc"

#ifdef THAI_NAMING_PRODUCTION

#include "constants/characters.h"
#include "load_save.h"
#include "pokemon.h"
#include "pokemon_storage_system.h"

STATIC_ASSERT(sizeof(struct SaveBlock2) == 0xF2C, ThaiNamingSaveBlock2Size);
STATIC_ASSERT(sizeof(struct BoxPokemon) == 80, ThaiNamingBoxPokemonSize);

static EWRAM_DATA u8 sThaiPlayerNameDisplay[THAI_PLAYER_NAME_SHAPED_CAPACITY];
static const u8 sInvalidThaiPlayerName[] = {CHAR_QUESTION_MARK, EOS};

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

bool32 IsPlayerNameThai(void)
{
    return gSaveBlock2Ptr != NULL && gSaveBlock2Ptr->playerNameIsThai;
}

void SetPlayerNameThai(bool32 isThai)
{
    if (gSaveBlock2Ptr != NULL)
        gSaveBlock2Ptr->playerNameIsThai = isThai ? TRUE : FALSE;
}

const u8 *GetPlayerNameForDisplay(void)
{
    u8 length = 0;

    if (gSaveBlock2Ptr == NULL)
        return sInvalidThaiPlayerName;

    if (!IsPlayerNameThai())
        return gSaveBlock2Ptr->playerName;

    while (length < PLAYER_NAME_LENGTH
        && gSaveBlock2Ptr->thaiPlayerName[length] != EOS)
        length++;

    if (!ThaiShapeCompactName(gSaveBlock2Ptr->thaiPlayerName,
                              length,
                              PLAYER_NAME_LENGTH,
                              sThaiPlayerNameDisplay,
                              sizeof(sThaiPlayerNameDisplay)))
        return sInvalidThaiPlayerName;

    return sThaiPlayerNameDisplay;
}

bool32 IsBoxMonNicknameThai(const struct BoxPokemon *boxMon)
{
    return boxMon != NULL && boxMon->nicknameIsThai;
}

void SetBoxMonNicknameThai(struct BoxPokemon *boxMon, bool32 isThai)
{
    if (boxMon != NULL)
        boxMon->nicknameIsThai = isThai ? TRUE : FALSE;
}

bool32 IsBoxNameThai(u8 boxId)
{
    if (gPokemonStoragePtr == NULL || boxId >= TOTAL_BOXES_COUNT)
        return FALSE;

    return (gPokemonStoragePtr->boxWallpapers[boxId]
          & THAI_BOX_NAME_WALLPAPER_FLAG) != 0;
}

void SetBoxNameThai(u8 boxId, bool32 isThai)
{
    if (gPokemonStoragePtr == NULL || boxId >= TOTAL_BOXES_COUNT)
        return;

    if (isThai)
        gPokemonStoragePtr->boxWallpapers[boxId] |= THAI_BOX_NAME_WALLPAPER_FLAG;
    else
        gPokemonStoragePtr->boxWallpapers[boxId] &= THAI_BOX_WALLPAPER_ID_MASK;
}

bool32 IsThaiCompactNameId(u8 compactId)
{
    return (compactId >= 0x37 && compactId <= 0x50)
        || (compactId >= 0x5E && compactId <= 0x67)
        || (compactId >= 0x69 && compactId <= 0x6E)
        || (compactId >= 0x70 && compactId <= 0x76)
        || compactId == 0x78
        || (compactId >= 0x7D && compactId <= 0x83)
        || (compactId >= 0x87 && compactId <= 0x8E);
}

static bool32 RuntimeKeyMatches(
    const struct ThaiNamingRuntimeMapEntry *entry,
    const u8 *source,
    u8 remaining
)
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

bool32 FitThaiPositionedGlyphAdvances(u8 *text, u32 originalWidth, u32 maxWidth, u8 minAdvance)
{
    u32 i;
    bool32 changed = FALSE;

    if (originalWidth <= maxWidth || originalWidth == 0)
        return FALSE;

    for (i = 0; text[i] != EOS;)
    {
        /* FC19: begin, Thai positioned glyph, glyph lo/hi, x, y, advance, flags. */
        if (text[i] == 0xFC && text[i + 1] == 0x19)
        {
            u32 advance = text[i + 6];
            u32 scaled = (advance * maxWidth) / originalWidth;

            if (scaled < minAdvance)
                scaled = minAdvance;
            if (scaled > advance)
                scaled = advance;

            if (scaled < advance)
            {
                text[i + 6] = scaled;
                changed = TRUE;
            }

            i += 8;
        }
        else
        {
            i++;
        }
    }

    return changed;
}


bool32 ThaiShapeCompactName(
    const u8 *source,
    u8 length,
    u8 maxChars,
    u8 *destination,
    u16 destinationCapacity
)
{
    u8 temporary[THAI_NAME_SHAPED_CAPACITY];
    u8 sourcePos = 0;
    u16 destinationPos = 0;
    u16 mapPos;

    if (source == NULL || destination == NULL)
        return FALSE;

    if (maxChars > THAI_NAME_MAX_SOURCE_LENGTH || length > maxChars)
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

        if (!IsThaiCompactNameId(source[sourcePos]))
        {
            /*
             * Mixed Thai/Western naming:
             * 0xA1..0xF6 are the existing one-byte Western printable
             * characters used for digits, punctuation, A-Z and a-z.
             *
             * Keep 0xF7+ rejected: those values are dynamic/control/prefix
             * bytes and must never be copied through as ordinary name text.
             */
            if (source[sourcePos] < 0xA1 || source[sourcePos] > 0xF6)
                return FALSE;

            if (destinationPos + 1 >= sizeof(temporary))
                return FALSE;

            temporary[destinationPos++] = source[sourcePos++];
            continue;
        }

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


const u8 *GetSpeciesNameForDisplay(u16 species)
{
    if (species < NUM_SPECIES && sThaiSpeciesNames[species] != NULL)
        return sThaiSpeciesNames[species];

    if (species < NUM_SPECIES)
        return gSpeciesNames[species];

    return gSpeciesNames[SPECIES_NONE];
}


bool32 CopyMonNameForDisplay(struct Pokemon *mon, u8 *destination, u16 destinationCapacity)
{
    u8 nickname[POKEMON_NAME_LENGTH + 1];
    const u8 *display;
    u16 species;

    if (destination == NULL || destinationCapacity == 0)
        return FALSE;

    species = GetMonData(mon, MON_DATA_SPECIES);
    GetMonData(mon, MON_DATA_NICKNAME, nickname);

    if (IsBoxMonNicknameThai(&mon->box))
    {
        if (ThaiShapeCompactName(
                nickname,
                StringLength(nickname),
                POKEMON_NAME_LENGTH,
                destination,
                destinationCapacity))
            return TRUE;

        display = GetSpeciesNameForDisplay(species);
    }
    else
    {
        StringGet_Nickname(nickname);

        if (species < NUM_SPECIES
         && StringCompare(nickname, gSpeciesNames[species]) == 0)
            display = GetSpeciesNameForDisplay(species);
        else
            display = nickname;
    }

    if (StringLength(display) + 1 > destinationCapacity)
        return FALSE;

    StringCopy(destination, display);
    return TRUE;
}



bool32 CopyBoxMonNameForDisplay(
    struct BoxPokemon *mon,
    u8 *destination,
    u16 destinationCapacity)
{
    u16 species;
    u8 nickname[POKEMON_NAME_BUFFER_SIZE];
    const u8 *display;

    if (mon == NULL || destination == NULL || destinationCapacity == 0)
        return FALSE;

    species = GetBoxMonData(mon, MON_DATA_SPECIES);
    GetBoxMonData(mon, MON_DATA_NICKNAME, nickname);

    if (IsBoxMonNicknameThai(mon))
    {
        if (ThaiShapeCompactName(
                nickname,
                StringLength(nickname),
                POKEMON_NAME_LENGTH,
                destination,
                destinationCapacity))
            return TRUE;

        display = GetSpeciesNameForDisplay(species);
    }
    else
    {
        StringGet_Nickname(nickname);

        if (species < NUM_SPECIES
         && StringCompare(nickname, gSpeciesNames[species]) == 0)
            display = GetSpeciesNameForDisplay(species);
        else
            display = nickname;
    }

    if (StringLength(display) + 1 > destinationCapacity)
        return FALSE;

    StringCopy(destination, display);
    return TRUE;
}

bool32 CopyStoredMonNameForDisplay(
    u16 species,
    const u8 *nickname,
    u8 *destination,
    u16 destinationCapacity)
{
    u8 normalized[POKEMON_NAME_LENGTH + 1];
    const u8 *display;
    u8 i;
    bool32 hasThaiCompact = FALSE;

    if (nickname == NULL || destination == NULL || destinationCapacity == 0)
        return FALSE;

    for (i = 0; i < POKEMON_NAME_LENGTH && nickname[i] != EOS; i++)
        normalized[i] = nickname[i];
    normalized[i] = EOS;

    StringGet_Nickname(normalized);

    if (species < NUM_SPECIES
     && StringCompare(normalized, gSpeciesNames[species]) == 0)
    {
        display = GetSpeciesNameForDisplay(species);
        if (StringLength(display) + 1 > destinationCapacity)
            return FALSE;

        StringCopy(destination, display);
        return TRUE;
    }

    for (i = 0; normalized[i] != EOS; i++)
    {
        if (IsThaiCompactNameId(normalized[i]))
        {
            hasThaiCompact = TRUE;
            break;
        }
    }

    if (hasThaiCompact
     && ThaiShapeCompactName(
            normalized,
            StringLength(normalized),
            POKEMON_NAME_LENGTH,
            destination,
            destinationCapacity))
        return TRUE;

    if (StringLength(normalized) + 1 > destinationCapacity)
        return FALSE;

    StringCopy(destination, normalized);
    return TRUE;
}

#endif // THAI_NAMING_PRODUCTION

#ifndef THAI_NAMING_PRODUCTION
const u8 *GetSpeciesNameForDisplay(u16 species)
{
    if (species < NUM_SPECIES)
        return gSpeciesNames[species];

    return gSpeciesNames[SPECIES_NONE];
}
#endif
