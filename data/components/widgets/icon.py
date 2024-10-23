import pygame
from data.components.widgets.bases import _Widget

class Icon(_Widget):
    def __init__(self, relative_position, size, icon, fill_colour=(100, 100, 100), margin=30, border_width=5, border_radius=50, border_colour=(255, 255, 255), shadow_distance=0, shadow_colour=(0, 0, 0)):
        super().__init__()
        self._screen_size = pygame.display.get_surface().get_size()

        self._relative_position = relative_position
        self._relative_size = (size[0] / self._screen_size[1], size[1] / self._screen_size[1])
        self._relative_border_width = border_width / self._screen_size[1]
        self._relative_margin = margin / self._screen_size[1]
        self._relative_border_radius = border_radius / self._screen_size[1]

        self._border_colour = border_colour
        self._fill_colour = fill_colour

        self._icon = icon
        
        self._empty_surface = pygame.Surface((0, 0), pygame.SRCALPHA)

    @property
    def _position(self):
        return (self._relative_position[0] * self._screen_size[0], self._relative_position[1] * self._screen_size[1])

    @property
    def _size(self):
        return (self._relative_size[0] * self._screen_size[1], self._relative_size[1] * self._screen_size[1])

    @property
    def _margin(self):
        return self._relative_margin * self._screen_size[1]

    @property
    def _border_width(self):
        return self._relative_border_width * self._screen_size[1]
    
    @property
    def _border_radius(self):
        return self._relative_border_radius * self._screen_size[1]
    
    def set_image(self):
        self.image = pygame.transform.scale(self._empty_surface, self._size)
        pygame.draw.rect(self.image, self._fill_colour, self.image.get_rect(), border_radius=int(self._border_radius))
        scaled_icon = pygame.transform.smoothscale(self._icon, (self._size[0] -  (2 * self._margin), self._size[1] -  (2 * self._margin)))
        self.image.blit(scaled_icon, (self._margin, self._margin))
        pygame.draw.rect(self.image, self._border_colour, self.image.get_rect(), width=int(self._border_width), border_radius=int(self._border_radius))

    
    def set_geometry(self):
        self.rect = self.image.get_rect()
        self.rect.topleft = self._position
    
    def set_screen_size(self, new_screen_size):
        self._screen_size = new_screen_size
    
    def process_event(self, event):
        pass