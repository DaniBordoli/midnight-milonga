"""Build the game's audio sprite (sounds.mp3 + sounds.json) from the files in an audio folder.

Usage: math\\env\\Scripts\\python.exe tools\\build_audio_sprite.py "<slot>/6. Audio"
Needs ffmpeg on PATH. Effects come from tools/make_sfx.py (<sound key>.wav); the two music tracks are
licensed downloads (see MUSIC below), looped as they are. The big-win music beds are an 8 s loop cut from
the free-spin track, shared by every tier until each tier has its own music.
"""

import json
import os
import subprocess
import sys
import tempfile

import numpy as np

RATE = 44100
GAP = 1.0  # seconds of silence between sounds so the browser never bleeds into the next one
OUT = os.path.join(os.path.dirname(__file__), "..", "web", "apps", "midnight-milonga", "static", "assets", "audio")

# sound key -> file name fragment of the licensed track (Pixabay Content License)
MUSIC = {
    "bgm_main": "rosas-de-la-noche",
    "bgm_freespin": "tango-bleu",
}
WIN_BEDS = ["bgm_winlevel_big", "bgm_winlevel_superwin", "bgm_winlevel_mega", "bgm_winlevel_epic", "bgm_winlevel_max"]
# playback volume per sound (sounds.json config, applied by the SDK player); everything else plays at 1
# music sits well under the effects; free spins and big wins a little louder than the base game
VOLUME = {"bgm_main": 0.25, "bgm_freespin": 0.35, **{key: 0.4 for key in WIN_BEDS}}
LOOPED = set(MUSIC) | set(WIN_BEDS) | {"sfx_bigwin_coinloop"}


def decode(path):
    """Any audio file -> float32 stereo array at RATE."""
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "2", "-ar", str(RATE), "-"],
        check=True, capture_output=True,
    ).stdout
    return np.frombuffer(raw, dtype="<f4").reshape(-1, 2).copy()


def trim_silence(x, threshold=0.003):
    loud = np.where(np.abs(x).max(axis=1) > threshold)[0]
    return x[loud[0] : loud[-1] + 1] if len(loud) else x


def edge_fades(x, seconds=0.02):
    n = min(len(x) // 2, int(RATE * seconds))
    ramp = np.linspace(0, 1, n)[:, None]
    x[:n] *= ramp
    x[-n:] *= ramp[::-1]
    return x


def loop_excerpt(x, start, seconds, crossfade=0.5):
    """Cut `seconds` from `start` and crossfade the tail into the head so it loops without a seam."""
    a, n, c = int(RATE * start), int(RATE * seconds), int(RATE * crossfade)
    body = x[a : a + n].copy()
    tail = x[a + n : a + n + c]
    ramp = np.linspace(0, 1, c)[:, None]
    body[:c] = body[:c] * ramp + tail * (1 - ramp)
    return body


def files(folder):
    """Every file under the audio folder (music and effects live in sub-folders)."""
    return [os.path.join(d, n) for d, _, names in os.walk(folder) for n in sorted(names)]


def find(folder, fragment):
    for path in files(folder):
        if fragment in os.path.basename(path).lower():
            return path
    raise FileNotFoundError(fragment)


def main(folder):
    sounds = {}
    for key, fragment in MUSIC.items():
        sounds[key] = edge_fades(trim_silence(decode(find(folder, fragment))))
    bed = loop_excerpt(sounds["bgm_freespin"], start=20, seconds=8) * 0.9
    for key in WIN_BEDS:
        sounds[key] = bed
    for path in files(folder):
        if path.endswith(".wav"):
            sounds[os.path.basename(path)[:-4]] = decode(path)

    # normalise music loudness to a common peak, effects keep the levels make_sfx.py gave them
    for key in MUSIC:
        sounds[key] *= 0.8 / max(1e-9, np.abs(sounds[key]).max())

    gap = np.zeros((int(RATE * GAP), 2), dtype="<f4")
    parts, sprite, cursor = [], {}, 0
    for key in sorted(sounds):
        x = sounds[key].astype("<f4")
        sprite[key] = [round(cursor / RATE * 1000, 3), round(len(x) / RATE * 1000, 3)] + ([True] if key in LOOPED else [])
        parts += [x, gap]
        cursor += len(x) + len(gap)
    audio = np.concatenate(parts)

    os.makedirs(OUT, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        raw = os.path.join(tmp, "sounds.f32")
        audio.tofile(raw)
        source = ["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ac", "2", "-ar", str(RATE), "-i", raw]
        # one format only (every browser plays MP3) at 96 kbps: Stake rates bundle size
        subprocess.run(source + ["-c:a", "libmp3lame", "-b:a", "96k", os.path.join(OUT, "sounds.mp3")], check=True)

    manifest = {
        "src": ["./assets/audio/sounds.mp3"],
        "sprite": sprite,
        "config": {key: {"volume": VOLUME.get(key, 1)} for key in sprite},
    }
    with open(os.path.join(OUT, "sounds.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent="\t")
    print(f"{len(sprite)} sounds, {cursor / RATE:.1f}s total")


if __name__ == "__main__":
    main(sys.argv[1])
