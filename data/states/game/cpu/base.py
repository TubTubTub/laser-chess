from data.states.game.cpu.evaluator import Evaluator
from data.constants import Colour, Score, Miscellaneous
from pprint import pprint
import time
from data.managers.logs import initialise_logger

logger = initialise_logger(__name__)

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
        if self._verbose is False:
            return

        self._stats['time_taken'] = round(1000 * (time.time() - self._stats['time_taken']), 3)
        self._stats['ms_per_node'] = round(self._stats['time_taken'] / self._stats['nodes'], 3)

        if self._verbose is True:
            logger.info(f'\n{self.__str__()} Search Results:', '\n')
            logger.info(self._stats, sort_dicts=False)
            logger.info('\n' + 'Best score:', score)
            logger.info('Best move:', move, '\n')
        
        elif self._verbose.lower() == 'compact':
            logger.info(self._stats)
            logger.info('Best score:', score, '     ', 'Best move:', move, '\n')

    def find_move(self, board, stop_event=None):
        raise NotImplementedError
    
    def search(self, board, depth, stop_event, absolute=False, **kwargs):
        if stop_event and stop_event.is_set():
            raise Exception(f'Thread killed - stopping minimax function ({self.__str__}.search)')
        
        self._stats['nodes'] += 1

        if (winner := board.check_win()) is not None:
            self._stats['leaf_nodes'] += 1
            return self.process_win(winner)

        if depth == 0:
            self._stats['leaf_nodes'] += 1
            return self._evaluator.evaluate(board, absolute), None
    
    def process_win(self, winner):
        self._stats['leaf_nodes'] += 1

        if winner == Miscellaneous.DRAW:
            self._stats['draws'] += 1
            return 0, None
        elif winner == Colour.BLUE:
            self._stats['mates'] += 1
            return Score.CHECKMATE, None
        elif winner == Colour.RED:
            self._stats['mates'] += 1
            return -Score.CHECKMATE, None
    
    def __str__(self):
        return self.__class__.__name__