import pygame
from data.widgets.bases import _Widget
from data.widgets.text import Text
from data.assets import FONTS

class MoveList(_Widget):
    def __init__(self, relative_position, width, fill_colour=(150, 150, 150), text_colour=(0, 0, 0), move_list=[('abc','cde'), ('fgh', 'ijk')], font=FONTS['default']):
        super().__init__()
        self._screen_size = pygame.display.get_surface().get_size()

        self._relative_position = relative_position
        self._relative_width = width / self._screen_size[1]
        self._move_list = move_list

        self._font = font

        self._fill_colour = pygame.Color(fill_colour)
        self._text_colour = pygame.Color(text_colour)
        
        self._empty_surface = pygame.Surface((0, 0), pygame.SRCALPHA)
        
        self.set_image()
        self.set_geometry()

    @property
    def _position(self):
        return (self._relative_position[0] * self._screen_size[0], self._relative_position[1] * self._screen_size[1])

    @property
    def _width(self):
        return self._relative_width * self._screen_size[1]
    
    def calculate_font_size(self):
        bounding_box_width = self._width / 5
        test_size = 1
        while True:
            glyph_metrics = self._font.get_metrics((' ' * 6), size=test_size)
            
            if glyph_metrics[0][4] > bounding_box_width:
                return (test_size - 1) / self._screen_size[1]

            test_size += 1

    def append_to_move_list(self, new_move):
        self._move_list.append(new_move)
        self.set_image()
        self.set_geometry()
    
    def set_image(self):
        self.image = pygame.transform.scale(self._empty_surface, (self._width, 200)) # TEMP SIZE
        self.image.fill(self._fill_colour)
        font_size = self.calculate_font_size() * self._screen_size[1]
        print(font_size)

        for blue_move, red_move in self._move_list:
            text_position = (self._width / 5, 0)
            self._font.render_to(self.image, text_position, text=(blue_move + (' ' * 6) + red_move), size=font_size / 5 // WHATS GOING ON HERE, fgcolor=self._text_colour)
    
    def set_geometry(self):
        self.rect = self.image.get_rect()
        self.rect.topleft = self._position
    
    def set_screen_size(self, new_screen_size):
        self._screen_size = new_screen_size
    
    def process_event(self, event):
        pass