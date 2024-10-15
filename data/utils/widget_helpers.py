import pygame
from math import sqrt

def create_gradient(size, border_width, border_colour):
    gradient_surface = pygame.Surface(size)

    first_round_end = gradient_surface.height / 2
    second_round_end = gradient_surface.width - first_round_end
    gradient_y_mid = gradient_surface.height / 2

    for i in range(gradient_surface.width):
        draw_height = gradient_surface.height

        if not (first_round_end < i < second_round_end):
            distance_from_cutoff = min(abs(first_round_end - i), abs(i - second_round_end))
            draw_height = calculate_gradient_slice_height(distance_from_cutoff, gradient_surface.height / 2)

        color = pygame.Color(0)
        color.hsva = (int(360 * i / gradient_surface.width), 100, 100)

        draw_rect = pygame.Rect((0, 0, 1, draw_height - 2 * border_width))
        draw_rect.center = (i, gradient_y_mid)

        pygame.draw.rect(gradient_surface, color, draw_rect)

    border_rect = pygame.Rect((0, 0, gradient_surface.width, gradient_surface.height))
    pygame.draw.rect(gradient_surface, border_colour, border_rect , width=border_width, border_radius=int(size[1] / 2))
    
    return gradient_surface
    
def calculate_gradient_slice_height(distance, radius):
    return sqrt(radius ** 2 - distance ** 2) * 2 + 2

def create_slider_thumb(radius, colour, border_colour, border_width):
    thumb_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(thumb_surface, border_colour, (radius, radius), radius, width=int(border_width))
    pygame.draw.circle(thumb_surface, colour, (radius, radius), (radius - border_width))

    return thumb_surface