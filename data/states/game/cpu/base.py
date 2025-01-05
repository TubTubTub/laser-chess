from data.states.game.components.evaluator import Evaluator
from data.constants import Colour, Score, Miscellaneous
from pprint import pprint
import time

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
        self._stats['time_taken'] = round(1000 * (time.time() - self._stats['time_taken']), 3)
        self._stats['ms_per_node'] = round(self._stats['time_taken'] / self._stats['nodes'], 3)

        print(f'\n{self.__str__()} Search Results:', '\n')
        pprint(self._stats, sort_dicts=False)
        print('\n' + 'Best score:', score)
        print('Best move:', move, '\n')

    def find_move(self, board, stop_event=None):
        raise NotImplementedError
    
    def search(self):
        raise NotImplementedError
    
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