import pygame
from data.widgets.bases import _Widget, _Pressable
from data.constants import WidgetState

class ColourButton(_Pressable, _Widget):
    def __init__(self, relative_position, relative_size, event, default_colour=(255, 255, 255), border_width=5, border_colour=(255, 255, 255)):
        _Pressable.__init__(
            self,
            event=event,
            hover_func=lambda: self.set_state_colour(WidgetState.HOVER),
            down_func=lambda: self.set_state_colour(WidgetState.PRESS),
            up_func=lambda: self.set_state_colour(WidgetState.BASE),
            play_sfx=False
        )
        _Widget.__init__(self)

        self._relative_position = relative_position
        self._relative_size = relative_size
        self._relative_border_width = border_width / self._surface_size[1]

        self._fill_colour = default_colour
        self._border_colour = border_colour

        self._empty_surface = pygame.Surface(self._size)

        self.initialise_new_colours(default_colour)

        self.set_image()
        self.set_geometry()
    
    @property
    def _size(self):
        return (self._relative_size[0] * self._surface_size[1], self._relative_size[1] * self._surface_size[1])
    
    @property
    def _position(self):
        return (self._relative_position[0] * self._surface_size[0], self._relative_position[1] * self._surface_size[1])

    @property
    def _border_width(self):
        return self._relative_border_width * self._surface_size[1]

    def initialise_new_colours(self, new_colour):
        r, g, b = pygame.Color(new_colour).rgb

        self._colours = {
            WidgetState.BASE: new_colour,
            WidgetState.HOVER: (max(r - 25, 0), max(g - 25, 0), max(b - 25, 0)),
            WidgetState.PRESS: (max(r - 50, 0), max(g - 50, 0), max(b - 50, 0))
        }

        self.set_state_colour(WidgetState.BASE)
    
    def set_state_colour(self, state):
        self._fill_colour = self._colours[state]

        self.set_image()

    def set_surface_size(self, new_surface_size):
        self._surface_size = new_surface_size

    def set_image(self):
        self.image = pygame.transform.scale(self._empty_surface, self._size)
        self.image.fill(self._fill_colour)
        pygame.draw.rect(self.image, self._border_colour, (0, 0, self._size[0], self._size[1]), width=int(self._border_width))
    
    def set_geometry(self):
        self.rect = self.image.get_rect()
        self.rect.topleft = self._position