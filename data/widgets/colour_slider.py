import pygame
from data.widgets.bases import _Widget
from data.widgets.slider_thumb import _SliderThumb
from data.constants import WidgetState
from data.utils.widget_helpers import create_slider_gradient

class _ColourSlider(_Widget):
    def __init__(self, get_parent_position, relative_width, **kwargs):
        super().__init__(relative_size=(relative_width, relative_width * 0.2))

        self._get_parent_position = get_parent_position

        self._gradient_surface = create_slider_gradient(self.calculate_gradient_size(), self.border_width, self._border_colour)

        self._selected_percent = 0

        self._thumb = _SliderThumb(radius=self.size[1] / 2, border_colour=self._border_colour)

        self._empty_surface = pygame.Surface(self.size, pygame.SRCALPHA)
    
    def calculate_gradient_size(self):
        return (self.size[0] - 2 * (self.size[1] / 2), self.size[1] / 2)
    
    def calculate_gradient_position(self):
        return (self.size[1] / 2, self.size[1] / 4)

    def calculate_gradient_percent(self, mouse_pos):
        parent_x, parent_y = self._get_parent_position()
        mouse_pos = (mouse_pos[0] - self.rect.topleft[0] - parent_x, mouse_pos[1] - self.rect.topleft[1] - parent_y)

        border_width = self._relative_border_width * self.surface_size[1]
        selected_percent = (mouse_pos[0] - (self.size[1] / 2) - border_width) / (self.calculate_gradient_size()[0] - 2 * border_width)
        selected_percent = max(0, min(selected_percent, 1))
        return selected_percent
    
    def calculate_thumb_position(self):
        gradient_size = self.calculate_gradient_size()
        x = gradient_size[0] * self._selected_percent
        y = 0

        return (x, y)

    def relative_to_global_position(self, position):
        relative_x, relative_y = position
        parent_x, parent_y = self._get_parent_position()
        return (relative_x + parent_x + self.position[0], relative_y + parent_y + self.position[1])

    def calculate_selected_colour(self):
        colour = pygame.Color(0)
        colour.hsva = (int(self._selected_percent * 360), 100, 100)
        return colour

    def set_colour(self, new_colour):
        colour = pygame.Color(new_colour)
        hue = colour.hsva[0]
        self._selected_percent = hue / 360
        self.set_image()
    
    def set_image(self):
        gradient_scaled = pygame.transform.smoothscale(self._gradient_surface, self.calculate_gradient_size())
        gradient_position = self.calculate_gradient_position()

        self.image = pygame.transform.scale(self._empty_surface, (self.size))
        self.image.blit(gradient_scaled, gradient_position)

        thumb_position = self.calculate_thumb_position()
        thumb_colour = self.calculate_selected_colour()

        self._thumb.initialise_new_colours(thumb_colour)
        self._thumb.set_surface(radius=self.size[1] / 2, border_width=self.border_width)
        self._thumb.set_position(self.relative_to_global_position((thumb_position[0], thumb_position[1])))

        thumb_surface = self._thumb.get_surface()
        self.image.blit(thumb_surface, thumb_position)
    
    def process_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self._thumb.process_event(event)

            if self._thumb.state == WidgetState.PRESS:
                selected_percent = self.calculate_gradient_percent(event.pos)

                if selected_percent:
                    self._selected_percent = selected_percent
                    return self.calculate_selected_colour()

        elif event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]:
            self._thumb.process_event(event)
            return self.calculate_selected_colour()