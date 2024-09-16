import pygame
from data.setup import GRAPHICS
from data.constants import Colour, Piece, ImageType
from data.tools import smoothscale_and_cache

class EmptyPiece(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((1, 1))
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)

class _PieceSprite(pygame.sprite.Sprite):
    def __init__(self, size, coords, high_res_img, low_res_img, colour):
        super().__init__()
        self.type = None
        self.low_res_img = low_res_img
        self.high_res_img = high_res_img

        self.colour = colour
        self.coords = coords

        self.anchor_position = None
        self.size = None

        self.set_image(ImageType.HIGH_RES)
        self.set_rect()
    
    def set_image(self, type):
        match (type):
            case ImageType.LOW_RES:
                self.image = pygame.transform.smoothscale(self.low_res_img, (self.size, self.size))

            case ImageType.HIGH_RES:
                self.image = smoothscale_and_cache(self.high_res_img, (self.size, self.size))

            case _:
                raise ValueError('Invalid type provided for square image')
    
    def set_rect(self):
        self.rect = self.image.get_rect()
        self.rect.topleft = self.calculate_rect_position()

    def calculate_rect_position(self):
        return (self.coords[0] * self.size + self.anchor_position[0], self.anchor_position[1] - self.size * (self.coords[1] + 1))

class SphinxImages(_PieceSprite):
    def __init__(self, **kwargs):
        colour = kwargs.get('colour')
        if colour == Colour.BLUE:
            super().__init__(high_res_img=GRAPHICS['sphinx1'], low_res_img=GRAPHICS['sphinx1_lq'], **kwargs)
        elif colour == Colour.RED:
            super().__init__(high_res_img=GRAPHICS['sphinx2'], low_res_img=GRAPHICS['sphinx2_lq'], **kwargs)
            
        self.type = Piece.SPHINX

class AnubisImages(_PieceSprite):
    def __init__(self, **kwargs):
        colour = kwargs.get('colour')
        if colour == Colour.BLUE:
            super().__init__(high_res_img=GRAPHICS['anubis1'], low_res_img=GRAPHICS['anubis1_lq'], **kwargs)
        elif colour == Colour.RED:
            super().__init__(high_res_img=GRAPHICS['anubis2'], low_res_img=GRAPHICS['anubis2_lq'], **kwargs)
            
        self.type = Piece.ANUBIS

class PyramidImages(_PieceSprite):
    def __init__(self, **kwargs):
        colour = kwargs.get('colour')
        if colour == Colour.BLUE:
            super().__init__(high_res_img=GRAPHICS['pyramid1'], low_res_img=GRAPHICS['pyramid1_lq'], **kwargs)
        elif colour == Colour.RED:
            super().__init__(high_res_img=GRAPHICS['pyramid2'], low_res_img=GRAPHICS['pyramid2_lq'], **kwargs)
            
        self.type = Piece.PYRAMID

class ScarabImages(_PieceSprite):
    def __init__(self, **kwargs):
        colour = kwargs.get('colour')
        if colour == Colour.BLUE:
            super().__init__(high_res_img=GRAPHICS['scarab1'], low_res_img=GRAPHICS['scarab1_lq'], **kwargs)
        elif colour == Colour.RED:
            super().__init__(high_res_img=GRAPHICS['scarab2'], low_res_img=GRAPHICS['scarab2_lq'], **kwargs)
            
        self.type = Piece.SCARAB

class PharoahImages(_PieceSprite):
    def __init__(self, **kwargs):
        colour = kwargs.get('colour')
        if colour == Colour.BLUE:
            super().__init__(high_res_img=GRAPHICS['pharoah1'], low_res_img=GRAPHICS['pharoah1_lq'], **kwargs)
        elif colour == Colour.RED:
            super().__init__(high_res_img=GRAPHICS['pharoah2'], low_res_img=GRAPHICS['pharoah2_lq'], **kwargs)
            
        self.type = Piece.PHAROAH

PIECE_DICTIONARY = {'f': PharoahImages, 'r': ScarabImages, 'p': PyramidImages, 'n': AnubisImages, 's': SphinxImages}

def create_piece(piece, coords, size, colour):
    target_piece_class = PIECE_DICTIONARY[piece]
    return target_piece_class(size=size, colour=colour, coords=coords)