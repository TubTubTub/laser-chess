import pygame
from data.widgets.bases import _Widget
from data.widgets.scrollbar import _Scrollbar

SCROLLBAR_WIDTH_FACTOR =  0.05

class ScrollArea(_Widget):
    def __init__(self, widget, vertical, scroll_factor=5, **kwargs):
        super().__init__(**kwargs, scale_mode='both')
        
        self._relative_scroll_factor = scroll_factor / self.surface_size[1]

        self._scroll_percentage = 0
        self._widget = widget
        self._vertical = vertical

        self._widget.register_get_rect(self.calculate_widget_rect)

        anchor_x = 'right' if self._vertical else 'left'
        anchor_y = 'bottom' if not self._vertical else 'right'
        scale_mode = 'height' if self._vertical else 'width'
        self._scrollbar = _Scrollbar(
            parent=self,
            relative_position=(0, 0),
            relative_size=None,
            anchor_x=anchor_x,
            anchor_y=anchor_y,
            scale_mode=scale_mode,
            vertical=vertical,
        )
        
        self._empty_surface = pygame.Surface((0, 0), pygame.SRCALPHA)

        self.set_image()
        self.set_geometry()

    @property
    def size(self):
        if self._vertical:
            return (self._relative_size[0] * self.surface_size[1], self._relative_size[1] * self.surface_size[1])
        else:
            return (self._relative_size[0] * self.surface_size[0], self._relative_size[1] * self.surface_size[1])
    
    @property
    def scroll_factor(self):
        return self._relative_scroll_factor * self.surface_size[1]

    @property
    def scrollbar_size(self):
        if self._vertical:
            return (self.size[0] * SCROLLBAR_WIDTH_FACTOR, min(1, self.size[1] / self._widget.rect.height) * self.size[1])
        else:
            return (min(1, self.size[0] / (self._widget.rect.width + 0.001)) * self.size[0], self.size[1] * SCROLLBAR_WIDTH_FACTOR)

    def calculate_scroll_percentage(self, offset, scrollbar=False):
        if self._vertical:
            widget_height = self._widget.rect.height

            if widget_height < self.size[1]:
                return 0
            
            if scrollbar:
                self._scroll_percentage += offset / (self.size[1] - self.scrollbar_size[1] + 0.001)
            else:
                max_scroll_height = widget_height - self.size[1]
                current_scroll_height = self._scroll_percentage * max_scroll_height
                self._scroll_percentage = (current_scroll_height + offset) / (max_scroll_height + 0.001)
        else:
            widget_width = self._widget.rect.width

            if widget_width < self.size[0]:
                return 0

            if scrollbar:
                self._scroll_percentage += offset / (self.size[0] - self.scrollbar_size[0] + 0.001)
            else:
                max_scoll_width = widget_width - self.size[0]
                current_scroll_width = self._scroll_percentage * max_scoll_width
                self._scroll_percentage = (current_scroll_width + offset) / max_scoll_width

        return min(1, max(0, self._scroll_percentage))
    
    def calculate_widget_rect(self):
        widget_position = self.calculate_widget_position()
        return pygame.Rect(widget_position[0] - self.position[0], self.position[1] + widget_position[1], self.size[0], self.size[1])

    def calculate_widget_position(self):
        if self._vertical:
            return (0, -self._scroll_percentage * (self._widget.rect.height - self.size[1]))
        else:
            return (-self._scroll_percentage * (self._widget.rect.width - self.size[0]), 0)

    def calculate_relative_scrollbar_position(self):
        if self._vertical:
            vertical_offset = (self.size[1] - self.scrollbar_size[1]) * self._scroll_percentage
            scrollbar_position = (self.size[0] * SCROLLBAR_WIDTH_FACTOR, vertical_offset)
        else:
            horizontal_offset = (self.size[0] - self.scrollbar_size[0]) * self._scroll_percentage
            scrollbar_position = (horizontal_offset, self.size[1] * SCROLLBAR_WIDTH_FACTOR)

        return (scrollbar_position[0] / self.size[0], scrollbar_position[1] / self.size[1])
    
    def set_widget(self, new_widget):
        self._widget = new_widget
        self.set_image()
        self.set_geometry()
    
    def set_image(self):
        self.image = pygame.transform.scale(self._empty_surface, self.size)
        self.image.fill((100, 100, 100))

        self._widget.set_image()
        self.image.blit(self._widget.image, self.calculate_widget_position())

        self._scrollbar.set_relative_position(self.calculate_relative_scrollbar_position()) # WRONG USING RELATIVE
        self._scrollbar.set_relative_size((self.scrollbar_size[0] / self.size[1], self.scrollbar_size[1] / self.size[1]))
        self._scrollbar.set_image()
        relative_scrollbar_position = (self._scrollbar.rect.left - self.position[0], self._scrollbar.rect.top - self.position[1])
        self.image.blit(self._scrollbar.image, relative_scrollbar_position)
    
    def set_geometry(self):
        super().set_geometry()
        self._widget.set_geometry()
        self._scrollbar.set_geometry()
    
    def set_surface_size(self, new_surface_size):
        super().set_surface_size(new_surface_size)
        self._widget.set_surface_size(new_surface_size)
        # self._scrollbar.set_surface_size(new_surface_size)
    
    def process_event(self, event):
        # WAITING FOR PYGAME-CE 2.5.3 TO RELEASE TO FIX SCROLL FLAGS
        # self.image.scroll(0, SCROLL_FACTOR)
        # self.image.scroll(0, -SCROLL_FACTOR)

        offset = self._scrollbar.process_event(event)

        if offset is not None:
            self.set_image()

            if abs(offset) > 0:
                self._scroll_percentage = self.calculate_scroll_percentage(offset, scrollbar=True)

        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    self._scroll_percentage = self.calculate_scroll_percentage(-self.scroll_factor)
                    self.set_image()
                    return
                elif event.button == 5:
                    if self._scroll_percentage == 100:
                        return
                    
                    self._scroll_percentage = self.calculate_scroll_percentage(self.scroll_factor)
                    self.set_image()
                    return
                
        widget_event = self._widget.process_event(event, scrolled_pos=self.calculate_widget_position())
        if widget_event is not None:
            self.set_image()
        return widget_event