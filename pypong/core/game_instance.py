import sys
import pygame

from pypong.core.game_stats import GameState
from pypong.core.game_stats import GameStats
from pypong.core.game_window import GameWindow
from pypong.core.ui import UIManager


COLOR_WHITE = (255, 255, 255)
COLOR_LIGHT_GREY = (150, 150, 150)
COLOR_DARK_GREY = (77, 77, 77)


TITLE_TEXT_SIZE = 72
SCORE_TEXT_SIZE = 48
PROMPT_TEXT_SIZE = 28


class GameInstance:
    def __init__(self, window_width: int, window_height: int, window_caption: str) -> None:
        pygame.init()
        self._window = GameWindow(window_width, window_height, window_caption)
        self._game_stats = GameStats()
        self._ui = UIManager([
            ("title", "./ka1.ttf", TITLE_TEXT_SIZE),
            ("prompt", "./ka1.ttf", PROMPT_TEXT_SIZE), 
            ("score", "./ka1.ttf", SCORE_TEXT_SIZE)
        ])
        # self._player_one = Paddle()
        # self._player_two = Paddle()
        # self._ball = Ball()

    def quit(self) -> None:
        pygame.quit()
        sys.exit()

    def run(self, delta_time: float) -> int:
        # TODO: Implement game loop
        event_result = self._handle_events()

        match(self._game_stats.get_current_game_state()):
            case GameState.ROUND_START:
                title_linesize = self._ui.get_font_line_size("title")
                title_card = self._ui.draw_prompt("Py-Pong!", "title", COLOR_WHITE)
                
                prompt_linesize = self._ui.get_font_line_size("prompt")
                space_prompt = self._ui.draw_prompt("Press SPACE to start", "prompt", COLOR_LIGHT_GREY)
                escape_prompt = self._ui.draw_prompt("Press ESC to quit the game", "prompt", COLOR_LIGHT_GREY)

                window_surface = self._window.get_surface()
                window_surface.blit(title_card[0], (self._window.get_width()/2 - title_card[1][0]/2, self._window.get_height()/2 - title_card[1][1]/2 - title_linesize))
                window_surface.blit(space_prompt[0], (self._window.get_width()/2 - space_prompt[1][0]/2, ((self._window.get_height()/2 - space_prompt[1][1]/2))))
                window_surface.blit(escape_prompt[0], (self._window.get_width()/2 - escape_prompt[1][0]/2, (self._window.get_height()/2 - escape_prompt[1][1]/2) + prompt_linesize))

            case GameState.ROUND_IN_PROGRESS:
                pass

            case GameState.ROUND_END:
                pass

        pygame.display.update()
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
                case pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return -1
        pass

    def _handle_input(self):
        # TODO: Implement player input handling
        pass