import pygame
from data.constants import EventType, BG_COLOUR

class GameView:
    def __init__(self, model, screen):
        self.model = model
        self._screen = pygame.display.get_surface()
        self._overlay_index = None
        self.event_to_func_map = {
            EventType.BOARD_CLICK: self.handle_board_click,
            EventType.PIECE_CLICK: self.handle_piece_click,
            EventType.WIDGET_CLICK: self.handle_widget_click,
        }

    def handle_board_click(self, event):
        raise NotImplementedError
    
    def handle_piece_click(self, event):
        raise NotImplementedError
    
    def handle_widget_click(self, event):
        raise NotImplementedError
    
    def draw_widgets(self):
        raise NotImplementedError

    def draw_board(self):
        raise NotImplementedError

    def draw_pieces(self):
        raise NotImplementedError

    def draw_overlay(self):
        if self._overlay_index is None:
            return
        
        raise NotImplementedError
    
    def draw(self):
        self._screen.fill(BG_COLOUR)
        self.draw_board()

    def process_model_event(self, event):
        self.event_to_func_map[event.type](event)