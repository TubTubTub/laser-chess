import pygame
from data.widgets.bases import _Widget

class Rectangle(_Widget):
    def __init__(self, relative_position, relative_size, fill_colour=(100, 100, 100), border_width=0, border_colour=(255, 255, 255), border_radius=5, surface=None):
        super().__init__(surface)

        self._relative_position = relative_position
        self._relative_size = (relative_size[0] * self._surface_size[0] / self._surface_size[1], relative_size[1])
        self._relative_border_width = border_width / self._surface_size[1]
        self._relative_border_radius = border_radius / self._surface_size[1]

        self._border_colour = border_colour
        self._fill_colour = pygame.Color(fill_colour)
        
        self._empty_surface = pygame.Surface((0, 0), pygame.SRCALPHA)
        
        self.set_image()
        self.set_geometry()

    @property
    def _position(self):
        return (self._relative_position[0] * self._surface_size[0], self._relative_position[1] * self._surface_size[1])

    @property
    def _size(self):
        return (self._relative_size[0] * self._surface_size[1], self._relative_size[1] * self._surface_size[1])

    @property
    def _border_width(self):
        return self._relative_border_width * self._surface_size[1]
    
    @property
    def _border_radius(self):
        return self._relative_border_radius * self._surface_size[1]
    
    def set_image(self):
        print('RECT')
        self.image = pygame.transform.scale(self._empty_surface, self._size)
        pygame.draw.rect(self.image, self._fill_colour, self.image.get_rect(), border_radius=int(self._border_radius))

        if self._border_width:
            pygame.draw.rect(self.image, self._border_colour, self.image.get_rect(), width=int(self._border_width), border_radius=int(self._border_radius))
    
    def set_geometry(self):
        self.rect = self.image.get_rect()
        self.rect.topleft = self._position
    
    def set_surface_size(self, new_surface_size):
        self._surface_size = new_surface_size
    
    def process_event(self, event):
        pass