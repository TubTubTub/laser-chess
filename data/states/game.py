import pygame
from data.tools import _State
from data.components.board import Board
from data.components.elements import Label, Button
from data.utils.settings_helpers import app_settings

from functools import partial

class Game(_State):
    def __init__(self):
        super().__init__()
        self._gui_elements = []
        self.next = 'menu'
    
    def cleanup(self):
        print('cleaning')
    
    def startup(self, screen):
        self.board = Board(app_settings=app_settings, screen=screen)

        rotate_piece_clockwise = partial(self.board.rotate_piece, clockwise=True)
        rotate_piece_anticlockwise = partial(self.board.rotate_piece, clockwise=False)
        self._gui_elements = {
            'label': Label(screen=screen, position=(10, 300), text="jamesdssdss", text_colour=(0, 0, 0), margin=15, label_colour=(20, 100, 1), border_radius=50, border_width=0),
            'clockwise_button': Button(screen=screen, position=(30, 10), text="clockwise", func=rotate_piece_clockwise, text_colour=(255, 0, 0), label_colour=(0, 255, 255), width=100, height=50),
            'anticlockwise_button': Button(screen=screen, position=(30, 100), text="anticlockwise", func=rotate_piece_anticlockwise, text_colour=(0, 0, 0), label_colour=(0, 255, 0), margin=50),
        }
        
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
            self.board.handle_events(event)
    
    def handle_resize(self):
        self.board.handle_resize()
        for element in self._gui_elements.values():
            element.handle_resize()

    def draw(self):
        self.board.draw_board()

        for element in self._gui_elements.values():
            element.draw()

    def update(self):
        board_clicked = self.board.clicked
        if board_clicked:
            self.board.handle_click()
            self._gui_elements['label'].text = self.board.status_text

        if self.board.has_moved_piece:
            print('firing')
            self.board.fire_laser()

            game_won_by = self.board.check_win()

            if game_won_by:
                print('quit', game_won_by)

            self.board.bitboards.flip_colour()
            
            self.board.has_moved_piece = False
        self.draw()