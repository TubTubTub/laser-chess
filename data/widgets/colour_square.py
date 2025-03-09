import pygame
from data.widgets.bases.widget import _Widget
from data.helpers.widget_helpers import create_square_gradient

class _ColourSquare(_Widget):
    def __init__(self, relative_width, **kwargs):
        super().__init__(relative_size=(relative_width, relative_width), scale_mode='width', **kwargs)

        self._colour = None

    def set_colour(self, new_colour):
        self._colour = pygame.Color(new_colour)

    def get_colour(self):
        return self._colour

    def set_image(self):
        self.image = create_square_gradient(side_length=self.size[0], colour=self._colour)

    def process_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            relative_mouse_pos = (event.pos[0] - self.position[0], event.pos[1] - self.position[1])

            if (
                0 > relative_mouse_pos[0] or
                self.size[0] < relative_mouse_pos[0] or
                0 > relative_mouse_pos[1] or
                self.size[1] < relative_mouse_pos[1]
            ): return None

            self.set_colour(self.image.get_at(relative_mouse_pos))

            return self._colour

        return None