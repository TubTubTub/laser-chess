import pygame
import pyperclip

from data.control import _State
from data.states.browser.widget_dict import BROWSER_WIDGETS

from data.components.widget_group import WidgetGroup
from data.managers.animation import animation
from data.components.cursor import Cursor
from data.managers.audio import audio

from data.assets import GRAPHICS, MUSIC

from data.constants import BrowserEventType, ShaderType, GAMES_PER_PAGE

from data.utils.database_helpers import delete_game, get_ordered_games

from data.utils.asset_helpers import draw_background

from data.managers.window import window
from data.managers.logs import initialise_logger
from random import randint

logger = initialise_logger(__name__)

class Browser(_State):
    def __init__(self):
        super().__init__()
        
        self._selected_index = None
        self._filter_column = 'number_of_ply'
        self._filter_ascend = False
        self._games_list = []
        self._page_number = 1
    
    def cleanup(self):
        super().cleanup()
        
        if self._selected_index is not None:
            return self._games_list[self._selected_index]

        return None
    
    def startup(self, persist=None):
        self.refresh_games_list() # BEFORE RESIZE TO FILL WIDGET BEFORE RESIZING
        super().startup(BROWSER_WIDGETS, music=MUSIC[f'menu_{randint(1, 3)}'])

        self._filter_column = 'number_of_ply'
        self._filter_ascend = False

        window.set_apply_arguments(ShaderType.BASE, background_type=ShaderType._BACKGROUND_WAVES)

        BROWSER_WIDGETS['help'].kill()
        BROWSER_WIDGETS['browser_strip'].kill()

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
        BROWSER_WIDGETS['browser_strip'].set_surface_size(window.size)
        BROWSER_WIDGETS['scroll_area'].set_image()

    def get_event(self, event):
        widget_event = self._widget_group.process_event(event)

        if event.type in [pygame.MOUSEBUTTONUP, pygame.KEYDOWN]:
            BROWSER_WIDGETS['help'].kill()

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
                logger.info('COPYING TO CLIPBOARD:', self._games_list[self._selected_index]['fen_string'])
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
            
            case BrowserEventType.HELP_CLICK:
                self._widget_group.add(BROWSER_WIDGETS['help'])
                self._widget_group.handle_resize(window.size)
    
    def draw(self):
        self._widget_group.draw()