import pygame
from data.constants import EventType, Colour, LaserType, BG_COLOUR, OVERLAY_COLOUR
from data.components.piece_group import PieceGroup
from data.components.widget_group import WidgetGroup
from data.components.game_event import GameEvent
from data.components.cursor import Cursor
from data.utils.settings_helpers import get_settings_json
from data.utils.board_helpers import coords_to_screen_pos
from data.utils.view_helpers import create_board, create_circle_overlay, create_square_overlay
from data.setup import GRAPHICS

class GameView:
    def __init__(self, model):
        self.model = model
        self._screen = pygame.display.get_surface()
        self._app_settings = get_settings_json()
        self.event_to_func_map = {
            EventType.UPDATE_PIECES: self.handle_update_pieces,
            EventType.REMOVE_PIECE: self.handle_remove_piece,
            EventType.SET_LASER: self.handle_set_laser,
        }

        self.model.register_listener(self.process_model_event)
        
        self._board_size = self.calculate_board_size()
        self._board_position = self.calculate_board_position()
        self._board_surface = create_board(self._board_size, self._app_settings['primaryBoardColour'], self._app_settings['secondaryBoardColour'])
        self._board_unscaled = self._board_surface.copy() # surface glitches if scaling in place

        self._cursor = Cursor()

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

        self.laser_path = []
        self.laser_start_ticks = 0
        self.laser_colour = None
    
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
    
    def handle_set_laser(self, event):
        laser_types = [LaserType.END]
        laser_rotation = [event.laser_path[0][1]]
        
        for i in range(1, len(event.laser_path)):
            previous_direction = event.laser_path[i-1][1]
            current_direction = event.laser_path[i][1]

            if current_direction == previous_direction:
                print('WOW3', event.laser_path[i][0])
                laser_types.append(LaserType.STRAIGHT)
                laser_rotation.append(current_direction)
            elif current_direction == previous_direction.get_clockwise():
                print('WOW2', event.laser_path[i][0])
                laser_types.append(LaserType.CORNER)
                laser_rotation.append(current_direction)
            elif current_direction == previous_direction.get_anticlockwise():
                print('WOW', event.laser_path[i][0])
                laser_types.append(LaserType.CORNER)
                laser_rotation.append(previous_direction.get_opposite())
            
            #WHY IS EVENT PATH NOT ORDERED?

        if (event.laser_path[-1][0][0] > 9) or (event.laser_path[-1][0][0] > 7):
            laser_types[-1] = LaserType.END
            event.laser_path[-1] = (event.laser_path[-1][0], event.laser_path[-1][1].get_opposite())
            laser_rotation[-1] = laser_rotation[-1].get_opposite()
        

        self.laser_path = [(coords, rotation, type) for (coords, dir), rotation, type in zip(event.laser_path, laser_rotation, laser_types)]
        print(event.laser_path)
        print(self.laser_path)
        self.laser_start_ticks = pygame.time.get_ticks()
        self.laser_colour = event.active_colour
    
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
    
    def draw_laser(self):
        if not self.laser_path:
            return
        
        elapsed_seconds = (pygame.time.get_ticks() - self.laser_start_ticks) / 1000

        # if elapsed_seconds >= 5:
        #     self.laser_path = []
        #     self.laser_start_ticks = 0
        #     self.laser_colour = None
        #     return
         
        square_size = self._board_size[0] / 10
        square = pygame.Surface((30, 30))
        square.fill(self.laser_colour)

        type_to_image = {
            LaserType.END: ['laser_end_1', 'laser_end_2'],
            LaserType.STRAIGHT: ['laser_straight_1', 'laser_straight_2'],
            LaserType.CORNER: ['laser_corner_1', 'laser_corner_2']
        }

        for coords, rotation, type in self.laser_path:
            square_x, square_y = coords_to_screen_pos(coords, self._board_position, square_size)

            image = GRAPHICS[type_to_image[type][self.laser_colour]]
            scaled_image = pygame.transform.scale(image, (square_size, square_size))
            rotated_image = pygame.transform.rotate(scaled_image, rotation.to_angle())

            self._screen.blit(rotated_image, (square_x, square_y))
    
    def draw(self):
        self._screen.fill(BG_COLOUR)
        self.draw_board()
        self.draw_pieces()
        self.draw_overlay()
        self.draw_widgets()
        self.draw_laser()

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

        elif collided := self._cursor.get_sprite_collision(mouse_pos, self._widget_group):
            return collided.event
        
        else:
            return GameEvent.create_event(EventType.EMPTY_CLICK)