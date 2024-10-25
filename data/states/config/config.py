import pygame

from data.tools import _State

from data.states.config.widget_dict import CONFIG_WIDGETS

from data.components.widget_group import WidgetGroup
from data.components.cursor import Cursor
from data.components.audio import audio

from data.assets import MUSIC_PATHS

from data.constants import ConfigEventType, BG_COLOUR

class Config(_State):
    def __init__(self):
        super().__init__()
        self._screen = pygame.display.get_surface()
        self._cursor = Cursor()
        
        self._widget_group = None
    
    def cleanup(self):
        print('cleaning config.py')

        return {
            # 'cpu_depth': 2,
        }
    
    def startup(self, persist=None):
        print('starting config.py')
        self._widget_group = WidgetGroup(CONFIG_WIDGETS)
        self._widget_group.handle_resize(self._screen.size)
        self.draw()

        audio.play_music(MUSIC_PATHS['cpu_hard'])
    
    def get_event(self, event):
        widget_event = self._widget_group.process_event(event)

        if widget_event is None:
            return

        match widget_event.type:
            case ConfigEventType.GAME_CLICK:
                self.next = 'game'
                self.done = True
            case ConfigEventType.MENU_CLICK:
                self.next = 'menu'
                self.done = True
    
    def handle_resize(self):
        self._widget_group.handle_resize(self._screen.get_size())
    
    def draw(self):
        self._screen.fill(BG_COLOUR)
        self._widget_group.draw(self._screen)
    
    def update(self, **kwargs):
        self.draw()