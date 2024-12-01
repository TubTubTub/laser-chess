import pygame
from data.widgets.bases import _Widget

class Icon(_Widget):
    def __init__(self, icon, stretch=True, is_mask=False, **kwargs):
        super().__init__(**kwargs)

        self._icon = icon
        self._is_mask = is_mask
        self._stretch = stretch
        
        self._empty_surface = pygame.Surface((0, 0), pygame.SRCALPHA)
        
        self.set_image()
        self.set_geometry()
    
    def set_image(self):
        self.image = pygame.transform.scale(self._empty_surface, self.size)
        pygame.draw.rect(self.image, self._fill_colour, self.image.get_rect(), border_radius=int(self.border_radius))

        if self._stretch:
            scaled_icon = pygame.transform.smoothscale(self._icon, (self.size[0] -  (2 * self.margin), self.size[1] -  (2 * self.margin)))
            icon_position = (self.margin, self.margin)
        else:
            max_height = self.size[1] - (2 * self.margin)
            max_width = self.size[0] - (2 * self.margin)
            scale_factor = min(max_width / self._icon.width, max_height / self._icon.height)
            scaled_icon = pygame.transform.smoothscale_by(self._icon, (scale_factor, scale_factor))
            icon_position = ((self.size[0] - scaled_icon.width) / 2, (self.size[1] - scaled_icon.height) / 2)

        if self._is_mask:
            self.image.blit(scaled_icon, icon_position, None, pygame.BLEND_RGBA_MULT)
        else:
            self.image.blit(scaled_icon, icon_position)

        if self.border_width:
            pygame.draw.rect(self.image, self._border_colour, self.image.get_rect(), width=int(self.border_width), border_radius=int(self.border_radius))
    
    def process_event(self, event):
        pass