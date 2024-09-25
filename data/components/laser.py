from data.utils import bitboard_helpers as bb_helpers
from data.constants import Piece, Colour, Rotation, LaserType, LaserDirection, A_FILE_MASK, J_FILE_MASK, ONE_RANK_MASK, EIGHT_RANK_MASK, EMPTY_BB

class Laser:
    def __init__(self, bitboards):
        self._bitboards = bitboards
        self.hit_square_bitboard, self.laser_path = self.calculate_trajectory()
    
    def calculate_trajectory(self):
        current_square = self._bitboards.get_piece_bitboard(Piece.SPHINX, self._bitboards.active_colour)
        previous_direction = self._bitboards.get_rotation_on(current_square)
        trajectory_bitboard = 0b0
        trajectory_list = []
        square_animation_states = []

        while current_square:
            blue_piece = self._bitboards.get_piece_on(current_square, Colour.BLUE)
            red_piece = self._bitboards.get_piece_on(current_square, Colour.RED)
            current_piece = blue_piece or red_piece
            current_rotation = self._bitboards.get_rotation_on(current_square)
            
            next_square, direction, piece_is_hit = self.calculate_next_square(current_square, current_piece, current_rotation, previous_direction)

            if next_square == EMPTY_BB:
                hit_square_bitboard = 0b0
                if piece_is_hit:
                    hit_square_bitboard = current_square

                return hit_square_bitboard, list(zip(trajectory_list, square_animation_states))
            
            trajectory_bitboard |= current_square
            trajectory_list.append(bb_helpers.bitboard_to_coords(current_square))
            square_animation_states.append(direction)
            
            current_square = next_square
            previous_direction = direction
    
    def calculate_next_square(self, square, piece, rotation, previous_direction):
        match piece:
            case Piece.SPHINX:
                next_square = self.next_square_bitboard(square, rotation)

                return next_square, previous_direction, False

            case Piece.PYRAMID:
                if previous_direction in [rotation, rotation.get_clockwise()]:
                    return EMPTY_BB, previous_direction, True
                
                if previous_direction == rotation.get_anticlockwise():
                    new_direction = previous_direction.get_clockwise()
                else:
                    new_direction = previous_direction.get_anticlockwise()

                next_square = self.next_square_bitboard(square, new_direction)
                
                return next_square, new_direction, False

            case Piece.ANUBIS:
                if previous_direction == rotation.get_clockwise().get_clockwise():
                    return EMPTY_BB, previous_direction, False

                return EMPTY_BB, previous_direction, True
                
            case Piece.SCARAB:
                if previous_direction in [rotation.get_clockwise(), rotation.get_anticlockwise()]:
                    new_direction = previous_direction.get_anticlockwise()
                else:
                    new_direction = previous_direction.get_clockwise()
                
                next_square = self.next_square_bitboard(square, new_direction)

                return next_square, new_direction, False

            case Piece.PHAROAH:
                return EMPTY_BB, previous_direction, True

            case None:
                next_square = self.next_square_bitboard(square, previous_direction)

                return next_square, previous_direction, False
    
    def next_square_bitboard(self, src_bitboard, previous_direction):
        match previous_direction:
            case Rotation.UP:
                masked_src_bitboard = src_bitboard & EIGHT_RANK_MASK
                return masked_src_bitboard << 10
            case Rotation.RIGHT:
                masked_src_bitboard = src_bitboard & J_FILE_MASK
                return masked_src_bitboard << 1
            case Rotation.DOWN:
                masked_src_bitboard = src_bitboard & ONE_RANK_MASK
                return masked_src_bitboard >> 10
            case Rotation.LEFT:
                masked_src_bitboard = src_bitboard & A_FILE_MASK
                return masked_src_bitboard >> 1