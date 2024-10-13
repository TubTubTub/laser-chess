import pygame
from data.components.widgets.bases import _Pressable

class SliderThumb(_Pressable):
    def __init__(self, radius, colour, border_width):
        super().__init__()
        self._colour = colour
        self._radius = radius

        self.thumb_surface = pygame.Surface((self._radius * 2, self._radius * 2))
        pygame.draw.circle(self.thumb_surface, colour, (self._radius, self._radius), self._radius, width=border_width)