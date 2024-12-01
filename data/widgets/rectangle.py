import pygame
from data.widgets.bases import _Widget

class Rectangle(_Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self._empty_surface = pygame.Surface((0, 0), pygame.SRCALPHA)
        
        self.set_image()
        self.set_geometry()
    
    def set_image(self):
        self.image = pygame.transform.scale(self._empty_surface, self.size)
        pygame.draw.rect(self.image, self._fill_colour, self.image.get_rect(), border_radius=int(self.border_radius))

        if self.border_width:
            pygame.draw.rect(self.image, self._border_colour, self.image.get_rect(), width=int(self.border_width), border_radius=int(self.border_radius))
    
    def process_event(self, event):
        pass