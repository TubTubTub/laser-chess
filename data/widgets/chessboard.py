import pygame
from data.widgets.bases import _Widget
from data.utils.board_helpers import create_board
from data.utils.data_helpers import get_user_settings

user_settings = get_user_settings()

class Chessboard(_Widget):
    def __init__(self, relative_width, center=False, **kwargs):
        super().__init__(relative_size=(relative_width, relative_width * 0.8), **kwargs)

        self._board_surface = create_board(self._size, user_settings['primaryBoardColour'], user_settings['secondaryBoardColour'])

        self._center = center

        self.set_image()
        self.set_geometry()

    @property
    def position(self):
        if self._center:
            return self.calculate_center_position()
        return (self._relative_position[0] * self._surface_size[0], self._relative_position[1] * self._surface_size[1])

    def get_position(self):
        return self.position

    def get_size(self):
        return self.size

    def calculate_center_position(self):
        '''Returns required board starting position to draw on center of the screen'''
        screen_x, screen_y = self._surface_size
        board_x, board_y = self.size

        x = screen_x / 2 - (board_x / 2)
        y = screen_y / 2 - (board_y / 2)

        return (x, y)
    
    def set_image(self):
        self.image = pygame.transform.smoothscale(self._board_surface, self.size)
    
    def process_event(self, event):
        pass