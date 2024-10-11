import pygame
from data.utils.settings_helpers import get_user_settings
from data.constants import WidgetState
import colorsys
from math import sqrt

user_settings = get_user_settings()

class _Widget(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        pass
    
    def set_image(self):
        raise NotImplementedError
    
    def set_geometry(self):
        raise NotImplementedError
    
    def process_event(self, event):
        raise NotImplementedError

class ColourSlider(_Widget):
    def __init__(self, position, width, height, border_colour=(255, 255, 255)):
        super().__init__()
        self._screen_size = pygame.display.get_surface().get_size()
        self._relative_size = (width / self._screen_size[0], height / self._screen_size[1])

        self._position = position
        self._border_width = 12
        self._thumb_radius = self.get_height_px() / 2
        self._selected_percent = 0
        
        self._gradient_surface = pygame.Surface((width - 2 * self._thumb_radius, height / 2))

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
        pygame.draw.rect(self._gradient_surface, border_colour, border_rect , width=self._border_width, border_radius=int(self._height / 2))
        
        self.image = pygame.Surface((width, height))
        self.image.fill((50, 50, 50))
        
        self.set_geometry()
        self.set_image()

    def get_width_px(self):
        return self._relative_size[0] * self._screen_size[0]
    
    def get_height_px(self):
        return self._relative_size[1] * self._screen_size[1]
    
    def calculate_rounded_slice_height(self, distance, radius):
        return sqrt(radius ** 2 - distance ** 2) * 2
    
    def set_image(self):
        self.image.blit(self._gradient_surface, (self._thumb_radius, self._height / 4))
        # center = (self._selected_percent * self._gradient_width + self.rect.left + self._border_width, self.rect.centery)
        # pygame.draw.circle(self.image, self.get_selected_colour(), center, self.rect.height // 2)

    def set_geometry(self):
        self.rect = pygame.Rect(self._position[0], self._position[1], self._width, self._height)
    
    def process_event(self, event):
        match event.type:
            case pygame.MOUSEBUTTONDOWN:
                self.slider_rect = (self.)
                if self.rect.collidepoint(event.pos):
                    self._selected_percent = (event.pos[0] - self.rect.left - self._border_width) / self._gradient_width
                    self._selected_percent = max(0, min(self._selected_percent, 1))

                    self.set_image()
    
    def get_selected_colour(self):
        colour = pygame.Color(0)
        print(int(self._selected_percent * self._gradient_width), 'sdsds')
        colour.hsva = (int(self._selected_percent * 360), 100, 100)
        return colour

class ColourPicker(_Widget):
    def __init__(self, origin_position, default_colour=(255, 0, 0), font_path=user_settings['primaryFont']):
        super().__init__()
        self._screen_size = pygame.display.get_surface().get_size()
        self._origin_position = origin_position
        self._colour = pygame.Color(default_colour)
        self._font = pygame.freetype.Font(font_path)

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

    def rgb_to_hsv(self, rgb):
        red, green, blue = rgb

        rgb_max = max(rgb)
        rgb_min = min(rgb)

        value = rgb_max
        if value == 0:
            return (0, 0, 0)

        saturation = 255 * (rgb_max - rgb_min) // value

        if saturation == 0:
            return (0, 0, value)
        
        if rgb_max == red:
            hue = 0 + 43 * (green - blue) // (rgb_max - rgb_min)
        elif rgb_max == green:
            hue = 85 + 43 * (blue - 4) // (rgb_max - rgb_min)
        else:
            hue = 171 + 43 * (red - green) // (rgb_max - rgb_min)
        
        return (hue, saturation, value)
    
    def hsv_to_rgb(self, hsv):
        hue, saturation, value = hsv

        if saturation == 0:
            return (value, value, value)
        
        region = hue // 43
        
        remainder = (hue - (region * 43)) * 6

        p = (value * (255 - saturation)) >> 8
        q = (value * (255 - ((saturation * remainder) >> 8))) >> 8
        t = (value * (255 - ((saturation * (255 - remainder)) >> 8))) >> 8

        if region == 0:
            return (value, t, p)
        elif region == 1:
            return (q, value, p)
        elif region == 2:
            return (p, value, t)
        elif region == 3:
            return (p, q, value)
        elif region == 4:
            return (t, p, value)
        else:
            return (value, p, q)

class Text(_Widget): # Pure text
    def __init__(self, relative_position, text, text_colour=(255, 255, 255), font_path=user_settings['primaryFont'], font_size=100, fill_colour=(255, 255, 255), margin=50, border_width=0, border_colour=(255, 255, 255), border_radius=5):
        super().__init__()
        self._screen_size = pygame.display.get_surface().get_size()

        self._relative_position = relative_position

        self._text = text
        self._text_colour = text_colour
        self._font = pygame.freetype.Font(font_path)

        self._margin = margin

        self._fill_colour = fill_colour

        self._border_width = border_width
        self._border_colour = border_colour
        self._border_radius = border_radius
        
        self._position = (self._relative_position[0] * self._screen_size[0], self._relative_position[1] * self._screen_size[1])
        self._relative_font_size = font_size / self._screen_size[1]

        self.rect = self._font.get_rect(self._text, size=font_size)
        self.rect.topleft = self._position

        self._text_surface = pygame.Surface((0, 0))

        self.set_image()
        self.set_geometry()
    
    def set_image(self):
        font_size = self._relative_font_size * self._screen_size[1]

        font_rect = self._font.get_rect(self._text, size=font_size)
        surface_size = font_rect.inflate(self._margin, self._margin).size

        text_surface = pygame.transform.scale(self._text_surface, surface_size)
        self.image = text_surface

        if self._fill_colour:
            fill_rect = pygame.Rect(0, 0, surface_size[0], surface_size[1])
            pygame.draw.rect(self.image, self._fill_colour, fill_rect, border_radius=self._border_radius)

        if self._border_width:
            fill_rect = pygame.Rect(0, 0, surface_size[0], surface_size[1])
            pygame.draw.rect(self.image, self._border_colour, fill_rect, width=self._border_width, border_radius=self._border_radius)

        font_center = ((surface_size[0] - font_rect.size[0]) / 2, (surface_size[1] - font_rect.size[1]) / 2)
        self._font.render_to(self.image, font_center, self._text, fgcolor=self._text_colour, size=font_size)
    
    def set_geometry(self):
        position = (self._relative_position[0] * self._screen_size[0], self._relative_position[1] * self._screen_size[1])
        self.rect = self.image.get_rect()
        self.rect.center = position
    
    def set_screen_size(self, new_screen_size):
        self._screen_size = new_screen_size
    
    def process_event(self, event):
        pass

class Button(Text):
    def __init__(self, shadow_distance=0, shadow_colour=(0, 0, 0), event=None, **kwargs):
        super().__init__(**kwargs)
        self._shadow_distance = shadow_distance
        self._shadow_colour = shadow_colour
        self._event = event
        self._pressed = False

        if self._fill_colour:
            r, g, b = self._fill_colour
            self._hover_colour = (max(r - 25, 0), max(g - 25, 0), max(b - 25, 0))
            self._press_colour = (max(r - 50, 0), max(g - 50, 0), max(b - 50, 0))
            self._fill_colour_copy = self._fill_colour

    def process_event(self, event):
        match event.type:
            case pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.set_state_colour(WidgetState.PRESS)
                    self._pressed = True
            
            case pygame.MOUSEBUTTONUP:
                if self.rect.collidepoint(event.pos):
                    self.set_state_colour(WidgetState.HOVER)
                    
                    if self._pressed:
                        self._pressed = False
                        return self._event
            
            case pygame.MOUSEMOTION:
                if self.rect.collidepoint(event.pos):
                    if self._pressed:
                        self.set_state_colour(WidgetState.PRESS)
                    else:
                        self.set_state_colour(WidgetState.HOVER)
                else:
                    self.set_state_colour(WidgetState.DEFAULT)
                    self._pressed = False
    
    def set_state_colour(self, state):
        if self._fill_colour is None:
            return

        match state:
            case WidgetState.DEFAULT:
                self._fill_colour = self._fill_colour_copy
            case WidgetState.HOVER:
                self._fill_colour = self._hover_colour
            case WidgetState.PRESS:
                self._fill_colour = self._press_colour

        self.set_image()

# class Label(_Widget):
#     '''Set 0 border width for filled rounded label'''
#     def __init__(self, screen, position, text, font_path=user_settings['primaryFont'], font_size=30, text_colour=(0, 0, 0), label_colour=None, border_width=0, border_radius=0, margin=None, width=None, height=None):
#         '''Font size as a percentage of screen height'''
#         super().__init__()
#         self._text = text

#         self._draw_type = None
#         self._label_rect = None
#         self._screen = screen
#         self._position = position
#         self._text_colour = text_colour
#         self._label_colour = label_colour
#         self._border_width = border_width
#         self._border_radius = border_radius
#         self._margin = margin
#         self._width = width
#         self._height = height
#         self._font = pygame.freetype.Font(font_path)
#         self._font_size = font_size
        
#         screen_width, screen_height = screen.get_size()
#         self._relative_position = (position[0] / screen_width, position[1] / screen_height)
#         self._relative_font_size = font_size / screen_height
#         if margin:
#             self._relative_margin = margin / screen_height
#         elif width and height:
#             self._relative_width = width / screen_width
#             self._relative_height = height / screen_height

#         if margin:
#             if margin < 0: raise ValueError('Provided margin must be 0 or above (elements.py)!')
#             if label_colour is None: raise ValueError('Label colour required when using margin (elements.py)!')
#             self._draw_type = 'margin'

#         elif width and height:
#             if label_colour is None: raise ValueError('Label colour required when using size arguments (elements.py)!')
#             self._draw_type = 'size'
        
#         if border_radius:
#             if border_width < 0: raise ValueError('Border width must be greater than 0! (elements.py)')
#             if border_radius == 0: raise ValueError('Border radius must be provided when border width is used! (elements.py)')
#     @property
#     def text(self):
#         return self._text
    
#     @text.setter
#     def text(self, new_text):
#         self._screen.fill((0, 0, 0))
#         self._text = new_text

#     def draw(self):
#         '''draw text alone'''
#         if self._draw_type is None:
#             self._font.render_to(self._screen, self._position, self.text, fgcolor=self._text_colour, size=self._font_size)
#             return

#         '''draw text with background'''
#         text_rect = self._font.get_rect(self.text, size=self._font_size)

#         match self._draw_type:
#             case 'margin':
#                 self._label_rect = pygame.Rect(self._position[0], self._position[1], text_rect.width + (self._margin * 2), text_rect.height + (self._margin * 2))
#             case 'size':
#                 self._label_rect = pygame.Rect(self._position[0], self._position[1], self._width, self._height)
        
#         text_x = self._position[0] + self._label_rect.width / 2 - text_rect.width / 2
#         text_y = self._position[1] + self._label_rect.height / 2 - text_rect.height / 2
        
#         pygame.draw.rect(self._screen, self._label_colour, self._label_rect, width=self._border_width, border_radius=self._border_radius)
#         self._font.render_to(self._screen, (text_x, text_y), self.text, fgcolor=self._text_colour, size=self._font_size)
    
#     def handle_events(self, event):
#         pass
    
#     def handle_resize(self):
#         screen_width, screen_height = self._screen.get_size()

#         self._position = self._relative_position[0] * screen_width, self._relative_position[1] * screen_height
#         self._font_size = self._relative_font_size * screen_height

#         if self._draw_type == 'margin':
#             self._margin = self._relative_margin * screen_height
#         elif self._draw_type == 'size':
#             self._width = self._relative_width * screen_width
#             self._height = self._relative_height * screen_height