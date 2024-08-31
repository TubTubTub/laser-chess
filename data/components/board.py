import pygame

from data.components.cursor import Cursor
from data.components.customspritegroup import CustomSpriteGroup
from data.components.square import Square

from data.components.constants import Colour, Rank, File, A_FILE_MASK, J_FILE_MASK, ONE_RANK_MASK, EIGHT_RANK_MASK, EMPTY_BB
from data.components import bitboard
from data.components import bitboard_helpers as bb_helpers

class Board:
    def __init__(self, screen, app_settings, fen_string="sc3ncfancpb2/2pc7/3Pd7/pa1Pc1rbra1pb1Pd/pb1Pd1RaRb1pa1Pc/6pb3/7Pa2/2PdNaFaNa3Sa b"):
        self.game_settings = app_settings
        self.screen = screen
        self.cursor = Cursor()

        self.bitboards = bitboard.BitboardCollection(fen_string)
        self.status_text = self.bitboards.active_colour.name

        self._board_size = self.calculate_board_size(self.screen)
        self._board_origin_position = self.calculate_board_position(self.screen, self._board_size)
        self._square_size = self._board_size[0] / 10
        self._square_group = self.initialize_square_group()

        self._selected_square = None
        self._pressed_on_board = False
        self._paused = False

    def initialize_square_group(self):
        square_group = CustomSpriteGroup()

        for i in range(80):
            x = i % 10
            y = i // 10


            if (x + y) % 2 == 0:
                square = Square(index=(x,y), size=self._square_size, board_colour=(self.game_settings.primaryBoardColour), anchor_position=self._board_origin_position)
            else:
                square = Square(index=(x,y), size=self._square_size, board_colour=(self.game_settings.secondaryBoardColour), anchor_position=self._board_origin_position)

            square_group.add(square)
            square_group.square_list.append(square)

            blue_piece_symbol = self.bitboards.get_piece_on(square.to_bitboard(), Colour.BLUE)
            red_piece_symbol = self.bitboards.get_piece_on(square.to_bitboard(), Colour.RED)
            rotation = self.bitboards.get_rotation_on(square.to_bitboard())

            if (blue_piece_symbol):
                square.set_piece(piece_symbol=blue_piece_symbol, colour=Colour.BLUE, rotation=rotation)
            elif (red_piece_symbol):
                square.set_piece(piece_symbol=red_piece_symbol, colour=Colour.RED, rotation=rotation)
        return square_group
    
    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self._pressed_on_board = True
        if event.type == pygame.VIDEORESIZE:
            self._square_group.handle_resize_end()
    
    @property
    def clicked(self):
        return self._pressed_on_board and not self._paused
    
    def play_turn(self):
        mouse_position = pygame.mouse.get_pos()
        self.process_board_press(mouse_position)
        self._pressed_on_board = False
    
    def get_move(self):
        try:
            input1 = input("From: ")
            input2 = input("To: ")
            return (input1, input2)
        except ValueError:
            print('Board.py: Invalid inputs!')

    def draw_board(self):
        self.cursor.update()
        self._square_group.draw(self.screen)

    def handle_resize(self):
        self._board_size = self.calculate_board_size(self.screen)
        self._board_origin_position = self.calculate_board_position(self.screen, self._board_size)
        self._square_size = self._board_size[0] / 10
        self._square_group.handle_resize(new_size=self._square_size, new_position=self._board_origin_position)

    def calculate_board_size(self, screen):
        '''Returns board size based on screen parameter'''
        screen_width, screen_height = screen.get_size()

        target_height = screen_height * 0.64
        target_width = target_height / 0.8

        return (target_width, target_height)

    def calculate_board_position(self, screen, board_size):
        '''Returns required board starting position to draw on center of the screen'''
        screen_x, screen_y = screen.get_size()
        board_x, board_y = board_size

        x = screen_x / 2 - (board_x / 2)
        y = screen_y / 2 + (board_y / 2)

        return (x, y)

    def process_board_press(self, mouse_position):
        print('rng')
        clicked_square = self.cursor.select_square(mouse_position, self._square_group)

        if (clicked_square is None):
            self._selected_square = None
            self._square_group.remove_valid_square_overlays()
            
        elif self._selected_square is None:
            if (clicked_square._piece is None) or not(self.check_valid_src(clicked_square.to_bitboard())):
                return
            else:
                self._selected_square = clicked_square
                valid_squares = self.return_valid_squares(clicked_square.to_bitboard())
                self._square_group.add_valid_square_overlays(valid_squares)
                self._square_group.draw_valid_square_overlays()

        else:
            valid_squares = self.return_valid_squares(self._selected_square.to_bitboard())

            if (clicked_square.to_bitboard() & valid_squares != EMPTY_BB):
                self.apply_move(self._selected_square, clicked_square)
                self.status_text = self.bitboards.active_colour.name

            self._square_group.remove_valid_square_overlays()
            self._selected_square = None

    def check_valid_src(self, src_square):
        return (src_square & self.bitboards.combined_colour_bitboards[self.bitboards.active_colour]) != EMPTY_BB
    
    def return_valid_squares(self, src_bitboard):
        target_top_left = (src_bitboard & A_FILE_MASK & EIGHT_RANK_MASK) << 9
        target_top_middle = (src_bitboard & EIGHT_RANK_MASK) << 10
        target_top_right = (src_bitboard & J_FILE_MASK & EIGHT_RANK_MASK) << 11
        target_middle_right = (src_bitboard & J_FILE_MASK) << 1

        target_bottom_right = (src_bitboard & J_FILE_MASK & ONE_RANK_MASK) >> 9
        target_bottom_middle = (src_bitboard & ONE_RANK_MASK) >> 10
        target_bottom_left = (src_bitboard & A_FILE_MASK & ONE_RANK_MASK)>> 11
        target_middle_left = (src_bitboard & A_FILE_MASK) >> 1

        possible_moves = target_top_left | target_top_middle | target_top_right | target_middle_right |	target_bottom_right | target_bottom_middle | target_bottom_left | target_middle_left

        valid_possible_moves = possible_moves & ~self.bitboards.combined_all_bitboard
        return valid_possible_moves
    
    def apply_move(self, src_square, dest_square):
        src_bitboard = src_square.to_bitboard()
        dest_bitboard = dest_square.to_bitboard()

        piece_symbol = self.bitboards.get_piece_on(src_bitboard, self.bitboards.active_colour)
        rotation = self.bitboards.get_rotation_on(src_bitboard)

        if piece_symbol is None:
            raise ValueError('Invalid move - no piece found on source square')
        
        self._square_group.update_squares_move(src_square.to_list_position(), dest_square.to_list_position(), piece_symbol, self.bitboards.active_colour, rotation)

        self.bitboards.update_bitboard_move(src_bitboard, dest_bitboard)
        self.bitboards.update_bitboard_rotation(src_bitboard, dest_bitboard, rotation)
        self.bitboards.flip_colour()
    
    def apply_rotation(self, src_square, new_rotation):
        src_bitboard = src_square.to_bitboard()
        src_list_position = src_square.to_list_position()
        piece_symbol = self.bitboards.get_piece_on(src_bitboard, self.bitboards.active_colour)

        self._square_group.update_squares_rotate(src_list_position, piece_symbol, self.bitboards.active_colour, new_rotation=new_rotation)
        self.bitboards.update_bitboard_rotation(src_bitboard, src_bitboard, new_rotation)
        self.bitboards.flip_colour()
    
    def rotate_piece(self, clockwise=True):
        if self._selected_square is None:
            print('No square selected to rotate (board.py)!')
            return
        
        src_rotation = self.bitboards.get_rotation_on(self._selected_square.to_bitboard())
        
        if clockwise:
            self.apply_rotation(self._selected_square, src_rotation.get_clockwise())
        else:
            self.apply_rotation(self._selected_square, src_rotation.get_anticlockwise())
    
    def notation_to_list_index(self, notation):
        if (len(notation) == 2) and (notation[0].upper() in File._member_names_) and (notation[1] in [str(rank.value + 1) for rank in Rank]):
            rank = int(notation[1]) - 1
            file = int(File[notation[0].upper()])
            return (rank * 10 + file)
        else:
            raise ValueError('Invalid input - cannot convert input into list index')