import pygame
import pyperclip
from data.widgets.text import Text
from data.widgets.bases import _Pressable
from data.components.custom_event import CustomEvent
from data.components.animation import animation
from data.constants import WidgetState
from data.assets import FONTS

class TextInput(_Pressable, Text):
    def __init__(self, size, event_type, blinking_interval=530, validator=(lambda x: True), default='', placeholder='PLACEHOLDER TEXT', placeholder_colour=(200, 200, 200), cursor_colour=(0, 0, 0), **kwargs):
        pygame.key.set_repeat(500, 50)
        _Pressable.__init__(
            self,
            event=None,
            hover_func=self.hover_func,
            down_func=self.down_func,
            up_func=self.up_func,
            play_sfx=False
        )

        self._screen_size = pygame.display.get_surface().get_size()
        self._relative_size = (size[0] / self._screen_size[1], size[1] / self._screen_size[1])
        self._cursor_index = None

        Text.__init__(self, text="", font=FONTS['comicsans'], center=False, **kwargs)

        self._relative_font_size = self.calculate_font_size()
        self._blinking_fps = 1000 / blinking_interval
        self._cursor_colour = cursor_colour
        self._cursor_colour_copy = cursor_colour
        self._placeholder_colour = placeholder_colour
        self._text_colour_copy = self._text_colour
        self.initialise_new_colours(self._fill_colour)

        self._placeholder_text = placeholder
        self._is_placeholder = None
        if default:
            self.set_text(default)
            self.is_placeholder = False
        else:
            self.set_text(self._placeholder_text)
            self.is_placeholder = True

        self._event_type = event_type
        self._validator = validator
        self._blinking_cooldown = 0

        self._empty_cursor = pygame.Surface((0, 0), pygame.SRCALPHA)

        self.set_image()
        self.set_geometry()
    
    @property
    def is_placeholder(self):
        return self._is_placeholder
    
    @is_placeholder.setter
    def is_placeholder(self, is_true):
        self._is_placeholder = is_true

        if is_true:
            self._text_colour = self._placeholder_colour
        else:
            self._text_colour = self._text_colour_copy
    
    @property
    def _size(self):
        return (self._relative_size[0] * self._screen_size[1], self._relative_size[1] * self._screen_size[1])

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
    
    def calculate_font_size(self):
        bounding_box_height = self._size[1] - self._margin
        test_size = 1
        while True:
            glyph_metrics = self._font.get_metrics('j', size=test_size)
            descender = self._font.get_sized_descender(test_size)
            test_height = abs(glyph_metrics[0][3] - glyph_metrics[0][2]) - descender
            if test_height > bounding_box_height:
                return (test_size - 1) / self._screen_size[1]

            test_size += 1

    def calculate_cursor_size(self):
        cursor_height = (self._size[1] - self._border_width * 2) * 0.75
        return (cursor_height * 0.1, cursor_height)

    def calculate_cursor_position(self):
        current_width = (self._margin / 2)
        cursor_size = self.calculate_cursor_size()
        for index, metrics in enumerate(self._font.get_metrics(self._text, size=self._font_size)):
            if index == self._cursor_index:
                return (current_width - cursor_size[0], (self._size[1] - cursor_size[1]) / 2)
            
            glyph_width = metrics[4]
            current_width += glyph_width
        return (current_width - cursor_size[0], (self._size[1] - cursor_size[1]) / 2)
    
    def relative_x_to_cursor_index(self, relative_x):
        current_width = 0

        for index, metrics in enumerate(self._font.get_metrics(self._text, size=self._font_size)):
            glyph_width = metrics[4]

            if relative_x <= current_width:
                return index
            
            current_width += glyph_width
        
        return len(self._text)
    
    def set_text(self, new_text):
        self._text = new_text
    
    def get_text(self):
        if self.is_placeholder:
            return ''

        return self._text
    
    def set_cursor_index(self, mouse_pos):
        if mouse_pos is None:
            self._cursor_index = mouse_pos
            return

        relative_x = mouse_pos[0] - (self._margin / 2) - self._position[0]
        relative_x = max(0, relative_x)
        self._cursor_index = self.relative_x_to_cursor_index(relative_x)
    
    def focus_input(self, mouse_pos):
        if self.is_placeholder:
            self.set_text('')
            self.is_placeholder = False

        self.set_cursor_index(mouse_pos)
        self.set_image()
    
    def unfocus_input(self):
        if self._text == '':
            self.set_text(self._placeholder_text)
            self.is_placeholder = True

        self.set_cursor_index(None)
        self.set_image()
    
    def process_event(self, event):
        previous_state = self.get_widget_state()
        super().process_event(event)
        current_state = self.get_widget_state()
        
        match event.type:
            case pygame.MOUSEBUTTONUP:
                if previous_state == WidgetState.PRESS:
                    self.focus_input(event.pos)
                if current_state == WidgetState.BASE and self._cursor_index is not None:
                    self.unfocus_input()
                    return CustomEvent(self._event_type, text=self.get_text())
            
            case pygame.KEYDOWN:
                if self._cursor_index is None:
                    return

                if event.mod & (pygame.KMOD_CTRL):
                    if event.key == pygame.K_c:
                            print('COPIED')
                    
                    elif event.key == pygame.K_v:
                        pasted_text = pyperclip.paste()
                        pasted_text = ''.join(char for char in pasted_text if 32 <= ord(char) <= 127)
                        self._text = self._text[:self._cursor_index] + pasted_text + self._text[self._cursor_index:]
                        self._cursor_index += len(pasted_text)
                    self.set_image()
                    self.set_geometry()
                    
                    return
                
                match event.key:
                    case pygame.K_BACKSPACE:
                        if self._cursor_index > 0:
                            self._text = self._text[:self._cursor_index - 1] + self._text[self._cursor_index:]
                        self._cursor_index = max(0, self._cursor_index - 1)
                    
                    case pygame.K_RIGHT:
                        self._cursor_index = min(len(self._text), self._cursor_index + 1)
                    
                    case pygame.K_LEFT:
                        self._cursor_index = max(0, self._cursor_index - 1)
                    
                    case pygame.K_ESCAPE:
                        self.unfocus_input()
                        return CustomEvent(self._event_type, text=self.get_text())

                    case pygame.K_RETURN:
                        self.unfocus_input()
                    
                    case _:
                        if not event.unicode:
                            return
                        
                        potential_text = self._text[:self._cursor_index] + event.unicode + self._text[self._cursor_index:]
                        
                        if self._validator(potential_text) is False:
                            return
                        
                        self._text = potential_text
                        self._cursor_index += 1
                
                self._blinking_cooldown += 1
                animation.set_timer(500, lambda: self.subtract_blinking_cooldown(1))
                self.set_image()
                self.set_geometry()
    
    def subtract_blinking_cooldown(self, cooldown):
        self._blinking_cooldown = self._blinking_cooldown - cooldown
    
    def set_image(self):
        super().set_image()

        if self._cursor_index is not None:
            cursor_size = self.calculate_cursor_size()
            cursor_position = self.calculate_cursor_position()
            scaled_cursor = pygame.transform.scale(self._empty_cursor, cursor_size)
            scaled_cursor.fill(self._cursor_colour)
            self.image.blit(scaled_cursor, cursor_position)
    
    def update(self):
        super().update()
        cursor_frame = animation.calculate_frame_index(0, 2, self._blinking_fps)
        if cursor_frame == 1 and self._blinking_cooldown == 0:
            self._cursor_colour = (0, 0, 0, 0)
        else:
            self._cursor_colour = self._cursor_colour_copy
        self.set_image()