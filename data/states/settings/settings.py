import pygame
from data.tools import _State
from data.components.widget_group import WidgetGroup
from data.components.widgets import ColourPicker, ColourButton
from data.components.widget_dict import WIDGET_DICT
from data.components.custom_event import CustomEvent
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
    
    def startup(self, persist=None):
        print('starting settings.py')
        self._settings = get_user_settings()

        primary_colour_button = ColourButton(
            relative_position=(0.1, 0.3),
            size=(70, 35),
            default_colour=pygame.Color(self._settings['primaryBoardColour']).rgb,
            border_width=5,
            event=CustomEvent(SettingsEventType.COLOUR_BUTTON_CLICK, colour_type='primary')
        )
        secondary_colour_button = ColourButton(
            relative_position=(0.1, 0.5),
            size=(70, 35),
            default_colour=pygame.Color(self._settings['secondaryBoardColour']).rgb,
            border_width=5,
            event=CustomEvent(SettingsEventType.COLOUR_BUTTON_CLICK, colour_type='secondary')
        )

        self._widget_group.add(primary_colour_button)
        self._widget_group.add(secondary_colour_button)

        self.draw()
    
    def create_colour_picker(self, origin_position, colour_type):
        colour_picker = ColourPicker(position=origin_position, size=(300, 300), colour_type=colour_type)
        self._widget_group.add(colour_picker)
    
    def get_event(self, event):
        widget_event = self._widget_group.process_event(event)

        if widget_event is None:
            return
            
        match widget_event.type:
            case SettingsEventType.MENU_CLICK:
                self.next = 'menu'
                self.done = True
            case SettingsEventType.UPDATE_PRIMARY:
                self._settings['primaryBoardColour'] = '0x000000'
            case SettingsEventType.RESET_DEFAULT:
                self._settings = get_default_settings()
            case SettingsEventType.RESET_USER:
                self._settings = get_user_settings()
            case SettingsEventType.COLOUR_BUTTON_CLICK:
                mouse_pos = pygame.mouse.get_pos()
                self.create_colour_picker(mouse_pos, widget_event.colour_type)
            case SettingsEventType.COLOUR_PICKER_CLICK:
                r, g, b = widget_event.colour.rgb
                print(hex(r)[2:].zfill(2), hex(g)[2:].zfill(2), hex(b)[2:].zfill(2), 'SLEEP')
                hex_colour = f'0x{hex(r)[2:].zfill(2)}{hex(g)[2:].zfill(2)}{hex(b)[2:].zfill(2)}'
                print(hex_colour, 'wow')
                if widget_event.colour_type == 'primary':
                    self._settings['primaryBoardColour'] = hex_colour
                elif widget_event.colour_type == 'secondary':
                    self._settings['secondaryBoardColour'] = hex_colour
    
    def handle_resize(self):
        self._widget_group.handle_resize(self._screen.get_size())
    
    def draw(self):
        self._screen.fill(BG_COLOUR)
        self._widget_group.draw(self._screen)
    
    def update(self):
        self.draw()