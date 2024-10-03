from data.constants import Piece, PieceScore, Colour
from data.utils.bitboard_helpers import print_bitboard, bitboard_to_coords, coords_to_bitboard, index_to_bitboard
from data.psqt import PSQT, FLIP

class CPU:
    def __init__(self, board, depth):
        self._board = board
        self._best_move = None
        self._depth = depth
        self.turns = 0
    
    def evaluate(self, board):
        blue_score = self.evaluate_pieces(board, Colour.BLUE) + self.evaluate_position(board, Colour.BLUE)
        red_score = self.evaluate_pieces(board, Colour.RED) + self.evaluate_position(board, Colour.RED)
        return blue_score - red_score
    
    def evaluate_pieces(self, board, colour):
        return (
            PieceScore.SPHINX * board.bitboards.get_piece_count(Piece.SPHINX, colour) +
            PieceScore.PYRAMID * board.bitboards.get_piece_count(Piece.PYRAMID, colour) +
            PieceScore.ANUBIS * board.bitboards.get_piece_count(Piece.ANUBIS, colour) +
            PieceScore.SCARAB * board.bitboards.get_piece_count(Piece.SCARAB, colour)
        )

    def evaluate_position(self, board, colour):
        score = 0
        for i in range(80):
            bitboard = index_to_bitboard(i)
            piece = board.bitboards.get_piece_on(bitboard, colour)

            if piece == Piece.SPHINX:
                continue

            if piece and colour == Colour.BLUE:
                score += PSQT[piece][FLIP[i]]
            elif piece and colour == Colour.RED:
                score += PSQT[piece][i]

        return score

    def minimax(self, board, depth, alpha, beta, debug):
        self.turns += 1

        if depth == 0:
            return self.evaluate(board)

        is_maximiser = board.get_active_colour() == Colour.BLUE 

        if is_maximiser:
            score = -PieceScore.INFINITE
            
            for move in board.generate_all_moves(board.get_active_colour()):
                before, before_score = board.bitboards.get_rotation_string(), self.evaluate(board)

                laser_result = board.apply_move(move)
                new_score = self.minimax(board, depth - 1, alpha, beta, False)

                if new_score >= score:
                    score = new_score

                    if depth == self._depth:
                        self._best_move = move

                board.undo_move(move, laser_result)

                alpha = max(alpha, score)
                if beta < alpha:
                    break
                
                after, after_score = board.bitboards.get_rotation_string(), self.evaluate(board)
                if (before != after or before_score != after_score):
                    print('shit\n\n')
                
            return score
            
        else:
            score = PieceScore.INFINITE
            
            for move in board.generate_all_moves(board.get_active_colour()):
                bef, before_score = board.bitboards.get_rotation_string(), self.evaluate(board)

                laser_result = board.apply_move(move)
                new_score = self.minimax(board, depth - 1, alpha, beta, False)

                if new_score <= score:
                    score = new_score
                    if depth == self._depth:
                        self._best_move = move
                
                board.undo_move(move, laser_result)

                beta = min(beta, score)
                if beta < alpha:
                    break
                
                after, after_score = board.bitboards.get_rotation_string(), self.evaluate(board)
                if (bef != after or before_score != after_score):
                    print('shit\n\n')
                
            return score

    def find_best_move(self, result):
        print('tset:', self.evaluate_position(self._board, Colour.BLUE), self.evaluate_position(self._board, Colour.RED))
        print('\nEvaluation:', self.minimax(self._board, self._depth, -PieceScore.INFINITE, PieceScore.INFINITE, False))
        print('\nBest move:', self._best_move)
        print('\nNumber of iterations:', self.turns)
        result.value = self._best_move
        # return self._best_move