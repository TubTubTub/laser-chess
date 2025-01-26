from sys import platform
import data.setup
from data.control import Control
from data.states.game.game import Game
from data.states.menu.menu import Menu
from data.states.settings.settings import Settings
from data.states.config.config import Config
from data.states.browser.browser import Browser
from data.states.review.review import Review
from data.states.editor.editor import Editor

def main():
    state_dict = {
        'menu': Menu(),
        'game': Game(),
        'settings': Settings(),
        'config': Config(),
        'browser': Browser(),
        'review': Review(),
        'editor': Editor()
    }

    app = Control()

    if platform == 'win32':
        import data.windows_setup as win_setup
        win_setup.set_win_resize_func(app.update_window)

    app.setup_states(state_dict, 'menu')
    app.main_game_loop()