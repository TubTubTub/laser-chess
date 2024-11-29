import pygame
from data.widgets.bases import _Widget
from data.widgets.colour_square import _ColourSquare
from data.widgets.colour_slider import _ColourSlider
from data.widgets.colour_display import _ColourDisplay
from data.components.custom_event import CustomEvent

class ColourPicker(_Widget):
    def __init__(self, relative_position, relative_length, default_colour, event_type, border_width=5, border_colour=(255, 255, 255)):
        super().__init__()

        self._relative_position = relative_position
        self._relative_size = (relative_length, relative_length)
        self._relative_border_width = border_width / self._surface_size[1]

        self._border_colour = border_colour

        self.image = pygame.Surface(self._size)
        self.rect = self.image.get_rect()

        self._square = _ColourSquare(surface=self.image, get_parent_position=lambda: self._position, relative_position=(0.1, 0.1), relative_length=0.5)
        self._square.set_colour(default_colour)

        self._slider = _ColourSlider(surface=self.image, get_parent_position=lambda: self._position, relative_position=(0.0, 0.7), relative_length=1.0, border_width=self._border_width, border_colour=self._border_colour)
        self._slider.set_colour(default_colour)

        self._display = _ColourDisplay(surface=self.image, relative_position=(0.7, 0.1), relative_size=(0.2, 0.5))
        self._display.set_colour(default_colour)

        self._event_type = event_type
        self._hover_event_type = event_type

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
        return (self._relative_border_width * self._surface_size[1])

    def set_image(self):
        self.image = pygame.Surface(self._size)
        self.image.fill((100, 100, 100))

        self._square.set_image()
        self._square.set_geometry()
        self.image.blit(self._square.image, self._square.rect)

        self._slider.set_image()
        self._slider.set_geometry()
        self.image.blit(self._slider.image, self._slider.rect)

        self._display.set_image()
        self._display.set_geometry()
        self.image.blit(self._display.image, self._display.rect)

        pygame.draw.rect(self.image, self._border_colour, (0, 0, self._size[0], self._size[1]), width=int(self._border_width))
    
    def set_geometry(self):
        self.rect = self.image.get_rect()
        self.rect.topleft = self._position
    
    def set_surface_size(self, new_surface_size):
        self._surface_size = new_surface_size
        self._square.set_surface_size(self._size)
        self._slider.set_surface_size(self._size)
        self._display.set_surface_size(self._size)
    
    def get_picker_position(self):
        return self._position
    
    def process_event(self, event):
        slider_colour = self._slider.process_event(event)
        square_colour = self._square.process_event(event)
        
        if square_colour:
            self._display.set_colour(square_colour)
            self.set_image()

        if slider_colour:
            self._square.set_colour(slider_colour)
            self.set_image()
        
        if event.type in [pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION] and self.rect.collidepoint(event.pos):
            return CustomEvent(self._event_type, colour=square_colour)