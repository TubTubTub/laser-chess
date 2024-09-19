import pygame
    
def create_board(board_size, primary_colour, secondary_colour):
    square_size = board_size[0] / 10
    board_surface = pygame.Surface(board_size)

    for i in range(80):
        x = i % 10
        y = i // 10

        if (x + y) % 2 == 0:
            square_colour = primary_colour
        else:
            square_colour = secondary_colour
        
        square_x = x * square_size
        square_y = y * square_size

        pygame.draw.rect(board_surface, square_colour, (square_x, square_y, square_size, square_size))
    
    return board_surface

def create_square_overlay(square_size, colour):
    overlay = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
    overlay.fill(colour)

    return overlay

def create_circle_overlay(square_size, colour):
    overlay = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
    pygame.draw.circle(overlay, colour, (square_size / 2, square_size / 2), square_size / 4)

    return overlay