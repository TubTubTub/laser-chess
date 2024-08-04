import pygame
pygame.init()

flags = pygame.HWSURFACE | pygame.RESIZABLE
screen = pygame.display.set_mode((500, 500), flags)

run = True
while (run):
    
    pygame.draw.rect(screen, (200,0,0), (screen.get_width()/3, screen.get_height()/3, 100, 100))
    screen.fill((250, 250, 0))

    for event in pygame.event.get():
        width = screen.get_width()
        height = screen.get_height()

        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.VIDEORESIZE:
            print(event.w, event.h)
            print(screen.get_rect().size)
            screen = pygame.display.set_mode(event.size, flags)
            print(screen.get_rect().size)
    pygame.display.flip()

pygame.quit()