#ifndef GUARD_THAI_NAME_H
#define GUARD_THAI_NAME_H

#include "global.h"
#include "constants/global.h"

#ifdef THAI_NAMING_PRODUCTION

#define THAI_NAME_MAX_SOURCE_LENGTH POKEMON_NAME_LENGTH
#define THAI_NAME_SHAPED_CAPACITY ((THAI_NAME_MAX_SOURCE_LENGTH * 8) + 1)
#define THAI_PLAYER_NAME_SHAPED_CAPACITY ((PLAYER_NAME_LENGTH * 8) + 1)

#define THAI_BOX_NAME_WALLPAPER_FLAG 0x80
#define THAI_BOX_WALLPAPER_ID_MASK   0x7F

struct BoxPokemon;

bool32 IsPlayerNameThai(void);
void SetPlayerNameThai(bool32 isThai);
const u8 *GetPlayerNameForDisplay(void);

bool32 IsBoxMonNicknameThai(const struct BoxPokemon *boxMon);
void SetBoxMonNicknameThai(struct BoxPokemon *boxMon, bool32 isThai);

bool32 IsBoxNameThai(u8 boxId);
void SetBoxNameThai(u8 boxId, bool32 isThai);

bool32 IsThaiCompactNameId(u8 compactId);

bool32 ThaiShapeCompactName(
    const u8 *source,
    u8 length,
    u8 maxChars,
    u8 *destination,
    u16 destinationCapacity
);

#endif // THAI_NAMING_PRODUCTION

#endif // GUARD_THAI_NAME_H
