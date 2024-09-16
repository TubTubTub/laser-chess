import pygame
from data.constants import EMPTY_BB, Colour
from data.components.piecesprite import EmptyPiece, create_piece
from data.utils import bitboard_helpers as bb_helpers

class PieceGroup(pygame.sprite.LayeredUpdates):
    def __init__(self, piece_list, board_position, board_size):
        # self.square_list = []
        # self.valid_square_list_positions = []
        super().__init__()
        self.initialise_pieces(piece_list)
        self.set_geometry(board_position, board_size)

    def initialise_pieces(self, piece_list):
        for index, piece_symbol in enumerate(piece_list):
            x = index % 10
            y = index // 10

            if piece_symbol:
                if piece_symbol.isupper():
                    colour = Colour.BLUE
                else:
                    colour = Colour.RED

                piece = create_piece(piece=piece_symbol, coords=(x, y), size=48, colour=colour)
                self.add(piece)
            else:
                self.add(EmptyPiece())
    
    def set_geometry(self, board_position, board_size):
        for sprite in self.sprites():
            sprite.anchor_position = board_position
            sprite.size = board_size[0] / 10
    
    def handle_resize(self, board_position, board_size):
        self.set_geometry(board_position, board_size)

        for sprite in self.sprites():
            sprite.set_image('low')
            sprite.set_rect()
    
    # def handle_resize_end(self):
    #     for sprite in self.sprites():
    #         sprite.handle_resize_end()

    # def clear_square(self, src_bitboard):
    #     list_position = bb_helpers.bitboard_to_index(src_bitboard)
    #     self.square_list[list_position].clear_piece()
    
    # def update_squares_move(self, src, dest, new_piece_symbol, new_colour, rotation):
    #     self.square_list[src].clear_piece()
    #     self.square_list[dest].clear_piece()
    #     self.square_list[dest].set_piece(piece_symbol=new_piece_symbol, colour=new_colour, rotation=rotation)
    
    # def update_squares_rotate(self, src, piece_symbol, colour, new_rotation):
    #     self.square_list[src].clear_piece()
    #     self.square_list[src].set_piece(piece_symbol=piece_symbol, colour=colour, rotation=new_rotation)
    
    # def add_valid_square_overlays(self, valid_bitboard):
    #     if valid_bitboard == EMPTY_BB:
    #         return

    #     list_positions = self.bitboard_to_list_positions(valid_bitboard)
    #     self.valid_square_list_positions = list_positions

    #     for square_position in list_positions:
    #         square = self.square_list[square_position]
    #         square.selected = True
    
    # def remove_valid_square_overlays(self):
    #     for square_position in self.valid_square_list_positions:
    #         square = self.square_list[square_position]
    #         square.selected = False
    #         square.remove_overlay()

    #     self.valid_square_list_positions = []
    
    # def draw_valid_square_overlays(self):
    #     for square_position in self.valid_square_list_positions:
    #         square = self.square_list[square_position]
    #         square.draw_overlay()

    # def bitboard_to_list_positions(self, bitboard):
    #     list_positions = []

    #     for square in bb_helpers.occupied_squares(bitboard):
    #         list_positions.append(bb_helpers.bitboard_to_index(square))
        
    #     return list_positions