"""Midnight Milonga: 5x4, 1024 ways, El Abrazo, La Rosa Roja, free spins with Compás multiplier."""

import os
from src.config.config import Config
from src.config.distributions import Distribution
from src.config.betmode import BetMode


class GameConfig(Config):
    """Game specific configuration class."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__()
        self.game_id = "midnight_milonga"
        self.provider_number = 0
        self.working_name = "Midnight Milonga"
        self.wincap = 15000
        self.win_type = "ways"
        self.rtp = 0.963
        self.construct_paths()

        # Game Dimensions
        self.num_reels = 5
        self.num_rows = [4] * self.num_reels

        # Pays in multiples of the total bet, per way. W pays the all-wild ways (e.g. a full Abrazo row).
        # H1 bandoneón, H2 rosa, H3 fedora, H4 champagne, L1-L4 pica/corazón/diamante/trébol.
        self.paytable = {
            # every value is a multiple of 0.1x: the RGS format check requires payouts in steps of 0.1x
            (5, "W"): 2.5, (4, "W"): 0.8, (3, "W"): 0.3,
            (5, "H1"): 2.5, (4, "H1"): 0.8, (3, "H1"): 0.3,
            (5, "H2"): 2, (4, "H2"): 0.6, (3, "H2"): 0.2,
            (5, "H3"): 1.5, (4, "H3"): 0.5, (3, "H3"): 0.2,
            (5, "H4"): 1, (4, "H4"): 0.4, (3, "H4"): 0.1,
            (5, "L1"): 0.6, (4, "L1"): 0.3, (3, "L1"): 0.1,
            (5, "L2"): 0.6, (4, "L2"): 0.3, (3, "L2"): 0.1,
            (5, "L3"): 0.5, (4, "L3"): 0.2, (3, "L3"): 0.1,
            (5, "L4"): 0.5, (4, "L4"): 0.2, (3, "L4"): 0.1,
        }

        self.include_padding = True
        # BM = Bailarín (reels 1-2), BF = Bailarina (reels 4-5), W = wild created by El Abrazo
        self.special_symbols = {"wild": ["W", "BM", "BF"], "scatter": ["S"], "multiplier": []}
        self.bailarin, self.bailarina, self.abrazo_wild = "BM", "BF", "W"

        self.freespin_triggers = {
            self.basegame_type: {3: 10, 4: 12, 5: 15},
            self.freegame_type: {3: 5, 4: 5, 5: 5},
        }
        self.anticipation_triggers = {self.basegame_type: 2, self.freegame_type: 2}

        # Reels
        reels = {"BR0": "BR0.csv", "FR0": "FR0.csv", "FR1": "FR1.csv", "FRWCAP": "FRWCAP.csv"}
        self.reels = {}
        for r, f in reels.items():
            self.reels[r] = self.read_reels_csv(os.path.join(self.reels_path, f))
        self.padding_reels[self.basegame_type] = self.reels["BR0"]
        self.padding_reels[self.freegame_type] = self.reels["FR0"]

        # La Rosa Roja (base game only): chance to land on a winning spin and its total-win multiplier
        rosa = {"rosa_prob": 0.12, "rosa_mults": {2: 50, 3: 30, 5: 15, 10: 5}}
        # Compás starting value in free spins; the super bonus starts higher and forces an Abrazo on spin 1.
        # fs_session_reels: one free-spin strip is drawn per bonus session (FR1 = "hot night", more dancers).
        session_reels = {"FR0": 10, "FR1": 1}
        normal_fs = {"compas_start": 1, "forced_first_abrazo": False, "fs_session_reels": session_reels}
        super_fs = {"compas_start": 5, "forced_first_abrazo": True, "fs_session_reels": session_reels}

        base_reels = {self.basegame_type: {"BR0": 1}, self.freegame_type: {"FR0": 1}}
        wincap_reels = {self.basegame_type: {"BR0": 1}, self.freegame_type: {"FR0": 1, "FRWCAP": 5}}
        scatters = {3: 100, 4: 20, 5: 5}
        maxwin = self.wincap

        def base_like(name, cost, fs_quota):
            return BetMode(
                name=name,
                cost=cost,
                rtp=self.rtp,
                max_win=maxwin,
                auto_close_disabled=False,
                is_feature=True,
                is_buybonus=False,
                distributions=[
                    Distribution(
                        criteria="wincap",
                        quota=0.0005,
                        win_criteria=maxwin,
                        conditions={
                            "reel_weights": wincap_reels,
                            "force_freegame": True,
                            "scatter_triggers": {4: 1, 5: 2},
                            **rosa,
                            **normal_fs,
                        },
                    ),
                    Distribution(
                        criteria="freegame",
                        quota=fs_quota,
                        conditions={
                            "reel_weights": base_reels,
                            "force_freegame": True,
                            "scatter_triggers": scatters,
                            **rosa,
                            **normal_fs,
                        },
                    ),
                    Distribution(
                        criteria="0",
                        quota=0.4,
                        win_criteria=0.0,
                        conditions={"reel_weights": base_reels, "force_freegame": False, **rosa, **normal_fs},
                    ),
                    Distribution(
                        criteria="basegame",
                        quota=0.5,
                        conditions={"reel_weights": base_reels, "force_freegame": False, **rosa, **normal_fs},
                    ),
                ],
            )

        def bought(name, cost, fs_conditions):
            return BetMode(
                name=name,
                cost=cost,
                rtp=self.rtp,
                max_win=maxwin,
                auto_close_disabled=False,
                is_feature=False,
                is_buybonus=True,
                distributions=[
                    Distribution(
                        criteria="wincap",
                        quota=0.0005,
                        win_criteria=maxwin,
                        conditions={
                            "reel_weights": wincap_reels,
                            "force_freegame": True,
                            "scatter_triggers": {4: 1, 5: 2},
                            **rosa,
                            **fs_conditions,
                        },
                    ),
                    Distribution(
                        criteria="freegame",
                        quota=0.9995,
                        conditions={
                            "reel_weights": base_reels,
                            "force_freegame": True,
                            "scatter_triggers": scatters,
                            **rosa,
                            **fs_conditions,
                        },
                    ),
                ],
            )

        # Mode names avoid "bet"/"buy"/"pay" (stake.us social-mode rule).
        self.bet_modes = [
            base_like("base", 1.0, 0.1),  # juego base
            base_like("ante", 1.5, 0.2),  # Noche de Gala
            bought("bonus", 100.0, normal_fs),  # La Pista
            bought("super", 400.0, super_fs),  # La Última Tanda
        ]
