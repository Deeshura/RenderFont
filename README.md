# RenderFont

A python script to render .ttf font files for importing into PMD EoS, either as window fonts, or banner fonts. This outputs a table-0.png and an accompanying char_tables.xml.

## Arguements

```
usage: renderfont.py [-h] [--banner] font size offset

Renders the specified .ttf font file in a format so that it can be imported into PMD - EoS. Requires the vanilla
table-0.png and char_tables.xml for the type of font you're trying to render (window or banner) in the current
directory.

positional arguments:
  font          Path to the .ttf font file
  size          Point size for the font
  offset        Offset distance of the font

options:
  -h, --help    show this help message and exit
  --banner, -b  Render banner text instead of window text
```

## Requirements

- A .ttf font you'd like to render.
- Python (to run the script!)
- Pillow 10.0.0 or above (see requirements.txt)
- SkyTemple (to insert your new fonts and extract the vanilla font files)
- The vanilla table-0.png and char_tables.xml (see [Vanilla Files](#vanilla-files))

## Vanilla Files

To run the script, you'll require the char_tables.xml and table-0.png of the vanilla game, respective to whether you're trying to generate a banner or window font. They are not distributed here in this repository- you will need to extract them from kanji_rd.dat or banner.bin using [SkyTemple](https://skytemple.org/).

To extract these files, open SkyTemple, and open your legally-acquired ROM of PMD EoS. Open the directory titled "Misc. Graphics". In there, you will see both FONT/kanji_rd.dat (which is the sprite files for window text), and FONT/banner.bin:FONT/b_pal.bin (sprite file for banner text).

Double-click on the respective file you wish to extract. A preview will open in SkyTemple showing the font in question. Click "Export" above the preview and save the vanilla font to a directory of your choosing. 

## Usage

1. Download renderfont.py (either by downloading the whole repository or just the script file itself). 
2. Download Pillow 10.0.0 or above using pip.
3. Ensure the vanilla char_tables.xml and table-0.png (for window or banner fonts) are in the same directory as renderfont.py, as well as the .ttf font you'd like to render.
4. Run renderfont.py using python, using the arguements to specify the font you'd like to render, the size you'd like to render it at, the vertical offset of the font (to ensure it lines up properly on the sprite sheet). Use -b if you're rendering a banner font.
5. renderfont.py will run and output your font file. It may take several attempts to get the font at the correct size and offset.
6. Once you are happy, copy the generate .png and .xml files into a new directory, and rename them to table-0.png and char_tables.xml. Then copy in the *additional* table-\*.png files that you exported earlier, where the asterisk is 48, 129, 130, 131, 132, 135, and 255.
7. Open SkyTemple, and open your legally-acquired ROM of PMD EoS. Open the directory titled "Misc. Graphics". In there, you will see both FONT/kanji_rd.dat (which is the sprite files for window text), and FONT/banner.bin:FONT/b_pal.bin (sprite file for banner text). Double-click on the respective file you wish to replace. 
8. A preview will open in SkyTemple showing the font in question. Click "Import" above the preview and then navigate to the directory where you moved and renamed your new font file. Open the directory, and SkyTemple will import your new font, which should be reflected in the preview.
9. Save your ROM and either use the SkyTemple debugger, an emulator, or even real hardware to see your new font in game!

## Credits

This project makes use of the Pillow package. The copyright and MIT-CMU license for Pillow is provided below;

```
The Python Imaging Library (PIL) is

    Copyright © 1997-2011 by Secret Labs AB
    Copyright © 1995-2011 by Fredrik Lundh and contributors

Pillow is the friendly PIL fork. It is

    Copyright © 2010 by Jeffrey A. Clark and contributors

Like PIL, Pillow is licensed under the open source MIT-CMU License:

By obtaining, using, and/or copying this software and/or its associated
documentation, you agree that you have read, understood, and will comply
with the following terms and conditions:

Permission to use, copy, modify and distribute this software and its
documentation for any purpose and without fee is hereby granted,
provided that the above copyright notice appears in all copies, and that
both that copyright notice and this permission notice appear in supporting
documentation, and that the name of Secret Labs AB or the author not be
used in advertising or publicity pertaining to distribution of the software
without specific, written prior permission.

SECRET LABS AB AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS
SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS.
IN NO EVENT SHALL SECRET LABS AB OR THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE
OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.
```
