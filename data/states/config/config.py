import pygame

from data.control import _State

from data.states.config.widget_dict import CONFIG_WIDGETS
from data.states.config.default_config import default_config

from data.components.widget_group import WidgetGroup
from data.components.cursor import Cursor
from data.components.audio import audio
from data.components.animation import animation
from data.theme import theme

from data.assets import MUSIC_PATHS, GRAPHICS

from data.constants import ConfigEventType, Colour

from data.utils.asset_helpers import draw_background

class Config(_State):
    def __init__(self):
        super().__init__()
        self._screen = pygame.display.get_surface()
        self._cursor = Cursor()
        self._config = None
        self._valid_fen = True
        self._selected_preset = None
        
        self._widget_group = None
    
    def cleanup(self):
        print('cleaning config.py')

        return self._config
    
    def startup(self, persist=None):
        print('starting config.py')
        self._widget_group = WidgetGroup(CONFIG_WIDGETS)
        self._widget_group.handle_resize(self._screen.size)
        CONFIG_WIDGETS['invalid_fen_string'].kill()

        self._config = default_config

        if persist:
            self._config['FEN_STRING'] = persist
        
        self.set_fen_string(self._config['FEN_STRING'])
        self.toggle_pvc(self._config['CPU_ENABLED'])

        CONFIG_WIDGETS['cpu_depth_carousel'].set_to_key(2)
        if self._config['CPU_ENABLED']:
            self.create_depth_picker()
        else:
            self.remove_depth_picker()

        self.draw()

        audio.play_music(MUSIC_PATHS['cpu_hard'])
    
    def create_depth_picker(self):
        # CONFIG_WIDGETS['start_button'].update_relative_position((0.5, 0.8))
        # CONFIG_WIDGETS['start_button'].set_image()
        CONFIG_WIDGETS['cpu_depth_carousel'].set_surface_size(self._screen.get_size())
        CONFIG_WIDGETS['cpu_depth_carousel'].set_image()
        CONFIG_WIDGETS['cpu_depth_carousel'].set_geometry()
        self._widget_group.add(CONFIG_WIDGETS['cpu_depth_carousel'])
    
    def remove_depth_picker(self):
        # CONFIG_WIDGETS['start_button'].update_relative_position((0.5, 0.7))
        # CONFIG_WIDGETS['start_button'].set_image()
        
        CONFIG_WIDGETS['cpu_depth_carousel'].kill()
    
    def toggle_pvc(self, pvc_enabled):
        if pvc_enabled:
            CONFIG_WIDGETS['pvc_button'].set_locked(True)
            CONFIG_WIDGETS['pvp_button'].set_locked(False)
        else:
            CONFIG_WIDGETS['pvp_button'].set_locked(True)
            CONFIG_WIDGETS['pvc_button'].set_locked(False)
        
        self._config['CPU_ENABLED'] = pvc_enabled
        
        if self._config['CPU_ENABLED']:
            self.create_depth_picker()
        else:
            self.remove_depth_picker()
    
    def set_fen_string(self, new_fen_string):
        CONFIG_WIDGETS['fen_string_input'].update_text(new_fen_string)
        self._config['FEN_STRING'] = new_fen_string

        self.set_preset_overlay(new_fen_string)

        try:
            CONFIG_WIDGETS['board_thumbnail'].initialise_board(new_fen_string)
            CONFIG_WIDGETS['invalid_fen_string'].kill()

            if new_fen_string[-1].lower() == 'r':
                self._config['COLOUR'] = Colour.RED
            else:
                self._config['COLOUR'] = Colour.BLUE
            
            self._valid_fen = True
        except:
            CONFIG_WIDGETS['board_thumbnail'].initialise_board('')
            self._widget_group.add(CONFIG_WIDGETS['invalid_fen_string'])
            
            self._valid_fen = False
    
    def get_event(self, event):
        widget_event = self._widget_group.process_event(event)

        if widget_event is None:
            return

        match widget_event.type:
            case ConfigEventType.GAME_CLICK:
                if self._valid_fen:
                    self.next = 'game'
                    self.done = True

            case ConfigEventType.MENU_CLICK:
                self.next = 'menu'
                self.done = True

            case ConfigEventType.TIME_CLICK:
                self._config['TIME_ENABLED'] = not(widget_event.data)
                CONFIG_WIDGETS['timer_button'].set_next_icon()

            case ConfigEventType.PVP_CLICK:
                self.toggle_pvc(False)

            case ConfigEventType.PVC_CLICK:
                self.toggle_pvc(True)

            case ConfigEventType.FEN_STRING_TYPE:
                self.set_fen_string(widget_event.text)

            case ConfigEventType.TIME_TYPE:
                if widget_event.text == '':
                    self._config['TIME'] = 5
                else:
                    self._config['TIME'] = float(widget_event.text)

            case ConfigEventType.CPU_DEPTH_CLICK:
                self._config['CPU_DEPTH'] = int(widget_event.data)
            
            case ConfigEventType.PRESET_CLICK:
                self.set_fen_string(widget_event.fen_string)
            
            case ConfigEventType.SETUP_CLICK:
                self.next = 'setup'
                self.done = True
    
    def set_preset_overlay(self, fen_string):
        fen_string_widget_map = {
            'sc3ncfancpb2/2pc7/3Pd6/pa1Pc1rbra1pb1Pd/pb1Pd1RaRb1pa1Pc/6pb3/7Pa2/2PdNaFaNa3Sa b': 'preset_1',
            'sc3ncfcncra2/10/3Pd2pa3/paPc2Pbra2pbPd/pbPd2Rapd2paPc/3Pc2pb3/10/2RaNaFaNa3Sa b': 'preset_2',
            'sc3pcncpb3/5fc4/pa3pcncra3/pb1rd1Pd1Pb3/3pd1pb1Rd1Pd/3RaNaPa3Pc/4Fa5/3PdNaPa3Sa b': 'preset_3'
        }

        if fen_string in fen_string_widget_map:
            self._selected_preset = CONFIG_WIDGETS[fen_string_widget_map[fen_string]]
        else:
            self._selected_preset = None
    
    def handle_resize(self):
        self._widget_group.handle_resize(self._screen.get_size())
    
    def draw(self):
        draw_background(self._screen, GRAPHICS['temp_background'])
        self._widget_group.draw()

        if self._selected_preset:
            pygame.draw.rect(self._screen, theme['borderPrimary'], (*self._selected_preset.position, *self._selected_preset.size), width=int(theme['borderWidth']))
    
    def update(self, **kwargs):
        self._widget_group.update()
        self.draw()