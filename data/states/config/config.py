import pygame

from data.tools import _State

from data.states.config.widget_dict import CONFIG_WIDGETS
from data.states.config.default_config import default_config

from data.components.widget_group import WidgetGroup
from data.components.cursor import Cursor
from data.components.audio import audio
from data.components.animation import animation

from data.utils.asset_helpers import draw_background

from data.assets import MUSIC_PATHS

from data.constants import ConfigEventType, Colour

class Config(_State):
    def __init__(self):
        super().__init__()
        self._screen = pygame.display.get_surface()
        self._cursor = Cursor()
        self._config = None
        
        self._widget_group = None
    
    def cleanup(self):
        print('cleaning config.py')

        return {
            # 'cpu_depth': 2,
        }
    
    def startup(self, persist=None):
        print('starting config.py')
        self._config = default_config

        self._widget_group = WidgetGroup(CONFIG_WIDGETS)
        self._widget_group.handle_resize(self._screen.size)

        # CONFIG_WIDGETS['timer_text_input'].set_text(self._config['TIME'])
        # if self._config['TIME_ENABLED']:
        #     CONFIG_WIDGETS['timer_button'].set_mode('TIME_ENABLED')
        # else:
        #     CONFIG_WIDGETS['timer_button'].set_mode('TIME_DISABLED')

        self.draw()

        audio.play_music(MUSIC_PATHS['cpu_hard'])
    
    def get_event(self, event):
        widget_event = self._widget_group.process_event(event)

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
                print('timer click')

            case ConfigEventType.PVP_CLICK:
                pvp_enabled = widget_event.data
                
                if not(pvp_enabled) == self._config['CPU_ENABLED']:
                    return

                CONFIG_WIDGETS['pvp_button'].set_locked(True)
                CONFIG_WIDGETS['pvc_button'].set_locked(False)
                CONFIG_WIDGETS['pvc_button'].set_next_icon()

                self._config['CPU_ENABLED'] = not(pvp_enabled)

                print('CPU ENABLED:', self._config['CPU_ENABLED'])

            case ConfigEventType.PVC_CLICK:
                pvc_enabled = widget_event.data

                if pvc_enabled == self._config['CPU_ENABLED']:
                    return
                CONFIG_WIDGETS['pvc_button'].set_locked(True)
                CONFIG_WIDGETS['pvp_button'].set_locked(False)
                CONFIG_WIDGETS['pvp_button'].set_next_icon()

                self._config['CPU_ENABLED'] = pvc_enabled
                
                print('CPU ENABLED:', self._config['CPU_ENABLED'])

            case ConfigEventType.FEN_STRING_TYPE:
                print(widget_event.text, 'fen string type')

            case ConfigEventType.TIME_TYPE:
                print(widget_event.text, 'time type')

            case ConfigEventType.CPU_DEPTH_CLICK:
                print(widget_event.data)
    
    def handle_resize(self):
        self._widget_group.handle_resize(self._screen.get_size())
    
    def draw(self):
        temp_background = pygame.Surface((1, 1))
        temp_background.fill((10, 10, 10))
        animation.draw_image(self._screen, temp_background, position=(0, 0), size=self._screen.size)
        self._widget_group.draw(self._screen)
    
    def update(self, **kwargs):
        self._widget_group.update()
        self.draw()