import pygame
from data.constants import LaserType
from data.utils.board_helpers import coords_to_screen_pos
from data.assets import GRAPHICS, SFX
from data.constants import EMPTY_BB, ShaderType, Colour
from data.managers.animation import animation
from data.managers.audio import audio
from data.managers.window import window
from pprint import pprint

type_to_image = {
    LaserType.END: ['laser_end_1', 'laser_end_2'],
    LaserType.STRAIGHT: ['laser_straight_1', 'laser_straight_2'],
    LaserType.CORNER: ['laser_corner_1', 'laser_corner_2']
}

GLOW_SCALE_FACTOR = 1.5

class LaserDraw:
    def __init__(self, board_position, board_size):
        self._board_position = board_position
        self._square_size = board_size[0] / 10
        self._laser_lists = []
    
    @property
    def firing(self):
        return len(self._laser_lists) > 0
    
    def add_laser(self, laser_result, laser_colour):
        laser_path = laser_result.laser_path.copy()
        laser_types = [LaserType.END]
        laser_rotation = [laser_path[0][1]]
        laser_lights = []
        
        for i in range(1, len(laser_path)):
            previous_direction = laser_path[i-1][1]
            current_coords, current_direction = laser_path[i]

            if current_direction == previous_direction:
                laser_types.append(LaserType.STRAIGHT)
                laser_rotation.append(current_direction)
            elif current_direction == previous_direction.get_clockwise():
                laser_types.append(LaserType.CORNER)
                laser_rotation.append(current_direction)
            elif current_direction == previous_direction.get_anticlockwise():
                laser_types.append(LaserType.CORNER)
                laser_rotation.append(current_direction.get_anticlockwise())
            
            if i in [1, len(laser_path) - 1]:
                abs_position = coords_to_screen_pos(current_coords, self._board_position, self._square_size)
                laser_lights.append([
                    (abs_position[0] / window.size[0], abs_position[1] / window.size[1]),
                    0.5,
                    (0, 0, 255) if laser_colour == Colour.BLUE else (255, 0, 0),
                ])
                print('adding light at', abs_position, laser_colour.name)
        
        if laser_result.hit_square_bitboard != EMPTY_BB:
            laser_types[-1] = LaserType.END
            laser_path[-1] = (laser_path[-1][0], laser_path[-2][1].get_opposite())
            laser_rotation[-1] = laser_path[-2][1].get_opposite()

        laser_path = [(coords, rotation, type) for (coords, dir), rotation, type in zip(laser_path, laser_rotation, laser_types)]
        self._laser_lists.append((laser_path, laser_colour))

        window.set_effect(ShaderType.RAYS, lights=laser_lights)
        animation.set_timer(1000, self.remove_laser)
        audio.play_sfx(SFX['laser'])
    
    def remove_laser(self):
        self._laser_lists.pop(0)

        if len(self._laser_lists) == 0:
            window.clear_effect(ShaderType.RAYS)
    
    def draw_laser(self, screen, laser_list, glow=True):
        laser_path, laser_colour = laser_list
        laser_list = []
        glow_list = []

        for coords, rotation, type in laser_path:
            square_x, square_y = coords_to_screen_pos(coords, self._board_position, self._square_size)

            image = GRAPHICS[type_to_image[type][laser_colour]]
            rotated_image = pygame.transform.rotate(image, rotation.to_angle())
            scaled_image = pygame.transform.scale(rotated_image, (self._square_size + 1, self._square_size + 1)) # +1 to prevent rounding creating black lines
            laser_list.append((scaled_image, (square_x, square_y)))

            scaled_glow = pygame.transform.scale(rotated_image, (self._square_size * GLOW_SCALE_FACTOR, self._square_size * GLOW_SCALE_FACTOR))
            offset = self._square_size * ((GLOW_SCALE_FACTOR - 1) / 2)
            glow_list.append((scaled_glow, (square_x - offset, square_y - offset)))

        if glow:
            screen.fblits(glow_list, pygame.BLEND_RGB_ADD)

        screen.blits(laser_list)
    
    def draw(self, screen):
        for laser_list in self._laser_lists:
            self.draw_laser(screen, laser_list)
    
    def handle_resize(self, board_position, board_size):
        self._board_position = board_position
        self._square_size = board_size[0] / 10