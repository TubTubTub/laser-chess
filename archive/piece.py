import pygame
from data.components.piecesprite import create_piece_images
from data.tools import smoothscale_and_cache
from data.constants import STARTING_SQUARE_SIZE, ImageType

class Piece(pygame.sprite.Sprite):
    '''self.drawing_index: Since the initialization loop starts drawing index(0, 0) from the top of the screen, and
    we want index (0, 0) to be drawn at the bottom-left corner, we will have to create a new index where the y-position
    is flipped so that the bottom-left square corresponds to index (0, 0)

    self._size: Added 1 to original desired size to prevent flickering when updating screen size
    
    self._high_quality_svg_layer: Have to manually draw high resolution svg on self.image each type, as cannot scale self._high_quality_svg_layer directly because that will rasterize the svg and lose its vector quality
    '''
    def __init__(self, piece_symbol, coords):
        pygame.sprite.Sprite.__init__(self)
        self._coords = coords
        self._piece_images = create_piece_images(piece_symbol, )
        self._size = size
        self._board_colour = board_colour
        self._colour = None
        self._rotation = None

        self._empty_layer = pygame.Surface((self._size, self._size))
        self._empty_layer.fill(self._board_colour)
        self._low_res_layer = None
        self._high_res_layer = None
        self._high_res_icon = None
        self._low_res_icon = None

        self.selected = False

        self.image = self._empty_layer.copy()
        self.rect = self.image.get_rect()
        self.rect.topleft = self.calculate_rect_position(size, anchor_position)

        # self._outline = pygame.Surface((self._size + 1, self._size + 1), pygame.SRCALPHA)
        # self._outline.fill((255, 0, 0, 128))
    
    # def to_bitboard(self):
    #     list_position = self._index[0] + self._index[1] * 10
    #     return (1 << list_position)
    
    # def to_list_position(self):
    #     list_position = self._index[0] + self._index[1] * 10
    #     return (list_position)

    def calculate_rect_position(self, size, anchor_position):
        return (self._index[0] * size + anchor_position[0], anchor_position[1] - size * (self._index[1] + 1))
    
    def initialize_piece_icons(self, piece):
        self._high_res_icon = pygame.transform.rotate(piece.high_res_svg, self._rotation.to_angle())
        self._low_res_icon = pygame.transform.rotate(piece.low_res_png, self._rotation.to_angle())
        self._low_res_icon = pygame.transform.scale(self._low_res_icon, (self._size, self._size))

        self._high_res_layer = self._empty_layer.copy()

        self._low_res_layer = self._empty_layer.copy()
        self._low_res_layer.blit(self._low_res_icon, (0, 0))

        self.set_square_image('high')
    
    # def handle_resize(self, new_size, new_position):
    #     self._size = new_size

    #     if self.piece is None:
    #         self.set_square_image('empty')
    #     else:
    #         self.set_square_image('low')
        
    #     if self.selected:
    #         self.draw_overlay()

    #     self.rect = self.image.get_rect()
    #     self.rect.topleft = self.calculate_rect_position(new_size, new_position)
    
    # def handle_resize_end(self):
    #     if self.piece:
    #         self.set_square_image('high')
    #     else:
    #         self.set_square_image('empty')
        
    #     if self.selected is True:
    #         self.draw_overlay()
    
    def set_square_image(self, type):
        match (type):
            case ImageType.LOW_RES_PIECE:
                self.image = pygame.transform.smoothscale(self._low_res_layer, (self._size + 1, self._size + 1))
                return

            case ImageType.EMPTY_PIECE:
                self.image = pygame.transform.scale(self._empty_layer, (self._size + 1, self._size + 1))
                return

            case ImageType.HIGH_RES_PIECE:
                self.image = pygame.transform.scale(self._high_res_layer, (self._size + 1, self._size + 1))
                piece_layer = smoothscale_and_cache(self._high_res_icon, (self._size + 1, self._size + 1))
                self.image.blit(piece_layer, (0, 0))
                return
                
            case _:
                raise ValueError('Invalid type provided for square image')
    
    # def draw_overlay(self):
    #     self.image.blit(pygame.transform.scale(self._outline, (self._size + 1, self._size + 1)), (0, 0))
    
    # def remove_overlay(self):
    #     if (self.piece):
    #         self.set_square_image('high')
    #     else:
    #         self.set_square_image('empty')
    
    def set_piece(self, piece_symbol, colour, rotation):
        self.piece = piece_symbol
        self._colour = colour
        self._rotation = rotation

        piece = create_piece(piece_symbol, self._size, self._colour)
    
    # def clear_piece(self):
    #     self.piece = None
    #     self.image = pygame.Surface((self._size, self._size))
    #     self.image.fill(self._board_colour)
    
    # def has_piece(self):
    #     return (self.piece is not None)