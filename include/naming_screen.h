#ifndef GUARD_NAMING_SCREEN_H
#define GUARD_NAMING_SCREEN_H

#include "main.h"

enum {
    NAMING_SCREEN_PLAYER,
    NAMING_SCREEN_BOX,
    NAMING_SCREEN_CAUGHT_MON,
    NAMING_SCREEN_NICKNAME,
    NAMING_SCREEN_WALDA,
#ifdef THAI_NAMING_KEYBOARD_K3C
    NAMING_SCREEN_THAI_PROTOTYPE,
#endif
};

void DoNamingScreen(u8 templateNum, u8 *destBuffer, u16 monSpecies, u16 monGender, u32 monPersonality, MainCallback returnCallback);
#ifdef THAI_NAMING_KEYBOARD_K3C
void DoThaiNamingScreenPrototype(MainCallback returnCallback);
#endif

#endif // GUARD_NAMING_SCREEN_H
