import pygame
from data.widgets.bases import _Widget
from data.utils.board_helpers import create_board
from data.utils.data_helpers import get_user_settings

user_settings = get_user_settings()

class Chessboard(_Widget):
    def __init__(self, relative_position, width, center=False):
        super().__init__()
        self._screen_size = pygame.display.get_surface().get_size()

        size = (width, width * 0.8)
        self._relative_position = relative_position
        self._relative_size = (size[0] / self._screen_size[1], size[1] / self._screen_size[1])

        self._board_surface = create_board(self._size, user_settings['primaryBoardColour'], user_settings['secondaryBoardColour'])

        self._center = center

        self.set_image()
        self.set_geometry()

    @property
    def _position(self):
        if self._center:
            return self.calculate_center_position()
        return (self._relative_position[0] * self._screen_size[0], self._relative_position[1] * self._screen_size[1])

    @property
    def _size(self):
        return (self._relative_size[0] * self._screen_size[1], self._relative_size[1] * self._screen_size[1])

    def get_position(self):
        return self._position

    def get_size(self):
        return self._size

    def calculate_center_position(self):
        '''Returns required board starting position to draw on center of the screen'''
        screen_x, screen_y = self._screen_size
        board_x, board_y = self._size

        x = screen_x / 2 - (board_x / 2)
        y = screen_y / 2 - (board_y / 2)

        return (x, y)
    
    def set_image(self):
        self.image = pygame.transform.smoothscale(self._board_surface, self._size)
    
    def set_geometry(self):
        self.rect = self.image.get_rect()
        self.rect.topleft = self._position
    
    def set_screen_size(self, new_screen_size):
        self._screen_size = new_screen_size
    
    def process_event(self, event):
        pass