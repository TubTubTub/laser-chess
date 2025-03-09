import pygame
from data.states.game.components.piece_sprite import PieceSprite
from data.utils.enums import Colour, Piece

class PieceGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def initialise_pieces(self, piece_list, board_position, board_size):
        self.empty()

        for index, piece_and_rotation in enumerate(piece_list):
            x = index % 10
            y = index // 10

            if piece_and_rotation:
                if piece_and_rotation[0].isupper():
                    colour = Colour.BLUE
                else:
                    colour = Colour.RED

                piece = PieceSprite(piece=Piece(piece_and_rotation[0].lower()), colour=colour, rotation=piece_and_rotation[1])
                piece.set_coords((x, y))
                piece.set_geometry(board_position, board_size[0] / 10)
                piece.set_image()
                self.add(piece)

    def set_geometry(self, board_position, board_size):
        for sprite in self.sprites():
            sprite.set_geometry(board_position, board_size[0] / 10)

    def handle_resize(self, board_position, board_size):
        self.set_geometry(board_position, board_size)

        for sprite in self.sprites():
            sprite.set_image()

    def remove_piece(self, coords):
        for sprite in self.sprites():
            if sprite.coords == coords:
                sprite.kill()