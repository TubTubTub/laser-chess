import pygame
from data.constants import SCREEN_SIZE, SCREEN_FLAGS
from data.utils.data_helpers import get_user_settings

display_mode = get_user_settings()['displayMode']
is_fullscreen = False
if display_mode == 'fullscreen':
    is_fullscreen = pygame.FULLSCREEN

pygame.mixer.init()
pygame.init()

pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_FORWARD_COMPATIBLE_FLAG, True)

pygame.display.set_mode(SCREEN_SIZE, SCREEN_FLAGS | is_fullscreen)