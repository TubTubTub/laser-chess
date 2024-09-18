from data.constants import Piece, Colour, Rotation, RotationIndex
from data.components.fen_parser import parse_fen_string
from data.utils import bitboard_helpers as bb_helpers

class BitboardCollection():
    def __init__(self, fen_string):
        self.piece_bitboards = None
        self.combined_colour_bitboards = None
        self.combined_all_bitboard = None
        self.rotation_bitboards = None
        self.active_colour = None

        try:
            self.piece_bitboards, self.combined_colour_bitboards, self.combined_all_bitboard, self.rotation_bitboards, self.active_colour = parse_fen_string(fen_string)
        except ValueError:
            print('Please input a valid FEN string')
    
    def update_move(self, src, dest):
        piece = self.get_piece_on(src, self.active_colour)

        self.clear_square(src, Colour.BLUE)
        self.clear_square(dest, Colour.BLUE)
        self.clear_square(src, Colour.RED)
        self.clear_square(dest, Colour.RED)

        self.set_square(dest, piece, self.active_colour)
    
    def update_rotation(self, src, dest, new_rotation):
        self.clear_rotation(src)
        self.set_rotation(dest, new_rotation)
    
    def clear_rotation(self, index):
        rotation_1, rotation_2 = self.rotation_bitboards
        self.rotation_bitboards[RotationIndex.FIRSTBIT] = bb_helpers.clear_square(rotation_1, index)
        self.rotation_bitboards[RotationIndex.SECONDBIT] = bb_helpers.clear_square(rotation_2, index)
    
    def clear_square(self, index, colour):
        piece = self.get_piece_on(index, colour)

        if piece is None:
            return
        
        piece_bitboard = self.get_piece_bitboard(piece, colour)
        colour_bitboard = self.combined_colour_bitboards[colour]
        all_bitboard = self.combined_all_bitboard

        self.piece_bitboards[colour][piece] = bb_helpers.clear_square(piece_bitboard, index)
        self.combined_colour_bitboards[colour] = bb_helpers.clear_square(colour_bitboard, index)
        self.combined_all_bitboard = bb_helpers.clear_square(all_bitboard, index)
    
    def set_rotation(self, index, rotation):
        rotation_1, rotation_2 = self.rotation_bitboards
        
        match rotation:
            case Rotation.UP:
                return
            case Rotation.RIGHT:
                self.rotation_bitboards[RotationIndex.FIRSTBIT] = bb_helpers.set_square(rotation_1, index)
                return
            case Rotation.DOWN:
                self.rotation_bitboards[RotationIndex.SECONDBIT] = bb_helpers.set_square(rotation_2, index)
                return
            case Rotation.LEFT:
                self.rotation_bitboards[RotationIndex.FIRSTBIT] = bb_helpers.set_square(rotation_1, index)
                self.rotation_bitboards[RotationIndex.SECONDBIT] = bb_helpers.set_square(rotation_2, index)
                return
            case _:
                raise ValueError('Invalid rotation input (bitboard.py):', rotation)
    
    def set_square(self, index, piece, colour):
        piece_bitboard = self.get_piece_bitboard(piece, colour)
        colour_bitboard = self.combined_colour_bitboards[colour]
        all_bitboard = self.combined_all_bitboard

        self.piece_bitboards[colour][piece] = bb_helpers.set_square(piece_bitboard, index)
        self.combined_colour_bitboards[colour] = bb_helpers.set_square(colour_bitboard, index)
        self.combined_all_bitboard = bb_helpers.set_square(all_bitboard, index)
    
    def get_piece_bitboard(self, piece, colour):
        return self.piece_bitboards[colour][piece]
    
    def get_piece_on(self, target_bitboard, colour):
        if not (bb_helpers.is_occupied(self.combined_colour_bitboards[colour], target_bitboard)):
            return None
    
        return next(
            (piece for piece in Piece if 
                bb_helpers.is_occupied(self.get_piece_bitboard(piece, colour), target_bitboard)),
            None)

    def get_rotation_on(self, index):
        rotationBits = [bb_helpers.is_occupied(self.rotation_bitboards[RotationIndex.SECONDBIT], index), bb_helpers.is_occupied(self.rotation_bitboards[RotationIndex.FIRSTBIT], index)]

        match rotationBits:
            case [False, False]:
                return Rotation.UP
            case [False, True]:
                return Rotation.RIGHT
            case [True, False]:
                return Rotation.DOWN
            case [True, True]:
                return Rotation.LEFT
    
    def convert_to_piece_list(self):
        piece_list = []

        for i in range(80):
            if x := self.get_piece_on(1 << i, Colour.BLUE):
                piece_list.append(x.upper())
            elif y := self.get_piece_on(1 << i, Colour.RED):
                piece_list.append(y)
            else:
                piece_list.append(None)
        
        return piece_list