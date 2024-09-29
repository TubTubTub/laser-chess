from data.constants import Piece, PieceScore, Colour
from data.utils.bitboard_helpers import print_bitboard, bitboard_to_coords, coords_to_bitboard
class CPU:
    def __init__(self, board, depth):
        self._board = board
        self._best_move = None
        self._depth = depth
    
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
        return 0

    def minimax(self, board, depth):
        if depth == 0:
            return self.evaluate(board)
        is_maximiser = board.get_active_colour() == Colour.BLUE 

        if is_maximiser:
            score = -100000
            
            for move in board.generate_all_moves(board.get_active_colour()):
                laser_result = board.apply_move(move)
                
                new_score = self.minimax(board, depth - 1)
                print('hi', new_score, score)

                if new_score >= score and depth == self._depth:
                    self._best_move = move
                
                score = max(score, new_score)
                
                board.undo_move(move, laser_result)
                
            return score
            
        else:
            score = 100000
            
            for move in board.generate_all_moves(board.get_active_colour()):

                laser_result = board.apply_move(move)

                new_score = self.minimax(board, depth - 1)

                if new_score <= score and depth == self._depth:
                    print('bitch')
                    self._best_move = move
                
                score = min(score, new_score)
                
                board.undo_move(move, laser_result)
                
            return score

    def find_best_move(self):
        print(self.minimax(self._board, self._depth), 'FINAL SCORE')
        return self._best_move