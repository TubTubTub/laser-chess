import pygame
from data.constants import GameEventType, MoveType, EMPTY_BB
from data.utils import bitboard_helpers as bb_helpers
from data.components.move import Move

class GameController:
    def __init__(self, model, view, pause_view):
        self._model = model
        self._view = view
        self._pause_view = pause_view
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self._model.states['PAUSED']:
                game_event = self._pause_view.convert_mouse_pos(event.pos)

                match game_event.type:
                    case GameEventType.PAUSE_CLICK:
                        self._model.toggle_paused()
                    
                    case GameEventType.EMPTY_CLICK:
                        pass
                
                return

            # print('MOUSEBUTTONDOWN:', event.pos)
            game_event = self._view.convert_mouse_pos(event.pos)
            
            match game_event.type:

                case GameEventType.BOARD_CLICK:
                    # print('COORDS:', game_event.coords)

                    if self._model.states['AWAITING_CPU']:
                        return

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
                            self.make_move(move)
                        else:
                            self._view.set_overlay_coords([], None)

                case GameEventType.WIDGET_CLICK:
                    print('widget clicked!')
                        
                case GameEventType.EMPTY_CLICK:
                    self._view.set_overlay_coords([], None)
                
                case GameEventType.ROTATE_PIECE:
                    src_coords = self._view.get_selected_overlay_coord()

                    if src_coords is None:
                        print('None square selected')
                        return

                    move = Move.instance_from_coords(MoveType.ROTATE, src_coords, src_coords, rotation_direction=game_event.rotation_direction)
                    self.make_move(move)

                case _:
                    raise Exception('Unhandled event type (GameController.handle_event)')

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._model.toggle_paused()
            elif event.key == pygame.K_l:
                print('stopping')
                self._model.thread_stop.set()

    def make_move(self, move):
        self._model.make_move(move)
        self._view.set_overlay_coords([], None)
        self.check_game_over()

        if self._model.states['CPU']:
            self._model.make_cpu_move()
            self.check_game_over()
    
    def check_game_over(self):
        winner = self._model.states['WINNER']
        if winner is not None:
            print(winner.name, 'WON')