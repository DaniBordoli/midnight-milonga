"""Turn the Ludo cartoon UI pieces into game sprites: board frame, label plate, buttons and button icons.

Usage (from the repo root):
    math\\env\\Scripts\\python.exe tools\\process_cartoon_ui.py "<slot>/7. Cartoon/chibi/ui"

Plates and buttons come with a transparent background: they are cropped and padded to the aspect the
components draw them at, so nothing is stretched. The icons come as rows of 4 on a cream background,
which is keyed out before each icon is cut. Prints the frame's inner window, for FRAME_SCALE in
src/components/BoardFrame.svelte.
"""

import os
import sys

import numpy as np
from PIL import Image, ImageDraw

from sprite_utils import FX, UI, fit, save_sprite

# output name: (source file, aspect width / height the component draws it at, max size)
PIECES = {
    "panel": ("placa_b.webp", 994 / 209, 994),  # UiLabel PANEL_HEIGHT
    "button_spin": ("giro_b.webp", 1, 512),
    "button_small": ("chico_b.webp", 1, 256),
    "button_buy": ("compra_a.webp", 768 / 251, 768),  # ButtonBuyBonus
    "button_menu": ("menu_b.webp", 1, 384),
}
# icon name: (source sheet, position in its row of 4)
ICONS = {
    "auto_spin": ("iconos1_a.webp", 0),
    "turbo": ("iconos1_a.webp", 1),
    "menu": ("iconos1_a.webp", 2),
    "increase": ("iconos1_a.webp", 3),
    "decrease": ("iconos2_a.webp", 0),
}


def pad_to(img, aspect):
    """Crop to content, then pad with transparency to the given width / height."""
    img = img.crop(img.getbbox())
    w, h = img.size
    W, H = (w, round(w / aspect)) if w / h > aspect else (round(h * aspect), h)
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    out.paste(img, ((W - w) // 2, (H - h) // 2), img)
    return out


def key_background(img, threshold=60):
    """Make the background transparent where it touches the image corners, so a cream fill inside an icon
    outline stays. The background is a soft gradient, hence a flood fill with a threshold."""
    rgb = img.convert("RGB")
    marker = (255, 0, 255)
    for corner in ((0, 0), (rgb.width - 1, 0), (0, rgb.height - 1), (rgb.width - 1, rgb.height - 1)):
        ImageDraw.floodfill(rgb, corner, marker, thresh=threshold)
    out = img.convert("RGBA")
    out.putalpha(Image.fromarray(np.where((np.asarray(rgb) == marker).all(axis=2), 0, 255).astype(np.uint8)))
    return out


def icon_columns(img, count=4):
    """Split a keyed row of icons at the empty columns between them."""
    filled = np.asarray(img.getchannel("A")).max(axis=0) > 30
    runs, start = [], None
    for x, f in enumerate(filled):
        if f and start is None:
            start = x
        if not f and start is not None:
            runs.append((start, x))
            start = None
    if start is not None:
        runs.append((start, len(filled)))
    runs = sorted(sorted(runs, key=lambda r: r[1] - r[0], reverse=True)[:count])  # drop specks
    return [img.crop((x0, 0, x1, img.height)) for x0, x1 in runs]


def frame_window(frame):
    """Inner window of the frame, as fractions of the image: the dark centre connected to the middle."""
    a = np.asarray(frame).astype(np.int32)
    h, w = a.shape[:2]
    dark = (a[..., :3].sum(axis=2) < 150) & (a[..., 3] > 200)  # transparent pixels outside are not window
    row, col = dark[h // 2], dark[:, w // 2]
    xs, ys = np.nonzero(row)[0], np.nonzero(col)[0]
    return (xs.max() - xs.min()) / w, (ys.max() - ys.min()) / h


def main(src):
    for name, (file, aspect, max_side) in PIECES.items():
        save_sprite(fit(pad_to(Image.open(os.path.join(src, file)).convert("RGBA"), aspect), max_side), name, UI)
        print("ok", name)
    sheets = {}
    for name, (file, index) in ICONS.items():
        if file not in sheets:
            sheets[file] = icon_columns(key_background(Image.open(os.path.join(src, file))))
        icon = sheets[file][index]
        save_sprite(fit(icon.crop(icon.getbbox()), 128), f"icon_{name}", UI)
        print("ok", f"icon_{name}")
    frame = Image.open(os.path.join(src, "marco_b.webp")).convert("RGBA")
    frame = frame.crop(frame.getbbox())
    save_sprite(fit(frame, 1600), "board_frame", FX)
    print("ok board_frame, inner window %.3f x %.3f of the image" % frame_window(frame))


if __name__ == "__main__":
    main(sys.argv[1])
