import pygame
from math import sqrt
from data.components.widgets.bases import _Widget
from data.components.widgets.slider_thumb import SliderThumb

class ColourSlider(_Widget):
    def __init__(self, relative_position, width, height, border_colour=(255, 255, 255)):
        super().__init__()
        self._screen_size = pygame.display.get_surface().get_size()
        self._relative_size = (width / self._screen_size[0], height / self._screen_size[1])
        self._relative_position = relative_position
        
        
        self._size = (self._relative_size[0] * self._screen_size[0], self._relative_size[1] * self._screen_size[1])
        self._thumb = SliderThumb(radius=self._size[1] / 2, colour=(255, 255, 255), center=self.set_thumb_center())
        self._thumb_center = self.set_thumb_center()

        self._border_width = 12
        self._thumb_radius = self._size[1] / 2
        self._selected_percent = 0
        
        self._gradient_surface = pygame.Surface(self.get_gradient_size())

        first_round_end = self._gradient_surface.height / 2
        second_round_end = self._gradient_surface.width - first_round_end
        gradient_y_mid = self._gradient_surface.height / 2

        for i in range(self._gradient_surface.width):
            draw_height = self._gradient_surface.height
  
            if not (first_round_end < i < second_round_end):
                distance_from_cutoff = min(abs(first_round_end - i), abs(i - second_round_end))
                draw_height = self.calculate_rounded_slice_height(distance_from_cutoff, self._gradient_surface.height / 2)

            color = pygame.Color(0)
            color.hsva = (int(360 * i / self._gradient_surface.width), 100, 100)

            draw_rect = pygame.Rect((0, 0, 1, draw_height - 2 * self._border_width))
            draw_rect.center = (i, gradient_y_mid)

            pygame.draw.rect(self._gradient_surface, color, draw_rect)

        border_rect = pygame.Rect((0, 0, self._gradient_surface.width, self._gradient_surface.height))
        pygame.draw.rect(self._gradient_surface, border_colour, border_rect , width=self._border_width, border_radius=int(self._size[1] / 2))
        
        self.image = pygame.Surface(self._size)
        self.image.fill((50, 50, 50))
        
        self.set_image()
        self.set_geometry()
    
    def get_gradient_size(self):
        return (self._size[0] - 2 * self._thumb_radius, self._size[1] / 2)
    
    def calculate_rounded_slice_height(self, distance, radius):
        return sqrt(radius ** 2 - distance ** 2) * 2
    
    def set_image(self):
        scaled_gradient = pygame.transform.smoothscale(self._gradient_surface, self.get_gradient_size())
        self.image.blit(scaled_gradient, (self._thumb_radius, self._size[1] / 4))
        self._thumb.draw()
        # center = (self._selected_percent * self._gradient_width + self.rect.left + self._border_width, self.rect.centery)
        # pygame.draw.circle(self.image, self.get_selected_colour(), center, self.rect.height // 2)

    def set_geometry(self):
        self._thumb_radius = self._size[1] / 2
        self.rect = self.image.get_rect()
    
    def set_thumb_center(self, pos_x):
        if pos_x:
            pos_y = self.rect.y + self._size[1] / 2
            self._thumb_center = (pos_x, pos_y)
            return

        print('ahh')
    
    def set_screen_size(self, new_screen_size):
        self._screen_size = new_screen_size
    
    def process_event(self, event):
        match event.type:
            case pygame.MOUSEBUTTONDOWN:
                if not self.rect.collidepoint(event.pos):
                    return
                
                self._selected_percent = (event.pos[0] - self.rect.left - self._thumb_radius - self._border_width) / (self.get_gradient_size()[0] - 2 * self._border_width)
                self._selected_percent = max(0, min(self._selected_percent, 1))
                self.set_thumb_center(event.pos[0])
            

                # self.set_image()
    
    def get_selected_colour(self):
        colour = pygame.Color(0)
        colour.hsva = (int(self._selected_percent * 360), 100, 100)
        return colour
