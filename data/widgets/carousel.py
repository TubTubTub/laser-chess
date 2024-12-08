import pygame
from data.widgets.bases import _Widget
from data.widgets.icon_button import IconButton
from data.components.circular_linked_list import CircularLinkedList
from data.assets import GRAPHICS
from data.constants import Miscellaneous
from data.components.custom_event import CustomEvent

class Carousel(_Widget):
    def __init__(self, event_type, widgets_dict, **kwargs):
        super().__init__(relative_size=None, **kwargs)

        self._widgets_dict = widgets_dict
        self._widgets = CircularLinkedList(list(self._widgets_dict.keys()))
        self._widget_key = self._widgets.get_head()
        self._widget = self._widgets_dict[self._widget_key.data]

        max_widget_size = (0, 0)
        for widget in self._widgets_dict.values():
            max_widget_size = (max(max_widget_size[0], widget.rect.width), max(max_widget_size[1], widget.rect.height))

        self._relative_max_widget_size = (max_widget_size[0] / self.surface_size[1], max_widget_size[1] / self.surface_size[1])
        self._relative_size = ((max_widget_size[0] + 2 * (self.margin + self.arrow_length)) / self.surface_size[1], (max_widget_size[1]) / self.surface_size[1])
        self._left_arrow = IconButton(
            event=Miscellaneous.PLACEHOLDER,
            relative_position=(0, 0),
            relative_size=(self.arrow_length / self.surface_size[1], self.arrow_length / self.surface_size[1]),
            icon=GRAPHICS['left_arrow'],
            scale_with_height=True,
            margin=0,
            border_radius=0,
            border_width=self.border_width,
            is_mask=True,
            fill_colour=(255, 0, 0)
        )
        self._right_arrow = IconButton(
            event=Miscellaneous.PLACEHOLDER,
            relative_position=(0, 0),
            relative_size=(self.arrow_length / self.surface_size[1], self.arrow_length / self.surface_size[1]),
            icon=GRAPHICS['right_arrow'],
            scale_with_height=True,
            margin=0,
            border_radius=0,
            border_width=self.border_width,
            is_mask=True,
            fill_colour=(255, 0, 0)
        )

        self._event_type = event_type

        self._empty_surface = pygame.Surface((0, 0), pygame.SRCALPHA)

        self.set_image()
        self.set_geometry()

    @property
    def max_widget_size(self):
        return (self._relative_max_widget_size[0] * self.surface_size[1], self._relative_max_widget_size[1] * self.surface_size[1])
    
    @property
    def size(self):
        return ((self.arrow_length + self.margin) * 2 + self.max_widget_size[0], self.max_widget_size[1])

    @property
    def arrow_length(self):
        return self.max_widget_size[1] / 2

    @property
    def left_arrow_position(self):
        return (0, (self.size[1] - self.arrow_length) / 2)
    
    @property
    def right_arrow_position(self):
        return (self.size[0] - self.arrow_length, (self.size[1] - self.arrow_length) / 2)

    def set_to_key(self, key):
        for i in range(len(self._widgets_dict)):
            if self._widget_key.data == key:
                return
        
            self._widget_key = self._widget_key.next
            self._widget = self._widgets_dict[self._widget_key.data]
        
        raise ValueError('(Carousel.set_to_key) Key not found!', key)
    
    def set_image(self):
        self.image = pygame.transform.scale(self._empty_surface, self.size)
        self.image.fill(self._fill_colour)

        self._left_arrow.set_image()
        self.image.blit(self._left_arrow.image, self.left_arrow_position)

        self._widget.set_image()
        self.image.blit(self._widget.image, ((self.size[0] - self._widget.rect.size[0]) / 2, (self.size[1] - self._widget.rect.size[1]) / 2))

        self._right_arrow.set_image()
        self.image.blit(self._right_arrow.image, self.right_arrow_position)
    
    def set_geometry(self):
        super().set_geometry()

        self._widget.set_geometry()
        self._left_arrow.set_geometry()
        self._right_arrow.set_geometry()

        self._widget.rect.center = self.rect.center
        self._left_arrow.rect.topleft = (self.position[0] + self.left_arrow_position[0], self.position[1] + self.left_arrow_position[1])
        self._right_arrow.rect.topleft = (self.position[0] + self.right_arrow_position[0], self.position[1] + self.right_arrow_position[1])
    
    def set_surface_size(self, new_surface_size):
        super().set_surface_size(new_surface_size)
        self._widget.set_surface_size(new_surface_size)
        self._left_arrow.set_surface_size(new_surface_size)
        self._right_arrow.set_surface_size(new_surface_size)
    
    def process_event(self, event):
        self._widget.process_event(event)
        left_arrow_event = self._left_arrow.process_event(event)
        right_arrow_event = self._right_arrow.process_event(event)

        if left_arrow_event:
            self._widget_key = self._widget_key.previous
            self._widget = self._widgets_dict[self._widget_key.data]

            self.set_image()
            self.set_geometry()
            return CustomEvent(self._event_type, data=self._widget_key.data)

        elif right_arrow_event:
            self._widget_key = self._widget_key.next
            self._widget = self._widgets_dict[self._widget_key.data]

            self.set_image()
            self.set_geometry()
            return CustomEvent(self._event_type, data=self._widget_key.data)
        
        elif event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION] and self.rect.collidepoint(event.pos):
            self.set_image()