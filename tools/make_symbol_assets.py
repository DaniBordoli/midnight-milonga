"""Cut the Midnight Milonga concept art into game sprites (placeholders until the final art).

Usage (from the repo root):
    math\\env\\Scripts\\python.exe tools\\make_symbol_assets.py "<folder with the concept art>"

Writes web/apps/midnight-milonga/static/assets/sprites/milonga/:
    <symbol>.webp, <symbol>_win.webp (brighter, gold rim), background.webp
"""

import os
import sys

from PIL import Image, ImageDraw, ImageEnhance

from process_animation_art import save_sprite

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "web", "apps", "midnight-milonga", "static", "assets", "sprites", "milonga")
SIZE = 256
GOLD = (222, 184, 98)

TOP_Y, BOTTOM_Y, HALF = 0.235, 0.78, 0.095
XS = [0.132, 0.316, 0.501, 0.685, 0.87]


def square(sheet, cx, cy):
    half_h = HALF * sheet.width / sheet.height
    box = (cx - HALF, cy - half_h, cx + HALF, cy + half_h)
    return sheet.crop(tuple(int(v * (sheet.width if i % 2 == 0 else sheet.height)) for i, v in enumerate(box)))


def frac(img, box):
    return img.crop((int(box[0] * img.width), int(box[1] * img.height), int(box[2] * img.width), int(box[3] * img.height)))


def tile(img):
    """Fit into a SIZE x SIZE dark tile."""
    img = img.convert("RGB")
    s = min(SIZE / img.width, SIZE / img.height)
    img = img.resize((int(img.width * s), int(img.height * s)), Image.LANCZOS)
    out = Image.new("RGB", (SIZE, SIZE), (18, 16, 16))
    out.paste(img, ((SIZE - img.width) // 2, (SIZE - img.height) // 2))
    return out


def win_variant(img):
    out = ImageEnhance.Brightness(img).enhance(1.3)
    ImageDraw.Draw(out).rounded_rectangle([3, 3, SIZE - 4, SIZE - 4], radius=18, outline=GOLD, width=7)
    return out


def main(art_dir):
    os.makedirs(OUT, exist_ok=True)
    sheet = Image.open(os.path.join(art_dir, "Hoja de símbolos.jpg"))
    wilds = Image.open(os.path.join(art_dir, "WILD.jpg"))
    abrazo = Image.open(os.path.join(art_dir, "Feature El abrazo.jpg"))

    symbols = {
        "h1": square(sheet, XS[0], TOP_Y),  # bandoneón
        "h2": square(sheet, XS[1], TOP_Y),  # rosa
        "h3": square(sheet, XS[2], TOP_Y),  # fedora
        "h4": square(sheet, XS[3], TOP_Y),  # champagne
        "s": square(sheet, XS[4], TOP_Y),  # entrada (scatter)
        "l1": square(sheet, XS[0], BOTTOM_Y),  # pica
        "l2": square(sheet, XS[1], BOTTOM_Y),  # corazón
        "l3": square(sheet, XS[2], BOTTOM_Y),  # diamante
        "l4": square(sheet, XS[3], BOTTOM_Y),  # trébol
        "bm": frac(wilds, (0.055, 0.115, 0.448, 0.905)),  # Bailarín
        "bf": frac(wilds, (0.533, 0.115, 0.94, 0.905)),  # Bailarina
        "w": frac(abrazo, (0.235, 0.372, 0.34, 0.535)),  # wild dorado de El Abrazo
    }
    for name, img in symbols.items():
        t = tile(img)
        save_sprite(t, name, OUT)
        save_sprite(win_variant(t), f"{name}_win", OUT)

    bg = Image.open(os.path.join(art_dir, "Key art o fondo.jpg")).convert("RGB")
    save_sprite(bg.resize((2048, int(2048 * bg.height / bg.width)), Image.LANCZOS), "background", OUT)
    print("ok:", OUT)


if __name__ == "__main__":
    main(sys.argv[1])
