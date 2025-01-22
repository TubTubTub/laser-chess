import pygame
import pyperclip
from data.control import _State
from data.components.widget_group import WidgetGroup
from data.states.setup.widget_dict import SETUP_WIDGETS
from data.constants import SetupEventType, Colour, RotationDirection, Piece, Rotation
from data.states.game.components.bitboard_collection import BitboardCollection
from data.states.game.components.overlay_draw import OverlayDraw
from data.states.game.components.piece_group import PieceGroup
from data.states.game.components.father import DragAndDrop
from data.components.cursor import Cursor
from data.assets import GRAPHICS, MUSIC_PATHS
from data.utils.bitboard_helpers import coords_to_bitboard
from data.utils.asset_helpers import draw_background
from data.utils.board_helpers import screen_pos_to_coords
from data.states.game.components.fen_parser import encode_fen_string
from data.managers.audio import audio
from data.managers.animation import animation
from data.managers.window import window

class Setup(_State):
    def __init__(self):
        super().__init__()
        self._cursor = Cursor()

        self._bitboards = None
        self._piece_group = None
        self._selected_coords = None
        self._selected_tool = None
        self._selected_tool_colour = None
        self._initial_fen_string = None
        self._starting_colour = None
        
        self._drag_and_drop = None
        self._overlay_draw = None
        self._widget_group = None
    
    def cleanup(self):
        print('cleaning setup.py')

        self.deselect_tool()

        return encode_fen_string(self._bitboards)
    
    def startup(self, persist):
        print('starting setup.py')
        self._widget_group = WidgetGroup(SETUP_WIDGETS)
        self._widget_group.handle_resize(window.size)

        self._drag_and_drop = DragAndDrop(SETUP_WIDGETS['chessboard'].position, SETUP_WIDGETS['chessboard'].size)
        self._overlay_draw = OverlayDraw(SETUP_WIDGETS['chessboard'].position, SETUP_WIDGETS['chessboard'].size)
        self._bitboards = BitboardCollection(persist['FEN_STRING'])
        self._initial_fen_string = persist['FEN_STRING']
        self._piece_group = PieceGroup()
        self._selected_coords = None
        self._selected_tool = None
        self._selected_tool_colour = None
        self._starting_colour = Colour.BLUE

        self.set_starting_colour(Colour.BLUE)

        # audio.play_music(MUSIC_PATHS['setup'])
        
        self.refresh_pieces()
        self.set_starting_colour(Colour.BLUE if persist['FEN_STRING'][-1].lower() == 'b' else Colour.RED)
        self.draw()
    
    @property
    def selected_coords(self):
        return self._selected_coords
    
    @selected_coords.setter
    def selected_coords(self, new_coords):
        self._overlay_draw.set_selected_coords(new_coords)
        self._selected_coords = new_coords
    
    def get_event(self, event):
        if event.type == pygame.VIDEORESIZE:
            self.handle_resize(resize_end=True)
            return
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked_coords = screen_pos_to_coords(event.pos, SETUP_WIDGETS['chessboard'].position, SETUP_WIDGETS['chessboard'].size)

            if clicked_coords:
                self.selected_coords = clicked_coords

                if self._selected_tool is None:
                    return

                if self._selected_tool == 'MOVE':
                    self.set_dragged_piece(clicked_coords)

                elif self._selected_tool == 'ERASE':
                    self.remove_piece()
                else:
                    self.set_piece(self._selected_tool, self._selected_tool_colour, Rotation.UP)
                    
                return
        
        if event.type == pygame.MOUSEBUTTONUP:
            clicked_coords = screen_pos_to_coords(event.pos, SETUP_WIDGETS['chessboard'].position, SETUP_WIDGETS['chessboard'].size)

            if self._drag_and_drop.dragged_sprite:
                self.remove_dragged_piece(clicked_coords)
                return
        
        widget_event = self._widget_group.process_event(event)

        if widget_event is None:
            if event.type == pygame.MOUSEBUTTONDOWN and self._cursor.get_sprite_collision(event.pos, self._widget_group) is None:
                self.selected_coords = None

            return

        match widget_event.type:
            case None:
                return

            case SetupEventType.MENU_CLICK:
                self.next = 'menu'
                self.done = True
            
            case SetupEventType.PICK_PIECE_CLICK:
                if widget_event.piece == self._selected_tool and widget_event.active_colour == self._selected_tool_colour:
                    self.deselect_tool()
                else:
                    self.select_tool(widget_event.piece, widget_event.active_colour)
            
            case SetupEventType.ROTATE_PIECE_CLICK:
                self.rotate_piece(widget_event.rotation_direction)
            
            case SetupEventType.EMPTY_CLICK:
                self._bitboards = BitboardCollection(fen_string='sc9/10/10/10/10/10/10/9Sa b')
                self.refresh_pieces()
            
            case SetupEventType.RESET_CLICK:
                self.reset_board()
            
            case SetupEventType.COPY_CLICK:
                print('COPYING TO CLIPBOARD:', encode_fen_string(self._bitboards))
                pyperclip.copy(encode_fen_string(self._bitboards))
            
            case SetupEventType.BLUE_START_CLICK:
                self.set_starting_colour(Colour.BLUE)
            
            case SetupEventType.RED_START_CLICK:
                self.set_starting_colour(Colour.RED)
            
            case SetupEventType.START_CLICK:
                self.next = 'config'
                self.done = True
            
            case SetupEventType.CONFIG_CLICK:
                self.reset_board()
                self.next = 'config'
                self.done = True
            
            case SetupEventType.ERASE_CLICK:
                if self._selected_tool == 'ERASE':
                    self.deselect_tool()
                else:
                    self.select_tool('ERASE', None)
            
            case SetupEventType.MOVE_CLICK:
                if self._selected_tool == 'MOVE':
                    self.deselect_tool()
                else:
                    self.select_tool('MOVE', None)
    
    def reset_board(self):
        self._bitboards = BitboardCollection(self._initial_fen_string)
        self.refresh_pieces()
    
    def refresh_pieces(self):
        self._piece_group.initialise_pieces(self._bitboards.convert_to_piece_list(), SETUP_WIDGETS['chessboard'].position, SETUP_WIDGETS['chessboard'].size)
    
    def set_starting_colour(self, new_colour):
        if new_colour == Colour.BLUE:
            SETUP_WIDGETS['blue_start_button'].set_locked(True)
            SETUP_WIDGETS['red_start_button'].set_locked(False)
        elif new_colour == Colour.RED:
            SETUP_WIDGETS['blue_start_button'].set_locked(False)
            SETUP_WIDGETS['red_start_button'].set_locked(True)
        
        if new_colour != self._starting_colour:
            SETUP_WIDGETS['blue_start_button'].set_next_icon()
            SETUP_WIDGETS['red_start_button'].set_next_icon()
        
        self._starting_colour = new_colour
        self._bitboards.active_colour = new_colour
    
    def set_dragged_piece(self, coords):
        bitboard_under_mouse = coords_to_bitboard(coords)
        dragged_piece = self._bitboards.get_piece_on(bitboard_under_mouse, Colour.BLUE) or self._bitboards.get_piece_on(bitboard_under_mouse, Colour.RED)

        if dragged_piece is None:
            return
        
        dragged_colour = self._bitboards.get_colour_on(bitboard_under_mouse)
        dragged_rotation = self._bitboards.get_rotation_on(bitboard_under_mouse)

        self._drag_and_drop.set_dragged_piece(dragged_piece, dragged_colour, dragged_rotation)
        self._overlay_draw.set_hover_limit(False)
    
    def remove_dragged_piece(self, coords):
        piece, colour, rotation = self._drag_and_drop.get_dragged_info()
        
        if coords and coords != self._selected_coords and piece != Piece.SPHINX:
            self.remove_piece()
            self.selected_coords = coords
            self.set_piece(piece, colour, rotation)
            self.selected_coords = None

        self._drag_and_drop.remove_dragged_piece()
        self._overlay_draw.set_hover_limit(True)

    def set_piece(self, piece, colour, rotation):
        if self.selected_coords is None or self.selected_coords == (0, 7) or self.selected_coords == (9, 0):
            return
        
        self.remove_piece()

        selected_bitboard = coords_to_bitboard(self.selected_coords)
        self._bitboards.set_square(selected_bitboard, piece, colour)
        self._bitboards.set_rotation(selected_bitboard, rotation)

        self.refresh_pieces()
    
    def remove_piece(self):
        if self.selected_coords is None or self.selected_coords == (0, 7) or self.selected_coords == (9, 0):
            return
        
        selected_bitboard = coords_to_bitboard(self.selected_coords)
        self._bitboards.clear_square(selected_bitboard, Colour.BLUE)
        self._bitboards.clear_square(selected_bitboard, Colour.RED)
        self._bitboards.clear_rotation(selected_bitboard)

        self.refresh_pieces()
    
    def rotate_piece(self, rotation_direction):
        if self.selected_coords is None or self.selected_coords == (0, 7) or self.selected_coords == (9, 0):
            return

        selected_bitboard = coords_to_bitboard(self.selected_coords)

        if self._bitboards.get_piece_on(selected_bitboard, Colour.BLUE) is None and self._bitboards.get_piece_on(selected_bitboard, Colour.RED) is None:
            return

        current_rotation = self._bitboards.get_rotation_on(selected_bitboard)

        if rotation_direction == RotationDirection.CLOCKWISE:
            self._bitboards.update_rotation(selected_bitboard, selected_bitboard, current_rotation.get_clockwise())
        elif rotation_direction == RotationDirection.ANTICLOCKWISE:
            self._bitboards.update_rotation(selected_bitboard, selected_bitboard, current_rotation.get_anticlockwise())

        self.refresh_pieces()

    def select_tool(self, piece, colour):
        dict_name_map = { Colour.BLUE: 'blue_piece_buttons', Colour.RED: 'red_piece_buttons' }

        self.deselect_tool()

        if piece == 'ERASE':
            SETUP_WIDGETS['erase_button'].set_locked(True)
            SETUP_WIDGETS['erase_button'].set_next_icon()
        elif piece == 'MOVE':
            SETUP_WIDGETS['move_button'].set_locked(True)
            SETUP_WIDGETS['move_button'].set_next_icon()
        else:
            SETUP_WIDGETS[dict_name_map[colour]][piece].set_locked(True)
            SETUP_WIDGETS[dict_name_map[colour]][piece].set_next_icon()
        
        self._selected_tool = piece
        self._selected_tool_colour = colour
    
    def deselect_tool(self):
        dict_name_map = { Colour.BLUE: 'blue_piece_buttons', Colour.RED: 'red_piece_buttons' }

        if self._selected_tool:
            if self._selected_tool == 'ERASE':
                SETUP_WIDGETS['erase_button'].set_locked(False)
                SETUP_WIDGETS['erase_button'].set_next_icon()
            elif self._selected_tool == 'MOVE':
                SETUP_WIDGETS['move_button'].set_locked(False)
                SETUP_WIDGETS['move_button'].set_next_icon()
            else:
                SETUP_WIDGETS[dict_name_map[self._selected_tool_colour]][self._selected_tool].set_locked(False)
                SETUP_WIDGETS[dict_name_map[self._selected_tool_colour]][self._selected_tool].set_next_icon()
        
        self._selected_tool = None
        self._selected_tool_colour = None
                
    def handle_resize(self, resize_end=False):
        self._widget_group.handle_resize(window.size)
        self._piece_group.handle_resize(SETUP_WIDGETS['chessboard'].position, SETUP_WIDGETS['chessboard'].size, resize_end)
        self._drag_and_drop.handle_resize(SETUP_WIDGETS['chessboard'].position, SETUP_WIDGETS['chessboard'].size)
        self._overlay_draw.handle_resize(SETUP_WIDGETS['chessboard'].position, SETUP_WIDGETS['chessboard'].size)
    
    def draw(self):
        draw_background(window.screen, GRAPHICS['temp_background'])
        self._widget_group.draw()
        self._overlay_draw.draw(window.screen)
        self._piece_group.draw(window.screen)
        self._drag_and_drop.draw(window.screen)
    
    def update(self, **kwargs):
        self.draw()