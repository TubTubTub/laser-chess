from data.constants import Score
from data.states.game.cpu.engines.alpha_beta import ABMinimaxCPU
from data.states.game.cpu.engines.transposition_table import TranspositionTableMixin

class IterativeDeepeningMixin:
    def find_move(self, board, stop_event):
        for depth in range(1, self._max_depth + 1):
            self.initialise_stats()
            
            self._stats['ID_depth'] = depth
            best_score, best_move  = self.search(board, depth, -Score.INFINITE, Score.INFINITE, stop_event)

            if self._verbose:
                self.print_stats(best_score, best_move)

        self._callback(best_move)

class IDMinimaxCPU(IterativeDeepeningMixin, TranspositionTableMixin, ABMinimaxCPU):
    def initialise_stats(self):
        super().initialise_stats()
        self._stats['cache_hits'] = 0
    
    def print_stats(self, score, move):
        self._stats['cache_hits_percentage'] = self._stats['cache_hits'] / self._stats['nodes']
        super().print_stats(score, move)