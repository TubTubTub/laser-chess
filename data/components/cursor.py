import pygame

class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((1, 1))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        
    # def update(self):
    #     self.rect.center = pygame.mouse.get_pos()
    
    def get_sprite_collision(self, mouse_pos, square_group):
        self.rect.center = mouse_pos
        sprite = pygame.sprite.spritecollideany(self, square_group)
        
        return sprite