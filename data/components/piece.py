import pygame
from data.setup import GRAPHICS
from data.components.constants import Colour

class _Piece(pygame.sprite.Sprite):
    def __init__(self, size, high_res_svg, low_res_png, colour):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(high_res_svg, (size, size))
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        
        self.low_res_png = low_res_png
        self.high_res_svg = high_res_svg

        self.type = None

class Sphinx(_Piece):
    def __init__(self, **kwargs):
        colour = kwargs.get('colour')
        if colour == Colour.BLUE:
            super().__init__(high_res_svg=GRAPHICS['sphinx1'], low_res_png=GRAPHICS['sphinx1_lq'], **kwargs)
        elif colour == Colour.RED:
            super().__init__(high_res_svg=GRAPHICS['sphinx2'], low_res_png=GRAPHICS['sphinx2_lq'], **kwargs)
            
        self.type = "sphinx"

class Anubis(_Piece):
    def __init__(self, **kwargs):
        colour = kwargs.get('colour')
        if colour == Colour.BLUE:
            super().__init__(high_res_svg=GRAPHICS['anubis1'], low_res_png=GRAPHICS['anubis1_lq'], **kwargs)
        elif colour == Colour.RED:
            super().__init__(high_res_svg=GRAPHICS['anubis2'], low_res_png=GRAPHICS['anubis2_lq'], **kwargs)
            
        self.type = "anubis"

class Pyramid(_Piece):
    def __init__(self, **kwargs):
        colour = kwargs.get('colour')
        if colour == Colour.BLUE:
            super().__init__(high_res_svg=GRAPHICS['pyramid1'], low_res_png=GRAPHICS['pyramid1_lq'], **kwargs)
        elif colour == Colour.RED:
            super().__init__(high_res_svg=GRAPHICS['pyramid2'], low_res_png=GRAPHICS['pyramid2_lq'], **kwargs)
            
        self.type = "pyramid"

class Scarab(_Piece):
    def __init__(self, **kwargs):
        colour = kwargs.get('colour')
        if colour == Colour.BLUE:
            super().__init__(high_res_svg=GRAPHICS['scarab1'], low_res_png=GRAPHICS['scarab1_lq'], **kwargs)
        elif colour == Colour.RED:
            super().__init__(high_res_svg=GRAPHICS['scarab2'], low_res_png=GRAPHICS['scarab2_lq'], **kwargs)
            
        self.type = "scarab"

class Pharoah(_Piece):
    def __init__(self, **kwargs):
        colour = kwargs.get('colour')
        if colour == Colour.BLUE:
            super().__init__(high_res_svg=GRAPHICS['pharoah1'], low_res_png=GRAPHICS['pharoah1_lq'], **kwargs)
        elif colour == Colour.RED:
            super().__init__(high_res_svg=GRAPHICS['pharoah2'], low_res_png=GRAPHICS['pharoah2_lq'], **kwargs)
            
        self.type = "pharoah"

PIECE_DICTIONARY = {'f': Pharoah, 'r': Scarab, 'p': Pyramid, 'n': Anubis, 's': Sphinx}

def create_piece(piece, size, colour):
    target_piece_class = PIECE_DICTIONARY[piece]
    return target_piece_class(size=size, colour=colour)