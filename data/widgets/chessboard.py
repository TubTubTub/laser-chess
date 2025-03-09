import pygame
from data.helpers.data_helpers import get_user_settings
from data.helpers.board_helpers import create_board
from data.widgets.bases.widget import _Widget
from data.utils.enums import CursorMode
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
        if self._change_cursor and event.type in [pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN]:
            current_cursor = cursor.get_mode()

            if self.rect.collidepoint(event.pos):
                if current_cursor == CursorMode.ARROW:
                    cursor.set_mode(CursorMode.OPENHAND)
                elif current_cursor == CursorMode.OPENHAND and (pygame.mouse.get_pressed()[0] is True or event.type == pygame.MOUSEBUTTONDOWN):
                    cursor.set_mode(CursorMode.CLOSEDHAND)
                elif current_cursor == CursorMode.CLOSEDHAND and (pygame.mouse.get_pressed()[0] is False or event.type == pygame.MOUSEBUTTONUP):
                    cursor.set_mode(CursorMode.OPENHAND)
            else:
                if current_cursor == CursorMode.OPENHAND or (current_cursor == CursorMode.CLOSEDHAND and event.type == pygame.MOUSEBUTTONUP):
                    cursor.set_mode(CursorMode.ARROW)