import pygame
from data.setup import GRAPHICS
from data.tools import smoothscale_and_cache

class Piece(pygame.sprite.Sprite):
    def __init__(self, size, high_res_svg, low_res_png):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(high_res_svg, (size, size))
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)

        self._image_copy = self.image.copy()
        
        self.low_res_png = low_res_png
        self.high_res_svg = high_res_svg

        self.type = None
    
    def update(self, size):
        self.image = smoothscale_and_cache(self._image_copy, (size, size))

class Sphinx(Piece):
    def __init__(self, **kwargs):
        super(Sphinx, self).__init__(high_res_svg=GRAPHICS['laser2'], low_res_png=GRAPHICS['black_roook'], **kwargs)
        self.type = "sphinx"