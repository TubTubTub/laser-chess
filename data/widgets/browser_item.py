import pygame
from data.widgets.bases import _Widget
from data.assets import FONTS, GRAPHICS
from data.utils.font_helpers import height_to_font_size
from data.widgets.board_thumbnail import BoardThumbnail
from data.widgets.icon_button import IconButton
from data.constants import Colour
from data.constants import Miscellaneous

FONT_DIVISION = 7

def get_winner_string(winner):
    if winner is None:
        return 'UNFINISHED'
    elif winner == Miscellaneous.DRAW:
        return 'DRAW'
    else:
        return Colour(winner).name

class BrowserItem(_Widget):
    def __init__(self, relative_position, game, width, text_colour=(100, 100, 100), font=FONTS['default']):
        super().__init__()
        self._screen_size = pygame.display.get_surface().get_size()

        self._font = font

        self._relative_position = relative_position
        self._relative_width = width / self._screen_size[1]
        
        line_height = (self._size[1] / 2) / FONT_DIVISION
        self._relative_font_size = height_to_font_size(self._font, line_height) / self._screen_size[1]

        self._text_colour = text_colour
        self._game = game
        self._board_thumbnail = BoardThumbnail(relative_position=(0, 0), width=self._size[0], fen_string=self._game['fen_string'])
        
        self._empty_surface = pygame.Surface((0, 0))
        
        self.set_image()
        self.set_geometry()

    @property
    def _position(self):
        return (self._relative_position[0] * self._screen_size[0], self._relative_position[1] * self._screen_size[1])
    
    @property
    def _size(self):
        return (self._relative_width * self._screen_size[1], self._relative_width * 2 * 0.8 * self._screen_size[1])

    @property
    def _font_size(self):
        return self._relative_font_size * self._screen_size[1]
    
    def set_image(self):
        self.image = pygame.Surface(self._size)
        resized_board = pygame.transform.smoothscale(self._board_thumbnail.image, (self._size[0], self._size[0] * 0.8))
        self.image.blit(resized_board, (0, 0))

        get_line_y = lambda line: (self._size[0] * 0.8) + ((self._size[0] * 0.8) / FONT_DIVISION) * line
        self._font.render_to(self.image, (0, get_line_y(0)), f'WINNER: {get_winner_string(self._game['winner'])}', fgcolor=self._text_colour, size=self._font_size)
        self._font.render_to(self.image, (0, get_line_y(1)), f'NO. MOVES: {int(self._game['number_of_ply'] / 2)}', fgcolor=self._text_colour, size=self._font_size)
    
    def set_geometry(self):
        self.rect = self.image.get_rect()
        self.rect.topleft = self._position
    
    def set_screen_size(self, new_screen_size):
        self._screen_size = new_screen_size
    
    def process_event(self, event):
        pass