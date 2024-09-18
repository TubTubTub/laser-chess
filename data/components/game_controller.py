import pygame
from data.constants import EventType
from data.utils import bitboard_helpers as bb_helpers

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

                    clicked_bitboard = bb_helpers.coords_to_bitboard(game_event.coords)
                    valid_squares = bb_helpers.bitboard_to_coords_list(self._model.get_valid_squares(clicked_bitboard))
                    overlay_coords = self._view.get_overlay_coords()

                    if not overlay_coords:
                        self._view.set_overlay_coords(valid_squares)
                    else:
                        if game_event.coords in overlay_coords:
                            print('processing')
                        else:
                            self._view.set_overlay_coords([])
                        
                case EventType.EMPTY_CLICK:
                    self._view.set_square_overlay(None)
                case _:
                    raise Exception('Unhandled event type (GameController.handle_event)')