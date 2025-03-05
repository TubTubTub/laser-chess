import threading
from data.states.game.components.board import Board
from data.managers.logs import initialise_logger
from data.states.game.cpu.engines import *

logger = initialise_logger(__name__)

board = Board(fen_string='sc3ncfcncpb2/2pc7/3Pd6/pa1Pc1rbra1pb1Pd/pb1Pd1RaRb1pa1Pc/6pb3/7Pa2/2PdNaFaNa3Sa b')
cpu = IDMinimaxCPU(
    max_depth=3,
    callback=lambda move: board.apply_move(move),
    verbose=True
)

while board.check_win() is None:
    cpu.find_move(board, threading.Event())