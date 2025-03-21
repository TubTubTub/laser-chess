import pygame
from data.helpers.font_helpers import text_width_to_font_size
from data.helpers.browser_helpers import get_winner_string
from data.widgets.board_thumbnail import BoardThumbnail
from data.helpers.asset_helpers import scale_and_cache
from data.widgets.bases.widget import _Widget

FONT_DIVISION = 7

class BrowserItem(_Widget):
    def __init__(self, relative_width, game, **kwargs):
        super().__init__(relative_size=(relative_width, relative_width * 2), scale_mode='height', **kwargs)

        self._relative_font_size = text_width_to_font_size('YYYY-MM-DD HH:MM:SS', self._font, self.size[0]) / self.surface_size[1]

        self._game = game
        self._board_thumbnail = BoardThumbnail(
            relative_position=(0, 0),
            scale_mode='height',
            relative_width=relative_width,
            fen_string=self._game['final_fen_string']
        )

        self.set_image()
        self.set_geometry()

    def get_text_to_render(self):
        depth_to_text = {
            2: 'EASY',
            3: 'MEDIUM',
            4: 'HARD'
        }

        format_moves = lambda no_of_moves:  int(no_of_moves / 2) if (no_of_moves / 2 % 1 == 0) else round(no_of_moves / 2, 1)

        if self._game['cpu_enabled'] == 1:
            depth_text = depth_to_text[self._game['cpu_depth']]
            cpu_text = f'PVC ({depth_text})'
        else:
            cpu_text = 'PVP'

        return [
            cpu_text,
            self._game['created_dt'].strftime('%Y-%m-%d %H:%M:%S'),
            f'WINNER: {get_winner_string(self._game['winner'])}',
            f'NO. MOVES: {format_moves(self._game['number_of_ply'])}'
        ]

    def set_image(self):
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        resized_board = scale_and_cache(self._board_thumbnail.image, (self.size[0], self.size[0] * 0.8))
        self.image.blit(resized_board, (0, 0))

        get_line_y = lambda line: (self.size[0] * 0.8) + ((self.size[0] * 0.8) / FONT_DIVISION) * (line + 0.5)

        text_to_render = self.get_text_to_render()

        for index, text in enumerate(text_to_render):
            self._font.render_to(self.image, (0, get_line_y(index)), text, fgcolor=self._text_colour, size=self.font_size)

    def process_event(self, event):
        pass