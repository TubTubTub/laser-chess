import win32gui
import win32con
import os
import ctypes
import sys

def wndProc(oldWndProc, draw_callback, hWnd, message, wParam, lParam):
    if message == win32con.WM_SIZING:
        draw_callback(resize=True)
        win32gui.RedrawWindow(hWnd, None, None, win32con.RDW_INVALIDATE | win32con.RDW_ERASE)
    elif message == win32con.WM_MOVE:
        draw_callback(resize=False)
    return win32gui.CallWindowProc(oldWndProc, hWnd, message, wParam, lParam)

def set_win_resize_func(resize_function):
    oldWndProc = win32gui.SetWindowLong(win32gui.GetForegroundWindow(), win32con.GWL_WNDPROC, lambda *args: wndProc(oldWndProc, resize_function, *args))

user32 = ctypes.windll.user32
user32.SetProcessDPIAware() # To deal with Windows High Text Size / Low Display Resolution Settings

if os.name != 'nt' or sys.getwindowsversion()[0] < 6:
    raise NotImplementedError("Incompatible OS!")