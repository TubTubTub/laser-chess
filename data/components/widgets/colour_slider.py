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
        self._relative_border_width = border_width / self._screen_size[1]

        self._selected_percent = 0

        self._gradient_surface = create_gradient(self.calculate_gradient_size(), border_width, border_colour)

        self._thumb = SliderThumb(radius=self._size[1] / 2, colour=(255, 0, 0), border_colour=border_colour)
        self._thumb.set_percent(0)

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
    
    def calculate_gradient_center(self):
        return (self._size[1] / 2, self._size[1] / 4)

    def calculate_gradient_percent(self, mouse_pos):
        mouse_pos = (mouse_pos[0] - self.rect.topleft[0], mouse_pos[1] - self.rect.topleft[1])

        if (self._size[1] / 2 < mouse_pos[0] < self._size[0] - self._size[1] / 2) and (self._size[1] / 4 < mouse_pos[1] < self._size[1] * 3/4):
            border_width = self._relative_border_width * self._screen_size[1]
            selected_percent = (mouse_pos[0] - (self._size[1] / 2) - border_width) / (self.calculate_gradient_size()[0] - 2 * border_width)
            selected_percent = max(0, min(selected_percent, 1))
            return selected_percent

        else:
            return None
    
    def calculate_thumb_position(self):
        percent = self._thumb.get_percent()

        x = self.calculate_gradient_size()[0] * percent
        y = 0

        return (x, y)
    
    def calculate_selected_colour(self, percent):
        colour = pygame.Color(0)
        colour.hsva = (int(percent * 360), 100, 100)
        return colour
    
    def set_image(self):
        gradient_scaled = pygame.transform.smoothscale(self._gradient_surface, self.calculate_gradient_size())
        gradient_position = self.calculate_gradient_center()

        self.image = pygame.transform.scale(self._empty_surface, (self._size))
        self.image.blit(gradient_scaled, gradient_position)

        self._thumb.set_radius((self._relative_size[1] * self._screen_size[1]) / 2)
        self._thumb.set_border_width(self._relative_border_width * self._screen_size[1])
        self._thumb.set_surface()
        self.image.blit(self._thumb.get_surface(), self.calculate_thumb_position())

    def set_geometry(self):
        self.rect = self.image.get_rect()
        self.rect.center = self._position
    
    def set_screen_size(self, new_screen_size):
        self._screen_size = new_screen_size
    
    def process_event(self, event):
        match event.type:
            case pygame.MOUSEBUTTONDOWN:
                if not self.rect.collidepoint(event.pos):
                    return
                
                selected_percent = self.calculate_gradient_percent(event.pos)
                if selected_percent:
                    self._selected_percent = selected_percent

                    self._thumb.set_percent(selected_percent)
                    self._thumb.set_colour(self.calculate_selected_colour(selected_percent))
                    self.set_image()
