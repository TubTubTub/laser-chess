from data.constants import MoveType, Rotation, RotationIndex
from data.utils.bitboard_helpers import index_to_bitboard

class Move():
    def __init__(self, move_type, src, dest=None, rotation=None):
        self.move_type = move_type
        self.src = src
        self.dest = dest
        self.rotation = rotation
    
    def input_from_notation(move_cls, move_type, src, dest=None, rotation=None):
        try:
            if move_type == MoveType.MOVE:
                src_bitboard = notation_to_bitboard(src)
                dest_bitboard = notation_to_bitboard(dest)
            
            elif move_type == MoveType.ROTATE:
                src_bitboard = notation_to_bitboard(src)
            
            return move_cls(move_type, src_bitboard, dest_bitboard, rotation)
        except Exception as error:
            print(error)

def notation_to_bitboard(notation):
    index = (notation[0] - 1) * 10 + ord(notation[1]) - 97
    print('CONVERTING NOTATION:', notation, index)

    return index_to_bitboard(index)