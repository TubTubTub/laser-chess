from data.states.game.cpu.engines import *
from data.states.game.components.board import Board
from data.constants import Colour, Miscellaneous
# sc3ncfancpb2/2pc7/3Pd6/pa1Pc1rbra1pb1Pd/pb1Pd1RaRb1pa1Pc/6pb3/7Pa2/2PdNaFaNa3Sa b
# scfaRa7/RaRaRaFa6/RaRaRa7/10/10/10/10/9Sa b
# scfa8/10/10/10/10/10/10/8FaSa b

def compare(cls1, cls2, depth, rounds):
    wins = [0, 0]
    
    board = Board()
    def callback(move):
        board.apply_move(move, add_hash=True)

    cpu1 = cls1(callback=callback, max_depth=depth, verbose='compact')
    cpu2 = cls2(callback=callback, max_depth=depth, verbose='compact')

    for i in range(rounds):
        board = Board(fen_string="scfa8/10/10/10/10/10/10/8FaSa b")
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

compare(TTNegamaxCPU, TTNegamaxCPU, 2, 1)