import pygame
from data.components.widgets.bases import _Widget
from data.utils.settings_helpers import get_user_settings
from data.utils.widget_helpers import create_square_gradient

user_settings = get_user_settings()

class ColourSquare(_Widget):
    def __init__(self, surface, relative_position, default_colour=(255, 0, 0)):
        super().__init__()
        self._screen_size = pygame.display.get_surface().get_size()
        self._origin_position = origin_position
        self._colour = pygame.Color(default_colour)
        self._font = pygame.freetype.Font(user_settings['primaryFont'])

        self._select_area = create_square_gradient*(self._screen_size[1] * 0.2,

        self.set_image()
        self.set_geometry()
    
    def set_colour(self, new_colour):
        self._square_surface = create_square_gradient()
    
    def set_image(self):
        self.image = self._select_area
    
    def set_geometry(self):
        self.rect = self.image.get_rect()
    
    def process_event(self, event):
        pass