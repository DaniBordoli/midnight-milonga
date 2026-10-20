"""Export the Midnight Milonga math into the web app.

Usage (from the repo root):
    math\\env\\Scripts\\python.exe tools\\export_front_data.py

Writes:
    web/apps/midnight-milonga/src/game/config.ts          FE config (symbols keyed by name, as the app expects)
    web/apps/midnight-milonga/src/stories/data/<mode>_books.ts   sample of real rounds per mode, for Storybook
"""

import io
import json
import os
import random

import zstandard

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIB = os.path.join(ROOT, "math", "games", "midnight_milonga", "library")
APP = os.path.join(ROOT, "web", "apps", "midnight-milonga", "src")

# how many rounds of each kind go into the Storybook sample
SAMPLE = {
    "base": {"zero": 40, "win": 120, "abrazo": 40, "rosa": 40, "freegame": 15, "wincap": 1},
    "bonus": {"freegame": 40, "big": 10, "wincap": 1},
    "super": {"freegame": 40, "big": 10, "wincap": 1},
}


def write_ts(path, data):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("export default ")
        json.dump(data, f, indent="\t", ensure_ascii=False)
        f.write(";\n")


def kind_of(book):
    types = {e["type"] for e in book["events"]}
    if book["criteria"] == "wincap":
        return "wincap"
    if book["criteria"] == "freegame":
        return "big" if book["payoutMultiplier"] >= 100_000 else "freegame"  # >= 1.000x
    if book["payoutMultiplier"] == 0:
        return "zero"
    if "abrazo" in types:
        return "abrazo"
    if "rosaRoja" in types:
        return "rosa"
    return "win"


def read_books(mode):
    with open(os.path.join(LIB, "publish_files", f"books_{mode}.jsonl.zst"), "rb") as f:
        reader = io.TextIOWrapper(zstandard.ZstdDecompressor().stream_reader(f), encoding="utf-8")
        for line in reader:
            yield json.loads(line)


def main():
    fe = json.load(open(os.path.join(LIB, "configs", "config_fe_midnight_milonga.json"), encoding="utf-8"))
    symbols = {}
    for entry in fe["symbols"]:
        symbols.update(entry)
    fe["symbols"] = symbols
    write_ts(os.path.join(APP, "game", "config.ts"), fe)

    rng = random.Random(1920)
    os.makedirs(os.path.join(APP, "stories", "data"), exist_ok=True)
    for mode, wanted in SAMPLE.items():
        pools = {k: [] for k in wanted}
        for book in read_books(mode):
            k = kind_of(book)
            if k in pools and len(pools[k]) < 2000:
                pools[k].append(book)
        sample = []
        for k, n in wanted.items():
            sample += rng.sample(pools[k], min(n, len(pools[k])))
        sample.sort(key=lambda b: b["id"])
        write_ts(os.path.join(APP, "stories", "data", f"{mode}_books.ts"), sample)
        print(mode, {k: min(n, len(pools[k])) for k, n in wanted.items()})


if __name__ == "__main__":
    main()
