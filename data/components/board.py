import pygame
from data.settings import app_settings
from data.components.cursor import Cursor
from data.components.piece import Sphinx
from data.tools import scale_and_cache

class Board:
    def __init__(self, screen):
        self.game_settings = app_settings
        self.screen = screen
        self.cursor = Cursor()

        self._board_size = self.calculate_board_size(self.screen)
        self._board_origin_position = self.calculate_board_position(self.screen, self._board_size)
        self._square_size = self._board_size[0] / 10
        self._square_group = self.initialize_square_group()

        self._selected_square_object = None

    def initialize_square_group(self):
        square_group = pygame.sprite.Group()

        for i in range(80):
            x = i % 10
            y = i // 10

            if (x + y) % 2 == 0:
                square = Square(index=(x,y), size=self._square_size, colour=(self.game_settings.primaryBoardColour), position=self._board_origin_position)
            else:
                square = Square(index=(x,y), size=self._square_size, colour=(self.game_settings.secondaryBoardColour), position=self._board_origin_position)

            square_group.add(square)

        return square_group

    def draw_board(self):
        self.cursor.update()

        self._square_group.draw(self.screen)

    def resize_board(self):
        self._board_size = self.calculate_board_size(self.screen)
        self._board_origin_position = self.calculate_board_position(self.screen, self._board_size)
        self._square_size = self._board_size[0] / 10
        self._square_group.update(new_size=self._square_size, new_position=self._board_origin_position)

    def calculate_board_size(self, screen):
        '''Returns board size based on screen parameter'''
        screen_width, screen_height = screen.get_size()

        target_height = screen_height * 0.64
        target_width = target_height / 0.8

        return (target_width, target_height)

    def calculate_board_position(self, screen, board_size):
        '''Returns required board starting position to draw on center of the screen'''
        screen_x, screen_y = screen.get_size()
        board_x, board_y = board_size

        x = screen_x / 2 - (board_x / 2)
        y = screen_y / 2 - (board_y / 2)

        return (x, y)

    def process_mouse_press(self, event):
        current_square_selected = self.cursor.select(event.pos, self._square_group)

        if (current_square_selected):
            if (self._selected_square_object):
                self._selected_square_object.selected = False
            
            self._selected_square_object = current_square_selected
            self._selected_square_object.selected = True
        
        print(current_square_selected)

class Square(pygame.sprite.Sprite):
    '''self.drawing_index: Since the initialization loop starts drawing index(0, 0) from the top of the screen, and
    we want index (0, 0) to be drawn at the bottom-left corner, we will have to create a new index where the y-position
    is flipped so that the bottom-left square corresponds to index (0, 0)
    self._size: Added 1 to original desired size to prevent flickering when updating screen size'''
    def __init__(self, index, size, colour, position):
        pygame.sprite.Sprite.__init__(self)
        self._index = index
        self._drawing_index = (index[0], 7 - index[1])
        self._size = size
        self._colour = colour

        self.selected = False
        self.piece = Sphinx()

        self.image = pygame.Surface((self._size, self._size))
        self.image.fill(colour)
        self.image_copy =  self.image.copy()
        self.rect = self.image.get_rect()
        self.rect.topleft = (self._drawing_index[0] * self._size + position[0], self._drawing_index[1] * self._size + position[1])
        self.image.blit(self.piece.image, (0, 0))

        self._outline = pygame.Surface((self._size + 1, self._size + 1), pygame.SRCALPHA)
        self._outline.fill((255, 0, 0, 128))
    
    def update(self, new_size, new_position):
        self._size = new_size

        self.image = scale_and_cache(self.image_copy, (new_size + 1, new_size + 1))
        self.rect.topleft = (self._drawing_index[0] * self._size + new_position[0], self._drawing_index[1] * self._size + new_position[1])

        self.piece.update(size=new_size)

        self.image.fill(self._colour)
        self.image.blit(self.piece.image, (0, 0))