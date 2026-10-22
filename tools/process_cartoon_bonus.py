"""Free spin intro, El Abrazo, La Rosa Roja and Compás art from the Ludo cartoon pieces.

Usage (from the repo root):
    math\\env\\Scripts\\python.exe tools\\process_cartoon_bonus.py "<slot>/7. Cartoon/chibi/bonus"

Writes web/apps/midnight-milonga/static/assets/sprites/milonga/fx/<name>.webp. Backgrounds are cover-cropped
to 2048 x 1143 (BACKGROUND in FreeSpinIntro.svelte); the rose and its burst are drawn square, so they are
padded square; the other cutouts keep their own aspect, which is printed for the components.
"""

import json
import os
import sys

from PIL import Image

from process_animation_art import OUT as FX, fit, save_sprite
from process_cartoon_background import cover
from process_cartoon_ui import pad_to

BACKGROUNDS = {"pista_bg": "pista_bg_a.webp", "tanda_bg": "tanda_bg_a.webp"}
# output name: (source file, aspect to pad to or None to keep, max size)
CUTOUTS = {
    "tanda_couple": ("tanda_couple_b.webp", None, 1024),
    "rosa_flying": ("rosa_flying_b.webp", 1, 512),
    "rosa_burst": ("rosa_burst_b.webp", 1, 768),
    "metronome_body": ("metronome_body_a.webp", None, 768),
    "metronome_pendulum": ("metronome_pendulum_b.webp", None, 768),
}


def abrazo_sheet(src, cols=5, rows=5, count=25, max_frame=384):
    """El Abrazo dance: the Ludo grid cropped to the frames' common bounds, written as a Pixi spritesheet
    (fx/abrazo_dance.webp + .json, animation "dance")."""
    sheet = Image.open(os.path.join(src, "abrazo_sheet.webp")).convert("RGBA")
    fw, fh = sheet.width // cols, sheet.height // rows
    frames = [sheet.crop(((i % cols) * fw, (i // cols) * fh, (i % cols + 1) * fw, (i // cols + 1) * fh)) for i in range(count)]
    boxes = [f.getbbox() for f in frames]
    box = (min(b[0] for b in boxes), min(b[1] for b in boxes), max(b[2] for b in boxes), max(b[3] for b in boxes))
    frames = [fit(f.crop(box), max_frame) for f in frames]
    w, h = frames[0].size
    out = Image.new("RGBA", (w * cols, h * rows), (0, 0, 0, 0))
    names = [f"abrazo_dance_{i}" for i in range(count)]  # non-numeric keys keep insertion order in Pixi
    meta = {}
    for i, (f, n) in enumerate(zip(frames, names)):
        out.paste(f, ((i % cols) * w, (i // cols) * h))
        rect = {"x": (i % cols) * w, "y": (i // cols) * h, "w": w, "h": h}
        meta[n] = {"frame": rect, "rotated": False, "trimmed": False, "spriteSourceSize": {"x": 0, "y": 0, "w": w, "h": h}, "sourceSize": {"w": w, "h": h}}
    save_sprite(out, "abrazo_dance", FX)
    data = {"frames": meta, "animations": {"dance": names}, "meta": {"image": "abrazo_dance.webp", "format": "RGBA8888", "size": {"w": out.width, "h": out.height}, "scale": "1"}}
    with open(os.path.join(FX, "abrazo_dance.json"), "w", encoding="utf-8") as fh_out:
        json.dump(data, fh_out, indent=1)
    print("ok abrazo_dance, frame", (w, h))


def main(src):
    abrazo_sheet(src)
    for name, file in BACKGROUNDS.items():
        save_sprite(cover(Image.open(os.path.join(src, file))), name, FX)
        print("ok", name)
    for name, (file, aspect, max_side) in CUTOUTS.items():
        img = Image.open(os.path.join(src, file)).convert("RGBA")
        img = pad_to(img, aspect) if aspect else img.crop(img.getbbox())
        img = fit(img, max_side)
        save_sprite(img, name, FX)
        print("ok", name, img.size)


if __name__ == "__main__":
    main(sys.argv[1])
