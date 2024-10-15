import pygame
from data.components.widgets.bases import _Widget
from data.components.widgets.slider_thumb import SliderThumb
from data.utils.widget_helpers import create_gradient

class ColourSlider(_Widget):
    def __init__(self, relative_position, width, height, border_width=12, border_colour=(255, 255, 255)):
        super().__init__()
        self._screen_size = pygame.display.get_surface().get_size()
        self._relative_size = (width / self._screen_size[1], height / self._screen_size[1])
        self._relative_position = relative_position
        
        self._border_width = border_width
        self._selected_percent = 0

        self._gradient_surface = create_gradient(self.calculate_gradient_size(), border_width, border_colour)

        self._thumb = SliderThumb(radius=self._size[1] / 2, colour=(255, 255, 255))
        self.set_thumb_position(0)

        self._empty_surface = pygame.Surface(self._size)
        self._empty_surface.fill((50, 50, 50))
        
        self.set_image()
        self.set_geometry()
    
    @property
    def _size(self):
        return (self._relative_size[0] * self._screen_size[1], self._relative_size[1] * self._screen_size[1])

    @property
    def _position(self):
        return (self._relative_position[0] * self._screen_size[0], self._relative_size[1] * self._screen_size[1])
    
    def calculate_gradient_size(self):
        return (self._size[0] - 2 * (self._size[1] / 2), self._size[1] / 2)
    
    def calculate_gradient_position(self):
        return (self._size[1] / 2, self._size[1] / 4)

    def calculate_gradient_percent(self, mouse_pos):
        mouse_pos = (mouse_pos[0] - self.rect.topleft[0], mouse_pos[1] - self.rect.topleft[1])

        if (self._size[1] / 2 < mouse_pos[0] < self._size[0] - self._size[1] / 2) and (self._size[1] / 4 < mouse_pos[1] < self._size[1] * 3/4):
            selected_percent = (mouse_pos[0] - (self._size[1] / 2) - self._border_width) / (self.calculate_gradient_size()[0] - 2 * self._border_width)
            selected_percent = max(0, min(selected_percent, 1))
            return selected_percent

        else:
            return None
    
    def set_image(self):
        gradient_scaled = pygame.transform.smoothscale(self._gradient_surface, self.calculate_gradient_size())
        gradient_position = self.calculate_gradient_position()

        self.image = pygame.transform.scale(self._empty_surface, (self._size))
        self.image.blit(gradient_scaled, gradient_position)

        self.image.blit(self._thumb.get_surface(), self._thumb.get_position())

    def set_geometry(self):
        self.rect = self.image.get_rect()
        self.rect.center = self._position
    
    def set_thumb_position(self, x):
        x = x - (self._size[1] / 2)
        y = 0
        self._thumb.set_position((x, y))
    
    def set_screen_size(self, new_screen_size):
        self._screen_size = new_screen_size
        self._thumb.set_radius((self._relative_size[1] * self._screen_size[1]) / 2)
    
    def process_event(self, event):
        pass
        match event.type:
            case pygame.MOUSEBUTTONDOWN:
                if not self.rect.collidepoint(event.pos):
                    return
                
                selected_percent = self.calculate_gradient_percent(event.pos)
                if selected_percent:
                    self._selected_percent = selected_percent

                    self.set_thumb_position(event.pos[0])
                    self.set_image()
    
    def get_selected_colour(self):
        colour = pygame.Color(0)
        colour.hsva = (int(self._selected_percent * 360), 100, 100)
        return colour
