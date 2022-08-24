from typing import Tuple
import pygame.display
import pygame.surface


"""Class that represents the window in which the game is taking place"""
class GameWindow:
    """Initialize the window's surface as pygame's main drawing surface
    to which all of the subsequent Surfaces are rendered"""
    def __init__(self, width: int, height: int, caption: str) -> None:
        self._width = width
        self._height = height
        self._caption = caption

        self._surface = pygame.display.set_mode((width, height))
        pygame.display.set_caption(caption)


    """De-initialize and dispose of the window"""
    def __del__(self) -> None:
        pygame.display.quit()
        del self._surface



    def get_surface(self) -> pygame.surface.Surface:
        return self._surface

    def get_size(self) -> Tuple[int, int]:
        return (self._width, self._height)

    def get_caption(self) -> str:
        return self._caption