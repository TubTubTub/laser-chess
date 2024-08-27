import pygame
from data.tools import _State
from data.components.board import Board
from data.components.button import Button

from functools import partial

class Game(_State):
    def __init__(self):
        _State.__init__(self)
        self._gui_elements = []
        self.next = 'menu'
    
    def cleanup(self):
        print('cleaning')
    
    def startup(self, screen):
        self.board = Board(screen=screen)

        rotate_piece_clockwise = partial(self.board.rotate_piece, clockwise=True)
        rotate_piece_anticlockwise = partial(self.board.rotate_piece, clockwise=False)
        self._gui_elements.append(Button(screen=screen, rect=pygame.Rect(10, 10, 50, 50), colour=(255, 0, 0), func=rotate_piece_clockwise))
        self._gui_elements.append(Button(screen=screen, rect=pygame.Rect(0, 70, 50, 50), colour=(0, 255, 0), func=rotate_piece_anticlockwise))
        
        print('starting')
    
    def get_event(self, event):
        '''Handle gui events before board events because selected square gets cancelled in board events'''
        if event.type == pygame.KEYDOWN:
            self.board.handle_events(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            for element in self._gui_elements:
                element.handle_events(event)

            self.board.handle_events(event)
        if event.type == pygame.VIDEORESIZE:
            self.board.handle_events(event)
    
    def resize(self):
        self.board.resize_board()

    def draw(self):
        self.board.draw_board()

        for element in self._gui_elements:
            element.draw()

    def update(self):
        self.draw()