"""Loading screen and game logo from the Ludo cartoon art.

Usage (from the repo root):
    math\\env\\Scripts\\python.exe tools\\process_cartoon_loading.py "<slot>/7. Cartoon/chibi/carga"

Writes web/apps/midnight-milonga/static/assets/sprites/milonga/fx/:
    loading_bg.webp    background, cover-cropped to 2048 x 1143 (BACKGROUND in LoadingScreen.svelte)
    title.webp         game logo, cropped to content (also drawn in the header, see Game.svelte)
    loading_rose.webp  spinner
    loading_bar.webp   frame over the progress bar
Prints the logo and bar sizes: LoadingScreen.svelte and Game.svelte size them by those aspects.
"""

import os
import sys

import numpy as np
from PIL import Image, ImageFilter

from sprite_utils import FX, fit, save_sprite
from process_cartoon_background import cover

# output name: (source file, max size)
CUTOUTS = {
    "title": ("logo_1.webp", 1400),
    "loading_rose": ("rosa_a.webp", 512),
    "loading_bar": ("barra_a.webp", 1012),
}


def darken_rim(img, width=5, factor=0.45):
    """Darken the outermost `width` px of the opaque shape: the logo's outline ends in a light pink rim
    that reads as a white edge once the logo is drawn small."""
    alpha = img.getchannel("A")
    inner = np.asarray(alpha.point(lambda v: 255 if v > 128 else 0).filter(ImageFilter.MinFilter(width * 2 + 1))) > 0
    a = np.asarray(img).astype(np.float32)
    rim = (a[..., 3] > 0) & ~inner
    a[..., :3][rim] *= factor
    return Image.fromarray(a.astype(np.uint8))


def main(src):
    save_sprite(cover(Image.open(os.path.join(src, "fondo_a.webp"))), "loading_bg", FX)
    for name, (file, max_side) in CUTOUTS.items():
        img = Image.open(os.path.join(src, file)).convert("RGBA")
        img = fit(img.crop(img.getbbox()), max_side)
        if name == "title":
            img = darken_rim(img)
        save_sprite(img, name, FX)
        print("ok", name, img.size)


if __name__ == "__main__":
    main(sys.argv[1])
