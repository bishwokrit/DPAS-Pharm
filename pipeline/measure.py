"""Measure real character widths so the deck builder can wrap text exactly like PowerPoint.

Carlito has the same character widths as Calibri, so its measurements match the deck's font.
Writes {"regular": {char: em}, "bold": {char: em}} for every character the lecture uses.
"""
import json
import sys
from pathlib import Path

from PIL import ImageFont

FONTS = {
    "regular": "/usr/share/fonts/truetype/crosextra/Carlito-Regular.ttf",
    "bold": "/usr/share/fonts/truetype/crosextra/Carlito-Bold.ttf",
}
SIZE = 1000


def main(content_path, out_path):
    chars = set(Path(content_path).read_text()) | {chr(c) for c in range(32, 127)} | set("•·→—–≠⚠✓")
    widths = {}
    for style, path in FONTS.items():
        font = ImageFont.truetype(path, SIZE)
        widths[style] = {ch: round(font.getlength(ch) / SIZE, 4) for ch in chars if ch.isprintable()}
    Path(out_path).write_text(json.dumps(widths, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
