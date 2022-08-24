import sys
import pygame

from pypong.core.game_stats      import GameState, GameStats
from pypong.core.game_window     import GameWindow
from pypong.core.ui              import Text, UIManager 
from pypong.gameplay.game_object import GameObject


COLOR_TITLE_CARD  = (255, 255, 255)
COLOR_PROMPT      = (150, 150, 150)
COLOR_GAME_OBJECT = (150, 150, 150)
COLOR_SCORE       = (77, 77, 77)
COLOR_BACKGROUND  = (0, 0, 0)


TITLE_TEXT_FONT_SIZE  = 72
SCORE_TEXT_FONT_SIZE  = 48
PROMPT_TEXT_FONT_SIZE = 28


PADDLE_SIZE     = (20, 125)
BALL_SIZE       = (25, 25)
PADDLE_X_OFFSET = 25


class GameInstance:
    def start(self, window_width: int, window_height: int, window_caption: str) -> None:
        # Init pygame
        pygame.init()
        
        # Create and init window
        self._window = GameWindow(window_width, window_height, window_caption)
        
        # Init game stats
        self._game_stats = GameStats()
        
        # Init resources
        self._init_resources()


    def quit(self) -> None:
        pygame.quit()
        sys.exit()


    def run(self, delta_time: float) -> int:
        # TODO: Implement game loop
        event_result = self._handle_events()

        match(self._game_stats.get_current_game_state()):
            case GameState.GAME_START:
                self._render_start_screen()
            
            case GameState.ROUND_START:
                self._render_game_screen()
                pass

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
        self._ui = UIManager([
            ("title", "./ka1.ttf", TITLE_TEXT_FONT_SIZE),
            ("prompt", "./ka1.ttf", PROMPT_TEXT_FONT_SIZE), 
            ("score", "./ka1.ttf", SCORE_TEXT_FONT_SIZE)
        ])
        
        window_size = self.get_window().get_size()
        player_one_pos = (
            0 + PADDLE_SIZE[0] / 2 + PADDLE_X_OFFSET,
            window_size[1] / 2 - PADDLE_SIZE[1] / 2    
        )
        player_two_pos = (
            window_size[0] - PADDLE_SIZE[0] * 1.5 - PADDLE_X_OFFSET,
            window_size[1] / 2 - PADDLE_SIZE[1] / 2    
        )
        ball_pos = (
            window_size[0] / 2 - BALL_SIZE[0] / 2,
            window_size[1] / 2 - BALL_SIZE[1] / 2,
        )
        self._player_one = GameObject(player_one_pos, PADDLE_SIZE, COLOR_GAME_OBJECT)
        self._player_two = GameObject(player_two_pos, PADDLE_SIZE, COLOR_GAME_OBJECT)
        self._ball = GameObject(ball_pos, BALL_SIZE, COLOR_GAME_OBJECT)
        pass


    def _handle_events(self) -> int:
        events = pygame.event.get()
        for event in events:
            match(event.type):
                case pygame.QUIT:
                    return -1
                
                case pygame.KEYDOWN:
                    match(event.key):
                        case pygame.K_ESCAPE:
                            return -1
                    
                        case pygame.K_SPACE:
                            current_game_state = self.get_game_stats().get_current_game_state()
                            
                            if current_game_state == GameState.GAME_START:
                                self.get_game_stats().set_current_game_state(GameState.ROUND_START)
                            
                            if current_game_state == GameState.ROUND_START:
                                self.get_game_stats().set_current_game_state(GameState.ROUND_IN_PROGRESS)

        return 1


    def _handle_input(self):
        # TODO: Implement player input handling
        pass


    def _render_start_screen(self) -> None:
        title_card: Text = self._ui.draw_text("Py-Pong!", "title", COLOR_TITLE_CARD)
        title_card_pos = (
            self._window.get_size()[0] / 2 - title_card.size[0] / 2, 
            self._window.get_size()[1] / 2 - title_card.size[1] / 2 - title_card.line_size
        )

        space_prompt: Text = self._ui.draw_text("Press SPACE to start", "prompt", COLOR_PROMPT)
        space_prompt_pos = (
            self._window.get_size()[0] / 2 - space_prompt.size[0] / 2,
            ((self._window.get_size()[1] / 2 - space_prompt.size[1] / 2))
        )
        
        escape_prompt: Text = self._ui.draw_text("Press ESC to quit the game", "prompt", COLOR_PROMPT)
        escape_prompt_pos = (
            self._window.get_size()[0] / 2 - escape_prompt.size[0] / 2,
            (self._window.get_size()[1] / 2 - escape_prompt.size[1] / 2) + space_prompt.line_size
        )

        window_surface = self._window.get_surface()
        window_surface.fill(COLOR_BACKGROUND)
        window_surface.blit(title_card.surface, title_card_pos)
        window_surface.blit(space_prompt.surface, space_prompt_pos)
        window_surface.blit(escape_prompt.surface, escape_prompt_pos)

    
    def _render_game_screen(self) -> None:
        player_one_rect = self._player_one.get_rect()
        player_one_pos = (player_one_rect.x, player_one_rect.y)
        
        player_two_rect = self._player_two.get_rect()
        player_two_pos = (player_two_rect.x, player_two_rect.y)
        
        ball_rect = self._ball.get_rect()
        ball_pos = (ball_rect.x, ball_rect.y)

        window_surface = self.get_window().get_surface()
        window_surface.fill(COLOR_BACKGROUND)
        window_surface.blit(self._player_one.get_surface(), player_one_pos)
        window_surface.blit(self._player_two.get_surface(), player_two_pos)
        window_surface.blit(self._ball.get_surface(), ball_pos)

