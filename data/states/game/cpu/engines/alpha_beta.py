from data.constants import Score, Colour
from data.states.game.cpu.base import BaseCPU
from random import choice

class ABMinimaxCPU(BaseCPU):
    def __init__(self, max_depth, callback, verbose=True):
        super().__init__(callback, verbose)
        self._max_depth = max_depth
    
    def initialise_stats(self):
        """
        Initialises the number of prunes to the statistics dictionary to be logged.
        """
        super().initialise_stats()
        self._stats['beta_prunes'] = 0
        self._stats['alpha_prunes'] = 0

    def find_move(self, board, stop_event):
        """
        Finds the best move for the current board state.

        Args:
            board (Board): The current board state.
            stop_event (threading.Event): Event used to kill search from an external class.
        """
        self.initialise_stats()
        best_score, best_move = self.search(board, self._max_depth, -Score.INFINITE, Score.INFINITE, stop_event)

        if self._verbose:
            self.print_stats(best_score, best_move)
            
        self._callback(best_move)

    def search(self, board, depth, alpha, beta, stop_event):
        """
        Recursively DFS through minimax tree while pruning branches using the alpha and beta bounds.

        Args:
            board (Board): The current board state.
            depth (int): The current search depth.
            alpha (int): The upper bound value.
            beta (int): The lower bound value.
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
                new_score = self.search(board, depth - 1, alpha, beta, stop_event)[0]

                if new_score > max_score:
                    max_score = new_score
                    best_move = move

                board.undo_move(move, laser_result)

                alpha = max(alpha, max_score)
                
                if beta <= alpha:
                    self._stats['alpha_prunes'] += 1
                    break
                
            return max_score, best_move
            
        else:
            min_score = Score.INFINITE
            
            for move in board.generate_all_moves(Colour.RED):
                laser_result = board.apply_move(move)
                new_score = self.search(board, depth - 1, alpha, beta, stop_event)[0]

                if new_score < min_score:
                    min_score = new_score
                    best_move = move
                
                board.undo_move(move, laser_result)

                beta = min(beta, min_score)
                if beta <= alpha:
                    self._stats['beta_prunes'] += 1
                    break
                
            return min_score, best_move

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