#ifndef GUARD_THAI_NAME_H
#define GUARD_THAI_NAME_H

#include "global.h"
#include "constants/global.h"

#ifdef THAI_NAMING_PRODUCTION

#define THAI_NAME_MAX_SOURCE_LENGTH POKEMON_NAME_LENGTH
#define THAI_NAME_SHAPED_CAPACITY ((THAI_NAME_MAX_SOURCE_LENGTH * 8) + 1)

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
