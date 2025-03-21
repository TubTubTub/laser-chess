import pygame
import sys
from data.managers.logs import initialise_logger
from data.main import main

logger = initialise_logger(__name__)
logger.info('Running run.py...')

if __name__ == '__main__':
    main()
    pygame.quit()
    sys.exit()