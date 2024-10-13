from data.components.widgets.bases import _Widget, _Pressable
from data.components.widgets.text import Text
from data.constants import WidgetState

class Button(_Pressable, Text):
    def __init__(self, shadow_distance=0, shadow_colour=(0, 0, 0), event=None, **kwargs):
        _Pressable.__init__(
            self,
            hover_func=lambda: self.set_state_colour(WidgetState.HOVER),
            down_func=lambda: self.set_state_colour(WidgetState.PRESS),
            up_func=lambda: self.set_state_colour(WidgetState.DEFAULT),
        )
        Text.__init__(self, **kwargs)

        self._shadow_distance = shadow_distance
        self._shadow_colour = shadow_colour
        self._event = event

        if self._fill_colour:
            r, g, b = self._fill_colour
            self._hover_colour = (max(r - 25, 0), max(g - 25, 0), max(b - 25, 0))
            self._press_colour = (max(r - 50, 0), max(g - 50, 0), max(b - 50, 0))
            self._fill_colour_copy = self._fill_colour
    
    def set_state_colour(self, state):
        if self._fill_colour is None:
            return

        match state:
            case WidgetState.DEFAULT:
                self._fill_colour = self._fill_colour_copy
            case WidgetState.HOVER:
                self._fill_colour = self._hover_colour
            case WidgetState.PRESS:
                self._fill_colour = self._press_colour

        self.set_image()