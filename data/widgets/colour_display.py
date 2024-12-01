import pygame
from data.widgets.bases import _Widget

class _ColourDisplay(_Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._colour = None
        
        self._empty_surface = pygame.Surface(self.size)

    def set_colour(self, new_colour):
        self._colour = new_colour
    
    def set_image(self):
        self.image = pygame.transform.scale(self._empty_surface, self.size)
        self.image.fill(self._colour)
    
    def process_event(self, event):
        pass