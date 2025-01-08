from data.states.game.cpu.transposition_table import TranspositionTable
from data.states.game.cpu.engines.alpha_beta import ABMinimaxCPU

class TranspositionTableMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._table = TranspositionTable()
    
    def search(self, board, depth, alpha, beta, stop_event):
        score, move = self._table.get_entry(board.to_hash(), depth, alpha, beta)

        if score is not None:
            self._stats['cache_hits'] += 1
            self._stats['nodes'] += 1

            return score, move
        
        score, move = super().search(board, depth, alpha, beta, stop_event)
        self._table.insert_entry(score, move, board.to_hash(), depth, alpha, beta)

        return score, move

class TTMinimaxCPU(TranspositionTableMixin, ABMinimaxCPU):
    def initialise_stats(self):
        super().initialise_stats()
        self._stats['cache_hits'] = 0
    
    def print_stats(self, score, move):
        self._stats['cache_hits_percentage'] = self._stats['cache_hits'] / self._stats['nodes']
        super().print_stats(score, move)