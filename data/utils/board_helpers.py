import pygame
from data.utils.data_helpers import get_user_settings
from data.assets import DEFAULT_FONT

user_settings = get_user_settings()

def create_board(board_size, primary_colour, secondary_colour, font=DEFAULT_FONT):
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

        pygame.draw.rect(board_surface, square_colour, (square_x, square_y, square_size + 1, square_size + 1)) # +1 to fill in black lines

        if y == 7:
            text_position = (square_x + square_size * 0.7, square_y + square_size * 0.55)
            text_size = square_size / 3
            font.render_to(board_surface, text_position, str(chr(x + 1 + 96)), fgcolor=(10, 10, 10, 175), size=text_size)
        if x == 0:
            text_position = (square_x + square_size * 0.1, square_y + square_size * 0.1)
            text_size = square_size / 3
            font.render_to(board_surface, text_position, str(7-y + 1), fgcolor=(10, 10, 10, 175), size=text_size)
    
    return board_surface

def create_square_overlay(square_size, colour):
    overlay = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
    overlay.fill(colour)

    return overlay

def create_circle_overlay(square_size, colour):
    overlay = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
    pygame.draw.circle(overlay, colour, (square_size / 2, square_size / 2), square_size / 4)

    return overlay

def coords_to_screen_pos(coords, board_position, square_size):
    x = board_position[0] + (coords[0] * square_size)
    y = board_position[1] + ((7 - coords[1]) * square_size)

    return (x, y)

def screen_pos_to_coords(mouse_position, board_position, board_size):
    if (board_position[0] <= mouse_position[0] <= board_position[0] + board_size[0]) and (board_position[1] <= mouse_position[1] <= board_position[1] + board_size[1]):
        x = (mouse_position[0] - board_position[0]) // (board_size[0] / 10)
        y = (board_size[1] - (mouse_position[1] - board_position[1])) // (board_size[0] / 10)
        return (int(x), int(y))
    
    return None