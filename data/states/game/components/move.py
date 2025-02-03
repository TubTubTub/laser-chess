from data.constants import MoveType, Colour, RotationDirection
from data.utils.bitboard_helpers import notation_to_bitboard, coords_to_bitboard, bitboard_to_coords, bitboard_to_notation, print_bitboard
import re
from data.managers.logs import initialise_logger

logger = initialise_logger(__name__)

class Move():
    def __init__(self, move_type, src, dest=None, rotation_direction=None):
        self.move_type = move_type
        self.src = src
        self.dest = dest
        self.rotation_direction = rotation_direction

    def to_notation(self, colour, piece, hit_square_bitboard):
        hit_square = ''
        if colour == Colour.BLUE:
            piece = piece.upper()
        
        if hit_square_bitboard:
            hit_square = 'x' + bitboard_to_notation(hit_square_bitboard)

        if self.move_type == MoveType.MOVE:
            return 'M' + piece + bitboard_to_notation(self.src) + bitboard_to_notation(self.dest) + hit_square
        else:
            return 'R' + piece + bitboard_to_notation(self.src) + self.rotation_direction + hit_square
    
    def __str__(self):
        rotate_text = ''
        coords_1 = '(' + chr(bitboard_to_coords(self.src)[0] + 65) + ',' + str(bitboard_to_coords(self.src)[1] + 1) + ')'

        if self.move_type == MoveType.ROTATE:
            rotate_text = ' ' + self.rotation_direction.name
            return f'{self.move_type.name}{rotate_text}: ON {coords_1}'
        
        elif self.move_type == MoveType.MOVE:
            coords_2 = '(' + chr(bitboard_to_coords(self.dest)[0] + 65) + ', ' + str(bitboard_to_coords(self.dest)[1] + 1) + ')'
            return f'{self.move_type.name}{rotate_text}: FROM {coords_1} TO {coords_2}'
        
        # (Rotation: {self.rotation_direction})
    
    @classmethod
    def instance_from_notation(move_cls, notation):
        try:
            notation = notation.split('x')[0]
            move_type = notation[0].lower()

            moves = notation[2:]
            letters = re.findall(r'[A-Za-z]+', moves)
            numbers = re.findall(r'\d+', moves)

            if move_type == MoveType.MOVE:
                src_bitboard = notation_to_bitboard(letters[0] + numbers[0])
                dest_bitboard = notation_to_bitboard(letters[1] + numbers[1])

                return move_cls(move_type, src_bitboard, dest_bitboard)
            
            elif move_type == MoveType.ROTATE:
                src_bitboard = notation_to_bitboard(letters[0] + numbers[0])
                rotation_direction = RotationDirection(letters[1])

                return move_cls(move_type, src_bitboard, src_bitboard, rotation_direction)
            else:
                raise ValueError('(Move.instance_from_notation) Invalid move type:', move_type)

        except Exception as error:
            logger.info('(Move.instance_from_notation) Error occured while parsing:', error)
            raise error
    
    @classmethod
    def instance_from_input(move_cls, move_type, src, dest=None, rotation=None):
        try:
            if move_type == MoveType.MOVE:
                src_bitboard = notation_to_bitboard(src)
                dest_bitboard = notation_to_bitboard(dest)
            
            elif move_type == MoveType.ROTATE:
                src_bitboard = notation_to_bitboard(src)
                dest_bitboard = src_bitboard
            
            return move_cls(move_type, src_bitboard, dest_bitboard, rotation)
        except Exception as error:
            logger.info('Error (Move.instance_from):', error)
            raise error
    
    @classmethod
    def instance_from_coords(move_cls, move_type, src_coords, dest_coords=None, rotation_direction=None):
        try:
            src_bitboard = coords_to_bitboard(src_coords)
            dest_bitboard = coords_to_bitboard(dest_coords)
            
            return move_cls(move_type, src_bitboard, dest_bitboard, rotation_direction)
        except Exception as error:
            logger.info('Error (Move.instance_from_coords):', error)
            raise error

    @classmethod
    def instance_from_bitboards(move_cls, move_type, src_bitboard, dest_bitboard=None, rotation_direction=None):
        try:
            return move_cls(move_type, src_bitboard, dest_bitboard, rotation_direction)
        except Exception as error:
            logger.info('Error (Move.instance_from_bitboards):', error)
            raise error