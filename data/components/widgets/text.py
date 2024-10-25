import pygame
from data.components.widgets.bases import _Widget
from data.assets import FONTS

class Text(_Widget): # Pure text
    def __init__(self, relative_position, text, text_colour=(100, 100, 100), font_size=100, fill_colour=(255, 255, 255), margin=50, border_width=0, border_colour=(255, 255, 255), border_radius=5):
        super().__init__()
        self._screen_size = pygame.display.get_surface().get_size()

        self._relative_position = relative_position

        self._text = text
        self._text_colour = text_colour
        self._font = FONTS['default']

        self._relative_margin = margin / self._screen_size[1]
        self._relative_font_size = font_size / self._screen_size[1]
        self._relative_border_width = border_width / self._screen_size[1]
        self._relative_border_radius = border_radius / self._screen_size[1]

        self._fill_colour = fill_colour

        self._border_colour = border_colour

        self.rect = self._font.get_rect(self._text, size=self._font_size)
        self.rect.topleft = self._position

        self._empty_surface = pygame.Surface((0, 0), pygame.SRCALPHA)

        self.set_image()
        self.set_geometry()

    @property
    def _position(self):
        return (self._relative_position[0] * self._screen_size[0], self._relative_position[1] * self._screen_size[1])

    @property
    def _size(self):
        font_rect = self._font.get_rect(self._text, size=self._font_size)
        return font_rect.inflate(2 *self._margin, 2 *self._margin).size

    @property
    def _font_size(self):
        return self._relative_font_size * self._screen_size[1]

    @property
    def _margin(self):
        return self._relative_margin * self._screen_size[1]

    @property
    def _border_width(self):
        return self._relative_border_width * self._screen_size[1]
    
    @property
    def _border_radius(self):
        return self._relative_border_radius * self._screen_size[1]
    
    def set_image(self):
        text_surface = pygame.transform.scale(self._empty_surface, self._size)
        self.image = text_surface

        if self._fill_colour:
            fill_rect = pygame.Rect(0, 0, self._size[0], self._size[1])
            pygame.draw.rect(self.image, self._fill_colour, fill_rect, border_radius=int(self._border_radius))

        if self._border_width:
            fill_rect = pygame.Rect(0, 0, self._size[0], self._size[1])
            pygame.draw.rect(self.image, self._border_colour, fill_rect, width=int(self._border_width), border_radius=int(self._border_radius))

        self._font.render_to(self.image, (self._margin, self._margin), self._text, fgcolor=self._text_colour, size=self._font_size)
    
    def set_geometry(self):
        self.rect = self.image.get_rect()
        self.rect.topleft = self._position
    
    def set_screen_size(self, new_screen_size):
        self._screen_size = new_screen_size

    def process_event(self, event):
        pass