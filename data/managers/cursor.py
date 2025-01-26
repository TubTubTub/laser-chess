import pygame
from data.assets import GRAPHICS
from data.constants import CursorMode

class CursorManager:
    def __init__(self):
        self.set_mode(CursorMode.ARROW)

    def set_mode(self, mode):
        pygame.mouse.set_visible(True)
        match mode:
            case CursorMode.ARROW:
                pygame.mouse.set_cursor((5, 5), GRAPHICS['cursor'])
            case CursorMode.IBEAM:
                pygame.mouse.set_cursor((5, 5), GRAPHICS['cursor'])
            case CursorMode.OPENHAND:
                pygame.mouse.set_cursor((5, 5), GRAPHICS['cursor'])
            case CursorMode.CLOSEDHAND:
                pygame.mouse.set_cursor((5, 5), GRAPHICS['cursor'])
            case CursorMode.NO:
                pygame.mouse.set_visible(False)

cursor = CursorManager()