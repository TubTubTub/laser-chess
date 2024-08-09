import pygame
import win32gui
import win32con

import data.setup
from data.tools import Control
from data.states.game import Game
from data.states.menu import Menu

def main():

    state_dict = {
        'menu': Menu(),
        'game': Game(),
    }

    app = Control()

    def wndProc(oldWndProc, draw_callback, hWnd, message, wParam, lParam):
        if message == win32con.WM_SIZE:
            draw_callback()
            win32gui.RedrawWindow(hWnd, None, None, win32con.RDW_INVALIDATE | win32con.RDW_ERASE)
        return win32gui.CallWindowProc(oldWndProc, hWnd, message, wParam, lParam)

    oldWndProc = win32gui.SetWindowLong(win32gui.GetForegroundWindow(), win32con.GWL_WNDPROC, lambda *args: wndProc(oldWndProc, app.resize_window_event, *args))\

    app.setup_states(state_dict, 'game')
    app.main_game_loop()