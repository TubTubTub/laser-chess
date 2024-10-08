import pygame
from data.tools import _State
from data.states.game.components.game_model import GameModel
from data.states.game.components.game_view import GameView
from data.states.game.components.game_controller import GameController
from data.states.game.components.pause_view import PauseView
from data.states.game.components.win_view import WinView
from data.constants import BG_COLOUR

class Game(_State):
    def __init__(self):
        super().__init__()
        self.next = 'menu'
        self._screen = pygame.display.get_surface()
    
    def cleanup(self):
        print('cleaning game.py')
    
    def switch_to_menu(self):
        self.done = True
    
    def startup(self, persist):
        self.model = GameModel(**persist)
        self.view = GameView(self.model)
        self.pause_view = PauseView(self.model)
        self.win_view = WinView(self.model)
        self.controller = GameController(self.model, self.view, self.win_view, self.pause_view, self.switch_to_menu, self.startup)

        self.view.draw()
        print('starting game.py')
    
    def get_event(self, event):
        '''Handle gui events before board events because selected square gets cancelled in board events'''
        if event.type == pygame.VIDEORESIZE:
            self.view.handle_resize(resize_end=True)
        else:
            self.controller.handle_event(event)
    
    def handle_resize(self):
        self.view.handle_resize()
        self.win_view.handle_resize()
        self.pause_view.handle_resize()

    def draw(self):
        self._screen.fill(BG_COLOUR)
        self.view.draw()
        self.win_view.draw()
        self.pause_view.draw()

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