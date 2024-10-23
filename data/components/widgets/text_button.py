from data.components.widgets.bases import _Pressable
from data.components.widgets.text import Text
from data.constants import WidgetState

class TextButton(_Pressable, Text):
    def __init__(self, shadow_distance=0, shadow_colour=(0, 0, 0), event=None, **kwargs):
        _Pressable.__init__(
            self,
            event=event,
            hover_func=lambda: self.set_state_colour(WidgetState.HOVER),
            down_func=lambda: self.set_state_colour(WidgetState.PRESS),
            up_func=lambda: self.set_state_colour(WidgetState.BASE),
        )
        Text.__init__(self, **kwargs)

        self._shadow_distance = shadow_distance
        self._shadow_colour = shadow_colour

        if self._fill_colour:
            self.initialise_new_colours(self._fill_colour)
            
    def initialise_new_colours(self, new_colour):
        r, g, b = new_colour

        self._colours = {
            WidgetState.BASE: new_colour,
            WidgetState.HOVER: (max(r - 25, 0), max(g - 25, 0), max(b - 25, 0)),
            WidgetState.PRESS: (max(r - 50, 0), max(g - 50, 0), max(b - 50, 0))
        }
    
    def set_state_colour(self, state):
        if self._fill_colour is None:
            return
        
        self._fill_colour = self._colours[state]

        self.set_image()