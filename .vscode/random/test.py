import pygame
pygame.init()

flags = pygame.HWSURFACE | pygame.RESIZABLE
screen = pygame.display.set_mode((500, 500), flags)

run = True
surface = pygame.Surface((500, 500))
surface2 = pygame.Surface((100, 100))
surface.fill((0, 0, 0))
surface2.fill((255, 0, 0))
surface.blit(surface2, (0, 0))
svg = pygame.image.load('C:/Users/Python/Documents/NEA/resources/graphics/sphinx1.svg')
svg_size = 48
svg = pygame.transform.scale(svg, (svg_size, svg_size))
size = 500
pygame.draw.rect(screen, 'red', (0, 0, 100, 100))
while (run):
    new_screen = pygame.transform.scale(surface, (size, size))
    screen.blit(new_screen, (0, 0))
    size += 1

    # svg_size += 1
    # scaled_svg = pygame.transform.scale(svg, (svg_size, svg_size))
    # screen.blit(scaled_svg, (0, 0))

    for event in pygame.event.get():
        width = screen.get_width()
        height = screen.get_height()

        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode(event.size, flags)
    
    pygame.display.flip()
