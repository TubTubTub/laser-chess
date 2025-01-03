from data.states.game.cpu.base import BaseCPU
from data.states.game.components.evaluator import Evaluator
from data.constants import Colour
from pprint import pprint
import threading
import time

class SimpleCPU(BaseCPU):
    def __init__(self, callback, verbose=True):
        self._verbose = verbose
        self._evaluator = Evaluator(verbose=False)
        self._callback = callback

        self._stats = {
            'nodes': 0,
            'leaf_nodes' : 0,
            'mates': 0
        }
    
    def find_move(self, board, stop_event=None):
        best_move = self.search(board, stop_event)

        if self._verbose:
            print('\nCPU Search Results:')
            pprint(self._stats)
            print('Best move:', best_move, '\n')

        self._callback(best_move)
    
    def search(self, board, stop_event):
        if stop_event and stop_event.is_set():
            raise Exception('Thread killed - stopping minimax function (CPU.minimax)')
        
        best_score = 0
        best_move = None
        active_colour = board.bitboards.active_colour
        self._stats['nodes'] += 1

        for move in board.generate_all_moves(active_colour):
            laser_result = board.apply_move(move)

            self._stats['nodes'] += 1
            self._stats['leaf_nodes'] += 1
            if board.check_win() is not None:
                self._stats['mates'] += 1

            score = self._evaluator.evaluate(board)
            if active_colour == Colour.RED:
                score = -score

            if score > best_score:
                best_move = move
                best_score = score
                
            board.undo_move(move, laser_result)
            
        return best_move