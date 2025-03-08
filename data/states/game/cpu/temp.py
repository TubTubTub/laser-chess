from data.constants import Score, Colour
from data.states.game.cpu.base import BaseCPU
from pprint import pprint

class MinimaxCPU(BaseCPU):
    def __init__(self, max_depth, callback, verbose):
        super().__init__(callback, verbose)
        self._max_depth = max_depth

    def find_move(self, board, stop_event):
        # No bit_length bug as None type returned, so Move __str__ called on NoneType I think (just deal with None being returned)
        try:
            best_move = self.search(board, self._max_depth, -Score.INFINITE, Score.INFINITE, stop_event)

            if self._verbose:
                print('\nCPU Search Results:')
                pprint(self._stats)
                print('Best move:', best_move, '\n')
                
                self._callback(self._best_move)
        except Exception as error:
            print('(MinimaxBase.find_move) Error has occured:')
            raise error

    def search(self, board, depth, alpha, beta, stop_event):
        if stop_event.is_set():
            raise Exception('Thread killed - stopping minimax function (CPU.minimax)')

        # cached_move, cached_score = self._transposition_table.get_entry(hash_key=board.bitboards.get_hash(), depth=depth, alpha=alpha, beta=beta)
        # if cached_move or cached_score:
        #     if depth == self._max_depth:
        #         self._best_move = cached_move
        #     return cached_score


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

                    if depth == self._max_depth:
                        self._best_move = move

                board.undo_move(move, laser_result)

                alpha = max(alpha, score)
                if depth == self._max_depth: # https://stackoverflow.com/questions/31429974/alphabeta-pruning-alpha-equals-or-greater-than-beta-why-equals
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
                    if depth == self._max_depth:
                        self._best_move = move
                
                board.undo_move(move, laser_result)

                beta = min(beta, score)
                if depth == self._max_depth:
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