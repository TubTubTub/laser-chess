import pygame
from data.widgets.bases import _Widget
from data.utils.font_helpers import text_width_to_font_size, text_height_to_font_size

class Text(_Widget): # Pure text
    def __init__(self, text, center=True, fit_vertical=True, **kwargs):
        super().__init__(**kwargs)
        self._text = text
        if fit_vertical:
            self._relative_font_size = text_height_to_font_size(self._text, self._font, (self.size[1] - 2 * (self.margin + self.border_width))) / self._surface_size[1]
        else:
            self._relative_font_size = text_width_to_font_size(self._text, self._font, (self.size[0] - 2 * (self.margin + self.border_width))) / self._surface_size[1]
        
        self._center = center
        self.rect = self._font.get_rect(self._text, size=self.font_size)
        self.rect.topleft = self.position

        self._empty_surface = pygame.Surface((0, 0), pygame.SRCALPHA)

        self.set_image()
        self.set_geometry()

    @property
    def minimum_width(self):
        return self._relative_minimum_width * self._surface_size[1]

    def update_text(self, new_text):
        self._text = new_text
        self.set_image()
        self.set_geometry()
    
    def set_image(self):
        text_surface = pygame.transform.scale(self._empty_surface, self.size)
        self.image = text_surface

        if self._fill_colour:
            fill_rect = pygame.Rect(0, 0, self.size[0], self.size[1])
            pygame.draw.rect(self.image, self._fill_colour, fill_rect, border_radius=int(self.border_radius))

        font_rect_size = self._font.get_rect(self._text, size=self.font_size).size
        if self._center:
            font_position = ((self.size[0] - font_rect_size[0]) / 2, (self.size[1] - font_rect_size[1]) / 2)
        else:
            font_position = (self.margin / 2, (self.size[1] - font_rect_size[1]) / 2)
        self._font.render_to(self.image, font_position, self._text, fgcolor=self._text_colour, size=self.font_size)

        if self.border_width:
            fill_rect = pygame.Rect(0, 0, self.size[0], self.size[1])
            pygame.draw.rect(self.image, self._border_colour, fill_rect, width=int(self.border_width), border_radius=int(self.border_radius))

    def process_event(self, event):
        pass