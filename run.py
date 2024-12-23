import pygame
import sys
from data.main import main
from data.states.game.components.game_model import Board

print('Running run.py...')

if __name__ == '__main__':
    main()
    pygame.quit()
    sys.exit()