import pygame
from data.widgets.bases.widget import _Widget
from data.widgets.bases.pressable import _Pressable
from data.constants import WidgetState, Miscellaneous

# self.set_state_colour(WidgetState.HOVER)
class _Scrollbar(_Pressable, _Widget):
    def __init__(self, vertical, **kwargs):
        _Pressable.__init__(
            self,
            event=Miscellaneous.PLACEHOLDER,
            hover_func=lambda: self.set_state_colour(WidgetState.HOVER),
            down_func=self.down_func,
            up_func=self.up_func,
            prolonged=True,
            sfx=None
        )
        _Widget.__init__(self, **kwargs)

        self._vertical = vertical
        self._last_mouse_px = None

        self._empty_surface = pygame.Surface(self.size, pygame.SRCALPHA)
        
        self.initialise_new_colours(self._fill_colour)
        self.set_state_colour(WidgetState.BASE)

        self.set_image()
        self.set_geometry()
    
    def down_func(self):
        if self._vertical:
            self._last_mouse_px = pygame.mouse.get_pos()[1]
        else:
            self._last_mouse_px = pygame.mouse.get_pos()[0]

        self.set_state_colour(WidgetState.PRESS)
    
    def up_func(self):
        self._last_mouse_px = None
        self.set_state_colour(WidgetState.BASE)
    
    def set_relative_position(self, relative_position):
        self._relative_position = relative_position
        self.set_geometry()
    
    def set_relative_size(self, new_relative_size):
        self._relative_size = new_relative_size

    def set_image(self):
        self.image = pygame.transform.scale(self._empty_surface, self.size)

        if self._vertical:
            rounded_radius = self.size[0] / 2
        else:
            rounded_radius = self.size[1] / 2

        pygame.draw.rect(self.image, self._fill_colour, (0, 0, self.size[0], self.size[1]), border_radius=int(rounded_radius))
    
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