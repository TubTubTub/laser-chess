from data.constants import Piece, PieceScore

class CPU:
    def __init__(self, bitboards):
        self._bitboards = bitboards
    
    def evaluate(self):
        return self.evaluate_pieces() + self.evaluate_position()

    def piece_count_difference(self, piece):
        colour = self._bitboards.active_colour
        return self._bitboards.get_piece_count(piece, colour) - self._bitboards.get_piece_count(piece, colour.get_flipped_colour())
    
    def evaluate_piece(self):
        return (
            PieceScore.PYRAMID * self.piece_count_difference(Piece.PYRAMID)
        )

    def evaluate_position(self):
        return 0