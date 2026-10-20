from game_executables import GameExecutables


class GameStateOverride(GameExecutables):
    """Game-specific overrides of the SDK state."""

    def reset_book(self):
        super().reset_book()
        # Set during a bonus session: same conditions, but the free-spin reel weights fixed to the strip drawn
        # for that session (see fs_session_reels).
        self.session_conditions = None

    def get_current_distribution_conditions(self) -> dict:
        if self.session_conditions is not None:
            return self.session_conditions
        return super().get_current_distribution_conditions()

    def assign_special_sym_function(self):
        self.special_symbol_functions = {}

    def check_repeat(self):
        """SDK checks, plus: the 'basegame' criteria only keeps winning spins (zero wins belong to criteria '0')."""
        super().check_repeat()
        if self.repeat is False:
            win_criteria = self.get_current_betmode_distributions().get_win_criteria()
            if win_criteria is None and self.final_win == 0:
                self.repeat = True
