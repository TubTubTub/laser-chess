import pygame
from data.widgets.bases import _Widget
from data.utils.board_helpers import create_board
from data.utils.data_helpers import get_user_settings
from data.constants import CursorMode
from data.managers.cursor import cursor

class Chessboard(_Widget):
    def __init__(self, relative_width, change_cursor=True, **kwargs):
        super().__init__(relative_size=(relative_width, relative_width * 0.8), **kwargs)

        self._board_surface = None
        self._change_cursor = change_cursor
        self._cursor_is_hand = False

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
        if self._change_cursor and event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                if self._cursor_is_hand is False:
                    self._cursor_is_hand = True
                    cursor.set_mode(CursorMode.OPENHAND)
            else:
                if self._cursor_is_hand:
                    self._cursor_is_hand = False
                    cursor.set_mode(CursorMode.ARROW)