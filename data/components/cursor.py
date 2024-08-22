import pygame

class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((1, 1))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        
    def update(self):
        self.rect.center = pygame.mouse.get_pos()
    
    def select_square(self, mouse_pos, square_group):
        self.rect.center = mouse_pos
        sprite = pygame.sprite.spritecollide(self, square_group, False)
        
        if not (sprite):
            return None

        return sprite[0]