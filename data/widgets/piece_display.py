import pygame
from data.widgets.bases import _Widget
from data.states.game.components.piece_sprite import create_piece
from data.constants import PieceScore

class PieceDisplay(_Widget):
    def __init__(self, active_colour, **kwargs):
        super().__init__(**kwargs)
        
        self._active_colour = active_colour
        self._piece_list = []
        self._piece_surface = None
        
        self.initialise_piece_surface()
        
        self.set_image()
        self.set_geometry()
    
    def add_piece(self, piece):
        self._piece_list.append(piece)
        self._piece_list.sort(key=lambda piece: PieceScore[piece.name])
        self.initialise_piece_surface()
    
    def remove_piece(self, piece):
        self._piece_list.remove(piece)
        self.initialise_piece_surface()
    
    def reset_piece_list(self):
        self._piece_list = []
        self.initialise_piece_surface()
        
    def initialise_piece_surface(self):
        self._piece_surface = pygame.Surface((self.size[0] - 2 * self.margin, self.size[1] - 2 * self.margin), pygame.SRCALPHA)

        if (len(self._piece_list) == 0):
            self.set_image()
            return

        piece_width = min(self.size[1] - 2 * self.margin, (self.size[0] - 2 * self.margin) / len(self._piece_list))

        for index, piece in enumerate(self._piece_list):
            piece_instance = create_piece(piece, colour=self._active_colour.get_flipped_colour(), coords=None)
            piece_image = pygame.transform.smoothscale(piece_instance.high_res_img, (piece_width, piece_width))
            self._piece_surface.blit(piece_image, (piece_width * index, (self._piece_surface.height - piece_width) / 2))
        
        self.set_image()
    
    def set_image(self):
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)

        pygame.draw.rect(self.image, self._fill_colour, (0, 0, *self.size), border_radius=int(self.border_radius))
        if self.border_width:
            pygame.draw.rect(self.image, self._border_colour, (0, 0, *self.size), width=int(self.border_width), border_radius=int(self.border_radius))

        resized_piece_surface = pygame.transform.smoothscale(self._piece_surface, (self.size[0] - 2 * self.margin, self.size[1] - 2 * self.margin))
        self.image.blit(resized_piece_surface, (self.margin, self.margin))
        
    def process_event(self, event):
        pass