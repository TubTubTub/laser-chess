import threading
import time
from data.states.game.components.board import Board
from data.states.game.cpu.evaluator import Evaluator
from data.managers.logs import initialise_logger
from data.states.game.cpu.engines import *
from data.constants import Colour

logger = initialise_logger(__name__)
evaluator = Evaluator(verbose=True)

def callback(move):
    print(move)
    board.apply_move(move)
    evaluator.evaluate(board)
    print(board)

# NEGAMAX BROKEN FOR SOME REASON
stop_event = threading.Event()
cpu = ABNegamaxCPU(max_depth=3, callback=callback)
board = Board(fen_string='sc3pcfcpb3/4Pb4Pc/pa6Ra2/2rd1nc5/5pb4/10/4Fa5/3PdNaPa3Sa b')

while board.check_win() is None:
    cpu.find_move(board, stop_event)
    # if board.get_active_colour() == Colour.BLUE:
    #     print('WAITING')
    #     time.sleep(10)