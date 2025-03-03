from data.states.game.cpu.engines.transposition_table import TranspositionTableMixin
from data.states.game.cpu.engines.alpha_beta import ABMinimaxCPU, ABNegamaxCPU
from data.constants import Score

class IterativeDeepeningMixin:
    def find_move(self, board, stop_event):
        best_move = None

        for depth in range(1, self._max_depth + 1):
            self.initialise_stats()
            self._stats['ID_depth'] = depth

            best_score, best_move = self.search(board, depth, -Score.INFINITE, Score.INFINITE, stop_event)

            if self._verbose:
                self.print_stats(best_score, best_move)

        self._callback(best_move)

class IDMinimaxCPU(TranspositionTableMixin, IterativeDeepeningMixin, ABMinimaxCPU):
    def initialise_stats(self):
        super().initialise_stats()
        self._stats['cache_hits'] = 0
    
    def print_stats(self, score, move):
        self._stats['cache_hits_percentage'] = round(self._stats['cache_hits'] / self._stats['nodes'], 3)
        self._stats['cache_entries'] = len(self._table._table)
        super().print_stats(score, move)

class IDNegamaxCPU(TranspositionTableMixin, IterativeDeepeningMixin, ABNegamaxCPU):
    def initialise_stats(self):
        super().initialise_stats()
        self._stats['cache_hits'] = 0
    
    def print_stats(self, score, move):
        self._stats['cache_hits_percentage'] = self._stats['cache_hits'] / self._stats['nodes']
        self._stats['cache_entries'] = len(self._table._table)
        super().print_stats(score, move)