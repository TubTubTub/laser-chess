import pygame
from data.widgets.bases import _Widget
from data.widgets.chessboard import Chessboard
from data.states.game.components.piece_group import PieceGroup
from data.states.game.components.bitboard_collection import BitboardCollection

class BoardThumbnail(_Widget):
    def __init__(self, relative_position, relative_width, fen_string='', **kwargs):
        super().__init__(**kwargs)
        self._relative_position = relative_position
        self._relative_size = (relative_width, relative_width * 0.8)

        self._board = Chessboard(relative_position, relative_width)

        self._empty_surface = pygame.Surface((0, 0))

        self.initialise_fen_string(fen_string)
        
        self.set_image()
        self.set_geometry()

    @property
    def position(self):
        return (self._relative_position[0] * self._surface_size[0], self._relative_position[1] * self._surface_size[1])

    @property
    def size(self):
        return (self._relative_size[0] * self._surface_size[1], self._relative_size[1] * self._surface_size[1])

    def initialise_fen_string(self, fen_string):
        if len(fen_string) == 0:
            piece_list = []
        else:
            piece_list = BitboardCollection(fen_string).convert_to_piece_list()

        self._piece_group = PieceGroup()
        self._piece_group.initialise_pieces(piece_list, (0, 0), self.size)
        
        self.set_image()
    
    def set_image(self):
        self.image = pygame.transform.scale(self._empty_surface, self.size)
        
        self._board.set_image()
        self.image.blit(self._board.image, (0, 0))

        self._piece_group.draw(self.image)
    
    def set_geometry(self):
        self.rect = self.image.get_rect()
        self.rect.topleft = self.position
        self._board.set_geometry()
    
    def set_surface_size(self, new_surface_size):
        self._surface_size = new_surface_size
        self._board.set_surface_size(new_surface_size)
        self._piece_group.handle_resize((0, 0), self.size, resize_end=False) # ONLY RENDERS PIECES IN LOW QUALITY
    
    def process_event(self, event):
        pass