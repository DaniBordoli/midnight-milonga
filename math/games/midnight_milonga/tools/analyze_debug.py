"""Summarize the uncompressed debug books (run.py debug) to tune the math before optimizing.

Usage (from math/): env\\Scripts\\python.exe games\\midnight_milonga\\tools\\analyze_debug.py
"""

import json
import os
import statistics as st

LIB = os.path.join(os.path.dirname(__file__), "..", "library", "books")
COST = {"base": 1, "ante": 1.5, "bonus": 100, "super": 400}


def summarize(mode):
    books = json.load(open(os.path.join(LIB, f"books_{mode}.json"), encoding="utf-8"))
    by_crit = {}
    for b in books:
        by_crit.setdefault(b["criteria"], []).append(b)
    print(f"== {mode} (cost {COST[mode]}x)")
    for crit, items in sorted(by_crit.items()):
        pays = sorted(b["payoutMultiplier"] / 100 for b in items)
        n = len(pays)
        abrazos = [sum(e["type"] == "abrazo" for e in b["events"]) for b in items]
        rosas = [sum(e["type"] == "rosaRoja" for e in b["events"]) for b in items]
        compas = [max([e["globalMult"] for e in b["events"] if e["type"] == "updateGlobalMult"] or [1]) for b in items]
        print(
            f"  {crit:9s} n={n:4d} mean={st.mean(pays):8.2f} median={pays[n // 2]:8.2f} "
            f"p90={pays[9 * n // 10]:8.2f} max={pays[-1]:9.2f} | abrazos/ronda={st.mean(abrazos):.2f} "
            f"rosas/ronda={st.mean(rosas):.2f} compás máx={max(compas)}"
        )


if __name__ == "__main__":
    for m in COST:
        summarize(m)
