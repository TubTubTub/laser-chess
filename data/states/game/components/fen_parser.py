from data.helpers.bitboard_helpers import occupied_squares, bitboard_to_index
from data.utils.enums import Colour, RotationIndex, Rotation, Piece
from data.utils.constants import EMPTY_BB

def parse_fen_string(fen_string):
    #sc3ncfcncpb2/2pc7/3Pd6/pa1Pc1rbra1pb1Pd/pb1Pd1RaRb1pa1Pc/6pb3/7Pa2/2PdNaFaNa3Sa b
    piece_bitboards = [{char: EMPTY_BB for char in Piece}, {char: EMPTY_BB for char in Piece}]
    rotation_bitboards = [EMPTY_BB, EMPTY_BB]
    combined_colour_bitboards = [EMPTY_BB, EMPTY_BB]
    combined_all_bitboard = 0
    part_1, part_2 = fen_string.split(' ')

    rank = 7
    file = 0

    piece_count = {char.lower(): 0 for char in Piece} | {char.upper(): 0 for char in Piece}

    for index, character in enumerate(part_1):
        square = rank * 10 + file

        if character.lower() in Piece:
            piece_count[character] += 1
            if character.isupper():
                piece_bitboards[Colour.BLUE][character.lower()] |= 1 << square

            else:
                piece_bitboards[Colour.RED][character.lower()] |= 1 << square

            rotation = part_1[index + 1]
            match rotation:
                case Rotation.UP:
                    pass
                case Rotation.RIGHT:
                    rotation_bitboards[RotationIndex.FIRSTBIT] |= 1 << square
                case Rotation.DOWN:
                    rotation_bitboards[RotationIndex.SECONDBIT] |= 1 << square
                case Rotation.LEFT:
                    rotation_bitboards[RotationIndex.SECONDBIT] |= 1 << square
                    rotation_bitboards[RotationIndex.FIRSTBIT] |= 1 << square
                case _:
                    raise ValueError('Invalid FEN String - piece character not followed by rotational character')

            file += 1
        elif character in '0123456789':
            if character == '1' and fen_string[index + 1] == '0':
                file += 10
                continue

            file += int(character)
        elif character == '/':
            rank = rank - 1
            file = 0
        elif character in Rotation:
            continue
        else:
            raise ValueError('Invalid FEN String - invalid character found:', character)

    if piece_count['s'] != 1 or piece_count['S'] != 1:
        raise ValueError('Invalid FEN string - invalid number of Sphinx pieces')
    # COMMENTED OUT AS NO PHAROAH PIECES IS OKAY IF PARSING FEN STRING FOR FINISHED GAME BOARD THUMBNAIL
    elif piece_count['f'] > 1 or piece_count['F'] > 1:
        raise ValueError('Invalid FEN string - invalid number of Pharoah pieces')

    if part_2 == 'b':
        colour = Colour.BLUE
    elif part_2 == 'r':
        colour = Colour.RED
    else:
        raise ValueError('Invalid FEN string - invalid active colour')

    for piece in Piece:
        combined_colour_bitboards[Colour.BLUE] |= piece_bitboards[Colour.BLUE][piece]
        combined_colour_bitboards[Colour.RED] |= piece_bitboards[Colour.RED][piece]

    combined_all_bitboard = combined_colour_bitboards[Colour.BLUE] | combined_colour_bitboards[Colour.RED]
    return (piece_bitboards, combined_colour_bitboards, combined_all_bitboard, rotation_bitboards, colour)

def encode_fen_string(bitboard_collection):
    blue_bitboards = bitboard_collection.piece_bitboards[Colour.BLUE]
    red_bitboards = bitboard_collection.piece_bitboards[Colour.RED]

    fen_string_list = [''] * 80

    for piece, bitboard in blue_bitboards.items():
        for individual_bitboard in occupied_squares(bitboard):
            index = bitboard_to_index(individual_bitboard)
            rotation = bitboard_collection.get_rotation_on(individual_bitboard)
            fen_string_list[index] = piece.upper() + rotation

    for piece, bitboard in red_bitboards.items():
        for individual_bitboard in occupied_squares(bitboard):
            index = bitboard_to_index(individual_bitboard)
            rotation = bitboard_collection.get_rotation_on(individual_bitboard)
            fen_string_list[index] = piece.lower() + rotation

    fen_string = ''
    row_string = ''
    empty_count = 0
    for index, square in enumerate(fen_string_list):
        if square == '':
            empty_count += 1
        else:
            if empty_count > 0:
                row_string += str(empty_count)
                empty_count = 0

            row_string += square

        if index % 10 == 9:
            if empty_count > 0:
                fen_string = '/' + row_string + str(empty_count) + fen_string
            else:
                fen_string = '/' + row_string + fen_string

            row_string = ''
            empty_count = 0

    fen_string = fen_string[1:]

    if bitboard_collection.active_colour == Colour.BLUE:
        colour = 'b'
    else:
        colour = 'r'

    return fen_string + ' ' + colour