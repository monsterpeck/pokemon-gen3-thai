#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

DATA_HEADER = ROOT / "include/data.h"
GLOBAL_HEADER = ROOT / "include/constants/global.h"
BATTLE_MESSAGE_HEADER = ROOT / "include/battle_message.h"
BATTLE_HEADER = ROOT / "include/battle.h"

BATTLE_MAIN = ROOT / "src/battle_main.c"
BATTLE_MESSAGE = ROOT / "src/battle_message.c"
BATTLE_CONTROLLER_PLAYER = ROOT / "src/battle_controller_player.c"
POKEMON_SUMMARY = ROOT / "src/pokemon_summary_screen.c"
MOVE_RELEARNER = ROOT / "src/move_relearner.c"
CONTEST = ROOT / "src/contest.c"
TRADE = ROOT / "src/trade.c"
SCRCMD = ROOT / "src/scrcmd.c"
APPRENTICE = ROOT / "src/apprentice.c"
ITEM_MENU = ROOT / "src/item_menu.c"
EASY_CHAT = ROOT / "src/easy_chat.c"

MOVE_NAME_SOURCE = ROOT / "src/move_names.c"

RUNTIME_BUFFER_SIZE = 128
MOVE_LIST_BUFFER_SIZE = 520


def fail(message: str) -> None:
    raise SystemExit(f"ERROR: {message}")


def read(path: Path) -> str:
    if not path.is_file():
        fail(f"ไม่พบไฟล์ {path.relative_to(ROOT)}")

    return path.read_text(encoding="utf-8")


def replace_exact(
    source: str,
    old: str,
    new: str,
    label: str,
    expected: int = 1,
) -> str:
    count = source.count(old)

    if count != expected:
        fail(
            f"{label}: คาดว่าจะพบ {expected} จุด "
            f"แต่พบ {count} จุด"
        )

    return source.replace(old, new)


def main() -> int:
    tracked_paths = (
        DATA_HEADER,
        GLOBAL_HEADER,
        BATTLE_MESSAGE_HEADER,
        BATTLE_HEADER,
        BATTLE_MAIN,
        BATTLE_MESSAGE,
        BATTLE_CONTROLLER_PLAYER,
        POKEMON_SUMMARY,
        MOVE_RELEARNER,
        CONTEST,
        TRADE,
        SCRCMD,
        APPRENTICE,
        ITEM_MENU,
        EASY_CHAT,
    )

    sources = {
        path: read(path)
        for path in tracked_paths
    }

    if "MOVE_NAME_RUNTIME_BUFFER_SIZE" in sources[GLOBAL_HEADER]:
        fail(
            "ตรวจพบ Runtime Proof ติดตั้งอยู่แล้ว "
            "จึงหยุดเพื่อป้องกันการแก้ซ้ำ"
        )

    if MOVE_NAME_SOURCE.exists():
        fail(
            "พบ src/move_names.c อยู่แล้ว "
            "กรุณาตรวจสอบก่อนติดตั้งซ้ำ"
        )

    original_decl = (
        "extern const u8 "
        "gMoveNames[MOVES_COUNT]"
        "[MOVE_NAME_LENGTH + 1];"
    )

    sources[DATA_HEADER] = replace_exact(
        sources[DATA_HEADER],
        original_decl,
        (
            original_decl
            + "\n"
            + "const u8 *GetMoveName(u16 move);"
        ),
        "Add GetMoveName declaration",
    )

    sources[GLOBAL_HEADER] = replace_exact(
        sources[GLOBAL_HEADER],
        "#define MOVE_NAME_LENGTH 12",
        (
            "#define MOVE_NAME_LENGTH 12\n"
            "\n"
            "// Encoded Thai move-name buffers. "
            "Includes EOS and control codes.\n"
            "#define MOVE_NAME_RUNTIME_BUFFER_SIZE "
            f"{RUNTIME_BUFFER_SIZE}\n"
            "#define MOVE_NAMES_LIST_BUFFER_SIZE "
            f"{MOVE_LIST_BUFFER_SIZE}"
        ),
        "Add move-name runtime constants",
    )

    sources[BATTLE_MESSAGE_HEADER] = replace_exact(
        sources[BATTLE_MESSAGE_HEADER],
        "\n// for 0xFD\n",
        (
            "\n"
            "#define BATTLE_TEXT_BUFFER_SIZE "
            "max(TEXT_BUFF_ARRAY_COUNT, "
            "MOVE_NAME_RUNTIME_BUFFER_SIZE)\n"
            "\n"
            "// for 0xFD\n"
        ),
        "Add local battle buffer size",
    )

    battle_header = sources[BATTLE_HEADER]

    for number in (1, 2, 3):
        battle_header = replace_exact(
            battle_header,
            (
                f"extern u8 gBattleTextBuff{number}"
                "[TEXT_BUFF_ARRAY_COUNT];"
            ),
            (
                f"extern u8 gBattleTextBuff{number}"
                "[BATTLE_TEXT_BUFFER_SIZE];"
            ),
            f"Resize battle buffer {number} declaration",
        )

    sources[BATTLE_HEADER] = battle_header

    battle_main = sources[BATTLE_MAIN]

    for number in (1, 2, 3):
        battle_main = replace_exact(
            battle_main,
            (
                f"EWRAM_DATA u8 gBattleTextBuff{number}"
                "[TEXT_BUFF_ARRAY_COUNT] = {0};"
            ),
            (
                f"EWRAM_DATA u8 gBattleTextBuff{number}"
                "[BATTLE_TEXT_BUFFER_SIZE] = {0};"
            ),
            f"Resize battle buffer {number} storage",
        )

    sources[BATTLE_MAIN] = battle_main

    # Battle message paths
    battle_message = sources[BATTLE_MESSAGE]

    battle_message = replace_exact(
        battle_message,
        (
            "StringCopy(gBattleTextBuff2, "
            "gMoveNames[gBattleMsgDataPtr->currentMove]);"
        ),
        (
            "StringCopy(gBattleTextBuff2, "
            "GetMoveName(gBattleMsgDataPtr->currentMove));"
        ),
        "Battle used-move buffer",
    )

    battle_message = replace_exact(
        battle_message,
        (
            "toCpy = "
            "gMoveNames[gBattleMsgDataPtr->currentMove];"
        ),
        (
            "toCpy = "
            "GetMoveName(gBattleMsgDataPtr->currentMove);"
        ),
        "Battle current-move pointer",
    )

    battle_message = replace_exact(
        battle_message,
        (
            "toCpy = "
            "gMoveNames[gBattleMsgDataPtr->originallyUsedMove];"
        ),
        (
            "toCpy = "
            "GetMoveName("
            "gBattleMsgDataPtr->originallyUsedMove);"
        ),
        "Battle original-move pointer",
    )

    battle_message = replace_exact(
        battle_message,
        (
            "StringAppend(dst, "
            "gMoveNames[T1_READ_16(&src[srcID + 1])]);"
        ),
        (
            "StringAppend(dst, "
            "GetMoveName(T1_READ_16(&src[srcID + 1])));"
        ),
        "Battle placeholder move name",
    )

    sources[BATTLE_MESSAGE] = battle_message

    sources[BATTLE_CONTROLLER_PLAYER] = replace_exact(
        sources[BATTLE_CONTROLLER_PLAYER],
        (
            "StringCopy(gDisplayedStringBattle, "
            "gMoveNames[moveInfo->moves[i]]);"
        ),
        (
            "StringCopy(gDisplayedStringBattle, "
            "GetMoveName(moveInfo->moves[i]));"
        ),
        "Battle move-selection display",
    )

    # Summary screen
    summary = sources[POKEMON_SUMMARY]

    summary = replace_exact(
        summary,
        (
            "PrintTextOnWindow(moveNameWindowId, "
            "gMoveNames[move], 0, "
            "moveIndex * 16 + 1, 0, 1);"
        ),
        (
            "PrintTextOnWindow(moveNameWindowId, "
            "GetMoveName(move), 0, "
            "moveIndex * 16 + 1, 0, 1);"
        ),
        "Summary move list",
    )

    summary = replace_exact(
        summary,
        (
            "PrintTextOnWindow(windowId1, "
            "gMoveNames[move], 0, 65, 0, 6);"
        ),
        (
            "PrintTextOnWindow(windowId1, "
            "GetMoveName(move), 0, 65, 0, 6);"
        ),
        "Summary move detail enabled",
    )

    summary = replace_exact(
        summary,
        (
            "PrintTextOnWindow(windowId1, "
            "gMoveNames[move], 0, 65, 0, 5);"
        ),
        (
            "PrintTextOnWindow(windowId1, "
            "GetMoveName(move), 0, 65, 0, 5);"
        ),
        "Summary move detail disabled",
    )

    # Move the PP text 8 pixels left so the final digit
    # is not clipped by the right-side Summary frame.
    summary = replace_exact(
        summary,
        (
            "x = GetStringRightAlignXOffset("
            "FONT_NORMAL, text, 44);"
        ),
        (
            "x = GetStringRightAlignXOffset("
            "FONT_NORMAL, text, 36);"
        ),
        "Move PP right alignment",
    )

    summary = replace_exact(
        summary,
        (
            "GetStringRightAlignXOffset("
            "FONT_NORMAL, gStringVar4, 44)"
        ),
        (
            "GetStringRightAlignXOffset("
            "FONT_NORMAL, gStringVar4, 36)"
        ),
        "New move PP right alignment",
    )

    sources[POKEMON_SUMMARY] = summary

    # Move Relearner
    relearner = sources[MOVE_RELEARNER]

    relearner = replace_exact(
        relearner,
        (
            "StringCopy(gStringVar2, "
            "gMoveNames[GetCurrentSelectedMove()]);"
        ),
        (
            "StringCopy(gStringVar2, "
            "GetMoveName(GetCurrentSelectedMove()));"
        ),
        "Move Relearner selected move",
        expected=2,
    )

    relearner = replace_exact(
        relearner,
        "StringCopy(gStringVar3, gMoveNames[move]);",
        "StringCopy(gStringVar3, GetMoveName(move));",
        "Move Relearner move variable",
    )

    relearner = replace_exact(
        relearner,
        "StringCopy(gStringVar2, gMoveNames[itemId]);",
        "StringCopy(gStringVar2, GetMoveName(itemId));",
        "Move Relearner item move",
    )

    relearner = replace_exact(
        relearner,
        (
            "sMoveRelearnerStruct->menuItems[i].name = "
            "gMoveNames["
            "sMoveRelearnerStruct->movesToLearn[i]];"
        ),
        (
            "sMoveRelearnerStruct->menuItems[i].name = "
            "GetMoveName("
            "sMoveRelearnerStruct->movesToLearn[i]);"
        ),
        "Move Relearner menu item",
    )

    sources[MOVE_RELEARNER] = relearner

    # Contest and Trade local buffers
    contest = sources[CONTEST]

    contest = replace_exact(
        contest,
        "u8 moveName[32];",
        (
            "u8 moveName"
            "[MOVE_NAME_RUNTIME_BUFFER_SIZE + 8];"
        ),
        "Resize Contest move buffer",
    )

    contest = replace_exact(
        contest,
        (
            "moveNameBuffer = StringCopy("
            "moveNameBuffer, gMoveNames[move]);"
        ),
        (
            "moveNameBuffer = StringCopy("
            "moveNameBuffer, GetMoveName(move));"
        ),
        "Contest move display",
    )

    sources[CONTEST] = contest

    trade = sources[TRADE]

    trade = replace_exact(
        trade,
        "u8 movesString[56];",
        (
            "u8 movesString"
            "[MOVE_NAMES_LIST_BUFFER_SIZE];"
        ),
        "Resize Trade move list",
    )

    trade = replace_exact(
        trade,
        "StringAppend(str, gMoveNames[moves[i]]);",
        "StringAppend(str, GetMoveName(moves[i]));",
        "Trade move list display",
    )

    sources[TRADE] = trade

    sources[SCRCMD] = replace_exact(
        sources[SCRCMD],
        (
            "StringCopy(sScriptStringVars[stringVarIndex], "
            "gMoveNames[move]);"
        ),
        (
            "StringCopy(sScriptStringVars[stringVarIndex], "
            "GetMoveName(move));"
        ),
        "Script move-name buffer",
    )

    apprentice = sources[APPRENTICE]

    apprentice = replace_exact(
        apprentice,
        (
            "StringCopy(stringDst, "
            "gMoveNames[gApprenticeQuestionData->move1]);"
        ),
        (
            "StringCopy(stringDst, "
            "GetMoveName(gApprenticeQuestionData->move1));"
        ),
        "Apprentice move 1",
    )

    apprentice = replace_exact(
        apprentice,
        (
            "StringCopy(stringDst, "
            "gMoveNames[gApprenticeQuestionData->move2]);"
        ),
        (
            "StringCopy(stringDst, "
            "GetMoveName(gApprenticeQuestionData->move2));"
        ),
        "Apprentice move 2",
    )

    sources[APPRENTICE] = apprentice

    sources[ITEM_MENU] = replace_exact(
        sources[ITEM_MENU],
        (
            "StringCopy(gStringVar2, "
            "gMoveNames[ItemIdToBattleMoveId(itemId)]);"
        ),
        (
            "StringCopy(gStringVar2, "
            "GetMoveName("
            "ItemIdToBattleMoveId(itemId)));"
        ),
        "Item menu move name",
    )

    sources[EASY_CHAT] = replace_exact(
        sources[EASY_CHAT],
        "return gMoveNames[index];",
        "return GetMoveName(index);",
        "Easy Chat move name",
    )

    move_name_source = """\
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
"""

    # เขียนไฟล์เมื่อการตรวจทุกจุดผ่านแล้วเท่านั้น
    for path, source in sources.items():
        path.write_text(
            source,
            encoding="utf-8",
        )

    MOVE_NAME_SOURCE.write_text(
        move_name_source,
        encoding="utf-8",
    )

    print("========================================")
    print("MOVE NAME LOOKUP RUNTIME PROOF")
    print("========================================")
    print("Original gMoveNames : PRESERVED")
    print("ROM header          : UNCHANGED")
    print("Thai overrides      : 3")
    print(
        f"Runtime name buffer : "
        f"{RUNTIME_BUFFER_SIZE} bytes"
    )
    print(
        f"Trade list buffer   : "
        f"{MOVE_LIST_BUFFER_SIZE} bytes"
    )
    print()
    print("MOVE_SCRATCH       -> ข่วน")
    print("MOVE_GROWL        -> คำราม")
    print("MOVE_FOCUS_ENERGY  -> รวมพลัง")
    print()
    print(
        "RESULT: MOVE NAME LOOKUP "
        "RUNTIME PROOF INSTALLED"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
