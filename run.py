# import pygame
import sys
# from data.main import main
from data.components.board import Board

print('Running run.py...')

board = Board()
def test():
    print(board)
    move = board.get_move()
    board.apply_move(move)

if __name__ == '__main__':
    # main()
    # pygame.quit()
    # sys.exit()
    test()