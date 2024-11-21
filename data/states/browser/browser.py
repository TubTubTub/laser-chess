import pygame
from data.tools import _State
from data.components.widget_group import WidgetGroup
from data.states.browser.widget_dict import BROWSER_WIDGETS
from data.constants import BrowserEventType
from data.components.cursor import Cursor
from data.assets import GRAPHICS, MUSIC_PATHS
from data.utils.asset_helpers import draw_background
from data.components.audio import audio
from data.components.animation import animation

class Browser(_State):
    def __init__(self):
        super().__init__()
        self._screen = pygame.display.get_surface()
        self._cursor = Cursor()
        
        self._widget_group = None
    
    def cleanup(self):
        print('cleaning browser.py')

        return None
    
    def startup(self, persist=None):
        print('starting browser.py')
        self._widget_group = WidgetGroup(BROWSER_WIDGETS)
        self._widget_group.handle_resize(self._screen.size)

        # audio.play_music(MUSIC_PATHS['menu'])

        self.draw()
    
    def get_event(self, event):
        widget_event = self._widget_group.process_event(event)

        if widget_event is None:
            return

        match widget_event.type:
            case BrowserEventType.MENU_CLICK:
                self.next = 'menu'
                self.done = True
    
    def handle_resize(self):
        self._widget_group.handle_resize(self._screen.get_size())
    
    def draw(self):
        background = pygame.Surface(self._screen.get_size())
        background.fill((50, 50, 50))
        draw_background(self._screen, background)
        self._widget_group.draw(self._screen)
    
    def update(self, **kwargs):
        self.draw()