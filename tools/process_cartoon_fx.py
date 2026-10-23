"""Glow effects and win particles from the Ludo cartoon art.

Usage (from the repo root):
    math\\env\\Scripts\\python.exe tools\\process_cartoon_fx.py "<slot>/7. Cartoon/chibi/efectos"

Writes web/apps/midnight-milonga/static/assets/sprites/milonga/fx/:
    win_sparkles_sheet.webp/.json  win particles, one frame per golden sparkle (see particle_sheet)
    sparkles.webp                  big-win backdrop, padded square
    anticipation.webp              reel anticipation column; its hard edges are faded out, since it is drawn
                                   with additive blending and would otherwise read as a solid block
    abrazo_trail.webp              golden trail across the Abrazo row
"""

import os
import sys

import numpy as np
from PIL import Image

from sprite_utils import FX, fit, particle_sheet, save_sprite
from process_cartoon_ui import pad_to


def soften_column(img, edge=0.9, ends=0.2):
    """Fade the alpha towards the left/right edges (cosine over `edge` of the half width) and the top/bottom
    ends (linear over `ends` of the height)."""
    a = np.asarray(img).astype(np.float32)
    h, w = a.shape[:2]
    x = np.abs(np.linspace(-1, 1, w))
    side = np.clip((1 - x) / edge, 0, 1)
    side = 0.5 - 0.5 * np.cos(side * np.pi)
    y = np.linspace(0, 1, h)
    end = np.clip(np.minimum(y, 1 - y) / ends, 0, 1)
    a[..., 3] *= end[:, None] * side[None, :]
    return Image.fromarray(a.astype(np.uint8))


def load(src, file):
    img = Image.open(os.path.join(src, file)).convert("RGBA")
    return img.crop(img.getbbox())


def main(src):
    print("win sparkles:", particle_sheet(load(src, "particulas_destellos.webp"), "win_sparkles_sheet", FX), "frames")
    save_sprite(fit(pad_to(load(src, "destellos_b.webp"), 1), 1024), "sparkles", FX)
    save_sprite(fit(soften_column(load(src, "anticipacion_b.webp")), 1024), "anticipation", FX)
    save_sprite(fit(load(src, "estela_b.webp"), 1024), "abrazo_trail", FX)
    print("ok sparkles, anticipation, abrazo_trail")


if __name__ == "__main__":
    main(sys.argv[1])
