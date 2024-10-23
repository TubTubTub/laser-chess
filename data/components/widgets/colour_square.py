import pygame
from data.components.widgets.bases import _Widget
from data.components.custom_event import CustomEvent
from data.constants import SettingsEventType
from data.utils.widget_helpers import create_square_gradient

class ColourSquare(_Widget):
    def __init__(self, surface, get_parent_position, relative_position, relative_length):
        super().__init__()
        self._screen = surface
        self._screen_size = self._screen.get_size()
        self._get_parent_position = get_parent_position

        self._relative_position = relative_position
        self._relative_length = relative_length

        self._colour = None
    
    @property
    def _length(self):
        return self._relative_length * self._screen_size[1]
    
    @property
    def _position(self):
        return (self._relative_position[0] * self._screen_size[0], self._relative_position[1] * self._screen_size[1])

    def set_colour(self, new_colour):
        self._colour = pygame.Color(new_colour)
    
    def set_image(self):
        self.image = create_square_gradient(side_length=self._length, colour=self._colour)
    
    def set_geometry(self):
        self.rect = self.image.get_rect()
        self.rect.topleft = (self._relative_position[0] * self._screen_size[0], self._relative_position[1] * self._screen_size[1])
    
    def set_screen_size(self, new_screen_size):
        self._screen_size = new_screen_size
    
    def global_to_relative_position(self, position):
        global_x, global_y = position
        parent_x, parent_y = self._get_parent_position()

        return (global_x - parent_x - self._position[0], global_y - parent_y - self._position[1])
    
    def process_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            relative_pos = self.global_to_relative_position(event.pos)

            if not (0 < relative_pos[0] < self._length and 0 < relative_pos[1] < self._length):
                return None

            clicked_colour = self.image.get_at(relative_pos)
            
            return CustomEvent.create_event(SettingsEventType.COLOUR_CLICK, colour=clicked_colour)