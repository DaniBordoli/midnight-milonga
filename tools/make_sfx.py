"""Synthesize the short UI / reel sound effects (no samples, no third-party licences).

Usage: math\\env\\Scripts\\python.exe tools\\make_sfx.py <output folder> [--options]
Writes 44.1 kHz mono WAVs named like the game's sound keys (sfx_reel_stop_1.wav, ...).
--options writes the alternative takes in OPTIONS instead, for review.
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


def at(x, seconds, length):
    """Place x starting at `seconds` inside a silent buffer of `length` seconds."""
    out = np.zeros(int(RATE * length))
    start = int(RATE * seconds)
    end = min(len(out), start + len(x))
    out[start:end] += x[: end - start]
    return out


# A minor / E7 voicings used by the tango-flavoured stingers
A_MINOR = [220.0, 261.63, 329.63, 440.0]
E7 = [164.81, 207.65, 246.94, 293.66]


def chord(freqs, seconds, decay=0.6):
    return sum(piano(f, seconds, decay) for f in freqs)


def reed_chord(freqs, seconds):
    tt = t(seconds)
    swell = np.minimum(1, tt / 0.08) * np.exp(-tt / (seconds * 0.6))
    return sum(reed(f, seconds) for f in freqs) * swell


def jingle_intro():
    # rising bandoneon arpeggio landing on A minor
    notes = [220.0, 261.63, 329.63, 440.0]
    out = sum(at(reed_chord([f], 0.5), i * 0.16, 2.0) for i, f in enumerate(notes))
    return out + at(reed_chord(A_MINOR, 1.4), 0.64, 2.0) * 0.8


def superfreespin():
    hit = chord(A_MINOR + [110.0], 4.0, 0.9)
    run = sum(at(bell(880 * 2 ** (i / 12), 1.2), 0.4 + i * 0.07, 4.0) for i in range(0, 13, 2))
    return hit + run * 0.5 + at(reed_chord(A_MINOR, 2.5), 1.3, 4.0) * 0.6


def scatter_win():
    return sum(at(bell(f, 2.5), i * 0.12, 3.0) for i, f in enumerate([1318.5, 1567.98, 1975.5, 2637.0]))


def youwon_panel():
    return at(chord(E7, 1.0, 0.5), 0, 3.0) + at(chord(A_MINOR, 2.2, 0.9), 0.55, 3.0) * 1.2


def winlevel_end():
    return chord([220.0, 329.63, 440.0, 523.25], 2.0, 0.7)


def bigwin_loop():
    # seamless loop of tiny golden chimes: events wrap around the loop end
    length = 10.0
    out = np.zeros(int(RATE * length))
    pentatonic = [1760.0, 1975.5, 2217.5, 2637.0, 2960.0]
    for i in range(70):
        note = bell(pentatonic[rng.integers(len(pentatonic))], 0.6) * rng.uniform(0.2, 0.5)
        start = rng.integers(len(out))
        idx = (start + np.arange(len(note))) % len(out)
        np.add.at(out, idx, note)
    return out


def wild_explode():
    swell = reed_chord([329.63, 440.0, 523.25], 1.5)
    sparkle = sum(at(bell(f, 0.8), 0.45 + i * 0.05, 1.5) for i, f in enumerate([1760.0, 2217.5, 2637.0]))
    return swell + sparkle * 0.6


def multiplier_landing():
    noise = lowpass(rng.standard_normal(int(RATE * 1.0)), 1500)
    whoosh = noise * np.sin(np.pi * np.clip(t(1.0) / 0.35, 0, 1)) ** 2 * (t(1.0) < 0.35)
    return whoosh * 0.5 + at(bell(1318.5, 0.7) + bell(1975.5, 0.7) * 0.5, 0.3, 1.0)


def multiplier_update():
    tick = reel_stop()[: int(RATE * 0.06)]
    out = sum(at(tick, s, 1.5) for s in [0, 0.22, 0.4, 0.54, 0.65])
    return out * 0.7 + at(piano(880.0, 0.8), 0.72, 1.5)


def anticipation():
    # tremolo reed with a slowly rising pitch and a heartbeat pulse underneath
    length = 7.0
    tt = t(length)
    freq = 110 * 2 ** (tt / length)
    phase = 2 * np.pi * np.cumsum(freq) / RATE
    tone = sum(np.sin(phase * h) / h for h in range(1, 8))
    tremolo = 0.6 + 0.4 * np.sin(2 * np.pi * 9 * tt)
    beat = sum(at(env(np.sin(2 * np.pi * 55 * t(0.2)), 0.002, 0.06), s, length) for s in np.arange(0, length, 0.55))
    return lowpass(tone, 1800) * tremolo * np.minimum(1, tt / 1.5) + beat * 0.8


def pluck(freq, seconds, brightness=0.5):
    """Plucked string (Karplus-Strong): double-bass / guitar pizzicato."""
    n = int(RATE / freq)
    buf = rng.uniform(-1, 1, n)
    out = np.empty(int(RATE * seconds))
    for i in range(len(out)):
        out[i] = buf[i % n]
        buf[i % n] = 0.996 * (brightness * buf[i % n] + (1 - brightness) * buf[(i + 1) % n])
    return env(out, 0.001, seconds)


# ---- options offered for review (written with --options; the chosen one is mapped in OPTIONS_CHOSEN) ----


def reel_stop_felt():
    """A: soft felt-hammer thump, darker and shorter than the original."""
    tt = t(0.2)
    freq = 90 * np.exp(-tt * 20) + 55
    thump = np.sin(2 * np.pi * np.cumsum(freq) / RATE)
    return lowpass(env(thump, 0.003, 0.04), 900)


def reel_stop_clave():
    """B: wooden clave click, bright and dry (a classic percussion accent)."""
    tt = t(0.15)
    tone = np.sin(2 * np.pi * 2500 * tt) + 0.5 * np.sin(2 * np.pi * 3700 * tt)
    return env(tone, 0.0005, 0.02)


def reel_stop_bass():
    """C: double-bass pizzicato on A (the tango 'marcato' bass note)."""
    return pluck(110.0, 0.35, 0.3) + env(np.sin(2 * np.pi * 110 * t(0.35)), 0.002, 0.08) * 0.4


def anticipation_bass():
    """A: walking double-bass pizzicato that accelerates and climbs (tango marcato)."""
    length = 7.0
    out = np.zeros(int(RATE * length))
    notes = [110.0, 123.47, 130.81, 146.83, 164.81, 174.61, 196.0, 220.0]
    s, gap, i = 0.0, 0.5, 0
    while s < length - 0.3:
        out += at(pluck(notes[i % len(notes)] * (2 if i >= 16 else 1), 0.4, 0.3), s, length)
        s, gap, i = s + gap, max(0.12, gap * 0.9), i + 1
    return out * np.minimum(1, t(length) / 0.5)


def anticipation_violin():
    """B: violin-like tremolo, rising a fifth and swelling, no heartbeat."""
    length = 7.0
    tt = t(length)
    freq = 440 * 2 ** (7 / 12 * tt / length) * (1 + 0.004 * np.sin(2 * np.pi * 5.5 * tt))  # with vibrato
    phase = 2 * np.pi * np.cumsum(freq) / RATE
    tone = lowpass(sum(np.sin(phase * h) / h for h in range(1, 12)), 3500)
    tremolo = 0.55 + 0.45 * np.abs(np.sin(2 * np.pi * 7 * tt))
    return tone * tremolo * (tt / length) ** 1.5


def anticipation_bandoneon():
    """C: bandoneon chord stabs (staccato marcato) getting faster, louder and higher."""
    length = 7.0
    out = np.zeros(int(RATE * length))
    s, gap, i = 0.0, 0.45, 0
    while s < length - 0.2:
        shift = 2 ** (min(i, 20) // 5 * 2 / 12)  # step up a tone every five stabs
        stab = reed_chord([f * shift for f in [220.0, 261.63, 329.63]], 0.18)
        out += at(stab * (0.4 + 0.6 * s / length), s, length)
        s, gap, i = s + gap, max(0.14, gap * 0.92), i + 1
    return out


OPTIONS = {
    "sfx_reel_stop_1 A felt": reel_stop_felt,
    "sfx_reel_stop_1 B clave": reel_stop_clave,
    "sfx_reel_stop_1 C bass": reel_stop_bass,
    "sfx_anticipation A bass": anticipation_bass,
    "sfx_anticipation B violin": anticipation_violin,
    "sfx_anticipation C bandoneon": anticipation_bandoneon,
}


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


def main(out, options=False):
    os.makedirs(out, exist_ok=True)
    if options:
        for name, make in OPTIONS.items():
            write(os.path.join(out, f"{name}.wav"), make(), 0.7)
        return
    sounds = {
        "sfx_btn_general": (btn_general(), 0.6),
        "sfx_btn_spin": (btn_spin(), 0.7),
        "sfx_reel_stop_1": (reel_stop(), 0.8),
        "sfx_winlevel_small": (winlevel_small(), 0.7),
        "jng_intro_fs": (jingle_intro(), 0.75),
        "sfx_superfreespin": (superfreespin(), 0.8),
        "sfx_scatter_win_v2": (scatter_win(), 0.7),
        "sfx_youwon_panel": (youwon_panel(), 0.75),
        "sfx_winlevel_end": (winlevel_end(), 0.6),
        "sfx_bigwin_coinloop": (bigwin_loop(), 0.4),
        "sfx_wild_explode": (wild_explode(), 0.75),
        "sfx_multiplier_landing": (multiplier_landing(), 0.7),
        "sfx_multiplier_update": (multiplier_update(), 0.7),
        "sfx_anticipation": (anticipation(), 0.6),
    }
    for step in range(1, 6):
        sounds[f"sfx_scatter_stop_{step}"] = (scatter_stop(step), 0.7)
    for name, (x, peak) in sounds.items():
        write(os.path.join(out, f"{name}.wav"), x, peak)


if __name__ == "__main__":
    main(sys.argv[1], options="--options" in sys.argv)
