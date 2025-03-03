import threading
import time
from data.states.game.components.board import Board
from data.states.game.cpu.evaluator import Evaluator
from data.states.game.cpu.move_orderer import MoveOrderer
from data.managers.logs import initialise_logger
from data.states.game.cpu.engines import *

logger = initialise_logger(__name__)
evaluator = Evaluator(verbose=False)

def callback(move):
    board.apply_move(move)

# NEGAMAX BROKEN FOR SOME REASON
stop_event = threading.Event()
cpu = TTMinimaxCPU(max_depth=3, callback=callback, verbose=True)
board = Board(fen_string='sc3ncfcncpb2/2pc7/3Pd6/pa1Pc1rbra1pb1Pd/pb1Pd1RaRb1pa1Pc/6pb3/7Pa2/2PdNaFaNa3Sa b')

while board.check_win() is None:
    cpu.find_move(board, stop_event)
    # if board.get_active_colour() == Colour.BLUE:
    #     print('WAITING')
    #     time.sleep(10)