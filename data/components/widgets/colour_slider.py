import pygame
from data.components.widgets.bases import _Widget
from data.components.widgets.slider_thumb import SliderThumb
from data.utils.widget_helpers import create_slider_gradient
from data.constants import WidgetState

class ColourSlider(_Widget):
    def __init__(self, relative_position, size, border_width=12, border_colour=(255, 255, 255)):
        super().__init__()
        self._screen = pygame.display.get_surface()
        self._screen_size = self._screen.get_size()
        self._relative_position = relative_position
        self._relative_size = (size[0] / self._screen_size[1], size[1] / self._screen_size[1])
        self._relative_border_width = border_width / self._screen_size[1]

        self._border_colour = border_colour

        self._gradient_surface = create_slider_gradient(self.calculate_gradient_size(), border_width, border_colour)

        self._selected_percent = 0

        self._thumb = SliderThumb(radius=self._size[1] / 2, border_colour=border_colour)

        self._empty_surface = pygame.Surface(self._size)
        self._empty_surface.fill((50, 50, 50))
        
        self.set_image()
        self.set_geometry()
    
    @property
    def _size(self):
        return (self._relative_size[0] * self._screen_size[1], self._relative_size[1] * self._screen_size[1])

    @property
    def _position(self):
        return (self._relative_position[0] * self._screen_size[0], self._relative_position[1] * self._screen_size[1])
    
    @property
    def _border_width(self):
        return self._relative_border_width * self._screen_size[1]
    
    def calculate_gradient_size(self):
        return (self._size[0] - 2 * (self._size[1] / 2), self._size[1] / 2)
    
    def calculate_gradient_position(self):
        return (self._size[1] / 2, self._size[1] / 4)

    def calculate_gradient_percent(self, mouse_pos):
        mouse_pos = (mouse_pos[0] - self.rect.topleft[0], mouse_pos[1] - self.rect.topleft[1])

        if (self._size[1] / 2 < mouse_pos[0] < self._size[0] - self._size[1] / 2):
        # and (self._size[1] / 4 < mouse_pos[1] < self._size[1] * 3/4)
            border_width = self._relative_border_width * self._screen_size[1]
            selected_percent = (mouse_pos[0] - (self._size[1] / 2) - border_width) / (self.calculate_gradient_size()[0] - 2 * border_width)
            selected_percent = max(0, min(selected_percent, 1))
            return selected_percent

        else:
            return None
    
    def calculate_thumb_position(self):
        gradient_size = self.calculate_gradient_size()
        x = gradient_size[0] * self._selected_percent
        y = 0

        return (x, y)
    
    # def calculate_thumb_position(self):
    #     percent = self._thumb.get_percent()

    #     x = self.calculate_gradient_size()[0] * percent
    #     y = 0

    #     return (x, y)

    # def calculate_thumb_screen_position(self):
    #     relative_position = self.calculate_thumb_position()

    #     x = relative_position[0] + self._position[0] - (self._size[0] / 2)
    #     y = self._position[1] - (self._size[1] / 2)

    #     return (x, y)
    
    def calculate_selected_colour(self):
        colour = pygame.Color(0)
        colour.hsva = (int(self._selected_percent * 360), 100, 100)
        return colour
    
    def set_image(self):
        gradient_scaled = pygame.transform.smoothscale(self._gradient_surface, self.calculate_gradient_size())
        gradient_position = self.calculate_gradient_position()

        self.image = pygame.transform.scale(self._empty_surface, (self._size))
        self.image.blit(gradient_scaled, gradient_position)

        thumb_position = self.calculate_thumb_position()
        thumb_colour = self.calculate_selected_colour()

        self._thumb.initialise_new_colours(thumb_colour)
        self._thumb.set_surface(radius=self._size[1] / 2, border_width=self._border_width)
        self._thumb.set_position((self._position[0] + thumb_position[0], self._position[1] + thumb_position[1]))

        thumb_surface = self._thumb.get_surface()
        self.image.blit(thumb_surface, thumb_position)

    def set_geometry(self):
        self.rect = self.image.get_rect()
        self.rect.topleft = self._position
    
    def set_screen_size(self, new_screen_size):
        self._screen_size = new_screen_size
    
    def process_event(self, event):
        if event.type in [pygame.MOUSEMOTION]:
            self._thumb.process_event(event)

            if self._thumb.state == WidgetState.PRESS:
                selected_percent = self.calculate_gradient_percent(event.pos)

                if selected_percent:
                    self._selected_percent = selected_percent
                    self.set_image()

        if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]:
            self._thumb.process_event(event)
            self.set_image()