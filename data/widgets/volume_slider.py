import pygame
from data.widgets.bases import _Widget
from data.widgets.slider_thumb import _SliderThumb
from data.components.custom_event import CustomEvent
from data.constants import SettingsEventType
from data.constants import WidgetState
from data.utils.widget_helpers import create_slider
from data.managers.theme import theme

class VolumeSlider(_Widget):
    def __init__(self, relative_length, default_volume, volume_type, thumb_colour=theme['fillSecondary'], **kwargs):
        super().__init__(relative_size=(relative_length, relative_length * 0.2), **kwargs)

        self._volume_type = volume_type
        self._selected_percent = default_volume
        self._last_mouse_x = None

        self._thumb = _SliderThumb(radius=self.size[1] / 2, border_colour=self._border_colour, fill_colour=thumb_colour)
        self._gradient_surface = create_slider(self.calculate_slider_size(), self._fill_colour, self.border_width, self._border_colour)
        
        self._empty_surface = pygame.Surface(self.size, pygame.SRCALPHA)

    @property
    def position(self):
        '''Minus so easier to position slider by starting from the left edge of the slider instead of the thumb'''
        return (self._relative_position[0] * self.surface_size[0] - (self.size[1] / 2), self._relative_position[1] * self.surface_size[1])
    
    def calculate_slider_position(self):
        return (self.size[1] / 2, self.size[1] / 4)
    
    def calculate_slider_size(self):
        return (self.size[0] - 2 * (self.size[1] / 2), self.size[1] / 2)

    def calculate_selected_percent(self, mouse_pos):
        if self._last_mouse_x is None:
            return
        
        x_change = (mouse_pos[0] - self._last_mouse_x) / (self.calculate_slider_size()[0] - 2 * self.border_width)
        return max(0, min(self._selected_percent + x_change, 1))
    
    def calculate_thumb_position(self):
        gradient_size = self.calculate_slider_size()
        x = gradient_size[0] * self._selected_percent
        y = 0

        return (x, y)

    def relative_to_global_position(self, position):
        relative_x, relative_y = position
        return (relative_x + self.position[0], relative_y + self.position[1])
    
    def set_image(self):
        gradient_scaled = pygame.transform.smoothscale(self._gradient_surface, self.calculate_slider_size())
        gradient_position = self.calculate_slider_position()

        self.image = pygame.transform.scale(self._empty_surface, (self.size))
        self.image.blit(gradient_scaled, gradient_position)

        thumb_position = self.calculate_thumb_position()
        self._thumb.set_surface(radius=self.size[1] / 2, border_width=self.border_width)
        self._thumb.set_position(self.relative_to_global_position((thumb_position[0], thumb_position[1])))

        thumb_surface = self._thumb.get_surface()
        self.image.blit(thumb_surface, thumb_position)
    
    def set_volume(self, volume):
        self._selected_percent = volume
        self.set_image()
    
    def process_event(self, event):
        if event.type not in [pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]:
            return
        
        before_state = self._thumb.state
        self._thumb.process_event(event)
        after_state = self._thumb.state

        if before_state != after_state:
            self.set_image()

            if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]:
                self._last_mouse_x = None
                return CustomEvent(SettingsEventType.VOLUME_SLIDER_CLICK, volume=round(self._selected_percent, 3), volume_type=self._volume_type)

        if self._thumb.state == WidgetState.PRESS:
            selected_percent = self.calculate_selected_percent(event.pos)
            self._last_mouse_x = event.pos[0]

            if selected_percent:
                self._selected_percent = selected_percent
                self.set_image()
                return CustomEvent(SettingsEventType.VOLUME_SLIDER_SLIDE)