from pathlib import Path
import re
import shutil

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]

FONT_SHEET = ROOT / "graphics/fonts/latin_normal.png"
FONT_SOURCE = ROOT / "src/fonts.c"
CHARMAP = ROOT / "charmap.txt"
STRINGS_SOURCE = ROOT / "src/strings.c"

GLYPH_DIR = ROOT / "graphics/fonts/thai/glyphs"

RO_RUEA_PATH = GLYPH_DIR / "0138_ro_ruea.png"
SO_SUEA_PATH = GLYPH_DIR / "013d_so_suea.png"

OUTPUT_DIR = (
    ROOT
    / "tools/thai/generated/start_game_precomposed_test"
)

GLYPH_SIZE = 16
BACKGROUND = 0
MAIN = 1
SHADOW = 2

GLYPH_SARA_E = 0x145
GLYPH_RO_RUEA_SARA_I_MAI_EK = 0x146
GLYPH_SO_SUEA_THANTHAKHAT = 0x147

WIDTH_PATTERN = re.compile(
    r"(gFontNormalLatinGlyphWidths\[\]\s*=\s*\{)"
    r"(.*?)"
    r"(\};)",
    re.S,
)


def require(path: Path) -> None:
    if not path.exists():
        raise SystemExit(f"ไม่พบไฟล์: {path}")


def backup(path: Path) -> None:
    target = path.with_name(
        path.name + ".before_start_game_test"
    )

    if not target.exists():
        shutil.copy2(path, target)
        print(f"สำรองไฟล์: {target}")


def load_glyph(path: Path) -> Image.Image:
    require(path)

    with Image.open(path) as opened:
        glyph = opened.copy()

    if glyph.mode != "P":
        glyph = glyph.convert("P")

    if glyph.size != (GLYPH_SIZE, GLYPH_SIZE):
        raise SystemExit(
            f"{path.name} ต้องมีขนาด 16x16 "
            f"แต่พบ {glyph.size}"
        )

    return glyph


def create_empty_glyph(
    palette: list[int],
) -> Image.Image:
    glyph = Image.new(
        "P",
        (GLYPH_SIZE, GLYPH_SIZE),
        BACKGROUND,
    )
    glyph.putpalette(palette)
    return glyph


def draw_pixels(
    glyph: Image.Image,
    pixels: set[tuple[int, int]],
) -> None:
    shadow_pixels: set[tuple[int, int]] = set()

    for x, y in pixels:
        for dx, dy in ((1, 0), (0, 1)):
            sx = x + dx
            sy = y + dy

            if (
                0 <= sx < GLYPH_SIZE
                and 0 <= sy < GLYPH_SIZE
                and (sx, sy) not in pixels
            ):
                shadow_pixels.add((sx, sy))

    for x, y in shadow_pixels:
        glyph.putpixel((x, y), SHADOW)

    for x, y in pixels:
        glyph.putpixel((x, y), MAIN)


def create_sara_e(
    palette: list[int],
) -> Image.Image:
    """
    สระเอแบบเดี่ยวสำหรับทดสอบคำจริง
    """
    glyph = create_empty_glyph(palette)

    pixels = {
        (5, 4),
        (6, 4),
        (5, 5),
        (5, 6),
        (5, 7),
        (5, 8),
        (5, 9),
        (5, 10),
        (5, 11),
        (5, 12),
        (5, 13),
        (6, 13),
    }

    draw_pixels(glyph, pixels)
    return glyph


def scale_to_bottom(
    source: Image.Image,
    target_height: int,
) -> Image.Image:
    bbox = source.getbbox()

    if bbox is None:
        raise SystemExit("Glyph ฐานไม่มีพิกเซล")

    left, top, right, bottom = bbox
    content = source.crop((left, top, right, bottom))

    resized = content.resize(
        (content.width, target_height),
        Image.Resampling.NEAREST,
    )

    result = create_empty_glyph(
        source.getpalette()
    )

    target_y = GLYPH_SIZE - target_height

    result.paste(
        resized,
        (left, target_y),
    )

    return result


def overlay_pixels(
    glyph: Image.Image,
    pixels: set[tuple[int, int]],
) -> None:
    draw_pixels(glyph, pixels)


def create_ro_ruea_sara_i_mai_ek(
    base: Image.Image,
) -> Image.Image:
    """
    ริ่ แบบสำเร็จรูป

    ไม้เอกอยู่ชั้นบนสุด
    สระอิอยู่ชั้นถัดลงมา
    ตัว ร ถูกย่อและตรึง baseline ด้านล่าง
    """
    glyph = scale_to_bottom(
        base,
        target_height=10,
    )

    mai_ek = {
        (8, 0),
        (8, 1),
    }

    sara_i = {
        (5, 3),
        (6, 2),
        (7, 2),
        (8, 2),
        (9, 3),
    }

    overlay_pixels(glyph, mai_ek)
    overlay_pixels(glyph, sara_i)

    return glyph


def create_so_suea_thanthakhat(
    base: Image.Image,
) -> Image.Image:
    """
    ส์ แบบสำเร็จรูป
    """
    glyph = scale_to_bottom(
        base,
        target_height=12,
    )

    thanthakhat = {
        (6, 0),
        (7, 0),
        (8, 0),
        (9, 0),
        (6, 1),
        (9, 1),
        (8, 2),
        (9, 2),
    }

    overlay_pixels(
        glyph,
        thanthakhat,
    )

    return glyph


def install_glyph(
    sheet: Image.Image,
    glyph: Image.Image,
    glyph_id: int,
) -> tuple[int, int]:
    columns = sheet.width // GLYPH_SIZE

    x = (glyph_id % columns) * GLYPH_SIZE
    y = (glyph_id // columns) * GLYPH_SIZE

    sheet.paste(
        glyph,
        (x, y),
    )

    return x, y


def read_widths(source: str) -> list[int]:
    match = WIDTH_PATTERN.search(source)

    if match is None:
        raise SystemExit(
            "ไม่พบ gFontNormalLatinGlyphWidths"
        )

    widths = [
        int(value)
        for value in re.findall(
            r"\b\d+\b",
            match.group(2),
        )
    ]

    if len(widths) != 512:
        raise SystemExit(
            f"Width table ต้องมี 512 ค่า "
            f"แต่พบ {len(widths)}"
        )

    return widths


def set_width(
    source: str,
    glyph_id: int,
    width: int,
) -> str:
    match = WIDTH_PATTERN.search(source)

    if match is None:
        raise SystemExit(
            "ไม่พบ Width table"
        )

    body = match.group(2)

    matches = list(
        re.finditer(r"\b\d+\b", body)
    )

    target = matches[glyph_id]
    old_width = int(target.group())

    updated_body = (
        body[:target.start()]
        + str(width)
        + body[target.end():]
    )

    updated = (
        source[:match.start(2)]
        + updated_body
        + source[match.end(2):]
    )

    print(
        f"Width 0x{glyph_id:03X}: "
        f"{old_width} -> {width}"
    )

    return updated


def update_charmap() -> None:
    source = CHARMAP.read_text(
        encoding="utf-8"
    )

    constants = {
        "THAI_SARA_E": "F9 45",
        "THAI_RO_RUEA_SARA_I_MAI_EK": "F9 46",
        "THAI_SO_SUEA_THANTHAKHAT": "F9 47",
    }

    for name, sequence in constants.items():
        source = re.sub(
            rf"^{name}\s*=.*\n?",
            "",
            source,
            flags=re.M,
        )

    if not source.endswith("\n"):
        source += "\n"

    source += "\n"

    for name, sequence in constants.items():
        source += f"{name} = {sequence}\n"

    CHARMAP.write_text(
        source,
        encoding="utf-8",
    )

    print("เพิ่ม Charmap Constants:")
    for name, sequence in constants.items():
        print(f"  {name} = {sequence}")


def update_test_string() -> None:
    source = STRINGS_SOURCE.read_text(
        encoding="utf-8"
    )

    pattern = re.compile(
        r'const u8 gText_MainMenuNewGame\[\]'
        r'\s*=\s*_\(".*?"\);'
    )

    # เริ่มเกมส์
    new_line = (
        'const u8 gText_MainMenuNewGame[] = '
        '_("{THAI_SARA_E}'
        '{THAI_RO_RUEA_SARA_I_MAI_EK}'
        'ม'
        '{THAI_SARA_E}'
        'กม'
        '{THAI_SO_SUEA_THANTHAKHAT}");'
    )

    updated, count = pattern.subn(
        new_line,
        source,
        count=1,
    )

    if count != 1:
        raise SystemExit(
            "ไม่พบ gText_MainMenuNewGame"
        )

    STRINGS_SOURCE.write_text(
        updated,
        encoding="utf-8",
    )

    print("เปลี่ยนข้อความทดสอบเป็น เริ่มเกมส์")
    print(new_line)


def main() -> None:
    required = [
        FONT_SHEET,
        FONT_SOURCE,
        CHARMAP,
        STRINGS_SOURCE,
        RO_RUEA_PATH,
        SO_SUEA_PATH,
    ]

    for path in required:
        require(path)

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    for path in (
        FONT_SHEET,
        FONT_SOURCE,
        CHARMAP,
        STRINGS_SOURCE,
    ):
        backup(path)

    with Image.open(FONT_SHEET) as opened:
        sheet = opened.copy()

    palette = sheet.getpalette()

    if palette is None:
        raise SystemExit(
            "latin_normal.png ไม่มี Palette"
        )

    ro_ruea = load_glyph(
        RO_RUEA_PATH
    )
    so_suea = load_glyph(
        SO_SUEA_PATH
    )

    sara_e = create_sara_e(
        palette
    )

    ro_cluster = (
        create_ro_ruea_sara_i_mai_ek(
            ro_ruea
        )
    )

    so_cluster = (
        create_so_suea_thanthakhat(
            so_suea
        )
    )

    glyphs = [
        (
            GLYPH_SARA_E,
            sara_e,
            "0145_sara_e.png",
        ),
        (
            GLYPH_RO_RUEA_SARA_I_MAI_EK,
            ro_cluster,
            "0146_ro_ruea_sara_i_mai_ek.png",
        ),
        (
            GLYPH_SO_SUEA_THANTHAKHAT,
            so_cluster,
            "0147_so_suea_thanthakhat.png",
        ),
    ]

    for glyph_id, glyph, filename in glyphs:
        output_path = OUTPUT_DIR / filename
        permanent_path = GLYPH_DIR / filename

        glyph.save(output_path)
        glyph.save(permanent_path)

        x, y = install_glyph(
            sheet,
            glyph,
            glyph_id,
        )

        print(
            f"ติดตั้ง 0x{glyph_id:03X} "
            f"ที่ X={x}, Y={y}"
        )
        print(f"  {permanent_path}")

    sheet.save(FONT_SHEET)

    font_source = FONT_SOURCE.read_text(
        encoding="utf-8"
    )

    widths = read_widths(font_source)

    ro_width = widths[0x138]
    so_width = widths[0x13D]

    font_source = set_width(
        font_source,
        GLYPH_SARA_E,
        7,
    )

    font_source = set_width(
        font_source,
        GLYPH_RO_RUEA_SARA_I_MAI_EK,
        ro_width,
    )

    font_source = set_width(
        font_source,
        GLYPH_SO_SUEA_THANTHAKHAT,
        so_width,
    )

    FONT_SOURCE.write_text(
        font_source,
        encoding="utf-8",
    )

    update_charmap()
    update_test_string()

    print("")
    print("=== เริ่มเกมส์ Prototype Installed ===")
    print("0x145 = เ")
    print("0x146 = ริ่")
    print("0x147 = ส์")
    print("Renderer ยังคงเป็นของเดิม")


if __name__ == "__main__":
    main()
