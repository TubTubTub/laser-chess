import pygame
from data.components.widgets.bases import _Widget
from data.components.widgets.colour_square import ColourSquare
from data.components.widgets.colour_slider import ColourSlider
from data.components.widgets.colour_display import ColourDisplay
from data.constants import SettingsEventType
from data.utils.settings_helpers import get_user_settings

user_settings = get_user_settings()

class ColourPicker(_Widget):
    def __init__(self, relative_position, size, border_width=5, border_colour=(255, 255, 255)):
        super().__init__()
        self._screen = pygame.display.get_surface()
        self._screen_size = self._screen.get_size()

        self._relative_position = relative_position
        self._relative_size = (size[0] / self._screen_size[1], size[1] / self._screen_size[1])
        self._relative_border_width = border_width / self._screen_size[1]

        self.image = pygame.Surface(self._size)
        self.rect = self.image.get_rect()
        self._border_colour = border_colour
        self._font = pygame.freetype.Font(user_settings['primaryFont'])

        self._square = ColourSquare(surface=self.image, get_parent_position=lambda: self._position, relative_position=(0.1, 0.1), relative_length=0.5)
        self._square.set_colour((255, 255, 0))

        self._slider = ColourSlider(surface=self.image, get_parent_position=lambda: self._position, relative_position=(0.0, 0.7), relative_length=1.0, border_width=self._border_width, border_colour=self._border_colour)

        self._display = ColourDisplay(surface=self.image, relative_position=(0.7, 0.1), relative_size=(0.2, 0.5))
        self._display.set_colour((255, 0, 255))

        self.set_image()
        self.set_geometry()
    
    @property
    def _size(self):
        return (self._relative_size[0] * self._screen_size[1], self._relative_size[1] * self._screen_size[1])

    @property
    def _position(self):
        return (self._relative_position[0] * self._screen_size[0], self._relative_position[1] * self._screen_size[1])
    
    @property
    def _border_width(self):
        return (self._relative_border_width * self._screen_size[1])

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
    
    def set_screen_size(self, new_screen_size):
        self._screen_size = new_screen_size
        self._square.set_screen_size(self._size)
        self._slider.set_screen_size(self._size)
        self._display.set_screen_size(self._size)
    
    def get_picker_position(self):
        return self._position
    
    def process_event(self, event):
        slider_event = self._slider.process_event(event)
        square_event = self._square.process_event(event)

        if slider_event:
            match slider_event.type:
                case SettingsEventType.COLOUR_SLIDER_SLIDE:
                    self._square.set_colour(slider_event.colour)
                    self.set_image()
                case SettingsEventType.COLOUR_SLIDER_CLICK:
                    self.set_image()
        
        if square_event:
            match square_event.type:
                case SettingsEventType.COLOUR_CLICK:
                    self._display.set_colour(square_event.colour)
                    self.set_image()