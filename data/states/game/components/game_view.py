import pygame
from data.constants import GameEventType, GameState, LaserType, Colour, StatusText, OVERLAY_COLOUR
from data.states.game.components.piece_group import PieceGroup
from data.components.widget_group import WidgetGroup
from data.components.custom_event import CustomEvent
from data.components.cursor import Cursor
from data.utils.data_helpers import get_user_settings
from data.utils.board_helpers import create_board, create_circle_overlay, create_square_overlay, coords_to_screen_pos
from data.assets import GRAPHICS
from data.states.game.widget_dict import GAME_WIDGETS

class GameView:
    def __init__(self, model):
        self._model = model
        self._screen = pygame.display.get_surface()
        self._user_settings = get_user_settings()
        self._event_to_func_map = {
            GameEventType.UPDATE_PIECES: self.handle_update_pieces,
            GameEventType.REMOVE_PIECE: self.handle_remove_piece,
            GameEventType.SET_LASER: self.handle_set_laser,
            GameEventType.PAUSE_CLICK: self.handle_pause,
        }
        self._model.register_listener(self.process_model_event, 'game')

        self._board_size = GAME_WIDGETS['chessboard'].get_size()
        self._board_position = GAME_WIDGETS['chessboard'].get_position()
        self._square_size = self._board_size[0] / 10

        self._cursor = Cursor()

        self._piece_group = PieceGroup()
        self.handle_update_pieces(toggle_timers=False)

        self.set_status_text(StatusText.PLAYER_MOVE)

        self._widget_group = WidgetGroup(GAME_WIDGETS)
        GAME_WIDGETS['move_list'].reset_move_list()
        GAME_WIDGETS['move_list'].kill()
        GAME_WIDGETS['scroll_area'].set_image()
        
        self._valid_overlay_coords = []
        self._selected_overlay_coord = None

        self._circle_overlay = create_circle_overlay(self._square_size, OVERLAY_COLOUR)
        self._square_overlay = create_square_overlay(self._square_size, OVERLAY_COLOUR)
        self._circle_overlay_unscaled = self._circle_overlay.copy()
        self._square_overlay_unscaled = self._square_overlay.copy()

        self._laser_path = []
        self._laser_start_ticks = 0
        self._laser_colour = None

        self.states = {
            GameState.LASER_FIRING: False,
        }
    
    def set_status_text(self, status):
        match status:
            case StatusText.PLAYER_MOVE:
                GAME_WIDGETS['status_text'].update_text(f"{self._model.states['ACTIVE_COLOUR'].name}'s turn to move")
            case StatusText.CPU_MOVE:
                GAME_WIDGETS['status_text'].update_text(f"CPU calculating a crazy move...")
            case StatusText.WIN:
                GAME_WIDGETS['status_text'].update_text(f"{self._model.states['WINNER'].name} won!")
            case StatusText.DRAW:
                GAME_WIDGETS['status_text'].update_text(f"Game is a draw! Boring...")
    
    def handle_resize(self, resize_end=False):
        self._piece_group.handle_resize(self._board_position, self._board_size, resize_end)
        self._widget_group.handle_resize(self._screen.get_size())

        self._circle_overlay = pygame.transform.scale(self._circle_overlay_unscaled, (self._square_size, self._square_size))
        self._square_overlay = pygame.transform.scale(self._square_overlay_unscaled, (self._square_size, self._square_size))

        self._board_size = GAME_WIDGETS['chessboard'].get_size()
        self._board_position = GAME_WIDGETS['chessboard'].get_position()
        self._square_size = self._board_size[0] / 10
    
    def handle_update_pieces(self, event=None, toggle_timers=True):
        piece_list = self._model.get_piece_list()
        self._piece_group.initialise_pieces(piece_list, self._board_position, self._board_size)

        if event:
            GAME_WIDGETS['move_list'].append_to_move_list(event.move_notation)
            GAME_WIDGETS['scroll_area'].set_image()

        if self._model.states['ACTIVE_COLOUR'] == Colour.BLUE:
            self.set_status_text(StatusText.PLAYER_MOVE)
        elif self._model.states['CPU_ENABLED'] is False:
            self.set_status_text(StatusText.PLAYER_MOVE)
        else:
            self.set_status_text(StatusText.CPU_MOVE)

        if self._model.states['WINNER']:
            self.toggle_timer(self._model.states['ACTIVE_COLOUR'], False)
            self.toggle_timer(self._model.states['ACTIVE_COLOUR'].get_flipped_colour(), False)

            self.set_status_text(StatusText.WIN)

        elif toggle_timers:
            self.toggle_timer(self._model.states['ACTIVE_COLOUR'], True)
            self.toggle_timer(self._model.states['ACTIVE_COLOUR'].get_flipped_colour(), False)
    
    def handle_remove_piece(self, event):
        self._piece_group.remove_piece(event.coords_to_remove)
    
    def handle_set_laser(self, event):
        laser_types = [LaserType.END]
        laser_rotation = [event.laser_path[0][1]]
        
        for i in range(1, len(event.laser_path)):
            previous_direction = event.laser_path[i-1][1]
            current_direction = event.laser_path[i][1]

            if current_direction == previous_direction:
                laser_types.append(LaserType.STRAIGHT)
                laser_rotation.append(current_direction)
            elif current_direction == previous_direction.get_clockwise():
                laser_types.append(LaserType.CORNER)
                laser_rotation.append(current_direction)
            elif current_direction == previous_direction.get_anticlockwise():
                laser_types.append(LaserType.CORNER)
                laser_rotation.append(current_direction.get_anticlockwise())
        
        if event.has_hit:
            laser_types[-1] = LaserType.END
            event.laser_path[-1] = (event.laser_path[-1][0], event.laser_path[-2][1].get_opposite())
            laser_rotation[-1] = event.laser_path[-2][1].get_opposite()

        self._laser_path = [(coords, rotation, type) for (coords, dir), rotation, type in zip(event.laser_path, laser_rotation, laser_types)]
        self._laser_start_ticks = pygame.time.get_ticks()
        self._laser_colour = self._model.states['ACTIVE_COLOUR']

        self.states[GameState.LASER_FIRING] = True
    
    def handle_pause(self, event):
        is_active = not(self._model.states['PAUSED'])
        self.toggle_timer(self._model.states['ACTIVE_COLOUR'], is_active)
    
    def handle_widget_click(self, event):
        raise NotImplementedError
    
    def initialise_timers(self, end_callback):
        if self._model.states['TIME_ENABLED'] is False:
            GAME_WIDGETS['blue_timer'].kill()
            GAME_WIDGETS['red_timer'].kill()
        else:
            GAME_WIDGETS['blue_timer'].set_time(self._model.states['TIME'] * 60 * 1000)
            GAME_WIDGETS['red_timer'].set_time(self._model.states['TIME'] * 60 * 1000)

            GAME_WIDGETS['blue_timer'].register_end_callback(end_callback)
            GAME_WIDGETS['red_timer'].register_end_callback(end_callback)

            self.toggle_timer(self._model.states['ACTIVE_COLOUR'], True)

    def toggle_timer(self, colour, is_active):
        if colour == Colour.BLUE:
            if GAME_WIDGETS['blue_timer'].get_active() != is_active:
                GAME_WIDGETS['blue_timer'].set_active(is_active)
        else:
            if GAME_WIDGETS['red_timer'].get_active() != is_active:
                GAME_WIDGETS['red_timer'].set_active(is_active)

    def draw_pieces(self):
        self._piece_group.draw(self._screen)
    
    def draw_widgets(self):
        self._widget_group.draw()

    def draw_overlay(self):
        if not self._selected_overlay_coord:
            return
        
        square_x, square_y = coords_to_screen_pos(self._selected_overlay_coord, self._board_position, self._square_size)
        self._screen.blit(self._square_overlay, (square_x, square_y))

        for coords in self._valid_overlay_coords:
            square_x, square_y = coords_to_screen_pos(coords, self._board_position, self._square_size)
            self._screen.blit(self._circle_overlay, (square_x, square_y))
    
    def draw_laser(self):
        if not self._laser_path:
            return
        
        elapsed_seconds = (pygame.time.get_ticks() - self._laser_start_ticks) / 1000

        if elapsed_seconds >= 1.5:
            self._laser_path = []
            self._laser_start_ticks = 0
            self._laser_colour = None
            self.states[GameState.LASER_FIRING] = False
            return

        self._square_size = self._board_size[0] / 10

        type_to_image = {
            LaserType.END: ['laser_end_1', 'laser_end_2'],
            LaserType.STRAIGHT: ['laser_straight_1', 'laser_straight_2'],
            LaserType.CORNER: ['laser_corner_1', 'laser_corner_2']
        }

        for coords, rotation, type in self._laser_path:
            square_x, square_y = coords_to_screen_pos(coords, self._board_position, self._square_size)

            image = GRAPHICS[type_to_image[type][self._laser_colour]]
            scaled_image = pygame.transform.scale(image, (self._square_size, self._square_size))
            rotated_image = pygame.transform.rotate(scaled_image, rotation.to_angle())

            self._screen.blit(rotated_image, (square_x, square_y))
    
    def draw(self):
        self._widget_group.update()
        self.draw_widgets()
        self.draw_pieces()
        self.draw_overlay()
        self.draw_laser()

    def process_model_event(self, event):
        try:
            self._event_to_func_map.get(event.type)(event)
        except:
            raise KeyError('Event type not recognized in Game View (GameView.process_model_event):', event.type)
    
    def set_overlay_coords(self, possible_coords_list, selected_coord):
        self._valid_overlay_coords = possible_coords_list
        self._selected_overlay_coord = selected_coord
    
    def get_valid_overlay_coords(self):
        return self._valid_overlay_coords
    
    def get_selected_overlay_coord(self):
        return self._selected_overlay_coord

    def convert_mouse_pos(self, event):
        mouse_x = event.pos[0]
        mouse_y = event.pos[1]

        if (self._board_position[0] <= mouse_x <= self._board_position[0] + self._board_size[0]) and (self._board_position[1] <= mouse_y <= self._board_position[1] + self._board_size[1]):
            x = (mouse_x - self._board_position[0]) // (self._board_size[0] / 10)
            y = (self._board_size[1] - (mouse_y - self._board_position[1])) // (self._board_size[0] / 10)

            return CustomEvent.create_event(GameEventType.BOARD_CLICK, coords=(int(x), int(y)))

        elif self._cursor.get_sprite_collision(event.pos, self._widget_group):
            return CustomEvent.create_event(GameEventType.WIDGET_CLICK)

        return CustomEvent.create_event(GameEventType.EMPTY_CLICK)

    def process_widget_event(self, event):
        return self._widget_group.process_event(event)