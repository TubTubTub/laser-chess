from data.constants import MoveType, Rotation
from data.utils.bitboard_helpers import index_to_bitboard

class Move():
    def __init__(self, src, dest=None, rotation=None):
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
                rotation_bitboard = rotation_to_bitboard(rotation)
            
            return move_cls(src_bitboard, dest_bitboard, rotation_bitboard)
        except Exception as error:
            print(error)
        
    
def notation_to_bitboard(notation):
    if not (97 <= ord(notation[0]) <= 106):
        raise ValueError('Invalid notation - file is out of range!')
    elif not (0 <= int(notation[1]) <= 10):
        raise ValueError('Invalid notation - rank is out of range!')
    
    index = (notation[0] - 1) * 10 + ord(notation[1]) - 97

    return index_to_bitboard(index)

def rotation_to_bitboard(rotation):
    if rotation not in Rotation:
        raise ValueError('Invalid notation - rotation is invalid!')

    raise NotImplementedError
    
    return Rotation[rotation]