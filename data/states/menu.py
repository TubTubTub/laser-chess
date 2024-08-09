import pygame
from data.tools import _State

class Menu(_State):
    def __init__(self):
        _State.__init__(self)
        self.next = 'game'
    
    def cleanup(self):
        print('cleaning')
    
    def startup(self):
        print('starting')
    
    def get_event(self, event):
        if event.type == pygame.KEYDOWN:
            print('key down')
            self.done = True
    
    def resize(self):
        print('NOT IMPLEMENTED RESIZING YET BOY!')
    
    def draw(self, screen):
        screen.fill((255, 255, 0))
        pygame.draw.rect(screen, pygame.Color('red'), pygame.Rect(10, 10, 50, 50).inflate(-10, -10))
    
    def update(self, screen):
        self.draw(screen)