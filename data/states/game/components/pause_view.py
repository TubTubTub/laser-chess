import pygame
from data.constants import GameEventType, PAUSE_COLOUR
from data.components.widget_group import WidgetGroup
from data.components.widget_dict import WIDGET_DICT
from data.components.custom_event import CustomEvent
from data.components.cursor import Cursor

class PauseView:
    def __init__(self, model):
        self._model = model
        self._screen = pygame.display.get_surface()
        self._cursor = Cursor()

        self._model.register_listener(self.process_model_event, 'pause')

        self._event_to_func_map = {
            GameEventType.PAUSE_CLICK: self.handle_pause_click
        }

        self._widget_group = WidgetGroup(WIDGET_DICT['pause'])

        self.states = {
            'PAUSED': False
        }

        self._screen_overlay = pygame.Surface(self._screen.get_size(), pygame.SRCALPHA)
        self._screen_overlay.fill(PAUSE_COLOUR)

    def handle_pause_click(self, event):
        self.states['PAUSED'] = not self.states['PAUSED']
    
    def handle_resize(self):
        self._widget_group.handle_resize(self._screen.get_size())
    
    def draw(self):
        if self.states['PAUSED']:
            self._screen.blit(self._screen_overlay, (0, 0))
            self._widget_group.draw(self._screen)
    
    def process_model_event(self, event):
        try:
            self._event_to_func_map.get(event.type)(event)
        except:
            raise KeyError('Event type not recognized in Paused View (PauseView.process_model_event)', event)
    
    def convert_mouse_pos(self, mouse_pos):
        if collided := self._cursor.get_sprite_collision(mouse_pos, self._widget_group):
            return collided.event

        return CustomEvent.create_event(GameEventType.EMPTY_CLICK)