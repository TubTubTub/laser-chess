from data.constants import Score, Colour, Miscellaneous
from data.states.game.cpu.base import BaseCPU
from data.utils.bitboard_helpers import print_bitboard

class MinimaxCPU(BaseCPU):
    def __init__(self, max_depth, callback, verbose=False):
        super().__init__(callback, verbose)
        self._max_depth = max_depth

    def find_move(self, board, stop_event):
        self.initialise_stats()
        best_score, best_move = self.search(board, self._max_depth, stop_event)

        if self._verbose:
            self.print_stats(best_score, best_move)
            
        self._callback(best_move)

    def search(self, board, depth, stop_event):
        if stop_event and stop_event.is_set():
            raise Exception('Thread killed - stopping minimax function (MinimaxCPU.searcg)')
        
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
                
                new_score = self.search(board, depth - 1, stop_event)[0]

                if new_score > max_score:
                    max_score = new_score
                    best_move = move

                board.undo_move(move, laser_result)
                
            return max_score, best_move
            
        else:
            min_score = Score.INFINITE
            
            for move in board.generate_all_moves(Colour.RED):
                laser_result = board.apply_move(move)
                new_score = self.search(board, depth - 1, stop_event)[0]

                if new_score < min_score:
                    min_score = new_score
                    best_move = move
                
                board.undo_move(move, laser_result)
                
            return min_score, best_move