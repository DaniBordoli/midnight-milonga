import random

from game_calculations import GameCalculations
from game_events import abrazo_event, rosa_roja_event
from src.calculations.ways import Ways
from src.calculations.statistics import get_random_outcome
from src.events.events import reveal_event

BAILARIN_REELS = (0, 1)
BAILARINA_REELS = (3, 4)


class GameExecutables(GameCalculations):
    """Midnight Milonga actions: board reveal, El Abrazo, La Rosa Roja and win evaluation."""

    def reveal_board(self, force_abrazo: bool = False) -> None:
        """Draw the board, optionally place both dancers (super bonus first spin), then emit the reveal."""
        self.draw_board(emit_event=False)
        if force_abrazo and not self.find_abrazo():
            self.place_dancers()
        reveal_event(self)

    def place_dancers(self) -> None:
        """Put the Bailarín on reel 1-2 and the Bailarina on reel 4-5, never over a scatter."""
        for name, reels in ((self.config.bailarin, BAILARIN_REELS), (self.config.bailarina, BAILARINA_REELS)):
            if any(s.name == name for r in reels for s in self.board[r]):
                continue
            options = [(r, i) for r in reels for i, s in enumerate(self.board[r]) if not s.check_attribute("scatter")]
            reel, row = random.choice(options)
            self.board[reel][row] = self.create_symbol(name)
        self.get_special_symbols_on_board()

    def find_abrazo(self):
        """Return (bailarin, bailarina) positions if both dancers are on their reels, else None."""
        bailarin = next(
            ({"reel": r, "row": i} for r in BAILARIN_REELS for i, s in enumerate(self.board[r]) if s.name == self.config.bailarin),
            None,
        )
        bailarina = next(
            ({"reel": r, "row": i} for r in BAILARINA_REELS for i, s in enumerate(self.board[r]) if s.name == self.config.bailarina),
            None,
        )
        if bailarin and bailarina:
            return bailarin, bailarina
        return None

    def apply_abrazo(self) -> bool:
        """El Abrazo: the Bailarín's row becomes wild across all reels (scatters stay). Returns True if it happened."""
        found = self.find_abrazo()
        if not found:
            return False
        bailarin, bailarina = found
        row = bailarin["row"]
        converted = []
        for reel in range(self.config.num_reels):
            if not self.board[reel][row].check_attribute("scatter"):
                self.board[reel][row] = self.create_symbol(self.config.abrazo_wild)
                converted.append({"reel": reel, "row": row})
        self.get_special_symbols_on_board()
        abrazo_event(self, bailarin, bailarina, row, converted)
        self.record({"abrazo": True, "gametype": self.gametype})
        return True

    def evaluate_spin(self, global_multiplier: int = 1, rosa_allowed: bool = False) -> None:
        """Ways wins (× Compás), optional La Rosa Roja on the total, then the standard win events."""
        self.win_data = self.get_ways_wins(global_multiplier)
        conditions = self.get_current_distribution_conditions()
        if rosa_allowed and self.win_data["totalWin"] > 0 and random.random() < conditions["rosa_prob"]:
            mult = get_random_outcome(conditions["rosa_mults"])
            rosa_roja_event(self, mult, self.win_data["totalWin"])
            for win in self.win_data["wins"]:
                win["win"] = round(win["win"] * mult, 2)
                win["meta"]["rosaMult"] = mult
            self.win_data["totalWin"] = round(self.win_data["totalWin"] * mult, 2)
            self.record({"rosa": mult, "gametype": self.gametype})

        if self.win_data["totalWin"] > 0:
            Ways.record_ways_wins(self)
            self.win_manager.update_spinwin(self.win_data["totalWin"])
        Ways.emit_wayswin_events(self)
