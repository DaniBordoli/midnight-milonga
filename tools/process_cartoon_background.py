"""Main game background from the Ludo cartoon art.

Usage (from the repo root):
    math\\env\\Scripts\\python.exe tools\\process_cartoon_background.py "<slot>/7. Cartoon/chibi/fondo/fondo_2_barra_b.webp"

Cover-crops the image to SIZE (BACKGROUND_SIZE in src/components/Background.svelte) and writes
web/apps/midnight-milonga/static/assets/sprites/milonga/background.webp
"""

import os
import sys

from PIL import Image

from process_animation_art import OUT as FX, save_sprite

SIZE = (2048, 1143)


def main(src):
    img = Image.open(src).convert("RGB")
    s = max(SIZE[0] / img.width, SIZE[1] / img.height)
    img = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    left, top = (img.width - SIZE[0]) // 2, (img.height - SIZE[1]) // 2
    save_sprite(img.crop((left, top, left + SIZE[0], top + SIZE[1])), "background", os.path.dirname(FX))


if __name__ == "__main__":
    main(sys.argv[1])
