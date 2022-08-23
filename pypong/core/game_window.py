import pygame


class GameWindow:
    def __init__(self, width: int, height: int, caption: str) -> None:
        self._width = width
        self._height = height
        self._caption = caption

        self._surface = pygame.display.set_mode((width, height))
        pygame.display.set_caption(caption)

    def __del__(self) -> None:
        pygame.display.quit()
        del self._surface


    def get_surface(self) -> pygame.Surface:
        return self._surface

    def get_width(self) -> int:
        return self._width

    def get_height(self) -> int:
        return self._height

    def get_caption(self) -> str:
        return self._caption