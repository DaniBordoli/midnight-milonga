"""Events specific to Midnight Milonga. Rows include the top padding symbol (row + 1), like the SDK events."""

from src.events.events import *  # noqa: F401,F403


def abrazo_event(gamestate, bailarin: dict, bailarina: dict, row: int, wild_positions: list) -> None:
    """El Abrazo: the dancers meet on the Bailarín's row and every non-scatter position of that row becomes W."""
    gamestate.book.add_event(
        {
            "index": len(gamestate.book.events),
            "type": "abrazo",
            "row": row + 1,
            "bailarin": {"reel": bailarin["reel"], "row": bailarin["row"] + 1},
            "bailarina": {"reel": bailarina["reel"], "row": bailarina["row"] + 1},
            "wildPositions": [{"reel": p["reel"], "row": p["row"] + 1} for p in wild_positions],
        }
    )


def rosa_roja_event(gamestate, multiplier: int, win_before: float) -> None:
    """La Rosa Roja: multiplies the total win of this base-game spin."""
    gamestate.book.add_event(
        {
            "index": len(gamestate.book.events),
            "type": "rosaRoja",
            "multiplier": int(multiplier),
            "winBefore": int(round(win_before * 100)),
        }
    )
