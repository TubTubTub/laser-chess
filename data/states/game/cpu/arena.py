from data.states.game.cpu.engines.simple import SimpleCPU
from data.states.game.cpu.engines.minimax import MinimaxCPU
from data.states.game.cpu.engines.negamax import NegamaxCPU
from data.states.game.cpu.engines.alpha_beta import ABNegamaxCPU, ABMinimaxCPU
from data.states.game.cpu.engines.transposition_table import TTMinimaxCPU, TTNegamaxCPU
from data.states.game.components.board import Board
from data.constants import Colour, Miscellaneous

def compare(cls1, cls2, rounds):
    wins = [0, 0]
    
    board = Board()
    def callback(move):
        board.apply_move(move, add_hash=True)

    cpu1 = cls1(callback=callback, max_depth=2, verbose='compact')
    cpu2 = cls2(callback=callback, max_depth=2, verbose='compact')

    for i in range(rounds):
        board = Board()
        ply = 0

        if i % 2 == 0:
            players = { Colour.BLUE: cpu1, Colour.RED: cpu2, Miscellaneous.DRAW: 'DRAW' }
        else:
            players = { Colour.BLUE: cpu2, Colour.RED: cpu1, Miscellaneous.DRAW: 'DRAW' }

        while (winner := board.check_win()) is None:
            players[board.get_active_colour()].find_move(board, None)
            ply += 1
            print('PLY:', ply)
        
        if winner == Miscellaneous.DRAW:
            wins[0] += 0.5
            wins[1] += 0.5
        else:
            if players[winner] == cpu1:
                wins[0] += 1
            else:
                wins[1] += 1

        print(f'ROUND {i + 1} | WINNER: {players[winner]} | PLY: {ply}')
    
    print(f'{cpu1} SCORE: {wins[0]} | {cpu2} SCORE: {wins[1]}')

compare(TTNegamaxCPU, TTNegamaxCPU, 3)