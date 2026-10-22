"""Main game background from the Ludo cartoon art.

Usage (from the repo root):
    math\\env\\Scripts\\python.exe tools\\process_cartoon_background.py "<slot>/7. Cartoon/chibi/fondo/fondo_2_barra_b.webp"

Cover-crops the image to SIZE (BACKGROUND_SIZE in src/components/Background.svelte) and writes
web/apps/midnight-milonga/static/assets/sprites/milonga/background.webp
"""

import os
import sys

from PIL import Image

from sprite_utils import FX, save_sprite

SIZE = (2048, 1143)


def cover(img, size=SIZE):
    """Scale to cover size, then crop the centre."""
    img = img.convert("RGB")
    s = max(size[0] / img.width, size[1] / img.height)
    img = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    left, top = (img.width - size[0]) // 2, (img.height - size[1]) // 2
    return img.crop((left, top, left + size[0], top + size[1]))


def main(src):
    save_sprite(cover(Image.open(src)), "background", os.path.dirname(FX))


if __name__ == "__main__":
    main(sys.argv[1])
