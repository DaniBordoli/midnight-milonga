"""Bonus menu card images, cropped from sprites the game already ships (run process_animation_art.py first).

Usage (from the repo root):
    math\\env\\Scripts\\python.exe tools\\make_bonus_card_art.py

Writes web/apps/midnight-milonga/static/assets/sprites/milonga/bonus/<mode>.webp at 360x200 (2x the card width).
"""

import os

from PIL import Image

from process_animation_art import OUT as FX, save_sprite

OUT = os.path.join(os.path.dirname(FX), "bonus")
SIZE = (360, 200)


def crop(img, cx, cy, zoom):
    """Card-shaped crop centred on (cx, cy) as fractions of the image; zoom 1 = the widest crop that fits."""
    w = min(img.width, img.height * SIZE[0] / SIZE[1]) / zoom
    h = w * SIZE[1] / SIZE[0]
    left = min(max(0, img.width * cx - w / 2), img.width - w)
    top = min(max(0, img.height * cy - h / 2), img.height - h)
    return img.crop((int(left), int(top), int(left + w), int(top + h))).resize(SIZE, Image.LANCZOS)


def sprite(name):
    return Image.open(os.path.join(FX, f"{name}.webp")).convert("RGBA")


def main():
    os.makedirs(OUT, exist_ok=True)
    # Noche de Gala: the milonga entrance at night
    save_sprite(crop(sprite("loading_bg"), 0.5, 0.45, 1.6), "ante", OUT)
    # La Pista: the dance floor
    save_sprite(crop(sprite("pista_bg"), 0.5, 0.55, 1.2), "bonus", OUT)
    # La Última Tanda: the couple standing in the spotlight
    stage = sprite("tanda_bg")
    couple = sprite("tanda_couple")
    scale = stage.height * 0.5 / couple.height
    couple = couple.resize((int(couple.width * scale), int(couple.height * scale)), Image.LANCZOS)
    stage.alpha_composite(couple, (int(stage.width * 0.5 - couple.width / 2), int(stage.height * 0.9 - couple.height)))
    save_sprite(crop(stage, 0.5, 0.55, 1.1), "super", OUT)


if __name__ == "__main__":
    main()
