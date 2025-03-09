import pygame
from data.utils.constants import OVERLAY_COLOUR_LIGHT, OVERLAY_COLOUR_DARK
from data.helpers.board_helpers import coords_to_screen_pos, screen_pos_to_coords, create_square_overlay, create_circle_overlay

class OverlayDraw:
    def __init__(self, board_position, board_size, limit_hover=True):
        self._board_position = board_position
        self._board_size = board_size

        self._hovered_coords = None
        self._selected_coords = None
        self._available_coords = None

        self._limit_hover = limit_hover

        self._selected_overlay = None
        self._hovered_overlay = None
        self._available_overlay = None

        self.initialise_overlay_surfaces()

    @property
    def square_size(self):
        return self._board_size[0] / 10

    def initialise_overlay_surfaces(self):
        self._selected_overlay = create_square_overlay(self.square_size, OVERLAY_COLOUR_DARK)
        self._hovered_overlay = create_square_overlay(self.square_size, OVERLAY_COLOUR_LIGHT)
        self._available_overlay = create_circle_overlay(self.square_size, OVERLAY_COLOUR_LIGHT)

    def set_hovered_coords(self, mouse_pos):
        self._hovered_coords = screen_pos_to_coords(mouse_pos, self._board_position, self._board_size)

    def set_selected_coords(self, coords):
        self._selected_coords = coords

    def set_available_coords(self, coords_list):
        self._available_coords = coords_list

    def set_hover_limit(self, new_limit):
        self._limit_hover = new_limit

    def draw(self, screen):
        self.set_hovered_coords(pygame.mouse.get_pos())

        if self._selected_coords:
            screen.blit(self._selected_overlay, coords_to_screen_pos(self._selected_coords, self._board_position, self.square_size))

        if self._available_coords:
            for coords in self._available_coords:
                screen.blit(self._available_overlay, coords_to_screen_pos(coords, self._board_position, self.square_size))

        if self._hovered_coords:
            if self._hovered_coords is None:
                return

            if self._limit_hover and ((self._available_coords is None) or (self._hovered_coords not in self._available_coords)):
                return

            screen.blit(self._hovered_overlay, coords_to_screen_pos(self._hovered_coords, self._board_position, self.square_size))

    def handle_resize(self, board_position, board_size):
        self._board_position = board_position
        self._board_size = board_size

        self.initialise_overlay_surfaces()