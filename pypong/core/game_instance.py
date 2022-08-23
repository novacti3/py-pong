import sys
import pygame

from pypong.core.game_stats import GameState, GameStats
from pypong.core.game_window import GameWindow
from pypong.core.ui import UIManager, Text


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
                title_card: Text = self._ui.draw_text("Py-Pong!", "title", COLOR_WHITE)
                title_card_pos = (
                    self._window.get_width() / 2 - title_card.size[0] / 2, 
                    self._window.get_height()/ 2 - title_card.size[1] / 2 - title_card.line_size
                )

                space_prompt: Text = self._ui.draw_text("Press SPACE to start", "prompt", COLOR_LIGHT_GREY)
                space_prompt_pos = (
                    self._window.get_width()/2 - space_prompt.size[0] / 2,
                    ((self._window.get_height()/2 - space_prompt.size[1] / 2))
                )
                
                escape_prompt: Text = self._ui.draw_text("Press ESC to quit the game", "prompt", COLOR_LIGHT_GREY)
                escape_prompt_pos = (
                    self._window.get_width()/2 - escape_prompt.size[0] / 2,
                    (self._window.get_height()/2 - escape_prompt.size[1] / 2) + space_prompt.line_size
                )

                window_surface = self._window.get_surface()
                window_surface.blit(title_card.surface, title_card_pos)
                window_surface.blit(space_prompt.surface, space_prompt_pos)
                window_surface.blit(escape_prompt.surface, escape_prompt_pos)

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