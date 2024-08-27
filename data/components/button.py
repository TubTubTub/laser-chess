import pygame

class Button:
    def __init__(self, screen, rect, colour, func, text=None, icon=None):
        self._screen = screen
        self._colour = colour
        self._rect = rect
        self._func = func
    
    def draw(self):
        pygame.draw.rect(self._screen, self._colour, self._rect)
    
    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self._rect.collidepoint(event.pos):
                self._func()