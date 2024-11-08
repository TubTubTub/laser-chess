from data.widgets.text import Text
from data.components.animation import animation
from data.components.custom_event import CustomEvent

class Timer(Text):
    def __init__(self, start_mins, active_colour, event_type, **kwargs):
        self._current_ms = float(start_mins) * 60 * 1000
        self._active = False
        self._active_colour = active_colour
        self._event_type = event_type
        super().__init__(text=self.format_to_text(), **kwargs)
        animation.set_timer(1000, self.decrement_second)
    
    def set_active(self, is_active):
        self._active = is_active
        if self._active:
            animation.set_timer(1000, self.decrement_second)
    
    def reset_time(self):
        self._text = self.format_to_text()
    
    def update_time(self):
        self._text = 'something'
    
    def decrement_second(self):
        if self._active:
            self._current_ms = self._current_ms - 1000
            self._text = self.format_to_text()
            self.set_image()
            self.set_geometry()

            animation.set_timer(1000, self.decrement_second)

    def format_to_text(self):
        raw_seconds = self._current_ms / 1000
        minutes, seconds = divmod(raw_seconds, 60)
        return f'{str(int(minutes)).zfill(2)}:{str(int(seconds)).zfill(2)}'

    def process_event(self, event):
        if self._current_ms == 0:
            return CustomEvent(self._event_type, active_colour=self._active_colour)