import pygame
from data.constants import LaserType
from data.utils.board_helpers import coords_to_screen_pos
from data.assets import GRAPHICS
from data.constants import EMPTY_BB
from data.components.animation import animation

type_to_image = {
    LaserType.END: ['laser_end_1', 'laser_end_2'],
    LaserType.STRAIGHT: ['laser_straight_1', 'laser_straight_2'],
    LaserType.CORNER: ['laser_corner_1', 'laser_corner_2']
}

class LaserDraw:
    def __init__(self, board_position, board_size):
        self._board_position = board_position
        self._square_size = board_size[0] / 10
        self._laser_lists = []
    
    def add_laser(self, laser_result, laser_colour):
        laser_path = laser_result.laser_path.copy()
        laser_types = [LaserType.END]
        laser_rotation = [laser_path[0][1]]
        
        for i in range(1, len(laser_path)):
            previous_direction = laser_path[i-1][1]
            current_direction = laser_path[i][1]

            if current_direction == previous_direction:
                laser_types.append(LaserType.STRAIGHT)
                laser_rotation.append(current_direction)
            elif current_direction == previous_direction.get_clockwise():
                laser_types.append(LaserType.CORNER)
                laser_rotation.append(current_direction)
            elif current_direction == previous_direction.get_anticlockwise():
                laser_types.append(LaserType.CORNER)
                laser_rotation.append(current_direction.get_anticlockwise())
        
        if laser_result.hit_square_bitboard != EMPTY_BB:
            laser_types[-1] = LaserType.END
            laser_path[-1] = (laser_path[-1][0], laser_path[-2][1].get_opposite())
            laser_rotation[-1] = laser_path[-2][1].get_opposite()

        laser_path = [(coords, rotation, type) for (coords, dir), rotation, type in zip(laser_path, laser_rotation, laser_types)]
        self._laser_lists.append((laser_path, laser_colour))
        animation.set_timer(1000, lambda: self._laser_lists.pop(0))
    
    def draw_laser(self, screen, laser_list):
        laser_path, laser_colour = laser_list
        for coords, rotation, type in laser_path:
            square_x, square_y = coords_to_screen_pos(coords, self._board_position, self._square_size)

            image = GRAPHICS[type_to_image[type][laser_colour]]
            scaled_image = pygame.transform.scale(image, (self._square_size + 1, self._square_size + 1)) # +1 to prevent rounding creating black lines
            rotated_image = pygame.transform.rotate(scaled_image, rotation.to_angle())

            screen.blit(rotated_image, (square_x, square_y))
    
    def draw(self, screen):
        for laser_list in self._laser_lists:
            self.draw_laser(screen, laser_list)
    
    def handle_resize(self, board_position, board_size):
        self._board_position = board_position
        self._square_size = board_size[0] / 10