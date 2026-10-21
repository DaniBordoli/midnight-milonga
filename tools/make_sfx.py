"""Synthesize the short UI / reel sound effects (no samples, no third-party licences).

Usage: math\\env\\Scripts\\python.exe tools\\make_sfx.py <output folder>
Writes 44.1 kHz mono WAVs named like the game's sound keys (sfx_reel_stop_1.wav, ...).
"""

import os
import sys
import wave

import numpy as np

RATE = 44100
rng = np.random.default_rng(7)


def t(seconds):
    return np.arange(int(RATE * seconds)) / RATE


def env(x, attack, decay):
    """Fast attack, exponential decay (decay = time constant in seconds)."""
    tt = np.arange(len(x)) / RATE
    return x * np.minimum(1, tt / attack) * np.exp(-tt / decay)


def lowpass(x, cutoff):
    a = np.exp(-2 * np.pi * cutoff / RATE)
    y = np.empty_like(x)
    acc = 0.0
    for i, v in enumerate(x):
        acc = (1 - a) * v + a * acc
        y[i] = acc
    return y


def piano(freq, seconds, decay=0.35):
    """Soft piano-like note: a few harmonics, higher ones dying faster."""
    tt = t(seconds)
    out = sum(np.sin(2 * np.pi * freq * h * tt) * np.exp(-tt * h / decay) / h**1.3 for h in range(1, 7))
    return env(out, 0.004, decay * 2)


def bell(freq, seconds):
    """Bell / chime: inharmonic partials."""
    tt = t(seconds)
    partials = [(1, 1.0, 0.9), (2.76, 0.5, 0.45), (5.4, 0.3, 0.25), (8.93, 0.15, 0.15)]
    out = sum(a * np.sin(2 * np.pi * freq * p * tt) * np.exp(-tt / d) for p, a, d in partials)
    return env(out, 0.002, 2)


def reed(freq, seconds):
    """Bandoneon-ish reed: two slightly detuned saw-like tones."""
    tt = t(seconds)
    out = np.zeros_like(tt)
    for detune in (1.0, 1.004):
        out += sum(np.sin(2 * np.pi * freq * detune * h * tt) / h for h in range(1, 10))
    return lowpass(out, 2500)


def btn_general():
    x = rng.standard_normal(int(RATE * 0.06))
    click = env(lowpass(x, 3000), 0.0005, 0.006)
    tick = env(np.sin(2 * np.pi * 1800 * t(0.06)), 0.0005, 0.01)
    return click * 0.6 + tick * 0.5


def btn_spin():
    length = 0.9
    tt = t(length)
    noise = rng.standard_normal(len(tt))
    # whoosh: noise through a lowpass whose cutoff sweeps up
    sweep = np.empty_like(noise)
    acc = 0.0
    for i, v in enumerate(noise):
        cutoff = 400 + 3000 * (i / len(noise))
        a = np.exp(-2 * np.pi * cutoff / RATE)
        acc = (1 - a) * v + a * acc
        sweep[i] = acc
    swell = np.sin(np.pi * np.clip(tt / length, 0, 1)) ** 2
    breath = reed(220, length) * swell * 0.25
    return sweep * swell * 0.8 + breath


def reel_stop():
    tt = t(0.25)
    freq = 120 * np.exp(-tt * 12) + 60  # pitch drops like a damped wooden hit
    thud = np.sin(2 * np.pi * np.cumsum(freq) / RATE)
    knock = lowpass(rng.standard_normal(len(tt)), 1200)
    return env(thud, 0.001, 0.05) + env(knock, 0.0005, 0.01) * 0.4


def scatter_stop(step):
    # each extra scatter rings a semitone pair higher: rising tension
    base = 880 * 2 ** ((step - 1) * 2 / 12)
    return bell(base, 1.0) + bell(base * 1.5, 1.0) * 0.35


def winlevel_small():
    first = piano(659.25, 1.0)  # E5
    second = np.concatenate([np.zeros(int(RATE * 0.12)), piano(987.77, 0.88)])  # B5
    return first + second


def write(path, x, peak=0.85):
    x = x / max(1e-9, np.abs(x).max()) * peak
    fade = min(len(x), int(RATE * 0.005))
    x[-fade:] *= np.linspace(1, 0, fade)
    data = (x * 32767).astype("<i2").tobytes()
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(data)
    print("ok", os.path.basename(path), f"{len(x) / RATE:.2f}s")


def main(out):
    os.makedirs(out, exist_ok=True)
    sounds = {
        "sfx_btn_general": (btn_general(), 0.6),
        "sfx_btn_spin": (btn_spin(), 0.7),
        "sfx_reel_stop_1": (reel_stop(), 0.8),
        "sfx_winlevel_small": (winlevel_small(), 0.7),
    }
    for step in range(1, 6):
        sounds[f"sfx_scatter_stop_{step}"] = (scatter_stop(step), 0.7)
    for name, (x, peak) in sounds.items():
        write(os.path.join(out, f"{name}.wav"), x, peak)


if __name__ == "__main__":
    main(sys.argv[1])
