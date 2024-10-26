import pygame
from data.components.widgets.bases import _Pressable
from data.constants import WidgetState

class TextInput(_Pressable):
    def __init__(self, relative_position, relative_size, text_colour=(0, 0, 0), fill_colour=(100, 100, 100), border_width=10, border_colour=(255, 255, 255)):
        super(
            self,
            event=None,
            hover_func=self.hover_func,
            down_func=self.down_func,
            up_func=self.up_func,
        )

        self._screen = pygame.display.get_surface()
        self._screen_size = self._screen.get_size()

        self._relative_position = relative_position
        self._relative_size = relative_size
        self._relative_border_width = border_width / self._screen_size[1]

        self._text_colour = text_colour
        self._fill_colour = fill_colour
        self._border_colour = border_colour
    
    @property
    def _size(self):
        return (self._relative_size[0] * self._screen_size[1], self._relative_size[1] * self._screen_size[1])
    
    @property
    def _position(self):
        return (self._relative_position[0] * self._screen_size[0], self._relative_position[1] * self._screen_size[1])
            
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
    def hover_func(self):
        self.set_state_colour(WidgetState.HOVER)
    def down_func(self):
        self.set_state_colour(WidgetState.PRESS)
    def up_func(self):
        self.set_state_colour(WidgetState.BASE)