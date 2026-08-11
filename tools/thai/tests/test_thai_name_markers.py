#!/usr/bin/env python3

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[3]

GLOBAL_H = (ROOT / "include/global.h").read_text(encoding="utf-8")
POKEMON_H = (ROOT / "include/pokemon.h").read_text(encoding="utf-8")
THAI_H = (ROOT / "include/thai_name.h").read_text(encoding="utf-8")
THAI_C = (ROOT / "src/thai_name.c").read_text(encoding="utf-8")
POKEMON_C = (ROOT / "src/pokemon.c").read_text(encoding="utf-8")
STORAGE_C = (ROOT / "src/pokemon_storage_system.c").read_text(encoding="utf-8")


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def test_marker_field_layout():
    require(
        re.search(
            r"#ifdef THAI_NAMING_PRODUCTION\s+"
            r"u16 playerNameIsThai:1;\s+"
            r"u16 padding1:3;\s+"
            r"#else\s+"
            r"//u16 padding1:4;\s+"
            r"#endif",
            GLOBAL_H,
        ),
        "SaveBlock2 production marker layout missing",
    )

    require(
        re.search(
            r"#ifdef THAI_NAMING_PRODUCTION\s+"
            r"u8 nicknameIsThai:1;\s+"
            r"u8 unused:3;\s+"
            r"#else\s+"
            r"u8 unused:4;\s+"
            r"#endif",
            POKEMON_H,
        ),
        "BoxPokemon production marker layout missing",
    )


def test_marker_constants():
    require(
        "#define THAI_BOX_NAME_WALLPAPER_FLAG 0x80" in THAI_H,
        "box-name marker flag must be 0x80",
    )
    require(
        "#define THAI_BOX_WALLPAPER_ID_MASK   0x7F" in THAI_H,
        "wallpaper ID mask must be 0x7F",
    )


def test_player_marker_model():
    value = 0

    value |= 1
    require(value == 1, "player marker set failed")

    value = 0
    require(value == 0, "player marker clear failed")

    require(
        "gSaveBlock2Ptr->playerNameIsThai = isThai ? TRUE : FALSE;" in THAI_C,
        "player marker setter contract missing",
    )


def test_pokemon_marker_model():
    value = 0

    value |= 1
    require(value == 1, "pokemon marker set failed")

    value = 0
    require(value == 0, "pokemon marker clear failed")

    require(
        "boxMon->nicknameIsThai = isThai ? TRUE : FALSE;" in THAI_C,
        "pokemon marker setter contract missing",
    )


def test_box_marker_model():
    FLAG = 0x80
    MASK = 0x7F

    for wallpaper in range(0x80):
        raw = wallpaper

        raw |= FLAG
        require((raw & FLAG) != 0, "box marker set failed")
        require((raw & MASK) == wallpaper, "box marker changed wallpaper ID")

        raw &= MASK
        require((raw & FLAG) == 0, "box marker clear failed")
        require(raw == wallpaper, "box marker clear changed wallpaper ID")


def test_wallpaper_getter_masks_marker():
    require(
        re.search(
            r"static u8 GetBoxWallpaper\(u8 boxId\).*?"
            r"#ifdef THAI_NAMING_PRODUCTION.*?"
            r"boxWallpapers\[boxId\]\s*&\s*THAI_BOX_WALLPAPER_ID_MASK",
            STORAGE_C,
            re.S,
        ),
        "GetBoxWallpaper does not mask Thai marker",
    )


def test_wallpaper_setter_preserves_marker():
    require(
        re.search(
            r"thaiNameFlag\s*=\s*gPokemonStoragePtr->boxWallpapers\[boxId\]\s*"
            r"&\s*THAI_BOX_NAME_WALLPAPER_FLAG",
            STORAGE_C,
            re.S,
        ),
        "SetBoxWallpaper does not capture existing Thai marker",
    )

    require(
        re.search(
            r"boxWallpapers\[boxId\]\s*=\s*thaiNameFlag\s*\|\s*wallpaperId",
            STORAGE_C,
        ),
        "SetBoxWallpaper does not preserve Thai marker",
    )


def test_storage_reset_clears_marker():
    reset_match = re.search(
        r"void ResetPokemonStorageSystem\(void\)\s*\{(.*?)\n\}",
        STORAGE_C,
        re.S,
    )
    require(reset_match is not None, "ResetPokemonStorageSystem not found")

    body = reset_match.group(1)

    clear_pos = body.find("SetBoxNameThai(boxId, FALSE);")
    wallpaper_pos = body.find(
        "SetBoxWallpaper(boxId, boxId % (MAX_DEFAULT_WALLPAPER + 1));"
    )

    require(clear_pos >= 0, "storage reset does not clear Thai box-name marker")
    require(wallpaper_pos >= 0, "storage reset wallpaper initialization missing")
    require(
        clear_pos < wallpaper_pos,
        "Thai box-name marker must be cleared before wallpaper initialization",
    )


def test_normal_nickname_write_clears_marker():
    write = "boxMon->nickname[i] = data[i];"
    clear = "SetBoxMonNicknameThai(boxMon, FALSE);"

    write_pos = POKEMON_C.find(write)
    require(write_pos >= 0, "nickname byte write missing")

    # The production marker clear must belong to the MON_DATA_NICKNAME
    # setter containing the raw nickname write, not the earlier getter case.
    case_pos = POKEMON_C.rfind("case MON_DATA_NICKNAME:", 0, write_pos)
    require(case_pos >= 0, "MON_DATA_NICKNAME setter case not found")

    break_pos = POKEMON_C.find("break;", write_pos)
    require(break_pos >= 0, "MON_DATA_NICKNAME setter break not found")

    clear_pos = POKEMON_C.find(clear, write_pos, break_pos)
    require(clear_pos >= 0, "ordinary nickname write does not clear Thai marker")

    require(
        write_pos < clear_pos < break_pos,
        "Thai nickname marker must be cleared after nickname bytes are written",
    )

def test_raw_box_wallpaper_access_allowlist():
    offenders = []

    for path in sorted((ROOT / "src").rglob("*.c")):
        text = path.read_text(encoding="utf-8", errors="replace")

        if "boxWallpapers[" not in text:
            continue

        rel = path.relative_to(ROOT).as_posix()

        if rel not in {
            "src/thai_name.c",
            "src/pokemon_storage_system.c",
        }:
            offenders.append(rel)

    require(
        not offenders,
        "raw boxWallpapers access outside marker/wallpaper API: "
        + ", ".join(offenders),
    )


TESTS = [
    test_marker_field_layout,
    test_marker_constants,
    test_player_marker_model,
    test_pokemon_marker_model,
    test_box_marker_model,
    test_wallpaper_getter_masks_marker,
    test_wallpaper_setter_preserves_marker,
    test_storage_reset_clears_marker,
    test_normal_nickname_write_clears_marker,
    test_raw_box_wallpaper_access_allowlist,
]


for test in TESTS:
    test()
    print(f"PASS: {test.__name__}")

print(f"PASS: {len(TESTS)} Thai-name marker contract groups")
