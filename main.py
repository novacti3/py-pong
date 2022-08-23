import pygame
import pypong.core.game_instance as pypong


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_CAPTION = "Py-Pong"

def main():
    pypong_instance = pypong.GameInstance(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_CAPTION)   
    
    delta_time = 0.0
    while pypong_instance.run(delta_time) != -1:
        pass
    pypong_instance.quit()


if __name__ == "__main__":
    main()