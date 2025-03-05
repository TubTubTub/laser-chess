from data.states.game.cpu.evaluator import Evaluator
from data.constants import Colour
from data.utils.bitboard_helpers import print_bitboard, pop_count

class SimpleEvaluator:
    def __init__(self):
        self._evaluator = Evaluator(verbose=False)
        self._cache = {}
    
    def evaluate(self, board):
        if (hashed := board.to_hash()) in self._cache:
            return self._cache[hashed]
    
        score = self._evaluator.evaluate_material(board, board.get_active_colour())
        self._cache[hashed] = score

        return score

class MoveOrderer:
    def __init__(self):
        self._evaluator = SimpleEvaluator()
    
    # def get_eval(self, board, move):
    #     laser_result = board.apply_move(move)
    #     score = self._evaluator.evaluate(board)
    #     board.undo_move(move, laser_result)
    #     return score

    # def score_moves(self, board, moves):
    #     for i in range(len(moves)):
    #         score = self.get_eval(board, moves[i])
    #         moves[i] = (moves[i], score)
        
    #     return moves

    def best_move_to_front(self, moves, start_idx, laser_coords):
        for i in range(start_idx + 1, len(moves)):
            if moves[i].src in laser_coords:
                moves[i], moves[start_idx] = moves[start_idx], moves[i]
                return
    
    def get_moves(self, board, hint=None, laser_coords=None):
        if hint:
            yield hint

        colour = board.get_active_colour()
        moves = list(board.generate_all_moves(colour))
        
        for i in range(len(moves)):
            if laser_coords:
                self.best_move_to_front(moves, i, laser_coords)

            yield moves[i]