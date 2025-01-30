import pygame
from data.widgets.bases import _Widget, _Pressable
from data.components.circular_linked_list import CircularLinkedList
from data.components.custom_event import CustomEvent
from data.constants import WidgetState

class ReactiveButton(_Pressable, _Widget):
    def __init__(self, widgets_dict, event, center=False, **kwargs):
        _Pressable.__init__(
            self,
            event=event,
            hover_func=lambda: self.set_to_key(WidgetState.HOVER),
            down_func=lambda: self.set_to_key(WidgetState.PRESS),
            up_func=lambda: self.set_to_key(WidgetState.BASE),
        )

        _Widget.__init__(self, **kwargs)

        self._widgets_dict = widgets_dict
        self._widgets_list = CircularLinkedList(list(self._widgets_dict.keys()))
        self._widget_key = self._widgets_list.get_head()
        self._widget = self._widgets_dict[self._widget_key.data]

        self._center = center
        
        self.initialise_new_colours(self._fill_colour)
    
    @property
    def position(self):
        position = super().position

        if self._center:
            self._size_diff = (self.size[0] - self.rect.width, self.size[1] - self.rect.height)
            return (position[0] + self._size_diff[0] / 2, position[1] + self._size_diff[1] / 2)
        else:
            return position
    
    def set_widget(self, widget_key):
        self._widget_key = widget_key
        self._widget = self._widgets_dict[self._widget_key.data]
        self._widget.set_surface_size(self._raw_surface_size)
    
    def set_next_widget(self):
        self.set_widget(self._widget_key.next)
        self.set_image()
    
    def set_previous_widget(self):
        self.set_widget(self._widget_key.previous)
        self.set_image()

    def set_to_key(self, key):
        if self._widgets_list.data_in_list(key) is False:
            raise ValueError('(ReactiveButton.set_to_key) Key not found!', key)
        
        for _ in range(len(self._widgets_dict)):
            if self._widget_key.data == key:
                self.set_image()
                self.set_geometry()
                return

            self.set_next_widget()
    
    def set_image(self):
        self._widget.set_image()
        self.image = self._widget.image
    
    def set_geometry(self):
        super().set_geometry()
        self._widget.set_geometry()
        self._widget.rect.topleft = self.rect.topleft

    def set_surface_size(self, new_surface_size):
        super().set_surface_size(new_surface_size)
        self._widget.set_surface_size(new_surface_size)
        
    def process_event(self, event):
        widget_event = super().process_event(event)
        self._widget.process_event(event)

        if widget_event:
            return CustomEvent(**vars(widget_event), data=self._widget_key.data)