import pygame
from data.widgets.bases import _Widget
from data.assets import FONTS
from data.utils.font_helpers import height_to_font_size

FONT_SIZE_FACTOR = 0.2

class BrowserItem(_Widget):
    def __init__(self, relative_position, width, margin, font_size=30, text_colour=(100, 100, 100), font=FONTS['default']):
        super().__init__()
        self._screen_size = pygame.display.get_surface().get_size()

        self._relative_position = relative_position
        self._font = font
        self._relative_margin = margin / self._screen_size[1]
        self._relative_width = width / self._screen_size[1]

        self._relative_font_size = font_size
        
        self._empty_surface = pygame.Surface((0, 0))

        if margin * 2 >= width:
            raise ValueError('Width is too small to fit specified margin! (BrowserItem.__init__)', width, self._margin)
        
        self.set_image()
        self.set_geometry()

    @property
    def _position(self):
        return (self._relative_position[0] * self._screen_size[0], self._relative_position[1] * self._screen_size[1])

    @property
    def _margin(self):
        return self._relative_margin * self._screen_size[1]

    @property
    def _width(self):
        return self._relative_width * self._screen_size[1]

    @property
    def _size(self):
        board_width = self._width - 2 * self._margin
        board_height = board_width * 0.8
        text_height = board_width * FONT_SIZE_FACTOR
        overall_height = (1 * board_height) + (4 * text_height) + (4 * self._margin)

        return (self._width, overall_height)

    @property
    def _font_size(self):
        return self._relative_font_size * self._screen_size[1]
    
    def set_image(self):
        pass
    
    def set_geometry(self):
        self.rect = self.image.get_rect()
        self.rect.topleft = self._position
    
    def set_screen_size(self, new_screen_size):
        self._screen_size = new_screen_size
    
    def process_event(self, event):
        pass