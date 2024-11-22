import pygame
from data.widgets.bases import _Widget
from data.assets import FONTS

class Icon(_Widget):
    def __init__(self, relative_position, width, margin, font_size=30, text_colour=(100, 100, 100), font=FONTS['default']):
        super().__init__()
        self._screen_size = pygame.display.get_surface().get_size()

        self._relative_position = relative_position
        self._font = font
        self._relative_margin = margin / self._screen_size[1]

        self._relative_font_size = font_size
        
        self._empty_surface = pygame.Surface((0, 0), pygame.SRCALPHA)

        if margin * 2 >= min(size[0], size[1]):
            raise ValueError('Size is too small to fit specified margin! (Icon.__init__)', self._size, self._margin)
        
        self.set_image()
        self.set_geometry()

    @property
    def _position(self):
        return (self._relative_position[0] * self._screen_size[0], self._relative_position[1] * self._screen_size[1])

    @property
    def _size(self):
        self._font.get_metric('')
        return (self._relative_size[0] * self._screen_size[1], self._relative_size[1] * self._screen_size[1])

    @property
    def _margin(self):
        return self._relative_margin * self._screen_size[1]

    @property
    def _font_size(self):
        return self._relative_font_size * self._screen_size[1]
    
    def set_image(self):
        self.image = pygame.transform.scale(self._empty_surface, self._size)
        pygame.draw.rect(self.image, self._fill_colour, self.image.get_rect(), border_radius=int(self._border_radius))

        if self._stretch:
            scaled_icon = pygame.transform.smoothscale(self._icon, (self._size[0] -  (2 * self._margin), self._size[1] -  (2 * self._margin)))
            icon_position = (self._margin, self._margin)
        else:
            max_height = self._size[1] - (2 * self._margin)
            max_width = self._size[0] - (2 * self._margin)
            scale_factor = min(max_width / self._icon.width, max_height / self._icon.height)
            scaled_icon = pygame.transform.smoothscale_by(self._icon, (scale_factor, scale_factor))
            icon_position = ((self._size[0] - scaled_icon.width) / 2, (self._size[1] - scaled_icon.height) / 2)

        if self._is_mask:
            self.image.blit(scaled_icon, icon_position, None, pygame.BLEND_RGBA_MULT)
        else:
            self.image.blit(scaled_icon, icon_position)

        if self._border_width:
            pygame.draw.rect(self.image, self._border_colour, self.image.get_rect(), width=int(self._border_width), border_radius=int(self._border_radius))
    
    def set_geometry(self):
        self.rect = self.image.get_rect()
        self.rect.topleft = self._position
    
    def set_screen_size(self, new_screen_size):
        self._screen_size = new_screen_size
    
    def process_event(self, event):
        pass