import pygame
from data.tools import _State
from data.components.widget_group import WidgetGroup
from data.components.widget_dict import WIDGET_DICT
from data.constants import MenuEventType, BG_COLOUR
from data.components.cursor import Cursor

class Menu(_State):
    def __init__(self):
        super().__init__()
        self._screen = pygame.display.get_surface()
        self._cursor = Cursor()
        
        self._widget_group = WidgetGroup(WIDGET_DICT['menu'])
    
    def cleanup(self):
        print('cleaning menu.py')
    
    def startup(self, persist=None):
        print('starting menu.py')
        self.draw()
    
    def get_event(self, event):
        widget_event = self._widget_group.process_event(event)

        match widget_event:
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
        self._screen.fill(BG_COLOUR)
        self._widget_group.draw(self._screen)
    
    def update(self):
        self.draw()