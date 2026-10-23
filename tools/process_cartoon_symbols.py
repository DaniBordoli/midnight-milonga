"""Turn the Ludo cartoon symbols into game sprites: a still per symbol plus a looping win spritesheet.

Usage (from the repo root):
    math\\env\\Scripts\\python.exe tools\\process_cartoon_symbols.py "<slot>/7. Cartoon/chibi"

Reads <dir>/elegidos/<code>.webp (stills, transparent) and <dir>/animaciones/<code>_win_sheet.webp, laid out
as described in <dir>/animaciones/sheets.json ({"<code>": {"cols": c, "rows": r, "frames": n}}).
Writes web/apps/midnight-milonga/static/assets/sprites/milonga/symbols/:
    <code>.webp           still, centred in a CELL x CELL square
    <code>_win.webp/.json Pixi spritesheet, WIN_PAD x larger cells so the motion has room; its first frame
                          lines up with the still, so the switch to the win animation does not jump
"""

import json
import math
import os
import sys

import numpy as np
from PIL import Image

from sprite_utils import FX, save_sprite

OUT = os.path.join(os.path.dirname(FX), "symbols")
CELL = 256
FILL = 0.92  # share of the cell the still's longest side takes
WIN_PAD = 1.25  # must match WIN_SCALE in src/game/constants.ts
COLS = 4


def content(img):
    return img.crop(img.getbbox())


def still(img):
    img = content(img)
    s = CELL * FILL / max(img.size)
    img = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    cell = Image.new("RGBA", (CELL, CELL), (0, 0, 0, 0))
    cell.paste(img, ((CELL - img.width) // 2, (CELL - img.height) // 2), img)
    return cell, s, img.size


def silhouette(img, size):
    return np.asarray(img.getchannel("A").resize((size, size), Image.BILINEAR)) > 128


def match_first_frame(frame, still_cell, side, s0, c0):
    """Scale and centre that lay the first frame's silhouette best over the still's (highest overlap), so the
    switch to the animation does not jump. Starts from the bounding-box guess (s0, c0), which is thrown off
    when the first frame already shows sparkles or streaks around the object."""
    work = side // 2  # compare at half resolution
    target = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    target.paste(still_cell, ((side - CELL) // 2, (side - CELL) // 2), still_cell)
    target = silhouette(target, work)
    best = (-1.0, s0, c0)
    for s in np.arange(0.8, 1.21, 0.02) * s0:
        f = frame.resize((max(1, round(frame.width * s)), max(1, round(frame.height * s))), Image.LANCZOS)
        cx0, cy0 = c0[0] * s / s0, c0[1] * s / s0
        for dx in range(-16, 17, 2):
            for dy in range(-16, 17, 2):
                cell = Image.new("RGBA", (side, side), (0, 0, 0, 0))
                cell.paste(f, (round(side / 2 - cx0 + dx), round(side / 2 - cy0 + dy)), f)
                m = silhouette(cell, work)
                iou = (m & target).sum() / max(1, (m | target).sum())
                if iou > best[0]:
                    best = (iou, s, (cx0 - dx, cy0 - dy))
    return best[1], best[2]


def win_sheet(sheet, layout, still_size, still_cell):
    fw, fh = sheet.width // layout["cols"], sheet.height // layout["rows"]
    frames = [
        sheet.crop(((i % layout["cols"]) * fw, (i // layout["cols"]) * fh, (i % layout["cols"] + 1) * fw, (i // layout["cols"] + 1) * fh))
        for i in range(layout["frames"])
    ]
    # scale and offset come from the first frame, so it matches the still
    x0, y0, x1, y1 = frames[0].getbbox()
    side = round(CELL * WIN_PAD)
    s0 = max(still_size) / max(x1 - x0, y1 - y0)
    s, (cx, cy) = match_first_frame(frames[0], still_cell, side, s0, ((x0 + x1) / 2 * s0, (y0 + y1) / 2 * s0))
    out = Image.new("RGBA", (side * COLS, side * math.ceil(len(frames) / COLS)), (0, 0, 0, 0))
    for i, f in enumerate(frames):
        f = f.resize((round(fw * s), round(fh * s)), Image.LANCZOS)
        cell = Image.new("RGBA", (side, side), (0, 0, 0, 0))
        cell.paste(f, (round(side / 2 - cx), round(side / 2 - cy)), f)  # clips motion beyond the padded cell
        out.paste(cell, ((i % COLS) * side, (i // COLS) * side))
    return out, side, len(frames)


def write_sheet_json(code, side, count, size):
    names = [f"{code}_win_{i}" for i in range(count)]  # non-numeric keys keep insertion order in Pixi
    frames = {
        n: {
            "frame": {"x": (i % COLS) * side, "y": (i // COLS) * side, "w": side, "h": side},
            "rotated": False,
            "trimmed": False,
            "spriteSourceSize": {"x": 0, "y": 0, "w": side, "h": side},
            "sourceSize": {"w": side, "h": side},
        }
        for i, n in enumerate(names)
    }
    data = {
        "frames": frames,
        "animations": {"win": names},
        "meta": {"image": f"{code}_win.webp", "format": "RGBA8888", "size": {"w": size[0], "h": size[1]}, "scale": "1"},
    }
    with open(os.path.join(OUT, f"{code}_win.json"), "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=1)


def main(src):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(src, "animaciones", "sheets.json"), encoding="utf-8") as fh:
        layouts = json.load(fh)
    for name in sorted(os.listdir(os.path.join(src, "elegidos"))):
        code = os.path.splitext(name)[0]
        cell, _, size = still(Image.open(os.path.join(src, "elegidos", name)).convert("RGBA"))
        save_sprite(cell, code, OUT)
        if code in layouts:
            sheet = Image.open(os.path.join(src, "animaciones", f"{code}_win_sheet.webp")).convert("RGBA")
            out, side, count = win_sheet(sheet, layouts[code], size, cell)
            save_sprite(out, f"{code}_win", OUT)
            write_sheet_json(code, side, count, out.size)
        print("ok", code, "+ win" if code in layouts else "(still only)")


if __name__ == "__main__":
    main(sys.argv[1])
