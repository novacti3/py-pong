import pygame.time
import pypong.core.game_instance as pypong


SCREEN_WIDTH   = 800
SCREEN_HEIGHT  = 600
SCREEN_CAPTION = "Py-Pong!"


def main():
    pypong_instance = pypong.GameInstance()  
    pypong_instance.start(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_CAPTION) 
    
    delta_time = 0.0
    last_time = 0.0
    while pypong_instance.run(delta_time) != -1:
        t = pygame.time.get_ticks()
        delta_time = (t - last_time) / 1000
        last_time = t

    pypong_instance.quit()


if __name__ == "__main__":
    main()