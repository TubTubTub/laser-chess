import pygame
from data.tools import _State
from data.components.widget_group import WidgetGroup
from data.components.widgets import ColourPicker, ColourButton, Dropdown
from data.states.settings.widget_dict import SETTINGS_WIDGETS
from data.components.custom_event import CustomEvent
from data.constants import SettingsEventType, BG_COLOUR, SCREEN_SIZE, SCREEN_FLAGS
from data.components.cursor import Cursor
import os

from data.utils.settings_helpers import get_default_settings, get_user_settings, update_user_settings

class Settings(_State):
    def __init__(self):
        super().__init__()
        self._screen = pygame.display.get_surface()
        self._cursor = Cursor()
        
        self._widget_group = None
        self._colour_picker = None

        self._settings = None
        self._window_size = pygame.display.get_window_size()
        self._window_position = pygame.display.get_window_position()
    
    def cleanup(self):
        print('cleaning settings.py')
        update_user_settings(self._settings)
    
    def startup(self, persist=None):
        print('starting settings.py')
        self._widget_group = WidgetGroup(SETTINGS_WIDGETS)
        self._widget_group.handle_resize(self._screen.size)
        self._settings = get_user_settings()

        self.draw()
    
    def create_colour_picker(self, origin_position, colour_type):
        if colour_type == 'primary':
            default_colour = self._settings['primaryBoardColour']
        else:
            default_colour = self._settings['secondaryBoardColour']

        self._colour_picker = ColourPicker(position=origin_position, relative_length=0.3, default_colour=default_colour, colour_type=colour_type)
        self._widget_group.add(self._colour_picker)
    
    def remove_colour_picker(self):
        self._colour_picker.kill()
    
    def set_display_mode(self, display_mode):
        if display_mode == 'fullscreen':
            self._window_size = pygame.display.get_window_size()
            self._window_position = pygame.display.get_window_position()
            pygame.display.set_mode((0, 0), SCREEN_FLAGS | pygame.FULLSCREEN)

        elif display_mode == 'windowed':
            os.environ['SDL_VIDEO_WINDOW_POS'] = str(self._window_position[0]) + ', ' + str(self._window_position[1])
            pygame.display.set_mode(self._window_size, SCREEN_FLAGS)
    
    def reload_settings(self):
        SETTINGS_WIDGETS['primary_colour_button'].initialise_new_colours(self._settings['primaryBoardColour'])
        SETTINGS_WIDGETS['secondary_colour_button'].initialise_new_colours(self._settings['secondaryBoardColour'])
        SETTINGS_WIDGETS['display_mode_dropdown'].set_selected_word(1)
        self.set_display_mode(self._settings['displayMode'])
    
    def get_event(self, event):
        widget_event = self._widget_group.process_event(event)

        if widget_event is None:
            if event.type == pygame.MOUSEBUTTONDOWN and self._colour_picker:
                self.remove_colour_picker()
            return
            
        match widget_event.type:
            case SettingsEventType.DROPDOWN_CLICK:
                selected_word = SETTINGS_WIDGETS['display_mode_dropdown'].get_selected_word()
                
                if selected_word is None or selected_word == self._settings['displayMode']:
                    return
                
                selected_word = selected_word.lower()
                self.set_display_mode(selected_word)

                self._settings['displayMode'] = selected_word

            case SettingsEventType.COLOUR_PICKER_HOVER:
                return

            case SettingsEventType.MENU_CLICK:
                self.next = 'menu'
                self.done = True
            
            case SettingsEventType.RESET_DEFAULT:
                self._settings = get_default_settings()
                self.reload_settings()
            
            case SettingsEventType.RESET_USER:
                self._settings = get_user_settings()
                self.reload_settings()
            
            case SettingsEventType.COLOUR_BUTTON_CLICK:
                mouse_pos = pygame.mouse.get_pos()

                if self._colour_picker:
                    self.remove_colour_picker()

                self.create_colour_picker(mouse_pos, widget_event.colour_type)
            
            case SettingsEventType.COLOUR_PICKER_CLICK:
                r, g, b = widget_event.colour.rgb
                hex_colour = f'0x{hex(r)[2:].zfill(2)}{hex(g)[2:].zfill(2)}{hex(b)[2:].zfill(2)}'

                if widget_event.colour_type == 'primary':
                    SETTINGS_WIDGETS['primary_colour_button'].initialise_new_colours(widget_event.colour)
                    self._settings['primaryBoardColour'] = hex_colour
                elif widget_event.colour_type == 'secondary':
                    SETTINGS_WIDGETS['secondary_colour_button'].initialise_new_colours(widget_event.colour)
                    self._settings['secondaryBoardColour'] = hex_colour
    
    def handle_resize(self):
        self._widget_group.handle_resize(self._screen.get_size())
    
    def draw(self):
        self._screen.fill(BG_COLOUR)
        self._widget_group.draw(self._screen)
    
    def update(self, **kwargs):
        self.draw()