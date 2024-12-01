import pygame
from data.widgets.bases import _Widget
from data.utils.widget_helpers import create_square_gradient

class _ColourSquare(_Widget):
    def __init__(self, get_parent_position, relative_length, **kwargs):
        super().__init__(relative_size=(relative_length, relative_length), **kwargs)

        self._get_parent_position = get_parent_position

        self._colour = None
    
    def global_to_relative_position(self, position):
        global_x, global_y = position
        parent_x, parent_y = self._get_parent_position()

        return (global_x - parent_x - self.position[0], global_y - parent_y - self.position[1])

    def set_colour(self, new_colour):
        self._colour = pygame.Color(new_colour)
    
    def get_colour(self):
        return self._colour
    
    def set_image(self):
        self.image = create_square_gradient(side_length=self.size[0], colour=self._colour)
    
    def process_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            relative_pos = self.global_to_relative_position(event.pos)

            if not (0 < relative_pos[0] < self.size[0] and 0 < relative_pos[1] < self.size[0]):
                return None

            clicked_colour = self.image.get_at(relative_pos)
            return clicked_colour
        
        return None