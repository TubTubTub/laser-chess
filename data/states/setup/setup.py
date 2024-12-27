import pygame
import pyperclip
from data.control import _State
from data.components.widget_group import WidgetGroup
from data.states.setup.widget_dict import SETUP_WIDGETS
from data.constants import SetupEventType, Colour, RotationDirection
from data.states.game.components.bitboard_collection import BitboardCollection
from data.states.game.components.piece_group import PieceGroup
from data.components.cursor import Cursor
from data.assets import GRAPHICS, MUSIC_PATHS
from data.utils.bitboard_helpers import coords_to_bitboard
from data.utils.asset_helpers import draw_background
from data.utils.board_helpers import screen_pos_to_coords, coords_to_screen_pos
from data.states.game.components.fen_parser import encode_fen_string
from data.components.audio import audio
from data.components.animation import animation
from data.theme import theme

class Setup(_State):
    def __init__(self):
        super().__init__()
        self._screen = pygame.display.get_surface()
        self._cursor = Cursor()

        self._bitboards = None
        self._piece_group = None
        self._selected_coords = None
        self._selected_piece = None
        self._selected_piece_colour = None
        
        self._widget_group = None
    
    def cleanup(self):
        print('cleaning setup.py')

        return encode_fen_string(self._bitboards)
    
    def startup(self, persist):
        print('starting setup.py')
        self._widget_group = WidgetGroup(SETUP_WIDGETS)
        self._widget_group.handle_resize(self._screen.size)

        self._bitboards = BitboardCollection(persist['FEN_STRING'])
        self._initial_fen_string = persist['FEN_STRING']
        self._piece_group = PieceGroup()
        self._selected_coords = None
        self._selected_piece = None
        self._selected_piece_colour = None
        self._starting_colour = Colour.BLUE

        # audio.play_music(MUSIC_PATHS['setup'])
        
        self.refresh_pieces()
        self.set_starting_colour(Colour.BLUE if persist['FEN_STRING'][-1].lower() == 'b' else Colour.RED)
        self.draw()
    
    def refresh_pieces(self):
        self._piece_group.initialise_pieces(self._bitboards.convert_to_piece_list(), SETUP_WIDGETS['chessboard'].position, SETUP_WIDGETS['chessboard'].size)
    
    def get_event(self, event):
        if event.type == pygame.VIDEORESIZE:
            self.handle_resize(resize_end=True)
            return
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked_coords = screen_pos_to_coords(event.pos, SETUP_WIDGETS['chessboard'].position, SETUP_WIDGETS['chessboard'].size)

            if clicked_coords:
                self._selected_coords = clicked_coords

                if self._selected_piece:
                    self.set_piece()
                    
                return
        
        widget_event = self._widget_group.process_event(event)

        if widget_event is None:
            if event.type == pygame.MOUSEBUTTONDOWN and self._cursor.get_sprite_collision(event.pos, self._widget_group) is None:
                self._selected_coords = None
                self.deselect_piece()

            return

        match widget_event.type:
            case None:
                return

            case SetupEventType.MENU_CLICK:
                self.next = 'menu'
                self.done = True
            
            case SetupEventType.PICK_PIECE_CLICK:
                self.select_piece(widget_event.piece, widget_event.active_colour)
            
            case SetupEventType.ROTATE_PIECE_CLICK:
                self.rotate_piece(widget_event.rotation_direction)
            
            case SetupEventType.EMPTY_CLICK:
                self._bitboards = BitboardCollection(None)
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
    
    def reset_board(self):
        self._bitboards = BitboardCollection(self._initial_fen_string)
        self.refresh_pieces()
    
    def set_starting_colour(self, new_colour):
        if new_colour == Colour.BLUE:
            print('seting blue')
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

    def set_piece(self):
        if self._selected_coords is None or self._selected_coords == (0, 7) or self._selected_coords == (9, 0):
            return
        
        selected_bitboard = coords_to_bitboard(self._selected_coords)
        self._bitboards.clear_square(selected_bitboard, Colour.BLUE)
        self._bitboards.clear_square(selected_bitboard, Colour.RED)
        self._bitboards.clear_rotation(selected_bitboard)
        self._bitboards.set_square(selected_bitboard, self._selected_piece, self._selected_piece_colour)

        self.refresh_pieces()
    
    def rotate_piece(self, rotation_direction):
        if self._selected_coords is None or self._selected_coords == (0, 7) or self._selected_coords == (9, 0):
            return

        selected_bitboard = coords_to_bitboard(self._selected_coords)

        if self._bitboards.get_piece_on(selected_bitboard, Colour.BLUE) is None and self._bitboards.get_piece_on(selected_bitboard, Colour.RED) is None:
            return

        current_rotation = self._bitboards.get_rotation_on(selected_bitboard)

        if rotation_direction == RotationDirection.CLOCKWISE:
            self._bitboards.update_rotation(selected_bitboard, selected_bitboard, current_rotation.get_clockwise())
        elif rotation_direction == RotationDirection.ANTICLOCKWISE:
            self._bitboards.update_rotation(selected_bitboard, selected_bitboard, current_rotation.get_anticlockwise())

        self.refresh_pieces()

    def select_piece(self, piece, colour):
        dict_name_map = { Colour.BLUE: 'blue_piece_buttons', Colour.RED: 'red_piece_buttons' }

        self.deselect_piece()
        
        SETUP_WIDGETS[dict_name_map[colour]][piece].set_locked(True)
        SETUP_WIDGETS[dict_name_map[colour]][piece].set_next_icon()
        
        self._selected_piece = piece
        self._selected_piece_colour = colour
    
    def deselect_piece(self):
        dict_name_map = { Colour.BLUE: 'blue_piece_buttons', Colour.RED: 'red_piece_buttons' }

        if self._selected_piece:
            SETUP_WIDGETS[dict_name_map[self._selected_piece_colour]][self._selected_piece].set_locked(False)
            SETUP_WIDGETS[dict_name_map[self._selected_piece_colour]][self._selected_piece].set_next_icon()
        
        self._selected_piece = None
        self._selected_piece_colour = None
                
    def handle_resize(self, resize_end=False):
        self._widget_group.handle_resize(self._screen.get_size())
        self._piece_group.handle_resize(SETUP_WIDGETS['chessboard'].position, SETUP_WIDGETS['chessboard'].size, resize_end)
    
    def draw(self):
        draw_background(self._screen, GRAPHICS['temp_background'])
        self._widget_group.draw()
        self._piece_group.draw(self._screen)

        if self._selected_coords:
            square_size = SETUP_WIDGETS['chessboard'].size[0] / 10
            overlay_position = coords_to_screen_pos(self._selected_coords, SETUP_WIDGETS['chessboard'].position, square_size)
            pygame.draw.rect(self._screen, theme['borderPrimary'], (*overlay_position, square_size, square_size), width=int(theme['borderWidth']))
    
    def update(self, **kwargs):
        self.draw()