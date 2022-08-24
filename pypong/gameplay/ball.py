from typing import Tuple
from pypong.gameplay.game_object import GameObject


"""Class representing the ball
Contains the ball's velocity used for movement calculations"""
class Ball(GameObject):
    def __init__(self, 
                 position: list[float, float] = [0.0, 0.0], 
                 velocity: list[float, float] = [0.0, 0.0],
                 scale: Tuple[int, int] = (1, 1), 
                 color: Tuple[int, int, int] = (255, 255, 255)) -> None:
        super().__init__(position, scale, color)
        self.velocity = list(velocity)