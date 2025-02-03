import pygame
from data.constants import GameEventType, MoveType, StatusText, Miscellaneous
from data.utils import bitboard_helpers as bb_helpers
from data.states.game.components.move import Move
from data.managers.logs import initialise_logger

logger = initialise_logger(__name__)

class GameController:
    def __init__(self, model, view, win_view, pause_view, to_menu, to_new_game):
        self._model = model
        self._view = view
        self._win_view = win_view
        self._pause_view = pause_view

        self._to_menu = to_menu
        self._to_new_game = to_new_game

        self._view.initialise_timers()
    
    def cleanup(self, next):
        self._model.kill_thread()

        if next == 'menu':
            self._to_menu()
        elif next == 'game':
            self._to_new_game()

    def make_move(self, move):
        self._model.make_move(move)
        self._view.set_overlay_coords([], None)

        if self._model.states['CPU_ENABLED']:
            self._model.make_cpu_move()

    def handle_pause_event(self, event):
        game_event = self._pause_view.convert_mouse_pos(event)

        if game_event is None:
            return

        match game_event.type:
            case GameEventType.PAUSE_CLICK:
                self._model.toggle_paused()
            
            case GameEventType.MENU_CLICK:
                self.cleanup('menu')

            case _:
                raise Exception('Unhandled event type (GameController.handle_event)')
    
    def handle_winner_event(self, event):
        game_event = self._win_view.convert_mouse_pos(event)

        if game_event is None:
            return

        match game_event.type:
            case GameEventType.MENU_CLICK:
                self.cleanup('menu')
                return
            
            case GameEventType.GAME_CLICK:
                self.cleanup('game')
                return

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
                    logger.info('None square selected')
                    return

                move = Move.instance_from_coords(MoveType.ROTATE, src_coords, src_coords, rotation_direction=widget_event.rotation_direction)
                self.make_move(move)
            
            case GameEventType.RESIGN_CLICK:
                self._model.set_winner(self._model.states['ACTIVE_COLOUR'].get_flipped_colour())
                self._view.set_status_text(StatusText.WIN)
                
            case GameEventType.DRAW_CLICK:
                self._model.set_winner(Miscellaneous.DRAW)
                self._view.set_status_text(StatusText.DRAW)
                
            case GameEventType.TIMER_END:
                self._model.set_winner(widget_event.active_colour.get_flipped_colour())
            
            case GameEventType.MENU_CLICK:
                self.cleanup('menu')
            
            case GameEventType.HELP_CLICK:
                self._view.add_help_screen()
            
            case _:
                raise Exception('Unhandled event type (GameController.handle_event)')
        
        return widget_event.type

    def handle_game_event(self, event):
        widget_event = self.handle_game_widget_event(event)
        
        if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.KEYDOWN]:
            game_event = self._view.convert_mouse_pos(event)

            if game_event is None:
                if widget_event is None:
                    if event.type in [pygame.MOUSEBUTTONUP, pygame.KEYDOWN]:
                        self._view.remove_help_screen()
                    if event.type == pygame.MOUSEBUTTONUP:
                        self._view.set_overlay_coords(None, None)
                    
                return

            match game_event.type:
                case GameEventType.BOARD_CLICK:
                    if self._model.states['AWAITING_CPU']:
                        return

                    clicked_coords = game_event.coords
                    clicked_bitboard = bb_helpers.coords_to_bitboard(clicked_coords)
                    selected_coords = self._view.get_selected_coords()

                    if selected_coords:
                        if clicked_coords == selected_coords:
                            self._view.set_dragged_piece(*self._model.get_piece_info(clicked_bitboard))
                            return
                        
                        selected_bitboard = bb_helpers.coords_to_bitboard(selected_coords)
                        available_bitboard = self._model.get_available_moves(selected_bitboard)

                        if bb_helpers.is_occupied(clicked_bitboard, available_bitboard):
                            move = Move.instance_from_coords(MoveType.MOVE, selected_coords, clicked_coords)
                            self.make_move(move)
                        else:
                            self._view.set_overlay_coords(None, None)
                            
                    elif self._model.is_selectable(clicked_bitboard):
                        available_bitboard = self._model.get_available_moves(clicked_bitboard)
                        self._view.set_overlay_coords(bb_helpers.bitboard_to_coords_list(available_bitboard), clicked_coords)
                        self._view.set_dragged_piece(*self._model.get_piece_info(clicked_bitboard))

                case GameEventType.PIECE_DROP:
                    hovered_coords = game_event.coords

                    if hovered_coords:
                        hovered_bitboard = bb_helpers.coords_to_bitboard(hovered_coords)
                        selected_coords = self._view.get_selected_coords()
                        selected_bitboard = bb_helpers.coords_to_bitboard(selected_coords)
                        available_bitboard = self._model.get_available_moves(selected_bitboard)

                        if bb_helpers.is_occupied(hovered_bitboard, available_bitboard):
                            move = Move.instance_from_coords(MoveType.MOVE, selected_coords, hovered_coords)
                            self.make_move(move)

                    if game_event.remove_overlay:
                        self._view.set_overlay_coords(None, None)

                    self._view.remove_dragged_piece()

                case _:
                    raise Exception('Unhandled event type (GameController.handle_event)', game_event.type)
    
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
                logger.info('\nSTOPPING CPU')
                self._model._cpu_thread.stop_cpu() #temp