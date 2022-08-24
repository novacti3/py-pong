from enum import Enum, IntEnum
from typing import Tuple


class GameState(Enum):
    GAME_START = 0
    ROUND_START = 1
    ROUND_IN_PROGRESS = 2
    ROUND_END = 3


class PlayerIndex(IntEnum):
    PLAYER_ONE = 1
    PLAYER_TWO = 2


class GameStats:
    def __init__(self) -> None:
        self._player_one_score = 0
        self._player_two_score = 0
        self._current_game_state = GameState.GAME_START
        self._last_player_to_score: PlayerIndex = 0

    
    def get_current_game_state(self) -> GameState:
        return self._current_game_state

    def set_current_game_state(self, new_state: GameState) -> None:
        self._current_game_state = new_state

    
    def get_score(self) -> Tuple[int, int]:
        return (self._player_one_score, self._player_two_score)

    def set_score(self, new_score: Tuple[int, int], player_index: PlayerIndex):
        self._player_one_score = new_score[0]
        self._player_two_score = new_score[1]
        self._last_player_to_score = player_index

    def get_last_player_to_score(self) -> PlayerIndex:
        return self._last_player_to_score