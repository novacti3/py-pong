import sys
import pygame

from pypong.core.game_stats import GameStats
from pypong.core.game_window import GameWindow


class GameInstance:
    def __init__(self, window_width: int, window_height: int, window_caption: str) -> None:
        pygame.init()
        self._window = GameWindow(window_width, window_height, window_caption)
        self._game_stats = GameStats()
        # self._ui = UIManager()
        # self._player_one = Paddle()
        # self._player_two = Paddle()
        # self._ball = Ball()

    def quit(self) -> None:
        pygame.quit()
        sys.exit()

    def run(self, delta_time: float) -> int:
        # TODO: Implement game loop
        event_result = self._handle_events()

        return event_result


    def get_window(self) -> GameWindow:
        return self._window

    def get_game_stats(self) -> GameStats:
        return self._game_stats


    def _init_resources(self):
        # TODO: Implement resource init
        pass

    def _handle_events(self):
        # TODO: Implement pygame event handling
        events = pygame.event.get()
        for event in events:
            match(event.type):
                case pygame.QUIT:
                    return -1
        pass

    def _handle_input(self):
        # TODO: Implement player input handling
        pass