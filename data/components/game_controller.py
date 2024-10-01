import pygame
from data.constants import GameState, EventType, MoveType, EMPTY_BB
from data.utils import bitboard_helpers as bb_helpers
from data.components.move import Move
from data.components.cpu import CPU

class GameController:
    def __init__(self, model, view):
        self._model = model
        self._view = view
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # print('MOUSEBUTTONDOWN:', event.pos)
            game_event = self._view.convert_mouse_pos(event.pos)
            
            match game_event.type:

                case EventType.BOARD_CLICK:
                    # print('COORDS:', game_event.coords)

                    clicked_bitboard = bb_helpers.coords_to_bitboard(game_event.coords)
                    current_selected = self._view.get_selected_overlay_coord()

                    if not current_selected:
                        possible_move_coords = self._model.get_clicked_coords(clicked_bitboard)

                        if possible_move_coords:
                            self._view.set_overlay_coords(possible_move_coords, game_event.coords)
                    else:
                        current_overlays = self._view.get_valid_overlay_coords()

                        if game_event.coords in current_overlays:
                            src_coords = self._view.get_selected_overlay_coord()
                            move = Move.instance_from_coords(MoveType.MOVE, src_coords, game_event.coords)

                            self.apply_player_move(move)
                            self.apply_cpu_move()
                        else:
                            self._view.set_overlay_coords([], None)

                case EventType.WIDGET_CLICK:
                    print('widget clicked!')
                        
                case EventType.EMPTY_CLICK:
                    self._view.set_overlay_coords([], None)
                
                case EventType.ROTATE_PIECE:
                    src_coords = self._view.get_selected_overlay_coord()

                    if src_coords is None:
                        print('None')
                        return

                    move = Move.instance_from_coords(MoveType.ROTATE, src_coords, src_coords, rotation_direction=game_event.rotation_direction)

                    self.apply_player_move(move)

                case _:
                    raise Exception('Unhandled event type (GameController.handle_event)')
    
    def apply_player_move(self, move):
        self._model.make_move(move)
        
        self._view.set_overlay_coords([], None)
    
    def apply_cpu_move(self):
        cpu = CPU(self._model.get_board(), depth=3)
        move = cpu.find_best_move()
        self._model.make_move(move)
    
    def check_game_over(self):
        if self._model.winner is not None:
            print(self._model.winner.name, 'WON')