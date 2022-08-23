from enum import Enum
from typing import Tuple


class GameState(Enum):
    ROUND_START = 0
    ROUND_IN_PROGRESS = 1
    ROUND_END = 2


class GameStats:
    def __init__(self) -> None:
        self._player_one_score = 0
        self._player_two_score = 0
        self._current_game_state = GameState.ROUND_START

    
    def get_current_game_state(self) -> GameState:
        return self._current_game_state

    def set_current_game_state(self, new_state: GameState) -> None:
        self._current_game_state = new_state

    
    def get_score(self) -> Tuple[int, int]:
        return (self._player_one_score, self._player_two_score)

    def set_score(self, new_player_one_score: int, new_player_two_score: int):
        self._player_one_score = new_player_one_score
        self._player_two_score = new_player_two_score