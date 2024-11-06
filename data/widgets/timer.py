from data.widgets.text import Text

class Timer(Text):
    def __init__(self, start_mins, **kwargs):
        super().__init__(text=self.format_mins(start_mins), **kwargs)
    
    def update_time(self):
        self._text = 'something'

    def format_mins(self, raw_minutes):
        raw_minutes = f'{round(float(raw_minutes), 2):.2f}'
        parsed_time = str(raw_minutes).split('.')
        seconds = 60 * (int(parsed_time[1]) / (10 ** len(parsed_time[1])))
        minutes, seconds = parsed_time[0], str(int(seconds)).zfill(2)
        return f'{minutes}:{seconds}'