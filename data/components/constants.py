from enum import IntEnum

PIECE_SYMBOLS = 'frpns'
EMPTY_BB = 0
A_FILE_MASK = 0b11111111101111111110111111111011111111101111111110111111111011111111101111111110
J_FILE_MASK = 0b01111111110111111111011111111101111111110111111111011111111101111111110111111111
ONE_RANK_MASK = 0b11111111111111111111111111111111111111111111111111111111111111111111110000000000
EIGHT_RANK_MASK = 0b00000000001111111111111111111111111111111111111111111111111111111111111111111111

class Colour(IntEnum):
    BLUE = 0
    RED = 1

class Piece(IntEnum):
    SPHINX = 0
    PYRAMID = 1
    ANUBIS = 2
    SCARAB = 3
    PHAROAH = 4

    def to_char(self):
        if self == Piece.SPHINX:
            return 's'
        elif self == Piece.PYRAMID:
            return 'p'
        elif self == Piece.ANUBIS:
            return 'n'
        elif self == Piece.SCARAB:
            return 'r'
        elif self == Piece.PHAROAH:
            return 'f'

class Rank(IntEnum):
    ONE = 0
    TWO = 1
    THREE = 2
    FOUR = 3
    FIVE = 4
    SIX = 5
    SEVEN = 6
    EIGHT = 7

class File(IntEnum):
    A = 0
    B = 1
    C = 2
    D = 3
    E = 4
    F = 5
    G = 6
    H = 7
    I = 8
    J = 9

class Rotation(IntEnum):
    HORIZONTAL = 0
    VERTICAL = 1
    UP = 1
    RIGHT = 1
    DOWN = 0
    LEFT = 0