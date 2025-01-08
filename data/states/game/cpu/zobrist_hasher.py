from random import randint
from data.constants import Piece, Colour, Rotation
from data.utils.bitboard_helpers import bitboard_to_index

zobrist_table = [[randint(0, 2 ** 64) for i in range(14)] for j in range(80)] # 10 pieces + 4 rotations, 8 y, 10 
red_move_hash = randint(0, 2 ** 64)

piece_lookup = {
    Colour.BLUE: {
        piece: i for i, piece in enumerate(Piece)
    },
    Colour.RED: {
        piece: i + 5 for i, piece in enumerate(Piece)
    },
}

rotation_lookup = {
    rotation: i + 10 for i, rotation in enumerate(Rotation)
}

class ZobristHasher:
    def __init__(self):
        self.hash = 0

    def get_piece_hash(self, index, piece, colour):
        piece_index = piece_lookup[colour][piece]
        return zobrist_table[index][piece_index]

    def get_rotation_hash(self, index, rotation):
        rotation_index = rotation_lookup[rotation]
        return zobrist_table[index][rotation_index]
    
    def apply_piece_hash(self, bitboard, piece, colour):
        index = bitboard_to_index(bitboard)
        piece_hash = self.get_piece_hash(index, piece, colour)
        self.hash ^= piece_hash
    
    def apply_rotation_hash(self, bitboard, rotation):
        index = bitboard_to_index(bitboard)
        rotation_hash = self.get_rotation_hash(index, rotation)
        self.hash ^= rotation_hash
    
    def apply_red_move_hash(self):
        self.hash ^= red_move_hash