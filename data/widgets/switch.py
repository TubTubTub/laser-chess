import pygame
from data.widgets.bases import _Widget, _Pressable
from data.constants import WidgetState
from data.utils.widget_helpers import create_switch

class Switch(_Pressable, _Widget):
    def __init__(self, relative_position, relative_length, colour, event, surface=None):
        _Pressable.__init__(
            self,
            event=event,
            hover_func=lambda: self.set_state_colour(WidgetState.HOVER),
            down_func=lambda: self.set_state_colour(WidgetState.PRESS),
            up_func=self.up_func,
        )
        _Widget.__init__(self, surface)

        self._relative_position = relative_position
        self._relative_size = (relative_length, relative_length * 0.5)

        self._is_toggled_on = False

        self._fill_colour = colour
        self._background_colour = colour
        self._thumb_colour = None
        self.initialise_new_colours((255, 255, 255))
        self.set_toggle_state(False)

        self.set_image()
        self.set_geometry()
    
    @property
    def _size(self):
        return (self._relative_size[0] * self._surface_size[1], self._relative_size[1] * self._surface_size[1])
    
    @property
    def _position(self):
        return (self._relative_position[0] * self._surface_size[0], self._relative_position[1] * self._surface_size[1])
    
    def set_toggle_state(self, state):
        self._is_toggled_on = state
        if state:
            self._fill_colour = self._background_colour
        else:
            self._fill_colour = (50, 50, 50)

        self.set_image()

    def initialise_new_colours(self, new_colour):
        r, g, b = pygame.Color(new_colour).rgb

        self._colours = {
            WidgetState.BASE: new_colour,
            WidgetState.HOVER: (max(r - 25, 0), max(g - 25, 0), max(b - 25, 0)),
            WidgetState.PRESS: (max(r - 50, 0), max(g - 50, 0), max(b - 50, 0))
        }

        self.set_state_colour(WidgetState.BASE)
    
    def set_state_colour(self, state):
        self._thumb_colour = self._colours[state]

        self.set_image()
    
    def up_func(self):
        if self.get_widget_state() == WidgetState.PRESS:
            toggle_state = not(self._is_toggled_on)
            self.set_toggle_state(toggle_state)
        self.set_state_colour(WidgetState.BASE)
    
    def draw_thumb(self):
        margin = self._size[1] * 0.1
        thumb_radius = (self._size[1] / 2) - margin

        if self._is_toggled_on:
            thumb_center = (self._size[0] - margin - thumb_radius, self._size[1] / 2)
        else:
            thumb_center = (margin + thumb_radius, self._size[1] / 2)
        
        pygame.draw.circle(self.image, self._thumb_colour, thumb_center, thumb_radius)

    def set_image(self):
        self.image = create_switch(self._size, self._fill_colour)
        self.draw_thumb()
    
    def set_geometry(self):
        self.rect = self.image.get_rect()
        self.rect.topleft = self._position

    def set_surface_size(self, new_surface_size):
        self._surface_size = new_surface_size