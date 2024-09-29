import pygame
from data.tools import _State
from data.components.game_model import GameModel
from data.components.game_view import GameView
from data.components.game_controller import GameController

class Game(_State):
    def __init__(self):
        super().__init__()
        self.next = 'menu'
    
    def cleanup(self):
        print('cleaning')
    
    def startup(self):
        self.model = GameModel()
        self.view = GameView(self.model)
        self.controller = GameController(self.model, self.view)

        self.view.draw()
        print('starting')
    
    def get_event(self, event):
        '''Handle gui events before board events because selected square gets cancelled in board events'''
        if event.type == pygame.VIDEORESIZE:
            self.view.handle_resize(resize_end=True)
        else:
            self.controller.handle_event(event)
    
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