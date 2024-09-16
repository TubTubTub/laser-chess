import pygame
pygame.init()

flags = pygame.HWSURFACE | pygame.RESIZABLE
screen = pygame.display.set_mode((500, 500), flags)

run = True
surface = pygame.Surface((300, 300))
surface.fill((255, 0, 0))
pygame.draw.rect(surface, 'blue', (30, 30 , 100, 100))
while (run):

    screen.fill((250, 250, 0))
    screen.blit(surface, (0, 0))

    for event in pygame.event.get():
        width = screen.get_width()
        height = screen.get_height()

        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.VIDEORESIZE:
            surface = pygame.transform.scale(surface, (event.w * 3/5, event.h * 3/5))
    pygame.display.flip()

pygame.quit()