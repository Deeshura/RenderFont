#!/usr/bin/env python3

# Renders the specified .ttf font file in a format
# so that it can be imported into PMD - EoS.
# Requires the vanilla table-0.png and char_tables.xml
# for the type of font you're trying to render (window or banner)
# in the current directory.

import argparse
import os
import xml.etree.ElementTree as ET

from PIL import Image, ImageDraw, ImageFont

TABLE129_ENTRIES = {
    64: 6,
    96: 9,
    168: 11,
    169: 12,
    170: 7,
    171: 7,
    244: 7,
}


def parse_args():
    parser = argparse.ArgumentParser(
        description="""
        Renders the specified .ttf font file in a format so that it can be imported into PMD - EoS.
        Requires the vanilla table-0.png and char_tables.xml for the type of font you're trying to render (window or banner) in the current directory.
        """
    )
    parser.add_argument("font", help="Path to the .ttf font file")
    parser.add_argument("size", type=int, help="Point size for the font")
    parser.add_argument("offset", type=int, help="Offset distance of the font")
    parser.add_argument(
        "--banner",
        "-b",
        action="store_true",
        help="Render banner text instead of window text",
    )
    return parser.parse_args()


def is_missing_glyph(font, ch):
    # i hate that this is probably the best way to do this
    mask = font.getmask(ch)
    bbox = mask.getbbox()
    if bbox is None:
        # treat as missing and use the vanilla charwidth (for spaces and stuff)
        return True

    # the fallback glyph, delicious tofu
    missing_mask = font.getmask("\uffff")
    missing_bbox = missing_mask.getbbox()

    # optimization, if bounding box is different, probably not tofu
    if bbox != missing_bbox:
        return False

    # if bounding box is the same, then check
    # per-pixel to see if it matches tofu or not
    return bytes(mask) == bytes(missing_mask)


def main():
    args = parse_args()

    print(
        "Rendering "
        + args.font
        + " at point size "
        + str(args.size)
        + ", offset by "
        + str(args.offset)
        + "."
    )

    # font and xml loading

    font = ImageFont.truetype(args.font, size=args.size)

    fallback_sheet = Image.open("table-0.png")
    fallback_tree = ET.parse("char_tables.xml")

    root = ET.Element("Font")
    fallback_root = fallback_tree.getroot()

    ## fallback widths for using the vanila charset

    fallback_widths = {}

    for table in fallback_root.findall("Table"):
        if table.get("tableid") == "0":
            for char in table.findall("Char"):
                cid = int(char.get("id"))
                width = int(char.get("width"))
                fallback_widths[cid] = width
            break

    # palette stuff. heated autolinter moment.

    PALETTE = (
        [
            0,
            0,
            0,
            15,
            15,
            15,
            31,
            31,
            31,
            47,
            47,
            47,
            63,
            63,
            63,
            79,
            79,
            79,
            95,
            95,
            95,
            111,
            111,
            111,
            127,
            127,
            127,
            143,
            143,
            143,
            159,
            159,
            159,
            175,
            175,
            175,
            191,
            191,
            191,
            207,
            207,
            207,
            215,
            215,
            215,
            231,
            231,
            231,
        ]
        if args.banner
        else [
            255,
            255,
            255,
            240,
            240,
            240,
            224,
            224,
            224,
            208,
            208,
            208,
            192,
            192,
            192,
            176,
            176,
            176,
            160,
            160,
            160,
            144,
            144,
            144,
            128,
            128,
            128,
            112,
            112,
            112,
            96,
            96,
            96,
            80,
            80,
            80,
            64,
            64,
            64,
            48,
            48,
            48,
            32,
            32,
            32,
            16,
            16,
            16,
        ]
    )

    palette_img = Image.new(
        "P",
        (
            1,
            1,
        ),
    )
    palette_img.putpalette(PALETTE)

    # metrics and theming

    cell_size = 24 if args.banner else 12
    sheet_w = cell_size * 16
    sheet_h = cell_size * 16

    bg_color = "#000000" if args.banner else "#FFFFFF"
    fg_color = "#FFFFFF" if args.banner else "#000000"

    sheet = Image.new("RGBA", (sheet_w, sheet_h), bg_color)
    draw = ImageDraw.Draw(sheet)

    # Render each CP1252 glyph

    for code in range(256):
        ch = bytes([code]).decode("cp1252", errors="replace")

        row = code // 16
        col = code % 16

        x = col * cell_size
        y = row * cell_size

        if is_missing_glyph(font, ch):
            # copy tile from original
            src_x = col * 12
            src_y = row * 12

            if code in fallback_widths:
                # copy tile from fallback sheet
                fallback_tile = fallback_sheet.crop(
                    (src_x, src_y, src_x + 12, src_y + 12)
                )
            else:
                # create a blank tile
                fallback_tile = Image.new("RGBA", (cell_size, cell_size), bg_color)

            if args.banner:
                fallback_tile = fallback_tile.resize((24, 24), Image.Resampling.NEAREST)

            sheet.paste(fallback_tile, (x, y))
            continue

        bbox = font.getbbox(ch)
        ox = -bbox[0]
        oy = args.offset

        draw.text((x + ox, y + oy), ch, font=font, fill=fg_color)

    indexed = sheet.convert("RGB").quantize(palette=palette_img, dither=Image.NONE)

    base = os.path.splitext(os.path.basename(args.font))[0]
    indexed.save(base + ".png", optimize=False)

    print("Saved sprite sheet to " + base + ".png")

    # xml handling

    ## table 0, aka the important one

    table0 = ET.SubElement(root, "Table", tableid="0")

    for code in range(32, 256):
        ch = bytes([code]).decode("cp1252", errors="replace")

        if is_missing_glyph(font, ch):
            width = fallback_widths.get(code, 0)

        else:
            bbox = font.getbbox(ch)
            width = bbox[2] - bbox[0]

        ET.SubElement(table0, "Char", id=str(code), width=str(width))

    ## 48, empty

    ET.SubElement(root, "Table", tableid="48")

    ## 129, which has some arrows

    table129 = ET.SubElement(root, "Table", tableid="129")
    for cid, width in TABLE129_ENTRIES.items():
        ET.SubElement(table129, "Char", id=str(cid), width=str(width))

    ## other empty tables

    for tid in [130, 131, 132, 135, 255]:
        ET.SubElement(root, "Table", tableid=str(tid))

    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ", level=0)  # pretty indenting

    # lots of annoying shit to make sure the xml is in the same styling as Skemple exports

    xml_bytes = ET.tostring(root, encoding="utf-8", xml_declaration=False)
    xml_text = xml_bytes.decode("utf-8")

    xml_text = xml_text.replace(" />", "/>")  # begone, space
    xml_text = (
        "<?xml version='1.0' ?>\n" + xml_text
    )  # custom xml declaration without heading

    with open(base + ".xml", "w", encoding="utf-8") as f:
        f.write(xml_text)

    print("Saved XML metadata to " + base + ".xml")


if __name__ == "__main__":
    main()
