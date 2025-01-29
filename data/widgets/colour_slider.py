import pygame
from data.widgets.bases import _Widget
from data.widgets.slider_thumb import _SliderThumb
from data.constants import WidgetState
from data.utils.widget_helpers import create_slider_gradient

class _ColourSlider(_Widget):
    def __init__(self, relative_width, **kwargs):
        super().__init__(relative_size=(relative_width, relative_width * 0.2), **kwargs)

        self._gradient_surface = create_slider_gradient(self.gradient_size, self.border_width, self._border_colour)
        self._thumb = _SliderThumb(radius=self.size[1] / 2, border_colour=self._border_colour)

        self._selected_percent = 0
        self._last_mouse_x = None

        self._empty_surface = pygame.Surface(self.size, pygame.SRCALPHA)
    
    @property
    def gradient_size(self):
        return (self.size[0] - 2 * (self.size[1] / 2), self.size[1] / 2)
    
    @property
    def gradient_position(self):
        return (self.size[1] / 2, self.size[1] / 4)
    
    @property
    def thumb_position(self):
        return (self.gradient_size[0] * self._selected_percent, 0)
    
    @property
    def selected_colour(self):
        colour = pygame.Color(0)
        colour.hsva = (int(self._selected_percent * 360), 100, 100)
        return colour
    
    def calculate_gradient_percent(self, mouse_pos):
        if self._last_mouse_x is None:
            return
        
        x_change = (mouse_pos[0] - self._last_mouse_x) / (self.gradient_size[0] - 2 * self.border_width)
        return max(0, min(self._selected_percent + x_change, 1))

    def relative_to_global_position(self, position):
        relative_x, relative_y = position
        return (relative_x + self.position[0], relative_y + self.position[1])

    def set_colour(self, new_colour):
        colour = pygame.Color(new_colour)
        hue = colour.hsva[0]
        self._selected_percent = hue / 360
        self.set_image()
    
    def set_image(self):
        gradient_scaled = pygame.transform.smoothscale(self._gradient_surface, self.gradient_size)
        gradient_position = self.gradient_position

        self.image = pygame.transform.scale(self._empty_surface, (self.size))
        self.image.blit(gradient_scaled, gradient_position)

        self._thumb.initialise_new_colours(self.selected_colour)
        self._thumb.set_surface(radius=self.size[1] / 2, border_width=self.border_width)
        self._thumb.set_position(self.relative_to_global_position((self.thumb_position[0], self.thumb_position[1])))

        thumb_surface = self._thumb.get_surface()
        self.image.blit(thumb_surface, self.thumb_position)
    
    def process_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self._thumb.process_event(event)

            if self._thumb.state == WidgetState.PRESS:
                selected_percent = self.calculate_gradient_percent(event.pos)
                self._last_mouse_x = event.pos[0]

                if selected_percent is not None:
                    self._selected_percent = selected_percent

                    return self.selected_colour

        elif event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]:
            if event.type == pygame.MOUSEBUTTONUP:
                self._last_mouse_x = None

            self._thumb.process_event(event)
            return self.selected_colour