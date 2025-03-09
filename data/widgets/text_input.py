import pyperclip
import pygame
from data.utils.constants import WidgetState, INPUT_COLOURS
from data.components.custom_event import CustomEvent
from data.widgets.bases.pressable import _Pressable
from data.managers.logs import initialise_logger
from data.managers.animation import animation
from data.widgets.bases.box import _Box
from data.utils.enums import CursorMode
from data.managers.cursor import cursor
from data.managers.theme import theme
from data.widgets.text import Text

logger = initialise_logger(__name__)

class TextInput(_Box, _Pressable, Text):
    def __init__(self, event, blinking_interval=530, validator=(lambda x: True), default='', placeholder='PLACEHOLDER TEXT', placeholder_colour=(200, 200, 200), cursor_colour=theme['textSecondary'], **kwargs):
        self._cursor_index = None
        # Multiple inheritance used here, adding the functionality of pressing, and custom box colours, to the text widget
        _Box.__init__(self, box_colours=INPUT_COLOURS)
        _Pressable.__init__(
            self,
            event=None,
            hover_func=lambda: self.set_state_colour(WidgetState.HOVER),
            down_func=lambda: self.set_state_colour(WidgetState.PRESS),
            up_func=lambda: self.set_state_colour(WidgetState.BASE),
            sfx=None
        )
        Text.__init__(self, text="", center=False, box_colours=INPUT_COLOURS[WidgetState.BASE], **kwargs)

        self.initialise_new_colours(self._fill_colour)
        self.set_state_colour(WidgetState.BASE)

        pygame.key.set_repeat(500, 50)

        self._blinking_fps = 1000 / blinking_interval
        self._cursor_colour = cursor_colour
        self._cursor_colour_copy = cursor_colour
        self._placeholder_colour = placeholder_colour
        self._text_colour_copy = self._text_colour

        self._placeholder_text = placeholder
        self._is_placeholder = None
        if default:
            self._text = default
            self.is_placeholder = False
        else:
            self._text = self._placeholder_text
            self.is_placeholder = True

        self._event = event
        self._validator = validator
        self._blinking_cooldown = 0

        self._empty_cursor = pygame.Surface((0, 0), pygame.SRCALPHA)

        self.resize_text()
        self.set_image()
        self.set_geometry()

    @property
    # Encapsulated getter method
    def is_placeholder(self):
        return self._is_placeholder

    @is_placeholder.setter
    # Encapsulated setter method, used to replace text colour if placeholder text is shown
    def is_placeholder(self, is_true):
        self._is_placeholder = is_true

        if is_true:
            self._text_colour = self._placeholder_colour
        else:
            self._text_colour = self._text_colour_copy

    @property
    def cursor_size(self):
        cursor_height = (self.size[1] - self.border_width * 2) * 0.75
        return (cursor_height * 0.1, cursor_height)

    @property
    def cursor_position(self):
        current_width = (self.margin / 2)
        for index, metrics in enumerate(self._font.get_metrics(self._text, size=self.font_size)):
            if index == self._cursor_index:
                return (current_width - self.cursor_size[0], (self.size[1] - self.cursor_size[1]) / 2)

            glyph_width = metrics[4]
            current_width += glyph_width
        return (current_width - self.cursor_size[0], (self.size[1] - self.cursor_size[1]) / 2)

    @property
    def text(self):
        if self.is_placeholder:
            return ''

        return self._text

    def relative_x_to_cursor_index(self, relative_x):
        """
        Calculates cursor index using mouse position relative to the widget position.

        Args:
            relative_x (int): Horizontal distance of the mouse from the left side of the widget.

        Returns:
            int: Cursor index.
        """
        current_width = 0

        for index, metrics in enumerate(self._font.get_metrics(self._text, size=self.font_size)):
            glyph_width = metrics[4]

            if current_width >= relative_x:
                return index

            current_width += glyph_width

        return len(self._text)

    def set_cursor_index(self, mouse_pos):
        """
        Sets cursor index based on mouse position.

        Args:
            mouse_pos (list[int, int]): Mouse position relative to window screen.
        """
        if mouse_pos is None:
            self._cursor_index = mouse_pos
            return

        relative_x = mouse_pos[0] - (self.margin / 2) - self.rect.left
        relative_x = max(0, relative_x)
        self._cursor_index = self.relative_x_to_cursor_index(relative_x)

    def focus_input(self, mouse_pos):
        """
        Draws cursor and sets cursor index when user clicks on widget.

        Args:
            mouse_pos (list[int, int]): Mouse position relative to window screen.
        """
        if self.is_placeholder:
            self._text = ''
            self.is_placeholder = False

        self.set_cursor_index(mouse_pos)
        self.set_image()
        cursor.set_mode(CursorMode.IBEAM)

    def unfocus_input(self):
        """
        Removes cursor when user unselects widget.
        """
        if self._text == '':
            self._text = self._placeholder_text
            self.is_placeholder = True
            self.resize_text()

        self.set_cursor_index(None)
        self.set_image()
        cursor.set_mode(CursorMode.ARROW)

    def set_text(self, new_text):
        """
        Called by a state object to change the widget text externally.

        Args:
            new_text (str): New text to display.

        Returns:
            CustomEvent: Object containing the new text to alert state of a text update.
        """
        super().set_text(new_text)
        return CustomEvent(**vars(self._event), text=self.text)

    def process_event(self, event):
        """
        Processes Pygame events.

        Args:
            event (pygame.Event): Event to process.

        Returns:
            CustomEvent: Object containing the new text to alert state of a text update.
        """
        previous_state = self.get_widget_state()
        super().process_event(event)
        current_state = self.get_widget_state()

        match event.type:
            case pygame.MOUSEMOTION:
                if self._cursor_index is None:
                    return

                # If mouse is hovering over widget, turn mouse cursor into an I-beam
                if self.rect.collidepoint(event.pos):
                    if cursor.get_mode() != CursorMode.IBEAM:
                        cursor.set_mode(CursorMode.IBEAM)
                else:
                    if cursor.get_mode() == CursorMode.IBEAM:
                        cursor.set_mode(CursorMode.ARROW)

                return

            case pygame.MOUSEBUTTONUP:
                # When user selects widget
                if previous_state == WidgetState.PRESS:
                    self.focus_input(event.pos)
                # When user unselects widget
                if current_state == WidgetState.BASE and self._cursor_index is not None:
                    self.unfocus_input()
                    return CustomEvent(**vars(self._event), text=self.text)

            case pygame.KEYDOWN:
                if self._cursor_index is None:
                    return

                # Handling Ctrl-C and Ctrl-V shortcuts
                if event.mod & (pygame.KMOD_CTRL):
                    if event.key == pygame.K_c:
                        pyperclip.copy(self.text)
                        logger.info(f'COPIED {self.text}')

                    elif event.key == pygame.K_v:
                        pasted_text = pyperclip.paste()
                        pasted_text = ''.join(char for char in pasted_text if 32 <= ord(char) <= 127)
                        self._text = self._text[:self._cursor_index] + pasted_text + self._text[self._cursor_index:]
                        self._cursor_index += len(pasted_text)

                    elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                        self._text = ''
                        self._cursor_index = 0

                    self.resize_text()
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
                        return CustomEvent(**vars(self._event), text=self.text)

                    case pygame.K_RETURN:
                        self.unfocus_input()
                        return CustomEvent(**vars(self._event), text=self.text)

                    case _:
                        if not event.unicode:
                            return

                        potential_text = self._text[:self._cursor_index] + event.unicode + self._text[self._cursor_index:]

                        # Validator lambda function used to check if inputted text is valid before displaying
                        # e.g. Time control input has a validator function checking if text represents a float
                        if self._validator(potential_text) is False:
                            return

                        self._text = potential_text
                        self._cursor_index += 1

                self._blinking_cooldown += 1
                animation.set_timer(500, lambda: self.subtract_blinking_cooldown(1))

                self.resize_text()
                self.set_image()
                self.set_geometry()

    def subtract_blinking_cooldown(self, cooldown):
        """
        Subtracts blinking cooldown after certain timeframe. When blinking_cooldown is 1, cursor is able to be drawn.

        Args:
            cooldown (float): Duration before cursor can no longer be drawn.
        """
        self._blinking_cooldown = self._blinking_cooldown - cooldown

    def set_image(self):
        """
        Draws text input widget to image.
        """
        super().set_image()

        if self._cursor_index is not None:
            scaled_cursor = pygame.transform.scale(self._empty_cursor, self.cursor_size)
            scaled_cursor.fill(self._cursor_colour)
            self.image.blit(scaled_cursor, self.cursor_position)

    def update(self):
        """
        Overrides based update method, to handle cursor blinking.
        """
        super().update()
        # Calculate if cursor should be shown or not
        cursor_frame = animation.calculate_frame_index(0, 2, self._blinking_fps)
        if cursor_frame == 1 and self._blinking_cooldown == 0:
            self._cursor_colour = (0, 0, 0, 0)
        else:
            self._cursor_colour = self._cursor_colour_copy
        self.set_image()