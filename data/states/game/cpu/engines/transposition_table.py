from data.states.game.cpu.transposition_table import TranspositionTable
from data.states.game.cpu.engines.alpha_beta import ABMinimaxCPU

class TranspositionTableMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._table = TranspositionTable()
    
    def find_move(self, *args, **kwargs):
        self._table = TranspositionTable()
        super().find_move(*args, **kwargs)
    
    def search(self, board, depth, alpha, beta, stop_event, hint=None, laser_coords=None):
        """
        Searches transposition table for a cached move before running a full search if necessary.
        Caches the searched result.

        Args:
            board (Board): The current board state.
            depth (int): The current search depth.
            alpha (int): The upper bound value.
            beta (int): The lower bound value.
            stop_event (threading.Event): Event used to kill search from an external class.

        Returns:
            tuple[int, Move]: The best score and the best move found.
        """
        hash = board.to_hash()
        score, move = self._table.get_entry(hash, depth, alpha, beta)

        if score is not None:
            self._stats['cache_hits'] += 1
            self._stats['nodes'] += 1

            return score, move
        else:
            # If board hash entry not found in cache, run a full search
            score, move = super().search(board, depth, alpha, beta, stop_event, hint)
            self._table.insert_entry(score, move, hash, depth, alpha, beta)

            return score, move

class TTMinimaxCPU(TranspositionTableMixin, ABMinimaxCPU):
    def initialise_stats(self):
        """
        Initialises cache statistics to be logged.
        """
        super().initialise_stats()
        self._stats['cache_hits'] = 0
    
    def print_stats(self, score, move):
        """
        Logs the statistics for the search.

        Args:
            score (int): The best score found.
            move (Move): The best move found.
        """
        # Calculate number of cached entries retrieved as a percentage of all nodes
        self._stats['cache_hits_percentage'] = round(self._stats['cache_hits'] / self._stats['nodes'], 3)
        self._stats['cache_entries'] = len(self._table._table)
        super().print_stats(score, move)