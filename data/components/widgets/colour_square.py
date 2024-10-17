import pygame
from data.components.widgets.bases import _Widget
from data.utils.widget_helpers import create_square_gradient

class ColourSquare(_Widget):
    def __init__(self, surface, relative_position, relative_length):
        super().__init__()
        self._screen = surface
        self._screen_size = self._screen.get_size()

        self._relative_position = relative_position
        self._relative_length = relative_length

        self._colour = None
    
    def set_colour(self, new_colour):
        self._colour = pygame.Color(new_colour)
    
    def set_image(self):
        self.image = create_square_gradient(side_length=self._relative_length * self._screen_size[1], colour=self._colour)
    
    def set_geometry(self):
        self.rect = self.image.get_rect()
        self.rect.topleft = (self._relative_position[0] * self._screen_size[0], self._relative_position[1] * self._screen_size[1])
    
    def set_screen_size(self, new_screen_size):
        self._screen_size = new_screen_size
    
    def process_event(self, event):
        pass