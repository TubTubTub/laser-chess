from data.managers.logs import initialise_logger
from data.utils.constants import EMPTY_BB
from data.utils.enums import Rank, File

logger = initialise_logger(__name__)

def print_bitboard(bitboard):
    if (bitboard >= (2 ** 80)):
        raise ValueError('Invalid bitboard: too many bits')

    characters = ''
    for rank in reversed(Rank):

        for file in File:
            mask = 1 << (rank * 10 + file)
            if (bitboard & mask) != 0:
                characters += '1  '
            else:
                characters += '.  '

        characters += '\n\n'

    logger.info('\n' + characters + '\n')

def is_occupied(bitboard, target_bitboard):
    return (target_bitboard & bitboard) != EMPTY_BB

def clear_square(bitboard, target_bitboard):
    return (~target_bitboard & bitboard)

def set_square(bitboard, target_bitboard):
    return (target_bitboard | bitboard)

def index_to_bitboard(index):
    return (1 << index)

def coords_to_bitboard(coords):
    index = coords[1] * 10 + coords[0]
    return index_to_bitboard(index)

def bitboard_to_notation(bitboard):
    index = bitboard_to_index(bitboard)
    x = index // 10
    y = index % 10

    return chr(y + 97) + str(x + 1)

def notation_to_bitboard(notation):
    index = (int(notation[1]) - 1) * 10 + int(ord(notation[0])) - 97

    return index_to_bitboard(index)

def bitboard_to_index(bitboard):
    return bitboard.bit_length() - 1

def bitboard_to_coords(bitboard):
    list_position = bitboard_to_index(bitboard)
    x = list_position % 10
    y = list_position // 10

    return x, y

def bitboard_to_coords_list(bitboard):
    list_positions = []

    for square in occupied_squares(bitboard):
        list_positions.append(bitboard_to_coords(square))

    return list_positions

def occupied_squares(bitboard):
    while bitboard:
        lsb_square = bitboard & -bitboard
        bitboard = bitboard ^ lsb_square

        yield lsb_square

def pop_count(bitboard):
    count = 0
    while bitboard:
        count += 1
        lsb_square = bitboard & -bitboard
        bitboard = bitboard ^ lsb_square

    return count

# def pop_count(bitboard):
#     count = 0
#     while bitboard:
#         count += 1
#         bitboard &= bitboard - 1

#     return count

def loop_all_squares():
    for i in range(80):
        yield 1 << i

#Solar
def get_LSB_value(bitboard: int):
    return bitboard & -bitboard

def pop_count_2(bitboard):
    count = 0
    while bitboard > 0:
        lsb_value = get_LSB_value(bitboard)
        count += 1
        bitboard ^= lsb_value

    return count