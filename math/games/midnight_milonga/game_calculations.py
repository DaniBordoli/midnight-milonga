"""Ways evaluation for Midnight Milonga.

The SDK's Ways.get_ways_data only starts ways from symbols on reel 1, so a wild on reel 1 never
substitutes. El Abrazo turns a full row (reel 1 included) into wilds, so this game needs wilds to
substitute everywhere:
- every paying symbol pays prod(symbol + wild count per reel) minus the all-wild paths,
- all-wild paths pay once, as symbol "W".
"""

from src.executables.executables import Executables


class GameCalculations(Executables):

    def get_ways_wins(self, global_multiplier: int = 1) -> dict:
        board = self.board
        wild_names = set(self.config.special_symbols["wild"])
        paying = sorted({sym for (_, sym) in self.config.paytable})

        wild_pos = [[{"reel": r, "row": i} for i, s in enumerate(board[r]) if s.name in wild_names] for r in range(len(board))]
        result = {"totalWin": 0, "wins": []}

        for sym in paying:
            if sym == self.config.abrazo_wild:
                sym_pos = [[] for _ in board]  # all-wild paths
            else:
                sym_pos = [[{"reel": r, "row": i} for i, s in enumerate(board[r]) if s.name == sym] for r in range(len(board))]

            kind, all_ways, wild_ways = 0, 1, 1
            for r in range(len(board)):
                count = len(sym_pos[r]) + len(wild_pos[r])
                if count == 0:
                    break
                kind += 1
                all_ways *= count
                wild_ways *= len(wild_pos[r])

            ways = wild_ways if sym == self.config.abrazo_wild else all_ways - wild_ways
            if ways <= 0 or (kind, sym) not in self.config.paytable:
                continue

            base_win = round(self.config.paytable[(kind, sym)] * ways, 2)
            win = round(base_win * global_multiplier, 2)
            positions = [p for r in range(kind) for p in sym_pos[r] + wild_pos[r]]
            result["wins"].append(
                {
                    "symbol": sym,
                    "kind": kind,
                    "win": win,
                    "positions": positions,
                    "meta": {"ways": ways, "globalMult": global_multiplier, "winWithoutMult": base_win},
                }
            )
            result["totalWin"] = round(result["totalWin"] + win, 2)

        return result
