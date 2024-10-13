import pygame
from data.components.widgets.bases import _Widget
from data.utils.settings_helpers import get_user_settings

user_settings = get_user_settings()

class Text(_Widget): # Pure text
    def __init__(self, relative_position, text, text_colour=(255, 255, 255), font_size=100, fill_colour=(255, 255, 255), margin=50, border_width=0, border_colour=(255, 255, 255), border_radius=5):
        super().__init__()
        self._screen_size = pygame.display.get_surface().get_size()

        self._relative_position = relative_position

        self._text = text
        self._text_colour = text_colour
        self._font = pygame.freetype.Font(user_settings['primaryFont'])

        self._margin = margin

        self._fill_colour = fill_colour

        self._border_width = border_width
        self._border_colour = border_colour
        self._border_radius = border_radius
        
        self._relative_font_size = font_size / self._screen_size[1]

        position = (self._relative_position[0] * self._screen_size[0], self._relative_position[1] * self._screen_size[1])
        self.rect = self._font.get_rect(self._text, size=font_size)
        self.rect.topleft = position

        self._text_surface = pygame.Surface((0, 0))

        self.set_image()
        self.set_geometry()
    
    def set_image(self):
        font_size = self._relative_font_size * self._screen_size[1]

        font_rect = self._font.get_rect(self._text, size=font_size)
        surface_size = font_rect.inflate(self._margin, self._margin).size

        text_surface = pygame.transform.scale(self._text_surface, surface_size)
        self.image = text_surface

        if self._fill_colour:
            fill_rect = pygame.Rect(0, 0, surface_size[0], surface_size[1])
            pygame.draw.rect(self.image, self._fill_colour, fill_rect, border_radius=self._border_radius)

        if self._border_width:
            fill_rect = pygame.Rect(0, 0, surface_size[0], surface_size[1])
            pygame.draw.rect(self.image, self._border_colour, fill_rect, width=self._border_width, border_radius=self._border_radius)

        font_center = ((surface_size[0] - font_rect.size[0]) / 2, (surface_size[1] - font_rect.size[1]) / 2)
        self._font.render_to(self.image, font_center, self._text, fgcolor=self._text_colour, size=font_size)
    
    def set_geometry(self):
        position = (self._relative_position[0] * self._screen_size[0], self._relative_position[1] * self._screen_size[1])
        self.rect = self.image.get_rect()
        self.rect.center = position
    
    def set_screen_size(self, new_screen_size):
        self._screen_size = new_screen_size
    
    def process_event(self, event):
        pass