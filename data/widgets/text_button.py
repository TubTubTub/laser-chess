import pygame
from data.widgets.bases import _Pressable, _Box
from data.widgets.text import Text
from data.constants import WidgetState, BLUE_BUTTON_COLOURS

class TextButton(_Box, _Pressable, Text):
    def __init__(self, event, **kwargs):
        _Box.__init__(self, box_colours=BLUE_BUTTON_COLOURS)
        _Pressable.__init__(
            self,
            event=event,
            hover_func=lambda: self.set_state_colour(WidgetState.HOVER),
            down_func=lambda: self.set_state_colour(WidgetState.PRESS),
            up_func=lambda: self.set_state_colour(WidgetState.BASE),
        )
        Text.__init__(self, box_colours=BLUE_BUTTON_COLOURS[WidgetState.BASE], **kwargs)
        
        self.initialise_new_colours(self._fill_colour)
        self.set_state_colour(WidgetState.BASE)
    
    def update_relative_position(self, new_relative_position):
        self._relative_position = new_relative_position
        self.set_image()
        self.set_geometry()