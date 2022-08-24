from enum import Enum, IntEnum


"""Enum of the possible states that the game can be in"""
class GameState(Enum):
    GAME_START = 0
    ROUND_START = 1
    ROUND_IN_PROGRESS = 2
    ROUND_END = 3


"""IntEnum containing the int index of each player
Ensures consistent indexes throughout the codebase.
"""
class PlayerIndex(IntEnum):
    PLAYER_ONE = 1
    PLAYER_TWO = 2


"""Struct containing the current statistics of the game
Keeps track of the current game state, score etc.
"""
class GameStats:
    def __init__(self) -> None:
        self.score = (0, 0)
        self.current_game_state = GameState.GAME_START
        self.player_who_last_scored: PlayerIndex = 0