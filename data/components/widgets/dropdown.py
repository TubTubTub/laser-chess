import pygame
from data.components.widgets.bases import _Widget, _Pressable
from data.constants import WidgetState
from data.utils.settings_helpers import get_user_settings
from data.tools import GRAPHICS

user_settings = get_user_settings()

class Dropdown(_Pressable, _Widget):
    def __init__(self, relative_position, word_list, font_size, fill_colour, event=None, text_colour=(0, 0, 0), border_colour=(255, 255, 255), border_width=4, margin=15):
        _Pressable.__init__(
            self,
            event=event,
            hover_func=lambda: self.hover_func(),
            down_func=lambda: self.set_state_colour(WidgetState.PRESS),
            up_func=lambda: self.up_func(),
        )
        _Widget.__init__(self)

        self._screen_size = pygame.display.get_surface().get_size()

        self._relative_position = relative_position
        self._relative_font_size = font_size / self._screen_size[1]
        self._relative_border_width = border_width / self._screen_size[1]
        self._relative_margin = margin / self._screen_size[1]

        self._font = pygame.freetype.Font(user_settings['primaryFont'])
        self._text_colour = text_colour
        self._word_list = [word_list[0]]
        self._word_list_copy = word_list

        self._fill_colour = fill_colour

        self._expanded = False
        self._hovered_index = None

        self._empty_surface = pygame.Surface((0, 0))
    
        self._border_colour = border_colour
        self._overlay_colour = None
        self.initialise_new_colours((255, 255, 255))

        self.set_image()
        self.set_geometry()

    @property
    def _position(self):
        return (self._relative_position[0] * self._screen_size[0], self._relative_position[1] * self._screen_size[1])

    @property
    def _size(self):
        max_word = sorted(self._word_list_copy, key=len)[-1]
        max_word_rect = self._font.get_rect(max_word, size=self._font_size)
        all_words_rect = pygame.Rect(0, 0, max_word_rect.size[0], (max_word_rect.size[1] * len(self._word_list)) + (self._margin * (len(self._word_list) - 1)))
        all_words_rect = all_words_rect.inflate(2 * self._margin, 2 * self._margin)
        return (all_words_rect.size[0] + max_word_rect.size[1], all_words_rect.size[1])

    @property
    def _font_size(self):
        return self._relative_font_size * self._screen_size[1]

    @property
    def _margin(self):
        return self._relative_margin * self._screen_size[1]

    @property
    def _border_width(self):
        return self._relative_border_width * self._screen_size[1]

    def get_selected_word(self):
        if self._expanded is False:
            return self._word_list[0]
        
        return None
    
    def toggle_expanded(self):
        if self._expanded:
            self._word_list = [self._word_list_copy[0]]
        else:
            self._word_list = [*self._word_list_copy]
        
        self._expanded = not(self._expanded)

    def hover_func(self):
        mouse_position = pygame.mouse.get_pos()
        relative_position = (mouse_position[0] - self._position[0], mouse_position[1] - self._position[1])
        self._hovered_index = self.calculate_hovered_index(relative_position)
        self.set_state_colour(WidgetState.HOVER)
    
    def set_selected_word(self, index):
        selected_word = self._word_list_copy.pop(index)
        self._word_list_copy.insert(0, selected_word)

        if self._expanded:
            self._word_list.pop(index)
            self._word_list.insert(0, selected_word)
        else:
            self._word_list = [selected_word]

    def up_func(self):
        if self.get_widget_state() == WidgetState.PRESS:
            if self._expanded and self._hovered_index is not None:
                self.set_selected_word(self._hovered_index)

            self.toggle_expanded()

        self._hovered_index = None

        self.set_state_colour(WidgetState.BASE)
        self.set_geometry()
    
    def initialise_new_colours(self, new_colour):
        r, g, b = pygame.Color(new_colour).rgb

        self._colours = {
            WidgetState.BASE: new_colour,
            WidgetState.HOVER: (max(r - 25, 0), max(g - 25, 0), max(b - 25, 0)),
            WidgetState.PRESS: (max(r - 50, 0), max(g - 50, 0), max(b - 50, 0))
        }

        self.set_state_colour(WidgetState.BASE)
    
    def set_state_colour(self, state):
        self._overlay_colour = self._colours[state]

        self.set_image()
    
    def calculate_hovered_index(self, mouse_pos):
        return int(mouse_pos[1] // (self._size[1] / len(self._word_list)))

    def set_image(self):
        text_surface = pygame.transform.scale(self._empty_surface, self._size)
        self.image = text_surface

        fill_rect = pygame.Rect(0, 0, self._size[0], self._size[1])
        pygame.draw.rect(self.image, self._fill_colour, fill_rect)
        pygame.draw.rect(self.image, self._border_colour, fill_rect, width=int(self._border_width))

        word_box_height = (self._size[1] - (2 * self._margin) - ((len(self._word_list) - 1) * self._margin)) / len(self._word_list)

        arrow_surface = pygame.transform.scale(GRAPHICS['dropdown_arrow'], (word_box_height, word_box_height))
        arrow_position = (self._size[0] - word_box_height - self._margin * 0.5, word_box_height)
        if self._expanded:
            self.image.blit(pygame.transform.rotate(arrow_surface, 180), arrow_position)
        else:
            self.image.blit(arrow_surface, arrow_position)

        for index, word in enumerate(self._word_list):
            word_position = (self._margin, self._margin + (word_box_height + self._margin) * index)
            self._font.render_to(self.image, word_position, word, fgcolor=self._text_colour, size=self._font_size)
        
        if self._hovered_index is not None:
            overlay_surface = pygame.Surface((self._size[0], word_box_height + 2 * self._margin), pygame.SRCALPHA)
            overlay_surface.fill((*self._overlay_colour, 128))
            overlay_position = (0, (word_box_height + self._margin) * self._hovered_index)
            self.image.blit(overlay_surface, overlay_position)
    
    def set_geometry(self):
        self.rect = self.image.get_rect()
        self.rect.topleft = self._position

    def set_screen_size(self, new_screen_size):
        self._screen_size = new_screen_size