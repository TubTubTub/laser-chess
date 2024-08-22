import pygame
from data.components.piece import create_piece
from data.tools import scale_and_cache

class Square(pygame.sprite.Sprite):
    '''self.drawing_index: Since the initialization loop starts drawing index(0, 0) from the top of the screen, and
    we want index (0, 0) to be drawn at the bottom-left corner, we will have to create a new index where the y-position
    is flipped so that the bottom-left square corresponds to index (0, 0)

    self._size: Added 1 to original desired size to prevent flickering when updating screen size
    
    self._high_quality_svg_layer: Have to manually draw high resolution svg on self.image each type, as cannot scale self._high_quality_svg_layer directly because that will rasterize the svg and lose its vector quality
    '''
    def __init__(self, index, size, board_colour, anchor_position):
        pygame.sprite.Sprite.__init__(self)
        self._index = index
        self._size = size
        self._board_colour = board_colour
        self._colour = None
        self._piece = None

        self.selected = False

        self.image = pygame.Surface((self._size, self._size))
        self.image.fill(self._board_colour)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.calculate_rect_position(size, anchor_position)

        self._outline = pygame.Surface((self._size + 1, self._size + 1), pygame.SRCALPHA)
        self._outline.fill((255, 0, 0, 128))
    
    @classmethod
    def instance_from_position(square_class, r, f):
        return square_class(r * 10 + f)

    def calculate_rect_position(self, size, anchor_position):
        return (self._index[0] * size + anchor_position[0], anchor_position[1] - size * (self._index[1] + 1))
    
    def update(self, new_size, new_position):
        if self._piece is not None:
            self.draw_low_res_png(new_size)
        else:
            self.draw_resized_square(new_size)
        
        if self.selected:
            self.draw_overlay()

        self.rect = self.image.get_rect()
        self.rect.topleft = self.calculate_rect_position(new_size, new_position)

        self._size = new_size
    
    def draw_resized_square(self, size):
        self.image = pygame.transform.scale(self.image, (size + 1, size + 1))
    
    def draw_high_res_svg(self):
        if self._piece is not None:
            self.image = pygame.transform.scale(self._high_res_svg_layer, (self._size + 1, self._size + 1))
            piece_layer = pygame.transform.scale(self._high_res_svg, (self._size + 1, self._size + 1))
            self.image.blit(piece_layer, (0, 0))
    
    def draw_low_res_png(self, size):
        self.image = scale_and_cache(self._low_res_png_layer, (size + 1, size + 1))
    
    def draw_overlay(self):
        self.image.blit(pygame.transform.scale(self._outline, (self._size + 1, self._size + 1)), (0, 0))
    
    def remove_overlay(self):
        self.draw_high_res_svg()
    
    def to_bitboard(self):
        list_position = self._index[0] + self._index[1] * 10
        return (1 << list_position)
    
    def to_list_position(self):
        list_position = self._index[0] + self._index[1] * 10
        return (list_position)

    def set_colour(self, colour):
        self._colour = colour
    
    def set_piece(self, piece_symbol):
        piece = create_piece(piece_symbol, self._size, self._colour)
        self._piece = piece

        self.initialize_draw_layers()
    
    def initialize_draw_layers(self):
        self._high_res_svg = self._piece.high_res_svg
        self._low_res_png = self._piece.low_res_png

        self._high_res_svg_layer = pygame.Surface((self._size, self._size))
        self._high_res_svg_layer.fill(self._board_colour)

        self._low_res_png_layer = pygame.Surface((self._size, self._size))
        self._low_res_png_layer.fill(self._board_colour)
        self._low_res_png_layer.blit(pygame.transform.scale(self._piece.low_res_png, (self._size, self._size)), (0, 0))

        self.draw_high_res_svg()
    
    def clear_piece(self):
        self._piece = None
        self.image = pygame.Surface((self._size, self._size))
        self.image.fill(self._board_colour)