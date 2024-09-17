import pygame

class GameController:
    def __init__(self, model, view):
        self._model = model
        self._view = view
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            print('MOUSEBUTTONDOWN:', event.pos)