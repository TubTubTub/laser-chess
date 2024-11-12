from data.widgets.text import Text
from data.components.animation import animation

class Timer(Text):
    def __init__(self, active_colour, event_type, start_mins=60, **kwargs):
        self._current_ms = float(start_mins) * 60 * 1000
        self._active = False
        self._times_out_callback = None
        self._active_colour = active_colour
        self._event_type = event_type
        super().__init__(text=self.format_to_text(), **kwargs)
    
    def register_end_callback(self, callback):
        self._times_out_callback = callback
    
    def get_active(self):
        return self._active
    
    def set_active(self, is_active):
        self._active = is_active
        if self._active:
            animation.set_timer(1000, self.decrement_second)
    
    def set_time(self, milliseconds):
        self._current_ms = milliseconds
        self._text = self.format_to_text()
        self.set_image()
        self.set_geometry()
    
    def reset_time(self):
        self._text = self.format_to_text()
    
    def decrement_second(self):
        if self._active:
            self.set_time(self._current_ms - 1000)

            if self._current_ms <= 0:
                self.set_time(0)
                self._times_out_callback()
            else:
                animation.set_timer(1000, self.decrement_second)

    def format_to_text(self):
        raw_seconds = self._current_ms / 1000
        minutes, seconds = divmod(raw_seconds, 60)
        return f'{str(int(minutes)).zfill(2)}:{str(int(seconds)).zfill(2)}'

    def process_event(self, event):
        pass