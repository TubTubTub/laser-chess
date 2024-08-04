import pygame
from .. import tools

class Game(tools._State):
    def __init__(self):
        tools._State.__init__(self)
        self.next = 'menu'
    
    def cleanup(self):
        print('cleaning')
    
    def startup(self):
        print('starting')
    
    def get_event(self, event):
        if event.type == pygame.KEYDOWN:
            print('key down')
            self.done = True
    
    def draw(self, screen):
        size = screen.get_rect().size
        x = size[0]
        y = size[1]
        length = min(x, y)

        rect1_size = (length * 0.8, length * 0.8)
        rect1 = pygame.Rect(0, 0, *(rect1_size))
        rect1.center = (x/2, y/2)

        rect2_size = (x/2 - rect1.width *0.8, length*0.8)
        rect2 = pygame.Rect(0, 0, *(rect2_size))
        rect2.center = (((x/2) - (rect1.width/2))/2, size[1]/2)
        
        rect3_size = (x/2 - rect1.width *0.8, length*0.8)
        rect3 = pygame.Rect(0, 0, *(rect2_size))
        rect3.center = (x - (((x/2) - (rect1.width/2))/2), size[1]/2)
        
        screen.fill((0, 255, 255))
        pygame.draw.rect(screen, (50, 50, 50), rect1)
        pygame.draw.rect(screen, (100, 100, 100), rect2)
        pygame.draw.rect(screen, (200, 200, 200), rect3)
    
    def update(self, screen):
        self.draw(screen)