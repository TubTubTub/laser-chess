import threading
from data.states.game.components.board import Board
from data.managers.logs import initialise_logger
from data.states.game.cpu.engines import *

logger = initialise_logger(__name__)

stop_event = threading.Event()
board = Board(fen_string='sc9/10/10/7fa2/10/7Pb1Pc/10/7Fa1Sa b')
cpu = ABNegamaxCPU(max_depth=3, callback=lambda move: logger.info(f'BEST MOVE: {move}'))
cpu.find_move(board, stop_event)