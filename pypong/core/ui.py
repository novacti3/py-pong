from typing import Tuple
import pygame


class Text:
    def __init__(self, 
                 surface: pygame.Surface = None, 
                 font: pygame.font.Font  = None, 
                 size: Tuple[int, int]   = (0,0), 
                 line_size: int          = 0) -> None:
        self.surface = surface
        self.font = font
        self.size = size
        self.line_size = line_size


class UIManager:
    def __init__(self, fonts: list[Tuple[str, str, int]]) -> None:
        self._loaded_fonts = dict()

        for font_pair in fonts:
            self._loaded_fonts[font_pair[0]] = pygame.font.Font(font_pair[1], font_pair[2])


    def __del__(self) -> None:
        pass


    def draw_text(self, 
                  text: str, 
                  font_name:str, 
                  color: Tuple[int, int, int]) -> Text:
        if font_name in self._loaded_fonts:
            font = self._loaded_fonts[font_name]
            text_surface = font.render(text, 0, color)
            text_size = font.size(text)
            text_line_size = font.get_linesize()
            
            return Text(text_surface, font, text_size, text_line_size)
        else:
            return Text()
