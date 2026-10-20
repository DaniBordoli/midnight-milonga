"""How many debug outcomes land in the big-win range (before optimization).

Usage (from math/): env\\Scripts\\python.exe games\\midnight_milonga\\tools\\tail_check.py <mode> [<mode> ...]
Needs uncompressed books from: run.py debug sims=N <mode>
"""

import json
import os
import sys

LIB = os.path.join(os.path.dirname(__file__), "..", "library", "books")
EDGES = [0, 100, 500, 1000, 2500, 5000, 10000, 15000]

for mode in sys.argv[1:]:
    books = json.load(open(os.path.join(LIB, f"books_{mode}.json"), encoding="utf-8"))
    pays = [b["payoutMultiplier"] / 100 for b in books if b["criteria"] != "wincap"]
    fs = [b["payoutMultiplier"] / 100 for b in books if b["criteria"] == "freegame"]
    counts = [sum(EDGES[i] <= p < EDGES[i + 1] for p in fs) for i in range(len(EDGES) - 1)]
    print(f"{mode}: rondas con free spins={len(fs)} promedio={sum(fs) / max(len(fs), 1):.1f}x máx={max(pays):,.1f}x")
    print("   " + "  ".join(f"[{EDGES[i]}-{EDGES[i + 1]}): {c}" for i, c in enumerate(counts)))
