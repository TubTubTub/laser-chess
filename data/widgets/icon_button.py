from data.widgets.bases.pressable import _Pressable
from data.widgets.bases.box import _Box
from data.widgets.icon import Icon
from data.utils.constants import WidgetState, RED_BUTTON_COLOURS

class IconButton(_Box, _Pressable, Icon):
    def __init__(self, event, box_colours=RED_BUTTON_COLOURS, **kwargs):
        _Box.__init__(self, box_colours=box_colours)
        _Pressable.__init__(
            self,
            event=event,
            hover_func=lambda: self.set_state_colour(WidgetState.HOVER),
            down_func=lambda: self.set_state_colour(WidgetState.PRESS),
            up_func=lambda: self.set_state_colour(WidgetState.BASE),
        )
        Icon.__init__(self, box_colours=box_colours[WidgetState.BASE], **kwargs)

        self.initialise_new_colours(self._fill_colour)
        self.set_state_colour(WidgetState.BASE)