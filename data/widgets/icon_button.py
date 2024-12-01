import pygame
from data.widgets.bases import _Pressable
from data.widgets.icon import Icon
from data.constants import WidgetState

class IconButton(_Pressable, Icon):
    def __init__(self, event, **kwargs):
        _Pressable.__init__(
            self,
            event=event,
            hover_func=lambda: self.set_state_colour(WidgetState.HOVER),
            down_func=lambda: self.set_state_colour(WidgetState.PRESS),
            up_func=self.up_func,
        )
        Icon.__init__(self, **kwargs)

        self.initialise_new_colours(self._fill_colour)
    
    def up_func(self):
        self.set_state_colour(WidgetState.BASE)

    def initialise_new_colours(self, new_colour):
        r, g, b, a = new_colour

        self._colours = {
            WidgetState.BASE: new_colour,
            WidgetState.HOVER: pygame.Color(max(r - 25, 0), max(g - 25, 0), max(b - 25, 0), a),
            WidgetState.PRESS: pygame.Color(max(r - 50, 0), max(g - 50, 0), max(b - 50, 0), a)
        }
    
    def set_state_colour(self, state):
        self._fill_colour = self._colours[state]

        self.set_image()