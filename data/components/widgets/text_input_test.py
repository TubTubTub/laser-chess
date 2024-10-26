import pygame
from data.components.widgets.text import Text
from data.components.widgets.bases import _Pressable
from data.constants import WidgetState

class TextInput(_Pressable, Text):
    def __init__(self, relative_size, **kwargs):
        _Pressable.__init__(
            self,
            event=None,
            hover_func=self.hover_func,
            down_func=self.down_func,
            up_func=self.up_func,
        )
        font_size = self.calculate_font_size(relative_size)
        Text.__init__(self, text="", font_size=font_size, **kwargs)
        self.initialise_new_colours(self._fill_colour)
    
    def calculate_font_size(self, relative_size):
        return 30
            
    def initialise_new_colours(self, new_colour):
        r, g, b, a = pygame.Color(new_colour).rgba

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

    def hover_func(self):
        self.set_state_colour(WidgetState.HOVER)
    def down_func(self):
        self.set_state_colour(WidgetState.PRESS)
    def up_func(self):
        self.set_state_colour(WidgetState.BASE)