import pygame
from data.widgets.bases import _Widget
from data.assets import FONTS

class Text(_Widget): # Pure text
    def __init__(self, relative_position, text, text_colour=(100, 100, 100), center=True, minimum_width=0, font=FONTS['default'], font_size=100, fill_colour=(255, 255, 255), margin=50, border_width=0, border_colour=(255, 255, 255), border_radius=5):
        super().__init__()

        self._relative_position = relative_position

        self._text = text
        self._text_colour = text_colour
        self._font = font

        self._relative_margin = margin / self._surface_size[1]
        self._relative_font_size = font_size / self._surface_size[1]
        self._relative_border_width = border_width / self._surface_size[1]
        self._relative_border_radius = border_radius / self._surface_size[1]
        
        self._center = center
        self._relative_minimum_width = minimum_width / self._surface_size[1]

        self._fill_colour = fill_colour

        self._border_colour = border_colour

        self.rect = self._font.get_rect(self._text, size=self._font_size)
        self.rect.topleft = self._position

        self._empty_surface = pygame.Surface((0, 0), pygame.SRCALPHA)

        if margin >= self._size[0] or margin >= self._size[1]:
            raise ValueError('Margin must be less than rect dimensinos (Text.__init__)')

        self.set_image()
        self.set_geometry()

    @property
    def _position(self):
        return (self._relative_position[0] * self._surface_size[0], self._relative_position[1] * self._surface_size[1])

    @property
    def _size(self):
        font_rect_size = self._font.get_rect(self._text, size=self._font_size).size
        if self._text == '':
            font_rect_size = (font_rect_size[0], self._font.get_rect('j', size=self._font_size).size[1])
        
        rect_size = pygame.Rect((0, 0, font_rect_size[0], font_rect_size[1])).inflate(self._margin, self._margin).size

        if self._minimum_width:
            if rect_size[0] < self._minimum_width:
                rect_size = (self._minimum_width, rect_size[1])

        return rect_size

    @property
    def _font_size(self):
        return self._relative_font_size * self._surface_size[1]

    @property
    def _margin(self):
        return self._relative_margin * self._surface_size[1]

    @property
    def _border_width(self):
        return self._relative_border_width * self._surface_size[1]
    
    @property
    def _border_radius(self):
        return self._relative_border_radius * self._surface_size[1]

    @property
    def _minimum_width(self):
        return self._relative_minimum_width * self._surface_size[1]

    def update_text(self, new_text):
        self._text = new_text
        self.set_image()
        self.set_geometry()
    
    def set_image(self):
        text_surface = pygame.transform.scale(self._empty_surface, self._size)
        self.image = text_surface

        if self._fill_colour:
            fill_rect = pygame.Rect(0, 0, self._size[0], self._size[1])
            pygame.draw.rect(self.image, self._fill_colour, fill_rect, border_radius=int(self._border_radius))

        font_rect_size = self._font.get_rect(self._text, size=self._font_size).size
        if self._center:
            font_position = ((self._size[0] - font_rect_size[0]) / 2, (self._size[1] - font_rect_size[1]) / 2)
        else:
            font_position = (self._margin / 2, (self._size[1] - font_rect_size[1]) / 2)
        self._font.render_to(self.image, font_position, self._text, fgcolor=self._text_colour, size=self._font_size)

        if self._border_width:
            fill_rect = pygame.Rect(0, 0, self._size[0], self._size[1])
            pygame.draw.rect(self.image, self._border_colour, fill_rect, width=int(self._border_width), border_radius=int(self._border_radius))

    def set_geometry(self):
        self.rect = self.image.get_rect()
        self.rect.topleft = self._position
    
    def set_surface_size(self, new_surface_size):
        self._surface_size = new_surface_size

    def process_event(self, event):
        pass