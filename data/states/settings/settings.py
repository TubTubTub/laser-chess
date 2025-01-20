import pygame
import pprint
import os

from data.control import _State

from data.states.settings.widget_dict import SETTINGS_WIDGETS

from data.components.widget_group import WidgetGroup
from data.widgets import ColourPicker
from data.managers.audio import audio
from data.managers.animation import animation

from data.utils.data_helpers import get_default_settings, get_user_settings, update_user_settings

from data.assets import MUSIC_PATHS, GRAPHICS
from data.utils.asset_helpers import draw_background

from data.constants import SettingsEventType, SCREEN_FLAGS
from data.managers.window import screen, window

class Settings(_State):
    def __init__(self):
        super().__init__()
        
        self._widget_group = None
        self._colour_picker = None

        self._settings = None
    
    def cleanup(self):
        print('cleaning settings.py')
        # print('\nUPDATING SETTINGS:', )
        # pprint.pprint(self._settings)
        # print('')

        update_user_settings(self._settings)

        return None
    
    def startup(self, persist=None):
        print('starting settings.py')
        self._widget_group = WidgetGroup(SETTINGS_WIDGETS)
        self._widget_group.handle_resize(screen.size)
        self._settings = get_user_settings()
        self.reload_settings()

        # print('\nGETTING USER SETTINGS:')
        # pprint.pprint(self._settings)
        # print('')

        audio.play_music(MUSIC_PATHS['menu'])

        self.draw()
    
    def create_colour_picker(self, relative_position, button_type):
        if button_type == SettingsEventType.PRIMARY_COLOUR_BUTTON_CLICK:
            fill_colour = self._settings['primaryBoardColour']
            event_type = SettingsEventType.PRIMARY_COLOUR_PICKER_CLICK
        else:
            fill_colour = self._settings['secondaryBoardColour']
            event_type = SettingsEventType.SECONDARY_COLOUR_PICKER_CLICK

        self._colour_picker = ColourPicker(
            relative_position=relative_position,
            relative_width=0.15,
            fill_colour=fill_colour,
            event_type=event_type
        )
        self._widget_group.add(self._colour_picker)
    
    def remove_colour_picker(self):
        self._colour_picker.kill()
    
    def set_display_mode(self, display_mode):
        if display_mode == 'fullscreen':
            window.set_fullscreen()

        elif display_mode == 'windowed':
            window.set_windowed()
            window.restore()
        
        self._widget_group.handle_resize(screen.size)
    
    def reload_settings(self):
        SETTINGS_WIDGETS['primary_colour_button'].initialise_new_colours(self._settings['primaryBoardColour'])
        SETTINGS_WIDGETS['secondary_colour_button'].initialise_new_colours(self._settings['secondaryBoardColour'])
        SETTINGS_WIDGETS['music_volume_slider'].set_volume(self._settings['musicVolume'])
        SETTINGS_WIDGETS['sfx_volume_slider'].set_volume(self._settings['sfxVolume'])
        SETTINGS_WIDGETS['display_mode_dropdown'].set_selected_word(self._settings['displayMode'])
        SETTINGS_WIDGETS['shader_carousel'].set_to_key(self._settings['shader'])
        SETTINGS_WIDGETS['particles_switch'].set_toggle_state(self._settings['particles'])
        self.set_display_mode(self._settings['displayMode'])
    
    def get_event(self, event):
        widget_event = self._widget_group.process_event(event)

        if widget_event is None:
            if event.type == pygame.MOUSEBUTTONDOWN and self._colour_picker:
                self.remove_colour_picker()
            return
            
        match widget_event.type:
            case SettingsEventType.VOLUME_SLIDER_SLIDE:
                return
            
            case SettingsEventType.VOLUME_SLIDER_CLICK:
                if widget_event.volume_type == 'music':
                    audio.set_music_volume(widget_event.volume)
                    self._settings['musicVolume'] = widget_event.volume
                elif widget_event.volume_type == 'sfx':
                    audio.set_sfx_volume(widget_event.volume)
                    self._settings['sfxVolume'] = widget_event.volume

            case SettingsEventType.DROPDOWN_CLICK:
                selected_word = SETTINGS_WIDGETS['display_mode_dropdown'].get_selected_word()
            
                if selected_word is None or selected_word == self._settings['displayMode']:
                    return
                
                self.set_display_mode(selected_word)

                self._settings['displayMode'] = selected_word

            case SettingsEventType.MENU_CLICK:
                self.next = 'menu'
                self.done = True
            
            case SettingsEventType.RESET_DEFAULT:
                self._settings = get_default_settings()
                self.reload_settings()
            
            case SettingsEventType.RESET_USER:
                self._settings = get_user_settings()
                self.reload_settings()
            
            case SettingsEventType.PRIMARY_COLOUR_BUTTON_CLICK | SettingsEventType.SECONDARY_COLOUR_BUTTON_CLICK:
                if self._colour_picker:
                    self.remove_colour_picker()

                relative_position = (event.pos[0] / screen.size[0], event.pos[1] / screen.size[1])
                self.create_colour_picker(relative_position, widget_event.type)
            
            case SettingsEventType.PRIMARY_COLOUR_PICKER_CLICK | SettingsEventType.SECONDARY_COLOUR_PICKER_CLICK:
                if widget_event.colour:
                    r, g, b = widget_event.colour.rgb
                    hex_colour = f'0x{hex(r)[2:].zfill(2)}{hex(g)[2:].zfill(2)}{hex(b)[2:].zfill(2)}'

                    if widget_event.type == SettingsEventType.PRIMARY_COLOUR_PICKER_CLICK:
                        SETTINGS_WIDGETS['primary_colour_button'].initialise_new_colours(widget_event.colour)
                        self._settings['primaryBoardColour'] = hex_colour
                    elif widget_event.type == SettingsEventType.SECONDARY_COLOUR_PICKER_CLICK:
                        SETTINGS_WIDGETS['secondary_colour_button'].initialise_new_colours(widget_event.colour)
                        self._settings['secondaryBoardColour'] = hex_colour
            
            case SettingsEventType.SHADER_CLICK:
                self._settings['shader'] = widget_event.data
            
            case SettingsEventType.PARTICLES_CLICK:
                self._settings['particles'] = widget_event.toggled
    
    def handle_resize(self):
        self._widget_group.handle_resize(screen.get_size())
    
    def draw(self):
        draw_background(screen, GRAPHICS['temp_background'])
        self._widget_group.draw()
    
    def update(self, **kwargs):
        self.draw()