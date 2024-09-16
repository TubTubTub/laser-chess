import pygame
from data.tools import _State
from data.components.board import Board
from data.components.gameview import GameView

class Game(_State):
    def __init__(self):
        super().__init__()
        self._gui_elements = []
        self.next = 'menu'
    
    def cleanup(self):
        print('cleaning')
    
    def startup(self):
        self.board = Board()
        self.view = GameView(self.board)

        self.view.draw()
        print('starting')
    
    def get_event(self, event):
        '''Handle gui events before board events because selected square gets cancelled in board events'''
        if event.type == pygame.KEYDOWN:
            self.board.handle_events(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            for element in self._gui_elements.values():
                element.handle_events(event)

            self.board.handle_events(event)
        if event.type == pygame.VIDEORESIZE:
            self.view.handle_resize(resize_end=True)
    
    def handle_resize(self):
        self.view.handle_resize()

    def draw(self):
        self.view.draw()

    def update(self):
        # board_clicked = self.board.clicked
        # if board_clicked:
        #     self.board.handle_click()
        #     self._gui_elements['label'].text = self.board.status_text

        # if self.board.has_moved_piece:
        #     print('firing')
        #     self.board.fire_laser()

        #     game_won_by = self.board.check_win()

        #     if game_won_by:
        #         print('quit', game_won_by)

        #     self.board.bitboards.flip_colour()
            
        #     self.board.has_moved_piece = False
        self.draw()