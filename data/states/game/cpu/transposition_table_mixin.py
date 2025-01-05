from data.states.game.cpu.transposition_table import TranspositionTable

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