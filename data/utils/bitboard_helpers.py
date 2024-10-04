from data.constants import Rank, File, EMPTY_BB

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
                characters += '0  '

        characters += '\n\n'
    
    print('\n' + characters + '\n')

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
        bitboard &= bitboard - 1
    
    return count