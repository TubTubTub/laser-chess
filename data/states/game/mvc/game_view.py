import pygame
from data.utils.board_helpers import create_circle_overlay, create_square_overlay, coords_to_screen_pos, screen_pos_to_coords
from data.utils.bitboard_helpers import bitboard_to_coords
from data.constants import GameEventType, Colour, StatusText, Miscellaneous, ShaderType
from data.states.game.components.piece_group import PieceGroup
from data.states.game.components.laser_draw import LaserDraw
from data.states.game.components.overlay_draw import OverlayDraw
from data.states.game.components.particles_draw import ParticlesDraw
from data.utils.data_helpers import get_user_settings
from data.states.game.widget_dict import GAME_WIDGETS
from data.components.widget_group import WidgetGroup
from data.components.custom_event import CustomEvent
from data.components.cursor import Cursor
from data.managers.window import screen, window

class GameView:
    def __init__(self, model):
        self._model = model
        self._user_settings = get_user_settings()
        self._event_to_func_map = {
            GameEventType.UPDATE_PIECES: self.handle_update_pieces,
            GameEventType.SET_LASER: self.handle_set_laser,
            GameEventType.PAUSE_CLICK: self.handle_pause,
        }
        self._model.register_listener(self.process_model_event, 'game')
        self._selected_coords = None

        self._widget_group = WidgetGroup(GAME_WIDGETS)
        self.initialise_widgets()
        
        self._board_size = GAME_WIDGETS['chessboard'].size
        self._board_position = GAME_WIDGETS['chessboard'].position
        self._square_size = self._board_size[0] / 10

        self._cursor = Cursor()
        self._laser_draw = LaserDraw(self._board_position, self._board_size)
        self._overlay_draw = OverlayDraw(self._board_position, self._board_size)
        self._particles_draw = ParticlesDraw()
        self._piece_group = PieceGroup()
        self.handle_update_pieces(toggle_timers=False)

        self.set_status_text(StatusText.PLAYER_MOVE)
    
    def initialise_widgets(self):
        GAME_WIDGETS['move_list'].reset_move_list()
        GAME_WIDGETS['move_list'].kill()

        GAME_WIDGETS['scroll_area'].set_image()
        
        GAME_WIDGETS['chessboard'].refresh_board()

        GAME_WIDGETS['blue_piece_display'].reset_piece_list()
        GAME_WIDGETS['red_piece_display'].reset_piece_list()
    
    def set_status_text(self, status):
        match status:
            case StatusText.PLAYER_MOVE:
                GAME_WIDGETS['status_text'].update_text(f"{self._model.states['ACTIVE_COLOUR'].name}'s turn to move")
            case StatusText.CPU_MOVE:
                GAME_WIDGETS['status_text'].update_text(f"CPU calculating a crazy move...")
            case StatusText.WIN:
                if self._model.states['WINNER'] == Miscellaneous.DRAW:
                    GAME_WIDGETS['status_text'].update_text(f"Game is a draw! Boring...")
                else:
                    GAME_WIDGETS['status_text'].update_text(f"{self._model.states['WINNER'].name} won!")
            case StatusText.DRAW:
                GAME_WIDGETS['status_text'].update_text(f"Game is a draw! Boring...")
    
    def handle_resize(self, resize_end=False):
        self._board_size = GAME_WIDGETS['chessboard'].size
        self._board_position = GAME_WIDGETS['chessboard'].position
        self._square_size = self._board_size[0] / 10
        
        self._piece_group.handle_resize(self._board_position, self._board_size, resize_end)
        self._widget_group.handle_resize(screen.get_size())
        self._laser_draw.handle_resize(self._board_position, self._board_size)
        self._laser_draw.handle_resize(self._board_position, self._board_size)
    
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

        if self._model.states['WINNER'] is not None:
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

            window.set_effect(ShaderType.SHAKE)

            if laser_result.piece_colour == Colour.BLUE:
                GAME_WIDGETS['red_piece_display'].add_piece(laser_result.piece_hit)
            elif laser_result.piece_colour == Colour.RED:
                GAME_WIDGETS['blue_piece_display'].add_piece(laser_result.piece_hit)

            if self._user_settings['particles']:
                self._particles_draw.add_captured_piece(
                    laser_result.piece_hit,
                    laser_result.piece_colour,
                    laser_result.piece_rotation,
                    coords_to_screen_pos(coords_to_remove, self._board_position, self._square_size),
                    self._square_size
                )
                self._particles_draw.add_sparks(
                    3,
                    (255, 0, 0) if self._model.states['ACTIVE_COLOUR'] == Colour.RED else (0, 0, 255),
                    coords_to_screen_pos(laser_result.laser_path[0][0],
                    self._board_position, self._square_size)
                )

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
        self._piece_group.draw(screen)
    
    def draw_widgets(self):
        self._widget_group.draw()
    
    def draw(self):
        self._widget_group.update()
        self._particles_draw.update()

        self.draw_widgets()
        self._overlay_draw.draw(screen)
        self.draw_pieces()
        self._laser_draw.draw(screen)
        self._particles_draw.draw(screen)

    def process_model_event(self, event):
        try:
            self._event_to_func_map.get(event.type)(event)
        except:
            raise KeyError('Event type not recognized in Game View (GameView.process_model_event):', event.type)
    
    def set_overlay_coords(self, available_coords_list, selected_coord):
        self._selected_coords = selected_coord
        self._overlay_draw.set_selected_coords(selected_coord)
        self._overlay_draw.set_available_coords(available_coords_list)
    
    def get_selected_coords(self):
        return self._selected_coords

    def convert_mouse_pos(self, event):
        clicked_coords = screen_pos_to_coords(event.pos, self._board_position, self._board_size)

        if clicked_coords:
            return CustomEvent.create_event(GameEventType.BOARD_CLICK, coords=clicked_coords)

        elif self._cursor.get_sprite_collision(event.pos, self._widget_group) is None:
            return CustomEvent.create_event(GameEventType.EMPTY_CLICK)

    def process_widget_event(self, event):
        return self._widget_group.process_event(event)