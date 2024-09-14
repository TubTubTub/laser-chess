import pygame
from data.constants import EventType, BG_COLOUR
from data.components.piecegroup import PieceGroup
from data.utils.settings_helpers import get_settings_json

class GameView:
    def __init__(self, model, fen_string=""):
        self.model = model
        self._screen = pygame.display.get_surface()
        self._app_settings = get_settings_json()
        self._overlay_index = None
        self.event_to_func_map = {
            EventType.BOARD_CLICK: self.handle_board_click,
            EventType.PIECE_CLICK: self.handle_piece_click,
            EventType.WIDGET_CLICK: self.handle_widget_click,
        }

        self.model.register_listener(self.process_model_event)
        
        self._board_size = self.calculate_board_size()
        self._board_position = self.calculate_board_position()
        self._board_surface = self.create_board()

        self._piece_group = PieceGroup(self.model.get_piece_list())
    
    def handle_resize(self):
        self._board_size = self.calculate_board_size()
        self._board_position = self.calculate_board_position()
        self._board_surface = pygame.transform.scale(self._board_surface, self._board_size)

    def handle_board_click(self, event):
        raise NotImplementedError
    
    def handle_piece_click(self, event):
        raise NotImplementedError
    
    def handle_widget_click(self, event):
        raise NotImplementedError
    
    def draw_widgets(self):
        raise NotImplementedError

    def draw_board(self):
        self._screen.blit(self._board_surface, self._board_position)

    def draw_pieces(self):
        self._piece_group.draw(self._screen)

    def draw_overlay(self):
        if self._overlay_index is None:
            return
        
        raise NotImplementedError
    
    def draw(self):
        print('drawing')
        self._screen.fill(BG_COLOUR)
        self.draw_board()

    def process_model_event(self, event):
        try:
            self.event_to_func_map[event.type](event)
        except:
            raise KeyError('Event type not recognized in Game View (GameView.process_model_event):', event.type)
    
    
    def create_board(self):
        square_size = self._board_size[0] / 10
        board_surface = pygame.Surface(self._board_size)

        for i in range(80):
            x = i % 10
            y = i // 10

            if (x + y) % 2 == 0:
                square_colour = self._app_settings['primaryBoardColour']
            else:
                square_colour = self._app_settings['secondaryBoardColour']
            
            square_x = x * square_size
            square_y = y * square_size

            pygame.draw.rect(board_surface, square_colour, (square_x, square_y, square_size, square_size))
        
        return board_surface

    def calculate_board_size(self):
        '''Returns board size based on screen parameter'''
        screen_width, screen_height = self._screen.get_size()

        target_height = screen_height * 0.64
        target_width = target_height / 0.8

        return (target_width, target_height)

    def calculate_board_position(self):
        '''Returns required board starting position to draw on center of the screen'''
        screen_x, screen_y = self._screen.get_size()
        board_x, board_y = self._board_size

        x = screen_x / 2 - (board_x / 2)
        y = screen_y / 2 - (board_y / 2)

        return (x, y)