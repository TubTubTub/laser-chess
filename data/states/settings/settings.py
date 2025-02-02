import pygame
from data.utils.data_helpers import get_default_settings, get_user_settings, update_user_settings
from data.constants import SettingsEventType, WidgetState, ShaderType, SHADER_MAP
from data.states.settings.widget_dict import SETTINGS_WIDGETS
from data.components.widget_group import WidgetGroup
from data.managers.window import window
from data.managers.audio import audio
from data.widgets import ColourPicker
from data.assets import MUSIC_PATHS
from data.control import _State

class Settings(_State):
    def __init__(self):
        super().__init__()

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
        window.set_apply_arguments(ShaderType.BASE, background_type=ShaderType._BACKGROUND_BALATRO)
        self._widget_group = WidgetGroup(SETTINGS_WIDGETS)
        self._widget_group.handle_resize(window.size)
        self._settings = get_user_settings()
        self.reload_settings()

        # print('\nGETTING USER SETTINGS:')
        # pprint.pprint(self._settings)
        # print('')

        audio.play_music(MUSIC_PATHS['menu'])

        self.draw()
    
    def create_colour_picker(self, mouse_pos, button_type):
        if button_type == SettingsEventType.PRIMARY_COLOUR_BUTTON_CLICK:
            selected_colour = self._settings['primaryBoardColour']
            event_type = SettingsEventType.PRIMARY_COLOUR_PICKER_CLICK
        else:
            selected_colour = self._settings['secondaryBoardColour']
            event_type = SettingsEventType.SECONDARY_COLOUR_PICKER_CLICK

        self._colour_picker = ColourPicker(
            relative_position=(mouse_pos[0] / window.size[0], mouse_pos[1] / window.size[1]),
            relative_width=0.15,
            selected_colour=selected_colour,
            event_type=event_type
        )
        self._widget_group.add(self._colour_picker)
    
    def remove_colour_picker(self):
        self._colour_picker.kill()
    
    def reload_display_mode(self):
        if self._settings['displayMode'] == 'fullscreen':
            window.set_fullscreen(desktop=True)

        elif self._settings['displayMode'] == 'windowed':
            window.set_windowed()
            window.restore()
        
        self._widget_group.handle_resize(window.size)
    
    def reload_shaders(self):
        window.clear_all_effects()

        for shader_type in SHADER_MAP[self._settings['shader']]:
            window.set_effect(shader_type)
    
    def reload_settings(self):
        SETTINGS_WIDGETS['primary_colour_button'].initialise_new_colours(self._settings['primaryBoardColour'])
        SETTINGS_WIDGETS['secondary_colour_button'].initialise_new_colours(self._settings['secondaryBoardColour'])
        SETTINGS_WIDGETS['primary_colour_button'].set_state_colour(WidgetState.BASE)
        SETTINGS_WIDGETS['secondary_colour_button'].set_state_colour(WidgetState.BASE)
        SETTINGS_WIDGETS['music_volume_slider'].set_volume(self._settings['musicVolume'])
        SETTINGS_WIDGETS['sfx_volume_slider'].set_volume(self._settings['sfxVolume'])
        SETTINGS_WIDGETS['display_mode_dropdown'].set_selected_word(self._settings['displayMode'])
        SETTINGS_WIDGETS['shader_carousel'].set_to_key(self._settings['shader'])
        SETTINGS_WIDGETS['particles_switch'].set_toggle_state(self._settings['particles'])
        SETTINGS_WIDGETS['opengl_switch'].set_toggle_state(self._settings['opengl'])

        self.reload_shaders()
        self.reload_display_mode()
    
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
                
                self._settings['displayMode'] = selected_word
                
                self.reload_display_mode()

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

                self.create_colour_picker(event.pos, widget_event.type)
            
            case SettingsEventType.PRIMARY_COLOUR_PICKER_CLICK | SettingsEventType.SECONDARY_COLOUR_PICKER_CLICK:
                if widget_event.colour:
                    r, g, b = widget_event.colour.rgb
                    hex_colour = f'0x{hex(r)[2:].zfill(2)}{hex(g)[2:].zfill(2)}{hex(b)[2:].zfill(2)}'

                    if widget_event.type == SettingsEventType.PRIMARY_COLOUR_PICKER_CLICK:
                        SETTINGS_WIDGETS['primary_colour_button'].initialise_new_colours(widget_event.colour)
                        SETTINGS_WIDGETS['primary_colour_button'].set_state_colour(WidgetState.BASE)
                        self._settings['primaryBoardColour'] = hex_colour
                    elif widget_event.type == SettingsEventType.SECONDARY_COLOUR_PICKER_CLICK:
                        SETTINGS_WIDGETS['secondary_colour_button'].initialise_new_colours(widget_event.colour)
                        SETTINGS_WIDGETS['secondary_colour_button'].set_state_colour(WidgetState.BASE)
                        self._settings['secondaryBoardColour'] = hex_colour
            
            case SettingsEventType.SHADER_PICKER_CLICK:
                self._settings['shader'] = widget_event.data
                self.reload_shaders()

            case SettingsEventType.OPENGL_CLICK:
                self._settings['opengl'] = widget_event.toggled
                self.reload_shaders()
            
            case SettingsEventType.PARTICLES_CLICK:
                self._settings['particles'] = widget_event.toggled
    
    def draw(self):
        self._widget_group.draw()