from typing import Tuple
import pygame


class UIManager:
    def __init__(self, fonts: list[Tuple[str, str, int]]) -> None:
        self._loaded_fonts = dict()

        for font_pair in fonts:
            self._loaded_fonts[font_pair[0]] = pygame.font.Font(font_pair[1], font_pair[2])


    def __del__(self) -> None:
        pass


    def get_font_line_size(self, font_name: str) -> int:
        if font_name in self._loaded_fonts:
            return self._loaded_fonts[font_name].get_linesize()
        else:
            return 0


    def draw_score(self, 
                   score: int, 
                   font_name:str, 
                   color: Tuple[int, int, int]) -> Tuple[pygame.Surface, Tuple[int, int]]:
        if font_name in self._loaded_fonts:
            font = self._loaded_fonts[font_name]
            text_surface = font.render(str(score), 0, color)
            text_size = font.size(str(score))
            return (text_surface, text_size)
        else:
            return (pygame.Surface((0,0)), (0,0))

    def draw_prompt(self, 
                    text: str, 
                    font_name:str, 
                    color: Tuple[int, int, int]) -> Tuple[pygame.Surface, Tuple[int, int]]:
        if font_name in self._loaded_fonts:
            font = self._loaded_fonts[font_name]
            text_surface = font.render(text, 0, color)
            text_size = font.size(text)
            return (text_surface, text_size)
        else:
            return (pygame.Surface((0,0)), (0,0))
