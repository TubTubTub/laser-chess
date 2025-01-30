import pygame
from data.constants import ImageType, CursorMode
from data.states.game.components.piece_sprite import create_piece
from data.managers.cursor import cursor

DRAG_THRESHOLD = 500

class DragAndDrop:
    def __init__(self, board_position, board_size, change_cursor=True):
        self._board_position = board_position
        self._board_size = board_size
        self._change_cursor = change_cursor
        self._ticks_since_drag = 0

        self.dragged_sprite = None
    
    def set_dragged_piece(self, piece, colour, rotation):
        sprite = create_piece(piece=piece, colour=colour, rotation=rotation)
        sprite.set_geometry((0, 0), self._board_size[0] / 10)
        sprite.set_image(ImageType.HIGH_RES)

        self.dragged_sprite = sprite
        self._ticks_since_drag = pygame.time.get_ticks()

        if self._change_cursor:
            cursor.set_mode(CursorMode.CLOSEDHAND)
    
    def remove_dragged_piece(self):
        self.dragged_sprite = None
        time_dragged = pygame.time.get_ticks() - self._ticks_since_drag
        self._ticks_since_drag = 0

        if self._change_cursor:
            cursor.set_mode(CursorMode.OPENHAND)

        return time_dragged > DRAG_THRESHOLD
    
    def get_dragged_info(self):
        return self.dragged_sprite.type, self.dragged_sprite.colour, self.dragged_sprite.rotation
    
    def draw(self, screen):
        if self.dragged_sprite is None:
            return
        
        self.dragged_sprite.rect.center = pygame.mouse.get_pos()
        screen.blit(self.dragged_sprite.image, self.dragged_sprite.rect.topleft)
    
    def handle_resize(self, board_position, board_size):
        if self.dragged_sprite:
            self.dragged_sprite.set_geometry(board_position, board_size[0] / 10)

        self._board_position = board_position
        self._board_size = board_size