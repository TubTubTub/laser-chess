import pygame
from data.utils.board_helpers import create_circle_overlay, create_square_overlay, coords_to_screen_pos, screen_pos_to_coords
from data.utils.bitboard_helpers import bitboard_to_coords
from data.constants import GameEventType, Colour, StatusText, OVERLAY_COLOUR
from data.states.game.components.piece_group import PieceGroup
from data.states.game.components.laser_draw import LaserDraw
from data.utils.data_helpers import get_user_settings
from data.states.game.widget_dict import GAME_WIDGETS
from data.components.widget_group import WidgetGroup
from data.components.custom_event import CustomEvent
from data.components.cursor import Cursor

class GameView:
    def __init__(self, model):
        self._model = model
        self._screen = pygame.display.get_surface()
        self._user_settings = get_user_settings()
        self._event_to_func_map = {
            GameEventType.UPDATE_PIECES: self.handle_update_pieces,
            GameEventType.SET_LASER: self.handle_set_laser,
            GameEventType.PAUSE_CLICK: self.handle_pause,
        }
        self._model.register_listener(self.process_model_event, 'game')

        self._widget_group = WidgetGroup(GAME_WIDGETS)
        GAME_WIDGETS['move_list'].reset_move_list()
        GAME_WIDGETS['move_list'].kill()
        GAME_WIDGETS['scroll_area'].set_image()
        
        GAME_WIDGETS['chessboard'].refresh_board()
        
        self._board_size = GAME_WIDGETS['chessboard'].size
        self._board_position = GAME_WIDGETS['chessboard'].position
        self._square_size = self._board_size[0] / 10

        self._cursor = Cursor()

        self._piece_group = PieceGroup()
        self.handle_update_pieces(toggle_timers=False)

        self._laser_draw = LaserDraw(self._board_position, self._board_size)

        self.set_status_text(StatusText.PLAYER_MOVE)
        
        self._valid_overlay_coords = []
        self._selected_overlay_coord = None

        self._circle_overlay = create_circle_overlay(self._square_size, OVERLAY_COLOUR)
        self._square_overlay = create_square_overlay(self._square_size, OVERLAY_COLOUR)
        self._circle_overlay_unscaled = self._circle_overlay.copy()
        self._square_overlay_unscaled = self._square_overlay.copy()
    
    def set_status_text(self, status):
        match status:
            case StatusText.PLAYER_MOVE:
                GAME_WIDGETS['status_text'].update_text(f"{self._model.states['ACTIVE_COLOUR'].name}'s turn to move")
            case StatusText.CPU_MOVE:
                GAME_WIDGETS['status_text'].update_text(f"CPU calculating a crazy move...")
            case StatusText.WIN:
                GAME_WIDGETS['status_text'].update_text(f"{self._model.states['WINNER'].name} won!")
            case StatusText.DRAW:
                GAME_WIDGETS['status_text'].update_text(f"Game is a draw! Boring...")
    
    def handle_resize(self, resize_end=False):
        self._board_size = GAME_WIDGETS['chessboard'].size
        self._board_position = GAME_WIDGETS['chessboard'].position
        self._square_size = self._board_size[0] / 10
        
        self._piece_group.handle_resize(self._board_position, self._board_size, resize_end)
        self._widget_group.handle_resize(self._screen.get_size())
        self._laser_draw.handle_resize(self._board_position, self._board_size)

        self._circle_overlay = pygame.transform.scale(self._circle_overlay_unscaled, (self._square_size, self._square_size))
        self._square_overlay = pygame.transform.scale(self._square_overlay_unscaled, (self._square_size, self._square_size))
    
    def handle_update_pieces(self, event=None, toggle_timers=True):
        piece_list = self._model.get_piece_list()
        self._piece_group.initialise_pieces(piece_list, self._board_position, self._board_size)

        if event:
            GAME_WIDGETS['move_list'].append_to_move_list(event.move_notation)
            GAME_WIDGETS['scroll_area'].set_image()

        if self._model.states['ACTIVE_COLOUR'] == Colour.BLUE:
            self.set_status_text(StatusText.PLAYER_MOVE)
        elif self._model.states['CPU_ENABLED'] is False:
            self.set_status_text(StatusText.PLAYER_MOVE)
        else:
            self.set_status_text(StatusText.CPU_MOVE)

        if self._model.states['WINNER']:
            self.toggle_timer(self._model.states['ACTIVE_COLOUR'], False)
            self.toggle_timer(self._model.states['ACTIVE_COLOUR'].get_flipped_colour(), False)

            self.set_status_text(StatusText.WIN)

        elif toggle_timers:
            self.toggle_timer(self._model.states['ACTIVE_COLOUR'], True)
            self.toggle_timer(self._model.states['ACTIVE_COLOUR'].get_flipped_colour(), False)
    
    def handle_set_laser(self, event):
        laser_result = event.laser_result
        if laser_result.hit_square_bitboard:
            coords_to_remove = bitboard_to_coords(laser_result.hit_square_bitboard)
            self._piece_group.remove_piece(coords_to_remove)

            if laser_result.piece_colour == Colour.BLUE:
                GAME_WIDGETS['red_piece_display'].add_piece(laser_result.piece_hit)
            elif laser_result.piece_colour == Colour.RED:
                GAME_WIDGETS['blue_piece_display'].add_piece(laser_result.piece_hit)

        self._laser_draw.add_laser(laser_result, self._model.states['ACTIVE_COLOUR'])
    
    def handle_pause(self, event):
        is_active = not(self._model.states['PAUSED'])
        self.toggle_timer(self._model.states['ACTIVE_COLOUR'], is_active)
    
    def initialise_timers(self):
        if self._model.states['TIME_ENABLED']:
            GAME_WIDGETS['blue_timer'].set_time(self._model.states['TIME'] * 60 * 1000)
            GAME_WIDGETS['red_timer'].set_time(self._model.states['TIME'] * 60 * 1000)
        else:
            GAME_WIDGETS['blue_timer'].kill()
            GAME_WIDGETS['red_timer'].kill()

        self.toggle_timer(self._model.states['ACTIVE_COLOUR'], True)

    def toggle_timer(self, colour, is_active):
        if colour == Colour.BLUE:
            GAME_WIDGETS['blue_timer'].set_active(is_active)
        else:
            GAME_WIDGETS['red_timer'].set_active(is_active)

    def draw_pieces(self):
        self._piece_group.draw(self._screen)
    
    def draw_widgets(self):
        self._widget_group.draw()

    def draw_overlay(self):
        if not self._selected_overlay_coord:
            return
        
        square_x, square_y = coords_to_screen_pos(self._selected_overlay_coord, self._board_position, self._square_size)
        self._screen.blit(self._square_overlay, (square_x, square_y))

        for coords in self._valid_overlay_coords:
            square_x, square_y = coords_to_screen_pos(coords, self._board_position, self._square_size)
            self._screen.blit(self._circle_overlay, (square_x, square_y))
    
    def draw(self):
        self._widget_group.update()
        self.draw_widgets()
        self.draw_pieces()
        self._laser_draw.draw()
        self.draw_overlay()

    def process_model_event(self, event):
        try:
            self._event_to_func_map.get(event.type)(event)
        except:
            raise KeyError('Event type not recognized in Game View (GameView.process_model_event):', event.type)
    
    def set_overlay_coords(self, possible_coords_list, selected_coord):
        self._valid_overlay_coords = possible_coords_list
        self._selected_overlay_coord = selected_coord
    
    def get_valid_overlay_coords(self):
        return self._valid_overlay_coords
    
    def get_selected_overlay_coord(self):
        return self._selected_overlay_coord

    def convert_mouse_pos(self, event):
        clicked_coords = screen_pos_to_coords(event.pos, self._board_position, self._board_size)

        if clicked_coords:
            return CustomEvent.create_event(GameEventType.BOARD_CLICK, coords=clicked_coords)

        elif self._cursor.get_sprite_collision(event.pos, self._widget_group) is None:
            return CustomEvent.create_event(GameEventType.EMPTY_CLICK)

    def process_widget_event(self, event):
        return self._widget_group.process_event(event)