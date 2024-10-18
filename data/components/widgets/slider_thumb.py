import pygame
from data.components.widgets.bases import _Pressable
from data.constants import WidgetState
from data.utils.widget_helpers import create_slider_thumb

class SliderThumb(_Pressable):
    def __init__(self, radius, border_colour=(255, 255, 255)):
        super().__init__(
            event=None,
            down_func=lambda: self.down_func(),
            up_func=lambda: self.up_func(),
            hover_func=lambda: self.hover_func(),
            prolonged=True
        )

        self._screen = pygame.display.get_surface()
        self._border_colour  = border_colour
        self._radius = radius
        self._percent = None

        self.state = WidgetState.BASE

        self._colours = {
            WidgetState.BASE: None,
            WidgetState.HOVER: None,
            WidgetState.PRESS: None
        }
    
    def initialise_new_colours(self, new_colour):
        new_colour = new_colour.rgb

        r, g, b = new_colour

        self._colours = {
            WidgetState.BASE: new_colour,
            WidgetState.HOVER: (max(r - 25, 0), max(g - 25, 0), max(b - 25, 0)),
            WidgetState.PRESS: (max(r - 50, 0), max(g - 50, 0), max(b - 50, 0))
        }
    
    def get_position(self):
        return (self.rect.x, self.rect.y)
    
    def set_position(self, position):
        self.rect = self._thumb_surface.get_rect()
        self.rect.topleft = position

    def get_surface(self):
        return self._thumb_surface
    
    def set_surface(self, radius, border_width):
        self._thumb_surface = create_slider_thumb(radius, self._colours[self.state], self._border_colour, border_width)
    
    def get_pressed(self):
        return self._pressed
    
    def down_func(self):
        self.state = WidgetState.PRESS
        # print('down')
    
    def up_func(self):
        self.state = WidgetState.BASE
        # print('up')
    
    def hover_func(self):
        self.state = WidgetState.HOVER