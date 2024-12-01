import pygame
from data.widgets.bases import _Pressable
from data.widgets.text import Text
from data.constants import WidgetState

class TextButton(_Pressable, Text):
    def __init__(self, event, **kwargs):
        _Pressable.__init__(
            self,
            event=event,
            hover_func=lambda: self.set_state_colour(WidgetState.HOVER),
            down_func=lambda: self.set_state_colour(WidgetState.PRESS),
            up_func=lambda: self.set_state_colour(WidgetState.BASE),
        )
        Text.__init__(self, **kwargs)

        if self._fill_colour:
            self.initialise_new_colours(pygame.Color(self._fill_colour))
    
    def update_relative_position(self, new_relative_position):
        self._relative_position = new_relative_position
        self.set_image()
        self.set_geometry()
            
    def initialise_new_colours(self, new_colour):
        r, g, b, a = new_colour.rgba

        self._colours = {
            WidgetState.BASE: new_colour,
            WidgetState.HOVER: pygame.Color(max(r - 25, 0), max(g - 25, 0), max(b - 25, 0), a),
            WidgetState.PRESS: pygame.Color(max(r - 50, 0), max(g - 50, 0), max(b - 50, 0), a)
        }
    
    def set_state_colour(self, state):
        if self._fill_colour is None:
            return
        
        self._fill_colour = self._colours[state]

        self.set_image()