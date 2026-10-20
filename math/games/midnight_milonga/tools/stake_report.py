"""Check the published math against Stake Engine's math verification rules.

Usage (from math/): env\\Scripts\\python.exe games\\midnight_milonga\\tools\\stake_report.py
Reads library/publish_files (index.json + lookup tables) and writes library/stake_report.md.

Definitions follow stake-engine.com/docs/approval-guidelines/math-verification:
- payouts are multipliers of the base bet; RTP = E[payout] / cost
- tail probabilities P(>= Nx) are raw (not scaled by cost)
- CVaR = mean payout of the worst 0.1% outcomes; per-stake = CVaR / cost
- ETL > 40x = RTP share from wins above 40 x cost, divided by cost; ETL > 10,000x likewise; "absolute" = before dividing
- std is reported raw and per unit of cost; the per-cost value is compared with the limits (the docs do not say which
  one applies to bought modes, so both are shown)
"""

import csv
import json
import math
import os

LIB = os.path.join(os.path.dirname(__file__), "..", "library")
PUB = os.path.join(LIB, "publish_files")

LIMITS = {  # (2-star, 3-star)
    "max_payout": (50_000, 100_000),
    "max_cost": (1_000, 5_000),
    "std": (50.0, 60.0),
    "cvar_per_stake": (700, 700),
    "cvar_abs": (20_000, 50_000),
    "p5k": (0.010, 0.050),
    "p10k": (0.005, 0.010),
    "p25k": (0.002, 0.005),
    "p50k": (0.001, 0.001),
    "p100k": (0.0005, 0.0005),
    "etl40": (0.8, 0.9),
    "etl10k": (0.6, 0.8),
    "etl_sum": (1.3, 1.5),
    "etl_abs_sum": (3_000, 10_000),
}
CLASSES = {
    "Maximum Payout Multiplier": ["max_payout"],
    "Cost Multiplier": ["max_cost"],
    "Volatility (Std Dev)": ["std"],
    "Risk Limit (CVaR)": ["cvar_per_stake", "cvar_abs"],
    "Expected Tail Liability": ["etl40", "etl10k", "etl_sum", "etl_abs_sum"],
    "Tail Probability": ["p5k", "p10k", "p25k", "p50k", "p100k"],
}


def load_mode(mode):
    rows = []
    with open(os.path.join(PUB, mode["weights"]), encoding="utf-8") as f:
        for _, w, p in csv.reader(f):
            rows.append((int(w), int(p) / 100))
    total = sum(w for w, _ in rows)
    return [(w / total, p) for w, p in rows]


def stats(dist, cost):
    mean = sum(p * x for p, x in dist)
    var = sum(p * (x - mean) ** 2 for p, x in dist)
    std = math.sqrt(var)
    maxwin = max(x for _, x in dist)
    p_max = sum(p for p, x in dist if x == maxwin)
    p_hit = sum(p for p, x in dist if x > 0)

    # CVaR: mean of the upper 0.1% tail
    tail, need, acc = 0.0, 0.001, 0.0
    for p, x in sorted(dist, key=lambda t: -t[1]):
        take = min(p, need - acc)
        tail += take * x
        acc += take
        if acc >= need:
            break
    cvar = tail / need

    etl40_abs = sum(p * x for p, x in dist if x > 40 * cost)
    etl10k_abs = sum(p * x for p, x in dist if x > 10_000)
    tail_p = {k: sum(p for p, x in dist if x >= v) for k, v in
              [("p5k", 5_000), ("p10k", 10_000), ("p25k", 25_000), ("p50k", 50_000), ("p100k", 100_000)]}
    return {
        "rtp": mean / cost,
        "std_raw": std,
        "std": std / cost,
        "hit_rate": 1 / p_hit if p_hit else float("inf"),
        "zero_share": 1 - p_hit,
        "max_payout": maxwin,
        "maxwin_freq": 1 / p_max,
        "cvar_abs": cvar,
        "cvar_per_stake": cvar / cost,
        "etl40": etl40_abs / cost,
        "etl10k": etl10k_abs / cost,
        "etl_sum": (etl40_abs + etl10k_abs) / cost,
        "etl_abs_sum": etl40_abs + etl10k_abs,
        **tail_p,
    }


def failed_classes(s, cost, tier):
    values = dict(s, max_cost=cost)
    return [name for name, keys in CLASSES.items() if any(values[k] > LIMITS[k][tier] for k in keys)]


def main():
    index = json.load(open(os.path.join(PUB, "index.json"), encoding="utf-8"))
    modes = index["modes"]
    results = {m["name"]: (m["cost"], stats(load_mode(m), m["cost"])) for m in modes}
    out = ["# Midnight Milonga · chequeos de Stake\n"]

    out.append("## Chequeos críticos (bloquean el envío)\n")
    cheapest = min(c for c, _ in results.values())
    crit = [
        ("Modo más barato cuesta 1.0x", cheapest == 1.0, f"{cheapest}x"),
        ("Desvío de los modos 1.0x ≥ 0.6",
         all(s["std"] >= 0.6 for c, s in results.values() if c == 1.0),
         ", ".join(f"{n}: {s['std']:.2f}" for n, (c, s) in results.items() if c == 1.0)),
        ("RTP de cada modo entre 96.0% y 96.7%",
         all(0.96 <= s["rtp"] <= 0.967 for _, s in results.values()),
         ", ".join(f"{n}: {s['rtp'] * 100:.3f}%" for n, (_, s) in results.items())),
        ("Ganancia máxima ≤ 1.000.000x", all(s["max_payout"] <= 1_000_000 for _, s in results.values()),
         ", ".join(f"{n}: {s['max_payout']:,.0f}x" for n, (_, s) in results.items())),
        ("Costo de modo ≤ 50.000x", all(c <= 50_000 for c, _ in results.values()),
         ", ".join(f"{n}: {c:g}x" for n, (c, _) in results.items())),
    ]
    out.append("| Chequeo | Resultado | Valores |\n|---|---|---|")
    for name, ok, val in crit:
        out.append(f"| {name} | {'✅' if ok else '❌'} | {val} |")

    out.append("\n## Por modo\n")
    out.append("| Métrica | " + " | ".join(results) + " |")
    out.append("|---|" + "---|" * len(results))
    rows = [
        ("Costo", lambda c, s: f"{c:g}x"),
        ("RTP", lambda c, s: f"{s['rtp'] * 100:.3f}%"),
        ("Frecuencia de premio", lambda c, s: f"1 cada {s['hit_rate']:.2f}"),
        ("Rondas sin premio", lambda c, s: f"{s['zero_share'] * 100:.1f}%"),
        ("Desvío (÷ costo / crudo)", lambda c, s: f"{s['std']:.2f} / {s['std_raw']:.1f}"),
        ("Ganancia máxima", lambda c, s: f"{s['max_payout']:,.0f}x"),
        ("Frecuencia de la ganancia máxima", lambda c, s: f"1 cada {s['maxwin_freq']:,.0f}"),
        ("P(≥ 5.000x)", lambda c, s: f"{s['p5k']:.6f}"),
        ("P(≥ 10.000x)", lambda c, s: f"{s['p10k']:.6f}"),
        ("CVaR por apuesta / absoluto", lambda c, s: f"{s['cvar_per_stake']:.1f} / {s['cvar_abs']:,.0f}"),
        ("ETL > 40x", lambda c, s: f"{s['etl40']:.3f}"),
        ("ETL > 10.000x", lambda c, s: f"{s['etl10k']:.3f}"),
        ("ETL suma / absoluta", lambda c, s: f"{s['etl_sum']:.3f} / {s['etl_abs_sum']:.1f}"),
        ("Clases que fallan 2★", lambda c, s: ", ".join(failed_classes(s, c, 0)) or "ninguna ✅"),
        ("Clases que fallan 3★", lambda c, s: ", ".join(failed_classes(s, c, 1)) or "ninguna ✅"),
    ]
    for label, fn in rows:
        out.append(f"| {label} | " + " | ".join(fn(c, s) for c, s in results.values()) + " |")

    rtps = [s["rtp"] for _, s in results.values()]
    out.append(f"\nDiferencia máxima de RTP entre modos: {(max(rtps) - min(rtps)) * 100:.3f} puntos (Stake avisa si supera 5).")
    report = "\n".join(out) + "\n"
    with open(os.path.join(LIB, "stake_report.md"), "w", encoding="utf-8") as f:
        f.write(report)
    print(report)


if __name__ == "__main__":
    main()
