import pygame

from data.settings import app_settings
from data.components.cursor import Cursor
from data.components.customspritegroup import CustomSpriteGroup
from data.components.square import Square

from data.components.constants import Colour, Rank, File, A_FILE_MASK, J_FILE_MASK, ONE_RANK_MASK, EIGHT_RANK_MASK
from data.components import bitboard
from data.components import bitboard_helpers as bb_helpers

class Board:
    def __init__(self, screen, fen_string="sc3ncfancpb2/2pc7/3Pd7/pa1Pc1rbra1pb1Pd/pb1Pd1RaRb1pa1Pc/6pb3/7Pa2/2PdNaFaNa3Sa b"):
        self.game_settings = app_settings
        self.screen = screen
        self.cursor = Cursor()

        self.bitboards = bitboard.BitboardCollection(fen_string)

        self._board_size = self.calculate_board_size(self.screen)
        self._board_origin_position = self.calculate_board_position(self.screen, self._board_size)
        self._square_size = self._board_size[0] / 10
        self._square_group = self.initialize_square_group()

        self._selected_square_bitboards = []

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

            if blue_piece_symbol is not None:
                square.set_colour(Colour.BLUE)
                square.set_piece(blue_piece_symbol)
            elif red_piece_symbol is not None:
                square.set_colour(Colour.RED)
                square.set_piece(red_piece_symbol)

        return square_group
    
    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            print('COLOUR TO MOVE:', self.bitboards.active_colour)
            src, dest = self.get_move()
            self.apply_move(src, dest)
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.process_mouse_press(event)
        if event.type == pygame.VIDEORESIZE:
            self._square_group.draw_resized_finish()
    
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

    def resize_board(self):
        self._board_size = self.calculate_board_size(self.screen)
        self._board_origin_position = self.calculate_board_position(self.screen, self._board_size)
        self._square_size = self._board_size[0] / 10
        self._square_group.update(new_size=self._square_size, new_position=self._board_origin_position)

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

    def process_mouse_press(self, event):
        current_square_selected = self.cursor.select_square(event.pos, self._square_group)

        if current_square_selected is None:
            self._selected_square_bitboards = []
            
        if len(self._selected_square_bitboards) == 0:
            valid_squares = self.return_valid_squares(current_square_selected.to_bitboard())
            # bb_helpers.print_bitboard(valid_squares)
            # self._square_group.draw_valid_squares(valid_squares)

        if len(self._selected_square_bitboards) == 1:
            valid_squares = self.return_valid_squares(self._selected_square_bitboards[0].to_bitboard())

            if (current_square_selected.to_bitboard() in valid_squares):
                self.apply_move(self._selected_square_bitboards[0], self._selected_square_bitboards[1])
                self._selected_square_bitboards = []
    
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
        bb_helpers.print_bitboard(valid_possible_moves)
        return valid_possible_moves
    
    def apply_move(self, src_square, dest_square):
        piece_symbol = self.bitboards.get_piece_on(src_square.to_bitboard(), self.bitboards.active_colour)

        if piece_symbol is None:
            raise ValueError('Invalid move - no piece found on source square')
        
        self._square_group.update_squares_move(src_square.to_list_position(), dest_square.to_list_position(), piece_symbol, self.bitboards.active_colour)

        self.bitboards.update_bitboard_move(src_square.to_bitboard(), dest_square.to_bitboard())
        print('applied', src_square, dest_square)
        self.bitboards.flip_colour()
    
    def notation_to_list_index(self, notation):
        if (len(notation) == 2) and (notation[0].upper() in File._member_names_) and (notation[1] in [str(rank.value + 1) for rank in Rank]):
            rank = int(notation[1]) - 1
            file = int(File[notation[0].upper()])
            return (rank * 10 + file)
        else:
            raise ValueError('Invalid input - cannot convert input into list index')