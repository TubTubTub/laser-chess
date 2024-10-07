import pygame
from data.tools import _State
from data.components.widget_group import WidgetGroup
from data.components.widget_dict import WIDGET_DICT
from data.constants import SettingsEventType, BG_COLOUR
from data.components.cursor import Cursor

class Settings(_State):
    def __init__(self):
        super().__init__()
        self._screen = pygame.display.get_surface()
        self._cursor = Cursor()
        
        self._widget_group = WidgetGroup(WIDGET_DICT['settings'])
    
    def cleanup(self):
        print('cleaning settings.py')
    
    def startup(self):
        print('starting settings.py')
        self.draw()
    
    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            collided = self._cursor.get_sprite_collision(event.pos, self._widget_group)

            if collided is None:
                return
            
            match collided.event.type:
                case SettingsEventType.MENU_CLICK:
                    self.next = 'menu'
                    self.done = True
    
    def handle_resize(self):
        self._widget_group.handle_resize(self._screen.get_size())
    
    def draw(self):
        self._screen.fill(BG_COLOUR)
        self._widget_group.draw(self._screen)
    
    def update(self):
        self.draw()