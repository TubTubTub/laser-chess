import pygame
import pyperclip

from data.control import _State
from data.states.browser.widget_dict import BROWSER_WIDGETS

from data.components.widget_group import WidgetGroup
from data.components.animation import animation
from data.components.cursor import Cursor
from data.components.audio import audio

from data.assets import GRAPHICS

from data.constants import BrowserEventType, GAMES_PER_PAGE

from data.database.database_helpers import delete_game, get_ordered_games

from data.utils.asset_helpers import draw_background

from data.window import screen

class Browser(_State):
    def __init__(self):
        super().__init__()
        self._cursor = Cursor()
        
        self._selected_index = None
        self._filter_column = 'number_of_ply'
        self._filter_ascend = False
        self._games_list = []
        self._widget_group = None
        self._page_number = 1
    
    def cleanup(self):
        print('cleaning browser.py')

        if self._selected_index is not None:
            return self._games_list[self._selected_index]

        return None
    
    def startup(self, persist=None):
        print('starting browser.py')
        # audio.play_music(MUSIC_PATHS['menu'])

        self._filter_column = 'number_of_ply'
        self._filter_ascend = False

        self._widget_group = WidgetGroup(BROWSER_WIDGETS)
        self._widget_group.handle_resize(screen.size)
        BROWSER_WIDGETS['browser_strip'].kill()

        self.refresh_games_list()

        self.draw()
    
    def refresh_games_list(self):
        column_map = {
            'moves': 'number_of_ply',
            'winner': 'winner',
            'time': 'created_dt'
        }

        ascend_map = {
            'asc': True,
            'desc': False
        }

        filter_column = BROWSER_WIDGETS['filter_column_dropdown'].get_selected_word()
        filter_ascend = BROWSER_WIDGETS['filter_ascend_dropdown'].get_selected_word()

        self._selected_index = None

        start_row = (self._page_number - 1) * GAMES_PER_PAGE + 1
        end_row = (self._page_number) * GAMES_PER_PAGE
        self._games_list = get_ordered_games(column_map[filter_column], ascend_map[filter_ascend], start_row=start_row, end_row=end_row)
        BROWSER_WIDGETS['browser_strip'].initialise_games_list(self._games_list)
        BROWSER_WIDGETS['scroll_area'].set_image()
    
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
                pyperclip.copy(self._games_list[self._selected_index]['fen_string'])

            case BrowserEventType.DELETE_CLICK:
                if self._selected_index is None:
                    return
                delete_game(self._games_list[self._selected_index]['id'])
                self.refresh_games_list()
            
            case BrowserEventType.REVIEW_CLICK:
                if self._selected_index is None:
                    return
                
                self.next = 'review'
                self.done = True

            case BrowserEventType.FILTER_COLUMN_CLICK:
                selected_word = BROWSER_WIDGETS['filter_column_dropdown'].get_selected_word()
            
                if selected_word is None:
                    return
                
                self.refresh_games_list()

            case BrowserEventType.FILTER_ASCEND_CLICK:
                selected_word = BROWSER_WIDGETS['filter_ascend_dropdown'].get_selected_word()
            
                if selected_word is None:
                    return
                
                self.refresh_games_list()
            
            case BrowserEventType.PAGE_CLICK:
                self._page_number = widget_event.data

                self.refresh_games_list()

    
    def handle_resize(self):
        self._widget_group.handle_resize(screen.get_size())
    
    def draw(self):
        draw_background(screen, GRAPHICS['temp_background'])
        self._widget_group.handle_resize(screen.get_size())
        self._widget_group.draw()
    
    def update(self, **kwargs):
        self.draw()
        