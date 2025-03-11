from data.states.game.cpu.evaluator import Evaluator
from data.states.game.components.board import Board
from data.managers.logs import initialise_logger

logger = initialise_logger(__name__)
evaluator = Evaluator(verbose=True)

TEST_FEN_STRINGS = [
    'sc9/10/10/4paPa4/5Pa4/10/10/9Sa b', # Material
    'sc9/4nanana3/10/10/10/4NaNaNa3/10/9Sa b', # Position
    'scpapa7/papapa7/papapa1Pa1Pa1Pa1/10/4Pa1Pa1Pa1/10/4Pa1Pa3/9Sa b', # Mobility
    'sc4fa3pa/10/10/10/10/10/10/5FaPa2Sa b', # King Safety
    'scnc1fcncpbpb3/pa9/pb1pc1rbpa3Pd/1Pc2Pd4Pc/2Pd1RaRb4/10/7Pa2/2PdNaFaNa3Sa b' # Combined
]

for fen_string in TEST_FEN_STRINGS:
    board = Board(fen_string)
    logger.info(f'Evaluating FEN string - {fen_string}')
    score = evaluator.evaluate(board)