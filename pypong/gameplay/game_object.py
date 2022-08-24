from typing import Tuple

import pygame.surface
import pygame.rect


class GameObject:
    def __init__(self, 
                 position: Tuple[int, int], 
                 size: Tuple[int, int],
                 color: Tuple[int, int, int]) -> None:
        self._surface = pygame.surface.Surface(size)
        self._surface.fill(color)
        self._rect = pygame.rect.Rect(position[0], position[1], size[0], size[1])
        self._size = size



    def move(self, speed: Tuple[int, int]):
        self._rect = self._rect.move(speed)
        pass



    def get_surface(self) -> pygame.surface.Surface:
        return self._surface

    
    def get_rect(self) -> pygame.rect.Rect:
        return self._rect