from data.constants import Score, Colour
from data.states.game.components.transposition_table import TranspositionTable
from data.states.game.cpu.simple import SimpleCPU

class MinimaxCPU(SimpleCPU):
    def __init__(self, max_depth, verbose):
        super().__init__(verbose)
        self._max_depth = max_depth

    def find_move(self, get_move_callback, stop_event):
        try:
            score = self.minimax(self._board, self._depth, -Score.INFINITE, Score.INFINITE, False, stop_event)

            if self._verbose:
                print('\nEvaluation:', score)
                print('\nBest move:', self._best_move) # No bit_length bug as None type returned, so Move __str__ called on NoneType I think (just deal with None being returned)
                print('\nNumber of iterations:', self.turns)
            
            get_move_callback(self._best_move)
        except Exception as error:
            print('(MinimaxBase.find_move) Error has occured:')
            raise error

    def minimax(self, board, depth, alpha, beta, debug, stop_event):
        if stop_event.is_set():
            raise Exception('Thread killed - stopping minimax function (CPU.minimax)')

        self.turns += 1

        cached_move, cached_score = self._transposition_table.get_entry(hash_key=board.bitboards.get_hash(), depth=depth, alpha=alpha, beta=beta)
        if cached_move or cached_score:
            if depth == self._depth:
                self._best_move = cached_move
            return cached_score


        if depth == 0:
            return self.evaluate(board)

        is_maximiser = board.get_active_colour() == Colour.BLUE 

        if is_maximiser:
            score = -Score.INFINITE
            
            for move in board.generate_all_moves(board.get_active_colour()):
                before, before_score = board.bitboards.get_rotation_string(), self.evaluate(board)

                laser_result = board.apply_move(move)
                new_score = self.minimax(board, depth - 1, alpha, beta, False, stop_event)

                if new_score >= score:
                    score = new_score

                    if depth == self._depth:
                        self._best_move = move

                board.undo_move(move, laser_result)

                alpha = max(alpha, score)
                if depth == self._depth: # https://stackoverflow.com/questions/31429974/alphabeta-pruning-alpha-equals-or-greater-than-beta-why-equals
                    if beta < alpha:
                        break
                else:
                    if beta <= alpha:
                        break
                
                after, after_score = board.bitboards.get_rotation_string(), self.evaluate(board)
                if (before != after or before_score != after_score):
                    print('shit\n\n')
                
            return score
            
        else:
            score = Score.INFINITE
            
            for move in board.generate_all_moves(board.get_active_colour()):
                bef, before_score = board.bitboards.get_rotation_string(), self.evaluate(board)

                laser_result = board.apply_move(move)
                new_score = self.minimax(board, depth - 1, alpha, beta, False, stop_event)

                if new_score <= score:
                    score = new_score
                    if depth == self._depth:
                        self._best_move = move
                
                board.undo_move(move, laser_result)

                beta = min(beta, score)
                if depth == self._depth:
                    if beta < alpha:
                        break
                else:
                    if beta <= alpha:
                        break
                
                after, after_score = board.bitboards.get_rotation_string(), self.evaluate(board)
                if (bef != after or before_score != after_score):
                    print('shit\n\n')
                    raise ValueError
                
            return score