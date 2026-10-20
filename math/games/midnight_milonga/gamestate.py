"""Midnight Milonga game flow."""

from game_override import GameStateOverride
from src.calculations.statistics import get_random_outcome
from src.events.events import update_global_mult_event


class GameState(GameStateOverride):
    """Base game and free spins (La Pista / La Última Tanda)."""

    def run_spin(self, sim: int, simulation_seed=None) -> None:
        self.reset_seed(sim)
        self.repeat = True
        while self.repeat:
            self.reset_book()
            self.reveal_board()
            self.apply_abrazo()
            self.evaluate_spin(global_multiplier=1, rosa_allowed=True)
            self.win_manager.update_gametype_wins(self.gametype)

            if self.check_fs_condition() and self.check_freespin_entry():
                self.run_freespin_from_base()

            self.evaluate_finalwin()
            self.check_repeat()

        self.imprint_wins()

    def run_freespin(self) -> None:
        self.reset_fs_spin()
        conditions = self.get_current_distribution_conditions()
        if self.criteria != "wincap":  # the max-win distribution keeps its own per-spin reel weights
            strip = get_random_outcome(conditions["fs_session_reels"])
            reel_weights = {**conditions["reel_weights"], self.config.freegame_type: {strip: 1}}
            self.session_conditions = {**conditions, "reel_weights": reel_weights}
        self.global_multiplier = conditions["compas_start"]
        update_global_mult_event(self)  # starting Compás value

        while self.fs < self.tot_fs and not self.wincap_triggered:
            self.update_freespin()
            self.reveal_board(force_abrazo=conditions["forced_first_abrazo"] and self.fs == 1)
            if self.apply_abrazo():
                self.update_global_mult()  # Compás +1, applies to this spin's wins
            self.evaluate_spin(global_multiplier=self.global_multiplier)

            if self.check_fs_condition():
                self.update_fs_retrigger_amt()

            self.win_manager.update_gametype_wins(self.gametype)
        self.end_freespin()
        self.session_conditions = None
