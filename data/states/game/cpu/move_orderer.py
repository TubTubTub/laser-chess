from data.states.game.cpu.evaluator import Evaluator
from data.constants import Colour
from data.utils.bitboard_helpers import print_bitboard
class MoveOrderer:
    def __init__(self):
        self._evaluator = Evaluator(verbose=False)
    
    def get_eval(self, board, move):
        laser_result = board.apply_move(move)
        score = -self._evaluator.evaluate(board)
        board.undo_move(move, laser_result)
        return score

    def score_moves(self, board, moves):
        for i in range(len(moves)):
            score = self.get_eval(board, moves[i])
            moves[i] = (moves[i], score)
        
        return moves

    def best_move_to_front(self, moves, start_idx, colour, hint):
        for i in range(start_idx + 1, len(moves)):
            if moves[i].src in hint:
                moves[i], moves[start_idx] = moves[start_idx], moves[i] 
                return
            # if moves[i][1] > moves[start_idx][1] and colour == Colour.BLUE:
                
            # if moves[i][1] < moves[start_idx][1] and colour == Colour.RED:
            #     moves[i], moves[start_idx] = moves[start_idx], moves[i] 
    
    def get_moves(self, board, hint=None):
        # if hint is not None:
        #     yield hint
        
        colour = board.get_active_colour()
        moves = list(board.generate_all_moves(colour))
        # moves = self.score_moves(board, moves)
        
        for i in range(len(moves)):
            before = moves[::]

            if hint:
                self.best_move_to_front(moves, i, colour, hint)
                
            # if before != moves:
            #     print('CHANGED')
            #     print_bitboard(moves[i].src)
            #     print(board)

            yield moves[i]

        # ordered_moves = sorted(moves, key=lambda move: self.get_eval(board, move), reverse=True)

        # for move in ordered_moves:
        #     yield move