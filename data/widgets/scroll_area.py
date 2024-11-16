import pygame
from data.widgets.bases import _Widget


class ScrollArea(_Widget):
    def __init__(self, relative_position, size, widget, scroll_factor=5):
        super().__init__()
        self._screen_size = pygame.display.get_surface().get_size()

        self._relative_position = relative_position
        self._relative_size = (size[0] / self._screen_size[1], size[1] / self._screen_size[1])
        self._relative_scroll_factor = scroll_factor / self._screen_size[1]

        self._scroll_height = 0
        self._widget = widget
        
        self._empty_surface = pygame.Surface((0, 0), pygame.SRCALPHA)

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
    
    def set_image(self):
        self.image = pygame.transform.scale(self._empty_surface, self._size)
        self.image.fill((100, 100, 100))

        self._widget.set_image()
        self.image.blit(self._widget.image, (0, self._scroll_height))
    
    def set_geometry(self):
        self.rect = self.image.get_rect()
        self.rect.topleft = self._position
        self._widget.set_geometry()
    
    def set_screen_size(self, new_screen_size):
        self._screen_size = new_screen_size
        self._widget.set_screen_size(new_screen_size)
    
    def process_event(self, event):
        # WAITING FOR PYGAME-CE 2.5.3 TO RELEASE TO FIX SCROLL FLAGS
        # self.image.scroll(0, SCROLL_FACTOR)
        # self.image.scroll(0, -SCROLL_FACTOR)
        if self.rect.collidepoint(pygame.mouse.get_pos()) is False:
            return
        
        if event.type != pygame.MOUSEBUTTONDOWN:
            return
        
        if event.button == 4:
            self._scroll_height = min(0, self._scroll_height + self._scroll_factor)
            self.set_image()
        elif event.button == 5:
            if (self._scroll_height + self._widget.rect.height) <= self._size[1]:
                return
            self._scroll_height = min(0, self._scroll_height - self._scroll_factor)
            self.set_image()
        else:
            return