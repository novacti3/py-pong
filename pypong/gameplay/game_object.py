from turtle import pos
from typing import Tuple
from math import copysign

import pygame.surface
import pygame.rect


class GameObject:
    def __init__(self, 
                 position: list[float, float], 
                 scale: Tuple[int, int],
                 color: Tuple[int, int, int]) -> None:
        self._surface = pygame.surface.Surface(scale)
        self._surface.fill(color)
        self._rect = pygame.rect.Rect(round(position[0]), round(position[1]), scale[0], scale[1])
        self._position = position
        self._scale = scale



    def move(self, speed: Tuple[float, float]):
        self._position[0] += speed[0]
        self._position[1] += speed[1]
        self._rect.x = round(self._position[0])
        self._rect.y = round(self._position[1])
    


    def get_surface(self) -> pygame.surface.Surface:
        return self._surface

    
    def get_rect(self) -> pygame.rect.Rect:
        return self._rect

    
    def get_position(self) -> Tuple[int, int]:
        return (self._rect.x, self._rect.y)


    def get_scale(self) -> Tuple[int, int]:
        return self._scale