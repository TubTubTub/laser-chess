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
    def __init__(self, relative_position, relative_width, game, text_colour=(200, 200, 200), font=FONTS['default']):
        super().__init__()

        self._font = font

        self._relative_position = relative_position
        self._relative_width = relative_width
        
        line_height = (self.size[1] / 2) / FONT_DIVISION
        self._relative_font_size = height_to_font_size(self._font, line_height) / self._surface_size[1]

        self._text_colour = text_colour
        self._game = game
        self._board_thumbnail = BoardThumbnail(
            surface=pygame.display.get_surface(),
            relative_position=(0, 0),
            width=self.size[0],
            fen_string=self._game['fen_string']
        )
        
        self._empty_surface = pygame.Surface((0, 0))
        
        self.set_image()
        self.set_geometry()

    @property
    def position(self):
        return (self._relative_position[0] * self._surface_size[0], self._relative_position[1] * self._surface_size[1])
    
    @property
    def size(self):
        return (self._relative_width * self._surface_size[1], self._relative_width * 2 * 0.8 * self._surface_size[1])

    @property
    def _font_size(self):
        return self._relative_font_size * self._surface_size[1]
    
    def set_image(self):
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        resized_board = pygame.transform.smoothscale(self._board_thumbnail.image, (self.size[0], self.size[0] * 0.8))
        self.image.blit(resized_board, (0, 0))

        get_line_y = lambda line: (self.size[0] * 0.8) + ((self.size[0] * 0.8) / FONT_DIVISION) * line

        text_to_render = self.get_text_to_render()

        for index, text in enumerate(text_to_render):
            self._font.render_to(self.image, (0, get_line_y(index)), text, fgcolor=self._text_colour, size=self._font_size)
    
    def get_text_to_render(self):
        depth_to_text = {
            2: 'EASY',
            3: 'MEDIUM',
            4: 'HARD'
        }

        if self._game['cpu_enabled'] == 1:
            depth_text = depth_to_text[self._game['cpu_depth']]
            cpu_text = f'PVC ({depth_text})'
        else:
            cpu_text = 'PVP'
        
        return [
            cpu_text,
            self._game['created_dt'].strftime('%Y-%m-%d %H:%M:%S'),
            f'WINNER: {get_winner_string(self._game['winner'])}',
            f'NO. MOVES: {int(self._game['number_of_ply'] / 2)}'
        ]
    
    def set_geometry(self):
        self.rect = self.image.get_rect()
        self.rect.topleft = self.position
    
    def set_surface_size(self, new_surface_size):
        self._surface_size = new_surface_size
    
    def process_event(self, event):
        pass