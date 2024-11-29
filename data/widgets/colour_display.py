import pygame
from data.widgets.bases import _Widget

class _ColourDisplay(_Widget):
    def __init__(self, relative_position, relative_size):

        self._relative_position = relative_position
        self._relative_size = relative_size

        self._colour = None
        
        self._empty_surface = pygame.Surface(self._size)
    
    @property
    def _size(self):
        return (self._relative_size[0] * self._surface_size[0], self._relative_size[1] * self._surface_size[1])
    
    @property
    def _position(self):
        return (self._relative_position[0] * self._surface_size[0], self._relative_position[1] * self._surface_size[1])

    def set_colour(self, new_colour):
        self._colour = new_colour
    
    def set_image(self):
        self.image = pygame.transform.scale(self._empty_surface, self._size)
        self.image.fill(self._colour)
    
    def set_geometry(self):
        self.rect = self.image.get_rect()
        self.rect.topleft = self._position
    
    def set_surface_suze(self, new_surface_size):
        self._surface_size = new_surface_size
    
    def process_event(self, event):
        pass