import pygame
from data.components.widgets.bases import _Widget
from data.components.widgets.colour_square import ColourSquare
from data.components.widgets.colour_slider import ColourSlider

class ColourPicker(_Widget):
    def __init__(self, relative_position, size):
        super().__init__()
        self._screen = pygame.display.get_surface()
        self._screen_size = self._screen.get_size()

        self._relative_position = relative_position
        self._relative_size = (size[0] / self._screen_size[0], size[1] / self._screen_size[1])

        self._square = ColourSquare(origin_position=(0.5, 0.5))
        # self._slider = ColourSlider(
        #     relative_position=(0.1, 0.2),
        #     size=(800, 200),
        #     border_width=12
        # )

        self.set_image()
        self.set_geometry()
    
    @property
    def _size(self):
        return (self._relative_size[0] * self._screen_size[1], self._relative_size[1] * self._screen_size[1])

    @property
    def _position(self):
        return (self._relative_position[0] * self._screen_size[0], self._relative_position[1] * self._screen_size[1])

    def set_image(self):
        self.image = pygame.Surface(self._size)
        self.image.fill((100, 100, 100))

        self.image.blit(self._square.image, self._square.rect)
        # self.image.blit(self._slider.image, self._slider.rect)
    
    def set_geometry(self):
        self.rect = self.image.get_rect()
        self.rect.topleft = self._position
    
    def set_screen_size(self, new_screen_size):
        self._screen_size = new_screen_size
    
    def process_event(self, event):
        pass
        # self._slider.process_event(event)