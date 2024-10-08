import pygame
from data.tools import _State
from data.components.widget_group import WidgetGroup
from data.components.widget_dict import WIDGET_DICT
from data.constants import SettingsEventType, BG_COLOUR
from data.components.cursor import Cursor

from data.utils.settings_helpers import get_default_settings, get_user_settings, update_user_settings

class Settings(_State):
    def __init__(self):
        super().__init__()
        self._screen = pygame.display.get_surface()
        self._cursor = Cursor()
        
        self._widget_group = WidgetGroup(WIDGET_DICT['settings'])

        self._settings = None
    
    def cleanup(self):
        print('cleaning settings.py')
        update_user_settings(self._settings)
    
    def startup(self):
        print('starting settings.py')
        self._settings = get_user_settings()
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
                case SettingsEventType.UPDATE_PRIMARY:
                    self._settings['primaryBoardColour'] = '0x000000'
                case SettingsEventType.RESET_DEFAULT:
                    self._settings = get_default_settings()
                case SettingsEventType.RESET_USER:
                    self._settings = get_user_settings()
    
    def handle_resize(self):
        self._widget_group.handle_resize(self._screen.get_size())
    
    def draw(self):
        self._screen.fill(BG_COLOUR)
        self._widget_group.draw(self._screen)
    
    def update(self):
        self.draw()