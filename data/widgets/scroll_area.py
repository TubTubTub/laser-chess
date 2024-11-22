import pygame
from data.widgets.bases import _Widget
from data.widgets.scrollbar import _Scrollbar

SCROLLBAR_WIDTH_FACTOR =  0.05

class ScrollArea(_Widget):
    def __init__(self, relative_position, size, widget, vertical, scroll_factor=5):
        super().__init__()
        self._screen_size = pygame.display.get_surface().get_size()

        self._relative_position = relative_position
        self._relative_size = (size[0] / self._screen_size[1], size[1] / self._screen_size[1])
        self._relative_scroll_factor = scroll_factor / self._screen_size[1]

        self._scroll_percentage = 0
        self._widget = widget
        self._vertical = vertical
        
        self._empty_surface = pygame.Surface((0, 0), pygame.SRCALPHA)
        
        self._scrollbar = _Scrollbar(
            position=self.calculate_scrollbar_position(),
            size=self._scrollbar_size,
            vertical=vertical,
        )

        self.set_image()
        self.set_geometry()

    @property
    def _position(self):
        return (self._relative_position[0] * self._screen_size[0], self._relative_position[1] * self._screen_size[1])

    @property
    def _size(self):
        return (self._relative_size[0] * self._screen_size[1], self._relative_size[1] * self._screen_size[1])
    
    @property
    def _scroll_factor(self):
        return self._relative_scroll_factor * self._screen_size[1]

    @property
    def _scrollbar_size(self):
        if self._vertical:
            return (self._size[0] * SCROLLBAR_WIDTH_FACTOR, min(1, self._size[1] / self._widget.rect.height) * self._size[1])
        else:
            return (min(1, self._size[0] / (self._widget.rect.width + 0.001)) * self._size[1], self._size[1] * SCROLLBAR_WIDTH_FACTOR)

    def calculate_scroll_percentage(self, offset, scrollbar=False):
        if self._vertical:
            widget_height = self._widget.rect.height

            if widget_height < self._size[1]:
                return 0
            
            if scrollbar:
                self._scroll_percentage += offset / (self._size[1] - self._scrollbar_size[1] + 0.001)
            else:
                max_scroll_height = widget_height - self._size[1]
                current_scroll_height = self._scroll_percentage * max_scroll_height
                self._scroll_percentage = (current_scroll_height + offset) / max_scroll_height
        else:
            widget_width = self._widget.rect.width

            if widget_width < self._size[0]:
                return 0

            if scrollbar:
                self._scroll_percentage += offset / (self._size[0] - self._scrollbar_size[0] + 0.001)
            else:
                max_scoll_width = widget_width - self._size[0]
                current_scroll_width = self._scroll_percentage * max_scoll_width
                self._scroll_percentage = (current_scroll_width + offset) / max_scoll_width
                print(self._scroll_percentage, (current_scroll_width + offset))

        return min(1, max(0, self._scroll_percentage))

    def calculate_widget_position(self):
        if self._vertical:
            return (0, -self._scroll_percentage * (self._widget.rect.height - self._size[1]))
        else:
            return (-self._scroll_percentage * (self._widget.rect.width - self._size[0]), 0)

    def calculate_scrollbar_position(self):
        if self._vertical:
            vertical_offset = (self._size[1] - self._scrollbar_size[1]) * self._scroll_percentage
            scrollbar_position = (self._size[0] * (1 - SCROLLBAR_WIDTH_FACTOR) + self._position[0], self._position[1] + vertical_offset)
        else:
            horizontal_offset = (self._size[0] - self._scrollbar_size[0]) * self._scroll_percentage
            scrollbar_position = (self._position[0] + horizontal_offset, self._size[1] * (1 - SCROLLBAR_WIDTH_FACTOR) + self._position[1])

        return scrollbar_position
    
    def set_widget(self, new_widget):
        self._widget = new_widget
        self.set_image()
        self.set_geometry()
    
    def set_image(self):
        self.image = pygame.transform.scale(self._empty_surface, self._size)
        self.image.fill((100, 100, 100))

        self._widget.set_image()
        self.image.blit(self._widget.image, self.calculate_widget_position())

        self._scrollbar.set_position(self.calculate_scrollbar_position())
        self._scrollbar.set_size(self._scrollbar_size)
        self._scrollbar.set_image()
        relative_scrollbar_position = (self._scrollbar.rect.left - self._position[0], self._scrollbar.rect.top - self._position[1])
        self.image.blit(self._scrollbar.image, relative_scrollbar_position)
    
    def set_geometry(self):
        self.rect = self.image.get_rect()
        self.rect.topleft = self._position

        self._widget.set_geometry()
        self._scrollbar.set_geometry()
    
    def set_screen_size(self, new_screen_size):
        self._screen_size = new_screen_size

        self._widget.set_screen_size(new_screen_size)
        # self._scrollbar.set_screen_size(new_screen_size)
    
    def process_event(self, event):
        # WAITING FOR PYGAME-CE 2.5.3 TO RELEASE TO FIX SCROLL FLAGS
        # self.image.scroll(0, SCROLL_FACTOR)
        # self.image.scroll(0, -SCROLL_FACTOR)

        offset = self._scrollbar.process_event(event)

        if offset is not None:
            self.set_image()

            if abs(offset) > 0:
                self._scroll_percentage = self.calculate_scroll_percentage(offset, scrollbar=True)

        if self.rect.collidepoint(pygame.mouse.get_pos()) is False:
            return
        
        if event.type != pygame.MOUSEBUTTONDOWN:
            return
        
        if event.button == 4:
            self._scroll_percentage = self.calculate_scroll_percentage(-self._scroll_factor)
            self.set_image()
        elif event.button == 5:
            if self._scroll_percentage == 100:
                return
            
            self._scroll_percentage = self.calculate_scroll_percentage(self._scroll_factor)
            self.set_image()
        else:
            return