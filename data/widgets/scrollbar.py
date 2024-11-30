import pygame
from data.widgets.bases import _Widget, _Pressable
from data.constants import WidgetState, Miscellaneous
# self.set_state_colour(WidgetState.HOVER)
class _Scrollbar(_Pressable, _Widget):
    def __init__(self, position, size, vertical, fill_colour=(255, 255, 255), surface=None):
        _Pressable.__init__(
            self,
            event=Miscellaneous.PLACEHOLDER,
            hover_func=lambda: self.set_state_colour(WidgetState.HOVER),
            down_func=self.down_func,
            up_func=self.up_func,
            prolonged=True,
            play_sfx=False
        )
        _Widget.__init__(self, surface)

        self._position = position
        self._size = size

        self._fill_colour = fill_colour

        self._vertical = vertical
        self._last_mouse_px = None

        self._empty_surface = pygame.Surface(self._size, pygame.SRCALPHA)

        self.initialise_new_colours(fill_colour)

        self.set_image()
        self.set_geometry()

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
    
    def down_func(self):
        if self._vertical:
            self._last_mouse_px = pygame.mouse.get_pos()[1]
        else:
            self._last_mouse_px = pygame.mouse.get_pos()[0]

        self.set_state_colour(WidgetState.PRESS)
    
    def up_func(self):
        self._last_mouse_px = None
        self.set_state_colour(WidgetState.BASE)
    
    def set_position(self, starting_position):
        self._position = starting_position
        self.set_geometry()
    
    def set_size(self, new_size):
        self._size = new_size

    def set_image(self):
        self.image = pygame.transform.scale(self._empty_surface, self._size)

        if self._vertical:
            rounded_radius = self._size[0] / 2
        else:
            rounded_radius = self._size[1] / 2

        pygame.draw.rect(self.image, self._fill_colour, (0, 0, self._size[0], self._size[1]), border_radius=int(rounded_radius))
    
    def set_geometry(self):
        self.rect = self.image.get_rect()
        self.rect.topleft = self._position
    
    def process_event(self, event):
        before_state = self.get_widget_state()
        widget_event = super().process_event(event)
        after_state = self.get_widget_state()

        if event.type == pygame.MOUSEMOTION and self._last_mouse_px:
            if self._vertical:
                offset_from_last_frame = event.pos[1] - self._last_mouse_px
                self._last_mouse_px = event.pos[1]

                return offset_from_last_frame
            else:
                offset_from_last_frame = event.pos[0] - self._last_mouse_px
                self._last_mouse_px = event.pos[0]

                return offset_from_last_frame


        if widget_event or before_state != after_state:
            return 0