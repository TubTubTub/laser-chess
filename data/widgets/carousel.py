import pygame
from data.widgets.bases import _Widget
from data.widgets.icon_button import IconButton
from data.components.circular_linked_list import CircularLinkedList
from data.assets import GRAPHICS
from data.constants import MiscellaneousEventType
from data.components.custom_event import CustomEvent

class Carousel(_Widget):
    def __init__(self, relative_position, event_type, widgets_dict, margin=10):
        super().__init__()
        self._screen = pygame.display.get_surface()
        self._screen_size = self._screen.get_size()

        self._widgets_dict = widgets_dict
        self._widgets = CircularLinkedList(list(self._widgets_dict.keys()))
        self._widget_key = self._widgets.get_head()
        self._widget = self._widgets_dict[self._widget_key.data]

        max_widget_size = (0, 0)
        for widget in self._widgets_dict.values():
            max_widget_size = (max(max_widget_size[0], widget.rect.width), max(max_widget_size[1], widget.rect.height))

        self._relative_max_widget_size = (max_widget_size[0] / self._screen_size[1], max_widget_size[1] / self._screen_size[1])
        self._relative_position = relative_position
        self._relative_margin = margin / self._screen_size[1]
        self._relative_size = ((max_widget_size[0] + 2 * (self._margin + self._arrow_size[0])) / self._screen_size[1], (max_widget_size[1]) / self._screen_size[1])

        self._left_arrow = IconButton(MiscellaneousEventType.PLACEHOLDER, relative_position=(0, 0), size=self._arrow_size, icon=GRAPHICS['left_arrow'], margin=0, border_radius=0, is_mask=True, fill_colour=(255, 0, 0))
        self._right_arrow = IconButton(MiscellaneousEventType.PLACEHOLDER, relative_position=(0, 0), size=self._arrow_size, icon=GRAPHICS['right_arrow'], margin=0, border_radius=0, is_mask=True, fill_colour=(255, 0, 0))

        self._event_type = event_type

        self._empty_surface = pygame.Surface((0, 0))

        self.set_image()
        self.set_geometry()
    
    @property
    def _position(self):
        return (self._relative_position[0] * self._screen_size[0], self._relative_position[1] * self._screen_size[1])

    @property
    def _max_widget_size(self):
        return (self._relative_max_widget_size[0] * self._screen_size[1], self._relative_max_widget_size[1] * self._screen_size[1])
    
    @property
    def _size(self):
        return ((self._arrow_size[0] + self._margin) * 2 + self._max_widget_size[0], self._max_widget_size[1])

    @property
    def _arrow_size(self):
        return (self._max_widget_size[1] / 2, self._max_widget_size[1] / 2)
    
    @property
    def _margin(self):
        return self._relative_margin * self._screen_size[1]

    @property
    def _left_arrow_position(self):
        return (0, (self._size[1] - self._arrow_size[1]) / 2)
    
    @property
    def _right_arrow_position(self):
        return (self._size[0] - self._arrow_size[0], (self._size[1] - self._arrow_size[1]) / 2)
    
    def set_image(self):
        self.image = pygame.transform.scale(self._empty_surface, self._size)
        self.image.fill((200, 200, 200))

        self._left_arrow.set_image()
        self.image.blit(self._left_arrow.image, self._left_arrow_position)

        self._widget.set_image()
        self.image.blit(self._widget.image, ((self._size[0] - self._widget.rect.size[0]) / 2, (self._size[1] - self._widget.rect.size[1]) / 2))

        self._right_arrow.set_image()
        self.image.blit(self._right_arrow.image, self._right_arrow_position)
    
    def set_geometry(self):
        self.rect = self.image.get_rect()
        self.rect.topleft = self._position

        self._widget.set_geometry()
        self._left_arrow.set_geometry()
        self._right_arrow.set_geometry()

        self._widget.rect.center = self.rect.center
        self._left_arrow.rect.topleft = (self._position[0] + self._left_arrow_position[0], self._position[1] + self._left_arrow_position[1])
        self._right_arrow.rect.topleft = (self._position[0] + self._right_arrow_position[0], self._position[1] + self._right_arrow_position[1])
    
    def set_screen_size(self, new_screen_size):
        self._screen_size = new_screen_size
        self._widget.set_screen_size(new_screen_size)
        self._left_arrow.set_screen_size(new_screen_size)
        self._right_arrow.set_screen_size(new_screen_size)
    
    def process_event(self, event):
        self._widget.process_event(event)
        left_arrow_event = self._left_arrow.process_event(event)
        right_arrow_event = self._right_arrow.process_event(event)

        if left_arrow_event:
            self._widget_key = self._widget_key.previous
            self._widget = self._widgets_dict[self._widget_key.data]

            self.set_geometry()
            self.set_image()
            return CustomEvent(self._event_type, data=self._widget_key.data)

        elif right_arrow_event:
            self._widget_key = self._widget_key.next
            self._widget = self._widgets_dict[self._widget_key.data]

            self.set_geometry()
            self.set_image()
            return CustomEvent(self._event_type, data=self._widget_key.data)
        
        elif event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION] and self.rect.collidepoint(event.pos):
            self.set_image()