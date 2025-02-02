import pygame

from data.states.game.mvc.game_model import GameModel
from data.states.game.mvc.game_view import GameView
from data.states.game.mvc.game_controller import GameController
from data.states.game.mvc.pause_view import PauseView
from data.states.game.mvc.win_view import WinView

from data.components.game_entry import GameEntry
from data.constants import ShaderType, BG_COLOUR
from data.control import _State
from data.database.database_helpers import insert_into_games

from functools import partial

from data.managers.window import window

class Game(_State):
    def __init__(self):
        super().__init__()
    
    def cleanup(self):
        print('cleaning game.py')
        window.clear_apply_arguments(ShaderType.BLOOM)

        game_entry = GameEntry(self.model.states, final_fen_string=self.model.get_fen_string())
        insert_into_games(game_entry.convert_to_row())

        return None
    
    def switch_to_menu(self):
        self.next = 'menu'
        self.done = True
    
    def startup(self, persist):
        window.set_apply_arguments(ShaderType.BASE, background_type=ShaderType._BACKGROUND_LASERS)
        window.set_apply_arguments(ShaderType.BLOOM, occlusion_colours=[(pygame.Color('0x95e0cc')).rgb, pygame.Color('0xf14e52').rgb], colour_intensity=0.8)
        binded_startup = partial(self.startup, persist)
        
        self.model = GameModel(persist)
        self.view = GameView(self.model)
        self.pause_view = PauseView(self.model)
        self.win_view = WinView(self.model)
        self.controller = GameController(self.model, self.view, self.win_view, self.pause_view, self.switch_to_menu, binded_startup)

        self.view.draw()
        print('starting game.py')
    
    def get_event(self, event):
        '''Handle gui events before board events because selected square gets cancelled in board events'''
        if event.type == pygame.VIDEORESIZE:
            self.view.handle_resize(resize_end=True)
        else:
            self.controller.handle_event(event)
    
    def handle_resize(self):
        self.view.handle_resize()
        self.win_view.handle_resize()
        self.pause_view.handle_resize()

    def draw(self):
        self.view.draw()
        self.win_view.draw()
        self.pause_view.draw()