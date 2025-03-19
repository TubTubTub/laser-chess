from data.helpers.bitboard_helpers import pop_count, occupied_squares, bitboard_to_index
from data.states.game.components.psqt import PSQT, FLIP
from data.utils.enums import Colour, Piece, Score
from data.managers.logs import initialise_logger

logger = initialise_logger(__name__)

class Evaluator:
    def __init__(self, verbose=True):
        self._verbose = verbose

    def evaluate(self, board, absolute=False):
        """
        Evaluates and returns a numerical score for the board state.

        Args:
            board (Board): The current board state.
            absolute (bool): Whether to always return the absolute score from the active colour's perspective (for NegaMax).

        Returns:
            int: Score representing advantage/disadvantage for the player.
        """
        blue_score = (
            self.evaluate_material(board, Colour.BLUE),
            self.evaluate_position(board, Colour.BLUE),
            self.evaluate_mobility(board, Colour.BLUE),
            self.evaluate_pharaoh_safety(board, Colour.BLUE)
        )

        red_score = (
            self.evaluate_material(board, Colour.RED),
            self.evaluate_position(board, Colour.RED),
            self.evaluate_mobility(board, Colour.RED),
            self.evaluate_pharaoh_safety(board, Colour.RED)
        )

        if self._verbose:
            logger.info(f'Material: {blue_score[0]} | {red_score[0]}')
            logger.info(f'Position: {blue_score[1]} | {red_score[1]}')
            logger.info(f'Mobility: {blue_score[2]} | {red_score[2]}')
            logger.info(f'Safety: {blue_score[3]} | {red_score[3]}')
            logger.info(f'Overall score: {sum(blue_score) - sum(red_score)}\n')

        if absolute and board.get_active_colour() == Colour.RED:
            return sum(red_score) - sum(blue_score)
        else:
            return sum(blue_score) - sum(red_score)

    def evaluate_material(self, board, colour):
        """
        Evaluates the material score for a given colour.

        Args:
            board (Board): The current board state.
            colour (Colour): The colour to evaluate.

        Returns:
            int: Sum of all piece scores.
        """
        return (
            Score.SPHINX * board.bitboards.get_piece_count(Piece.SPHINX, colour) +
            Score.PYRAMID * board.bitboards.get_piece_count(Piece.PYRAMID, colour) +
            Score.ANUBIS * board.bitboards.get_piece_count(Piece.ANUBIS, colour) +
            Score.SCARAB * board.bitboards.get_piece_count(Piece.SCARAB, colour)
        )

    def evaluate_position(self, board, colour):
        """
        Evaluates the positional score for a given colour.

        Args:
            board (Board): The current board state.
            colour (Colour): The colour to evaluate.

        Returns:
            int: Score representing positional advantage/disadvantage.
        """
        score = 0

        for piece in Piece:
            if piece == Piece.SPHINX:
                continue

            piece_bitboard = board.bitboards.get_piece_bitboard(piece, colour)

            for bitboard in occupied_squares(piece_bitboard):
                index = bitboard_to_index(bitboard)
                # Flip PSQT if using from blue player's perspective
                index = FLIP[index] if colour == Colour.BLUE else index

                score += PSQT[piece][index] * Score.POSITION

        return score

    def evaluate_mobility(self, board, colour):
        """
        Evaluates the mobility score for a given colour.

        Args:
            board (Board): The current board state.
            colour (Colour): The colour to evaluate.

        Returns:
            int: Score on numerical representation of mobility.
        """
        number_of_moves = board.get_mobility(colour)
        return number_of_moves * Score.MOVE

    def evaluate_pharaoh_safety(self, board, colour):
        """
        Evaluates the safety of the Pharaoh for a given colour.

        Args:
            board (Board): The current board state.
            colour (Colour): The colour to evaluate.

        Returns:
            int: Score representing mobility of the Pharaoh.
        """
        pharaoh_bitboard = board.bitboards.get_piece_bitboard(Piece.PHARAOH, colour)

        if pharaoh_bitboard:
            pharaoh_available_moves = pop_count(board.get_valid_squares(pharaoh_bitboard, colour))
            return (8 - pharaoh_available_moves) * Score.PHARAOH_SAFETY
        else:
            return 0