from typing import Tuple
import pygame.surface
import pygame.font


"""Struct that represents a single line of text"""
class Text:
    def __init__(self, 
                 surface: pygame.surface.Surface = None, 
                 font: pygame.font.Font = None, 
                 size: Tuple[int, int] = (0,0), 
                 line_size: int = 0) -> None:
        """Renderable Surface that the text occupies"""
        self.surface = surface
        """The font used for this line of textx"""
        self.font = font
        """The size of this *entire line* of text"""
        self.size = size
        """Height (in pixels) offset that another line of text of the same font and font size
        should follow in order to render properly"""
        self.line_size = line_size


"""Class that handles font loading and preparation of Text objects for rendering"""
class UIManager:
    """Create UIManager and load the provided list of fonts into memory for use by text rendering
    Format: Tuple(identifier, path_to_font_file, font_size)
    Fonts are stored in a dictionary. The identifier string is used as a key to access the desired font.
    """
    def __init__(self, fonts_to_load: list[Tuple[str , str, int]]) -> None:
        self._loaded_fonts = dict()

        # Load every font in the provided list into the dictionary of loaded fonts
        # following the format described: 
        # dict({key: str=identifier, value: Font=Font(path_to_font_file, font_size)})
        for font_info in fonts_to_load:
            self._loaded_fonts[font_info[0]] = pygame.font.Font(font_info[1], font_info[2])


    """Create a Text object from the following string
    Parameter 'font_name' must correspond to an identifier stored inside of the dictionary of loaded fonts.
    Text object is only created if a font with the same identifier as provided is found among loaded fonts,
    otherwise an empty Text object is returned"""
    def draw_text(self, 
                  text: str, 
                  font_name:str, 
                  color: Tuple[int, int, int]) -> Text:
        if font_name in self._loaded_fonts:
            font = self._loaded_fonts[font_name]
            # Create the Surface using the provided text str for rendering later
            text_surface = font.render(text, 0, color)
            text_size = font.size(text)
            text_line_size = font.get_linesize()
            
            return Text(text_surface, font, text_size, text_line_size)
        else:
            return Text()
