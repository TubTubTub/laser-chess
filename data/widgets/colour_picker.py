import pygame
from data.widgets.bases import _Widget
from data.widgets.colour_square import _ColourSquare
from data.widgets.colour_slider import _ColourSlider
from data.widgets.colour_display import _ColourDisplay
from data.components.custom_event import CustomEvent

class ColourPicker(_Widget):
    def __init__(self, relative_width, event_type, **kwargs):
        super().__init__(relative_size=(relative_width, relative_width), **kwargs)

        self.image = pygame.Surface(self.size)
        self.rect = self.image.get_rect()

        self._square = _ColourSquare(surface=self.image, get_parent_position=lambda: self.position, relative_position=(0.1, 0.1), relative_length=0.5)
        self._square.set_colour(kwargs.get('fill_colour'))

        self._slider = _ColourSlider(surface=self.image, get_parent_position=lambda: self.position, relative_position=(0.0, 0.7), relative_length=1.0, border_width=self.border_width, border_colour=self._border_colour)
        self._slider.set_colour(kwargs.get('fill_colour'))

        self._display = _ColourDisplay(surface=self.image, relative_position=(0.7, 0.1), relative_size=(0.2, 0.5))
        self._display.set_colour(kwargs.get('fill_colour'))

        self._event_type = event_type
        self._hover_event_type = event_type

        self.set_image()
        self.set_geometry()

    def set_image(self):
        self.image = pygame.Surface(self.size)
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

        pygame.draw.rect(self.image, self._border_colour, (0, 0, self.size[0], self.size[1]), width=int(self.border_width))
    
    def set_surface_size(self, new_surface_size):
        super().set_surface_size(new_surface_size)
        self._square.set_surface_size(self.size)
        self._slider.set_surface_size(self.size)
        self._display.set_surface_size(self.size)
    
    def get_picker_position(self):
        return self.position
    
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