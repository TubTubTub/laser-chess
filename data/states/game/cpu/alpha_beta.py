from data.constants import Score, Colour
from data.states.game.cpu.base import BaseCPU
from data.states.game.cpu.transposition_table_mixin import TranspositionTableMixin

class AlphaBetaCPU(BaseCPU):
    def __init__(self, max_depth, callback, verbose=True):
        super().__init__(callback, verbose)
        self._max_depth = max_depth

    def find_move(self, board, stop_event):
        self.initialise_stats()
        best_score, best_move = self.search(board, self._max_depth, -Score.INFINITE, Score.INFINITE, stop_event)

        if self._verbose:
            self.print_stats(best_score, best_move)
            
        self._callback(best_move)

    def search(self, board, depth, alpha, beta, stop_event):
        if stop_event.is_set():
            raise Exception('Thread killed - stopping minimax function (AlphaBetaCPU.search)')
        
        self._stats['nodes'] += 1

        if (winner := board.check_win()) is not None:
            return self.process_win(winner)

        if depth == 0:
            self._stats['leaf_nodes'] += 1
            return self._evaluator.evaluate(board), None

        best_move = None

        if board.get_active_colour() == Colour.BLUE: # is_maximiser
            max_score = -Score.INFINITE
            
            for move in board.generate_all_moves(Colour.BLUE):
                laser_result = board.apply_move(move)
                new_score = self.search(board, depth - 1, alpha, beta, stop_event)[0]

                if new_score > max_score:
                    max_score = new_score
                    best_move = move

                board.undo_move(move, laser_result)

                alpha = max(alpha, max_score)
                
                if beta <= alpha:
                    break
                
            return max_score, best_move
            
        else:
            min_score = Score.INFINITE
            
            for move in board.generate_all_moves(Colour.RED):
                laser_result = board.apply_move(move)
                new_score = self.search(board, depth - 1, alpha, beta, stop_event)[0]

                if new_score < min_score:
                    min_score = new_score
                    best_move = move
                
                board.undo_move(move, laser_result)

                beta = min(beta, min_score)
                if beta <= alpha:
                    break
                
            return min_score, best_move

class CachedAlphaBetaCPU(TranspositionTableMixin, AlphaBetaCPU):
    def initialise_stats(self):
        super().initialise_stats()
        self._stats['cache_hits'] = 0
    
    def print_stats(self, score, move):
        self._stats['cache_hits_percentage'] = self._stats['cache_hits'] / self._stats['nodes']
        super().print_stats(score, move)