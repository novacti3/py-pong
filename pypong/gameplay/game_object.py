from typing import Tuple
import pygame.surface
import pygame.rect


"""Class that represents a movable and interactable object in the game
Should be used as a base for other objects
"""
class GameObject:
    """Create a new GameObject of the provided scale at the provided position"""
    def __init__(self, 
                 position: list[float, float] = [0.0, 0.0], 
                 scale: Tuple[int, int] = (1, 1),
                 color: Tuple[int, int, int] = (255, 255, 255)) -> None:
        # Renderable Surface of this object
        self._surface = pygame.surface.Surface(scale)
        self._surface.fill(color)
        # Collision rectangle of this object
        self._rect = pygame.rect.Rect(round(position[0]), round(position[1]), scale[0], scale[1])
        
        # Calling list() and tuple() class constructors here to copy values
        # of position and scale into a new list/tuple respectively so that
        # overwriting eg. self._position doesn't affect self._initial_position
        # ----
        # Using a separate _position attribute for enhanced precision (float)
        # pygame.Rect operate using ints, so using its positional attributes
        # directly isn't well suited for movement and the like
        self._position = list(position)
        self._initial_position = list(position)
        # Size of the object (in pixels)
        self._scale = tuple(scale)



    """Move the GameObject by the provided speed"""
    def move(self, speed: Tuple[float, float]):
        self._position[0] += speed[0]
        self._position[1] += speed[1]
        # pygame.Rect operates using int
        # Doing a simple assignment here would lead 
        # to an implicit loss of numbers past the decimal mark,
        # which'd mean a potential loss of data
        # and a possibly different position of the collision rect
        # relative to the object's actual position in space
        self._rect.x = round(self._position[0])
        self._rect.y = round(self._position[1])
    

    """Resets the GameObject's position to the position where it was first created"""
    def reset(self) -> None:
        self._position = list(self._initial_position)
        self._rect.x = round(self._position[0])
        self._rect.y = round(self._position[1])



    def get_surface(self) -> pygame.surface.Surface:
        return self._surface

    
    def get_rect(self) -> pygame.rect.Rect:
        return self._rect

    
    def get_position(self) -> Tuple[float, float]:
        return (self._position[0], self._position[1])


    def get_scale(self) -> Tuple[int, int]:
        return tuple(self._scale)