import pygame
from data.constants import SCREEN_SIZE, SCREEN_FLAGS
from data.utils.settings_helpers import get_user_settings

display_mode = get_user_settings()['displayMode']
is_fullscreen = False
if display_mode == 'fullscreen':
    is_fullscreen = pygame.FULLSCREEN

pygame.init()
pygame.display.set_mode(SCREEN_SIZE, SCREEN_FLAGS | is_fullscreen)