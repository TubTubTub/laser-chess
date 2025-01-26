import pygame
from data.widgets.bases import _Widget
from data.utils.font_helpers import width_to_font_size

class MoveList(_Widget):
    def __init__(self, relative_width, minimum_height=0, move_list=[], **kwargs):
        super().__init__(relative_size=None, **kwargs)

        self._relative_width = relative_width * self.surface_size[0] / self.surface_size[1]
        self._relative_minimum_height = minimum_height / self.surface_size[1]
        self._move_list = move_list
        self._relative_font_size = width_to_font_size(self._font, self.surface_size[0] / 5) / self.surface_size[1]
        
        self._empty_surface = pygame.Surface((0, 0), pygame.SRCALPHA)
        
        self.set_image()
        self.set_geometry()
    
    @property
    def size(self):
        font_metrics = self._font.get_metrics('j', size=self.font_size)

        width = self._relative_width * self.surface_size[0]
        minimum_height = self._relative_minimum_height * self.surface_size[0]
        row_gap = font_metrics[0][3] - font_metrics[0][2]
        number_of_rows = 2 * ((len(self._move_list) + 1) // 2) + 1

        return (width, max(minimum_height, row_gap * number_of_rows))
    
    def register_get_rect(self, get_rect_func):
        pass
    
    def reset_move_list(self):
        self._move_list = []
        self.set_image()
        self.set_geometry()

    def append_to_move_list(self, new_move):
        self._move_list.append(new_move)
        self.set_image()
        self.set_geometry()
    
    def pop_from_move_list(self):
        self._move_list.pop()
        self.set_image()
        self.set_geometry()
    
    def set_image(self):
        self.image = pygame.transform.scale(self._empty_surface, self.size)
        self.image.fill(self._fill_colour)
        
        font_metrics = self._font.get_metrics('j', size=self.font_size)
        row_gap = font_metrics[0][3] - font_metrics[0][2]

        for index, move in enumerate(self._move_list):
            if index % 2 == 0:
                text_position = (self.size[0] / 5, row_gap * (1 + 2 * (index // 2)))
            else:
                text_position = (self.size[0] * 3 / 5, row_gap * (1 + 2 * (index // 2)))
            self._font.render_to(self.image, text_position, text=move, size=self.font_size, fgcolor=self._text_colour)

            move_number = (index // 2) + 1
            move_number_position = (self.size[0] / 10, row_gap * (1 + 2 * (index // 2)))
            self._font.render_to(self.image, move_number_position, text=str(move_number), size=self.font_size, fgcolor=self._text_colour)
    
    def process_event(self, event, scrolled_pos=None):
        pass