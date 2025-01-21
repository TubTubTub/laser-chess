import pygame
from data.control import _State
from data.components.widget_group import WidgetGroup
from data.states.menu.widget_dict import MENU_WIDGETS
from data.constants import MenuEventType
from data.components.cursor import Cursor
from data.assets import GRAPHICS, MUSIC_PATHS
from data.utils.asset_helpers import draw_background
from data.managers.audio import audio
from data.managers.animation import animation
from data.managers.window import screen

class Menu(_State):
    def __init__(self):
        super().__init__()
        self._cursor = Cursor()
        
        self._widget_group = None
    
    def cleanup(self):
        print('cleaning menu.py')

        return None
    
    def startup(self, persist=None):
        print('starting menu.py')
        self._widget_group = WidgetGroup(MENU_WIDGETS)
        self._widget_group.handle_resize(screen.size)

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
            case MenuEventType.BROWSER_CLICK:
                self.next = 'browser'
                self.done = True
    
    def handle_resize(self):
        self._widget_group.handle_resize(screen.get_size())
    
    def draw(self):
        draw_background(screen, GRAPHICS['temp_background'])
        surface = pygame.Surface(screen.size)
        surface.fill((0, 0, 100))
        draw_background(screen, surface)
        self._widget_group.draw()
    
    def update(self, **kwargs):
        self.draw()