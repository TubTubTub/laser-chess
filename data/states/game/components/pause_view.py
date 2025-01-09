import pygame
from data.components.widget_group import WidgetGroup
from data.components.cursor import Cursor
from data.constants import GameEventType, PAUSE_COLOUR
from data.states.game.widget_dict import PAUSE_WIDGETS
from data.screen import screen

class PauseView:
    def __init__(self, model):
        self._model = model
        self._cursor = Cursor()

        self._model.register_listener(self.process_model_event, 'pause')

        self._event_to_func_map = {
            GameEventType.PAUSE_CLICK: self.handle_pause_click
        }

        self._widget_group = WidgetGroup(PAUSE_WIDGETS)

        self.states = {
            'PAUSED': False
        }

        self._screen_overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        self._screen_overlay.fill(PAUSE_COLOUR)

    def handle_pause_click(self, event):
        self.states['PAUSED'] = not self.states['PAUSED']
    
    def handle_resize(self):
        self._widget_group.handle_resize(screen.get_size())
        self._screen_overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        self._screen_overlay.fill(PAUSE_COLOUR)
    
    def draw(self):
        if self.states['PAUSED']:
            screen.blit(self._screen_overlay, (0, 0))
            self._widget_group.draw()
    
    def process_model_event(self, event):
        try:
            self._event_to_func_map.get(event.type)(event)
        except:
            raise KeyError('Event type not recognized in Paused View (PauseView.process_model_event)', event)
    
    def convert_mouse_pos(self, event):
        return self._widget_group.process_event(event)