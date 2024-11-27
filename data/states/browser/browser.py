import pygame
import pyperclip

from data.tools import _State
from data.states.browser.widget_dict import BROWSER_WIDGETS

from data.components.widget_group import WidgetGroup
from data.components.animation import animation
from data.components.cursor import Cursor
from data.components.audio import audio

from data.constants import BrowserEventType

from data.database.database_helpers import get_all_games
from data.utils.asset_helpers import draw_background

class Browser(_State):
    def __init__(self):
        super().__init__()
        self._screen = pygame.display.get_surface()
        self._cursor = Cursor()
        
        self._selected_index = None
        self._games_list = []
        self._widget_group = None
    
    def cleanup(self):
        print('cleaning browser.py')

        return None
    
    def startup(self, persist=None):
        print('starting browser.py')
        # audio.play_music(MUSIC_PATHS['menu'])

        self._widget_group = WidgetGroup(BROWSER_WIDGETS)
        self._widget_group.handle_resize(self._screen.size)
        BROWSER_WIDGETS['browser_strip'].kill()

        self._selected_index = None
        self._games_list = get_all_games()
        BROWSER_WIDGETS['browser_strip'].initialise_games_list(self._games_list)
        BROWSER_WIDGETS['scroll_area'].set_image()

        self.draw()
    
    def get_event(self, event):
        widget_event = self._widget_group.process_event(event)

        if widget_event is None:
            return

        match widget_event.type:
            case BrowserEventType.MENU_CLICK:
                self.next = 'menu'
                self.done = True
            case BrowserEventType.BROWSER_STRIP_CLICK:
                self._selected_index = widget_event.selected_index
            case BrowserEventType.COPY_CLICK:
                if self._selected_index is None:
                    return
                print('COPYING TO CLIPBOARD:', self._games_list[self._selected_index]['fen_string'])
                pyperclip.copy(self._games_list[self._selected_index]['fen_string']) // IF COPY FEN STRING THEN LASER COLOUR STARTS WRONG SOMETIMES
    
    def handle_resize(self):
        self._widget_group.handle_resize(self._screen.get_size())
    
    def draw(self):
        background = pygame.Surface(self._screen.get_size())
        background.fill((50, 50, 50))
        draw_background(self._screen, background)
        self._widget_group.draw(self._screen)
    
    def update(self, **kwargs):
        self.draw()
        