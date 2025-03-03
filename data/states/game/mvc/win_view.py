from data.constants import Colour, Miscellaneous, CursorMode
from data.components.widget_group import WidgetGroup
from data.states.game.widget_dict import WIN_WIDGETS
from data.managers.window import window
from data.managers.cursor import cursor

class WinView:
    def __init__(self, model):
        self._model = model

        self._widget_group = WidgetGroup(WIN_WIDGETS)
        self._widget_group.handle_resize(window.size)
    
    def handle_resize(self):
        self._widget_group.handle_resize(window.size)
    
    def draw(self):
        if self._model.states['WINNER'] is not None:
            if cursor.get_mode() != CursorMode.ARROW:
                cursor.set_mode(CursorMode.ARROW)

            if self._model.states['WINNER'] == Colour.BLUE:
                WIN_WIDGETS['red_won'].kill()
                WIN_WIDGETS['draw_won'].kill()
            elif self._model.states['WINNER'] == Colour.RED:
                WIN_WIDGETS['blue_won'].kill()
                WIN_WIDGETS['draw_won'].kill()
            elif self._model.states['WINNER'] == Miscellaneous.DRAW:
                WIN_WIDGETS['red_won'].kill()
                WIN_WIDGETS['blue_won'].kill()
        
            self._widget_group.draw()
    
    def set_win_type(self, win_type):
        WIN_WIDGETS['by_draw'].kill()
        WIN_WIDGETS['by_timeout'].kill()
        WIN_WIDGETS['by_resignation'].kill()
        WIN_WIDGETS['by_checkmate'].kill()

        match win_type:
            case 'CAPTURE':
                self._widget_group.add(WIN_WIDGETS['by_checkmate'])
            case 'DRAW':
                self._widget_group.add(WIN_WIDGETS['by_draw'])
            case 'RESIGN':
                self._widget_group.add(WIN_WIDGETS['by_resignation'])
            case 'TIME':
                self._widget_group.add(WIN_WIDGETS['by_timeout'])
    
    def convert_mouse_pos(self, event):
        return self._widget_group.process_event(event)