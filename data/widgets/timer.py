import pygame
from data.constants import WidgetState, Colour, BLUE_BUTTON_COLOURS, RED_BUTTON_COLOURS
from data.components.custom_event import CustomEvent
from data.managers.animation import animation
from data.widgets.text import Text

class Timer(Text):
    def __init__(self, active_colour, event=None, start_mins=60, **kwargs):
        box_colours = BLUE_BUTTON_COLOURS[WidgetState.BASE] if active_colour == Colour.BLUE else RED_BUTTON_COLOURS[WidgetState.BASE]
        
        self._current_ms = float(start_mins) * 60 * 1000
        self._active_colour = active_colour
        self._active = False
        self._timer_running = False
        self._event = event

        super().__init__(text=self.format_to_text(), fit_vertical=False, box_colours=box_colours, **kwargs)
    
    def set_active(self, is_active):
        if self._active == is_active:
            return

        if is_active and self._timer_running is False:
            self._timer_running = True
            animation.set_timer(1000, self.decrement_second)

        self._active = is_active
    
    def set_time(self, milliseconds):
        self._current_ms = milliseconds
        self._text = self.format_to_text()
        self.set_image()
        self.set_geometry()
    
    def get_time(self):
        return self._current_ms / (1000 * 60)
    
    def decrement_second(self):
        if self._active:
            self.set_time(self._current_ms - 1000)

            if self._current_ms <= 0:
                self._active = False
                self._timer_running = False
                self.set_time(0)
                pygame.event.post(pygame.event.Event(pygame.MOUSEMOTION, pos=pygame.mouse.get_pos())) # RANDOM EVENT TO TRIGGER process_event
            else:
                animation.set_timer(1000, self.decrement_second)
        else:
            self._timer_running = False

    def format_to_text(self):
        raw_seconds = self._current_ms / 1000
        minutes, seconds = divmod(raw_seconds, 60)
        return f'{str(int(minutes)).zfill(2)}:{str(int(seconds)).zfill(2)}'

    def process_event(self, event):
        if self._current_ms <= 0:
            return CustomEvent(**vars(self._event), active_colour=self._active_colour)