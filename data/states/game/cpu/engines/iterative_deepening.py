from copy import deepcopy
from random import choice
from data.states.game.cpu.engines.transposition_table import TranspositionTableMixin
from data.states.game.cpu.transposition_table import TranspositionTable
from data.states.game.cpu.engines.alpha_beta import ABMinimaxCPU
from data.managers.logs import initialise_logger
from data.utils.enums import Score

logger = initialise_logger(__name__)

class IterativeDeepeningMixin:
    def find_move(self, board, stop_event):
        """
        Iterates through increasing depths to find the best move.

        Args:
            board (Board): The current board state.
            stop_event (threading.Event): Event used to kill search from an external class.
        """
        self._table = TranspositionTable()

        best_move = None

        for depth in range(1, self._max_depth + 1):
            self.initialise_stats()

            # Use copy of board as search can be terminated before all tested moves are undone
            board_copy = deepcopy(board)

            try:
                best_score, best_move = self.search(board_copy, depth, -Score.INFINITE, Score.INFINITE, stop_event, hint=best_move)
            except TimeoutError:
                # If allocated time is up, use previous depth's best move
                logger.info(f'Terminated CPU search early at depth {depth}. Using existing best move: {best_move}')

                if best_move is None:
                    # If search is terminated at depth 0, use random move
                    best_move = choice(board_copy.generate_all_moves())
                    logger.warning('CPU terminated before any best move found! Using random move.')

                break

            self._stats['ID_depth'] = depth

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