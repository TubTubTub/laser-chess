import pygame
from data.components.widgets.bases import _Pressable
from data.utils.widget_helpers import create_slider_thumb
from data.constants import WidgetState

class SliderThumb(_Pressable):
    def __init__(self, radius, colour, border_width=12, border_colour=(255, 255, 255)):
        super().__init__(
            down_func=lambda: self.down_func(),
            up_func=lambda: self.up_func(),
            hover_func=lambda: self.hover_func()
        )

        self._screen = pygame.display.get_surface()
        self._border_colour  = border_colour
        self._radius = radius
        self._border_width = border_width
        self._percent = None
        self._event = None

        self._colour = colour
        self.set_colour(pygame.Color(self._colour))

        self.set_surface()
    
    def set_colour(self, new_colour):
        self._colour = new_colour.rgb

        r, g, b = self._colour
        self._hover_colour = (max(r - 25, 0), max(g - 25, 0), max(b - 25, 0))
        self._press_colour = (max(r - 50, 0), max(g - 50, 0), max(b - 50, 0))
        self._colour_copy = self._colour

        self.set_surface()

    def get_surface(self):
        return self._thumb_surface
    
    def set_surface(self, radius, colour, border_colour, border_width):
        self._thumb_surface = create_slider_thumb()
        self.rect = self._thumb_surface.get_rect()
    
    def get_position(self):
        return (self.rect.x, self.rect.y)
    
    def set_position(self, position):
        self.rect.topleft = position
    
    def set_radius(self, radius):
        self._radius = radius
        self.set_surface()
    
    def set_state_colour(self, state):
        match state:
            case WidgetState.DEFAULT:
                # print('1 state')
                self.set_surface(self._colour_copy)
            case WidgetState.HOVER:
                # print('2 state')
                self.set_surface(self._hover_colour)
            case WidgetState.PRESS:
                # print('3 state')
                self.set_surface(self._press_colour)
    
    def down_func(self):
        self.set_state_colour(WidgetState.PRESS)
    
    def up_func(self):
        self.set_state_colour(WidgetState.DEFAULT)
    
    def hover_func(self):
        self.set_state_colour(WidgetState.HOVER)