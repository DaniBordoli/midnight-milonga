"""Pampa Play logo for the in-game header (top right).

Usage (from the repo root):
    math\\env\\Scripts\\python.exe tools\\make_brand_logo.py "<slot>/2. Marca Pampa Play"

The horizontal white logo already has a transparent background: cropped to its content and resized.
Writes web/apps/midnight-milonga/static/assets/sprites/milonga/ui/pampa_play_logo.webp
"""

import os
import sys

from PIL import Image

from sprite_utils import UI as OUT, fit, save_sprite


def main(src):
    logo = Image.open(os.path.join(src, "pampa-play-stake-logo.png")).convert("RGBA")
    logo = logo.crop(logo.getbbox())
    save_sprite(fit(logo, 512), "pampa_play_logo", OUT)


if __name__ == "__main__":
    main(sys.argv[1])
