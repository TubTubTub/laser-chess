import pygame
from data.components.widgets.bases import _Pressable, _Widget
from data.constants import WidgetState

class SliderThumb(_Pressable):
    def __init__(self, radius, colour, border_width=12, border_colour=(255, 255, 255)):
        super().__init__(
            down_func=lambda: self.down_func(),
            up_func=lambda: self.up_func(),
            hover_func=lambda: None
        )
        self._screen = pygame.display.get_surface()
        self._colour = colour
        self._radius = radius
        self._center = None

        r, g, b = self._colour
        self._hover_colour = (max(r - 25, 0), max(g - 25, 0), max(b - 25, 0))
        self._press_colour = (max(r - 50, 0), max(g - 50, 0), max(b - 50, 0))
        self._colour_copy = self._colour

        self._thumb_surface = pygame.Surface((self._radius * 2, self._radius * 2))
        pygame.draw.circle(self._thumb_surface, colour, (self._radius, self._radius), self._radius, width=border_width)

        self.rect = self._thumb_surface.get_rect()
    
    def set_center(self, position):
        self._center = position
    
    def set_radius(self, radius):
        self._radius = radius
    
    def draw(self):
        rect = pygame.Rect(0, 0, self._radius, self._radius)
        rect.center = self._center
        test = pygame.Surface((50, 50))
        test.fill((255, 0, 0))
        self._screen.blit(test, (0, 0))
        print('sd')
    
    def down_func(self):
        self.set_state_colour(WidgetState.PRESS)
    
    def up_func(self):
        self.set_state_colour(WidgetState.DEFAULT)
    
    def set_colour(self, colour):
        self._colour = colour
    
    def set_state_colour(self, state):
        if self._fill_colour is None:
            return

        match state:
            case WidgetState.DEFAULT:
                self._fill_colour = self._colour_copy
            case WidgetState.HOVER:
                self._fill_colour = self._hover_colour
            case WidgetState.PRESS:
                self._fill_colour = self._press_colour

    def get_surface(self):
        return self._thumb_surface