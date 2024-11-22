from data.states.game.components.move import Move
from data.states.game.components.laser import Laser

from data.constants import Colour, Piece, Rank, File, MoveType, RotationDirection, A_FILE_MASK, J_FILE_MASK, ONE_RANK_MASK, EIGHT_RANK_MASK, EMPTY_BB
from data.states.game.components import bitboard_collection
from data.utils import bitboard_helpers as bb_helpers

class Board:
    def __init__(self, fen_string="sc3ncfancpb2/2pc7/3Pd6/pa1Pc1rbra1pb1Pd/pb1Pd1RaRb1pa1Pc/6pb3/7Pa2/2PdNaFaNa3Sa b"):
        self.bitboards = bitboard_collection.BitboardCollection(fen_string)

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
    
    def get_piece_list(self):
        return self.bitboards.convert_to_piece_list()

    def get_active_colour(self):
        return self.bitboards.active_colour
    
    def flip_colour(self):
        self.bitboards.active_colour = self.bitboards.active_colour.get_flipped_colour()
    
    def check_win(self):
        for colour in Colour:
            if self.get_all_valid_squares(colour) == EMPTY_BB:
                print(colour.get_flipped_colour(), '(Board.check_win) Returning')
                return colour.get_flipped_colour()
            elif self.bitboards.get_piece_bitboard(Piece.PHAROAH, colour) == EMPTY_BB:
                print(colour.get_flipped_colour(), '(Board.check_win) Returning')
                return colour.get_flipped_colour()

        return None
    
    def apply_move(self, move, fire_laser=True):
        piece_symbol = self.bitboards.get_piece_on(move.src, self.bitboards.active_colour)

        if piece_symbol is None:
            raise ValueError('Invalid move - no piece found on source square')
        elif piece_symbol == Piece.SPHINX:
            raise ValueError('Invalid move - sphinx piece is immovable')

        if move.move_type == MoveType.MOVE:
            possible_moves = self.get_valid_squares(move.src)
            if bb_helpers.is_occupied(move.dest, possible_moves) is False:
                raise ValueError('Invalid move - destination square is occupied')

            piece_rotation = self.bitboards.get_rotation_on(move.src)

            self.bitboards.update_move(move.src, move.dest)
            self.bitboards.update_rotation(move.src, move.dest, piece_rotation)

        elif move.move_type == MoveType.ROTATE:
            piece_symbol = self.bitboards.get_piece_on(move.src, self.bitboards.active_colour)
            piece_rotation = self.bitboards.get_rotation_on(move.src)

            if move.rotation_direction == RotationDirection.CLOCKWISE:
                new_rotation = piece_rotation.get_clockwise()
            elif move.rotation_direction == RotationDirection.ANTICLOCKWISE:
                new_rotation = piece_rotation.get_anticlockwise()

            self.bitboards.update_rotation(move.src, move.src, new_rotation)

        laser = None
        if fire_laser:
            laser = self.fire_laser()

        self.flip_colour()
        return laser
    
    def undo_move(self, move, laser_result):
        self.flip_colour()
        if laser_result.hit_square_bitboard:
            src = laser_result.hit_square_bitboard
            piece = laser_result.piece_hit
            colour = laser_result.piece_colour
            rotation = laser_result.piece_rotation

            self.bitboards.set_square(src, piece, colour)
            self.bitboards.clear_rotation(src)
            self.bitboards.set_rotation(src, rotation)

        if move.move_type == MoveType.MOVE:
            reversed_move = Move.instance_from_bitboards(MoveType.MOVE, move.dest, move.src)
        elif move.move_type == MoveType.ROTATE:
            reversed_move = Move.instance_from_bitboards(MoveType.ROTATE, move.src, move.src, move.rotation_direction.get_opposite())
        
        self.apply_move(reversed_move, fire_laser=False)
        self.flip_colour()
    
    def remove_piece(self, square_bitboard):
        self.bitboards.clear_square(square_bitboard, Colour.BLUE)
        self.bitboards.clear_square(square_bitboard, Colour.RED)
        self.bitboards.clear_rotation(square_bitboard)
    
    def get_valid_squares(self, src_bitboard, colour=None):
        target_top_left = (src_bitboard & A_FILE_MASK & EIGHT_RANK_MASK) << 9
        target_top_middle = (src_bitboard & EIGHT_RANK_MASK) << 10
        target_top_right = (src_bitboard & J_FILE_MASK & EIGHT_RANK_MASK) << 11
        target_middle_right = (src_bitboard & J_FILE_MASK) << 1

        target_bottom_right = (src_bitboard & J_FILE_MASK & ONE_RANK_MASK) >> 9
        target_bottom_middle = (src_bitboard & ONE_RANK_MASK) >> 10
        target_bottom_left = (src_bitboard & A_FILE_MASK & ONE_RANK_MASK)>> 11
        target_middle_left = (src_bitboard & A_FILE_MASK) >> 1

        possible_moves = target_top_left | target_top_middle | target_top_right | target_middle_right |	target_bottom_right | target_bottom_middle | target_bottom_left | target_middle_left
        
        if colour:
            valid_possible_moves = possible_moves & ~self.bitboards.combined_colour_bitboards[colour]
        else:
            valid_possible_moves = possible_moves & ~self.bitboards.combined_all_bitboard

        return valid_possible_moves
    
    def get_all_valid_squares(self, colour):
        piece_bitboard = self.bitboards.combined_colour_bitboards[colour]
        possible_moves = 0b0

        for square in bb_helpers.occupied_squares(piece_bitboard):
            possible_moves |= self.get_valid_squares(square)
        
        return possible_moves

    def get_all_active_pieces(self):
        active_pieces = self.bitboards.combined_colour_bitboards[self.bitboards.active_colour]
        sphinx_bitboard = self.bitboards.get_piece_bitboard(Piece.SPHINX, self.bitboards.active_colour)
        return active_pieces ^ sphinx_bitboard

    def fire_laser(self):
        laser = Laser(self.bitboards)

        if laser.hit_square_bitboard:
            laser.piece_rotation = self.bitboards.get_rotation_on(laser.hit_square_bitboard)
            laser.piece_colour = self.bitboards.get_colour_on(laser.hit_square_bitboard)
            self.remove_piece(laser.hit_square_bitboard)
        
        return laser
    
    def generate_square_moves(self, src):
        for dest in bb_helpers.occupied_squares(self.get_valid_squares(src)):
            yield Move(MoveType.MOVE, src, dest)
    
    def generate_all_moves(self, colour):
        for piece in (Piece.ANUBIS, Piece.PYRAMID, Piece.SCARAB, Piece.PHAROAH):
            piece_bitboard = self.bitboards.get_piece_bitboard(piece, colour)

            for square in bb_helpers.occupied_squares(piece_bitboard):
                yield from self.generate_square_moves(square)
        
        sphinx_bitboard = self.bitboards.get_piece_bitboard(Piece.SPHINX, colour)
        colour_bitboard = self.bitboards.combined_colour_bitboards[colour] ^ sphinx_bitboard

        for square in bb_helpers.occupied_squares(colour_bitboard):
            for rotation_direction in RotationDirection:
                yield Move(MoveType.ROTATE, square, rotation_direction=rotation_direction)