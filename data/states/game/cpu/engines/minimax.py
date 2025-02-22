from data.states.game.cpu.base import BaseCPU
from data.constants import Score, Colour
from random import choice

class MinimaxCPU(BaseCPU):
    def __init__(self, max_depth, callback, verbose=False):
        super().__init__(callback, verbose)
        self._max_depth = max_depth

    def find_move(self, board, stop_event):
        """
        Finds the best move for the current board state.

        Args:
            board (Board): The current board state.
            stop_event (threading.Event): Event used to kill search from an external class.
        """
        self.initialise_stats()
        best_score, best_move = self.search(board, self._max_depth, stop_event)

        if self._verbose:
            self.print_stats(best_score, best_move)
            
        self._callback(best_move)

    def search(self, board, depth, stop_event):
        """
        Recursively DFS through minimax tree with evaluation score.

        Args:
            board (Board): The current board state.
            depth (int): The current search depth.
            stop_event (threading.Event): Event used to kill search from an external class.
        Returns:
            tuple[int, Move]: The best score and the best move found.
        """
        if (base_case := super().search(board, depth, stop_event)):
            return base_case

        best_move = None
        
        # Blue is the maximising player
        if board.get_active_colour() == Colour.BLUE:
            max_score = -Score.INFINITE
            
            for move in board.generate_all_moves(Colour.BLUE):
                laser_result = board.apply_move(move)
                
                new_score = self.search(board, depth - 1, stop_event)[0]

                if new_score > max_score:
                    max_score = new_score
                    best_move = move
                elif new_score == max_score:
                    # If evaluated scores are equal, pick a random move
                    choice([best_move, move])

                board.undo_move(move, laser_result)
                
            return max_score, best_move
            
        else:
            min_score = Score.INFINITE
            
            for move in board.generate_all_moves(Colour.RED):
                laser_result = board.apply_move(move)
                new_score = self.search(board, depth - 1, stop_event)[0]

                if new_score < min_score:
                    min_score = new_score
                    best_move = move
                elif new_score == min_score:
                    choice([best_move, move])
                
                board.undo_move(move, laser_result)
                
            return min_score, best_move