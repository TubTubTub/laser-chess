import pygame
from data.components.constants import EMPTY_BB

class CustomSpriteGroup(pygame.sprite.Group):
    def __init__(self):
        self.square_list = []
        self.valid_square_list_positions = []
        pygame.sprite.Group.__init__(self)
    
    def handle_resize(self, new_size, new_position):
        for sprite in self.sprites():
            sprite.handle_resize(new_size, new_position)
    
    def handle_resize_end(self):
        for sprite in self.sprites():
            sprite.handle_resize_end()
    
    def update_squares_move(self, src, dest, new_piece_symbol, new_colour):
        self.square_list[src].clear_piece()
        self.square_list[dest].clear_piece()
        self.square_list[dest].set_colour(new_colour)
        self.square_list[dest].set_piece(new_piece_symbol)
    
    def add_valid_square_overlays(self, valid_bitboard):
        if valid_bitboard == EMPTY_BB:
            return

        list_positions = self.bitboard_to_list_positions(valid_bitboard)
        self.valid_square_list_positions = list_positions

        for square_position in list_positions:
            square = self.square_list[square_position]
            square.selected = True
    
    def remove_valid_square_overlays(self):
        for square_position in self.valid_square_list_positions:
            square = self.square_list[square_position]
            square.selected = False
            square.remove_overlay()

        self.valid_square_list_positions = []
    
    def draw_valid_square_overlays(self):
        for square_position in self.valid_square_list_positions:
            square = self.square_list[square_position]
            square.draw_overlay()

    def bitboard_to_list_positions(self, bitboard):
        list_positions = []
        while (bitboard != EMPTY_BB):
            lsb = bitboard & -bitboard
            bitboard = bitboard ^ lsb

            list_positions.append(lsb.bit_length() - 1)
        
        return list_positions