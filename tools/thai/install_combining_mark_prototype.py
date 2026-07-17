from pathlib import Path
import re
import shutil

from PIL import Image


BASE_FONT_PATH = Path("graphics/fonts/latin_normal.png")
FONTS_SOURCE_PATH = Path("src/fonts.c")
CHARMAP_PATH = Path("charmap.txt")
GLYPH_DIR = Path("graphics/fonts/thai/glyphs")

GLYPH_SIZE = 16

BACKGROUND = 0
MAIN_STROKE = 1
SHADOW = 2

ARRAY_PATTERN = re.compile(
    r"(gFontNormalLatinGlyphWidths\[\]\s*=\s*\{)"
    r"(.*?)"
    r"(\};)",
    re.S,
)

MARKS = [
    {
        "char": "ิ",
        "name": "sara_i",
        "glyph_id": 0x143,
        "mapping": "F9 43",
        "width": 11,
        "pixels": {
            (5, 1),
            (6, 0),
            (7, 0),
            (8, 0),
            (9, 1),
        },
    },
    {
        "char": "่",
        "name": "mai_ek",
        "glyph_id": 0x144,
        "mapping": "F9 44",
        "width": 9,
        "pixels": {
            (7, 0),
            (7, 1),
            (7, 2),
        },
    },
]


def backup_file(path: Path) -> None:
    backup_path = path.with_name(path.name + ".before_combining_proto")
    if not backup_path.exists():
        shutil.copy2(path, backup_path)


def create_palette_glyph(
    palette: list[int],
    pixels: set[tuple[int, int]],
) -> Image.Image:
    image = Image.new(
        mode="P",
        size=(GLYPH_SIZE, GLYPH_SIZE),
        color=BACKGROUND,
    )
    image.putpalette(palette)

    main_pixels = set(pixels)
    shadow_pixels: set[tuple[int, int]] = set()

    for x, y in main_pixels:
        for offset_x, offset_y in ((1, 0), (0, 1)):
            sx = x + offset_x
            sy = y + offset_y

            if not (0 <= sx < GLYPH_SIZE and 0 <= sy < GLYPH_SIZE):
                continue

            if (sx, sy) not in main_pixels:
                shadow_pixels.add((sx, sy))

    for x, y in shadow_pixels:
        image.putpixel((x, y), SHADOW)

    for x, y in main_pixels:
        image.putpixel((x, y), MAIN_STROKE)

    return image


def paste_glyph_to_sheet(
    font_sheet: Image.Image,
    glyph: Image.Image,
    glyph_id: int,
) -> tuple[int, int]:
    columns = font_sheet.width // GLYPH_SIZE
    x = (glyph_id % columns) * GLYPH_SIZE
    y = (glyph_id // columns) * GLYPH_SIZE
    font_sheet.paste(glyph, (x, y))
    return x, y


def ensure_mapping(character: str, mapping: str) -> None:
    source = CHARMAP_PATH.read_text(encoding="utf-8")
    line = f"'{character}' = {mapping}"

    pattern = re.compile(
        rf"^'{re.escape(character)}'\s*=.*$",
        re.M,
    )

    if pattern.search(source):
        updated = pattern.sub(line, source)
    else:
        if not source.endswith("\n"):
            source += "\n"
        updated = source + line + "\n"

    CHARMAP_PATH.write_text(updated, encoding="utf-8")


def set_width(glyph_id: int, new_width: int) -> None:
    source = FONTS_SOURCE_PATH.read_text(encoding="utf-8")
    match = ARRAY_PATTERN.search(source)

    if match is None:
        raise SystemExit(
            "ไม่พบ gFontNormalLatinGlyphWidths ใน src/fonts.c"
        )

    array_body = match.group(2)
    number_matches = list(re.finditer(r"\b\d+\b", array_body))

    if len(number_matches) != 512:
        raise SystemExit(
            f"คาดว่าจะพบ Width 512 ค่า แต่พบ {len(number_matches)} ค่า"
        )

    target = number_matches[glyph_id]
    old_width = int(target.group())

    updated_body = (
        array_body[:target.start()]
        + str(new_width)
        + array_body[target.end():]
    )

    updated_source = (
        source[:match.start(2)]
        + updated_body
        + source[match.end(2):]
    )

    FONTS_SOURCE_PATH.write_text(
        updated_source,
        encoding="utf-8",
    )

    print(
        f"Width updated: 0x{glyph_id:03X} "
        f"{old_width} -> {new_width}"
    )


def main() -> None:
    if not BASE_FONT_PATH.exists():
        raise SystemExit(f"ไม่พบไฟล์: {BASE_FONT_PATH}")

    if not FONTS_SOURCE_PATH.exists():
        raise SystemExit(f"ไม่พบไฟล์: {FONTS_SOURCE_PATH}")

    if not CHARMAP_PATH.exists():
        raise SystemExit(f"ไม่พบไฟล์: {CHARMAP_PATH}")

    GLYPH_DIR.mkdir(parents=True, exist_ok=True)

    backup_file(BASE_FONT_PATH)
    backup_file(FONTS_SOURCE_PATH)
    backup_file(CHARMAP_PATH)

    font_sheet = Image.open(BASE_FONT_PATH)
    palette = font_sheet.getpalette()

    if palette is None:
        raise SystemExit("ไม่พบ palette ใน latin_normal.png")

    print("=== Install Combining Mark Prototype ===")

    for mark in MARKS:
        glyph = create_palette_glyph(
            palette=palette,
            pixels=mark["pixels"],
        )

        glyph_path = GLYPH_DIR / (
            f"{mark['glyph_id']:04X}_{mark['name']}.png"
        )
        glyph.save(glyph_path)

        x, y = paste_glyph_to_sheet(
            font_sheet=font_sheet,
            glyph=glyph,
            glyph_id=mark["glyph_id"],
        )

        ensure_mapping(
            character=mark["char"],
            mapping=mark["mapping"],
        )

        set_width(
            glyph_id=mark["glyph_id"],
            new_width=mark["width"],
        )

        print(
            f"Glyph installed: {mark['char']} "
            f"-> 0x{mark['glyph_id']:03X} "
            f"at X={x}, Y={y}"
        )
        print(f"Saved glyph   : {glyph_path}")
        print(f"Mapping       : '{mark['char']}' = {mark['mapping']}")
        print("")

    font_sheet.save(BASE_FONT_PATH)

    print(f"Updated font sheet : {BASE_FONT_PATH}")
    print("Backup created if missing:")
    print(f"- {BASE_FONT_PATH.name}.before_combining_proto")
    print(f"- {FONTS_SOURCE_PATH.name}.before_combining_proto")
    print(f"- {CHARMAP_PATH.name}.before_combining_proto")


if __name__ == "__main__":
    main()

