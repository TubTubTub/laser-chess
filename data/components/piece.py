import pygame
from data.setup import GRAPHICS
from data.tools import smoothscale_and_cache

class Piece(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(image, (48, 48))
        self.rect = image.get_rect()
        self.rect.topleft = (0, 0)

        self._image_copy = image.copy()
        
        self.type = None
    
    def update(self, size):
        self.image = smoothscale_and_cache(self._image_copy, (size, size))

class Sphinx(Piece):
    def __init__(self, **kwargs):
        super(Sphinx, self).__init__(image=GRAPHICS['sphinx1'], **kwargs)
        self.type = "sphinx"