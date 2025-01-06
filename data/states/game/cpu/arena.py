from data.states.game.cpu.simple import SimpleCPU
from data.states.game.cpu.minimax import MinimaxCPU
from data.states.game.components.board import Board
from data.constants import Colour, Miscellaneous

def compare(cls1, cls2, rounds):
    wins = [0, 0]
    
    board = Board()
    def callback(move):
        board.apply_move(move)
        print('APPLYING MOVE:', move)
    cpu1 = cls1(callback=callback, verbose=False)
    cpu2 = cls2(callback=callback, max_depth=2, verbose=False)

    for i in range(rounds):
        board = Board()

        if i % 2 == 0:
            players = { Colour.BLUE: cpu1, Colour.RED: cpu2 }
        else:
            players = { Colour.BLUE: cpu2, Colour.RED: cpu1 }

        while (winner := board.check_win()) is None:
            players[board.get_active_colour()].find_move(board, None)
        
        if winner == Miscellaneous.DRAW:
            wins[0] += 0.5
            wins[1] += 0.5
        else:
            if players[winner] == cpu1:
                wins[0] += 1
            else:
                wins[1] += 1

        print(f'ROUND {i + 1} | WINNER: {players[winner]} | PLY: {len(board.hash_list) - 1}')
    # print(f'{cpu1} WINS: {wins[0]} | {cpu2} WINS: {wins[1]}')

compare(SimpleCPU, MinimaxCPU, 10)