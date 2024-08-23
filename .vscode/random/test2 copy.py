import pygame
pygame.init()

flags = pygame.HWSURFACE | pygame.RESIZABLE
screen = pygame.display.set_mode((500, 500), flags)

surface1 = pygame.Surface((500, 500))
surface1.fill((255, 0, 0))
surface2 = pygame.Surface((200, 200))
surface2.fill((0, 0, 255))
surface1.blit(surface2, (10, 10))
size = 100
run = True
while (run):
    
    screen.fill((250, 250, 0))
    size += 0.1
    screen.blit(pygame.transform.scale(surface1, (size, size)), (0, 0))

    for event in pygame.event.get():
        width = screen.get_width()
        height = screen.get_height()

        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode(event.size, flags)
    pygame.display.flip()

pygame.quit()