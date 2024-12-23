import pygame
from data.widgets.bases import _Widget
from data.utils.board_helpers import create_board
from data.utils.data_helpers import get_user_settings

class Chessboard(_Widget):
    def __init__(self, relative_width, **kwargs):
        super().__init__(relative_size=(relative_width, relative_width * 0.8), **kwargs)

        self._board_surface = None

        self.refresh_board()
        self.set_image()
        self.set_geometry()
    
    def refresh_board(self):
        user_settings = get_user_settings()
        self._board_surface = create_board(self.size, user_settings['primaryBoardColour'], user_settings['secondaryBoardColour'])
        
        self.set_image()

    def set_image(self):
        self.image = pygame.transform.smoothscale(self._board_surface, self.size)
    
    def process_event(self, event):
        pass