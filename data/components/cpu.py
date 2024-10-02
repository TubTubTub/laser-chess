from data.constants import Piece, PieceScore, Colour
from data.utils.bitboard_helpers import print_bitboard, bitboard_to_coords, coords_to_bitboard
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
        return 0

    def minimax(self, board, depth, alpha, beta, move):
        self.turns += 1
        if depth == 0:
            return self.evaluate(board)

        is_maximiser = board.get_active_colour() == Colour.BLUE 

        if is_maximiser:
            score = -PieceScore.INFINITE
            
            for move in board.generate_all_moves(board.get_active_colour()):
                before = board.bitboards.get_rotation_string()
                before_score = self.evaluate(board)

                laser_result = board.apply_move(move)
                new_score = self.minimax(board, depth - 1, alpha, beta, move)
                # if (self.evaluate(board) != before_score) and depth==2: print('DIFFERENT', before_score, self.evaluate(board), bitboard_to_coords(laser_result.hit_square_bitboard), move)
                # if depth == 2: print('BLUE DEPTH 2 MOVE:', move, new_score)

                if new_score >= score:
                    score = new_score

                    if depth == self._depth:
                        self._best_move = move

                board.undo_move(move, laser_result)

                alpha = max(alpha, score)
                if beta <= alpha:
                    break
                
                after = board.bitboards.get_rotation_string()
                after_score = self.evaluate(board)
                if (before != after):
                    print('shit')
                if (before_score != after_score):
                    print('wtf')
                
            return score
            
        else:
            score = PieceScore.INFINITE
            
            for move in board.generate_all_moves(board.get_active_colour()):
                bef = board.bitboards.get_rotation_string()
                before_score = self.evaluate(board)

                laser_result = board.apply_move(move)
                new_score = self.minimax(board, depth - 1, alpha, beta, move)

                # if (self.evaluate(board) != before_score) and depth==2: print('DIFFERENT', before_score, self.evaluate(board), bitboard_to_coords(laser_result.hit_square_bitboard), move)
                # if depth == 3: print('RED MOVE DEPTH 3:', move, new_score) # (0,4) to (1, 5) gives correct evaluation but wrong score

                if new_score <= score:
                    score = new_score
                    if depth == self._depth:
                        self._best_move = move
                
                board.undo_move(move, laser_result)

                beta = min(beta, score)
                if beta <= alpha:
                    break
                
                after = board.bitboards.get_rotation_string()
                after_score = self.evaluate(board)
                if (bef != after):
                    print('shit')
                if (before_score != after_score):
                    print('wtf')
                
            return score

    def find_best_move(self):
        print('Minimax evaluation:', self.minimax(self._board, self._depth, -PieceScore.INFINITE, PieceScore.INFINITE, None))
        print('Best move:', self._best_move, 'Number of iterations:', self.turns)
        return self._best_move