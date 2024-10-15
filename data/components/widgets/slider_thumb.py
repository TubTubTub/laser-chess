import pygame
from data.components.widgets.bases import _Pressable
from data.utils.widget_helpers import create_slider_thumb
from data.constants import WidgetState

class SliderThumb(_Pressable):
    def __init__(self, radius, colour, border_width=12, border_colour=(255, 255, 255)):
        super().__init__(
            down_func=lambda: self.down_func(),
            up_func=lambda: self.up_func(),
            hover_func=lambda: None
        )

        self._screen = pygame.display.get_surface()
        self._colour = colour
        self._border_colour  = border_colour
        self._radius = radius
        self._border_width = border_width
        self._percent = None

        self.set_surface()
        self.rect = self._thumb_surface.get_rect()

    def get_surface(self):
        return self._thumb_surface
    
    def get_percent(self):
        return self._percent
    
    def set_percent(self, percent):
        self._percent = percent
    
    def set_radius(self, radius):
        self._radius = radius
    
    def set_colour(self, new_colour):
        self._colour = new_colour.rgb

        r, g, b = self._colour
        self._hover_colour = (max(r - 25, 0), max(g - 25, 0), max(b - 25, 0))
        self._press_colour = (max(r - 50, 0), max(g - 50, 0), max(b - 50, 0))
        self._colour_copy = self._colour
    
    def set_border_width(self, new_border_width):
        self._border_width = new_border_width
    
    def set_surface(self, new_colour=None):
        if new_colour is None:
            new_colour = self._colour

        self._thumb_surface = create_slider_thumb(self._radius, new_colour, self._border_colour, self._border_width)
        self.rect = self._thumb_surface.get_rect()
    
    def set_state_colour(self, state):
        match state:
            case WidgetState.DEFAULT:
                self.set_surface(self._colour_copy)
            case WidgetState.HOVER:
                self.set_surface(self._hover_colour)
            case WidgetState.PRESS:
                self.set_surface(self._press_colour)
    
    def down_func(self):
        self.set_state_colour(WidgetState.PRESS)
    
    def up_func(self):
        self.set_state_colour(WidgetState.DEFAULT)