import pygame
from data.tools import GRAPHICS
from data.constants import Colour, Piece, ImageType
from data.tools import smoothscale_and_cache
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

class _PieceSprite(pygame.sprite.Sprite):
    def __init__(self, coords, high_res_img, low_res_img, colour):
        super().__init__()
        self.type = None
        self.low_res_img = low_res_img
        self.high_res_img = high_res_img

        self.colour = colour
        self.coords = coords

        self.anchor_position = None
        self.size = None
        self.rotation = None
    
    def set_image(self, type):
        match (type):
            case ImageType.LOW_RES:
                rotated_img = pygame.transform.rotate(self.low_res_img, self.rotation.to_angle())
                self.image = pygame.transform.scale(rotated_img, (self.size, self.size))
                self.set_rect()

            case ImageType.HIGH_RES:
                rotated_img = pygame.transform.rotate(self.high_res_img, self.rotation.to_angle())
                self.image = smoothscale_and_cache(rotated_img, (self.size, self.size))
                self.set_rect()

            case _:
                raise ValueError('Invalid type provided for square image')
    
    def set_rect(self):
        self.rect = self.image.get_rect()
        self.rect.topleft = coords_to_screen_pos(self.coords, self.anchor_position, self.size)
    
    def set_geometry(self, anchor_position, size):
        self.anchor_position = anchor_position
        self.size = size
    
    def set_rotation(self, rotation):
        self.rotation = rotation

class SphinxImages(_PieceSprite):
    def __init__(self, **kwargs):
        colour = kwargs.get('colour')
        if colour == Colour.BLUE:
            super().__init__(high_res_img=GRAPHICS['sphinx_1'], low_res_img=GRAPHICS['sphinx_1_lq'], **kwargs)
        elif colour == Colour.RED:
            super().__init__(high_res_img=GRAPHICS['sphinx_2'], low_res_img=GRAPHICS['sphinx_2_lq'], **kwargs)
            
        self.type = Piece.SPHINX

class AnubisImages(_PieceSprite):
    def __init__(self, **kwargs):
        colour = kwargs.get('colour')
        if colour == Colour.BLUE:
            super().__init__(high_res_img=GRAPHICS['anubis_1'], low_res_img=GRAPHICS['anubis_1_lq'], **kwargs)
        elif colour == Colour.RED:
            super().__init__(high_res_img=GRAPHICS['anubis_2'], low_res_img=GRAPHICS['anubis_2_lq'], **kwargs)
            
        self.type = Piece.ANUBIS

class PyramidImages(_PieceSprite):
    def __init__(self, **kwargs):
        colour = kwargs.get('colour')
        if colour == Colour.BLUE:
            super().__init__(high_res_img=GRAPHICS['pyramid_1'], low_res_img=GRAPHICS['pyramid_1_lq'], **kwargs)
        elif colour == Colour.RED:
            super().__init__(high_res_img=GRAPHICS['pyramid_2'], low_res_img=GRAPHICS['pyramid_2_lq'], **kwargs)
            
        self.type = Piece.PYRAMID

class ScarabImages(_PieceSprite):
    def __init__(self, **kwargs):
        colour = kwargs.get('colour')
        if colour == Colour.BLUE:
            super().__init__(high_res_img=GRAPHICS['scarab_1'], low_res_img=GRAPHICS['scarab_1_lq'], **kwargs)
        elif colour == Colour.RED:
            super().__init__(high_res_img=GRAPHICS['scarab_2'], low_res_img=GRAPHICS['scarab_2_lq'], **kwargs)
            
        self.type = Piece.SCARAB

class PharoahImages(_PieceSprite):
    def __init__(self, **kwargs):
        colour = kwargs.get('colour')
        if colour == Colour.BLUE:
            super().__init__(high_res_img=GRAPHICS['pharoah_1'], low_res_img=GRAPHICS['pharoah_1_lq'], **kwargs)
        elif colour == Colour.RED:
            super().__init__(high_res_img=GRAPHICS['pharoah_2'], low_res_img=GRAPHICS['pharoah_2_lq'], **kwargs)
            
        self.type = Piece.PHAROAH

PIECE_DICTIONARY = {'f': PharoahImages, 'r': ScarabImages, 'p': PyramidImages, 'n': AnubisImages, 's': SphinxImages}

def create_piece(piece, coords, colour):
    target_piece_class = PIECE_DICTIONARY[piece.lower()]
    return target_piece_class(colour=colour, coords=coords)