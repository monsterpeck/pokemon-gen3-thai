#include "global.h"
#include "data.h"
#include "constants/moves.h"

static const u8 sMoveNameThai_Scratch[] = _("ข่วน");
static const u8 sMoveNameThai_Growl[] = _("คำราม");
static const u8 sMoveNameThai_FocusEnergy[] = _("รวมพลัง");

const u8 *GetMoveName(u16 move)
{
    switch (move)
    {
    case MOVE_SCRATCH:
        return sMoveNameThai_Scratch;
    case MOVE_GROWL:
        return sMoveNameThai_Growl;
    case MOVE_FOCUS_ENERGY:
        return sMoveNameThai_FocusEnergy;
    default:
        if (move >= MOVES_COUNT)
            move = MOVE_NONE;

        return gMoveNames[move];
    }
}
