from data.states.game.cpu.base import BaseCPU
from data.utils.enums import Colour, Score

class SimpleCPU(BaseCPU):
    def __init__(self, callback, verbose=True):
        super().__init__(callback, verbose)

    def find_move(self, board, stop_event=None):
        self.initialise_stats()
        best_score, best_move = self.search(board, stop_event)

        if self._verbose:
            self.print_stats(best_score, best_move)

        self._callback(best_move)

    def search(self, board, stop_event):
        if stop_event and stop_event.is_set():
            raise Exception('Thread killed - stopping simple function (SimpleCPU.search)')

        active_colour = board.bitboards.active_colour
        best_score = -Score.INFINITE if active_colour == Colour.BLUE else Score.INFINITE
        best_move = None

        for move in board.generate_all_moves(active_colour):
            laser_result = board.apply_move(move)

            self._stats['nodes'] += 1

            if winner := board.check_win() is not None:
                self.process_win(winner)
            else:
                self._stats['leaf_nodes'] += 1

            score = self._evaluator.evaluate(board)

            if (active_colour == Colour.BLUE and score > best_score) or (active_colour == Colour.RED and score < best_score):
                best_move = move
                best_score = score

            board.undo_move(move, laser_result)

        return best_score, best_move