import pygame
from data.components.widgets.text import Text
from data.components.widgets.bases import _Pressable
from data.constants import WidgetState

class TextInput(_Pressable, Text):
    def __init__(self, relative_size, cursor_colour=(0, 255, 0), **kwargs):
        pygame.key.set_repeat(500, 100)

        self._cursor_pos = None
        _Pressable.__init__(
            self,
            event=None,
            hover_func=self.hover_func,
            down_func=self.down_func,
            up_func=self.up_func,
            play_sfx=False
        )
        font_size = self.calculate_font_size(relative_size)
        Text.__init__(self, text="", font_size=font_size, margin=15, **kwargs)
        self.initialise_new_colours(self._fill_colour)

        self.set_text('hello')

        self._empty_cursor = pygame.Surface((0, 0))
        self._cursor_colour = cursor_colour

        self.set_image()
        self.set_geometry()

    def hover_func(self):
        self.set_state_colour(WidgetState.HOVER)
    def down_func(self):
        self.set_state_colour(WidgetState.PRESS)
    def up_func(self):
        self.set_state_colour(WidgetState.BASE)
            
    def initialise_new_colours(self, new_colour):
        r, g, b, a = pygame.Color(new_colour).rgba

        self._colours = {
            WidgetState.BASE: new_colour,
            WidgetState.HOVER: pygame.Color(max(r - 25, 0), max(g - 25, 0), max(b - 25, 0), a),
            WidgetState.PRESS: pygame.Color(max(r - 50, 0), max(g - 50, 0), max(b - 50, 0), a)
        }
    
    def set_state_colour(self, state):
        if self._fill_colour is None:
            return
        
        self._fill_colour = self._colours[state]

        self.set_image()
    
    def calculate_font_size(self, relative_size):
        return 30

    def calculate_cursor_position(self):
        current_width = self._border_width + (self._margin / 2)
        for index, metrics in enumerate(self._font.get_metrics(self._text, size=self._font_size)):
            if index == self._cursor_pos:
                return (current_width, self._margin / 2 + self._border_width)
            
            glyph_width = metrics[1]
            current_width += glyph_width
        return (current_width, self._margin / 2 + self._border_width)
    
    def relative_x_to_cursor_pos(self, relative_x):
        current_width = 0

        for index, metrics in enumerate(self._font.get_metrics(self._text, size=self._font_size)):
            glyph_width = metrics[1]

            if relative_x <= current_width:
                return index
            
            current_width += glyph_width
        
        return len(self._text)
    
    def set_text(self, new_text):
        self._text = new_text
    
    def set_cursor_pos(self, mouse_pos):
        if mouse_pos is None:
            self._cursor_pos = mouse_pos
            return

        relative_x = mouse_pos[0] - self._margin - self._border_width - self._position[0]
        relative_x = max(0, relative_x)
        self._cursor_pos = self.relative_x_to_cursor_pos(relative_x)
    
    def process_event(self, event):
        previous_state = self.get_widget_state()
        super().process_event(event)
        current_state = self.get_widget_state()
        
        match event.type:
            case pygame.MOUSEBUTTONUP:
                if previous_state == WidgetState.PRESS:
                    self.set_cursor_pos(event.pos)
                    self.set_image()
                if current_state == WidgetState.BASE:
                    self.set_cursor_pos(None)
                    self.set_image()
            
            case pygame.KEYDOWN:
                if self._cursor_pos is None:
                    return

                if event.mod & (pygame.KMOD_CTRL):
                    if event.key == pygame.K_c:
                            print('COPIED')
                    
                    elif event.key == pygame.K_v:
                            print('PASTED')
                    
                    return
                
                match event.key:
                    case pygame.K_BACKSPACE:
                        print('wow')
    
    def set_image(self):
        super().set_image()

        if self._cursor_pos is not None:
            cursor_height = self._size[1] - self._border_width - self._margin
            cursor_size = (cursor_height * 0.1, cursor_height)
            cursor_position = self.calculate_cursor_position()
            scaled_cursor = pygame.transform.scale(self._empty_cursor, cursor_size)
            scaled_cursor.fill(self._cursor_colour)
            self.image.blit(scaled_cursor, cursor_position)