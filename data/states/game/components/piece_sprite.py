import pygame
from data.helpers.board_helpers import coords_to_screen_pos
from data.helpers.asset_helpers import scale_and_cache
from data.utils.assets import GRAPHICS
from data.utils.enums import Piece

class PieceSprite(pygame.sprite.Sprite):
    def __init__(self, piece, colour, rotation):
        super().__init__()
        self.colour = colour
        self.rotation = rotation

        self.type = piece
        self.coords = None
        self.size = None

    @property
    def image_name(self):
        return Piece(self.type).name.lower() + '_' + str(self.colour) + '_' + self.rotation

    def set_image(self):
        self.image = scale_and_cache(GRAPHICS[self.image_name], (self.size, self.size))

    def set_geometry(self, new_position, square_size):
        self.size = square_size
        self.rect = pygame.FRect((0, 0, square_size, square_size))

        if self.coords:
            self.rect.topleft = coords_to_screen_pos(self.coords, new_position, square_size)
        else:
            self.rect.topleft = new_position

    def set_coords(self, new_coords):
        self.coords = new_coords