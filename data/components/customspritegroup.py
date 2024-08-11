import pygame

class CustomSpriteGroup(pygame.sprite.Group):
    def __init__(self):
        pygame.sprite.Group.__init__(self)
    
    def draw_high_res_svg(self, screen):
        for sprite in self.sprites():
            sprite.draw_high_res_svg(screen)