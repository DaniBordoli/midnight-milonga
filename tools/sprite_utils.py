"""Shared helpers for the art scripts in tools/: output folders, resizing and the WebP writer."""

import json
import os

import numpy as np
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPRITES = os.path.join(ROOT, "web", "apps", "midnight-milonga", "static", "assets", "sprites", "milonga")
FX = os.path.join(SPRITES, "fx")
UI = os.path.join(SPRITES, "ui")


def save_sprite(img, name, out_dir=FX):
    """Every game sprite ships as WebP (Stake rates bundle size): lossy with alpha, about a fifth of a PNG."""
    path = os.path.join(out_dir, f"{name}.webp")
    img.save(path, "WEBP", quality=88, method=6)
    return path


def fit(img, max_side):
    s = min(1.0, max_side / max(img.size))
    return img.resize((int(img.width * s), int(img.height * s)), Image.LANCZOS) if s < 1 else img


def particle_sheet(pieces, name, out_dir, max_side=160):
    """Split a transparent image of separate pieces into frames and write a Pixi spritesheet (same format as the
    sample coin sheet: frames 1.png..N.png and an animation named "coin", so the particle emitter can use it)."""
    alpha = pieces.getchannel("A")
    w, h = alpha.size
    small = alpha.point(lambda v: 255 if v > 40 else 0).resize((w // 4, h // 4), Image.NEAREST)
    boxes, label = [], 1
    for y, x in zip(*np.nonzero(np.asarray(small) == 255)):
        if np.asarray(small)[y, x] != 255:
            continue
        ImageDraw.floodfill(small, (int(x), int(y)), label)
        ys, xs = np.nonzero(np.asarray(small) == label)
        if len(xs) > 40:  # ignore specks
            boxes.append((int(xs.min()) * 4 - 4, int(ys.min()) * 4 - 4, int(xs.max()) * 4 + 8, int(ys.max()) * 4 + 8))
        label += 1
    frames = [fit(pieces.crop(box), max_side) for box in boxes]
    sheet_w = sum(f.width for f in frames) + 2 * len(frames)
    sheet = Image.new("RGBA", (sheet_w, max(f.height for f in frames)), (0, 0, 0, 0))
    meta, x = {}, 0
    for i, f in enumerate(frames, start=1):
        sheet.paste(f, (x, 0))
        meta[f"{i}.png"] = {
            "frame": {"x": x, "y": 0, "w": f.width, "h": f.height},
            "rotated": False,
            "trimmed": False,
            "spriteSourceSize": {"x": 0, "y": 0, "w": f.width, "h": f.height},
            "sourceSize": {"w": f.width, "h": f.height},
        }
        x += f.width + 2
    save_sprite(sheet, name, out_dir)
    data = {
        "frames": meta,
        "animations": {"coin": list(meta)},
        "meta": {"image": f"{name}.webp", "format": "RGBA8888", "size": {"w": sheet.width, "h": sheet.height}, "scale": "1"},
    }
    with open(os.path.join(out_dir, f"{name}.json"), "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=1)
    return len(frames)
