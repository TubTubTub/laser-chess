import pygame
from data.widgets.bases.widget import _Widget
from data.utils.widget_helpers import create_text_box

class Icon(_Widget):
    def __init__(self, icon, stretch=False, is_mask=False, smooth=False, fit_icon=False, box_colours=None, **kwargs):
        super().__init__(**kwargs)

        if fit_icon:
            aspect_ratio = icon.width / icon.height
            self._relative_size = (self._relative_size[1] * aspect_ratio, self._relative_size[1])

        self._icon = icon
        self._is_mask = is_mask
        self._stretch = stretch
        self._smooth = smooth
        self._box_colours = box_colours
        
        self._empty_surface = pygame.Surface((0, 0), pygame.SRCALPHA)

        self.set_image()
        self.set_geometry()
    
    def set_icon(self, icon):
        self._icon = icon
        self.set_image()
    
    def set_image(self):
        if self._box_colours:
            self.image = create_text_box(self.size, self.border_width, self._box_colours)
        else:
            self.image = pygame.transform.scale(self._empty_surface, self.size)

            if self._fill_colour:
                pygame.draw.rect(self.image, self._fill_colour, self.image.get_rect(), border_radius=int(self.border_radius))

        if self._stretch:
            if self._smooth:
                scaled_icon = pygame.transform.smoothscale(self._icon, (self.size[0] -  (2 * self.margin), self.size[1] -  (2 * self.margin)))
            else:
                scaled_icon = pygame.transform.scale(self._icon, (self.size[0] -  (2 * self.margin), self.size[1] -  (2 * self.margin)))

            icon_position = (self.margin, self.margin)
        else:
            max_height = self.size[1] - (2 * self.margin)
            max_width = self.size[0] - (2 * self.margin)
            scale_factor = min(max_width / self._icon.width, max_height / self._icon.height)

            if self._smooth:
                scaled_icon = pygame.transform.smoothscale_by(self._icon, (scale_factor, scale_factor))
            else:
                scaled_icon = pygame.transform.scale_by(self._icon, (scale_factor, scale_factor))
            icon_position = ((self.size[0] - scaled_icon.width) / 2, (self.size[1] - scaled_icon.height) / 2)

        if self._is_mask:
            self.image.blit(scaled_icon, icon_position, None, pygame.BLEND_RGBA_MULT)
        else:
            self.image.blit(scaled_icon, icon_position)

        if self._box_colours is None and self.border_width:
            pygame.draw.rect(self.image, self._border_colour, self.image.get_rect(), width=int(self.border_width), border_radius=int(self.border_radius))
    
    def process_event(self, event):
        pass