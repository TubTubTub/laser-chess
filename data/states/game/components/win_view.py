import pygame
from data.constants import GameEventType
from data.components.widget_group import WidgetGroup
from data.states.game.widget_dict import WIN_WIDGETS
from data.components.cursor import Cursor
from data.components.custom_event import CustomEvent

class WinView:
    def __init__(self, model):
        self._model = model
        self._screen = pygame.display.get_surface()
        self._cursor = Cursor()

        # self._model.register_listener(self.process_model_event, 'win')

        self._widget_group = WidgetGroup(WIN_WIDGETS)
    
    def handle_resize(self):
        self._widget_group.handle_resize(self._screen.get_size())
    
    def draw(self):
        if self._model.states['WINNER'] is not None:
            self._widget_group.draw(self._screen)
    
    # def process_model_event(self, event):
    #     try:
    #         self._event_to_func_map.get(event.type)(event)
    #     except:
    #         raise KeyError('Event type not recognized in Win View (WinView.process_model_event)', event)
    
    def convert_mouse_pos(self, event):
        return self._widget_group.process_event(event)