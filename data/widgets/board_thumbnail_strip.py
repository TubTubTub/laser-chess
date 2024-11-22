import pygame
from data.widgets.bases import _Widget
from data.widgets.board_thumbnail import BoardThumbnail

class BoardThumbnailStrip(_Widget):
    def __init__(self, relative_position, board_width, fen_string_list, gap=20):
        super().__init__()
        self._screen_size = pygame.display.get_surface().get_size()
        
        self._relative_position = relative_position
        self._relative_board_width = board_width / self._screen_size[1]
        self._relative_gap = gap / self._screen_size[1]

        self.initialise_fen_string_list(fen_string_list)

    @property
    def _position(self):
        return (self._relative_position[0] * self._screen_size[0], self._relative_position[1] * self._screen_size[1])

    @property
    def _size(self):
        return (self._relative_size[0] * self._screen_size[1], self._relative_size[1] * self._screen_size[1])

    @property
    def _board_width(self):
        return self._relative_board_width * self._screen_size[1]
    
    @property
    def _gap(self):
        return self._relative_gap * self._screen_size[1]
    
    def initialise_fen_string_list(self, fen_string_list):
        if len(fen_string_list) == 0:
            self._relative_size = (0, 0)
            self._image_copy = pygame.Surface((0, 0))
            self.set_image()
            self.set_geometry()
            return

        width = len(fen_string_list) * (self._board_width + self._gap) - self._gap

        self._relative_size = (width / self._screen_size[1], self._board_width * 0.8)

        strip_surface = pygame.Surface(self._size)

        for index, fen_string in enumerate(fen_string_list):
            board_thumbnail = BoardThumbnail(relative_position=(0, 0), width=self._board_width, fen_string=fen_string)
            strip_surface.blit(board_thumbnail.image, (index * (self._board_width + self._gap), 0))
        
        self._image_copy = strip_surface.copy()

        self.set_image()
        self.set_geometry()
    
    def set_image(self):
        self.image = pygame.transform.smoothscale(self._image_copy, self._size)
    
    def set_geometry(self):
        self.rect = self.image.get_rect()
        self.rect.topleft = self._position
    
    def set_screen_size(self, new_screen_size):
        self._screen_size = new_screen_size
    
    def process_event(self, event):
        pass