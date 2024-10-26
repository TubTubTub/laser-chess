import pygame
from data.tools import _State
from data.components.widget_group import WidgetGroup
from data.states.menu.widget_dict import MENU_WIDGETS
from data.constants import MenuEventType
from data.components.cursor import Cursor
from data.assets import GRAPHICS, MUSIC_PATHS
from data.utils.asset_helpers import draw_background
from data.components.audio import audio

class Menu(_State):
    def __init__(self):
        super().__init__()
        self._screen = pygame.display.get_surface()
        self._cursor = Cursor()
        self._current_time = 0
        self._delta_time = 0.0
        
        self._widget_group = None
    
    def cleanup(self):
        print('cleaning menu.py')
    
    def startup(self, persist=None):
        print('starting menu.py')
        self._widget_group = WidgetGroup(MENU_WIDGETS)
        self._widget_group.handle_resize(self._screen.size)

        audio.play_music(MUSIC_PATHS['menu'])

        self.draw()
    
    def get_event(self, event):
        widget_event = self._widget_group.process_event(event)

        if widget_event is None:
            return

        match widget_event.type:
            case None:
                return

            case MenuEventType.CONFIG_CLICK:
                self.next = 'config'
                self.done = True
            case MenuEventType.SETTINGS_CLICK:
                self.next = 'settings'
                self.done = True
    
    def handle_resize(self):
        self._widget_group.handle_resize(self._screen.get_size())
    
    def draw(self):
        # draw_background(self._screen, GRAPHICS['background'], current_time=self._current_time)
        self._widget_group.draw(self._screen)
    
    def update(self, **kwargs):
        self._current_time = kwargs.get('current_time')
        self._delta_time = kwargs.get('delta_time')
        self.draw()