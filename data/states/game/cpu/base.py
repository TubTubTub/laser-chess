import time
from pprint import PrettyPrinter
from data.constants import Colour, Score, Miscellaneous
from data.states.game.cpu.evaluator import Evaluator
from data.managers.logs import initialise_logger

logger = initialise_logger(__name__)
printer = PrettyPrinter(indent=2, sort_dicts=False)

class BaseCPU:
    def __init__(self, callback, verbose=True):
        self._evaluator = Evaluator(verbose=False)
        self._verbose = verbose
        self._callback = callback
        self._stats = {}
    
    def initialise_stats(self):
        self._stats = {
            'nodes': 0,
            'leaf_nodes' : 0,
            'draws': 0,
            'mates': 0,
            'ms_per_node': 0,
            'time_taken': time.time()
        }
    
    def print_stats(self, score, move):
        """
        Prints statistics after traversing tree.

        Args:
            score (int): Final score obtained after traversal.
            move (Move): Best move obtained after traversal.
        """
        if self._verbose is False:
            return

        self._stats['time_taken'] = round(1000 * (time.time() - self._stats['time_taken']), 3)
        self._stats['ms_per_node'] = round(self._stats['time_taken'] / self._stats['nodes'], 3)

        # Prints stats across multiple lines
        if self._verbose is True:
            logger.info(f'\n\n'
                        f'{self.__str__()} Search Results:\n'
                        f'{printer.pformat(self._stats)}\n'
                        f'Best score:  {score}   Best move: {move}\n'
                        )
        
        # Prints stats in a compacted format
        elif self._verbose.lower() == 'compact':
            logger.info(self._stats)
            logger.info(f'Best score: {score}   Best move: {move}')

    def find_move(self, board, stop_event=None):
        raise NotImplementedError
    
    def search(self, board, depth, stop_event, absolute=False, **kwargs):
        if stop_event and stop_event.is_set():
            raise TimeoutError(f'Thread killed - stopping minimax function ({self.__str__}.search)')
        
        self._stats['nodes'] += 1

        if (winner := board.check_win()) is not None:
            self._stats['leaf_nodes'] += 1
            return self.process_win(winner, depth, absolute)

        if depth == 0:
            self._stats['leaf_nodes'] += 1
            return self._evaluator.evaluate(board, absolute), None
    
    def process_win(self, winner, depth, absolute):
        self._stats['leaf_nodes'] += 1

        if winner == Miscellaneous.DRAW:
            self._stats['draws'] += 1
            return 0, None
        elif winner == Colour.BLUE or absolute:
            self._stats['mates'] += 1
            return Score.CHECKMATE + depth, None
        elif winner == Colour.RED:
            self._stats['mates'] += 1
            return -Score.CHECKMATE - depth, None
    
    def __str__(self):
        return self.__class__.__name__