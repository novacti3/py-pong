import pygame
# Importing everything directly because this file contains the entry point
# of the entire package (game) and the project is small enough
# that the extra verbosity of typing out the entire module path
# is redundant 
from pypong.core.game_stats import GameState, GameStats, PlayerIndex
from pypong.core.game_window import GameWindow
from pypong.core.ui import Text, UIManager
from pypong.gameplay.game_object import GameObject
from pypong.gameplay.ball import Ball 


# Color constants for each kind of object in the game
# for ease of use and easy customizability
COLOR_TITLE_CARD = (255, 237, 38)
COLOR_IMPORTANT_PROMPT = (255, 255, 255)
COLOR_PROMPT = (150, 150, 150)
COLOR_GAME_OBJECT = (150, 150, 150)
COLOR_SCORE = (77, 77, 77)
COLOR_BACKGROUND = (0, 0, 0)


# Constants for the font sizes used for different kinds
# of text in the game, again in the name of ease of use,
# consistency and customizability
TITLE_TEXT_FONT_SIZE = 72
SCORE_TEXT_FONT_SIZE = 48
PROMPT_TEXT_FONT_SIZE = 28


# Game options
PADDLE_SIZE = (20, 125)
PADDLE_SPEED = 200.0
PADDLE_X_OFFSET = 25

BALL_SIZE = (25, 25)
BALL_SPEED = 235.0

CENTER_LINE_WIDTH = 3


"""Class representing the entry point of the entire package (game)
Contains the game loop as well as the game logic, along with all parts
necessary to make it work"""
class GameInstance:
    """Initializes the game, window and all of the game's resources, priming it for playing"""
    def start(self, window_width: int, window_height: int, window_caption: str) -> None:
        # Init pygame
        pygame.init()
        
        # Create and init window
        self._window = GameWindow(window_width, window_height, window_caption)
        
        # Init game stats
        self._game_stats = GameStats()
        
        # Load the game's resources
        self._init_resources()


    """Stops the game and cleans up everything"""
    def quit(self) -> None:
        pygame.quit()


    """Continues running the core game loop and the game logic"""
    def run(self, delta_time: float) -> int:
        # Handle pygame's events first
        # If pygame.QUIT event is encountered (either through closing the window
        # or the user pressing ESC) quit out of the game because there's
        # no point in finishing this iteration of the game loop since the game
        # will stop and quit next frame anyway
        event_result = self._handle_events()
        if event_result == -1:
            return event_result

        # Cache the window's Surface for rendering purposes 
        window_surface = self._window.get_surface()
        
        # Core game loop
        # Choose what happens depending on the current state of the game
        match(self._game_stats.current_game_state):
            # Display the start screen
            case GameState.GAME_START:
                window_surface.fill(COLOR_BACKGROUND)
                self._render_start_screen()
            
            # Display instructions on how to start the round
            # along with the playing field and score
            case GameState.ROUND_START:
                window_surface.fill(COLOR_BACKGROUND)
                self._render_score_counter()
                self._render_paddles()
                self._render_ball()
                self._render_round_start_prompt()

            # Main game logic. Move the paddles based on player input,
            # move the ball, see who scored
            case GameState.ROUND_IN_PROGRESS:
                self._handle_input(delta_time)
                self._move_ball(delta_time)
                self._handle_collisions()
                self._evaluate_score()
                window_surface.fill(COLOR_BACKGROUND)
                self._render_score_counter()
                self._render_paddles()
                self._render_ball()
                pass

            # Display who won the current round and instructions
            # on how to begin the next round
            case GameState.ROUND_END:
                window_surface.fill(COLOR_BACKGROUND)
                self._render_score_counter()
                self._render_paddles()
                self._render_ball()
                self._render_round_end_prompt()
                pass

        # Switch swapchain buffers and show rendered Surfaces to the screen
        pygame.display.update()
        return event_result



    def get_window(self) -> GameWindow:
        return self._window


    def get_game_stats(self) -> GameStats:
        return self._game_stats


    # Creates and initializes all of the resources required by the game to work
    def _init_resources(self):
        # Load the font in all of the desired font sizes 
        # for the different Text objects in the game
        self._ui = UIManager([
            ("title", "./ka1.ttf", TITLE_TEXT_FONT_SIZE),
            ("prompt", "./ka1.ttf", PROMPT_TEXT_FONT_SIZE), 
            ("score", "./ka1.ttf", SCORE_TEXT_FONT_SIZE)
        ])
        
        window_size = self._window.get_size()
        # Player one pos:
        # Since the left part of the screen is 0, add 1/2 of paddle width
        # to the border (so that the center of the paddle is properly placed)
        # and further offset it from the window border by the specified X offset 
        player_one_pos = [
            0 + PADDLE_SIZE[0] / 2 + PADDLE_X_OFFSET,
            window_size[1] / 2 - PADDLE_SIZE[1] / 2    
        ]
        # Player two pos:
        # Since the right part of the screen is the specified screen resolution width,   
        # subtract 1/2 of paddle width from the right border 
        # (so that the center of the paddle is properly placed) and further offset it 
        # by the specified X offset so that there's a bit of space between it 
        # and the side of the window
        player_two_pos = [
            window_size[0] - PADDLE_SIZE[0] * 1.5 - PADDLE_X_OFFSET,
            window_size[1] / 2 - PADDLE_SIZE[1] / 2    
        ]

        # Ball pos:
        # Move the center of the ball Surface (BALL_SIZE / 2) to the center of the screen 
        ball_pos = [
            window_size[0] / 2 - BALL_SIZE[0] / 2,
            window_size[1] / 2 - BALL_SIZE[1] / 2,
        ]

        # Initialize the actual GameObjects
        self._player_one = GameObject(player_one_pos, PADDLE_SIZE, COLOR_GAME_OBJECT)
        self._player_two = GameObject(player_two_pos, PADDLE_SIZE, COLOR_GAME_OBJECT)
        self._ball = Ball(ball_pos, [0.0, 0.0], BALL_SIZE, COLOR_GAME_OBJECT)


    # Handles all of the pygame library events, such as whether to quit the game etc.
    # Returns the result of pygame events. If pygame.QUIT is encountered, return -1
    # so that the user program knows to stop running the game and exit
    def _handle_events(self) -> int:
        # Queue of all events that have occured last frame
        events = pygame.event.get()
        for event in events:
            match(event.type):
                # Game window "X" button pressed
                case pygame.QUIT:
                    return -1
                
                case pygame.KEYDOWN:
                    match(event.key):
                        # Allow the player to quit the game at any time using ESC
                        case pygame.K_ESCAPE:
                            return -1
                    
                        # Handle game state switching relative to whichever state
                        # the game is currently in
                        case pygame.K_SPACE:
                            # Caching the state here to make the following conditionals
                            # a bit more readable and less cluttered
                            current_game_state = self._game_stats.current_game_state

                            # Advance the game to the start of the round                            
                            if current_game_state == GameState.GAME_START:
                                self._game_stats.current_game_state = GameState.ROUND_START
                            
                            # Start the actual gameplay                            
                            if current_game_state == GameState.ROUND_START:
                                # Give the ball some velocity so that it actually moves around
                                self._ball.velocity = [-BALL_SPEED, BALL_SPEED]
                                self._game_stats.current_game_state = GameState.ROUND_IN_PROGRESS

                            # Reset all of the objects' positions and start a new round
                            if current_game_state == GameState.ROUND_END:
                                self._player_one.reset()
                                self._player_two.reset()
                                self._ball.reset()
                                self._game_stats.current_game_state = GameState.ROUND_START

        return 1


    # Detects and handles player input (both players), moves the respective paddles
    def _handle_input(self, delta_time: float):
        pressed_keys = pygame.key.get_pressed()

        window_size = self._window.get_size()
        
        player_one_pos = self._player_one.get_position()
        player_one_scale = self._player_one.get_scale()
        
        player_two_pos = self._player_two.get_position()
        player_two_scale = self._player_two.get_scale()

        # Player one (left paddle)
        if pressed_keys[pygame.K_w]:
            # Ensures that the paddle doesn't go "above" the visible screen
            if player_one_pos[1] > 0:
                # Multiply the speed by the current delta_time to ensure
                # the same speed across all devices, regardless of the game's FPS
                self._player_one.move((0, -PADDLE_SPEED * delta_time))
        
        if pressed_keys[pygame.K_s]:
            # Ensures that the paddle doesn't go "below" the visible screen
            # The paddle height must be added on top of the position
            # because the paddle's origin point is at the top,
            # not the bottom
            if player_one_pos[1] + player_one_scale[1] < window_size[1]:
                self._player_one.move((0, PADDLE_SPEED * delta_time))

        # Player two (right paddle)
        if pressed_keys[pygame.K_UP]:
            if player_two_pos[1] > 0:
                self._player_two.move((0, -PADDLE_SPEED * delta_time))
        if pressed_keys[pygame.K_DOWN]:
            if player_two_pos[1] + player_two_scale[1] < window_size[1]:
                self._player_two.move((0, PADDLE_SPEED * delta_time))


    # Moves the ball and ensures that it bounces back from the edges of the screen (if necessary)
    def _move_ball(self, delta_time: float):
        window_size = self._window.get_size()
        ball_pos = self._ball.get_position()
        # Works as an "alias" for _ball.velocity because it's a reference
        ball_velocity = self._ball.velocity

        # Revert X velocity if the ball touches either the left or right border of window respectively
        # (it is necessary to add the ball's width to the right edge check because the origin
        # of the ball is in the top left corner)
        if ball_pos[0] <= 0 or ball_pos[0] + BALL_SIZE[0] >= window_size[0]:
            ball_velocity[0] *= -1
        # Revert X velocity if the ball touches either the top of bottom edge of window respectively
        # (same thing for the bottom edge as for the right edge before, just with the ball's height this time)
        if ball_pos[1] <= 0 or ball_pos[1] + BALL_SIZE[1] >= window_size[1]:
            ball_velocity[1] *= -1

        # Multiply the velocity by delta_time to make sure that the ball moves by the same speed
        # across all devices, no matter how fast they are running the game
        self._ball.move((
            ball_velocity[0] * delta_time, 
            ball_velocity[1] * delta_time
        ))        


    # Bounces the ball back if it collides with a paddle
    def _handle_collisions(self):
        ball_rect = self._ball.get_rect()
        if ball_rect.colliderect(self._player_one.get_rect()) or \
           ball_rect.colliderect(self._player_two.get_rect()):
           self._ball.velocity[0] *= -1

    
    # Checks if the ball has moved to the same level as the paddles
    # If so, it evaluates who has scored a point
    def _evaluate_score(self):
        game_stats = self._game_stats
        score = list(game_stats.score)
        
        ball_pos_x = self._ball.get_rect().center[0]
        player_one_pos_x = self._player_one.get_rect().center[0]
        player_two_pos_x = self._player_two.get_rect().center[0]

        has_score_changed = False
        player_who_scored: PlayerIndex = 0

        if ball_pos_x <= player_one_pos_x:
            score[0] += 1
            has_score_changed = True
            player_who_scored = PlayerIndex.PLAYER_TWO
        elif ball_pos_x >= player_two_pos_x:
            score[1] += 1
            has_score_changed = True
            player_who_scored = PlayerIndex.PLAYER_ONE

        if has_score_changed:
            game_stats.score = tuple(score)
            game_stats.player_who_last_scored = player_who_scored
            game_stats.current_game_state = GameState.ROUND_END
            self._ball.velocity = [0.0, 0.0]



    # Renders the start screen to the game window screen
    def _render_start_screen(self) -> None:
        title_card: Text = self._ui.draw_text("Py-Pong!", "title", COLOR_TITLE_CARD)
        space_prompt: Text = self._ui.draw_text("Press SPACE to start", "prompt", COLOR_IMPORTANT_PROMPT)
        escape_prompt: Text = self._ui.draw_text("Press ESC to quit the game", "prompt", COLOR_IMPORTANT_PROMPT)
        
        window_size = self._window.get_size()
        # Center the title card to the middle of the screen and move it up slightly
        # to make room for the other text
        title_card_pos = (
            window_size[0] / 2 - title_card.size[0] / 2, 
            window_size[1] / 2 - title_card.size[1] / 2 - title_card.line_size
        )

        # Center the space prompt and place it slightly below the title card
        space_prompt_pos = (
            window_size[0] / 2 - space_prompt.size[0] / 2,
            title_card_pos[1] + title_card.line_size * 1.5
        )
        
        # Center the escape prompt and place it below the space prompt
        escape_prompt_pos = (
            window_size[0] / 2 - escape_prompt.size[0] / 2,
            space_prompt_pos[1] + space_prompt.line_size
        )

        window_surface = self._window.get_surface()
        window_surface.blit(title_card.surface, title_card_pos)
        window_surface.blit(space_prompt.surface, space_prompt_pos)
        window_surface.blit(escape_prompt.surface, escape_prompt_pos)


    # Renders the start round instruction prompt to the screen
    def _render_round_start_prompt(self) -> None:
        window = self._window
        window_size = window.get_size()

        prompt = self._ui.draw_text("Press SPACE to start", "prompt", COLOR_IMPORTANT_PROMPT)
        # Center the prompt horizontally and place it just above the ball
        prompt_pos = (
            window_size[0] / 2 - prompt.size[0] / 2,
            self._ball.get_position()[1] - prompt.line_size * 2 
        )
        window.get_surface().blit(prompt.surface, prompt_pos)
    

    # Render who scored and how to start a new round at the end of the current round to the screen
    def _render_round_end_prompt(self) -> None:
        window = self._window
        window_size = window.get_size()
        last_player_to_score = self._game_stats.player_who_last_scored

        winner_prompt = self._ui.draw_text(f"Player {int(last_player_to_score)} scored!", "prompt", COLOR_IMPORTANT_PROMPT)
        space_prompt = self._ui.draw_text("Press SPACE", "prompt", COLOR_PROMPT)
        new_round_prompt = self._ui.draw_text("to start new round", "prompt", COLOR_PROMPT)

        center_width = window_size[0] / 2
        # Center the winner prompt horizontally and place it slightly above the center of the screen
        winner_prompt_pos = (
            center_width - winner_prompt.size[0] / 2,
            window_size[1] / 2 - winner_prompt.size[1] / 2 - winner_prompt.line_size
        )
        # Horizontally center the SPACE instruction prompt and place it a bit below the winner prompt
        space_prompt_pos = (
            center_width - space_prompt.size[0] / 2,
            winner_prompt_pos[1] + winner_prompt.line_size * 2
        )
        # Put the rest of the instruction prompt just below the first part
        new_round_prompt_pos = (
            center_width - new_round_prompt.size[0] / 2,
            space_prompt_pos[1] + space_prompt.line_size
        )

        window.get_surface().blit(winner_prompt.surface, winner_prompt_pos)
        window.get_surface().blit(space_prompt.surface, space_prompt_pos)
        window.get_surface().blit(new_round_prompt.surface, new_round_prompt_pos)


    # Render the player paddles to the screen, along with the line separating them
    def _render_paddles(self) -> None:
        player_one_rect = self._player_one.get_rect()
        player_two_rect = self._player_two.get_rect()
        
        player_one_pos = (player_one_rect.x, player_one_rect.y)
        player_two_pos = (player_two_rect.x, player_two_rect.y)
        
        window_size = self._window.get_size()
        window_surface = self._window.get_surface()

        pygame.draw.line(window_surface, COLOR_SCORE, (window_size[0] / 2, 0), (window_size[0] / 2, window_size[1]), CENTER_LINE_WIDTH)
        window_surface.blit(self._player_one.get_surface(), player_one_pos)
        window_surface.blit(self._player_two.get_surface(), player_two_pos)


    # Render the ball to the screen
    def _render_ball(self) -> None:
        window_surface = self._window.get_surface()
        window_surface.blit(self._ball.get_surface(), self._ball.get_position())


    # Render the score counter to the screen
    def _render_score_counter(self) -> None:
        score = self._game_stats.score
        
        player_one_score = self._ui.draw_text(str(score[0]), "score", COLOR_SCORE)
        player_two_score = self._ui.draw_text(str(score[1]), "score", COLOR_SCORE)
        
        window_size = self._window.get_size()
        # Center the first player's score between the left edge of the screen
        # and the line in the center of the field and place it a bit below
        # the top edge of the window
        player_one_score_pos = (
            window_size[0] / 4 - player_one_score.size[0] / 2,
            0 + player_one_score.size[1] + player_one_score.line_size
        )
        # Center the second player's score between the right edge of the screen
        # and the line in the center of the field and place it a bit below
        # the top edge of the window
        player_two_score_pos = (
            3 * window_size[0] / 4 - player_two_score.size[0] / 2,
            0 + player_two_score.size[1] + player_two_score.line_size
        )

        window_surface = self._window.get_surface()
        window_surface.blit(player_one_score.surface, player_one_score_pos)
        window_surface.blit(player_two_score.surface, player_two_score_pos)