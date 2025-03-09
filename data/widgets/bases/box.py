from data.utils.constants import WidgetState

class _Box:
    def __init__(self, box_colours):
        self._box_colours_dict = box_colours
        self._box_colours = self._box_colours_dict[WidgetState.BASE]

    def set_state_colour(self, state):
        self._box_colours = self._box_colours_dict[state]
        super().set_state_colour(state)