from pathlib import Path
import argparse
import re


FONTS_SOURCE_PATH = Path("src/fonts.c")

ARRAY_PATTERN = re.compile(
    r"(gFontNormalLatinGlyphWidths\[\]\s*=\s*\{)"
    r"(.*?)"
    r"(\};)",
    re.S,
)


def parse_glyph_id(value: str) -> int:
    cleaned = value.strip().lower()

    if cleaned.startswith("0x"):
        cleaned = cleaned[2:]

    try:
        glyph_id = int(cleaned, 16)
    except ValueError as error:
        raise argparse.ArgumentTypeError(
            f"Glyph ID '{value}' ไม่ใช่เลขฐานสิบหก"
        ) from error

    if not 0 <= glyph_id <= 0x1FF:
        raise argparse.ArgumentTypeError(
            "Glyph ID ต้องอยู่ระหว่าง 0x000 ถึง 0x1FF"
        )

    return glyph_id


def parse_width(value: str) -> int:
    try:
        width = int(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError(
            f"Width '{value}' ไม่ใช่ตัวเลข"
        ) from error

    if not 1 <= width <= 16:
        raise argparse.ArgumentTypeError(
            "Width ต้องอยู่ระหว่าง 1 ถึง 16 พิกเซล"
        )

    return width


def main() -> None:
    parser = argparse.ArgumentParser(
        description="กำหนดความกว้างของ Glyph ใน src/fonts.c"
    )

    parser.add_argument(
        "glyph_id",
        type=parse_glyph_id,
        help="Glyph ID ฐานสิบหก เช่น 118 หรือ 0x118",
    )

    parser.add_argument(
        "width",
        type=parse_width,
        help="ความกว้าง 1–16 พิกเซล",
    )

    args = parser.parse_args()

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

    target = number_matches[args.glyph_id]
    old_width = int(target.group())

    updated_body = (
        array_body[:target.start()]
        + str(args.width)
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

    print("=== Glyph Width Updated ===")
    print(f"Glyph ID  : 0x{args.glyph_id:03X}")
    print(f"Old width : {old_width}")
    print(f"New width : {args.width}")
    print(f"File      : {FONTS_SOURCE_PATH}")


if __name__ == "__main__":
    main()