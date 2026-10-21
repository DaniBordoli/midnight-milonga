"""Turn the Gemini UI art (plates, buttons, icon sheet) into UI sprites.

Usage (from the repo root):
    math\\env\\Scripts\\python.exe tools\\process_ui_art.py "<slot>/5. Interfaz"

Plates and buttons are chroma-keyed like the animation art. The icon sheet is a 4 x 2 grid of gold
line icons, each on its own dark tile: only the gold line work is kept, so the icons can sit on the
round button. Writes web/apps/midnight-milonga/static/assets/sprites/milonga/ui/<name>.webp
"""

import os
import sys

import numpy as np
from PIL import Image

from process_animation_art import fit, key_green, save_sprite

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "web", "apps", "midnight-milonga", "static", "assets", "sprites", "milonga", "ui")

# output name: (file name, max size)
PLATES = {
    "panel": ("Panel info.jpg", 1024),
    "button_spin": ("Boton girar.jpg", 512),
    "button_small": ("Boton chico.jpg", 256),
    "button_buy": ("Boton compra.jpg", 768),
    "button_menu": ("Boton menu.jpg", 384),
}

# icon sheet cells, left to right, top to bottom
ICONS = ["auto_spin", "turbo", "menu", "increase", "decrease", "sound_on", "sound_off", "info"]
CELL_CENTERS_X = [140, 387, 637, 885]  # measured on the 1024 x 506 sheet
CELL_CENTERS_Y = [132, 376]
ICON_HALF = 85  # inside each tile, clear of its corner ornaments


def gold_only(img):
    """Keep the gold line work: gold has a strong green channel, the dark tile (black / deep red) none."""
    a = np.asarray(img.convert("RGB")).astype(np.int32)
    alpha = np.clip((a[..., 1] - 55) * 4, 0, 255)
    out = Image.fromarray(np.dstack([a, alpha]).astype(np.uint8), "RGBA")
    return out.crop(out.getchannel("A").getbbox())


def main(src):
    os.makedirs(OUT, exist_ok=True)
    for name, (file, max_side) in PLATES.items():
        save_sprite(fit(key_green(Image.open(os.path.join(src, file))), max_side), name, OUT)
        print("ok", name)

    sheet = Image.open(os.path.join(src, "Iconos.jpg"))
    scale = sheet.width / 1024
    for i, name in enumerate(ICONS):
        cx, cy = CELL_CENTERS_X[i % 4] * scale, CELL_CENTERS_Y[i // 4] * scale
        h = ICON_HALF * scale
        cell = sheet.crop((int(cx - h), int(cy - h), int(cx + h), int(cy + h)))
        save_sprite(fit(gold_only(cell), 128), f"icon_{name}", OUT)
        print("ok", f"icon_{name}")


if __name__ == "__main__":
    main(sys.argv[1])
