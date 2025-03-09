import pygame
from data.states.game.widget_dict import PAUSE_WIDGETS
from data.components.widget_group import WidgetGroup
from data.utils.event_types import GameEventType
from data.utils.constants import PAUSE_COLOUR
from data.managers.window import window
from data.managers.audio import audio

class PauseView:
    def __init__(self, model):
        self._model = model

        self._screen_overlay = pygame.Surface(window.size, pygame.SRCALPHA)
        self._screen_overlay.fill(PAUSE_COLOUR)

        self._widget_group = WidgetGroup(PAUSE_WIDGETS)
        self._widget_group.handle_resize(window.size)

        self._model.register_listener(self.process_model_event, 'pause')

        self._event_to_func_map = {
            GameEventType.PAUSE_CLICK: self.handle_pause_click
        }

        self.states = {
            'PAUSED': False
        }

    def handle_pause_click(self, event):
        self.states['PAUSED'] = not self.states['PAUSED']

        if self.states['PAUSED']:
            audio.pause_sfx()
        else:
            audio.unpause_sfx()

    def handle_resize(self):
        self._screen_overlay = pygame.Surface(window.size, pygame.SRCALPHA)
        self._screen_overlay.fill(PAUSE_COLOUR)
        self._widget_group.handle_resize(window.size)

    def draw(self):
        if self.states['PAUSED']:
            window.screen.blit(self._screen_overlay, (0, 0))
            self._widget_group.draw()

    def process_model_event(self, event):
        try:
            self._event_to_func_map.get(event.type)(event)
        except:
            raise KeyError('Event type not recognized in Paused View (PauseView.process_model_event)', event)

    def convert_mouse_pos(self, event):
        return self._widget_group.process_event(event)