import pygame
from data.widgets.bases.widget import _Widget
from data.widgets.bases.pressable import _Pressable
from data.constants import WidgetState
from data.utils.widget_helpers import create_switch
from data.components.custom_event import CustomEvent
from data.managers.theme import theme

class Switch(_Pressable, _Widget):
    def __init__(self, relative_height, event, fill_colour=theme['fillTertiary'], on_colour=theme['fillSecondary'], off_colour=theme['fillPrimary'], **kwargs):
        _Pressable.__init__(
            self,
            event=event,
            hover_func=self.hover_func,
            down_func=lambda: self.set_state_colour(WidgetState.PRESS),
            up_func=self.up_func,
        )
        _Widget.__init__(self, relative_size=(relative_height * 2, relative_height), scale_mode='height',fill_colour=fill_colour, **kwargs)

        self._on_colour = on_colour
        self._off_colour = off_colour
        self._background_colour = None

        self._is_toggled = None
        self.set_toggle_state(False)
        
        self.initialise_new_colours(self._fill_colour)
        self.set_state_colour(WidgetState.BASE)

        self.set_image()
        self.set_geometry()
    
    def hover_func(self):
        self.set_state_colour(WidgetState.HOVER)
    
    def set_toggle_state(self, is_toggled):
        self._is_toggled = is_toggled
        if is_toggled:
            self._background_colour = self._on_colour
        else:
            self._background_colour = self._off_colour

        self.set_image()
    
    def up_func(self):
        if self.get_widget_state() == WidgetState.PRESS:
            toggle_state = not(self._is_toggled)
            self.set_toggle_state(toggle_state)

        self.set_state_colour(WidgetState.BASE)
    
    def draw_thumb(self):
        margin = self.size[1] * 0.1
        thumb_radius = (self.size[1] / 2) - margin

        if self._is_toggled:
            thumb_center = (self.size[0] - margin - thumb_radius, self.size[1] / 2)
        else:
            thumb_center = (margin + thumb_radius, self.size[1] / 2)
        
        pygame.draw.circle(self.image, self._fill_colour, thumb_center, thumb_radius)

    def set_image(self):
        self.image = create_switch(self.size, self._background_colour)
        self.draw_thumb()
    
    def process_event(self, event):
        data = super().process_event(event)

        if data:
            return CustomEvent(**vars(data), toggled=self._is_toggled)