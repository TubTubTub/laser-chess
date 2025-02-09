import pygame
from data.constants import GameEventType, Colour, StatusText, Miscellaneous, ShaderType
from data.states.game.components.overlay_draw import OverlayDraw
from data.states.game.components.capture_draw import CaptureDraw
from data.states.game.components.piece_group import PieceGroup
from data.states.game.components.laser_draw import LaserDraw
from data.states.game.components.father import DragAndDrop
from data.utils.bitboard_helpers import bitboard_to_coords
from data.utils.board_helpers import screen_pos_to_coords
from data.utils.data_helpers import get_user_settings
from data.states.game.widget_dict import GAME_WIDGETS
from data.components.custom_event import CustomEvent
from data.components.widget_group import WidgetGroup
from data.components.cursor import Cursor
from data.managers.window import window
from data.managers.audio import audio
from data.assets import SFX

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
        self._widget_group.handle_resize(window.size)
        self.initialise_widgets()

        self._cursor = Cursor()
        self._laser_draw = LaserDraw(self.board_position, self.board_size)
        self._overlay_draw = OverlayDraw(self.board_position, self.board_size)
        self._drag_and_drop = DragAndDrop(self.board_position, self.board_size)
        self._capture_draw = CaptureDraw(self.board_position, self.board_size)
        self._piece_group = PieceGroup()
        self.handle_update_pieces(toggle_timers=False)

        self._hide_pieces = False

        self.set_status_text(StatusText.PLAYER_MOVE)
    
    @property
    def board_position(self):
        return GAME_WIDGETS['chessboard'].position
    
    @property
    def board_size(self):
        return GAME_WIDGETS['chessboard'].size

    @property
    def square_size(self):
        return self.board_size[0] / 10
    
    def initialise_widgets(self):
        GAME_WIDGETS['move_list'].reset_move_list()
        GAME_WIDGETS['move_list'].kill()
        GAME_WIDGETS['help'].kill()
        GAME_WIDGETS['tutorial'].kill()

        GAME_WIDGETS['scroll_area'].set_image()
        
        GAME_WIDGETS['chessboard'].refresh_board()

        GAME_WIDGETS['blue_piece_display'].reset_piece_list()
        GAME_WIDGETS['red_piece_display'].reset_piece_list()
    
    def set_status_text(self, status):
        match status:
            case StatusText.PLAYER_MOVE:
                GAME_WIDGETS['status_text'].set_text(f"{self._model.states['ACTIVE_COLOUR'].name}'s turn to move")
            case StatusText.CPU_MOVE:
                GAME_WIDGETS['status_text'].set_text(f"CPU calculating a crazy move...")
            case StatusText.WIN:
                if self._model.states['WINNER'] == Miscellaneous.DRAW:
                    GAME_WIDGETS['status_text'].set_text(f"Game is a draw! Boring...")
                else:
                    GAME_WIDGETS['status_text'].set_text(f"{self._model.states['WINNER'].name} won!")
            case StatusText.DRAW:
                GAME_WIDGETS['status_text'].set_text(f"Game is a draw! Boring...")
    
    def handle_resize(self):
        self._overlay_draw.handle_resize(self.board_position, self.board_size)
        self._capture_draw.handle_resize(self.board_position, self.board_size)
        self._piece_group.handle_resize(self.board_position, self.board_size)
        self._laser_draw.handle_resize(self.board_position, self.board_size)
        self._laser_draw.handle_resize(self.board_position, self.board_size)
        self._widget_group.handle_resize(window.size)

        if self._laser_draw.firing:
            self.update_laser_mask()
    
    def handle_update_pieces(self, event=None, toggle_timers=True):
        piece_list = self._model.get_piece_list()
        self._piece_group.initialise_pieces(piece_list, self.board_position, self.board_size)

        if event:
            GAME_WIDGETS['move_list'].append_to_move_list(event.move_notation)
            GAME_WIDGETS['scroll_area'].set_image()
            audio.play_sfx(SFX['piece_move'])

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

            audio.play_sfx(SFX['sphinx_destroy_1'])
            audio.play_sfx(SFX['sphinx_destroy_2'])
            audio.play_sfx(SFX['sphinx_destroy_3'])

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

            self._capture_draw.add_capture(
                laser_result.piece_hit,
                laser_result.piece_colour,
                laser_result.piece_rotation,
                coords_to_remove,
                laser_result.laser_path[0][0],
                self._model.states['ACTIVE_COLOUR']
            )

        self._laser_draw.add_laser(laser_result, self._model.states['ACTIVE_COLOUR'])
        self.update_laser_mask()
    
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
        elif colour == Colour.RED:
            GAME_WIDGETS['red_timer'].set_active(is_active)
    
    def update_laser_mask(self):
        temp_surface = pygame.Surface(window.size, pygame.SRCALPHA)
        self._piece_group.draw(temp_surface)
        mask = pygame.mask.from_surface(temp_surface, threshold=127)
        mask_surface = mask.to_surface(unsetcolor=(0, 0, 0, 255), setcolor=(255, 0, 0, 255))

        window.set_apply_arguments(ShaderType.RAYS, occlusion=mask_surface)
    
    def draw(self):
        self._widget_group.update()
        self._capture_draw.update()

        self._widget_group.draw()
        self._overlay_draw.draw(window.screen)

        if self._hide_pieces is False:
            self._piece_group.draw(window.screen)
            
        self._laser_draw.draw(window.screen)
        self._drag_and_drop.draw(window.screen)
        self._capture_draw.draw(window.screen)

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

    def set_dragged_piece(self, piece, colour, rotation):
        self._drag_and_drop.set_dragged_piece(piece, colour, rotation)
    
    def remove_dragged_piece(self):
        self._drag_and_drop.remove_dragged_piece()

    def convert_mouse_pos(self, event):
        clicked_coords = screen_pos_to_coords(event.pos, self.board_position, self.board_size)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if clicked_coords:
                return CustomEvent.create_event(GameEventType.BOARD_CLICK, coords=clicked_coords)

            else:
                return None

        elif event.type == pygame.MOUSEBUTTONUP:
            if self._drag_and_drop.dragged_sprite:
                piece, colour, rotation = self._drag_and_drop.get_dragged_info()
                piece_dragged = self._drag_and_drop.remove_dragged_piece()
                return CustomEvent.create_event(GameEventType.PIECE_DROP, coords=clicked_coords, piece=piece, colour=colour, rotation=rotation, remove_overlay=piece_dragged)
    
    def add_help_screen(self):
        self._widget_group.add(GAME_WIDGETS['help'])
        self._widget_group.handle_resize(window.size)
    
    def add_tutorial_screen(self):
        self._widget_group.add(GAME_WIDGETS['tutorial'])
        self._widget_group.handle_resize(window.size)
        self._hide_pieces = True
            
    def remove_help_screen(self):
        GAME_WIDGETS['help'].kill()
            
    def remove_tutorial_screen(self):
        GAME_WIDGETS['tutorial'].kill()
        self._hide_pieces = False

    def process_widget_event(self, event):
        return self._widget_group.process_event(event)