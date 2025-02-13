from data.constants import Colour, Piece, Score
from data.utils.bitboard_helpers import index_to_bitboard, pop_count, occupied_squares, bitboard_to_index
from data.states.game.components.psqt import PSQT, FLIP
import random
from data.managers.logs import initialise_logger

logger = initialise_logger(__name__)

class Evaluator:
    def __init__(self, verbose=True):
        self._verbose = verbose
        pass
    
    def evaluate(self, board, absolute=False):
        #Add tapered evaluation
        blue_score = self.evaluate_pieces(board, Colour.BLUE) + self.evaluate_position(board, Colour.BLUE) + self.evaluate_mobility(board, Colour.BLUE) + self.evaluate_pharoah_safety(board, Colour.BLUE)

        red_score = self.evaluate_pieces(board, Colour.RED) + self.evaluate_position(board, Colour.RED) + self.evaluate_mobility(board, Colour.RED) + self.evaluate_pharoah_safety(board, Colour.RED)

        if (self._verbose):
            logger.info('\nPosition:', self.evaluate_position(board, Colour.BLUE), self.evaluate_position(board, Colour.RED))
            logger.info('Mobility:', self.evaluate_mobility(board, Colour.BLUE), self.evaluate_mobility(board, Colour.RED))
            logger.info('Safety:', self.evaluate_pharoah_safety(board, Colour.BLUE), self.evaluate_pharoah_safety(board, Colour.RED))
            logger.info('Overall score', blue_score - red_score)

        if absolute and board.get_active_colour() == Colour.RED:
            return red_score - blue_score
        
        return blue_score - red_score
    
    def evaluate_pieces(self, board, colour):
        # return random.randint(-100, 100)
        return (
            Score.SPHINX * board.bitboards.get_piece_count(Piece.SPHINX, colour) +
            Score.PYRAMID * board.bitboards.get_piece_count(Piece.PYRAMID, colour) +
            Score.ANUBIS * board.bitboards.get_piece_count(Piece.ANUBIS, colour) +
            Score.SCARAB * board.bitboards.get_piece_count(Piece.SCARAB, colour)
        )

    def evaluate_position(self, board, colour):
        score = 0

        for piece in Piece:
            if piece == Piece.SPHINX:
                continue

            for colour in Colour:
                piece_bitboard = board.bitboards.get_piece_bitboard(piece, colour)
                
                for bitboard in occupied_squares(piece_bitboard):
                    index = bitboard_to_index(bitboard)
                    index = FLIP[index] if colour == Colour.BLUE else index

                    score += PSQT[piece][index] * Score.POSITION
        
        return score
    
    def evaluate_mobility(self, board, colour):
        number_of_moves = pop_count(board.get_all_valid_squares(colour))

        return number_of_moves * Score.MOVE

    def evaluate_pharoah_safety(self, board, colour):
        pharoah_bitboard = board.bitboards.get_piece_bitboard(Piece.PHAROAH, colour)
        pharoah_available_moves = pop_count(board.get_valid_squares(pharoah_bitboard, colour))
        return (8 - pharoah_available_moves) * Score.PHAROAH_SAFETY