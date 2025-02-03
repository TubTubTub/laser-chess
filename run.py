import pygame
import sys
from data.main import main

from data.managers.logs import initialise_logger
logger = initialise_logger(__name__)

logger.info('Running run.py...')

if __name__ == '__main__':
    main()
    pygame.quit()
    sys.exit()