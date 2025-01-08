from data.constants import Score, Colour, Miscellaneous
from data.states.game.cpu.base import BaseCPU
from data.utils.bitboard_helpers import print_bitboard
from random import choice, randint
from copy import deepcopy

class NegamaxCPU(BaseCPU):
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
            raise Exception('Thread killed - stopping minimax function (MinimaxCPU.search)')
        
        self._stats['nodes'] += 1
        active_colour = board.get_active_colour()
        
        if (winner := board.check_win()) is not None:
            return self.process_win(winner)
        
        if depth == 0:
            self._stats['leaf_nodes'] += 1
            return self._evaluator.evaluate(board), None

        best_move = None
        best_score = -Score.INFINITE

        for move in board.generate_all_moves(active_colour):
            laser_result = board.apply_move(move)

            new_score = self.search(board, depth - 1, stop_event)[0]
            new_score = -new_score

            if new_score > best_score:
                best_score = new_score
                best_move = move
            elif new_score == best_score:
                best_move = choice([best_move, move])
            
            board.undo_move(move, laser_result)

        return best_score, best_move