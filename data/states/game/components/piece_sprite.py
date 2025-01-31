import pygame
from data.assets import GRAPHICS
from data.constants import Colour, Piece, ImageType
from data.utils.asset_helpers import scale_and_cache
from data.utils.board_helpers import coords_to_screen_pos

class EmptyPiece(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((1, 1))
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
    
    def set_image(self, type):
        pass

    def set_rect(self):
        pass
    
    def set_geometry(self, anchor_position, size):
        pass

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