import pygame
from data.components.widgets.bases import _Widget
from data.components.widgets.slider_thumb import SliderThumb
from data.components.custom_event import CustomEvent
from data.constants import SettingsEventType
from data.constants import WidgetState
from data.utils.widget_helpers import create_slider

class VolumeSlider(_Widget):
    def __init__(self, relative_position, relative_length, default_volume, volume_type, fill_colour=(100, 100, 100), thumb_colour=(200, 200, 200), border_width=12, border_colour=(255, 255, 255)):
        super().__init__()
        self._screen = pygame.display.get_surface()
        self._screen_size = self._screen.get_size()
 
        self._relative_position = relative_position
        self._relative_length = relative_length
        self._relative_border_width = border_width / self._screen_size[1]

        self._fill_colour = pygame.Color(fill_colour)
        self._thumb_colour = pygame.Color(thumb_colour)
        self._border_colour = pygame.Color(border_colour)

        self._volume_type = volume_type
        self._selected_percent = default_volume

        self._thumb = SliderThumb(radius=self._size[1] / 2, border_colour=border_colour)
        self._thumb.initialise_new_colours(self._thumb_colour)
        self._gradient_surface = create_slider(self.calculate_slider_size(), self._fill_colour, border_width, border_colour)
        self._empty_surface = pygame.Surface(self._size, pygame.SRCALPHA)
    
    @property
    def _size(self):
        return (self._relative_length * self._screen_size[1], self._relative_length * 0.2 * self._screen_size[1])

    @property
    def _position(self):
        '''Minus so easier to position slider by starting from the left edge of the slider instead of the thumb'''
        return (self._relative_position[0] * self._screen_size[0] - (self._size[1] / 2), self._relative_position[1] * self._screen_size[1])
    
    @property
    def _border_width(self):
        return self._relative_border_width * self._screen_size[1]
    
    def calculate_slider_position(self):
        return (self._size[1] / 2, self._size[1] / 4)
    
    def calculate_slider_size(self):
        return (self._size[0] - 2 * (self._size[1] / 2), self._size[1] / 2)

    def calculate_selected_percent(self, mouse_pos):
        relative_mouse_pos = (mouse_pos[0] - self.rect.topleft[0], mouse_pos[1] - self.rect.topleft[1])

        selected_percent = (relative_mouse_pos[0] - (self._size[1] / 2) - self._border_width) / (self.calculate_slider_size()[0] - 2 * self._border_width)
        selected_percent = max(0, min(selected_percent, 1))
        return selected_percent
    
    def calculate_thumb_position(self):
        gradient_size = self.calculate_slider_size()
        x = gradient_size[0] * self._selected_percent
        y = 0

        return (x, y)

    def relative_to_global_position(self, position):
        relative_x, relative_y = position
        return (relative_x + self._position[0], relative_y + self._position[1])
    
    def set_image(self):
        gradient_scaled = pygame.transform.smoothscale(self._gradient_surface, self.calculate_slider_size())
        gradient_position = self.calculate_slider_position()

        self.image = pygame.transform.scale(self._empty_surface, (self._size))
        self.image.blit(gradient_scaled, gradient_position)

        thumb_position = self.calculate_thumb_position()
        self._thumb.set_surface(radius=self._size[1] / 2, border_width=self._border_width)
        self._thumb.set_position(self.relative_to_global_position((thumb_position[0], thumb_position[1])))

        thumb_surface = self._thumb.get_surface()
        self.image.blit(thumb_surface, thumb_position)
    
    def set_volume(self, volume):
        self._selected_percent = volume
        self.set_image()

    def set_geometry(self):
        self.rect = self.image.get_rect()
        self.rect.topleft = self._position
    
    def set_screen_size(self, new_screen_size):
        self._screen_size = new_screen_size
    
    def process_event(self, event):
        if event.type in [pygame.MOUSEMOTION]:
            self._thumb.process_event(event)

            if self._thumb.state == WidgetState.PRESS:
                selected_percent = self.calculate_selected_percent(event.pos)

                if selected_percent:
                    self._selected_percent = selected_percent
                    self.set_image()
                    return CustomEvent(SettingsEventType.VOLUME_SLIDER_SLIDE)
            

        if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]:
            previous_state = self._thumb.state

            self._thumb.process_event(event)
            self.set_image()

            if self._thumb.state != previous_state:
                return CustomEvent(SettingsEventType.VOLUME_SLIDER_CLICK, volume=self._selected_percent, volume_type=self._volume_type)