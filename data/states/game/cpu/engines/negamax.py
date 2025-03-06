from random import choice
from data.states.game.cpu.engines.transposition_table import TranspositionTableMixin
from data.states.game.cpu.engines.iterative_deepening import IterativeDeepeningMixin
from data.states.game.cpu.base import BaseCPU
from data.constants import Score

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

    def search(self, board, depth, stop_event, moves=None):
        if (base_case := super().search(board, depth, stop_event, absolute=True)):
            return base_case
        
        best_move = None
        best_score = -Score.INFINITE

        for move in board.generate_all_moves(board.get_active_colour()):
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

class ABNegamaxCPU(BaseCPU):
    def __init__(self, max_depth, callback, verbose=True):
        super().__init__(callback, verbose)
        self._max_depth = max_depth
    
    def initialise_stats(self):
        """Initialises the statistics for the search."""
        super().initialise_stats()
        self._stats['beta_prunes'] = 0

    def find_move(self, board, stop_event):
        """Finds the best move for the current board state.

        Args:
            board (Board): The current board state.
            stop_event (threading.Event): The event to signal stopping the search.
        """
        self.initialise_stats()
        best_score, best_move = self.search(board, self._max_depth, -Score.INFINITE, Score.INFINITE, stop_event)

        if self._verbose:
            self.print_stats(best_score, best_move)
            
        self._callback(best_move)

    def search(self, board, depth, alpha, beta, stop_event):
        """Searches for the best move using the Alpha-Beta Negamax algorithm.

        Args:
            board (Board): The current board state.
            depth (int): The current depth in the game tree.
            alpha (int): The alpha value for pruning.
            beta (int): The beta value for pruning.
            stop_event (threading.Event): The event to signal stopping the search.

        Returns:
            tuple: The best score and the best move found.
        """
        if (base_case := super().search(board, depth, stop_event, absolute=True)):
            return base_case

        best_move = None
        best_score = alpha

        for move in board.generate_all_moves(board.get_active_colour()):
            laser_result = board.apply_move(move)

            new_score = self.search(board, depth - 1, -beta, -best_score, stop_event)[0]
            new_score = -new_score

            if new_score > best_score:
                best_score = new_score
                best_move = move
            elif new_score == best_score:
                best_move = choice([best_move, move])
                
            board.undo_move(move, laser_result)
            
            if best_score >= beta:
                self._stats['beta_prunes'] += 1
                break
        
        return best_score, best_move

class TTNegamaxCPU(TranspositionTableMixin, ABNegamaxCPU):
    def initialise_stats(self):
        """Initialises the statistics for the search."""
        super().initialise_stats()
        self._stats['cache_hits'] = 0
    
    def print_stats(self, score, move):
        """Prints the statistics for the search.

        Args:
            score (int): The best score found.
            move (Move): The best move found.
        """
        self._stats['cache_hits_percentage'] = round(self._stats['cache_hits'] / self._stats['nodes'], 3)
        self._stats['cache_entries'] = len(self._table._table)
        super().print_stats(score, move)

class IDNegamaxCPU(TranspositionTableMixin, IterativeDeepeningMixin, ABNegamaxCPU):
    def initialise_stats(self):
        """Initialises the statistics for the search."""
        super().initialise_stats()
        self._stats['cache_hits'] = 0
    
    def print_stats(self, score, move):
        """Prints the statistics for the search.

        Args:
            score (int): The best score found.
            move (Move): The best move found.
        """
        self._stats['cache_hits_percentage'] = self._stats['cache_hits'] / self._stats['nodes']
        self._stats['cache_entries'] = len(self._table._table)
        super().print_stats(score, move)