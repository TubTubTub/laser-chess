import pygame
import sys
from data.main import main
from data.states.game.components.game_model import Board

print('Running run.py...')

board = Board()
def test():
    while True:
        print(board)
        move = board.get_move()
        board.apply_move(move)
        board.fire_laser()
        board.flip_colour()

if __name__ == '__main__':
    main()
    pygame.quit()
    sys.exit()
    test()