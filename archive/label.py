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
#                 self._label_rect = pygame.FRect(self._position[0], self._position[1], text_rect.width + (self._margin * 2), text_rect.height + (self._margin * 2))
#             case 'size':
#                 self._label_rect = pygame.FRect(self._position[0], self._position[1], self._width, self._height)
        
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