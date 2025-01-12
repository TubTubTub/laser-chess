from data.states.game.cpu.evaluator import Evaluator

class MoveOrderer:
    def __init__(self):
        self._evaluator = Evaluator(verbose=False)
    
    def get_eval(self, board, move):
        laser_result = board.apply_move(move)
        score = -self._evaluator.evaluate(board)
        board.undo_move(move, laser_result)
        return score
    
    def get_ordered_moves(self, board, colour):
        moves = board.generate_all_moves(colour)
        ordered_moves = sorted(moves, key=lambda move: self.get_eval(board, move), reverse=True)

        for move in ordered_moves:
            yield move