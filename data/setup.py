import pygame
import os
import ctypes
import sys
from pathlib import Path
from data.tools import load_all_gfx

SCREEN_SIZE = (1000, 600)
SCREEN_FLAGS = pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE #DONT USE SCALED

pygame.init()
pygame.display.set_mode(SCREEN_SIZE, SCREEN_FLAGS)

if os.name != 'nt' or sys.getwindowsversion()[0] < 6:
    raise NotImplementedError("Incompatible OS!")

user32 = ctypes.windll.user32
user32.SetProcessDPIAware() # To deal with Windows High Text Size / Low Display Resolution Settings

module_path = Path(__file__).parent
GRAPHICS = load_all_gfx((module_path / '../resources/graphics').resolve())