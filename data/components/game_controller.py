import pygame
from data.constants import EventType

class GameController:
    def __init__(self, model, view):
        self._model = model
        self._view = view
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            print('MOUSEBUTTONDOWN:', event.pos)
            game_event = self._view.convert_mouse_pos(event.pos)
            
            match game_event.event_type:
                case EventType.BOARD_CLICK:
                    print('COORDS:', game_event.coords)
                    self._view.set_square_overlay(game_event.coords)