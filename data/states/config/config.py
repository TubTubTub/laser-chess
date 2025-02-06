import pygame
from data.constants import ConfigEventType, Colour, ShaderType
from data.states.config.default_config import default_config
from data.states.config.widget_dict import CONFIG_WIDGETS
from data.managers.logs import initialise_logger
from data.managers.animation import animation
from data.assets import MUSIC, SFX
from data.managers.window import window
from data.managers.audio import audio
from data.managers.theme import theme
from data.control import _State
from random import randint

logger = initialise_logger(__name__)

class Config(_State):
    def __init__(self):
        super().__init__()
        
        self._config = None
        self._valid_fen = True
        self._selected_preset = None
    
    def cleanup(self):
        super().cleanup()
        
        window.clear_apply_arguments(ShaderType.BLOOM)

        return self._config
    
    def startup(self, persist=None):
        super().startup(CONFIG_WIDGETS, music=MUSIC[f'menu_{randint(1, 3)}'])
        window.set_apply_arguments(ShaderType.BLOOM, occlusion_colours=[(pygame.Color('0x95e0cc')).rgb, pygame.Color('0xf14e52').rgb], colour_intensity=0.9)

        CONFIG_WIDGETS['invalid_fen_string'].kill()
        CONFIG_WIDGETS['help'].kill()

        self._config = default_config

        if persist:
            self._config['FEN_STRING'] = persist
        
        self.set_fen_string(self._config['FEN_STRING'])
        self.toggle_pvc(self._config['CPU_ENABLED'])
        self.set_active_colour(self._config['COLOUR'])

        CONFIG_WIDGETS['cpu_depth_carousel'].set_to_key(self._config['CPU_DEPTH'])
        if self._config['CPU_ENABLED']:
            self.create_depth_picker()
        else:
            self.remove_depth_picker()

        print(self._config, 'stting',default_config)

        self.draw()
    
    def create_depth_picker(self):
        # CONFIG_WIDGETS['start_button'].update_relative_position((0.5, 0.8))
        # CONFIG_WIDGETS['start_button'].set_image()
        CONFIG_WIDGETS['cpu_depth_carousel'].set_surface_size(window.size)
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
        CONFIG_WIDGETS['fen_string_input'].set_text(new_fen_string)
        self._config['FEN_STRING'] = new_fen_string

        self.set_preset_overlay(new_fen_string)

        try:
            CONFIG_WIDGETS['board_thumbnail'].initialise_board(new_fen_string)
            CONFIG_WIDGETS['invalid_fen_string'].kill()

            if new_fen_string[-1].lower() == 'r':
                self.set_active_colour(Colour.RED)
            else:
                self.set_active_colour(Colour.BLUE)
            
            self._valid_fen = True
        except:
            CONFIG_WIDGETS['board_thumbnail'].initialise_board('')
            self._widget_group.add(CONFIG_WIDGETS['invalid_fen_string'])

            window.set_effect(ShaderType.SHAKE)
            animation.set_timer(500, lambda: window.clear_effect(ShaderType.SHAKE))

            audio.play_sfx(SFX['error_1'])
            audio.play_sfx(SFX['error_2'])
            
            self._valid_fen = False
    
    def get_event(self, event):
        widget_event = self._widget_group.process_event(event)

        if event.type in [pygame.MOUSEBUTTONUP, pygame.KEYDOWN]:
            CONFIG_WIDGETS['help'].kill()

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
                self.next = 'editor'
                self.done = True
            
            case ConfigEventType.COLOUR_CLICK:
                self.set_active_colour(widget_event.data.get_flipped_colour())
            
            case ConfigEventType.HELP_CLICK:
                self._widget_group.add(CONFIG_WIDGETS['help'])
                self._widget_group.handle_resize(window.size)
    
    def set_preset_overlay(self, fen_string):
        fen_string_widget_map = {
            'sc3ncfcncpb2/2pc7/3Pd6/pa1Pc1rbra1pb1Pd/pb1Pd1RaRb1pa1Pc/6pb3/7Pa2/2PdNaFaNa3Sa b': 'preset_1',
            'sc3ncfcncra2/10/3Pd2pa3/paPc2Pbra2pbPd/pbPd2Rapd2paPc/3Pc2pb3/10/2RaNaFaNa3Sa b': 'preset_2',
            'sc3pcncpb3/5fc4/pa3pcncra3/pb1rd1Pd1Pb3/3pd1pb1Rd1Pd/3RaNaPa3Pc/4Fa5/3PdNaPa3Sa b': 'preset_3'
        }

        if fen_string in fen_string_widget_map:
            self._selected_preset = CONFIG_WIDGETS[fen_string_widget_map[fen_string]]
        else:
            self._selected_preset = None
    
    def set_active_colour(self, colour):
        if self._config['COLOUR'] != colour:
            CONFIG_WIDGETS['to_move_button'].set_next_icon()

        self._config['COLOUR'] = colour
        
        if colour == Colour.BLUE:
            CONFIG_WIDGETS['to_move_text'].set_text('BLUE TO MOVE')
        elif colour == Colour.RED:
            CONFIG_WIDGETS['to_move_text'].set_text('RED TO MOVE')
        
        if self._valid_fen:
            self._config['FEN_STRING'] = self._config['FEN_STRING'][:-1] + colour.name[0].lower()
            CONFIG_WIDGETS['fen_string_input'].set_text(self._config['FEN_STRING'])
    
    def draw(self):
        self._widget_group.draw()

        if self._selected_preset:
            pygame.draw.rect(window.screen, theme['borderPrimary'], (*self._selected_preset.position, *self._selected_preset.size), width=int(theme['borderWidth']))
    
    def update(self, **kwargs):
        self._widget_group.update()
        super().update(**kwargs)