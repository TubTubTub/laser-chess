from data.constants import MoveType, Rotation, RotationIndex
from data.utils.bitboard_helpers import notation_to_bitboard, coords_to_bitboard

class Move():
    def __init__(self, move_type, src, dest=None, rotation_direction=None):
        self.move_type = move_type
        self.src = src
        self.dest = dest
        self.rotation_direction = rotation_direction
    
    @classmethod
    def instance_from_notation(move_cls, move_type, src, dest=None, rotation=None):
        try:
            if move_type == MoveType.MOVE:
                src_bitboard = notation_to_bitboard(src)
                dest_bitboard = notation_to_bitboard(dest)
            
            elif move_type == MoveType.ROTATE:
                src_bitboard = notation_to_bitboard(src)
                dest_bitboard = src_bitboard
            
            return move_cls(move_type, src_bitboard, dest_bitboard, rotation)
        except Exception as error:
            print('Error (Move.input_from_notation):', error)
    
    @classmethod
    def instance_from_coords(move_cls, move_type, src_coords, dest_coords, rotation_direction=None):
        try:
            src_bitboard = coords_to_bitboard(src_coords)
            dest_bitboard = coords_to_bitboard(dest_coords)
            
            return move_cls(move_type, src_bitboard, dest_bitboard, rotation_direction)
        except Exception as error:
            print('Error (Move.input_from_notation):', error)