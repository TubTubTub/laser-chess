import pygame
from data.widgets.bases.widget import _Widget
from data.states.game.components.piece_sprite import PieceSprite
from data.constants import Score, Rotation, WidgetState, Colour, BLUE_BUTTON_COLOURS, RED_BUTTON_COLOURS
from data.utils.widget_helpers import create_text_box
from data.utils.asset_helpers import scale_and_cache

class PieceDisplay(_Widget):
    def __init__(self, active_colour, **kwargs):
        super().__init__(**kwargs)
        
        self._active_colour = active_colour
        self._piece_list = []
        self._piece_surface = None
        self._box_colours = BLUE_BUTTON_COLOURS[WidgetState.BASE] if active_colour == Colour.BLUE else RED_BUTTON_COLOURS[WidgetState.BASE]
        
        self.initialise_piece_surface()
        
        self.set_image()
        self.set_geometry()
    
    def add_piece(self, piece):
        self._piece_list.append(piece)
        self._piece_list.sort(key=lambda piece: Score[piece.name])
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
        piece_list = []

        for index, piece in enumerate(self._piece_list):
            piece_instance = PieceSprite(piece, self._active_colour.get_flipped_colour(), Rotation.UP)
            piece_instance.set_geometry((0, 0), piece_width)
            piece_instance.set_image()
            piece_list.append((piece_instance.image, (piece_width * index, (self._piece_surface.height - piece_width) / 2)))
        
        self._piece_surface.fblits(piece_list)
        
        self.set_image()
    
    def set_image(self):
        self.image = create_text_box(self.size, self.border_width, self._box_colours)

        resized_piece_surface = scale_and_cache(self._piece_surface, (self.size[0] - 2 * self.margin, self.size[1] - 2 * self.margin))
        self.image.blit(resized_piece_surface, (self.margin, self.margin))
        
    def process_event(self, event):
        pass