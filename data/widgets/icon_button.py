import pygame
from data.widgets.bases import _Pressable, _Box
from data.widgets.icon import Icon
from data.constants import WidgetState, RED_BUTTON_COLOURS

class IconButton(_Box, _Pressable, Icon):
    def __init__(self, event, **kwargs):
        _Box.__init__(self, box_colours=RED_BUTTON_COLOURS)
        _Pressable.__init__(
            self,
            event=event,
            hover_func=lambda: self.set_state_colour(WidgetState.HOVER),
            down_func=lambda: self.set_state_colour(WidgetState.PRESS),
            up_func=lambda: self.set_state_colour(WidgetState.BASE),
        )
        Icon.__init__(self, box_colours=RED_BUTTON_COLOURS[WidgetState.BASE], **kwargs)
        
        self.initialise_new_colours(self._fill_colour)
        self.set_state_colour(WidgetState.BASE)
    
    def process_event(self, event):
        return super().process_event(event)