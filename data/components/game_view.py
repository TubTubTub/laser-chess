import pygame
from data.constants import EventType, BG_COLOUR, OVERLAY_COLOUR
from data.components.piece_group import PieceGroup
from data.components.widget_group import WidgetGroup
from data.components.game_event import GameEvent
from data.utils.settings_helpers import get_settings_json
from data.utils.board_helpers import coords_to_screen_pos
from data.utils.view_helpers import create_board, create_circle_overlay, create_square_overlay

class GameView:
    def __init__(self, model):
        self.model = model
        self._screen = pygame.display.get_surface()
        self._app_settings = get_settings_json()
        self.event_to_func_map = {
            EventType.UPDATE_PIECES: self.handle_update_pieces,
            EventType.REMOVE_PIECE: self.handle_remove_piece
        }

        self.model.register_listener(self.process_model_event)
        
        self._board_size = self.calculate_board_size()
        self._board_position = self.calculate_board_position()
        self._board_surface = create_board(self._board_size, self._app_settings['primaryBoardColour'], self._app_settings['secondaryBoardColour'])
        self._board_unscaled = self._board_surface.copy() # surface glitches if scaling in place

        self._piece_group = PieceGroup()
        self.handle_update_pieces()

        self._widget_group = WidgetGroup()
        self._widget_group.initialise_widgets(self._screen.get_size())
        
        self._valid_overlay_coords = []
        self._selected_overlay_coord = None

        square_size = self._board_size[0] / 10
        self._circle_overlay = create_circle_overlay(square_size, OVERLAY_COLOUR)
        self._square_overlay = create_square_overlay(square_size, OVERLAY_COLOUR)
        self._circle_overlay_unscaled = self._circle_overlay.copy()
        self._square_overlay_unscaled = self._square_overlay.copy()
    
    def handle_resize(self, resize_end=False):
        self._board_size = self.calculate_board_size()
        self._board_position = self.calculate_board_position()
        self._board_surface = pygame.transform.scale(self._board_unscaled, self._board_size)

        self._piece_group.handle_resize(self._board_position, self._board_size, resize_end)
        self._widget_group.handle_resize(self._screen.get_size())

        square_size = self._board_size[0] / 10
        self._circle_overlay = pygame.transform.scale(self._circle_overlay_unscaled, (square_size, square_size))
        self._square_overlay = pygame.transform.scale(self._square_overlay_unscaled, (square_size, square_size))
    
    def handle_update_pieces(self, event=None):
        piece_list = self.model.get_piece_list()
        self._piece_group.initialise_pieces(piece_list, self._board_position, self._board_size)
    
    def handle_remove_piece(self, event):
        self._piece_group.remove_piece(event.coords_to_remove)
    
    def handle_widget_click(self, event):
        raise NotImplementedError

    def draw_board(self):
        self._screen.blit(self._board_surface, self._board_position)

    def draw_pieces(self):
        self._piece_group.draw(self._screen)
    
    def draw_widgets(self):
        self._widget_group.draw(self._screen)

    def draw_overlay(self):
        if not self._selected_overlay_coord:
            return
        
        square_size = self._board_size[0] / 10
        
        square_x, square_y = coords_to_screen_pos(self._selected_overlay_coord, self._board_position, square_size)
        self._screen.blit(self._square_overlay, (square_x, square_y))

        for coords in self._valid_overlay_coords:
            square_x, square_y = coords_to_screen_pos(coords, self._board_position, square_size)
            self._screen.blit(self._circle_overlay, (square_x, square_y))
    
    def draw(self):
        self._screen.fill(BG_COLOUR)
        self.draw_board()
        self.draw_pieces()
        self.draw_overlay()
        self.draw_widgets()

    def process_model_event(self, event):
        try:
            self.event_to_func_map.get(event.type)(event)
        except:
            raise KeyError('Event type not recognized in Game View (GameView.process_model_event):', event)

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
    
    def set_overlay_coords(self, possible_coords_list, selected_coord):
        self._valid_overlay_coords = possible_coords_list
        self._selected_overlay_coord = selected_coord
    
    def get_valid_overlay_coords(self):
        return self._valid_overlay_coords
    
    def get_selected_overlay_coord(self):
        return self._selected_overlay_coord

    def convert_mouse_pos(self, mouse_pos):
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]

        if (self._board_position[0] <= mouse_x <= self._board_position[0] + self._board_size[0]) and (self._board_position[1] <= mouse_y <= self._board_position[1] + self._board_size[1]):
            x = (mouse_x - self._board_position[0]) // (self._board_size[0] / 10)
            y = (self._board_size[1] - (mouse_y - self._board_position[1])) // (self._board_size[0] / 10)

            return GameEvent.create_event(EventType.BOARD_CLICK, coords=(int(x), int(y)))

        else:
            return GameEvent.create_event(EventType.EMPTY_CLICK)