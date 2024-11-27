import pygame
from data.widgets.bases import _Widget
from data.assets import FONTS
from data.utils.font_helpers import width_to_font_size

class MoveList(_Widget):
    def __init__(self, relative_position, width, minimum_height=0, fill_colour=(150, 150, 150), text_colour=(0, 0, 0), move_list=[], font=FONTS['default']):
        super().__init__()
        self._screen_size = pygame.display.get_surface().get_size()

        self._relative_position = relative_position
        self._relative_width = width / self._screen_size[1]
        self._relative_minimum_height = minimum_height / self._screen_size[1]
        self._move_list = move_list

        self._font = font
        self._relative_font_size = width_to_font_size(self._font, self._width / 5) / self._screen_size[1]

        self._fill_colour = pygame.Color(fill_colour)
        self._text_colour = pygame.Color(text_colour)
        
        self._empty_surface = pygame.Surface((0, 0), pygame.SRCALPHA)
        
        self.set_image()
        self.set_geometry()

    @property
    def _position(self):
        return (self._relative_position[0] * self._screen_size[0], self._relative_position[1] * self._screen_size[1])

    @property
    def _width(self):
        return self._relative_width * self._screen_size[1]
    
    @property
    def _minimum_height(self):
        return self._relative_minimum_height * self._screen_size[1]
    
    @property
    def _font_size(self):
        return self._relative_font_size * self._screen_size[1]
    
    def register_get_rect(self, get_rect_func):
        pass

    def append_to_move_list(self, new_move):
        self._move_list.append(new_move)
        self.set_image()
        self.set_geometry()
    
    def set_image(self):
        font_metrics = self._font.get_metrics('j', size=self._font_size)
        row_gap = font_metrics[0][3] - font_metrics[0][2]

        image_size = (self._width, max(self._minimum_height, row_gap * ( 2 * ((len(self._move_list) + 1) // 2) + 1 ) ))
        self.image = pygame.transform.scale(self._empty_surface, image_size)
        self.image.fill(self._fill_colour)

        for index, move in enumerate(self._move_list):
            if index % 2 == 0:
                text_position = (self._width / 5, row_gap * (1 + 2 * (index // 2)))
            else:
                text_position = (self._width * 3 / 5, row_gap * (1 + 2 * (index // 2)))
            self._font.render_to(self.image, text_position, text=move, size=self._font_size, fgcolor=self._text_colour)

            move_number = (index // 2) + 1
            move_number_position = (self._width / 10, row_gap * (1 + 2 * (index // 2)))
            self._font.render_to(self.image, move_number_position, text=str(move_number), size=self._font_size, fgcolor=self._text_colour)
    
    def set_geometry(self):
        self.rect = self.image.get_rect()
        self.rect.topleft = self._position
    
    def set_screen_size(self, new_screen_size):
        self._screen_size = new_screen_size
        self._relative_font_size = width_to_font_size(self._font, self._width / 5) / self._screen_size[1]
    
    def process_event(self, event, scrolled_pos=None):
        pass