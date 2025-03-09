import pygame
from data.utils.enums import CursorMode
from data.utils.assets import GRAPHICS

class CursorManager:
    def __init__(self):
        self._mode = CursorMode.ARROW
        self.set_mode(CursorMode.ARROW)

    def set_mode(self, mode):
        pygame.mouse.set_visible(True)

        match mode:
            case CursorMode.ARROW:
                pygame.mouse.set_cursor((7, 5), pygame.transform.scale(GRAPHICS['arrow'], (32, 32)))
            case CursorMode.IBEAM:
                pygame.mouse.set_cursor((15, 5), pygame.transform.scale(GRAPHICS['ibeam'], (32, 32)))
            case CursorMode.OPENHAND:
                pygame.mouse.set_cursor((17, 5), pygame.transform.scale(GRAPHICS['hand_open'], (32, 32)))
            case CursorMode.CLOSEDHAND:
                pygame.mouse.set_cursor((17, 5), pygame.transform.scale(GRAPHICS['hand_closed'], (32, 32)))
            case CursorMode.NO:
                pygame.mouse.set_visible(False)

        self._mode = mode

    def get_mode(self):
        return self._mode

cursor = CursorManager()