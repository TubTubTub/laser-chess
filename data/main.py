import pygame
import os
import sys
import ctypes
import win32gui
import win32con

from . import tools
from .states import game, menu

def main():
    pygame.init()

    if os.name != 'nt' or sys.getwindowsversion()[0] < 6:
        raise NotImplementedError("Incompatible OS!")

    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware() # To deal with Windows High Text Size / Low Display Resolution Settings

    settings = {
        'size': (1000, 600),
        'fps': 60,
        'screenFlags': pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE #DONT USE SCALED
    }
    state_dict = {
        'menu': menu.Menu(),
        'game': game.Game(),
    }

    app = tools.Control(**settings)

    def wndProc(oldWndProc, draw_callback, hWnd, message, wParam, lParam):
        if message == win32con.WM_SIZE:
            draw_callback()
            win32gui.RedrawWindow(hWnd, None, None, win32con.RDW_INVALIDATE | win32con.RDW_ERASE)
        return win32gui.CallWindowProc(oldWndProc, hWnd, message, wParam, lParam)

    oldWndProc = win32gui.SetWindowLong(win32gui.GetForegroundWindow(), win32con.GWL_WNDPROC, lambda *args: wndProc(oldWndProc, app.update, *args))\

    app.setup_states(state_dict, 'game')
    app.main_game_loop()