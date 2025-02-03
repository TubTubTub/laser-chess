import pygame
from data.widgets.bases.widget import _Widget
from data.widgets.bases.circular import _Circular
from data.widgets.reactive_icon_button import ReactiveIconButton
from data.components.circular_linked_list import CircularLinkedList
from data.assets import GRAPHICS
from data.constants import Miscellaneous
from data.components.custom_event import CustomEvent

class Carousel(_Circular, _Widget):
    def __init__(self, event, widgets_dict, **kwargs):
        _Circular.__init__(self, items_dict=widgets_dict)
        _Widget.__init__(self, relative_size=None, **kwargs)

        max_widget_size = (
            max([widget.rect.width for widget in widgets_dict.values()]),
            max([widget.rect.height for widget in widgets_dict.values()])
        )

        self._relative_max_widget_size = (max_widget_size[0] / self.surface_size[1], max_widget_size[1] / self.surface_size[1])
        self._relative_size = ((max_widget_size[0] + 2 * (self.margin + self.arrow_size[0])) / self.surface_size[1], (max_widget_size[1]) / self.surface_size[1])
        
        self._left_arrow = ReactiveIconButton(
            relative_position=(0, 0),
            relative_size=(0, self.arrow_size[1] / self.surface_size[1]),
            base_icon=GRAPHICS['left_arrow_base'],
            hover_icon=GRAPHICS['left_arrow_hover'],
            press_icon=GRAPHICS['left_arrow_press'],
            scale_mode='height',
            event=CustomEvent(Miscellaneous.PLACEHOLDER),
        )
        self._right_arrow = ReactiveIconButton(
            relative_position=(0, 0),
            relative_size=(0, self.arrow_size[1] / self.surface_size[1]),
            base_icon=GRAPHICS['right_arrow_base'],
            hover_icon=GRAPHICS['right_arrow_hover'],
            press_icon=GRAPHICS['right_arrow_press'],
            scale_mode='height',
            event=CustomEvent(Miscellaneous.PLACEHOLDER),
        )

        self._event = event
        self._empty_surface = pygame.Surface((0, 0), pygame.SRCALPHA)

        self.set_image()
        self.set_geometry()

    @property
    def max_widget_size(self):
        return (self._relative_max_widget_size[0] * self.surface_size[1], self._relative_max_widget_size[1] * self.surface_size[1])

    @property
    def arrow_size(self):
        height = self.max_widget_size[1] * 0.75
        width = (GRAPHICS['left_arrow_base'].width / GRAPHICS['left_arrow_base'].height) * height
        return (width, height)
    
    @property
    def size(self):
        return ((self.arrow_size[0] + self.margin) * 2 + self.max_widget_size[0], self.max_widget_size[1])
    
    @property
    def left_arrow_position(self):
        return (0, (self.size[1] - self.arrow_size[1]) / 2)
    
    @property
    def right_arrow_position(self):
        return (self.size[0] - self.arrow_size[0], (self.size[1] - self.arrow_size[1]) / 2)
    
    def set_image(self):
        self.image = pygame.transform.scale(self._empty_surface, self.size)
        self.image.fill(self._fill_colour)

        if self.border_width:
            pygame.draw.rect(self.image, self._border_colour, (0, 0, *self.size), width=int(self.border_width), border_radius=int(self.border_radius))

        self._left_arrow.set_image()
        self.image.blit(self._left_arrow.image, self.left_arrow_position)

        self.current_item.set_image()
        self.image.blit(self.current_item.image, ((self.size[0] - self.current_item.rect.size[0]) / 2, (self.size[1] - self.current_item.rect.size[1]) / 2))

        self._right_arrow.set_image()
        self.image.blit(self._right_arrow.image, self.right_arrow_position)
    
    def set_geometry(self):
        super().set_geometry()
    
        self.current_item.set_geometry()
        self._left_arrow.set_geometry()
        self._right_arrow.set_geometry()

        self.current_item.rect.center = self.rect.center
        self._left_arrow.rect.topleft = (self.position[0] + self.left_arrow_position[0], self.position[1] + self.left_arrow_position[1])
        self._right_arrow.rect.topleft = (self.position[0] + self.right_arrow_position[0], self.position[1] + self.right_arrow_position[1])
    
    def set_surface_size(self, new_surface_size):
        super().set_surface_size(new_surface_size)
        self._left_arrow.set_surface_size(new_surface_size)
        self._right_arrow.set_surface_size(new_surface_size)

        for item in self._items_dict.values():
            item.set_surface_size(new_surface_size)
    
    def process_event(self, event):
        self.current_item.process_event(event)
        left_arrow_event = self._left_arrow.process_event(event)
        right_arrow_event = self._right_arrow.process_event(event)
        
        if left_arrow_event:
            self.set_previous_item()
            self.current_item.set_surface_size(self._raw_surface_size)

        elif right_arrow_event:
            self.set_next_item()
            self.current_item.set_surface_size(self._raw_surface_size)

        if left_arrow_event or right_arrow_event:
            self.set_image()
            self.set_geometry()

            return CustomEvent(**vars(self._event), data=self.current_key)
        
        elif event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]:
            self.set_image()
            self.set_geometry()