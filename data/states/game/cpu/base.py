import pygame
from data.states.game.components.evaluator import Evaluator
from pprint import pprint
import time

class BaseCPU:
    def __init__(self, callback, verbose=True):
        self._verbose = verbose
        self._evaluator = Evaluator(verbose=False)
        self._callback = callback
        self._stats = {}
    
    def initialise_stats(self):
        self._stats = {
            'nodes': 0,
            'leaf_nodes' : 0,
            'mates': 0,
            'ms_per_node': 0,
            'time_taken': time.time()
        }
    
    def print_stats(self, score, move):
        self._stats['time_taken'] = round(1000 * (time.time() - self._stats['time_taken']), 3)
        self._stats['ms_per_node'] = round(self._stats['time_taken'] / self._stats['nodes'], 3)

        print('\nCPU Search Results:')
        pprint(self._stats, sort_dicts=False)
        print('Best score:', score, '\n')
        print('Best move:', move, '\n')

    def find_move(self, board, stop_event=None):
        raise NotImplementedError
    
    def search(self):
        raise NotImplementedError