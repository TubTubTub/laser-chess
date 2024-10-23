import pygame
from pathlib import Path
from data.tools import load_all_gfx
from data.constants import SCREEN_SIZE, SCREEN_FLAGS
from data.utils.settings_helpers import get_user_settings

display_mode = get_user_settings()['displayMode']
is_fullscreen = 0
if display_mode == 'fullscreen':
    is_fullscreen = pygame.FULLSCREEN

pygame.init()
pygame.display.set_mode(SCREEN_SIZE, SCREEN_FLAGS | is_fullscreen)

module_path = Path(__file__).parent
print((module_path / '../resources/graphics').resolve())
GRAPHICS = load_all_gfx((module_path / '../resources/graphics').resolve())