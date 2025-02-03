import pygame
from data.widgets.bases.widget import _Widget
from data.widgets.bases.pressable import _Pressable
from data.constants import WidgetState
from data.utils.data_helpers import get_user_settings
from data.utils.font_helpers import text_width_to_font_size, text_height_to_font_size
from data.assets import GRAPHICS, FONTS

user_settings = get_user_settings()

class Dropdown(_Pressable, _Widget):
    def __init__(self, word_list, event=None, **kwargs):
        _Pressable.__init__(
            self,
            event=event,
            hover_func=self.hover_func,
            down_func=lambda: self.set_state_colour(WidgetState.PRESS),
            up_func=self.up_func,
            play_sfx=False
        )
        _Widget.__init__(self, relative_size=None, **kwargs)

        if kwargs.get('relative_width'):
            self._relative_font_size = text_width_to_font_size(max(word_list, key=len), self._font, kwargs.get('relative_width') * self.surface_size[0] - self.margin) / self.surface_size[1]
        elif kwargs.get('relative_height'):
            self._relative_font_size = text_height_to_font_size(max(word_list, key=len), self._font, kwargs.get('relative_height') * self.surface_size[1] - self.margin) / self.surface_size[1]

        self._word_list = [word_list[0].capitalize()]
        self._word_list_copy = [word.capitalize() for word in word_list]

        self._expanded = False
        self._hovered_index = None

        self._empty_surface = pygame.Surface((0, 0))
        self._background_colour = self._fill_colour
        
        self.initialise_new_colours(self._fill_colour)
        self.set_state_colour(WidgetState.BASE)

        self.set_image()
        self.set_geometry()

    @property
    def size(self):
        max_word = sorted(self._word_list_copy, key=len)[-1]
        max_word_rect = self._font.get_rect(max_word, size=self.font_size)
        all_words_rect = pygame.FRect(0, 0, max_word_rect.size[0], (max_word_rect.size[1] * len(self._word_list)) + (self.margin * (len(self._word_list) - 1)))
        all_words_rect = all_words_rect.inflate(2 * self.margin, 2 * self.margin)
        return (all_words_rect.size[0] + max_word_rect.size[1], all_words_rect.size[1])

    def get_selected_word(self):
        return self._word_list[0].lower()
    
    def toggle_expanded(self):
        if self._expanded:
            self._word_list = [self._word_list_copy[0]]
        else:
            self._word_list = [*self._word_list_copy]
        
        self._expanded = not(self._expanded)

    def hover_func(self):
        mouse_position = pygame.mouse.get_pos()
        relative_position = (mouse_position[0] - self.position[0], mouse_position[1] - self.position[1])
        self._hovered_index = self.calculate_hovered_index(relative_position)
        self.set_state_colour(WidgetState.HOVER)
    
    def set_selected_word(self, word):
        index = self._word_list_copy.index(word.capitalize())
        selected_word = self._word_list_copy.pop(index)
        self._word_list_copy.insert(0, selected_word)

        if self._expanded:
            self._word_list.pop(index)
            self._word_list.insert(0, selected_word)
        else:
            self._word_list = [selected_word]
        
        self.set_image()

    def up_func(self):
        if self.get_widget_state() == WidgetState.PRESS:
            if self._expanded and self._hovered_index is not None:
                self.set_selected_word(self._word_list_copy[self._hovered_index])

            self.toggle_expanded()

        self._hovered_index = None

        self.set_state_colour(WidgetState.BASE)
        self.set_geometry()
    
    def calculate_hovered_index(self, mouse_pos):
        return int(mouse_pos[1] // (self.size[1] / len(self._word_list)))

    def set_image(self):
        text_surface = pygame.transform.scale(self._empty_surface, self.size)
        self.image = text_surface

        fill_rect = pygame.FRect(0, 0, self.size[0], self.size[1])
        pygame.draw.rect(self.image, self._background_colour, fill_rect)
        pygame.draw.rect(self.image, self._border_colour, fill_rect, width=int(self.border_width))

        word_box_height = (self.size[1] - (2 * self.margin) - ((len(self._word_list) - 1) * self.margin)) / len(self._word_list)

        arrow_size = (GRAPHICS['dropdown_arrow_open'].width / GRAPHICS['dropdown_arrow_open'].height * word_box_height, word_box_height)
        open_arrow_surface = pygame.transform.scale(GRAPHICS['dropdown_arrow_open'], arrow_size)
        closed_arrow_surface = pygame.transform.scale(GRAPHICS['dropdown_arrow_close'], arrow_size)
        arrow_position = (self.size[0] - arrow_size[0] - self.margin, (word_box_height) / 3)

        if self._expanded:
            self.image.blit(closed_arrow_surface, arrow_position)
        else:
            self.image.blit(open_arrow_surface, arrow_position)

        for index, word in enumerate(self._word_list):
            word_position = (self.margin, self.margin + (word_box_height + self.margin) * index)
            self._font.render_to(self.image, word_position, word, fgcolor=self._text_colour, size=self.font_size)
        
        if self._hovered_index is not None:
            overlay_surface = pygame.Surface((self.size[0], word_box_height + 2 * self.margin), pygame.SRCALPHA)
            overlay_surface.fill((*self._fill_colour.rgb, 128))
            overlay_position = (0, (word_box_height + self.margin) * self._hovered_index)
            self.image.blit(overlay_surface, overlay_position)