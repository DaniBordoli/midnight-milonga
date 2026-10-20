"""Optimization targets per mode. Each mode's criteria RTPs must add up to 0.963 (relative to the mode cost)."""

from optimization_program.optimization_config import (
    ConstructScaling,
    ConstructParameters,
    ConstructConditions,
    ConstructFenceBias,
    verify_optimization_input,
)

WINCAP_RTP = 0.002  # 15.000x max win: about 1 in 7.5M base spins, inside Stake's "more often than 1 in 10M"


def base_like(wincap, fs_rtp, fs_hr, base_rtp):
    return {
        "conditions": {
            "wincap": ConstructConditions(rtp=WINCAP_RTP, av_win=wincap, search_conditions=wincap).return_dict(),
            "0": ConstructConditions(rtp=0, av_win=0, search_conditions=0).return_dict(),
            "freegame": ConstructConditions(rtp=fs_rtp, hr=fs_hr, search_conditions={"symbol": "scatter"}).return_dict(),
            "basegame": ConstructConditions(hr=3.5, rtp=base_rtp).return_dict(),
        },
        "scaling": ConstructScaling(
            [
                {"criteria": "basegame", "scale_factor": 1.2, "win_range": (1, 2), "probability": 1.0},
                {"criteria": "basegame", "scale_factor": 1.5, "win_range": (10, 20), "probability": 1.0},
                {"criteria": "freegame", "scale_factor": 0.8, "win_range": (1000, 2000), "probability": 1.0},
            ]
        ).return_dict(),
        "parameters": ConstructParameters(
            num_show=5000,
            num_per_fence=10000,
            min_m2m=4,
            max_m2m=8,
            pmb_rtp=1.0,
            sim_trials=5000,
            test_spins=[50, 100, 200],
            test_weights=[0.3, 0.4, 0.3],
            score_type="rtp",
        ).return_dict(),
        "distribution_bias": ConstructFenceBias(
            applied_criteria=["basegame"], bias_ranges=[(1.5, 3.5)], bias_weights=[0.4]
        ).return_dict(),
    }


def bought(wincap, wincap_rtp):
    return {
        "conditions": {
            "wincap": ConstructConditions(rtp=wincap_rtp, av_win=wincap, search_conditions=wincap).return_dict(),
            "freegame": ConstructConditions(rtp=0.963 - wincap_rtp, hr="x").return_dict(),
        },
        "scaling": ConstructScaling(
            [
                {"criteria": "freegame", "scale_factor": 0.9, "win_range": (20, 50), "probability": 1.0},
                {"criteria": "freegame", "scale_factor": 0.8, "win_range": (1000, 2000), "probability": 1.0},
            ]
        ).return_dict(),
        "parameters": ConstructParameters(
            num_show=5000,
            num_per_fence=10000,
            min_m2m=4,
            max_m2m=8,
            pmb_rtp=1.0,
            sim_trials=5000,
            test_spins=[10, 20, 50],
            test_weights=[0.6, 0.2, 0.2],
            score_type="rtp",
        ).return_dict(),
    }


class OptimizationSetup:
    """Amends game_config.opt_params for the Rust optimizer."""

    def __init__(self, game_config):
        self.game_config = game_config
        wincaps = {bm.get_name(): bm.get_wincap() for bm in game_config.bet_modes}
        self.game_config.opt_params = {
            # base: free spins 1 in 200, ~35% of RTP
            "base": base_like(wincaps["base"], fs_rtp=0.35, fs_hr=200, base_rtp=0.963 - WINCAP_RTP - 0.35),
            # ante (1.5x): free spins twice as often (1 in 100). fs_rtp kept low enough that wins above 40x the cost
            # stay under 0.8 of the stake both per unit of cost (Stake docs) and unscaled (SDK etl40b check).
            "ante": base_like(wincaps["ante"], fs_rtp=0.45, fs_hr=100, base_rtp=0.963 - WINCAP_RTP - 0.45),
            # bought modes: the forced max-win share is kept small so that wins >= 10,000x stay well under 0.6 of the
            # bet even unscaled by cost (SDK etl10k check): 0.002 x 100 = 0.2 and 0.0005 x 400 = 0.2
            "bonus": bought(wincaps["bonus"], wincap_rtp=WINCAP_RTP),
            "super": bought(wincaps["super"], wincap_rtp=0.0005),
        }
        verify_optimization_input(self.game_config, self.game_config.opt_params)
