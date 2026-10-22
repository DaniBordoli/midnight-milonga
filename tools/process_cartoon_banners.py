"""Win, feature and bonus banners from the Ludo cartoon art.

Usage (from the repo root):
    math\\env\\Scripts\\python.exe tools\\process_cartoon_banners.py "<slot>/7. Cartoon/chibi/carteles"

Crops each chosen banner to its content and writes it to
web/apps/midnight-milonga/static/assets/sprites/milonga/fx/<name>.webp. Prints every size: WinAnimation,
FeatureBanner, FreeSpinIntro and FreeSpinOutro draw the banners by those aspects.
"""

import os
import sys

from PIL import Image

from process_animation_art import OUT as FX, fit, save_sprite

# output name: chosen file (variants a/b from the first round, c/d from the redo)
CHOSEN = {
    "big_win": "big_win_b.webp",
    "super_win": "super_win_a.webp",
    "mega_win": "mega_win_a.webp",
    "epic_win": "epic_win_c.webp",
    "max_win": "max_win_c.webp",
    "banner_rosa": "banner_rosa_c.webp",
    "banner_abrazo": "banner_abrazo_d.webp",
    "pista_title": "pista_title_d.webp",
    "tanda_title": "tanda_title_d.webp",
    "spins_plate": "spins_plate_b.webp",
    "total_win_panel": "total_win_panel_a.webp",
}


def main(src):
    for name, file in CHOSEN.items():
        img = Image.open(os.path.join(src, file)).convert("RGBA")
        img = fit(img.crop(img.getbbox()), 1024)
        save_sprite(img, name, FX)
        print(name, img.size)


if __name__ == "__main__":
    main(sys.argv[1])
