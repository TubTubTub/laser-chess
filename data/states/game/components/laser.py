from data.utils import bitboard_helpers as bb_helpers
from data.constants import Piece, Colour, Rotation, A_FILE_MASK, J_FILE_MASK, ONE_RANK_MASK, EIGHT_RANK_MASK, EMPTY_BB
from data.utils.bitboard_helpers import print_bitboard

class Laser:
    def __init__(self, bitboards):
        self._bitboards = bitboards
        self.hit_square_bitboard, self.piece_hit, self.laser_path, self.path_bitboard, self.pieces_on_trajectory = self.calculate_trajectory()
        
        if (self.hit_square_bitboard != EMPTY_BB):
            self.piece_rotation = self._bitboards.get_rotation_on(self.hit_square_bitboard)
            self.piece_colour = self._bitboards.get_colour_on(self.hit_square_bitboard)
    
    def calculate_trajectory(self):
        current_square = self._bitboards.get_piece_bitboard(Piece.SPHINX, self._bitboards.active_colour)
        previous_direction = self._bitboards.get_rotation_on(current_square)
        trajectory_bitboard = 0b0
        trajectory_list = []
        square_animation_states = []
        pieces_on_trajectory = []

        while current_square:
            current_piece = self._bitboards.get_piece_on(current_square, Colour.BLUE) or self._bitboards.get_piece_on(current_square, Colour.RED)
            current_rotation = self._bitboards.get_rotation_on(current_square)
            
            next_square, direction, piece_hit = self.calculate_next_square(current_square, current_piece, current_rotation, previous_direction)
            
            trajectory_bitboard |= current_square
            trajectory_list.append(bb_helpers.bitboard_to_coords(current_square))
            square_animation_states.append(direction)

            if previous_direction != direction:
                pieces_on_trajectory.append(current_square)

            if next_square == EMPTY_BB:
                hit_square_bitboard = 0b0

                if piece_hit:
                    hit_square_bitboard = current_square
                    
                return hit_square_bitboard, piece_hit, list(zip(trajectory_list, square_animation_states)), trajectory_bitboard, pieces_on_trajectory
            
            current_square = next_square
            previous_direction = direction
    
    def calculate_next_square(self, square, piece, rotation, previous_direction):
        match piece:
            case Piece.SPHINX:
                if previous_direction != rotation:
                    return EMPTY_BB, previous_direction, None

                next_square = self.next_square_bitboard(square, rotation)
                return next_square, previous_direction, Piece.SPHINX

            case Piece.PYRAMID:
                if previous_direction in [rotation, rotation.get_clockwise()]:
                    return EMPTY_BB, previous_direction, Piece.PYRAMID
                
                if previous_direction == rotation.get_anticlockwise():
                    new_direction = previous_direction.get_clockwise()
                else:
                    new_direction = previous_direction.get_anticlockwise()

                next_square = self.next_square_bitboard(square, new_direction)
                
                return next_square, new_direction, None

            case Piece.ANUBIS:
                if previous_direction == rotation.get_clockwise().get_clockwise():
                    return EMPTY_BB, previous_direction, None

                return EMPTY_BB, previous_direction, Piece.ANUBIS
                
            case Piece.SCARAB:
                if previous_direction in [rotation.get_clockwise(), rotation.get_anticlockwise()]:
                    new_direction = previous_direction.get_anticlockwise()
                else:
                    new_direction = previous_direction.get_clockwise()
                
                next_square = self.next_square_bitboard(square, new_direction)

                return next_square, new_direction, None

            case Piece.PHAROAH:
                return EMPTY_BB, previous_direction, Piece.PHAROAH

            case None:
                next_square = self.next_square_bitboard(square, previous_direction)

                return next_square, previous_direction, None
    
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