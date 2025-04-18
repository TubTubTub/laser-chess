import pygame
from data.widgets.bases.widget import _Widget
from data.widgets.chessboard import Chessboard
from data.states.game.components.piece_group import PieceGroup
from data.states.game.components.bitboard_collection import BitboardCollection

class BoardThumbnail(_Widget):
    def __init__(self, relative_width, fen_string='', **kwargs):
        super().__init__(relative_size=(relative_width, relative_width * 0.8), **kwargs)

        self._board = Chessboard(
            parent=self._parent,
            relative_position=(0, 0),
            scale_mode=kwargs.get('scale_mode'),
            relative_width=relative_width
        )

        self._empty_surface = pygame.Surface((0, 0), pygame.SRCALPHA)

        self.initialise_board(fen_string)
        self.set_image()
        self.set_geometry()

    def initialise_board(self, fen_string):
        if len(fen_string) == 0:
            piece_list = []
        else:
            piece_list = BitboardCollection(fen_string).convert_to_piece_list()

        self._piece_group = PieceGroup()
        self._piece_group.initialise_pieces(piece_list, (0, 0), self.size)
        
        self._board.refresh_board()
        self.set_image()
    
    def set_image(self):
        self.image = pygame.transform.scale(self._empty_surface, self.size)

        self._board.set_image()
        self.image.blit(self._board.image, (0, 0))

        self._piece_group.draw(self.image)
    
    def set_geometry(self):
        super().set_geometry()
        self._board.set_geometry()
    
    def set_surface_size(self, new_surface_size):
        super().set_surface_size(new_surface_size)
        self._board.set_surface_size(new_surface_size)
        self._piece_group.handle_resize((0, 0), self.size)
    
    def process_event(self, event):
        pass