from sys import platform
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

    if platform == 'win32':
        import data.windows_setup as win_setup
        win_setup.set_win_resize_func(app.resize_window)

    app.setup_states(state_dict, 'menu')
    app.main_game_loop()