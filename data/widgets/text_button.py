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
        
        self.initialise_new_colours(self._fill_colour)
        self.set_state_colour(WidgetState.BASE)
    
    def update_relative_position(self, new_relative_position):
        self._relative_position = new_relative_position
        self.set_image()
        self.set_geometry()