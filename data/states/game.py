import pygame
from data.tools import _State
from data.components.board import Board

class Game(_State):
    def __init__(self):
        _State.__init__(self)
        self.next = 'menu'
    
    def cleanup(self):
        print('cleaning')
    
    def startup(self, screen):
        self.board = Board(screen=screen)
        print('starting')
    
    def get_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.board.process_mouse_press(event)
        if event.type == pygame.VIDEORESIZE:
            self.board.process_resize_finish()
    
    def resize(self):
        self.board.resize_board()

    def draw(self):
        self.board.draw_board()
    
    def update(self):
        self.draw()