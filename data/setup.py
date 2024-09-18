import pygame
from pathlib import Path
from data.tools import load_all_gfx
from data.constants import SCREEN_SIZE, SCREEN_FLAGS

pygame.init()
pygame.display.set_mode(SCREEN_SIZE, SCREEN_FLAGS)

module_path = Path(__file__).parent
GRAPHICS = load_all_gfx((module_path / '../resources/graphics').resolve())