"""Turn the Gemini animation art into game sprites.

Usage (from the repo root):
    math\\env\\Scripts\\python.exe tools\\process_animation_art.py "<slot>/4. Animaciones"

- "key": plain chroma-green background (#00B140) removed, green spill corrected, cropped to content.
- "add": glow art on pure black, kept as is (drawn with additive blending, black disappears).
- "opaque": full backgrounds, resized only.
Writes web/apps/midnight-milonga/static/assets/sprites/milonga/fx/<name>.png|jpg
"""

import json
import os
import sys

import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "web", "apps", "midnight-milonga", "static", "assets", "sprites", "milonga", "fx")

# output name: (folder prefix, file name start, mode, max size)
ART = {
    "loading_bg": ("01.", "Fondo de carga", "opaque", 2048),
    "loading_bar": ("01.", "Marco de la barra", "key", 1024),
    "loading_rose": ("01.", "cono de carga", "key", 512),
    "rosa_burst": ("10.", "explosion", "add", 768),
    "rosa_flying": ("10.", "single red rose", "key", 512),
    "anticipation": ("11.", "Anticipaci", "add", 1024),
    "win_frame": ("11.", "Marco de s", "add", 512),
    "board_frame": ("11.", "Marco final", "key", 1600),
    "pista_title": ("02.", "Cartel del t", "key", 1024),
    "pista_bg": ("02.", "Fondo", "opaque", 2048),
    "total_win_panel": ("03.", "Panel TOTAL WIN", "key", 1024),
    "spins_plate": ("02.", "Placa para", "key", 768),
    "tanda_title": ("04.", "Cartel del t", "key", 1024),
    "tanda_bg": ("04.", "Fondo", "opaque", 2048),
    "tanda_couple": ("04.", "Pareja en el haz", "key", 1024),
    "big_win": ("05.", "BIG WIN", "key", 1024),
    "super_win": ("05.", "SUPER WIN", "key", 1024),
    "mega_win": ("05.", "MEGA WIN", "key", 1024),
    "epic_win": ("05.", "EPIC WIN", "key", 1024),
    "max_win": ("05.", "MAX WIN", "key", 1024),
    "sparkles": ("06.", "golden sparkle", "add", 1024),
    "petals": ("06.", "red rose", "key", 1024),
    "metronome_body": ("07.", "Cuerpo del metr", "key", 768),
    "metronome_pendulum": ("07.", "ndulo suelto", "key", 768),
    "banner_rosa": ("08.", "LA ROSA ROJA", "key", 1024),
    "banner_abrazo": ("08.", "EL ABRAZO", "key", 1024),
    "abrazo_trail": ("09.", "Estela dorada", "add", 1024),
    "abrazo_1": ("09.", "walking toward", "key", 768),
    "abrazo_2": ("09.", "meeting and joining", "key", 768),
    "abrazo_3": ("09.", "in a close tango", "key", 768),
    "abrazo_4": ("09.", "in a dramatic final", "key", 768),
}


def find(src, prefix, start):
    for folder in os.listdir(src):
        if folder.startswith(prefix + " "):
            for name in os.listdir(os.path.join(src, folder)):
                if start in name:
                    return os.path.join(src, folder, name)
    raise FileNotFoundError(f"{prefix} / {start}")


BEAM_ART = {"tanda_couple", "abrazo_1", "abrazo_2", "abrazo_3", "abrazo_4"}


def key_green(img, beam=False):
    """Remove the chroma green: alpha from how much green dominates red/blue, then despill and crop.

    beam=True also removes yellow-green spotlight haze painted over the green: there green beats red,
    which never happens on skin, the red dress, the black suit or gold.
    """
    a = np.asarray(img.convert("RGB")).astype(np.int32)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    green = g - np.maximum(r, b)
    alpha = np.clip(255 - (green - 18) * 255 // 50, 0, 255)
    if beam:
        # opaque only where red clearly beats green (skin, hair, red dress, gold); fades out as g reaches r
        haze = np.clip((r - g + 2) * 255 // 22, 0, 255)
        pale_core = (np.minimum(np.minimum(r, g), b) > 150) & (g >= r - 12)  # near-white beam origin
        is_beam = ((g * 100 > b * 118) & (g > 60)) | pale_core
        alpha = np.minimum(alpha, np.where(is_beam, haze, 255))
        green = np.maximum(green, g - r)
    # near-white edge strips some generations leave around the art
    white = (r > 225) & (g > 225) & (b > 225)
    alpha = np.where(white, 0, alpha)
    g = np.where(green > 0, np.minimum(g, np.maximum(r, b)), g)  # despill
    out = Image.fromarray(np.dstack([r, g, b, alpha]).astype(np.uint8), "RGBA")
    # drop the faint halo left by light beams painted over the green
    out.putalpha(out.getchannel("A").point(lambda v: 0 if v < 24 else v))
    if beam:
        out = keep_main_figure(out)
    return out.crop(out.getchannel("A").getbbox())


def keep_main_figure(img):
    """Clean spotlight leftovers around the dancers.

    1. In the upper-left area (where the beam comes from) bright yellowish pixels are removed: the beam has
       green close to red, while skin and gold have red well above green, and the black suit is dark.
    2. Only large connected regions are kept (both dancers, even when they stand apart); stray blobs go.
    """
    from PIL import ImageDraw, ImageFilter

    a = np.asarray(img).astype(np.int32)
    r, g, b, alpha = a[..., 0], a[..., 1], a[..., 2], a[..., 3]
    h, w = alpha.shape
    yy, xx = np.mgrid[0:h, 0:w]
    beam_zone = (xx < w * 0.5) & (yy < h * 0.75)
    beam_colour = (g >= r - 15) & (np.maximum(r, g) > 110)
    alpha = np.where(beam_zone & beam_colour, 0, alpha)

    # label regions on a quarter-size mask with flood fills, keep those >= 8% of the largest
    small = Image.fromarray(np.where(alpha > 60, 255, 0).astype(np.uint8)).resize((w // 4, h // 4), Image.NEAREST)
    labels, label = {}, 1
    arr = np.asarray(small).copy()
    for y, x in zip(*np.nonzero(arr == 255)):
        if np.asarray(small)[y, x] != 255:
            continue
        ImageDraw.floodfill(small, (int(x), int(y)), label)
        labels[label] = int((np.asarray(small) == label).sum())
        label += 1
        if label >= 255:
            break
    biggest = max(labels.values())
    keep_ids = [k for k, v in labels.items() if v >= biggest * 0.08]
    keep = np.isin(np.asarray(small), keep_ids).astype(np.uint8) * 255
    keep = Image.fromarray(keep).resize((w, h), Image.NEAREST).filter(ImageFilter.MaxFilter(9))
    alpha = np.minimum(alpha, np.asarray(keep))
    return Image.fromarray(np.dstack([r, g, b, alpha]).astype(np.uint8), "RGBA")


def key_black(img, floor=16, gain=5):
    """Art on black (the game title): brightness becomes alpha."""
    alpha = img.convert("L").point(lambda v: 0 if v < floor else min(255, (v - floor) * gain))
    out = img.convert("RGBA")
    out.putalpha(alpha)
    return out.crop(alpha.getbbox())


def black_to_alpha(img, floor=6, gain=3):
    """Glow art on black, drawn additively: also make black transparent so no renderer can show the
    black square (seen in Chrome as a light box behind the sparkles). Keeps the canvas size (no crop)."""
    rgb = img.convert("RGB")
    alpha = Image.fromarray(np.asarray(rgb).max(axis=2).astype(np.uint8)).point(
        lambda v: 0 if v < floor else min(255, (v - floor) * gain)
    )
    out = rgb.convert("RGBA")
    out.putalpha(alpha)
    return out


def petal_sheet(petals, out_dir, max_side=160):
    """Split the keyed petals image into separate frames and write a Pixi spritesheet (same format as the
    sample coin sheet: frames 1.png..N.png and an animation named "coin", so the particle emitter can use it)."""
    from PIL import ImageDraw

    alpha = petals.getchannel("A")
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
    frames = [fit(petals.crop(box), max_side) for box in boxes]
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
    sheet.save(os.path.join(out_dir, "petals_sheet.png"), optimize=True)
    data = {
        "frames": meta,
        "animations": {"coin": list(meta)},
        "meta": {"image": "petals_sheet.png", "format": "RGBA8888", "size": {"w": sheet.width, "h": sheet.height}, "scale": "1"},
    }
    with open(os.path.join(out_dir, "petals_sheet.json"), "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=1)
    return len(frames)


def fit(img, max_side):
    s = min(1.0, max_side / max(img.size))
    return img.resize((int(img.width * s), int(img.height * s)), Image.LANCZOS) if s < 1 else img


def main(src):
    os.makedirs(OUT, exist_ok=True)
    for name, (prefix, start, mode, max_side) in ART.items():
        img = Image.open(find(src, prefix, start))
        if mode == "key":
            fit(key_green(img, beam=name in BEAM_ART), max_side).save(os.path.join(OUT, f"{name}.png"), optimize=True)
        elif mode == "add":
            fit(black_to_alpha(img), max_side).save(os.path.join(OUT, f"{name}.png"), optimize=True)
        else:
            fit(img.convert("RGB"), max_side).save(os.path.join(OUT, f"{name}.jpg"), quality=86)
        print("ok", name)

    petals = Image.open(os.path.join(OUT, "petals.png")).convert("RGBA")
    print("petal frames:", petal_sheet(petals, OUT))

    # game title from the concept art folder next to "para animaciones"
    title = Image.open(os.path.join(src, "..", "3. Arte Midnight Milonga", "logo.jpg"))
    fit(key_black(title), 1400).save(os.path.join(OUT, "title.png"), optimize=True)
    print("ok title")


if __name__ == "__main__":
    main(sys.argv[1])
