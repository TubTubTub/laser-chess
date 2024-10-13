import pygame
from data.components.widgets.bases import _Widget
from data.utils.settings_helpers import get_user_settings

user_settings = get_user_settings()

class ColourPicker(_Widget):
    def __init__(self, origin_position, default_colour=(255, 0, 0)):
        super().__init__()
        self._screen_size = pygame.display.get_surface().get_size()
        self._origin_position = origin_position
        self._colour = pygame.Color(default_colour)
        self._font = pygame.freetype.Font(user_settings['primaryFont'])

        self._select_area = pygame.Surface((self._screen_size[1] * 0.2, self._screen_size[1] * 0.2))

        mix_1 = pygame.Surface((1, 2))
        mix_1.fill((255, 255, 255))
        mix_1.set_at((0, 1), (0, 0, 0))
        mix_1 = pygame.transform.smoothscale(mix_1, self._select_area.size)

        hue = self._colour.hsva[0]
        saturated_rgb = pygame.Color(0)
        saturated_rgb.hsva = (hue, 100, 100)

        mix_2 = pygame.Surface((2, 1))
        mix_2.fill((255, 255, 255))
        mix_2.set_at((1, 0), saturated_rgb)
        mix_2 = pygame.transform.smoothscale(mix_2, self._select_area.size)

        mix_1.blit(mix_2, (0, 0), special_flags=pygame.BLEND_MULT)

        self._select_area.blit(mix_1, (0, 0))

        self.set_image()
        self.set_geometry()
    
    def set_image(self):
        self.image = self._select_area
    
    def set_geometry(self):
        self.rect = self.image.get_rect()
    
    def process_event(self, event):
        pass