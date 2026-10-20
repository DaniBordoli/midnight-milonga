"""Generate the reel strips for Midnight Milonga.

Usage (from this folder): python generate_reels.py

Rules enforced on every strip:
- BM (Bailarín) only on reels 1-2, BF (Bailarina) only on reels 4-5, W never on strips
  (W only appears when El Abrazo converts a row).
- Scatters and dancers are spaced at least ROWS apart, so a visible window of 4 rows
  never shows two of the same special symbol on one reel.
"""

import os
import random

ROWS = 4
LENGTH = 60
HERE = os.path.dirname(os.path.abspath(__file__))

LOWS = ["L1", "L2", "L3", "L4"]
SPACED = {"S", "BM", "BF"}

# symbol -> count per reel (index 0..4). Remaining stops are filled with lows.
STRIPS = {
    "BR0": {
        "H1": [3, 3, 3, 3, 3],
        "H2": [4, 4, 4, 4, 4],
        "H3": [5, 5, 5, 5, 5],
        "H4": [6, 6, 6, 6, 6],
        "S": [2, 2, 2, 2, 2],
        "BM": [1, 1, 0, 0, 0],
        "BF": [0, 0, 0, 1, 1],
    },
    "FR0": {
        "H1": [3, 3, 3, 3, 3],
        "H2": [4, 4, 4, 4, 4],
        "H3": [5, 5, 5, 5, 5],
        "H4": [6, 6, 6, 6, 6],
        "S": [2, 2, 2, 2, 2],
        "BM": [2, 2, 0, 0, 0],
        "BF": [0, 0, 0, 2, 2],
    },
    # "hot" free-spin strip, drawn for a minority of whole bonus sessions (see fs_session_reels in game_config)
    "FR1": {
        "H1": [5, 5, 5, 5, 5],
        "H2": [5, 5, 5, 5, 5],
        "H3": [5, 5, 5, 5, 5],
        "H4": [5, 5, 5, 5, 5],
        "S": [2, 2, 2, 2, 2],
        "BM": [7, 7, 0, 0, 0],
        "BF": [0, 0, 0, 7, 7],
    },
    # wild-heavy strip used only by the max-win distribution
    "FRWCAP": {
        "H1": [14, 14, 14, 14, 14],
        "H2": [10, 10, 10, 10, 10],
        "H3": [8, 8, 8, 8, 8],
        "H4": [8, 8, 8, 8, 8],
        "S": [0, 0, 0, 0, 0],
        "BM": [8, 8, 0, 0, 0],
        "BF": [0, 0, 0, 8, 8],
    },
}


def spaced_ok(strip):
    """No two symbols from the same SPACED family within ROWS positions (wrapping)."""
    n = len(strip)
    for i, sym in enumerate(strip):
        if sym in SPACED:
            for d in range(1, ROWS):
                if strip[(i + d) % n] == sym:
                    return False
    return True


def build_reel(counts, reel, rng):
    stops = []
    for sym, per_reel in counts.items():
        stops += [sym] * per_reel[reel]
    assert len(stops) <= LENGTH, f"too many symbols on reel {reel}"
    i = 0
    while len(stops) < LENGTH:
        stops.append(LOWS[i % len(LOWS)])
        i += 1
    for _ in range(10_000):
        rng.shuffle(stops)
        if spaced_ok(stops):
            return stops
    raise RuntimeError(f"could not space specials on reel {reel}")


def main():
    rng = random.Random(1920)
    for name, counts in STRIPS.items():
        reels = [build_reel(counts, r, rng) for r in range(5)]
        with open(os.path.join(HERE, f"{name}.csv"), "w", encoding="UTF-8", newline="\n") as f:
            for row in zip(*reels):
                f.write(",".join(row) + "\n")
        print(name, "ok")


if __name__ == "__main__":
    main()
