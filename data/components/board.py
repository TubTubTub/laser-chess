# from data.components.laser import Laser
from data.components.move import Move

from data.constants import Colour, Piece, Rank, File, MoveType, A_FILE_MASK, J_FILE_MASK, ONE_RANK_MASK, EIGHT_RANK_MASK, EMPTY_BB
from data.components import bitboard
from data.utils import bitboard_helpers as bb_helpers
from data.utils import input_helpers as ip_helpers

class Board:
    def __init__(self, fen_string="sc3ncfancpb2/2pc7/3Pd7/pa1Pc1rbra1pb1Pd/pb1Pd1RaRb1pa1Pc/6pb3/7Pa2/2PdNaFaNa3Sa b"):
        self.bitboards = bitboard.BitboardCollection(fen_string)
        self.status_text = self.bitboards.active_colour.name
        self.has_moved_piece = False

        self._laser_shapes = []
        self._selected_square = None
        self._pressed_on_board = False
        self._paused = False
    
    @property
    def clicked(self):
        return self._pressed_on_board and not self._paused
    
    def __str__(self):
        characters = ''
        for rank in reversed(Rank):

            for file in File:
                mask = 1 << (rank * 10 + file)
                blue_piece = self.bitboards.get_piece_on(mask, Colour.BLUE)
                red_piece = self.bitboards.get_piece_on(mask, Colour.RED)

                if blue_piece:
                    characters += f'{blue_piece.upper()}  '
                elif red_piece:
                    characters += f'{red_piece}  '
                else:
                    characters += '0  '

            characters += '\n\n'
        
        characters += f'CURRENT PLAYER TO MOVE: {self.bitboards.active_colour.name}'
        return characters

    def get_move(self):
        while True:
            try:
                move_type = ip_helpers.parse_move_type(input('Input move type (m/r): '))
                src_square = ip_helpers.parse_notation(input("From: "))
                dest_square = ip_helpers.parse_notation(input("To: "))
                rotation = ip_helpers.parse_rotation(input("Enter rotation (a/b/c/d): "))
                return Move.input_from_notation(move_type, src_square, dest_square, rotation)
            except ValueError as error:
                print('Input error (Board.get_move): ' + str(error))
    
    def check_win(self):
        if self.return_all_valid_squares(self.bitboards.active_colour) == EMPTY_BB:
            return self.bitboards.active_colour.get_flipped_colour()

        return None

    # def check_valid_src(self, src_square):
    #     return (src_square & self.bitboards.combined_colour_bitboards[self.bitboards.active_colour]) != EMPTY_BB
    
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
    
    def return_all_valid_squares(self, colour):
        all_valid_squares = EMPTY_BB
        for piece in Piece:
            piece_bitboard = self.bitboards.get_piece_bitboard(piece, colour)

            for square in bb_helpers.occupied_squares(piece_bitboard):
                valid_moves = self.return_valid_squares(square)
                all_valid_squares = all_valid_squares | valid_moves
            
        return all_valid_squares
    
    def apply_move(self, move):
        bb_helpers.print_bitboard(move.src)
        piece_symbol = self.bitboards.get_piece_on(move.src, self.bitboards.active_colour)

        if piece_symbol is None:
            raise ValueError('Invalid move - no piece found on source square')
        elif piece_symbol == Piece.SPHINX:
            raise ValueError('Invalid move - sphinx piece is immovable')

        if move.move_type == MoveType.MOVE:
            possible_moves = self.return_valid_squares(move.src)
            if bb_helpers.is_occupied(move.dest, possible_moves) is False:
                raise ValueError('Invalid move - destination square is occupied')

            piece_rotation = self.bitboards.get_rotation_on(move.src)
            
            # self._square_group.update_squares_move(src_square.to_list_position(), dest_square.to_list_position(), piece_symbol, self.bitboards.active_colour, rotation)

            self.bitboards.update_move(move.src, move.dest)
            self.bitboards.update_rotation(move.src, move.dest, piece_rotation)

            bb_helpers.print_bitboard(move.src)
            print('GAGHGAGAHAGH')
            bb_helpers.print_bitboard(move.dest)

        elif move.move_type == MoveType.ROTATE:
            # src_bitboard = src_square.to_bitboard()
            # src_list_position = src_square.to_list_position()

            piece_symbol = self.bitboards.get_piece_on(move.src, self.bitboards.active_colour)

            # self._square_group.update_squares_rotate(src_list_position, piece_symbol, self.bitboards.active_colour, new_rotation=new_rotation)
            self.bitboards.update_rotation(move.src, move.src, move.rotation)

        self.has_moved_piece = True
        self.bitboards.flip_colour()
        print(f'PLAYER MOVE: {self.bitboards.active_colour.name}')
    
    def rotate_piece(self, clockwise=True):
        if self._selected_square is None:
            print('No square selected to rotate (board.py)!')
            return
        
        src_rotation = self.bitboards.get_rotation_on(self._selected_square.to_bitboard())
        
        if clockwise:
            self.apply_rotation(self._selected_square, src_rotation.get_clockwise())
        else:
            self.apply_rotation(self._selected_square, src_rotation.get_anticlockwise())
    
    def capture_piece(self, square_bitboard):
        self.bitboards.clear_square(square_bitboard, Colour.BLUE)
        self.bitboards.clear_square(square_bitboard, Colour.RED)

        self._square_group.clear_square(square_bitboard)
    
    # def fire_laser(self):
    #     if self.bitboards.active_colour == Colour.BLUE:
    #         laser_colour = self.game_settings.laserColourBlue
    #     else:
    #         laser_colour = self.game_settings.laserColourRed
    #     laser = Laser(screen=self.screen, laser_colour=laser_colour, bitboards=self.bitboards)

    #     captured_square, laser_shapes = laser.calculate_trajectory()
    #     self._laser_shapes = laser_shapes
    #     if captured_square:
    #         print('captured_square:')
    #         bb_helpers.print_bitboard(captured_square)
    #         print(captured_square)
    #         self.capture_piece(captured_square)
    
    # def draw_laser(self):
    #     for shape, index in self._laser_shapes:
    #         position = (index[0] * self._square_size + self._board_origin_position[0], self._board_origin_position[1] - self._square_size * (index[1] + 1))
    #         pygame.draw.rect(self.screen, 'red', (position[0], position[1], shape.width, shape.height))