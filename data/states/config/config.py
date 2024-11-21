import pygame

from data.tools import _State

from data.states.config.widget_dict import CONFIG_WIDGETS
from data.states.config.default_config import default_config

from data.components.widget_group import WidgetGroup
from data.components.cursor import Cursor
from data.components.audio import audio
from data.components.animation import animation

from data.widgets import Carousel, Text

from data.utils.asset_helpers import draw_background

from data.assets import MUSIC_PATHS

from data.constants import ConfigEventType

class Config(_State):
    def __init__(self):
        super().__init__()
        self._screen = pygame.display.get_surface()
        self._cursor = Cursor()
        self._config = None
        
        self._widget_group = None
    
    def cleanup(self):
        print('cleaning config.py')

        return self._config
    
    def startup(self, persist=None):
        print('starting config.py')
        self._widget_group = WidgetGroup(CONFIG_WIDGETS)
        self._widget_group.handle_resize(self._screen.size)

        self._config = default_config

        CONFIG_WIDGETS['invalid_fen_string'].kill()
        
        try:
            CONFIG_WIDGETS['board_thumbnail'].initialise_fen_string(self._config['FEN_STRING'])
        except:
            CONFIG_WIDGETS['board_thumbnail'].initialise_fen_string([])
            self._widget_group.add(CONFIG_WIDGETS['invalid_fen_string'])
        
        self._cpu_depth_carousel = Carousel(
            relative_position=(0.5, 0.68),
            margin=95,
            event_type=ConfigEventType.CPU_DEPTH_CLICK,
            fill_colour=(0, 0, 0, 0),
            widgets_dict={
                1: Text(
                    relative_position=(0, 0),
                    text="EASY",
                    text_colour=(255, 255, 255),
                    font_size=70,
                    margin=0,
                    fill_colour=(0, 0, 0, 0)
                ),
                2: Text(
                    relative_position=(0, 0),
                    text="MEDIUM",
                    text_colour=(255, 255, 255),
                    font_size=70,
                    margin=0,
                    fill_colour=(0, 0, 0, 0)
                ),
                3: Text(
                    relative_position=(0, 0),
                    text="HARD",
                    text_colour=(255, 255, 255),
                    font_size=70,
                    margin=0,
                    fill_colour=(0, 0, 0, 0)
                ),
            }
        )

        if self._config['CPU_ENABLED']:
            self.create_depth_picker()

        self.draw()

        audio.play_music(MUSIC_PATHS['cpu_hard'])
    
    def create_depth_picker(self):
        CONFIG_WIDGETS['start_button'].update_relative_position((0.5, 0.8))
        CONFIG_WIDGETS['start_button'].set_image()

        self._widget_group.add(self._cpu_depth_carousel)
    
    def remove_depth_picker(self):
        CONFIG_WIDGETS['start_button'].update_relative_position((0.5, 0.7))
        CONFIG_WIDGETS['start_button'].set_image()
        
        self._cpu_depth_carousel.kill()
    
    def get_event(self, event):
        widget_event = self._widget_group.process_event(event)

        if event.type == pygame.VIDEORESIZE:
            self.handle_resize(resize_end=True)
            return

        if widget_event is None:
            return

        match widget_event.type:
            case ConfigEventType.GAME_CLICK:
                self.next = 'game'
                self.done = True

            case ConfigEventType.MENU_CLICK:
                self.next = 'menu'
                self.done = True

            case ConfigEventType.TIME_CLICK:
                print('timer click', widget_event.data)
                self._config['TIME_ENABLED'] = widget_event.data

            case ConfigEventType.PVP_CLICK:
                pvp_enabled = widget_event.data
                
                if not(pvp_enabled) == self._config['CPU_ENABLED']:
                    return

                CONFIG_WIDGETS['pvp_button'].set_locked(True)
                CONFIG_WIDGETS['pvc_button'].set_locked(False)
                CONFIG_WIDGETS['pvc_button'].set_next_icon()

                self._config['CPU_ENABLED'] = not(pvp_enabled)
                
                if self._config['CPU_ENABLED']:
                    self.create_depth_picker()
                else:
                    self.remove_depth_picker()

            case ConfigEventType.PVC_CLICK:
                pvc_enabled = widget_event.data

                if pvc_enabled == self._config['CPU_ENABLED']:
                    return

                CONFIG_WIDGETS['pvc_button'].set_locked(True)
                CONFIG_WIDGETS['pvp_button'].set_locked(False)
                CONFIG_WIDGETS['pvp_button'].set_next_icon()

                self._config['CPU_ENABLED'] = pvc_enabled
                
                if self._config['CPU_ENABLED']:
                    self.create_depth_picker()
                else:
                    self.remove_depth_picker()

            case ConfigEventType.FEN_STRING_TYPE:
                print(widget_event.text, 'fen string type')
                self._config['FEN_STRING'] = widget_event.text
                try:
                    CONFIG_WIDGETS['board_thumbnail'].initialise_fen_string(self._config['FEN_STRING'])
                    CONFIG_WIDGETS['invalid_fen_string'].kill()
                except:
                    CONFIG_WIDGETS['board_thumbnail'].initialise_fen_string([])
                    self._widget_group.add(CONFIG_WIDGETS['invalid_fen_string'])

            case ConfigEventType.TIME_TYPE:
                self._config['TIME'] = float(widget_event.text)

            case ConfigEventType.CPU_DEPTH_CLICK:
                print(widget_event.data)
                self._config['CPU_DEPTH'] = int(widget_event.data)
    
    def handle_resize(self, resize_end=False):
        self._widget_group.handle_resize(self._screen.get_size())
    
    def draw(self):
        temp_background = pygame.Surface((1, 1))
        temp_background.fill((10, 10, 10))
        animation.draw_image(self._screen, temp_background, position=(0, 0), size=self._screen.size)

        self._widget_group.draw(self._screen)
    
    def update(self, **kwargs):
        self._widget_group.update()
        self.draw()