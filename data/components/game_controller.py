import pygame
from data.constants import EventType, EMPTY_BB
from data.utils import bitboard_helpers as bb_helpers
from data.components.move import Move

class GameController:
    def __init__(self, model, view):
        self._model = model
        self._view = view
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            print('MOUSEBUTTONDOWN:', event.pos)
            game_event = self._view.convert_mouse_pos(event.pos)
            
            match game_event.type:

                case EventType.BOARD_CLICK:
                    print('COORDS:', game_event.coords)

                    clicked_bitboard = bb_helpers.coords_to_bitboard(game_event.coords)
                    current_selected = self._view.get_selected_overlay_coord()

                    if not current_selected:
                        if (clicked_bitboard & self._model.get_all_active_pieces()) != EMPTY_BB:
                            possible_move_coords = bb_helpers.bitboard_to_coords_list(self._model.get_valid_squares(clicked_bitboard))
                            self._view.set_overlay_coords(possible_move_coords, game_event.coords)
                        else:
                            return

                    else:
                        current_overlays = self._view.get_valid_overlay_coords()

                        if game_event.coords in current_overlays:
                            src_coords = self._view.get_selected_overlay_coord()
                            move = Move.instance_from_coords(src_coords, game_event.coords)

                            self._model.apply_move(move)
                            self._model.fire_laser()
                            self._model.flip_colour()
                            
                            self._view.set_overlay_coords([], None)
                        else:
                            self._view.set_overlay_coords([], None)
                        
                case EventType.EMPTY_CLICK:
                    self._view.set_overlay_coords([], None)
                case _:
                    raise Exception('Unhandled event type (GameController.handle_event)')