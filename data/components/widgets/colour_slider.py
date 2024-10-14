import pygame
from data.components.widgets.bases import _Widget
from data.components.widgets.slider_thumb import SliderThumb
from data.utils.widget_helpers import create_gradient

class ColourSlider(_Widget):
    def __init__(self, relative_position, width, height, border_width=12, border_colour=(255, 255, 255)):
        super().__init__()
        self._screen_size = pygame.display.get_surface().get_size()
        self._relative_size = (width / self._screen_size[1], height / self._screen_size[1])
        self._relative_position = relative_position
        
        self._selected_percent = 0

        self._gradient_surface = create_gradient(self.calculate_gradient_size(), border_width, border_colour)

        self._thumb = SliderThumb(radius=self._size[1] / 2, colour=(255, 255, 255))
        self.set_thumb_center(0)

        self._empty_surface = pygame.Surface(self._size)
        self._empty_surface.fill((50, 50, 50))
        
        self.set_image()
        self.set_geometry()
    
    @property
    def _size(self):
        return (self._relative_size[0] * self._screen_size[1], self._relative_size[1] * self._screen_size[1])

    @property
    def _position(self):
        return (self._relative_position[0] * self._screen_size[0], self._relative_size[1] * self._screen_size[1])
    
    def calculate_gradient_size(self):
        return (self._size[0] - 2 * (self._size[1] / 2), self._size[1] / 2)
    
    def calculate_gradient_position(self):
        return (self._size[1] / 2, self._size[1] / 4)
    
    def set_image(self):
        gradient_scaled = pygame.transform.smoothscale(self._gradient_surface, self.calculate_gradient_size())
        gradient_position = self.calculate_gradient_position()

        self.image = pygame.transform.scale(self._empty_surface, (self._size))
        self.image.blit(gradient_scaled, gradient_position)

        # center = (self._selected_percent * self._gradient_width + self.rect.left + self._border_width, self.rect.centery)
        # pygame.draw.circle(self.image, self.get_selected_colour(), center, self.rect.height // 2)

    def set_geometry(self):
        self.rect = self.image.get_rect()
        self.rect.center = self._position
    
    def set_thumb_center(self, pos_x):
        pos_y = self._relative_position[1] * self._screen_size[1] + self._size[1] / 2
        self._thumb.set_center((pos_x, pos_y))
    
    def set_screen_size(self, new_screen_size):
        self._screen_size = new_screen_size
        self._thumb.set_radius((self._relative_size[1] * self._screen_size[1]) / 2)
    
    def process_event(self, event):
        pass
    #     match event.type:
    #         case pygame.MOUSEBUTTONDOWN:
    #             if not self.rect.collidepoint(event.pos):
    #                 return
                
    #             self._selected_percent = (event.pos[0] - self.rect.left - self._thumb_radius - self._border_width) / (self.get_gradient_size()[0] - 2 * self._border_width)
    #             self._selected_percent = max(0, min(self._selected_percent, 1))
    #             self.set_thumb_center(event.pos[0])
            

                # self.set_image()
    
    def get_selected_colour(self):
        colour = pygame.Color(0)
        colour.hsva = (int(self._selected_percent * 360), 100, 100)
        return colour
