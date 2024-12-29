import pygame
from data.constants import GameEventType, MoveType, Colour, StatusText, Miscellaneous
from data.utils import bitboard_helpers as bb_helpers
from data.states.game.components.move import Move

class GameController:
    def __init__(self, model, view, win_view, pause_view, to_menu, to_new_game):
        self._model = model
        self._view = view
        self._win_view = win_view
        self._pause_view = pause_view

        self._to_menu = to_menu
        self._to_new_game = to_new_game

        self._view.initialise_timers()
    
    def handle_event(self, event):
        if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]:
            if self._model.states['PAUSED']:
                self.handle_pause_event(event)
            elif self._model.states['WINNER'] is not None:
                self.handle_winner_event(event)
            else:
                self.handle_game_event(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._model.toggle_paused()
            elif event.key == pygame.K_l:
                self._model.thread_stop.set()

    def handle_pause_event(self, event):
        game_event = self._pause_view.convert_mouse_pos(event)

        if game_event is None:
            return

        match game_event.type:
            case GameEventType.PAUSE_CLICK:
                self._model.toggle_paused()
            
            case GameEventType.MENU_CLICK:
                self._to_menu()

            case _:
                raise Exception('Unhandled event type (GameController.handle_event)')
    
    def handle_winner_event(self, event):
        game_event = self._win_view.convert_mouse_pos(event)

        if game_event is None:
            return

        match game_event.type:
            case GameEventType.MENU_CLICK:
                self._to_menu()
            
            case GameEventType.GAME_CLICK:
                self._to_new_game()

            case _:
                raise Exception('Unhandled event type (GameController.handle_event)')

    def handle_game_widget_event(self, event):
        widget_event = self._view.process_widget_event(event)

        if widget_event is None:
            return None

        match widget_event.type:
            case GameEventType.ROTATE_PIECE:
                src_coords = self._view.get_selected_coords()

                if src_coords is None:
                    print('None square selected')
                    return

                move = Move.instance_from_coords(MoveType.ROTATE, src_coords, src_coords, rotation_direction=widget_event.rotation_direction)
                self.make_move(move)
            
            case GameEventType.RESIGN_CLICK:
                self._model.set_winner(self._model.states['ACTIVE_COLOUR'].get_flipped_colour())
                self._view.set_status_text(StatusText.WIN)
                self.check_game_over()
                return
                
            case GameEventType.DRAW_CLICK:
                self._model.set_winner(Miscellaneous.DRAW)
                self._view.set_status_text(StatusText.DRAW)
                self.check_game_over()
                return
                
            case GameEventType.TIMER_END:
                self._model.set_winner(widget_event.active_colour.get_flipped_colour())
                return
            
            case _:
                raise Exception('Unhandled event type (GameController.handle_event)')

    def handle_game_event(self, event):
        self.handle_game_widget_event(event)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            game_event = self._view.convert_mouse_pos(event)

            if game_event is None:
                return

            match game_event.type:
                case GameEventType.BOARD_CLICK:
                    if self._model.states['AWAITING_CPU']:
                        return

                    clicked_bitboard = bb_helpers.coords_to_bitboard(game_event.coords)

                    if self._view.get_selected_coords():
                        src_coords = self._view.get_selected_coords()
                        possible_move_coords = self._model.get_clicked_coords(bb_helpers.coords_to_bitboard(src_coords))

                        if game_event.coords in possible_move_coords:
                            src_coords = self._view.get_selected_coords()
                            move = Move.instance_from_coords(MoveType.MOVE, src_coords, game_event.coords)
                            self.make_move(move)
                        else:
                            self._view.set_overlay_coords(None, None)
                    else:
                        possible_move_coords = self._model.get_clicked_coords(clicked_bitboard)
                        if possible_move_coords:
                            self._view.set_overlay_coords(possible_move_coords, game_event.coords)

                case GameEventType.EMPTY_CLICK:
                    self._view.set_overlay_coords(None, None)
                    return

                case _:
                    raise Exception('Unhandled event type (GameController.handle_event)')

    def make_move(self, move):
        self._model.make_move(move)
        self._view.set_overlay_coords([], None)
        self.check_game_over()

        if self._model.states['CPU_ENABLED']:
            self._model.make_cpu_move()
            self.check_game_over()
    
    def check_game_over(self):
        winner = self._model.states['WINNER']
        if winner is not None:
            print('\n(GameController.check_game_over) Handling game end!', winner.name)
            self._view.toggle_timer(Colour.BLUE, False)
            self._view.toggle_timer(Colour.RED, False)