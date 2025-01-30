import pygame
from data.widgets.icon_button import IconButton
from data.components.circular_linked_list import CircularLinkedList
from data.components.custom_event import CustomEvent
from data.constants import WidgetState

class MultipleIconButton(IconButton):
    def __init__(self, icons_dict, **kwargs):
        self._icons_dict = icons_dict
        self._icons_list = CircularLinkedList(list(self._icons_dict.keys()))
        self._icon = self._icons_dict[self.current_key]

        super().__init__(icon=self._icon, **kwargs)

        self._fill_colour_copy = self._fill_colour
        
        self._locked = None
    
    @property
    def current_key(self):
        return self._icons_list.get_head().data
    
    def set_locked(self, is_locked):
        self._locked = is_locked
        if self._locked:
            r, g, b, a  = pygame.Color(self._fill_colour_copy).rgba
            self.initialise_new_colours((max(r + 50, 0), max(g + 50, 0), max(b + 50, 0), a))
        else:
            self.initialise_new_colours(self._fill_colour_copy)

        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.set_state_colour(WidgetState.HOVER)
        else:
            self.set_state_colour(WidgetState.BASE)
    
    def set_next_icon(self):
        self._icons_list.shift_head()
        self._icon = self._icons_dict[self.current_key]

        self.set_image()
        
    def process_event(self, event):
        widget_event = super().process_event(event)

        if widget_event:
            return CustomEvent(**vars(widget_event), data=self.current_key)