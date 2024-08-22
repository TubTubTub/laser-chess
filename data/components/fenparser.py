from data.components.constants import Colour, Rotation, PIECE_SYMBOLS

def parse_fen_string(fen_string):
    #sc3ncfancpb2/2pc7/3Pd7/pa1Pc1rbra1pb1Pd/pb1Pd1RaRb1pa1Pc/6pb3/7Pa2/2PdNaFaNa3Sa r
    piece_bitboards = [{char: 0 for char in PIECE_SYMBOLS}, {char: 0 for char in PIECE_SYMBOLS}]
    rotation_bitboards = [0, 0]
    combined_colour_bitboards = [0, 0]
    combined_all_bitboard = 0
    part_1, part_2 = fen_string.split(' ')

    rank = 7
    file = 0
    
    for index, character in enumerate(part_1):
        square = rank * 10 + file

        if character.lower() in PIECE_SYMBOLS:
            if character.isupper():
                piece_bitboards[Colour.BLUE][character.lower()] |= 1 << square

            else:
                piece_bitboards[Colour.RED][character.lower()] |= 1 << square
                
            rotation = part_1[index + 1]
            match rotation:
                case 'a':
                    rotation_bitboards[Rotation.VERTICAL] |= Rotation.UP << square
                case 'b':
                    rotation_bitboards[Rotation.HORIZONTAL] |= Rotation.RIGHT << square
                case 'c':
                    pass
                case 'd':
                    pass
                case _:
                    raise ValueError('Invalid FEN String - piece character not followed by rotational character')
            
            file += 1
        elif character in '12346789':
            file += int(character)
        elif character == '/':
            rank = rank - 1
            file = 0
        elif character in 'abcd':
            continue
        else:
            print(character)
            raise ValueError('Invalid FEN String - invalid character found')
    
    if (part_2 == 'b'):
        colour = Colour.BLUE
    else:
        colour = Colour.RED
    
    for piece in PIECE_SYMBOLS:
        combined_colour_bitboards[Colour.BLUE] |= piece_bitboards[Colour.BLUE][piece]
        combined_colour_bitboards[Colour.RED] |= piece_bitboards[Colour.RED][piece]
    
    combined_all_bitboard = combined_colour_bitboards[Colour.BLUE] | combined_colour_bitboards[Colour.RED]
    
    return (piece_bitboards, combined_colour_bitboards, combined_all_bitboard, rotation_bitboards, colour)