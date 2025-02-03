import pygame
from data.widgets.bases.pressable import _Pressable
from data.widgets.board_thumbnail import BoardThumbnail
from data.constants import WidgetState
from data.components.custom_event import CustomEvent

class BoardThumbnailButton(_Pressable, BoardThumbnail):
    def __init__(self, event, **kwargs):
        _Pressable.__init__(
            self,
            event=CustomEvent(**vars(event), fen_string=kwargs.get('fen_string')),
            hover_func=lambda: self.set_state_colour(WidgetState.HOVER),
            down_func=lambda: self.set_state_colour(WidgetState.PRESS),
            up_func=lambda: self.set_state_colour(WidgetState.BASE),
        )
        BoardThumbnail.__init__(self, **kwargs)
        
        self.initialise_new_colours(self._fill_colour)
        self.set_state_colour(WidgetState.BASE)