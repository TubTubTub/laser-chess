from data.widgets.bases.pressable import _Pressable
from data.constants import WidgetState
from data.utils.widget_helpers import create_slider_thumb
from data.managers.theme import theme

class _SliderThumb(_Pressable):
    def __init__(self, radius, border_colour=theme['borderPrimary'], fill_colour=theme['fillPrimary']):
        super().__init__(
            event=None,
            down_func=self.down_func,
            up_func=self.up_func,
            hover_func=self.hover_func,
            prolonged=True,
            sfx=None
        )
        self._border_colour = border_colour
        self._radius = radius
        self._percent = None

        self.state = WidgetState.BASE
        self.initialise_new_colours(fill_colour)
    
    def get_position(self):
        return (self.rect.x, self.rect.y)
    
    def set_position(self, position):
        self.rect = self._thumb_surface.get_rect()
        self.rect.topleft = position

    def get_surface(self):
        return self._thumb_surface
    
    def set_surface(self, radius, border_width):
        self._thumb_surface = create_slider_thumb(radius, self._colours[self.state], self._border_colour, border_width)
    
    def get_pressed(self):
        return self._pressed
    
    def down_func(self):
        self.state = WidgetState.PRESS
    
    def up_func(self):
        self.state = WidgetState.BASE
    
    def hover_func(self):
        self.state = WidgetState.HOVER