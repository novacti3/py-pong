import sys
import pygame.time
# Importing the game's entry point as an alias
# for clarity and convenience
import pypong.core.game_instance as pypong


# Game window options
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_CAPTION = "Py-Pong!"


def main():
    pypong_instance = pypong.GameInstance()  
    pypong_instance.start(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_CAPTION) 
    
    # Delta time = time between this frame and the last
    # Used to keep a consistent movement speed across devices
    # regardless of the frames-per-second that the game is
    # running at
    delta_time = 0.0
    last_time = 0.0
    # Keep running the game loop until either the window is closed
    # or the player presses ESC
    while pypong_instance.run(delta_time) != -1:
        # Amount of time since creation of the game instance
        # (in milliseconds)
        t = pygame.time.get_ticks()
 
        # Convert delta time from milliseconds to nanoseconds 
        # because for game calculations, milliseconds 
        # is a huge number to multiply by
        delta_time = (t - last_time) / 1000
        last_time = t

    # Close the game and clean up
    pypong_instance.quit()
    sys.exit()


if __name__ == "__main__":
    main()